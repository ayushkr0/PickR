import uuid

import pendo_sdk
from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.dependencies import get_optional_user
from app.models.schemas import ChatRequest, ChatResponse, WhyPickRequest, WhyPickResponse
from app.models.user import User
from app.services.pipeline import run_pipeline, generate_why_pick

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, body: ChatRequest, user: User | None = Depends(get_optional_user)) -> ChatResponse:
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    session_id = body.session_id or str(uuid.uuid4())

    pendo_sdk.set_identity(
        visitor_id=user.id if user else None,  # TODO: map to the visitor id your Pendo web snippet uses
        account_id=None,  # TODO: map to the Pendo account id for this user
        conversation_id=session_id,  # TODO: confirm the chat session id is the conversation id to report
    )
    try:
        response = await run_pipeline(
            session_id=session_id,
            message=body.message,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    finally:
        pendo_sdk.close_turn(session_id)

    return response


@router.post("/chat/why", response_model=WhyPickResponse)
async def why_this_pick(request: WhyPickRequest) -> WhyPickResponse:
    try:
        explanation = await generate_why_pick(
            session_id=request.session_id,
            product_name=request.product_name,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return WhyPickResponse(explanation=explanation)


@router.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    return {"cleared": True}
