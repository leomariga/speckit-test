"""Conversion endpoints."""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, Literal
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...db.mongodb import get_db
from ...services.conversion_service import ConversionService
from .auth import get_current_user


router = APIRouter()


class ConversionRequest(BaseModel):
    """Request model for conversion tracking."""
    input_type: Literal["text", "file"]
    page_count: int
    conversion_method: Literal["client", "server"]
    input_file_name: Optional[str] = None
    input_file_size: Optional[int] = None


def get_conversion_service(db: AsyncIOMotorDatabase = Depends(get_db)) -> ConversionService:
    """Dependency for conversion service."""
    return ConversionService(db)


@router.post("/conversions")
async def track_conversion(
    request: ConversionRequest,
    current_user: dict = Depends(get_current_user),
    conversion_service: ConversionService = Depends(get_conversion_service),
):
    """
    Track a conversion and enforce plan limits.
    
    This endpoint should be called after client-side PDF generation
    to track the conversion and update the user's page count.
    """
    try:
        result = await conversion_service.track_conversion(
            user_id=str(current_user['_id']),
            input_type=request.input_type,
            page_count=request.page_count,
            conversion_method=request.conversion_method,
            input_file_name=request.input_file_name,
            input_file_size=request.input_file_size,
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Plan limit exceeded",
                    "message": result["error"],
                    **result["limit_info"]
                }
            )
        
        return {
            "message": "Conversion tracked successfully",
            "conversion_id": result["conversion_id"],
            "page_count": result["page_count"],
            "total_pages": result["total_pages"],
            "remaining_pages": result["remaining_pages"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to track conversion: {str(e)}"
        )


@router.get("/conversions/history")
async def get_conversion_history(
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    conversion_service: ConversionService = Depends(get_conversion_service),
):
    """
    Get user's conversion history.
    
    Returns paginated list of conversions.
    """
    try:
        history = await conversion_service.get_user_history(
            user_id=str(current_user['_id']),
            page=page,
            limit=limit
        )
        return history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch conversion history: {str(e)}"
        )

