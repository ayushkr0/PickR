import re

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from app.services.agent.nodes import (
    converse,
    extract_intent,
    fallback,
    follow_up,
    recommend,
    retrieve,
    validate,
)
from app.services.agent.state import AgentState

_compiled = None

_FOLLOWUP_RE = re.compile(
    r"compare|versus|vs\.?|difference|which one|which is better|tell me more"
    r"|other options|alternatives|cheaper|more premium|top two|top 2"
    r"|first one|second one|third one|between them|pros and cons",
    re.IGNORECASE,
)


def _is_followup_about_products(state: AgentState) -> bool:
    """True when the user is asking about products already recommended."""
    if not state.get("products"):
        return False
    msgs = state.get("messages", [])
    last_human = ""
    for m in reversed(msgs):
        if isinstance(m, HumanMessage):
            last_human = m.content if isinstance(m.content, str) else str(m.content)
            break
    return bool(_FOLLOWUP_RE.search(last_human))


def _route_after_intent(state: AgentState) -> str:
    intent = state["intent"]
    if intent is None:
        return "converse"

    if intent.message_type in ("question", "general"):
        return "converse"

    if intent.message_type == "product_request" and _is_followup_about_products(state):
        return "converse"

    ready = (
        intent.category is not None
        and intent.use_case is not None
    )
    if ready:
        return "retrieve"

    return "follow_up"


def _route_after_validate(state: AgentState) -> str:
    if state.get("validation_error") is None:
        return END
    if state.get("retry_count", 0) < 2:
        return "recommend"
    return "fallback"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("extract_intent", extract_intent)
    graph.add_node("converse", converse)
    graph.add_node("follow_up", follow_up)
    graph.add_node("retrieve", retrieve)
    graph.add_node("recommend", recommend)
    graph.add_node("validate", validate)
    graph.add_node("fallback", fallback)

    graph.add_edge(START, "extract_intent")

    graph.add_conditional_edges(
        "extract_intent",
        _route_after_intent,
        {"converse": "converse", "follow_up": "follow_up", "retrieve": "retrieve"},
    )

    graph.add_edge("converse", END)
    graph.add_edge("follow_up", END)
    graph.add_edge("retrieve", "recommend")
    graph.add_edge("recommend", "validate")

    graph.add_conditional_edges(
        "validate",
        _route_after_validate,
        {END: END, "recommend": "recommend", "fallback": "fallback"},
    )

    graph.add_edge("fallback", END)

    return graph


_checkpointer_conn = None


async def get_compiled_graph():
    global _compiled, _checkpointer_conn
    if _compiled is not None:
        return _compiled

    from app.core.config import settings

    graph = build_graph()

    if settings.database_url:
        from psycopg import AsyncConnection
        from psycopg.rows import dict_row
        from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

        db_url = settings.database_url
        if db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

        _checkpointer_conn = await AsyncConnection.connect(
            db_url, autocommit=True, prepare_threshold=0, row_factory=dict_row
        )
        checkpointer = AsyncPostgresSaver(conn=_checkpointer_conn)
        await checkpointer.setup()
        _compiled = graph.compile(checkpointer=checkpointer)
    else:
        _compiled = graph.compile()

    return _compiled
