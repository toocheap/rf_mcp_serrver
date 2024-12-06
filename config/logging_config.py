import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
from datetime import datetime

class SecurityAwareJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensitive_fields = {'api_key', 'token', 'password', 'secret'}

    def process_log_record(self, log_record):
        log_record['timestamp'] = datetime.utcnow().isoformat()
        for field in self.sensitive_fields:
            if field in log_record:
                log_record[field] = "***MASKED***"
        return super().process_log_record(log_record)

def setup_logging(log_level: str = "INFO"):
    logger = logging.getLogger("mcp_server")
    logger.setLevel(getattr(logging, log_level))

    # ファイルハンドラー
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/mcp_server.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(SecurityAwareJsonFormatter(
        '%(timestamp)s %(request_id)s %(levelname)s %(name)s %(message)s'
    ))

    # コンソールハンドラー
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(SecurityAwareJsonFormatter(
        '%(timestamp)s %(levelname)s %(message)s'
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_logger():
    return logging.getLogger("mcp_server")
