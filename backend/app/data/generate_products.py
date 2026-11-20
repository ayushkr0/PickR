"""
Generate a large, realistic product catalog using Claude.

Run with: python -m app.data.generate_products
Options:
  --per-category N   Products per category (default: 200)
  --force            Clear existing products first
  --skip-pinecone    Only populate DB, skip Pinecone sync
"""

import asyncio
import json
import sys
import time
import uuid

from anthropic import Anthropic
from sqlalchemy import text

from app.core.config import settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.models.product import Product

CATEGORIES = {
    "laptop": {
        "spec_fields": "chip, ram, storage, display, battery_hours (number), weight_lbs (number), os, gpu (if applicable)",
        "brands": "Apple, Dell, HP, Lenovo, ASUS, Acer, MSI, Razer, Samsung, Microsoft, LG, Huawei, Gigabyte, Framework, Toshiba/Dynabook",
        "price_ranges": [
            ("budget (£200-£500)", 8),
            ("mid-range (£500-£900)", 10),
            ("upper mid-range (£900-£1300)", 8),
            ("premium (£1300-£2000)", 7),
            ("high-end (£2000-£3500)", 5),
        ],
        "use_cases": "student, business/professional, gaming, creative/content creation, everyday/general, lightweight travel, programming/developer, budget, 2-in-1 convertible",
    },
    "headphone": {
        "spec_fields": "type (over-ear/on-ear/in-ear/earbuds), driver_size, connectivity (wired/wireless/both), battery_hours (number, if wireless), noise_cancelling (boolean), weight_grams (number), microphone (boolean), water_resistance (e.g. IPX4)",
        "brands": "Sony, Apple, Bose, Sennheiser, Audio-Technica, Beyerdynamic, JBL, Samsung, Jabra, AKG, Shure, Bang & Olufsen, Beats, Skullcandy, Anker/Soundcore, 1MORE, Focal, HiFiMAN",
        "price_ranges": [
            ("budget (£20-£60)", 8),
            ("mid-range (£60-£150)", 10),
            ("upper mid-range (£150-£300)", 8),
            ("premium (£300-£500)", 7),
            ("audiophile/high-end (£500-£1500)", 5),
        ],
        "use_cases": "music listening, gaming, commuting, working from home, studio/professional, running/sports, audiophile, budget, office calls",
    },
    "camera": {
        "spec_fields": "type (mirrorless/DSLR/compact/action/instant), sensor_size, megapixels (number), video_max (e.g. 4K60), lens_mount (if interchangeable), weight_grams (number), viewfinder (electronic/optical/none), stabilization (in-body/lens/digital/none)",
        "brands": "Sony, Canon, Nikon, Fujifilm, Panasonic, GoPro, DJI, Olympus/OM System, Leica, Ricoh, Insta360, Hasselblad, Sigma",
        "price_ranges": [
            ("budget (£100-£400)", 8),
            ("mid-range (£400-£800)", 10),
            ("upper mid-range (£800-£1300)", 8),
            ("premium (£1300-£2000)", 7),
            ("professional/high-end (£2000-£4000)", 5),
        ],
        "use_cases": "beginner/first camera, vlogging/YouTube, travel, street photography, portrait, landscape, sports/action, professional/commercial, filmmaking, casual/family",
    },
}

GENERATION_PROMPT = """\
Generate exactly {count} real {category} products as a JSON array. These must be REAL products \
that actually exist on the market (current or recent models from 2022-2025).

Requirements:
- Each product must be a real, identifiable product (real brand, real model name)
- Price in GBP (£) — use realistic UK market prices for the {price_range} range
- Distribute across these brands (not all from one): {brands}
- Cover various use cases: {use_cases}
- Each product needs:
  - "name": full product name with model/year
  - "brand": brand name
  - "price": number in GBP
  - "specs": object with fields: {spec_fields}
  - "summary": one compelling sentence pitch (max 20 words)
  - "pros": array of 3 strings (specific, not generic)
  - "cons": array of 3 strings (honest, specific drawbacks)
  - "searchable_text": 30-50 words covering use cases, features, who it's for

CRITICAL:
- NO duplicate products (each must be a different model)
- Prices must be realistic GBP prices for the UK market
- Pros/cons must be specific to THAT product, not generic category statements
- Do NOT include any products from this exclusion list: {exclude}

Return ONLY the JSON array, no markdown fences, no explanation.
"""


def _client():
    return Anthropic(api_key=settings.anthropic_api_key)


def _extract_text(response) -> str:
    """Extract text from response, skipping ThinkingBlocks."""
    for block in response.content:
        if hasattr(block, "text"):
            return block.text.strip()
    return ""


