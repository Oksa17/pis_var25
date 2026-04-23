from src.application.query.get_recipe_by_id_query import GetRecipeByIdQuery
from src.application.query.dto.recipe_dto import RecipeDTO


class GetRecipeByIdHandler:
    """Обработчик запроса получения рецепта по ID"""

    def __init__(self, recipe_repository):
        self._recipe_repository = recipe_repository

    def handle(self, query: GetRecipeByIdQuery) -> RecipeDTO:
        recipe = self._recipe_repository.find_by_id(query.recipe_id)

        if not recipe:
            return None

        return RecipeDTO(
            id=recipe.id,
            user_id=recipe.user_id,
            name=recipe.name,
            ingredients=[i.name for i in recipe.ingredients],
            steps=[step.get_display_text() for step in recipe.steps],
            status=recipe.status.value,
            source=recipe.source,
            rating=recipe.rating,
            created_at=recipe.created_at
        )
