from pydantic_settings import BaseSettings
from functools import lru_cache
import logging
from logging import Logger
from typing import Optional

class Settings(BaseSettings):
    # アプリケーション設定
    VERSION: str = "1.0.0"
    ENV: str = "development"
    DEBUG: bool = False

    # API設定
    CLAUDE_API_KEY: str
    CLAUDE_API_BASE_URL: str = "https://api.anthropic.com/v1"
    RF_API_KEY: str
    RF_API_BASE_URL: str

    # キャッシュ設定
    CACHE_TTL: int = 300  # 5分
    CACHE_MAX_SIZE: int = 1000

    # ログ設定
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # セキュリティ設定
    ADMIN_TOKENS: set[str] = set()
    API_KEY_HEADER: str = "x-api-key"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_logger() -> Logger:
    settings = get_settings()

    # ロガーの設定
    logger = logging.getLogger("mcp")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # ハンドラーの設定
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger.addHandler(handler)

    return logger
