from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class WellnessRequest(BaseModel):
    detected_emotion: str
    intensity: float = 0.0

class WellnessSuggestion(BaseModel):
    id: str
    title: str
    description: str
    duration_minutes: int

# Simple in-router mapping; can be moved to service
EMOTION_SUGGESTIONS = {
    "sad": [
        {"id": "w1", "title": "2-min breathing", "description": "Short deep breathing exercise", "duration_minutes": 2},
        {"id": "w2", "title": "Gratitude journal", "description": "Write 3 things you're grateful for", "duration_minutes": 5},
    ],
    "angry": [
        {"id": "w3", "title": "Boxing breathing", "description": "4-4-4-4 breathing exercise", "duration_minutes": 3},
        {"id": "w4", "title": "Progressive muscle relax", "description": "Tense and release muscle groups", "duration_minutes": 8},
    ],
    "happy": [
        {"id": "w5", "title": "Mindful savoring", "description": "Notice pleasant details around you", "duration_minutes": 3}
    ],
    "neutral": [
        {"id": "w6", "title": "5-min stretch", "description": "Light full-body stretching", "duration_minutes": 5}
    ]
}

@router.post("/", response_model=List[WellnessSuggestion])
async def get_wellness(req: WellnessRequest):
    try:
        key = req.detected_emotion.lower()
        suggestions = EMOTION_SUGGESTIONS.get(key, EMOTION_SUGGESTIONS["neutral"])
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))