from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Optional

from models.schemas import EmotionRequestText, EmotionResponse
from services.emotion_detector import analyze_image_emotion
from services.text_sentiment import analyze_text_sentiment

router = APIRouter()

@router.post("/image", response_model=EmotionResponse)
async def detect_emotion_image(file: UploadFile = File(...)):
    """
    Accepts an image file and returns detected emotion and confidence.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")
    try:
        content = await file.read()
        label, confidence = await analyze_image_emotion(content)
        return EmotionResponse(source="image", label=label, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text", response_model=EmotionResponse)
async def detect_emotion_text(payload: EmotionRequestText):
    """
    Accepts text and returns sentiment/emotion label + confidence
    """
    try:
        label, confidence = await analyze_text_sentiment(payload.text)
        return EmotionResponse(source="text", label=label, confidence=confidence)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))