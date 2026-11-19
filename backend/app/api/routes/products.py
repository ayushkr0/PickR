from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter()


@router.get("/products/{product_id}/price-context")
async def price_context(
    product_id: str,
    db: AsyncSession = Depends(get_db),
):
    product = (await db.execute(
        text("SELECT id, price, category FROM products WHERE id = :pid"),
        {"pid": product_id},
    )).first()
    if not product:
        raise HTTPException(404, "Product not found")

    stats = (await db.execute(
        text("""
            SELECT AVG(price) as avg_price, MIN(price) as min_price, MAX(price) as max_price, COUNT(*) as total
            FROM products
            WHERE category = :cat
        """),
        {"cat": product.category},
    )).first()

    if not stats or not stats.total:
        return {"price": product.price, "category_avg": product.price, "category_min": product.price, "category_max": product.price, "percentile": 50, "verdict": "average"}

    pct_rank = (await db.execute(
        text("""
            SELECT ROUND(
                (COUNT(*) FILTER (WHERE price <= :price)::numeric / COUNT(*)::numeric) * 100
            ) as percentile
            FROM products
            WHERE category = :cat
        """),
        {"price": product.price, "cat": product.category},
    )).scalar() or 50

    avg = float(stats.avg_price)
    diff_pct = ((product.price - avg) / avg) * 100

    if diff_pct < -15:
        verdict = "below_average"
    elif diff_pct > 15:
        verdict = "above_average"
    else:
        verdict = "average"

    return {
        "price": float(product.price),
        "category_avg": round(avg, 2),
        "category_min": float(stats.min_price),
        "category_max": float(stats.max_price),
        "percentile": int(pct_rank),
        "diff_pct": round(diff_pct, 1),
        "verdict": verdict,
    }
