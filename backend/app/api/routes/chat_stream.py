import json
import uuid

import pendo_sdk
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
        pendo_sdk.set_identity(
            visitor_id=user.id if user else None,  # TODO: map to the visitor id your Pendo web snippet uses
            account_id=None,  # TODO: map to the Pendo account id for this user
            conversation_id=session_id,  # TODO: confirm the chat session id is the conversation id to report
        )
        try:
            from app.services.pipeline import run_pipeline_stream

            async for event in run_pipeline_stream(session_id, body.message, user_id=user.id if user else None):
                yield _sse(event["event"], event["data"])

        except Exception as e:
            import logging
            logging.getLogger("pickr").exception("Stream error: %s", e)
            yield _sse("error", {"detail": "Something went wrong. Please try again."})
        finally:
            pendo_sdk.close_turn(session_id)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
