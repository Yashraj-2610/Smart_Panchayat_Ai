import os
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Panchayat Decision Support System"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./smart_panchayat.db")

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "super-secret-key-for-smart-panchayat-2026"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

    # AI & Multi-Agent
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    USE_LOCAL_LLM: bool = os.getenv("USE_LOCAL_LLM", "False").lower() == "true"

    # Multilingual
    SUPPORTED_LANGUAGES: List[str] = ["en", "hi", "mr"]
    DEFAULT_LANGUAGE: str = "mr"  # Marathi default for Maharashtra Panchayats

    # Village Settings
    VILLAGE_NAME: str = "Alandi Gram Panchayat"
    DISTRICT: str = "Pune"
    STATE: str = "Maharashtra"
    TOTAL_WARDS: int = 6

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))  # seconds

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")

    # CORS
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://localhost:8502,http://localhost:8000"
    )

    # Deployment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()