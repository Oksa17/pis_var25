from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class RecipeGeneratedEvent:
    """Событие: Рецепт сгенерирован"""
    recipe_id: str
    user_id: str
    ingredient_names: List[str]
    occurred_at: datetime = datetime.now()
