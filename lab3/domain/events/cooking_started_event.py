from dataclasses import dataclass
from datetime import datetime


@dataclass
class CookingStartedEvent:
    """Событие: Начало готовки"""
    recipe_id: str
    user_id: str
    estimated_minutes: int
    started_at: datetime = datetime.now()
