# utils/stats_utils.py
"""
Computes analytics and insights from emotion and progress data:
- Average mood score
- Learning streaks
- Improvement over time
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional

def average_mood(entries: List[Dict], window_days: int = 7) -> Optional[float]:
    """Compute average mood score within the past N days."""
    now = datetime.utcnow()
    cutoff = now - timedelta(days=window_days)
    scores = [e["mood_score"] for e in entries if e.get("timestamp") and e["timestamp"] >= cutoff]
    return round(sum(scores) / len(scores), 2) if scores else None

def daily_streak(entries: List[Dict], threshold: int = 10) -> int:
    """Count consecutive days with at least `threshold` minutes of learning."""
    today = datetime.utcnow().date()
    daily_minutes = {}
    for e in entries:
        if not e.get("timestamp"):
            continue
        date = e["timestamp"].date()
        daily_minutes[date] = daily_minutes.get(date, 0) + (e.get("duration_minutes") or 0)

    streak = 0
    while daily_minutes.get(today, 0) >= threshold:
        streak += 1
        today -= timedelta(days=1)
    return streak

def improvement(entries: List[Dict], key: str = "score") -> Optional[float]:
    """Estimate performance improvement percentage across progress entries."""
    valid = [e[key] for e in entries if isinstance(e.get(key), (int, float))]
    if len(valid) < 2 or valid[0] == 0:
        return None
    return round(((valid[-1] - valid[0]) / valid[0]) * 100, 2)
