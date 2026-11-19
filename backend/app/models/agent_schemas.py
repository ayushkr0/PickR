from typing import Literal

from pydantic import BaseModel, Field, model_validator


class Intent(BaseModel):
    message_type: Literal["product_request", "question", "general"]
    category: Literal["laptop", "headphone", "camera"] | None = None
    max_budget: float | None = Field(default=None, gt=0)
    use_case: str | None = None
    user_context: Literal["student", "professional", "casual"] | None = None
    experience_level: Literal["beginner", "intermediate", "expert"] = "beginner"


class Pick(BaseModel):
    product_id: str
    reason: str = Field(max_length=500)


class Recommendation(BaseModel):
    best_pick: Pick
    alternatives: list[Pick] = Field(default_factory=list, max_length=4)
    tip: str = Field(max_length=500)

    @model_validator(mode="after")
    def no_duplicate_picks(self) -> "Recommendation":
        all_picks = [self.best_pick] + self.alternatives
        seen: set[str] = set()
        for p in all_picks:
            if p.product_id in seen:
                raise ValueError(f"Duplicate product_id: {p.product_id}")
            seen.add(p.product_id)
        return self


def validate_recommendation(
    rec: Recommendation,
    retrieved_ids: set[str],
    price_lookup: dict[str, float],
    max_budget: float | None,
) -> list[str]:
    """Validate a Recommendation against retrieved products and budget.

    Returns a list of error strings. Empty list means valid.
    """
    errors: list[str] = []
    all_picks = [rec.best_pick] + rec.alternatives

    for p in all_picks:
        if p.product_id not in retrieved_ids:
            errors.append(f"product_id '{p.product_id}' was not in the retrieved set")

        if max_budget is not None and p.product_id in price_lookup:
            price = price_lookup[p.product_id]
            if price > max_budget:
                errors.append(
                    f"product '{p.product_id}' costs £{price} which exceeds budget £{max_budget}"
                )

    return errors
