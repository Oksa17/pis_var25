from src.application.query.get_user_history_query import GetUserHistoryQuery
from src.application.query.dto.recipe_dto import RecipeDTO


class GetUserHistoryHandler:
    """Обработчик запроса истории рецептов пользователя"""

    def __init__(self, recipe_repository):
        self._recipe_repository = recipe_repository

    def handle(self, query: GetUserHistoryQuery):
        # 1. Получить рецепты пользователя
        recipes = self._recipe_repository.find_by_user_id(query.user_id)

        # 2. Фильтр по статусу
        if query.status_filter:
            recipes = [r for r in recipes if r.status.value == query.status_filter]

        # 3. Сортировка по дате (новые сверху)
        recipes = sorted(recipes, key=lambda r: r.created_at, reverse=True)

        # 4. Пагинация
        paginated = recipes[query.offset:query.offset + query.limit]

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
            for r in paginated
        ]
