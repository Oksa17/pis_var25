import pytest
from datetime import datetime
from domain.aggregates.cooking_session import CookingSession
from domain.entities.user import User
from domain.value_objects.ingredient import Ingredient
from domain.value_objects.cooking_step import CookingStep
from domain.entities.recipe import Recipe


class TestCookingSession:
    def test_generate_recipe_success(self):
        session = CookingSession()
        user = User(id="1", email="test@mail.com", name="Test")
        ingredients = [Ingredient(name="хлеб"), Ingredient(name="яйца")]
        
        recipe = session.generate_recipe(user, ingredients)
        
        assert recipe is not None
        assert len(session.get_events()) == 1
    
    def test_cannot_generate_with_empty_ingredients(self):
        session = CookingSession()
        user = User(id="1", email="test@mail.com", name="Test")
        
        with pytest.raises(ValueError, match="без ингредиентов"):
            session.generate_recipe(user, [])
    
    def test_cannot_generate_exceeding_limit(self):
        session = CookingSession()
        user = User(id="1", email="test@mail.com", name="Test")
        
        for _ in range(10):
            user.add_generation_request()
        
        with pytest.raises(ValueError, match="Превышен лимит"):
            session.generate_recipe(user, [Ingredient(name="хлеб")])
    
    def test_start_cooking_success(self):
        session = CookingSession()
        user = User(id="1", email="test@mail.com", name="Test")
        recipe = Recipe(
            user_id="1",
            name="Гренки",
            ingredients=[Ingredient(name="хлеб")],
            steps=[CookingStep(order=1, description="Порезать")]
        )
        recipe.generate()
        
        session.start_cooking(recipe, estimated_minutes=15)
        
        assert session.cooking_time is not None
        assert len(session.get_events()) == 1
    
    def test_complete_step_sequential(self):
        session = CookingSession()
        user = User(id="1", email="test@mail.com", name="Test")
        recipe = Recipe(
            user_id="1",
            name="Гренки",
            ingredients=[Ingredient(name="хлеб")],
            steps=[
                CookingStep(order=1, description="Порезать"),
                CookingStep(order=2, description="Обжарить")
            ]
        )
        recipe.generate()
        session.start_cooking(recipe, estimated_minutes=15)
        
        session.complete_step(1)
        assert 1 in session.completed_steps
        
        session.complete_step(2)
        assert len(session.completed_steps) == 2
        assert recipe.status.value == "завершён"
    
    def test_cannot_complete_step_out_of_order(self):
        session = CookingSession()
        user = User(id="1", email="test@mail.com", name="Test")
        recipe = Recipe(
            user_id="1",
            name="Гренки",
            ingredients=[Ingredient(name="хлеб")],
            steps=[
                CookingStep(order=1, description="Порезать"),
                CookingStep(order=2, description="Обжарить")
            ]
        )
        recipe.generate()
        session.start_cooking(recipe, estimated_minutes=15)
        
        with pytest.raises(ValueError, match="по порядку"):
            session.complete_step(2)
