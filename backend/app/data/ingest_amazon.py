"""
Ingest products from the Amazon Reviews 2023 HuggingFace dataset into Postgres + Pinecone.

Usage:
    python -m app.data.ingest_amazon --category laptop --limit 200
    python -m app.data.ingest_amazon --category headphone --limit 200
    python -m app.data.ingest_amazon --category camera --limit 200
    python -m app.data.ingest_amazon --all --limit 200
"""

import argparse
import asyncio
import re
import uuid

import pandas as pd
from sqlalchemy import text

from app.core.config import settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.models.product import Product
from app.services.vector_store import upsert_products

USD_TO_GBP = 0.79

CATEGORY_KEYWORDS = {
    "laptop": {
        "title_patterns": [
            r"\blaptop\b", r"\bnotebook\b", r"\bchromebook\b",
            r"\bmacbook\b", r"\bultrabook\b",
        ],
        "category_keywords": ["Laptops", "Laptop", "Notebook", "Chromebook", "Computers & Tablets"],
    },
    "headphone": {
        "title_patterns": [
            r"\bheadphone\b", r"\bearphone\b", r"\bearbuds?\b",
            r"\bheadset\b", r"\bin-ear\b", r"\bover-ear\b",
            r"\bon-ear\b", r"\bairpods?\b", r"\bbuds\b",
        ],
        "category_keywords": ["Headphones", "Earbuds", "In-Ear", "Over-Ear", "On-Ear", "Earphones"],
    },
    "camera": {
        "title_patterns": [
            r"\bcamera\b", r"\bdslr\b", r"\bmirrorless\b",
            r"\bcamcorder\b", r"\baction cam\b", r"\bgopro\b",
            r"\bdigital camera\b",
        ],
        "category_keywords": ["Camera", "Digital Cameras", "DSLR", "Mirrorless", "Point & Shoot", "Camcorders"],
    },
}

EXCLUDE_PATTERNS = [
    r"\bcase\b", r"\bcover\b", r"\bstand\b", r"\bmount\b",
    r"\bcharger\b", r"\bcable\b", r"\badapter\b", r"\bprotector\b",
    r"\btripod\b", r"\bstrap\b", r"\bbag\b", r"\bsleeve\b",
    r"\breplacement\b", r"\bfilter\b", r"\bhood\b", r"\bcleaning\b",
]


def _extract_price(price_val) -> float | None:
    if price_val is None or (isinstance(price_val, float) and pd.isna(price_val)):
        return None
    s = str(price_val).strip()
    match = re.search(r"[\d,]+\.?\d*", s.replace(",", ""))
    if not match:
        return None
    val = float(match.group())
    if val <= 0 or val > 10000:
        return None
    return round(val * USD_TO_GBP, 2)


def _extract_brand(title: str, store: str | None) -> str:
    if store and not pd.isna(store) and len(store) < 50:
        return store.strip()
    parts = title.split()
    if parts:
        return parts[0]
    return "Unknown"


def _matches_category(row, category: str) -> bool:
    cfg = CATEGORY_KEYWORDS[category]
    title = str(row.get("title", "")).lower()
    categories = row.get("categories", [])

    if isinstance(categories, str):
        categories = [categories]

    for pattern in cfg["title_patterns"]:
        if re.search(pattern, title, re.IGNORECASE):
            break
    else:
        cat_text = " ".join(str(c) for c in categories).lower()
        for kw in cfg["category_keywords"]:
            if kw.lower() in cat_text:
                break
        else:
            return False

    title_lower = title.lower()
    for excl in EXCLUDE_PATTERNS:
        if re.search(excl, title_lower):
            return False

    return True


def _build_specs(row, category: str) -> dict:
    details = row.get("details", {})
    if isinstance(details, str):
        try:
            import json
            details = json.loads(details)
        except (json.JSONDecodeError, TypeError):
            details = {}
    if not isinstance(details, dict):
        details = {}

    specs = {}
    for k, v in details.items():
        k_lower = k.lower()
        if any(x in k_lower for x in ["dimension", "weight", "battery", "screen", "display",
                                        "processor", "ram", "memory", "storage", "resolution",
                                        "connectivity", "driver", "impedance", "frequency",
                                        "sensor", "megapixel", "lens", "zoom", "iso"]):
            specs[k] = str(v)[:200]
        if len(specs) >= 8:
            break

    return specs


def _build_summary(row) -> str:
    title = str(row.get("title", ""))
    features = row.get("features", [])
    if isinstance(features, list) and features:
        return f"{title}. {features[0][:150]}" if features[0] else title
    desc = row.get("description", [])
    if isinstance(desc, list) and desc:
        first = str(desc[0])[:150]
        return f"{title}. {first}"
    return title


