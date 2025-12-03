"""Application configuration from environment variables."""

import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, Union


class Settings(BaseSettings):
    """Application settings."""

    # Database
    neon_database_url: str = os.getenv(
        "NEON_DATABASE_URL",
        "postgresql://user:password@localhost/chatbot_dev"
    )
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

    # Qdrant Vector Database
    qdrant_url: str = os.getenv("QDRANT_URL", "https://1521bc26-af63-4594-8df5-c4a2e64c549b.us-east4-0.gcp.cloud.qdrant.io:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

    # OpenAI API
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    # Application
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS - Accept both string and list, convert to list via validator
    allowed_origins: Union[str, list] = "http://localhost:3000,http://localhost:8000,https://92bilal26.github.io,https://92Bilal26.github.io"
    
    # Redis (optional for caching)
    redis_url: str = os.getenv("REDIS_URL", "")

    # Session Configuration
    session_expiry_days: int = 30
    max_conversation_history: int = 50

    # API Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    # Feature Flags
    enable_hallucination_check: bool = True
    enable_rate_limit_graceful_degradation: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env

    @field_validator("openai_api_key")
    @classmethod
    def check_openai_api_key(cls, v):
        """Check that OpenAI API key is set."""
        if not v:
            raise ValueError("OPENAI_API_KEY must be set")
        return v

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v):
        """Parse CORS origins from string"""
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v if isinstance(v, list) else []


# Create global settings instance
settings = Settings()
