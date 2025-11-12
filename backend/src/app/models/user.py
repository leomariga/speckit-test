"""User Pydantic models."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    plan_type: Literal["free", "premium"] = "free"


class UserCreate(UserBase):
    """Model for creating a user."""
    oauth_provider: str = "google"
    oauth_user_id: str


class UserResponse(UserBase):
    """Model for user response."""
    id: str
    total_pages_converted: int = 0
    account_created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class UserAccountResponse(UserResponse):
    """Extended user response with plan information."""
    plan_limits: dict
    remaining_pages: int

