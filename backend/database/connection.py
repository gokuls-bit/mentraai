# database/connection.py
"""
Handles MongoDB connection using Motor (async driver).
Creates a single cached connection for all operations.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB", "mantra_ai")

@lru_cache(maxsize=1)
def get_client() -> AsyncIOMotorClient:
    """
    Create a cached MongoDB client.
    This prevents creating multiple connections per request.
    """
    return AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)

def get_db():
    """
    Return the active MongoDB database object.
    """
    client = get_client()
    return client[DB_NAME]

def get_collection(name: str):
    """
    Return a MongoDB collection handle.
    """
    db = get_db()
    return db[name]
