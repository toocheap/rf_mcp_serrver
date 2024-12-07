from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Union, Dict, Any
from datetime import datetime
import uuid

class MessageContent(BaseModel):
    """メッセージコンテンツモデル（Anthropic Claude形式）"""
    type: str = Field(default="text", description="コンテンツタイプ（現在はtextのみ）")
    text: str = Field(..., description="メッセージのテキスト内容")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "text",
                    "text": "与えられたコードを分析してください。"
                }
            ]
        }
    }

class Message(BaseModel):
    """メッセージモデル（Anthropic Claude形式）"""
    role: str = Field(..., description="メッセージの役割（user/assistant）")
    content: Union[str, MessageContent] = Field(..., description="メッセージの内容")
    name: Optional[str] = Field(None, description="送信者の識別子（オプション）")

    @computed_field
    def text_content(self) -> str:
        """メッセージのテキスト内容を取得"""
        if isinstance(self.content, str):
            return self.content
        return self.content.text

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "role": "user",
                    "content": "与えられたコードを分析してください。"
                }
            ]
        }
    }

class MCPRequest(BaseModel):
    """Claude MCP リクエストモデル"""
    messages: List[Message] = Field(..., description="会話履歴")
    model: str = Field(default="claude-3-opus-20240229", description="使用するClaudeモデル")
    max_tokens: Optional[int] = Field(None, ge=0, le=4096, description="生成する最大トークン数（0-4096）")
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0, description="生成時の温度（0.0-1.0）")
    system: Optional[str] = Field(None, description="システムプロンプト")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="追加のメタデータ")

    @computed_field
    def message_count(self) -> int:
        """会話履歴のメッセージ数"""
        return len(self.messages)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {"role": "user", "content": "与えられたコードを分析してください。"}
                    ],
                    "model": "claude-3-opus-20240229",
                    "temperature": 0.7
                }
            ]
        }
    }

class Usage(BaseModel):
    """トークン使用量モデル（Anthropic Claude形式）"""
    input_tokens: int = Field(..., ge=0, description="入力トークン数")
    output_tokens: int = Field(..., ge=0, description="出力トークン数")

    @computed_field
    def total_tokens(self) -> int:
        """合計トークン数"""
        return self.input_tokens + self.output_tokens

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "input_tokens": 50,
                    "output_tokens": 200
                }
            ]
        }
    }

class MCPResponse(BaseModel):
    """Claude MCP レスポンスモデル"""
    id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4()}", description="メッセージID")
    type: str = Field(default="message", description="レスポンスタイプ")
    role: str = Field(default="assistant", description="応答者の役割")
    content: str = Field(..., min_length=1, description="応答メッセージ")
    model: str = Field(..., description="使用されたClaudeモデル")
    stop_reason: str = Field(default="end_turn", description="生成停止理由")
    stop_sequence: Optional[str] = Field(None, description="停止シーケンス")
    usage: Usage = Field(..., description="トークン使用量")

    @computed_field
    def timestamp(self) -> str:
        """メッセージのタイムスタンプ（ISO 8601形式）"""
        return datetime.utcnow().isoformat() + "Z"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "msg_12345",
                    "type": "message",
                    "role": "assistant",
                    "content": "コードを分析しました。",
                    "model": "claude-3-opus-20240229",
                    "stop_reason": "end_turn",
                    "usage": {
                        "input_tokens": 50,
                        "output_tokens": 200
                    }
                }
            ]
        }
    }
