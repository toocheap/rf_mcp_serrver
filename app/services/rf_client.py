import httpx
from typing import Dict, Optional
from config import get_settings, get_logger
from app.core.exceptions import RFAPIException
from .cache import RFCache

settings = get_settings()
logger = get_logger()

class RFClient:
    def __init__(self, cache: RFCache):
        self.base_url = settings.RF_API_BASE_URL
        self.api_key = settings.RF_API_KEY
        self.cache = cache
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"X-RFToken": self.api_key},
            timeout=30.0
        )

    async def _make_request(self, path: str, params: Optional[Dict] = None) -> Dict:
        try:
            response = await self.client.get(path, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"RF API error: {str(e)}")
            raise RFAPIException(str(e), status_code=e.response.status_code)
        except Exception as e:
            logger.error(f"Unexpected error in RF API request: {str(e)}")
            raise RFAPIException(str(e))

    async def get_ip_info(self, ip: str) -> Dict:
        cached = self.cache.get("ip", ip)
        if cached:
            return cached

        result = await self._make_request(f"/ip/{ip}")
        self.cache.set("ip", ip, result)
        return result

    async def get_domain_info(self, domain: str) -> Dict:
        cached = self.cache.get("domain", domain)
        if cached:
            return cached

        result = await self._make_request(f"/domain/{domain}")
        self.cache.set("domain", domain, result)
        return result

    async def get_vulnerability_info(self, cve: str) -> Dict:
        cached = self.cache.get("vulnerability", cve)
        if cached:
            return cached

        result = await self._make_request(f"/vulnerability/{cve}")
        self.cache.set("vulnerability", cve, result)
        return result
