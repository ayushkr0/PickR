import json
import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.dependencies import get_optional_user
from app.models.schemas import ChatRequest
from app.models.user import User

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def _sse(event: str, data: dict | str) -> str:
    payload = json.dumps(data) if isinstance(data, dict) else data
    return f"event: {event}\ndata: {payload}\n\n"


@router.post("/chat/stream")
@limiter.limit("10/minute")
async def chat_stream(request: Request, body: ChatRequest, user: User | None = Depends(get_optional_user)):
    if not body.message.strip():
        async def err():
            yield _sse("error", {"detail": "Message cannot be empty."})
        return StreamingResponse(err(), media_type="text/event-stream")

    session_id = body.session_id or str(uuid.uuid4())

    async def event_generator():
        try:
            from app.services.pipeline import run_pipeline_stream

            async for event in run_pipeline_stream(session_id, body.message, user_id=user.id if user else None):
                yield _sse(event["event"], event["data"])

        except Exception as e:
            yield _sse("error", {"detail": str(e)})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
