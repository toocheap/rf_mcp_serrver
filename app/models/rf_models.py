from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IOCData(BaseModel):
    """IOC（Indicator of Compromise）データモデル"""
    type: str = Field(..., description="IOCのタイプ（例：IP、ドメイン、CVE）")
    value: str = Field(..., description="IOCの実際の値")
    risk_score: Optional[float] = Field(None, description="リスクスコア（0-100）")
    timestamps: Optional[Dict[str, str]] = Field(None, description="関連する時間情報")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "ip",
                    "value": "192.0.2.1",
                    "risk_score": 85.5,
                    "timestamps": {"first_seen": "2024-01-01T00:00:00Z"}
                }
            ]
        }
    }

class RFQueryResult(BaseModel):
    """Recorded Futureクエリ結果モデル"""
    data: IOCData = Field(..., description="IOCの基本データ")
    risk: Optional[Dict[str, Any]] = Field(None, description="リスク関連の詳細情報")
    timestamps: Optional[Dict[str, Any]] = Field(None, description="時間関連の詳細情報")
    metrics: Optional[Dict[str, Any]] = Field(None, description="メトリクス関連の詳細情報")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": {
                        "type": "ip",
                        "value": "192.0.2.1",
                        "risk_score": 85.5
                    },
                    "risk": {"rules_triggered": 5},
                    "timestamps": {"last_updated": "2024-03-01T00:00:00Z"},
                    "metrics": {"references": 10}
                }
            ]
        }
    }

class EnhancedContext(BaseModel):
    """強化されたコンテキスト情報モデル"""
    ioc_type: str = Field(..., description="IOCのタイプ")
    original_value: str = Field(..., description="元のIOC値")
    rf_data: RFQueryResult = Field(..., description="Recorded Futureからの詳細データ")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ioc_type": "ip",
                    "original_value": "192.0.2.1",
                    "rf_data": {
                        "data": {
                            "type": "ip",
                            "value": "192.0.2.1",
                            "risk_score": 85.5
                        },
                        "risk": {"rules_triggered": 5}
                    }
                }
            ]
        }
    }
