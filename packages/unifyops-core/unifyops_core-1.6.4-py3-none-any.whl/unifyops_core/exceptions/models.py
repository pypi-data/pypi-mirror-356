from uuid import uuid4
from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_serializer

class ErrorDetail(BaseModel):
    loc: Optional[List[str]]
    msg: str
    type: str
    code: Optional[str] = None

class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        # Enable serialization by alias and other modern features
        populate_by_name=True,
    )
    
    status_code: int
    error_id: str = Field(default_factory=lambda: str(uuid4()))
    message: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    error_type: str

    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime) -> str:
        """Serialize datetime to ISO format string"""
        return dt.isoformat() if dt else None
