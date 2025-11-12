"""User account endpoints."""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...db.mongodb import get_db
from ...models.user import UserAccountResponse
from ...models.plan import get_plan_limits
from ...services.plan_service import PlanService
from .auth import get_current_user


router = APIRouter()


def get_plan_service() -> PlanService:
    """Dependency for plan service."""
    return PlanService()


@router.get("/users/account", response_model=UserAccountResponse)
async def get_user_account(
    current_user: dict = Depends(get_current_user),
    plan_service: PlanService = Depends(get_plan_service),
):
    """
    Get user account information including plan and usage details.
    """
    # Get plan limits
    plan_info = get_plan_limits(current_user["plan_type"])
    
    # Calculate remaining pages
    remaining_pages = plan_service.get_remaining_pages(
        current_user["plan_type"],
        current_user["total_pages_converted"]
    )
    
    return {
        "id": str(current_user['_id']),
        "email": current_user['email'],
        "plan_type": current_user['plan_type'],
        "total_pages_converted": current_user['total_pages_converted'],
        "account_created_at": current_user['account_created_at'],
        "last_login_at": current_user.get('last_login_at'),
        "plan_limits": {
            "min": plan_info["min_page_limit"],
            "max": plan_info["max_page_limit"],
        },
        "remaining_pages": remaining_pages,
    }

