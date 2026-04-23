import pytest
from datetime import datetime
from domain.entities.user import User
from domain.entities.recipe import Recipe
from domain.value_objects.ingredient import Ingredient
from domain.value_objects.recipe_status import RecipeStatus
from domain.value_objects.cooking_step import CookingStep


class TestUser:
    def test_user_equality_by_id(self):
        user1 = User(id="123", email="test@mail.com", name="Test")
        user2 = User(id="123", email="other@mail.com", name="Other")
        assert user1 == user2
    
    def test_can_generate_recipe_within_limit(self):
        user = User(id="1", email="a@b.com", name="A")
        assert user.can_generate_recipe(limit=2) is True
    
    def test_limit_exceeded(self):
        user = User(id="1", email="a@b.com", name="A")
        for _ in range(11):
            user.add_generation_request()
        assert user.can_generate_recipe(limit=10) is False


class TestRecipe:
    def test_generate_recipe_from_draft(self):
        recipe = Recipe(
            user_id="1",
            name="Гренки",
            ingredients=[Ingredient(name="хлеб")],
            steps=[CookingStep(order=1, description="Порезать")]
        )
        recipe.generate()
        assert recipe.status == RecipeStatus.GENERATED
    
    def test_cannot_generate_recipe_without_ingredients(self):
        recipe = Recipe(user_id="1", name="Пусто", ingredients=[], steps=[])
        with pytest.raises(ValueError, match="без ингредиентов"):
            recipe.generate()
    
    def test_cannot_start_cooking_from_wrong_status(self):
        recipe = Recipe(user_id="1", name="Тест", ingredients=[], steps=[])
        with pytest.raises(ValueError, match="Нельзя начать готовку"):
            recipe.start_cooking()
    
    def test_complete_cooking_flow(self):
        recipe = Recipe(
            user_id="1",
            name="Гренки",
            ingredients=[Ingredient(name="хлеб")],
            steps=[CookingStep(order=1, description="Порезать")]
        )
        recipe.generate()
        recipe.start_cooking()
        recipe.complete_cooking()
        assert recipe.status == RecipeStatus.COMPLETED
    
    def test_cannot_archive_unfinished_recipe(self):
        recipe = Recipe(user_id="1", name="Тест", ingredients=[], steps=[])
        recipe.generate()
        with pytest.raises(ValueError, match="Нельзя архивировать"):
            recipe.archive()
