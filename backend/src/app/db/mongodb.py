"""MongoDB database connection and management."""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from ..config import settings


class MongoDB:
    """MongoDB connection manager."""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect_to_database(cls):
        """Connect to MongoDB."""
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db = cls.client[settings.MONGODB_DB]
        print(f"Connected to MongoDB: {settings.MONGODB_DB}")
    
    @classmethod
    async def close_database_connection(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            print("Closed MongoDB connection")
    
    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if not cls.db:
            raise Exception("Database not initialized. Call connect_to_database first.")
        return cls.db


# Database instance
mongodb = MongoDB()


def get_db() -> AsyncIOMotorDatabase:
    """Dependency for getting database instance."""
    return mongodb.get_database()

