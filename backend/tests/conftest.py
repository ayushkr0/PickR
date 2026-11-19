import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.schemas import ProductOut


MOCK_PRODUCTS = [
    ProductOut(
        id="prod-001",
        name="Test Laptop Pro",
        category="laptop",
        brand="TestBrand",
        price=799.99,
        image_url=None,
        affiliate_url=None,
        specs={"ram": "16GB", "storage": "512GB SSD"},
        summary="A great laptop for professionals.",
        pros=["Fast processor", "Good display"],
        cons=["Average battery"],
    ),
    ProductOut(
        id="prod-002",
        name="Budget Laptop",
        category="laptop",
        brand="ValueBrand",
        price=449.99,
        image_url=None,
        affiliate_url=None,
        specs={"ram": "8GB", "storage": "256GB SSD"},
        summary="Affordable laptop for students.",
        pros=["Great price", "Lightweight"],
        cons=["Limited storage"],
    ),
    ProductOut(
        id="prod-003",
        name="Premium Headphones X",
        category="headphone",
        brand="AudioCo",
        price=299.99,
        image_url=None,
        affiliate_url=None,
        specs={"driver": "40mm", "type": "Over-ear"},
        summary="Premium noise-cancelling headphones.",
        pros=["Excellent ANC", "Comfortable fit"],
        cons=["Expensive"],
    ),
]


@pytest.fixture
def mock_products():
    return MOCK_PRODUCTS


@pytest.fixture
def sample_intent_data():
    return {
        "message_type": "product_request",
        "category": "laptop",
        "max_budget": 800.0,
        "use_case": "programming",
        "user_context": "student",
        "experience_level": "beginner",
    }
