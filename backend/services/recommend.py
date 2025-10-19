import asyncio
from typing import List, Dict

# Simple rule-based recommendation engine for skeleton
RECOMMENDATION_DB = {
    "happy": [
        {"id": "r1", "type": "lesson", "title": "Level up: Positive reinforcement", "description": "Short lesson on leveraging positive emotions", "difficulty": "easy"},
        {"id": "r2", "type": "quiz", "title": "Quick quiz: Confidence booster", "description": "5-question quiz", "difficulty": "easy"},
    ],
    "sad": [
        {"id": "r3", "type": "lesson", "title": "Growth mindset tips", "description": "Gentle lesson focusing on progress", "difficulty": "easy"},
        {"id": "r4", "type": "quiz", "title": "Reflection quiz", "description": "Self-reflection prompts", "difficulty": "easy"},
    ],
    "angry": [
        {"id": "r5", "type": "lesson", "title": "Managing frustration", "description": "Coping strategies lesson", "difficulty": "medium"},
    ],
    "neutral": [
        {"id": "r6", "type": "lesson", "title": "Adaptive practice", "description": "Balanced practice session", "difficulty": "medium"},
    ]
}

async def generate_recommendations(user_id: str, emotion: str, intensity: float) -> List[Dict]:
    await asyncio.sleep(0.01)
    key = emotion.lower()
    recs = RECOMMENDATION_DB.get(key, RECOMMENDATION_DB["neutral"])
    # Optionally adjust difficulty by intensity
    result = []
    for r in recs:
        item = r.copy()
        if intensity >= 0.8:
            # if intensity high, pick gentler content
            if item["difficulty"] == "medium":
                item["difficulty"] = "easy"
        result.append(item)
    return result