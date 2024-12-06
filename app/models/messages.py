from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict
from datetime import datetime
import uuid

class MessageContent(BaseModel):
    type: str = "text"
    text: str

class Message(BaseModel):
    role: str
    content: Union[str, MessageContent]
    name: Optional[str] = None

    def get_text(self) -> str:
        if isinstance(self.content, str):
            return self.content
        return self.content.text

class MCPRequest(BaseModel):
    messages: List[Message]
    model: str = "claude-3-opus-20240229"
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    system: Optional[str] = None

class Usage(BaseModel):
    input_tokens: int
    output_tokens: int

class MCPResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4()}")
    type: str = "message"
    role: str = "assistant"
    content: str
    model: str
    stop_reason: str = "end_turn"
    stop_sequence: Optional[str] = None
    usage: Usage
