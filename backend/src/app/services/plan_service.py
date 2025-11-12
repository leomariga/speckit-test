"""Plan service for limit checking and enforcement."""
from fastapi import HTTPException, status
from ..models.plan import PLANS, get_plan_limits


class PlanService:
    """Service for handling plan limits and enforcement."""
    
    def get_plan_info(self, plan_type: str) -> dict:
        """Get plan information."""
        return get_plan_limits(plan_type)
    
    def check_page_limit(self, plan_type: str, current_pages: int, requested_pages: int) -> dict:
        """
        Check if user can convert requested pages without exceeding limit.
        
        Returns dict with:
        - allowed: bool - whether conversion is allowed
        - reason: str - reason if not allowed
        - limit: int - plan page limit
        - current: int - current pages converted
        - requested: int - requested pages
        - remaining: int - remaining pages available
        """
        plan = self.get_plan_info(plan_type)
        max_limit = plan["max_page_limit"]
        
        # Calculate total after conversion
        total_after = current_pages + requested_pages
        
        # For free plan, limit is exclusive (<20)
        # For premium plan, limit is inclusive (<=500)
        if plan_type == "free":
            allowed = total_after < max_limit
        else:
            allowed = total_after <= max_limit
        
        remaining = max(0, max_limit - current_pages)
        
        return {
            "allowed": allowed,
            "reason": f"{plan_type.capitalize()} plan limit of {max_limit} pages reached" if not allowed else "",
            "limit": max_limit,
            "current": current_pages,
            "requested": requested_pages,
            "remaining": remaining,
        }
    
    def get_remaining_pages(self, plan_type: str, current_pages: int) -> int:
        """Get remaining pages available for user."""
        plan = self.get_plan_info(plan_type)
        max_limit = plan["max_page_limit"]
        return max(0, max_limit - current_pages)

