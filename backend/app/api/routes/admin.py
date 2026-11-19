from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter()


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")
    return user


@router.get("/admin/stats")
async def admin_stats(
    user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    totals = (await db.execute(text("""
        SELECT
            (SELECT COUNT(*) FROM chat_sessions) as total_sessions,
            (SELECT COUNT(*) FROM users) as total_users,
            (SELECT COUNT(*) FROM chat_sessions WHERE created_at >= CURRENT_DATE) as sessions_today,
            (SELECT ROUND(AVG(msg_count)::numeric, 1) FROM (
                SELECT COUNT(*) as msg_count FROM chat_messages GROUP BY session_id
            ) sub) as avg_messages
    """))).first()

    categories = (await db.execute(text("""
        SELECT category, COUNT(*) as count
        FROM chat_sessions
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC
        LIMIT 10
    """))).fetchall()

    recent = (await db.execute(text("""
        SELECT s.id, s.category, s.created_at, s.updated_at,
               (SELECT content FROM chat_messages WHERE session_id = s.id ORDER BY created_at LIMIT 1) as preview
        FROM chat_sessions s
        ORDER BY s.updated_at DESC
        LIMIT 10
    """))).fetchall()

    total_sessions = totals.total_sessions if totals else 0

    return {
        "total_sessions": total_sessions,
        "total_users": totals.total_users if totals else 0,
        "sessions_today": totals.sessions_today if totals else 0,
        "avg_messages": float(totals.avg_messages) if totals and totals.avg_messages else 0,
        "categories": [
            {"name": r.category, "count": r.count, "pct": round(r.count / total_sessions * 100, 1) if total_sessions else 0}
            for r in categories
        ],
        "recent_sessions": [
            {
                "id": r.id,
                "category": r.category,
                "preview": (r.preview or "")[:120],
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
            for r in recent
        ],
    }
