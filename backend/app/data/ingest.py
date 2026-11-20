"""
Run with: python -m app.data.ingest
Seeds the products table with MVP product data and upserts to Pinecone.

Use --force to delete existing products and reseed from scratch.
"""

import asyncio
import sys
import uuid

from sqlalchemy import text

from app.core.config import settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.data.seed_products import PRODUCTS
from app.models.product import Product


async def seed(force: bool = False):
    if engine is None:
        print("DATABASE_URL not set — skipping Postgres seed.")
        print("    Products available in memory only (seed_products.py).")
    else:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created")

        async with AsyncSessionLocal() as session:
            if force:
                await session.execute(text("DELETE FROM products"))
                await session.commit()
                print("Cleared existing products (--force)")

            result = await session.execute(text("SELECT COUNT(*) FROM products"))
            count = result.scalar()

            if count and count > 0 and not force:
                print(f"Already seeded ({count} products). Use --force to reseed.")
            else:
                for p in PRODUCTS:
                    product = Product(
                        id=str(uuid.uuid4()),
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
                print(f"Seeded {len(PRODUCTS)} products into Postgres")

    if settings.pinecone_api_key:
        from app.services.vector_store import get_or_create_index, upsert_products

        if force:
            index = get_or_create_index()
            index.delete(delete_all=True)
            print("Cleared Pinecone index")

        if engine is not None:
            async with AsyncSessionLocal() as session:
                from sqlalchemy import select

                from app.models.product import Product as ProductModel
                result = await session.execute(select(ProductModel))
                db_products = result.scalars().all()

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
        else:
            products_for_pinecone = [
                {
                    "id": str(uuid.uuid4()),
                    "name": p["name"],
                    "category": p["category"],
                    "brand": p["brand"],
                    "price": p["price"],
                    "summary": p.get("summary", ""),
                    "specs": p.get("specs", {}),
                    "pros": p.get("pros", []),
                    "cons": p.get("cons", []),
                }
                for p in PRODUCTS
            ]

        count = upsert_products(products_for_pinecone)
        print(f"Upserted {count} products to Pinecone")
    else:
        print("PINECONE_API_KEY not set — skipping Pinecone upsert.")

    print("\nProducts by category:")
    categories: dict[str, list[str]] = {}
    for p in PRODUCTS:
        categories.setdefault(p["category"], []).append(p["name"])
    for cat, names in categories.items():
        print(f"  {cat}: {len(names)} products")
        for name in names:
            print(f"    - {name}")


if __name__ == "__main__":
    force = "--force" in sys.argv
    asyncio.run(seed(force=force))
