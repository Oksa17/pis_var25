from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class RecipeDTO:
    """DTO для передачи данных о рецепте"""
    id: str
    user_id: str
    name: str
    ingredients: List[str]
    steps: List[str]
    status: str
    source: str
    rating: Optional[int]
    created_at: datetime
