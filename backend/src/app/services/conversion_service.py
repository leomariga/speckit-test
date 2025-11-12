"""Conversion service for tracking conversions and updating user page counts."""
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..db.models.user import UserDB
from ..db.models.conversion import ConversionDB
from ..services.plan_service import PlanService


class ConversionService:
    """Service for managing conversions and page count tracking."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.user_db = UserDB(db)
        self.conversion_db = ConversionDB(db)
        self.plan_service = PlanService()
    
    async def track_conversion(
        self,
        user_id: str,
        input_type: str,
        page_count: int,
        conversion_method: str,
        input_content: Optional[str] = None,
        input_file_name: Optional[str] = None,
        input_file_size: Optional[int] = None,
    ) -> dict:
        """
        Track a conversion and update user's page count.
        
        This should be called after successful PDF generation.
        """
        # Get user to verify plan limits
        user = await self.user_db.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check plan limits
        limit_check = self.plan_service.check_page_limit(
            user["plan_type"],
            user["total_pages_converted"],
            page_count
        )
        
        if not limit_check["allowed"]:
            # Create failed conversion record
            conversion = await self.conversion_db.create_conversion(
                user_id=user_id,
                input_type=input_type,
                input_content=input_content if input_type == "text" else None,
                input_file_name=input_file_name if input_type == "file" else None,
                input_file_size=input_file_size if input_type == "file" else None,
                page_count=page_count,
                conversion_method=conversion_method,
                status="failed",
                error_message=limit_check["reason"],
            )
            
            return {
                "success": False,
                "error": limit_check["reason"],
                "limit_info": limit_check,
                "conversion_id": str(conversion["_id"]),
            }
        
        # Create successful conversion record
        conversion = await self.conversion_db.create_conversion(
            user_id=user_id,
            input_type=input_type,
            input_content=input_content if input_type == "text" else None,
            input_file_name=input_file_name if input_type == "file" else None,
            input_file_size=input_file_size if input_type == "file" else None,
            page_count=page_count,
            conversion_method=conversion_method,
            status="success",
        )
        
        # Update user's total pages converted
        await self.user_db.update_pages_converted(user_id, page_count)
        
        return {
            "success": True,
            "conversion_id": str(conversion["_id"]),
            "page_count": page_count,
            "total_pages": user["total_pages_converted"] + page_count,
            "remaining_pages": limit_check["remaining"] - page_count,
        }
    
    async def get_user_history(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 20
    ) -> dict:
        """Get conversion history for a user."""
        skip = (page - 1) * limit
        
        conversions = await self.conversion_db.get_user_conversions(
            user_id, skip=skip, limit=limit
        )
        
        total = await self.conversion_db.count_user_conversions(user_id)
        
        # Format conversions
        formatted_conversions = []
        for conv in conversions:
            formatted_conversions.append({
                "id": str(conv["_id"]),
                "input_type": conv["input_type"],
                "input_file_name": conv.get("input_file_name"),
                "page_count": conv["page_count"],
                "conversion_method": conv["conversion_method"],
                "status": conv["status"],
                "error_message": conv.get("error_message"),
                "converted_at": conv["converted_at"].isoformat(),
            })
        
        return {
            "conversions": formatted_conversions,
            "total": total,
            "page": page,
            "limit": limit,
        }

