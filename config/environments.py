from typing import Dict, Any

env_settings: Dict[str, Dict[str, Any]] = {
    "development": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
    },
    "production": {
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "CACHE_TTL": 600,  # 10分
    },
    "testing": {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "CACHE_TTL": 60,  # 1分
    }
}
