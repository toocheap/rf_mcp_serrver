from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class IOCData(BaseModel):
    type: str
    value: str
    risk_score: Optional[float] = None
    timestamps: Optional[Dict[str, str]] = None

class RFQueryResult(BaseModel):
    data: IOCData
    risk: Optional[Dict[str, Any]] = None
    timestamps: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None

class EnhancedContext(BaseModel):
    ioc_type: str
    original_value: str
    rf_data: RFQueryResult
