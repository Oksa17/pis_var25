from src.application.query.get_popular_recipes_query import GetPopularRecipesQuery
from src.application.query.dto.recipe_dto import RecipeDTO


class GetPopularRecipesHandler:
    """Обработчик запроса популярных рецептов"""

    def __init__(self, recipe_repository):
        self._recipe_repository = recipe_repository

    def handle(self, query: GetPopularRecipesQuery):
        # 1. Получить все рецепты
        all_recipes = self._recipe_repository.find_all()

        # 2. Фильтр по рейтингу
        filtered = [r for r in all_recipes if r.rating and r.rating >= query.min_rating]

        # 3. Сортировка по рейтингу (высшие оценки сверху)
        sorted_recipes = sorted(filtered, key=lambda r: r.rating or 0, reverse=True)

        # 4. Лимит
        limited = sorted_recipes[:query.limit]

        # 5. Конвертация в DTO
        return [
            RecipeDTO(
                id=r.id,
                user_id=r.user_id,
                name=r.name,
                ingredients=[i.name for i in r.ingredients],
                steps=[step.get_display_text() for step in r.steps],
                status=r.status.value,
                source=r.source,
                rating=r.rating,
                created_at=r.created_at
            )
            for r in limited
        ]
