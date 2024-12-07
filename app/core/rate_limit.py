from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

class RateLimiter:
    def __init__(self):
        self._requests: Dict[str, Tuple[int, float]] = {}

    async def check_rate_limit(self, request: Request):
        key = f"{request.client.host}:{request.url.path}"
        current_time = time.time()

        if key in self._requests:
            count, window_start = self._requests[key]
            if current_time - window_start < 60:  # 1分間のウィンドウ
                if count >= 100:  # 1分間に100リクエストまで
                    raise HTTPException(
                        status_code=429,
                        detail="Too many requests"
                    )
                self._requests[key] = (count + 1, window_start)
            else:
                self._requests[key] = (1, current_time)
        else:
            self._requests[key] = (1, current_time)
