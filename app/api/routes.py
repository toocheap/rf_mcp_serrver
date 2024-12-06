from fastapi import APIRouter, Request, Depends, HTTPException
from app.models.messages import MCPRequest, MCPResponse
from app.services import RFClient, ClaudeClient, ContextEnhancer, RFCache
from app.core.exceptions import MCPError
from config import get_logger, get_settings
from typing import Dict

router = APIRouter()
logger = get_logger()
settings = get_settings()

# サービスの初期化
rf_cache = RFCache()
rf_client = RFClient(rf_cache)
claude_client = ClaudeClient()
context_enhancer = ContextEnhancer(rf_client)

@router.post("/v1/messages", response_model=MCPResponse)
async def create_message(request: Request, mcp_request: MCPRequest):
    request_id = request.state.request_id
    logger.info(f"Processing message request", extra={"request_id": request_id})

    try:
        # メッセージの強化
        enhanced_messages = await context_enhancer.enhance_messages(mcp_request.messages)

        # Claudeでの処理
        response = await claude_client.create_message(
            messages=enhanced_messages,
            model=mcp_request.model,
            max_tokens=mcp_request.max_tokens,
            temperature=mcp_request.temperature
        )

        logger.info(
            "Message processed successfully",
            extra={
                "request_id": request_id,
                "model": mcp_request.model
            }
        )

        return response

    except MCPError as e:
        logger.error(
            f"MCP error while processing message: {str(e)}",
            extra={"request_id": request_id, "error_type": e.error_type}
        )
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        logger.error(
            f"Unexpected error while processing message: {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check(request: Request) -> Dict:
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "cache_stats": {
            "ip": len(rf_cache.ip_cache),
            "domain": len(rf_cache.domain_cache),
            "vulnerability": len(rf_cache.vulnerability_cache)
        }
    }
