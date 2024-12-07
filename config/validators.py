from pydantic import field_validator
from typing import Set

class Settings(BaseSettings):
    # ... 既存の設定 ...

    @field_validator("ADMIN_TOKENS", mode="before")
    @classmethod
    def validate_admin_tokens(cls, v) -> Set[str]:
        if isinstance(v, str):
            import json
            return set(json.loads(v))
        return set(v)

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v):
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v not in allowed_levels:
            raise ValueError(f"Log level must be one of {allowed_levels}")
        return v
