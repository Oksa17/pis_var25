import pytest
from datetime import date, datetime
from domain.value_objects.ingredient import Ingredient
from domain.value_objects.recipe_status import RecipeStatus
from domain.value_objects.cooking_step import CookingStep
from domain.value_objects.cooking_time import CookingTime


class TestIngredient:
    def test_invalid_name_raises_error(self):
        with pytest.raises(ValueError, match="Название ингредиента не может быть пустым"):
            Ingredient(name="")
    
    def test_expired_ingredient(self):
        ingredient = Ingredient(name="молоко", expiry_date=date(2020, 1, 1))
        assert ingredient.is_expired() is True
    
    def test_fresh_ingredient(self):
        ingredient = Ingredient(name="молоко", expiry_date=date(2099, 1, 1))
        assert ingredient.is_expired() is False
    
    def test_ingredient_immutable(self):
        ingredient = Ingredient(name="соль")
        with pytest.raises(Exception):
            ingredient.name = "перец"  # frozen=True запрещает изменение


class TestRecipeStatus:
    def test_valid_transition(self):
        assert RecipeStatus.DRAFT.can_transition_to(RecipeStatus.GENERATED) is True
    
    def test_invalid_transition(self):
        assert RecipeStatus.GENERATED.can_transition_to(RecipeStatus.DRAFT) is False
    
    def test_archived_no_transitions(self):
        assert RecipeStatus.ARCHIVED.can_transition_to(RecipeStatus.GENERATED) is False


class TestCookingStep:
    def test_invalid_order_raises_error(self):
        with pytest.raises(ValueError, match="Номер шага должен быть положительным"):
            CookingStep(order=0, description="шаг")
    
    def test_display_text_with_duration(self):
        step = CookingStep(order=1, description="Порезать лук", duration_minutes=5)
        assert step.get_display_text() == "1. Порезать лук (⏱️ 5 мин)"


class TestCookingTime:
    def test_negative_duration_raises_error(self):
        with pytest.raises(ValueError):
            CookingTime(start_time=datetime.now(), estimated_duration_minutes=-10)
    
    def test_get_end_time(self):
        start = datetime(2026, 1, 1, 12, 0)
        cooking_time = CookingTime(start_time=start, estimated_duration_minutes=30)
        assert cooking_time.get_end_time() == datetime(2026, 1, 1, 12, 30)
