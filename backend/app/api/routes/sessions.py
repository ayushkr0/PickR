from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter()


@router.get("/sessions")
async def list_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = (await db.execute(
        text("""
            SELECT s.id, s.category, s.updated_at,
                   (SELECT content FROM chat_messages WHERE session_id = s.id ORDER BY created_at LIMIT 1) as preview
            FROM chat_sessions s
            WHERE s.user_id = :uid
            ORDER BY s.updated_at DESC
            LIMIT 50
        """),
        {"uid": user.id},
    )).fetchall()

    return [
        {
            "id": r.id,
            "category": r.category,
            "preview": (r.preview or "")[:120],
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in rows
    ]


@router.get("/sessions/{session_id}")
async def get_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    session_row = (await db.execute(
        text("SELECT id, user_id, category FROM chat_sessions WHERE id = :sid"),
        {"sid": session_id},
    )).first()
    if not session_row or session_row.user_id != user.id:
        raise HTTPException(404, "Session not found")

    messages = (await db.execute(
        text("SELECT role, content, created_at FROM chat_messages WHERE session_id = :sid ORDER BY created_at"),
        {"sid": session_id},
    )).fetchall()

    return {
        "id": session_row.id,
        "category": session_row.category,
        "messages": [
            {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat() if m.created_at else None}
            for m in messages
        ],
    }


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    session_row = (await db.execute(
        text("SELECT id, user_id FROM chat_sessions WHERE id = :sid"),
        {"sid": session_id},
    )).first()
    if not session_row or session_row.user_id != user.id:
        raise HTTPException(404, "Session not found")

    await db.execute(text("DELETE FROM chat_messages WHERE session_id = :sid"), {"sid": session_id})
    await db.execute(text("DELETE FROM chat_sessions WHERE id = :sid"), {"sid": session_id})
    await db.commit()
    return {"deleted": True}
