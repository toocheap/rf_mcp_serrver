from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from config import get_logger, get_settings
import time

logger = get_logger()
settings = get_settings()

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # リクエスト元IPのチェック
        client_ip = request.client.host
        if self._is_blocked_ip(client_ip):
            logger.warning(f"Blocked IP attempt: {client_ip}")
            raise HTTPException(status_code=403, detail="Access denied")

        # リクエストヘッダーの検証
        self._validate_headers(request)

        # XSS対策ヘッダーの追加
        response = await call_next(request)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        return response

    def _is_blocked_ip(self, ip: str) -> bool:
        # IPブラックリストのチェック
        return False

    def _validate_headers(self, request: Request):
        # 必須ヘッダーのチェック
        required_headers = ["user-agent"]
        for header in required_headers:
            if header not in request.headers:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required header: {header}"
                )
