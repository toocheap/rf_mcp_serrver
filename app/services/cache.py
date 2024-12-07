from cachetools import TTLCache
from typing import Optional, Dict, Any
from config import get_logger, get_settings

logger = get_logger()
settings = get_settings()

class RFCache:
    def __init__(self):
        self.ip_cache = TTLCache(
            maxsize=settings.CACHE_MAX_SIZE,
            ttl=settings.CACHE_TTL
        )
        self.domain_cache = TTLCache(maxsize=1000, ttl=300)
        self.vulnerability_cache = TTLCache(maxsize=1000, ttl=1800)  # 30分
        self.hash_cache = TTLCache(maxsize=1000, ttl=300)

    def get(self, cache_type: str, key: str) -> Optional[Dict[str, Any]]:
        try:
            cache = getattr(self, f"{cache_type}_cache")
            return cache.get(key)
        except AttributeError:
            logger.error(f"Invalid cache type: {cache_type}")
            return None

    def set(self, cache_type: str, key: str, value: Dict[str, Any]):
        try:
            cache = getattr(self, f"{cache_type}_cache")
            cache[key] = value
            logger.debug(f"Cached {cache_type} data for key: {key}")
        except AttributeError:
            logger.error(f"Invalid cache type: {cache_type}")

    def clear_all(self):
        self.ip_cache.clear()
        self.domain_cache.clear()
        self.vulnerability_cache.clear()
        self.hash_cache.clear()
        logger.info("All caches cleared")
