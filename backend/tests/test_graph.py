"""Test graph routing logic."""

import pytest

from app.models.agent_schemas import Intent
from app.services.agent.graph import _route_after_intent, _route_after_validate, build_graph


class TestRouteAfterIntent:
    def _state(self, **kwargs):
        base = {"intent": None, "messages": [], "products": [], "recommendation": None,
                "retry_count": 0, "validation_error": None, "session_id": "test"}
        base.update(kwargs)
        return base

    def test_question_routes_to_converse(self):
        intent = Intent(message_type="question")
        assert _route_after_intent(self._state(intent=intent)) == "converse"

    def test_general_routes_to_converse(self):
        intent = Intent(message_type="general")
        assert _route_after_intent(self._state(intent=intent)) == "converse"

    def test_ready_product_request_routes_to_retrieve(self):
        intent = Intent(
            message_type="product_request",
            category="laptop",
            use_case="gaming",
            max_budget=1000,
        )
        assert _route_after_intent(self._state(intent=intent)) == "retrieve"

    def test_ready_with_context_instead_of_budget(self):
        intent = Intent(
            message_type="product_request",
            category="headphone",
            use_case="music",
            user_context="student",
        )
        assert _route_after_intent(self._state(intent=intent)) == "retrieve"

    def test_incomplete_request_routes_to_follow_up(self):
        intent = Intent(
            message_type="product_request",
            category="laptop",
        )
        assert _route_after_intent(self._state(intent=intent)) == "follow_up"

    def test_no_category_routes_to_follow_up(self):
        intent = Intent(
            message_type="product_request",
            use_case="gaming",
            max_budget=1000,
        )
        assert _route_after_intent(self._state(intent=intent)) == "follow_up"

    def test_none_intent_routes_to_converse(self):
        assert _route_after_intent(self._state(intent=None)) == "converse"


class TestRouteAfterValidate:
    def _state(self, **kwargs):
        base = {"intent": None, "messages": [], "products": [], "recommendation": None,
                "retry_count": 0, "validation_error": None, "session_id": "test"}
        base.update(kwargs)
        return base

    def test_pass_routes_to_end(self):
        result = _route_after_validate(self._state(validation_error=None))
        assert result == "__end__"

    def test_first_failure_retries(self):
        result = _route_after_validate(self._state(validation_error="bad id", retry_count=1))
        assert result == "recommend"

    def test_max_retries_falls_back(self):
        result = _route_after_validate(self._state(validation_error="bad id", retry_count=2))
        assert result == "fallback"

    def test_over_max_retries_falls_back(self):
        result = _route_after_validate(self._state(validation_error="bad id", retry_count=5))
        assert result == "fallback"


class TestGraphStructure:
    def test_graph_compiles(self):
        graph = build_graph()
        compiled = graph.compile()
        nodes = list(compiled.get_graph().nodes.keys())
        assert "extract_intent" in nodes
        assert "converse" in nodes
        assert "follow_up" in nodes
        assert "retrieve" in nodes
        assert "recommend" in nodes
        assert "validate" in nodes
        assert "fallback" in nodes

    def test_graph_has_start_and_end(self):
        graph = build_graph()
        compiled = graph.compile()
        nodes = list(compiled.get_graph().nodes.keys())
        assert "__start__" in nodes
        assert "__end__" in nodes
