"""Plan Pydantic models."""
from pydantic import BaseModel, Field
from typing import List, Literal


class PlanBase(BaseModel):
    """Base plan model."""
    plan_type: Literal["free", "premium"]
    min_page_limit: int = Field(ge=0)
    max_page_limit: int = Field(ge=1)
    features: List[str] = []
    description: str = ""


class PlanResponse(PlanBase):
    """Model for plan response."""
    pass


# Reference data for plans
PLANS = {
    "free": {
        "plan_type": "free",
        "min_page_limit": 0,
        "max_page_limit": 20,
        "features": ["basic_conversion"],
        "description": "Free plan with up to 20 pages"
    },
    "premium": {
        "plan_type": "premium",
        "min_page_limit": 20,
        "max_page_limit": 500,
        "features": ["basic_conversion", "large_documents", "priority_support"],
        "description": "Premium plan with up to 500 pages"
    }
}


def get_plan_limits(plan_type: str) -> dict:
    """Get plan limits for a given plan type."""
    return PLANS.get(plan_type, PLANS["free"])

