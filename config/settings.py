from typing import List
from pydantic_settings import BaseSettings # type: ignore
from functools import lru_cache

class Settings(BaseSettings):
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    RF_API_KEY: str
    CLAUDE_API_KEY: str
    RF_API_BASE_URL: str = "https://api.recordedfuture.com/v2"
    CLAUDE_API_BASE_URL: str = "https://api.anthropic.com/v1"
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = ["*"]
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
