from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from services.recommend import generate_recommendations

router = APIRouter()

class AdaptiveRequest(BaseModel):
    user_id: str
    detected_emotion: str
    intensity: float = 0.0  # 0.0 - 1.0

class Recommendation(BaseModel):
    id: str
    type: str  # "quiz" | "lesson"
    title: str
    description: str
    difficulty: str

@router.post("/", response_model=List[Recommendation])
async def get_adaptive_content(req: AdaptiveRequest):
    try:
        recs = await generate_recommendations(req.user_id, req.detected_emotion, req.intensity)
        return recs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))