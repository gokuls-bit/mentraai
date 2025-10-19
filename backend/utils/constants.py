# utils/constants.py
"""
Contains constants, thresholds, and configuration keys
used throughout Mantra AI backend.
"""

# Database
DEFAULT_DB = "mantra_ai"
DEFAULT_COLLECTION = "users"

# Emotion scale thresholds
MOOD_THRESHOLDS = {
    "low": 0,
    "moderate": 50,
    "high": 80
}

# Progress tracking
PROGRESS_DEFAULTS = {
    "required_minutes_per_day": 10,
    "lookback_days": 30
}

# General App Info
APP_NAME = "Mantra AI"
APP_VERSION = "1.0.0"