def _parse_json_array(text: str) -> list[dict]:
    """Robustly extract a JSON array from model output."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    # Find the JSON array in the text
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return json.loads(text)


def generate_batch(
    category: str,
    price_range: str,
    count: int,
    exclude_names: list[str],
) -> list[dict]:
    cat_config = CATEGORIES[category]
    exclude_str = ", ".join(exclude_names[-60:]) if exclude_names else "none"

    prompt = GENERATION_PROMPT.format(
        count=count,
        category=category,
        price_range=price_range,
        brands=cat_config["brands"],
        use_cases=cat_config["use_cases"],
        spec_fields=cat_config["spec_fields"],
        exclude=exclude_str,
    )

    client = _client()
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = client.messages.create(
                model="claude-haiku-5-5",
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt if attempt == 0 else prompt + "\n\nIMPORTANT: Return ONLY a raw JSON array. No markdown, no explanation. Start with [ and end with ]."}],
            )
            text = _extract_text(response)
            if not text:
                raise ValueError("Empty response from model")
            products = _parse_json_array(text)
            break
        except (json.JSONDecodeError, ValueError) as e:
            if attempt < max_attempts - 1:
                print(f"[retry {attempt+1}] ", end="", flush=True)
                continue
            raise

    for p in products:
        p["category"] = category
        if "brand" not in p:
            p["brand"] = p["name"].split()[0]

    return products


def generate_all_products(per_category: int = 200) -> list[dict]:
    all_products = []

    for category, config in CATEGORIES.items():
        print(f"\n{'='*60}")
        print(f"Generating {per_category} {category} products...")
        print(f"{'='*60}")

        category_products = []
        exclude_names = []

        total_weight = sum(w for _, w in config["price_ranges"])
        for price_range, weight in config["price_ranges"]:
            batch_count = max(3, round(per_category * weight / total_weight))
            remaining = batch_count
            while remaining > 0:
                chunk = min(remaining, 5)
                print(f"  Generating {chunk} {price_range} {category}s... ", end="", flush=True)
                try:
                    batch = generate_batch(category, price_range, chunk, exclude_names)
                    # Deduplicate
                    new = [p for p in batch if p["name"] not in exclude_names]
                    category_products.extend(new)
                    exclude_names.extend(p["name"] for p in new)
                    print(f"got {len(new)}")
                except Exception as e:
                    print(f"ERROR: {e}")
                remaining -= chunk
                time.sleep(0.5)

        print(f"\n  Total {category}: {len(category_products)} products")
        all_products.extend(category_products)

    print(f"\n{'='*60}")
    print(f"Total products generated: {len(all_products)}")
    return all_products


async def save_to_db(products: list[dict], force: bool = False):
    if engine is None:
        print("DATABASE_URL not set — skipping DB save.")
        return []

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        if force:
            await session.execute(text("DELETE FROM products"))
            await session.commit()
            print("Cleared existing products from DB")

        db_products = []
        for p in products:
            product = Product(
                id=str(uuid.uuid4()),
                name=p["name"],
                category=p["category"],
                brand=p["brand"],
                price=float(p["price"]),
                image_url=p.get("image_url"),
                affiliate_url=p.get("affiliate_url"),
                specs=p.get("specs", {}),
                summary=p.get("summary", ""),
                pros=p.get("pros", []),
                cons=p.get("cons", []),
            )
            session.add(product)
            db_products.append(product)

        await session.commit()
        print(f"Saved {len(db_products)} products to Postgres")
        return db_products


async def sync_pinecone(db_products: list):
    if not settings.pinecone_api_key:
        print("PINECONE_API_KEY not set — skipping Pinecone sync.")
        return

    from app.services.vector_store import get_or_create_index, upsert_products

    index = get_or_create_index()
    index.delete(delete_all=True)
    print("Cleared Pinecone index")

    products_for_pinecone = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "brand": p.brand,
            "price": p.price,
            "summary": p.summary or "",
            "specs": p.specs or {},
            "pros": p.pros or [],
            "cons": p.cons or [],
        }
        for p in db_products
    ]

    count = upsert_products(products_for_pinecone)
    print(f"Upserted {count} products to Pinecone")


async def main():
    per_category = 200
    force = "--force" in sys.argv
    skip_pinecone = "--skip-pinecone" in sys.argv

    for arg in sys.argv:
        if arg.startswith("--per-category"):
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                per_category = int(sys.argv[idx + 1])

    print(f"Generating {per_category} products per category ({per_category * 3} total)")
    print(f"Force: {force}, Skip Pinecone: {skip_pinecone}")

    products = generate_all_products(per_category=per_category)

    # Save generated data to a JSON backup
    backup_path = "app/data/generated_products.json"
    with open(backup_path, "w") as f:
        json.dump(products, f, indent=2)
    print(f"\nBackup saved to {backup_path}")

    db_products = await save_to_db(products, force=force)

    if not skip_pinecone and db_products:
        await sync_pinecone(db_products)

    print("\nDone! Summary:")
    from collections import Counter
    cats = Counter(p["category"] for p in products)
    for cat, count in cats.items():
        prices = [p["price"] for p in products if p["category"] == cat]
        print(f"  {cat}: {count} products (£{min(prices):.0f} - £{max(prices):.0f})")


if __name__ == "__main__":
    asyncio.run(main())
