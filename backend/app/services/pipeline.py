"""
Pipeline entry point — translates between the FastAPI layer and the LangGraph agent.
"""

import uuid
from datetime import datetime

from langchain_core.messages import AIMessage, HumanMessage

from app.models.schemas import ChatResponse, ProductOut
from app.services.agent import get_compiled_graph


async def _persist_turn(
    session_id: str,
    user_message: str,
    assistant_reply: str,
    category: str | None = None,
    user_id: str | None = None,
):
    from app.core.database import AsyncSessionLocal
    if not AsyncSessionLocal:
        return
    async with AsyncSessionLocal() as db:
        from sqlalchemy import text
        row = (await db.execute(
            text("SELECT id FROM chat_sessions WHERE id = :sid"),
            {"sid": session_id},
        )).first()
        now = datetime.utcnow()
        if not row:
            await db.execute(
                text("INSERT INTO chat_sessions (id, user_id, category, created_at, updated_at) VALUES (:id, :uid, :cat, :now, :now)"),
                {"id": session_id, "uid": user_id, "cat": category, "now": now},
            )
        else:
            params: dict = {"sid": session_id, "now": now}
            sets = ["updated_at = :now"]
            if category:
                sets.append("category = :cat")
                params["cat"] = category
            if user_id:
                sets.append("user_id = :uid")
                params["uid"] = user_id
            await db.execute(text(f"UPDATE chat_sessions SET {', '.join(sets)} WHERE id = :sid"), params)

        await db.execute(
            text("INSERT INTO chat_messages (id, session_id, role, content, created_at) VALUES (:id, :sid, 'user', :content, :now)"),
            {"id": str(uuid.uuid4()), "sid": session_id, "content": user_message, "now": now},
        )
        await db.execute(
            text("INSERT INTO chat_messages (id, session_id, role, content, created_at) VALUES (:id, :sid, 'assistant', :content, :now)"),
            {"id": str(uuid.uuid4()), "sid": session_id, "content": assistant_reply, "now": now},
        )
        await db.commit()


async def run_pipeline(session_id: str, message: str) -> ChatResponse:
    graph = await get_compiled_graph()

    config = {"configurable": {"thread_id": session_id}}
    input_state = {"messages": [HumanMessage(content=message)]}

    result = await graph.ainvoke(input_state, config=config)

    recommendation = result.get("recommendation")
    products: list[ProductOut] = result.get("products", [])
    intent = result.get("intent")

    if recommendation and products:
        best_id = recommendation.best_pick.product_id
        alt_ids = [a.product_id for a in recommendation.alternatives]
        ordered_ids = [best_id] + alt_ids

        product_map = {p.id: p for p in products}
        reordered = [product_map[pid] for pid in ordered_ids if pid in product_map]
        remaining = [p for p in products if p.id not in set(ordered_ids)]
        reordered.extend(remaining)

        reason_map = {recommendation.best_pick.product_id: recommendation.best_pick.reason}
        for alt in recommendation.alternatives:
            reason_map[alt.product_id] = alt.reason

        lines = [f"⭐ Best Pick: {product_map[best_id].name} — {recommendation.best_pick.reason}"]
        if recommendation.alternatives:
            lines.append("\nAlso worth a look:")
            for alt in recommendation.alternatives:
                name = product_map.get(alt.product_id, None)
                display = name.name if name else alt.product_id
                lines.append(f"• {display} — {alt.reason}")
        lines.append(f"\n💡 {recommendation.tip}")
        reply = "\n".join(lines)

        return ChatResponse(
            session_id=session_id,
            reply=reply,
            products=reordered,
            best_pick_index=0,
            stage="recommendation",
        )

    last_ai = None
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage):
            last_ai = msg
            break

    if last_ai is None:
        reply = "I'm not sure how to help with that. Could you tell me more?"
    elif isinstance(last_ai.content, str):
        reply = last_ai.content
    elif isinstance(last_ai.content, list):
        reply = "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in last_ai.content
        )
    else:
        reply = str(last_ai.content)

    if intent and intent.message_type == "product_request":
        stage = "follow_up"
    elif intent and intent.message_type in ("question", "general"):
        stage = "conversation"
    else:
        stage = "follow_up"

    if products and not recommendation:
        stage = "recommendation"

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        products=products,
        best_pick_index=0,
        stage=stage,
    )


