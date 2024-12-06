import httpx
from typing import List, Dict, Optional
from config import get_settings, get_logger
from app.core.exceptions import ClaudeAPIException
from app.models.messages import Message, MCPResponse, Usage

settings = get_settings()
logger = get_logger()

class ClaudeClient:
    def __init__(self):
        self.base_url = settings.CLAUDE_API_BASE_URL
        self.api_key = settings.CLAUDE_API_KEY
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2024-01-01"
            },
            timeout=60.0
        )

    async def create_message(
        self,
        messages: List[Message],
        model: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> MCPResponse:
        try:
            response = await self.client.post(
                "/messages",
                json={
                    "messages": [
                        {"role": msg.role, "content": msg.get_text()}
                        for msg in messages
                    ],
                    "model": model,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            response.raise_for_status()
            data = response.json()

            return MCPResponse(
                content=data["content"][0]["text"],
                model=model,
                usage=Usage(
                    input_tokens=data["usage"]["input_tokens"],
                    output_tokens=data["usage"]["output_tokens"]
                )
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"Claude API error: {str(e)}")
            raise ClaudeAPIException(str(e), status_code=e.response.status_code)
        except Exception as e:
            logger.error(f"Unexpected error in Claude API request: {str(e)}")
            raise ClaudeAPIException(str(e))