def _build_pros_cons(row) -> tuple[list[str], list[str]]:
    features = row.get("features", [])
    if not isinstance(features, list):
        features = []
    features = [str(f)[:100] for f in features if f and len(str(f)) > 10]

    pros = features[:4] if features else ["Popular product with good reviews"]
    cons = ["Check latest reviews for potential issues"]
    rating = row.get("average_rating", 0)
    if isinstance(rating, (int, float)) and rating < 4.0:
        cons.append("Mixed user reviews")

    return pros, cons


def load_and_filter(category: str, limit: int = 200) -> list[dict]:
    print(f"\nLoading Electronics metadata from HuggingFace...")
    shards = [
        f"hf://datasets/McAuley-Lab/Amazon-Reviews-2023/raw_meta_Electronics/full-0000{i}-of-00010.parquet"
        for i in range(10)
    ]

    products = []
    seen_titles = set()

    for shard_url in shards:
        if len(products) >= limit:
            break

        print(f"  Reading shard: ...{shard_url[-30:]}")
        try:
            df = pd.read_parquet(shard_url)
        except Exception as e:
            print(f"  Warning: Failed to load shard: {e}")
            continue

        for _, row in df.iterrows():
            if len(products) >= limit:
                break

            title = str(row.get("title", ""))
            if not title or len(title) < 10 or title in seen_titles:
                continue

            price = _extract_price(row.get("price"))
            if price is None:
                continue

            rating = row.get("average_rating", 0)
            if not isinstance(rating, (int, float)) or rating < 3.5:
                continue

            rating_count = row.get("rating_number", 0)
            if not isinstance(rating_count, (int, float)) or rating_count < 10:
                continue

            if not _matches_category(row, category):
                continue

            seen_titles.add(title)
            brand = _extract_brand(title, row.get("store"))
            specs = _build_specs(row, category)
            summary = _build_summary(row)
            pros, cons = _build_pros_cons(row)

            images = row.get("images", {})
            image_url = None
            if isinstance(images, dict):
                hi_res = images.get("hi_res", [])
                large = images.get("large", [])
                for img_list in [hi_res, large]:
                    if hasattr(img_list, '__iter__'):
                        for img in img_list:
                            if img and not pd.isna(img):
                                image_url = str(img)
                                break
                    if image_url:
                        break

            products.append({
                "id": str(uuid.uuid4()),
                "name": title[:255],
                "category": category,
                "brand": brand[:100],
                "price": price,
                "image_url": image_url,
                "affiliate_url": f"https://www.amazon.com/dp/{row.get('parent_asin', '')}",
                "specs": specs,
                "summary": summary[:500],
                "pros": pros,
                "cons": cons,
            })

    print(f"  Found {len(products)} {category} products")
    return products


async def ingest_to_postgres(products: list[dict]):
    if engine is None:
        print("  DATABASE_URL not set — skipping Postgres.")
        return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        for p in products:
            product = Product(
                id=p["id"],
                name=p["name"],
                category=p["category"],
                brand=p["brand"],
                price=p["price"],
                image_url=p.get("image_url"),
                affiliate_url=p.get("affiliate_url"),
                specs=p["specs"],
                summary=p["summary"],
                pros=p["pros"],
                cons=p["cons"],
            )
            session.add(product)

        await session.commit()
        print(f"  Inserted {len(products)} products into Postgres")


def ingest_to_pinecone(products: list[dict]):
    count = upsert_products(products, batch_size=50)
    print(f"  Upserted {count} vectors to Pinecone")


async def main():
    parser = argparse.ArgumentParser(description="Ingest Amazon products into PickR")
    parser.add_argument("--category", choices=["laptop", "headphone", "camera"])
    parser.add_argument("--all", action="store_true", help="Ingest all categories")
    parser.add_argument("--limit", type=int, default=200, help="Max products per category")
    parser.add_argument("--skip-pinecone", action="store_true", help="Skip Pinecone upsert")
    parser.add_argument("--skip-postgres", action="store_true", help="Skip Postgres insert")
    args = parser.parse_args()

    if not args.category and not args.all:
        parser.error("Specify --category or --all")

    categories = ["laptop", "headphone", "camera"] if args.all else [args.category]

    for cat in categories:
        print(f"\n{'='*50}")
        print(f"Ingesting: {cat} (limit={args.limit})")
        print(f"{'='*50}")

        products = load_and_filter(cat, limit=args.limit)

        if not products:
            print(f"  No {cat} products found. Skipping.")
            continue

        if not args.skip_postgres:
            await ingest_to_postgres(products)

        if not args.skip_pinecone:
            ingest_to_pinecone(products)

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