async def run_pipeline_stream(session_id: str, message: str, user_id: str | None = None):
    """Async generator that yields SSE events for streaming chat responses."""
    graph = await get_compiled_graph()
    config = {"configurable": {"thread_id": session_id}}
    input_state = {"messages": [HumanMessage(content=message)]}

    text_nodes = {"converse", "follow_up", "fallback"}
    accumulated: dict = {}
    full_reply_parts: list[str] = []

    async for mode, chunk in graph.astream(
        input_state, config=config, stream_mode=["messages", "updates"]
    ):
        if mode == "messages":
            msg_chunk, metadata = chunk
            node = metadata.get("langgraph_node", "")
            if node in text_nodes:
                content = getattr(msg_chunk, "content", "")
                if isinstance(content, str) and content:
                    full_reply_parts.append(content)
                    yield {"event": "token", "data": {"text": content}}
                elif isinstance(content, list):
                    text = "".join(
                        b.get("text", "") if isinstance(b, dict) else str(b)
                        for b in content
                    )
                    if text:
                        full_reply_parts.append(text)
                        yield {"event": "token", "data": {"text": text}}

        elif mode == "updates":
            for node_name, update in chunk.items():
                if node_name == "__end__":
                    continue
                if isinstance(update, dict):
                    accumulated.update(update)
                yield {"event": "node", "data": {"node": node_name, "status": "completed"}}

    recommendation = accumulated.get("recommendation")
    products: list[ProductOut] = accumulated.get("products", [])
    intent = accumulated.get("intent")

    if recommendation and products:
        best_id = recommendation.best_pick.product_id
        product_map = {p.id: p for p in products}
        alt_ids = [a.product_id for a in recommendation.alternatives]
        ordered_ids = [best_id] + alt_ids
        reordered = [product_map[pid] for pid in ordered_ids if pid in product_map]
        remaining = [p for p in products if p.id not in set(ordered_ids)]
        reordered.extend(remaining)

        lines = [f"⭐ Best Pick: {product_map[best_id].name} — {recommendation.best_pick.reason}"]
        if recommendation.alternatives:
            lines.append("\nAlso worth a look:")
            for alt in recommendation.alternatives:
                name_obj = product_map.get(alt.product_id)
                display = name_obj.name if name_obj else alt.product_id
                lines.append(f"• {display} — {alt.reason}")
        lines.append(f"\n💡 {recommendation.tip}")
        rec_text = "\n".join(lines)
        full_reply_parts.append(rec_text)
        yield {"event": "token", "data": {"text": rec_text}}

        products_data = [p.model_dump() for p in reordered]
        yield {"event": "products", "data": {"products": products_data, "best_pick_index": 0}}
        yield {"event": "stage", "data": {"stage": "recommendation"}}

    elif products and not recommendation:
        products_data = [p.model_dump() for p in products]
        yield {"event": "products", "data": {"products": products_data, "best_pick_index": 0}}
        yield {"event": "stage", "data": {"stage": "recommendation"}}

    else:
        if intent and intent.message_type == "product_request":
            stage = "follow_up"
        elif intent and intent.message_type in ("question", "general"):
            stage = "conversation"
        else:
            stage = "follow_up"
        yield {"event": "stage", "data": {"stage": stage}}

    category = intent.category if intent and hasattr(intent, "category") else None
    full_reply = "".join(full_reply_parts)
    if full_reply:
        try:
            await _persist_turn(session_id, message, full_reply, category=category, user_id=user_id)
        except Exception:
            pass

    yield {"event": "done", "data": {"session_id": session_id}}


async def generate_why_pick(session_id: str, product_name: str) -> str:
    from langchain_anthropic import ChatAnthropic
    from langchain_core.messages import SystemMessage

    from app.core.config import settings
    from app.services.prompts import WHY_PICK_SYSTEM

    graph = await get_compiled_graph()

    config = {"configurable": {"thread_id": session_id}}
    state = await graph.aget_state(config)

    history = state.values.get("messages", [])

    llm = ChatAnthropic(
        model="claude-haiku-5-5",
        api_key=settings.anthropic_api_key,
        max_tokens=512,
    )

    messages = [
        SystemMessage(content=WHY_PICK_SYSTEM),
        *history,
        HumanMessage(content=f"Why did you recommend the {product_name}?"),
    ]

    response = await llm.ainvoke(messages)
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    return str(content)
