
"""
Mantra AI - The Empathetic Learning Copilot
AI Models Package for Emotion and Mental Health Analysis
"""

from .emotion_detection.predict import predict_text_emotion
from .stress_analysis.predict import predict_stress_level

__version__ = "1.0.0"
__all__ = ["predict_text_emotion", "predict_stress_level"]