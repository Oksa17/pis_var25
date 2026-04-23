from dataclasses import dataclass


@dataclass(frozen=True)
class GetRecipeByIdQuery:
    """Запрос: получить рецепт по ID"""
    recipe_id: str
