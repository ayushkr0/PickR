from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.core.config import settings
from app.core.database import AsyncSessionLocal, get_products_by_ids
from app.models.agent_schemas import Intent, Recommendation, validate_recommendation
from app.models.schemas import ProductOut
from app.services.agent.state import AgentState
from app.services.prompts import (
    CONVERSATION_SYSTEM,
    FOLLOWUP_SYSTEM,
    INTENT_SYSTEM,
    QUERY_EXPANSION_SYSTEM,
    RECOMMENDATION_SYSTEM,
    RERANK_SYSTEM,
)
from app.services.vector_store import search_products as pinecone_search

_haiku = None
_sonnet = None


def _sanitize_messages(messages: list) -> list:
    """Remove empty text content blocks that the Anthropic API rejects."""
    cleaned = []
    for msg in messages:
        c = msg.content
        if isinstance(c, list):
            blocks = [
                b for b in c
                if not (isinstance(b, dict) and b.get("type") == "text" and not b.get("text"))
                and not (isinstance(b, str) and not b.strip())
            ]
            if not blocks:
                continue
            if len(blocks) != len(c):
                msg = msg.__class__(
                    content=blocks[0]["text"] if len(blocks) == 1 and isinstance(blocks[0], dict) and blocks[0].get("type") == "text" else blocks,
                    **({"name": msg.name} if getattr(msg, "name", None) else {}),
                )
        elif isinstance(c, str) and not c.strip():
            continue
        cleaned.append(msg)
    return cleaned


def _get_haiku() -> ChatAnthropic:
    global _haiku
    if _haiku is None:
        _haiku = ChatAnthropic(
            model="claude-haiku-5-5",
            api_key=settings.anthropic_api_key,
            max_tokens=256,
        )
    return _haiku


def _get_sonnet() -> ChatAnthropic:
    global _sonnet
    if _sonnet is None:
        _sonnet = ChatAnthropic(
            model="claude-sonnet-5-5",
            api_key=settings.anthropic_api_key,
            max_tokens=1024,
        )
    return _sonnet


async def extract_intent(state: AgentState) -> dict:
    llm = _get_haiku().with_structured_output(Intent, method="json_schema")
    messages = [SystemMessage(content=INTENT_SYSTEM)] + _sanitize_messages(state["messages"])
    intent = await llm.ainvoke(messages)
    return {"intent": intent}


async def converse(state: AgentState) -> dict:
    llm = _get_sonnet()

    product_context = ""
    products = state.get("products")
    if products:
        product_lines = []
        for i, p in enumerate(products):
            specs_str = ", ".join(f"{k}: {v}" for k, v in (p.specs or {}).items()) if p.specs else "N/A"
            label = " [BEST PICK]" if i == 0 else ""
            product_lines.append(
                f"- {p.name} by {p.brand}: £{p.price}{label}\n"
                f"  Specs: {specs_str}\n"
                f"  Pros: {', '.join(p.pros)} | Cons: {', '.join(p.cons)}\n"
                f"  Summary: {p.summary or 'N/A'}"
            )
        product_context = "\n\nPreviously recommended products (use ONLY this data):\n" + "\n".join(product_lines)

    system = CONVERSATION_SYSTEM + product_context
    messages = [SystemMessage(content=system)] + _sanitize_messages(state["messages"])
    response = await llm.ainvoke(messages)
    return {"messages": [response]}


async def follow_up(state: AgentState) -> dict:
    intent = state["intent"]
    missing = []
    if not intent.category:
        missing.append("product category (laptop, headphone, or camera)")
    if not intent.use_case:
        missing.append("main use case")
    if not intent.user_context:
        missing.append("user context (student, professional, or casual)")
    if not intent.max_budget:
        missing.append("budget")

    context = f"\n\nMissing information: {', '.join(missing)}." if missing else ""
    system = FOLLOWUP_SYSTEM + context

    llm = _get_haiku()
    messages = [SystemMessage(content=system)] + _sanitize_messages(state["messages"])
    response = await llm.ainvoke(messages)
    return {"messages": [response]}


async def _expand_query(intent) -> str:
    """Use LLM to translate user intent into spec-rich search terms."""
    llm = _get_haiku()
    user_request = f"Category: {intent.category or 'any'}, Use case: {intent.use_case or 'general'}"
    if intent.max_budget:
        user_request += f", Budget: £{intent.max_budget}"
    else:
        user_request += ", Budget: unlimited / no limit"
    if intent.user_context:
        user_request += f", User: {intent.user_context}"

    messages = [
        SystemMessage(content=QUERY_EXPANSION_SYSTEM),
        HumanMessage(content=user_request),
    ]
    response = await llm.ainvoke(messages)
    content = response.content
    if isinstance(content, list):
        content = "".join(
            b.get("text", "") if isinstance(b, dict) else str(b)
            for b in content
        )
    return str(content).strip()


async def _rerank_products(intent, rows: list) -> list:
    """Use LLM to score and re-rank products by relevance to user needs."""
    if len(rows) <= 5:
        return rows

    import json
    llm = _get_haiku()

    products_text = "\n".join(
        f"- id: {r.id} | {r.name} | £{r.price} | specs: {json.dumps(r.specs or {})}"
        for r in rows
    )
    user_needs = f"Category: {intent.category}, Use case: {intent.use_case or 'general'}"
    if intent.max_budget:
        user_needs += f", Budget: £{intent.max_budget}"
    else:
        user_needs += ", Budget: unlimited"
    if intent.user_context:
        user_needs += f", User: {intent.user_context}"

    messages = [
        SystemMessage(content=RERANK_SYSTEM),
        HumanMessage(content=f"User needs: {user_needs}\n\nProducts:\n{products_text}"),
    ]
    response = await llm.ainvoke(messages)
    content = response.content
    if isinstance(content, list):
        content = "".join(
            b.get("text", "") if isinstance(b, dict) else str(b)
            for b in content
        )

    try:
        text = str(content).strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1:
            text = text[start:end + 1]
        scored = json.loads(text)
        id_to_score = {item["id"]: item["score"] for item in scored}
        rows.sort(key=lambda r: id_to_score.get(r.id, 0), reverse=True)
    except (json.JSONDecodeError, KeyError, TypeError):
        pass

    return rows


