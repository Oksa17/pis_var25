import pytest
from unittest.mock import Mock

from src.application.command.generate_recipe_command import GenerateRecipeCommand
from src.application.command.handlers.generate_recipe_handler import GenerateRecipeHandler
from src.domain.entities.user import User
from src.domain.entities.recipe import Recipe
from src.domain.value_objects.ingredient import Ingredient
from src.domain.value_objects.cooking_step import CookingStep


class TestGenerateRecipeHandler:
    def test_handle_success(self):
        # Mock репозиториев
        mock_user_repo = Mock()
        mock_recipe_repo = Mock()
        mock_notification = Mock()

        # Создаём пользователя
        user = User(id="user-1", email="test@mail.com", name="Test")
        mock_user_repo.find_by_id.return_value = user

        # Создаём обработчик
        handler = GenerateRecipeHandler(
            mock_user_repo, mock_recipe_repo, mock_notification
        )

        # Выполняем команду
        command = GenerateRecipeCommand(
            user_id="user-1",
            ingredient_names=["хлеб", "яйца", "молоко"]
        )

        events = handler.handle(command)

        # Проверки
        assert len(events) == 1  # RecipeGeneratedEvent
        assert mock_recipe_repo.save.called
        assert mock_notification.notify.called

    def test_handle_user_not_found(self):
        mock_user_repo = Mock()
        mock_user_repo.find_by_id.return_value = None
        mock_recipe_repo = Mock()
        mock_notification = Mock()

        handler = GenerateRecipeHandler(
            mock_user_repo, mock_recipe_repo, mock_notification
        )

        command = GenerateRecipeCommand(
            user_id="user-xxx",
            ingredient_names=["хлеб"]
        )

        with pytest.raises(ValueError, match="Пользователь user-xxx не найден"):
            handler.handle(command)

    def test_handle_empty_ingredients(self):
        mock_user_repo = Mock()
        user = User(id="user-1", email="test@mail.com", name="Test")
        mock_user_repo.find_by_id.return_value = user

        handler = GenerateRecipeHandler(mock_user_repo, Mock(), Mock())

        command = GenerateRecipeCommand(user_id="user-1", ingredient_names=[])

        with pytest.raises(ValueError, match="без ингредиентов"):
            handler.handle(command)
