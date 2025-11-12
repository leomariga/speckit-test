"""User MongoDB model and database operations."""
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional
from datetime import datetime


class UserDB:
    """User database operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.users
    
    async def create_indexes(self):
        """Create indexes for users collection."""
        await self.collection.create_index("email", unique=True)
        await self.collection.create_index("oauth_user_id", unique=True)
        await self.collection.create_index("plan_type")
    
    async def create_user(
        self,
        email: str,
        oauth_provider: str,
        oauth_user_id: str,
        plan_type: str = "free"
    ) -> dict:
        """Create a new user."""
        user_doc = {
            "email": email,
            "plan_type": plan_type,
            "total_pages_converted": 0,
            "account_created_at": datetime.utcnow(),
            "last_login_at": datetime.utcnow(),
            "oauth_provider": oauth_provider,
            "oauth_user_id": oauth_user_id,
        }
        
        result = await self.collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return user_doc
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        return await self.collection.find_one({"email": email})
    
    async def get_user_by_oauth_id(self, oauth_user_id: str) -> Optional[dict]:
        """Get user by OAuth user ID."""
        return await self.collection.find_one({"oauth_user_id": oauth_user_id})
    
    async def update_last_login(self, user_id: str):
        """Update user's last login timestamp."""
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login_at": datetime.utcnow()}}
        )
    
    async def update_pages_converted(self, user_id: str, page_count: int):
        """Update user's total pages converted."""
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"total_pages_converted": page_count}}
        )
    
    async def update_plan_type(self, user_id: str, plan_type: str):
        """Update user's plan type."""
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"plan_type": plan_type}}
        )

