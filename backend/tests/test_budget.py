"""Budget regression tests — all returned prices must be <= stated budget."""

import pytest

from app.models.agent_schemas import Pick, Recommendation, validate_recommendation
from app.models.schemas import ProductOut


class TestBudgetEnforcement:
    def _make_products(self, prices: list[float]) -> list[ProductOut]:
        return [
            ProductOut(
                id=f"p-{i}",
                name=f"Product {i}",
                category="laptop",
                brand="Brand",
                price=price,
                image_url=None,
                affiliate_url=None,
                specs={},
                summary="Test",
                pros=["Good"],
                cons=["Bad"],
            )
            for i, price in enumerate(prices)
        ]

    def test_all_within_budget(self):
        products = self._make_products([500, 600, 700])
        rec = Recommendation(
            best_pick=Pick(product_id="p-0", reason="Best value"),
            alternatives=[
                Pick(product_id="p-1", reason="Good option"),
                Pick(product_id="p-2", reason="Premium choice"),
            ],
            tip="Check reviews",
        )
        retrieved_ids = {p.id for p in products}
        price_lookup = {p.id: p.price for p in products}

        errors = validate_recommendation(rec, retrieved_ids, price_lookup, max_budget=800)
        assert errors == [], f"Budget violations: {errors}"

    def test_over_budget_detected(self):
        products = self._make_products([500, 900, 700])
        rec = Recommendation(
            best_pick=Pick(product_id="p-0", reason="Best value"),
            alternatives=[
                Pick(product_id="p-1", reason="Over budget"),
            ],
            tip="Save money",
        )
        retrieved_ids = {p.id for p in products}
        price_lookup = {p.id: p.price for p in products}

        errors = validate_recommendation(rec, retrieved_ids, price_lookup, max_budget=800)
        assert len(errors) == 1
        assert "exceeds budget" in errors[0]

    def test_no_budget_allows_any_price(self):
        products = self._make_products([5000, 10000])
        rec = Recommendation(
            best_pick=Pick(product_id="p-0", reason="Expensive"),
            alternatives=[Pick(product_id="p-1", reason="Very expensive")],
            tip="Invest wisely",
        )
        retrieved_ids = {p.id for p in products}
        price_lookup = {p.id: p.price for p in products}

        errors = validate_recommendation(rec, retrieved_ids, price_lookup, max_budget=None)
        assert errors == []

    def test_hallucinated_product_detected(self):
        products = self._make_products([500])
        rec = Recommendation(
            best_pick=Pick(product_id="p-0", reason="OK"),
            alternatives=[Pick(product_id="fake-id", reason="Hallucinated")],
            tip="Oops",
        )
        retrieved_ids = {p.id for p in products}
        price_lookup = {p.id: p.price for p in products}

        errors = validate_recommendation(rec, retrieved_ids, price_lookup, max_budget=1000)
        assert any("not in the retrieved set" in e for e in errors)

    def test_duplicate_products_rejected(self):
        with pytest.raises(Exception, match="Duplicate"):
            Recommendation(
                best_pick=Pick(product_id="p-0", reason="Good"),
                alternatives=[Pick(product_id="p-0", reason="Same")],
                tip="Duplicate test",
            )

    def test_zero_budget_violations_on_golden_scenario(self):
        """The core regression: given a budget, NO product should exceed it."""
        budget = 500.0
        products = self._make_products([399, 450, 499, 350, 480])
        rec = Recommendation(
            best_pick=Pick(product_id="p-2", reason="Best within budget"),
            alternatives=[
                Pick(product_id="p-4", reason="Close to budget"),
                Pick(product_id="p-1", reason="Mid range"),
                Pick(product_id="p-0", reason="Budget friendly"),
            ],
            tip="All within your budget",
        )
        retrieved_ids = {p.id for p in products}
        price_lookup = {p.id: p.price for p in products}

        errors = validate_recommendation(rec, retrieved_ids, price_lookup, max_budget=budget)
        assert errors == [], f"BUDGET REGRESSION: {errors}"
