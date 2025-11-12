"""Conversion Pydantic model."""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId


class ConversionBase(BaseModel):
    """Base conversion model."""
    input_type: Literal["text", "file"]
    input_content: Optional[str] = None
    input_file_name: Optional[str] = None
    input_file_size: Optional[int] = None
    page_count: int = Field(ge=1)
    conversion_method: Literal["client", "server"]
    status: Literal["success", "failed"]
    error_message: Optional[str] = None


class ConversionCreate(ConversionBase):
    """Model for creating a conversion."""
    user_id: str


class ConversionResponse(ConversionBase):
    """Model for conversion response."""
    id: str
    user_id: str
    converted_at: datetime
    pdf_file_reference: Optional[str] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class ConversionDB(ConversionBase):
    """Database model for conversion."""
    user_id: ObjectId
    converted_at: datetime
    pdf_file_reference: Optional[str] = None

