from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import get_settings, get_logger

logger = get_logger()
settings = get_settings()

class SecurityHandler:
    def __init__(self):
        self.bearer = HTTPBearer()
        self._admin_tokens = {"admin-token"}  # 本番環境では安全な方法で管理

    async def validate_admin_token(self, request: Request) -> bool:
        try:
            credentials: HTTPAuthorizationCredentials = await self.bearer(request)
            is_valid = credentials.credentials in self._admin_tokens
            if not is_valid:
                logger.warning(f"Invalid admin token attempt from {request.client.host}")
            return is_valid
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False

    async def verify_api_key(self, request: Request) -> bool:
        api_key = request.headers.get("x-api-key")
        if not api_key:
            logger.warning(f"Missing API key in request from {request.client.host}")
            raise HTTPException(status_code=401, detail="API key is required")
        # ここで実際のAPI key検証ロジックを実装
        return True

security_handler = SecurityHandler()
