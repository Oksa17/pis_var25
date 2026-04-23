from dataclasses import dataclass


@dataclass(frozen=True)
class StartCookingCommand:
    """Команда: начать приготовление рецепта"""
    recipe_id: str
    user_id: str
    estimated_minutes: int
