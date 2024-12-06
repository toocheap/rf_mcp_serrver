from fastapi import APIRouter, Request, Depends, HTTPException
from app.core.security import security_handler
from app.core.maintenance import maintenance
from config import get_logger
from typing import Dict

router = APIRouter(prefix="/admin", tags=["admin"])
logger = get_logger()

async def verify_admin(request: Request):
    if not await security_handler.validate_admin_token(request):
        raise HTTPException(
            status_code=401,
            detail="Invalid admin token"
        )

@router.post("/maintenance/start")
async def start_maintenance(request: Request, _=Depends(verify_admin)) -> Dict:
    maintenance.activate()
    logger.warning(
        "Maintenance mode activated",
        extra={"request_id": request.state.request_id}
    )
    return {"status": "Maintenance mode activated"}

@router.post("/maintenance/end")
async def end_maintenance(request: Request, _=Depends(verify_admin)) -> Dict:
    maintenance.deactivate()
    logger.warning(
        "Maintenance mode deactivated",
        extra={"request_id": request.state.request_id}
    )
    return {"status": "Maintenance mode deactivated"}

@router.post("/cache/clear")
async def clear_cache(request: Request, _=Depends(verify_admin)) -> Dict:
    from app.api.routes import rf_cache
    rf_cache.clear_all()
    logger.info(
        "Cache cleared by admin",
        extra={"request_id": request.state.request_id}
    )
    return {"status": "Cache cleared successfully"}
