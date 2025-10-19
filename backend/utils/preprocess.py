# utils/preprocess.py
"""
Preprocessing utilities for text-based or emotion data.
These are helpful for upcoming ML/NLP or AR-coaching modules.
"""

import re
from typing import Dict

def clean_text(text: str) -> str:
    """Clean text input for emotion analysis."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

def normalize_emotion_input(data: Dict) -> Dict:
    """Normalize mood label and fields in emotion payload."""
    if "mood_label" in data:
        data["mood_label"] = clean_text(data["mood_label"])
    return data
