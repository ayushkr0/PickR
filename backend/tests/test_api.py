"""Test API contract — response shapes match frontend expectations."""

import pytest

from app.models.schemas import ChatRequest, ChatResponse, ProductOut, WhyPickRequest, WhyPickResponse


class TestChatResponseSchema:
    def test_minimal_response(self):
        resp = ChatResponse(
            session_id="abc-123",
            reply="Hello! How can I help?",
        )
        assert resp.session_id == "abc-123"
        assert resp.products == []
        assert resp.best_pick_index == 0
        assert resp.stage == "follow_up"

    def test_recommendation_response(self):
        product = ProductOut(
            id="p1",
            name="Test Laptop",
            category="laptop",
            brand="Brand",
            price=599.99,
            image_url="https://example.com/img.jpg",
            affiliate_url="https://example.com/buy",
            specs={"ram": "16GB"},
            summary="Good laptop",
            pros=["Fast", "Light"],
            cons=["Pricey"],
        )
        resp = ChatResponse(
            session_id="abc-123",
            reply="Here's my recommendation",
            products=[product],
            best_pick_index=0,
            stage="recommendation",
        )
        assert len(resp.products) == 1
        assert resp.products[0].name == "Test Laptop"
        assert resp.stage == "recommendation"

    def test_product_out_from_attributes(self):
        data = {
            "id": "p1",
            "name": "Test",
            "category": "laptop",
            "brand": "B",
            "price": 100.0,
            "image_url": None,
            "affiliate_url": None,
            "specs": {},
            "summary": None,
            "pros": [],
            "cons": [],
        }
        product = ProductOut(**data)
        assert product.id == "p1"

    def test_chat_request_optional_session(self):
        req = ChatRequest(message="hello")
        assert req.session_id is None
        assert req.message == "hello"

    def test_chat_request_with_session(self):
        req = ChatRequest(session_id="sess-1", message="hi")
        assert req.session_id == "sess-1"

    def test_why_pick_request(self):
        req = WhyPickRequest(session_id="sess-1", product_name="Test Laptop")
        assert req.session_id == "sess-1"

    def test_why_pick_response(self):
        resp = WhyPickResponse(explanation="Great laptop for students")
        assert "students" in resp.explanation

    def test_chat_response_serialization(self):
        resp = ChatResponse(
            session_id="s1",
            reply="test",
            products=[],
            stage="conversation",
        )
        data = resp.model_dump()
        assert "session_id" in data
        assert "reply" in data
        assert "products" in data
        assert "best_pick_index" in data
        assert "stage" in data
        assert "follow_up_questions" in data
