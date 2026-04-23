from dataclasses import dataclass


@dataclass(frozen=True)
class RateRecipeCommand:
    """Команда: оценить рецепт"""
    recipe_id: str
    user_id: str
    rating: int  # от 1 до 5
