from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# Engine is created lazily — only connects when DATABASE_URL is set
def get_engine():
    if not settings.database_url:
        return None
    # asyncpg driver for async postgres
    url = settings.database_url.strip().replace("postgresql://", "postgresql+asyncpg://")
    return create_async_engine(url, echo=False)


engine = get_engine()

AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = (
    async_sessionmaker(engine, expire_on_commit=False) if engine else None
)


async def get_db():
    if AsyncSessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured")
    async with AsyncSessionLocal() as session:
        yield session


async def get_products_by_ids(
    db: AsyncSession, product_ids: list[str]
) -> list:
    """Fetch Product rows by IDs, preserving the input order."""
    from app.models.product import Product

    if not product_ids:
        return []

    result = await db.execute(
        select(Product).where(Product.id.in_(product_ids))
    )
    rows = {p.id: p for p in result.scalars().all()}
    return [rows[pid] for pid in product_ids if pid in rows]
