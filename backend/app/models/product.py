import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # laptop | headphone | camera
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    affiliate_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Flexible spec storage — different per category
    specs: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    # AI-generated fields
    summary: Mapped[str] = mapped_column(Text, nullable=True)       # 1-line pitch
    pros: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    cons: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    # Embedding stored in Vector DB — only the ID is kept here for reference
    embedding_id: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
