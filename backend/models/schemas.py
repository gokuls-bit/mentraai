from pydantic import BaseModel, Field

class EmotionRequestText(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

class EmotionResponse(BaseModel):
    source: str  # "image" or "text"
    label: str
    confidence: float