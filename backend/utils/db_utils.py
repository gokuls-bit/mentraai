# utils/db_utils.py
"""
Async database utility functions for CRUD operations on user, emotion,
and progress data. Uses Motor without any ORM.
"""

from datetime import datetime
from typing import Dict, Optional, List
from database.connection import get_collection
from user_model import EmotionEntry, ProgressEntry
from utils.logger import get_logger

logger = get_logger(__name__)
COLLECTION_NAME = "users"

# ---------------- User Operations ---------------- #

async def create_user(user_data: Dict) -> Dict:
    """Insert a new user document."""
    coll = get_collection(COLLECTION_NAME)
    user_data.setdefault("created_at", datetime.utcnow())
    user_data.setdefault("last_active", datetime.utcnow())
    res = await coll.insert_one(user_data)
    logger.info(f"New user created with _id={res.inserted_id}")
    return await coll.find_one({"_id": res.inserted_id})

async def get_user(user_id: str) -> Optional[Dict]:
    """Fetch user by platform user_id."""
    coll = get_collection(COLLECTION_NAME)
    return await coll.find_one({"user_id": user_id})

async def update_user_profile(user_id: str, patch: Dict) -> Optional[Dict]:
    """Update user profile information."""
    coll = get_collection(COLLECTION_NAME)
    return await coll.find_one_and_update(
        {"user_id": user_id},
        {"$set": {"profile": patch, "last_active": datetime.utcnow()}},
        return_document=True
    )

# ---------------- Emotion Entries ---------------- #

async def insert_emotion(user_id: str, entry: EmotionEntry) -> Optional[Dict]:
    """Append a new emotion entry for a user."""
    coll = get_collection(COLLECTION_NAME)
    res = await coll.find_one_and_update(
        {"user_id": user_id},
        {"$push": {"emotion_entries": entry.dict()}, "$set": {"last_active": datetime.utcnow()}},
        return_document=True
    )
    logger.info(f"Emotion logged for {user_id}")
    return res

async def fetch_emotions(user_id: str, limit: int = 50) -> List[Dict]:
    """Fetch recent emotion entries."""
    coll = get_collection(COLLECTION_NAME)
    doc = await coll.find_one({"user_id": user_id}, {"emotion_entries": {"$slice": -limit}})
    return doc.get("emotion_entries", []) if doc else []

# ---------------- Progress Entries ---------------- #

async def insert_progress(user_id: str, entry: ProgressEntry) -> Optional[Dict]:
    """Add a learning progress entry."""
    coll = get_collection(COLLECTION_NAME)
    res = await coll.find_one_and_update(
        {"user_id": user_id},
        {"$push": {"progress_entries": entry.dict()}, "$set": {"last_active": datetime.utcnow()}},
        return_document=True
    )
    logger.info(f"Progress updated for {user_id}")
    return res

async def fetch_progress(user_id: str, limit: int = 50) -> List[Dict]:
    """Fetch recent progress entries."""
    coll = get_collection(COLLECTION_NAME)
    doc = await coll.find_one({"user_id": user_id}, {"progress_entries": {"$slice": -limit}})
    return doc.get("progress_entries", []) if doc else []
