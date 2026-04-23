import pytest
from datetime import datetime
from unittest.mock import Mock

from src.application.query.get_recipe_by_id_query import GetRecipeByIdQuery
from src.application.query.handlers.get_recipe_by_id_handler import GetRecipeByIdHandler
from src.domain.entities.recipe import Recipe
from src.domain.value_objects.ingredient import Ingredient
from src.domain.value_objects.cooking_step import CookingStep


class TestGetRecipeByIdHandler:
    def test_handle_recipe_exists(self):
        # Mock репозитория
        mock_repo = Mock()
        recipe = Recipe(
            user_id="user-1",
            name="Гренки",
            ingredients=[Ingredient(name="хлеб")],
            steps=[CookingStep(order=1, description="Порезать хлеб")]
        )
        mock_repo.find_by_id.return_value = recipe

        handler = GetRecipeByIdHandler(mock_repo)
        query = GetRecipeByIdQuery(recipe_id=recipe.id)

        result = handler.handle(query)

        assert result is not None
        assert result.name == "Гренки"
        assert len(result.ingredients) == 1
        assert result.id == recipe.id

    def test_handle_recipe_not_found(self):
        mock_repo = Mock()
        mock_repo.find_by_id.return_value = None

        handler = GetRecipeByIdHandler(mock_repo)
        query = GetRecipeByIdQuery(recipe_id="non-existent")

        result = handler.handle(query)
        assert result is None


class TestGetUserHistoryHandler:
    def test_handle_success(self):
        mock_repo = Mock()
        recipes = [
            Recipe(user_id="user-1", name="Рецепт 1", ingredients=[], steps=[]),
            Recipe(user_id="user-1", name="Рецепт 2", ingredients=[], steps=[])
        ]
        mock_repo.find_by_user_id.return_value = recipes

        from src.application.query.get_user_history_query import GetUserHistoryQuery
        from src.application.query.handlers.get_user_history_handler import GetUserHistoryHandler

        handler = GetUserHistoryHandler(mock_repo)
        query = GetUserHistoryQuery(user_id="user-1", limit=10)

        results = handler.handle(query)

        assert len(results) == 2
        assert results[0].name == "Рецепт 2"  # сортировка по дате
