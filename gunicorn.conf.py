import multiprocessing
import os

# サーバーソケット
bind = os.getenv("BIND", "0.0.0.0:8000")

# ワーカープロセス
workers = int(os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"

# タイムアウト設定
timeout = int(os.getenv("TIMEOUT", 30))
keepalive = int(os.getenv("KEEPALIVE", 5))

# ワーカーの再起動設定
max_requests = int(os.getenv("MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("MAX_REQUESTS_JITTER", 50))

# ログ設定
accesslog = os.getenv("ACCESS_LOG", "/var/log/gunicorn/access.log")
errorlog = os.getenv("ERROR_LOG", "/var/log/gunicorn/error.log")
loglevel = os.getenv("LOG_LEVEL", "warning")

# セキュリティ設定
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
