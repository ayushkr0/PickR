from pydantic import BaseModel


# ── Product ──────────────────────────────────────────────────────────────────

class ProductOut(BaseModel):
    id: str
    name: str
    category: str
    brand: str
    price: float
    image_url: str | None
    affiliate_url: str | None
    specs: dict
    summary: str | None
    pros: list[str]
    cons: list[str]

    model_config = {"from_attributes": True}


# ── Chat ─────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    session_id: str | None = None   # None = start a new session
    message: str


class MessageOut(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str                          # assistant's text reply
    products: list[ProductOut] = []     # populated when recommendations are ready
    best_pick_index: int = 0            # index of the best recommendation in products list
    follow_up_questions: list[str] = [] # clarifying questions if more info needed
    stage: str = "follow_up"           # "follow_up" | "recommendation" | "conversation"


class WhyPickRequest(BaseModel):
    session_id: str
    product_name: str


class WhyPickResponse(BaseModel):
    explanation: str
