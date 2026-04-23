from dataclasses import dataclass


@dataclass(frozen=True)
class GetPopularRecipesQuery:
    """Запрос: получить популярные рецепты"""
    limit: int = 10
    min_rating: int = 4
