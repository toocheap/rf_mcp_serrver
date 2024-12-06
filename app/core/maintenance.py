from typing import Set
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config import get_logger

logger = get_logger()

class MaintenanceMode:
    def __init__(self):
        self._is_active: bool = False
        self._allowed_paths: Set[str] = {"/health"}

    @property
    def is_active(self) -> bool:
        return self._is_active

    def activate(self):
        self._is_active = True
        logger.warning("Maintenance mode activated")

    def deactivate(self):
        self._is_active = False
        logger.warning("Maintenance mode deactivated")

    def is_path_allowed(self, path: str) -> bool:
        return path in self._allowed_paths

maintenance = MaintenanceMode()

def setup_maintenance_middleware(app: FastAPI):
    @app.middleware("http")
    async def maintenance_middleware(request: Request, call_next):
        if maintenance.is_active and not maintenance.is_path_allowed(request.url.path):
            return JSONResponse(
                status_code=503,
                content={
                    "error": "System under maintenance",
                    "type": "maintenance_error",
                    "message": "The system is currently under maintenance"
                }
            )
        return await call_next(request)
