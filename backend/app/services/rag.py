"""
In-memory RAG using keyword scoring over searchable_text.
No vector DB required for MVP — swap in Pinecone here later.

Scoring: each word in the query gets +1 per match in searchable_text.
Budget filtering is soft — within-budget products are prioritized,
but slightly over-budget options are included if there aren't enough matches.
"""

from app.data.seed_products import PRODUCTS


def _score(product: dict, query_tokens: set[str]) -> float:
    text = product["searchable_text"].lower()
    name = product["name"].lower()
    summary = (product.get("summary") or "").lower()
    combined = f"{text} {name} {summary}"
    return sum(1 for token in query_tokens if token in combined)


def search_products(
    query: str,
    category: str | None = None,
    max_budget: float | None = None,
    top_k: int = 5,
) -> list[dict]:
    """
    Return the top_k most relevant products matching the query.
    Filters by category. Budget is a soft filter — within-budget products
    come first, then over-budget ones fill remaining slots.
    """
    query_tokens = set(query.lower().split())

    candidates = PRODUCTS

    # Hard filter: category
    if category and category in ("laptop", "headphone", "camera"):
        candidates = [p for p in candidates if p["category"] == category]

    if not candidates:
        return []

    # Soft budget: split into within-budget and over-budget
    if max_budget:
        within = [p for p in candidates if p["price"] <= max_budget]
        over = [p for p in candidates if p["price"] > max_budget]

        # Score both groups
        within_scored = sorted(within, key=lambda p: _score(p, query_tokens), reverse=True)
        over_scored = sorted(over, key=lambda p: _score(p, query_tokens), reverse=True)

        # Fill with within-budget first, then pad with over-budget if needed
        results = within_scored[:top_k]
        if len(results) < top_k:
            results += over_scored[:top_k - len(results)]
        return results

    # No budget constraint — score and sort
    scored = sorted(candidates, key=lambda p: _score(p, query_tokens), reverse=True)
    return scored[:top_k]
