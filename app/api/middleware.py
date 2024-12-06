from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config import get_logger
import time
import uuid

logger = get_logger()

class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # リクエスト開始時間
        start_time = time.time()

        # リクエストログ
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host
            }
        )

        try:
            response = await call_next(request)

            # レスポンス時間の計算
            process_time = time.time() - start_time

            logger.info(
                f"Request completed in {process_time:.3f}s",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "process_time": process_time
                }
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    "request_id": request_id,
                    "error": str(e)
                },
                exc_info=True
            )
            raise
