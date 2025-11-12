"""Health check endpoint."""
from fastapi import APIRouter, Depends
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...db.mongodb import get_db

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Health check endpoint.
    
    Returns API health status and database connectivity.
    """
    # Check database connection
    try:
        await db.command("ping")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
    }

