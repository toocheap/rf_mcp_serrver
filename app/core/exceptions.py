from typing import Optional, Any, Dict

class MCPError(Exception):
    def __init__(
        self,
        error_type: str,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.error_type = error_type
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class RFAPIException(MCPError):
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_type="rf_api_error",
            message=message,
            status_code=status_code,
            details=details
        )

class ClaudeAPIException(MCPError):
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_type="claude_api_error",
            message=message,
            status_code=status_code,
            details=details
        )

class ValidationError(MCPError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            error_type="validation_error",
            message=message,
            status_code=400,
            details=details
        )
