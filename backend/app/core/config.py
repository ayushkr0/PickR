from pathlib import Path

from pydantic_settings import BaseSettings

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    anthropic_api_key: str = ""

    database_url: str = ""

    pinecone_api_key: str = ""
    pinecone_index_name: str = "pickr-products"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    langchain_tracing_v2: str = ""
    langchain_api_key: str = ""
    langchain_project: str = "pickr"

    jwt_secret: str = "pickr-dev-secret-change-in-prod"
    jwt_expiry_hours: int = 72

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001", "https://pick-r.vercel.app"]
    environment: str = "development"

    model_config = {"env_file": str(_BACKEND_DIR / ".env"), "extra": "ignore"}


settings = Settings()
