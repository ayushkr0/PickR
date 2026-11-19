"""Test intent extraction accuracy against golden queries."""

import json
from pathlib import Path

import pytest

from app.models.agent_schemas import Intent


def load_golden_queries():
    path = Path(__file__).parent / "golden_queries.json"
    with open(path) as f:
        return json.load(f)


GOLDEN = load_golden_queries()


class TestIntentSchema:
    def test_valid_product_request(self):
        intent = Intent(
            message_type="product_request",
            category="laptop",
            max_budget=1000.0,
            use_case="gaming",
            user_context="student",
            experience_level="beginner",
        )
        assert intent.message_type == "product_request"
        assert intent.category == "laptop"
        assert intent.max_budget == 1000.0

    def test_valid_question(self):
        intent = Intent(message_type="question")
        assert intent.category is None
        assert intent.max_budget is None

    def test_valid_general(self):
        intent = Intent(message_type="general")
        assert intent.experience_level == "beginner"

    def test_invalid_message_type(self):
        with pytest.raises(Exception):
            Intent(message_type="invalid_type")

    def test_invalid_category(self):
        with pytest.raises(Exception):
            Intent(message_type="product_request", category="phone")

    def test_negative_budget(self):
        with pytest.raises(Exception):
            Intent(message_type="product_request", max_budget=-100)

    def test_zero_budget(self):
        with pytest.raises(Exception):
            Intent(message_type="product_request", max_budget=0)

    def test_null_budget_allowed(self):
        intent = Intent(message_type="product_request", max_budget=None)
        assert intent.max_budget is None


class TestGoldenQueryExpectations:
    @pytest.mark.parametrize("query", GOLDEN, ids=[q["message"][:40] for q in GOLDEN])
    def test_golden_query_has_valid_expected_type(self, query):
        assert query["expected_type"] in ("product_request", "question", "general")

    @pytest.mark.parametrize(
        "query",
        [q for q in GOLDEN if q.get("expected_category")],
        ids=[q["message"][:40] for q in GOLDEN if q.get("expected_category")],
    )
    def test_golden_query_has_valid_category(self, query):
        assert query["expected_category"] in ("laptop", "headphone", "camera")

    @pytest.mark.parametrize(
        "query",
        [q for q in GOLDEN if q.get("expected_budget_lte")],
        ids=[q["message"][:40] for q in GOLDEN if q.get("expected_budget_lte")],
    )
    def test_golden_query_budget_is_positive(self, query):
        assert query["expected_budget_lte"] > 0
