from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import get_settings, get_logger
from typing import Optional
import secrets
import time
from datetime import datetime, timedelta

logger = get_logger()
settings = get_settings()

class SecurityHandler:
    def __init__(self):
        self.bearer = HTTPBearer()
        self._token_cache = {}  # {token: (expiry_time, rate_limit_info)}

    async def validate_admin_token(self, request: Request) -> bool:
        try:
            credentials: HTTPAuthorizationCredentials = await self.bearer(request)
            token = credentials.credentials

            # トークンの検証
            if not self._verify_token(token):
                logger.warning(
                    "Invalid admin token attempt",
                    extra={
                        "ip": request.client.host,
                        "path": request.url.path
                    }
                )
                return False

            # レート制限のチェック
            if not self._check_rate_limit(token):
                logger.warning(
                    "Rate limit exceeded",
                    extra={
                        "token": token[:8] + "...",
                        "ip": request.client.host
                    }
                )
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )

            return True

        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False

    async def verify_api_key(self, request: Request) -> bool:
        api_key = request.headers.get(settings.API_KEY_HEADER)
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="API key is required"
            )

        # API keyの検証
        if not await self._validate_api_key(api_key):
            logger.warning(
                "Invalid API key attempt",
                extra={
                    "ip": request.client.host,
                    "path": request.url.path
                }
            )
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )

        return True

    def _verify_token(self, token: str) -> bool:
        # トークンの有効期限チェック
        if token in self._token_cache:
            expiry_time, _ = self._token_cache[token]
            if expiry_time > time.time():
                return token in settings.ADMIN_TOKENS
        return False

    def _check_rate_limit(self, token: str) -> bool:
        current_time = time.time()
        if token in self._token_cache:
            _, rate_info = self._token_cache[token]
            if current_time - rate_info["last_request"] < 1:  # 1秒あたりの制限
                rate_info["count"] += 1
                if rate_info["count"] > 10:  # 1秒あたり10リクエストまで
                    return False
            else:
                rate_info["count"] = 1
                rate_info["last_request"] = current_time
        else:
            self._token_cache[token] = (
                current_time + 3600,  # 1時間の有効期限
                {"count": 1, "last_request": current_time}
            )
        return True

    async def _validate_api_key(self, api_key: str) -> bool:
        # ここで実際のAPI key検証ロジックを実装
        # 例：データベースでの検証やハッシュ比較など
        return True

security_handler = SecurityHandler()