async def retrieve(state: AgentState) -> dict:
    intent = state["intent"]

    # Stage 1: LLM-powered query expansion
    expanded_query = await _expand_query(intent)

    search_budget = intent.max_budget * 1.15 if intent.max_budget else None

    product_ids = pinecone_search(
        query=expanded_query,
        category=intent.category,
        max_budget=search_budget,
        top_k=15,
    )

    if not product_ids and search_budget is not None:
        product_ids = pinecone_search(
            query=expanded_query,
            category=intent.category,
            max_budget=None,
            top_k=15,
        )

    if not product_ids:
        return {"products": []}

    if AsyncSessionLocal is None:
        return {"products": []}

    async with AsyncSessionLocal() as db:
        rows = await get_products_by_ids(db, product_ids)

    # Stage 2: LLM-powered re-ranking by spec relevance
    rows = await _rerank_products(intent, rows)

    if search_budget is not None and intent.max_budget is not None:
        within_budget = []
        slightly_over = []
        for row in rows:
            if row.price > intent.max_budget:
                slightly_over.append(row)
            else:
                within_budget.append(row)
        rows = within_budget + slightly_over[:max(0, 3 - len(within_budget))]

    products = []
    for row in rows[:5]:
        products.append(
            ProductOut(
                id=row.id,
                name=row.name,
                category=row.category,
                brand=row.brand,
                price=row.price,
                image_url=row.image_url,
                affiliate_url=row.affiliate_url,
                specs=row.specs,
                summary=row.summary,
                pros=row.pros,
                cons=row.cons,
            )
        )

    return {"products": products}


async def recommend(state: AgentState) -> dict:
    products = state["products"]
    intent = state["intent"]

    product_context = "\n\n".join(
        f"product_id: {p.id}\n"
        f"Name: {p.name}\n"
        f"Price: £{p.price}\n"
        f"Summary: {p.summary}\n"
        f"Pros: {', '.join(p.pros)}\n"
        f"Cons: {', '.join(p.cons)}"
        for p in products
    )

    user_context = (
        f"User profile:\n"
        f"- Category: {intent.category}\n"
        f"- Budget: £{intent.max_budget or 'not specified'}\n"
        f"- Use case: {intent.use_case or 'general use'}\n"
        f"- Who they are: {intent.user_context or 'not specified'}\n"
        f"- Experience level: {intent.experience_level}\n"
    )

    retry_note = ""
    if state.get("validation_error"):
        retry_note = (
            f"\n\nPREVIOUS ATTEMPT FAILED VALIDATION: {state['validation_error']}\n"
            "Fix the issues and try again. Use ONLY product_id values from the list above."
        )

    prompt = f"{user_context}\n\nAvailable products:\n{product_context}{retry_note}"

    llm = _get_sonnet().with_structured_output(Recommendation, method="json_schema")
    messages = [
        SystemMessage(content=RECOMMENDATION_SYSTEM),
        *_sanitize_messages(state["messages"]),
        HumanMessage(content=prompt),
    ]
    rec = await llm.ainvoke(messages)
    return {"recommendation": rec}


async def validate(state: AgentState) -> dict:
    rec = state["recommendation"]
    products = state["products"]

    retrieved_ids = {p.id for p in products}
    price_lookup = {p.id: p.price for p in products}
    max_budget = state["intent"].max_budget if state["intent"] else None

    errors = validate_recommendation(rec, retrieved_ids, price_lookup, max_budget)

    if errors:
        return {
            "validation_error": "; ".join(errors),
            "retry_count": state.get("retry_count", 0) + 1,
        }

    return {"validation_error": None}


async def fallback(state: AgentState) -> dict:
    from app.services.rag import search_products as keyword_search

    intent = state["intent"]
    query = " ".join(filter(None, [intent.use_case, intent.category]))

    products = keyword_search(
        query=query,
        category=intent.category,
        max_budget=intent.max_budget,
        top_k=5,
    )

    if not products:
        msg = (
            "I couldn't find products matching your exact criteria. "
            "Could you adjust your budget or let me know if you're flexible on category?"
        )
        return {"messages": [AIMessage(content=msg)], "products": []}

    product_text = "\n".join(
        f"- {p['name']} (£{p['price']}) — {p.get('summary', '')}"
        for p in products
    )

    llm = _get_sonnet()
    messages = [
        SystemMessage(content=RECOMMENDATION_SYSTEM),
        *_sanitize_messages(state["messages"]),
        HumanMessage(content=f"Available products:\n{product_text}"),
    ]
    response = await llm.ainvoke(messages)

    products_out: list[ProductOut] = [
        ProductOut(
            id=p.get("id", p["name"]),
            name=p["name"],
            category=p["category"],
            brand=p["brand"],
            price=p["price"],
            image_url=p.get("image_url"),
            affiliate_url=p.get("affiliate_url"),
            specs=p["specs"],
            summary=p.get("summary"),
            pros=p["pros"],
            cons=p["cons"],
        )
        for p in products
    ]

    return {"messages": [response], "products": products_out}
