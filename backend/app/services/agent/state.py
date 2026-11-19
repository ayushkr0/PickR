from langgraph.graph import MessagesState

from app.models.agent_schemas import Intent, Recommendation
from app.models.schemas import ProductOut


class AgentState(MessagesState):
    intent: Intent | None = None
    products: list[ProductOut] = []
    recommendation: Recommendation | None = None
    retry_count: int = 0
    validation_error: str | None = None
    session_id: str = ""
