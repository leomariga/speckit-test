"""Conversion MongoDB model and database operations."""
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional, List
from datetime import datetime


class ConversionDB:
    """Conversion database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.conversions
    
    async def create_indexes(self):
        """Create indexes for conversions collection."""
        await self.collection.create_index("user_id")
        await self.collection.create_index("converted_at")
        await self.collection.create_index("status")
    
    async def create_conversion(
        self,
        user_id: str,
        input_type: str,
        input_content: Optional[str],
        input_file_name: Optional[str],
        input_file_size: Optional[int],
        page_count: int,
        conversion_method: str,
        status: str,
        error_message: Optional[str] = None,
    ) -> dict:
        """Create a new conversion record."""
        conversion_doc = {
            "user_id": ObjectId(user_id),
            "input_type": input_type,
            "input_content": input_content,
            "input_file_name": input_file_name,
            "input_file_size": input_file_size,
            "page_count": page_count,
            "conversion_method": conversion_method,
            "status": status,
            "error_message": error_message,
            "converted_at": datetime.utcnow(),
            "pdf_file_reference": None,
        }
        
        result = await self.collection.insert_one(conversion_doc)
        conversion_doc["_id"] = result.inserted_id
        return conversion_doc
    
    async def get_user_conversions(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[dict]:
        """Get conversions for a specific user."""
        cursor = self.collection.find(
            {"user_id": ObjectId(user_id)}
        ).sort("converted_at", -1).skip(skip).limit(limit)
        
        return await cursor.to_list(length=limit)
    
    async def count_user_conversions(self, user_id: str) -> int:
        """Count total conversions for a user."""
        return await self.collection.count_documents({"user_id": ObjectId(user_id)})

