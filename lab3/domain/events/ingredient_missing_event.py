from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class IngredientMissingEvent:
    """Событие: Отсутствует ингредиент"""
    recipe_id: str
    missing_ingredient: str
    available_ingredients: List[str]
    occurred_at: datetime = datetime.now()
