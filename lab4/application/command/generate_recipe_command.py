from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GenerateRecipeCommand:
    """Команда: сгенерировать рецепт из ингредиентов"""
    user_id: str
    ingredient_names: List[str]
