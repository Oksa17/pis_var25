from datetime import datetime
from domain.events.recipe_generated_event import RecipeGeneratedEvent
from domain.events.cooking_started_event import CookingStartedEvent
from domain.events.step_completed_event import StepCompletedEvent
from domain.events.ingredient_missing_event import IngredientMissingEvent


class TestEvents:
    def test_recipe_generated_event_creation(self):
        event = RecipeGeneratedEvent(
            recipe_id="r-1",
            user_id="u-1",
            ingredient_names=["хлеб", "яйца"]
        )
        assert event.recipe_id == "r-1"
        assert event.user_id == "u-1"
        assert len(event.ingredient_names) == 2
    
    def test_cooking_started_event_creation(self):
        event = CookingStartedEvent(
            recipe_id="r-1",
            user_id="u-1",
            estimated_minutes=30
        )
        assert event.estimated_minutes == 30
        assert isinstance(event.started_at, datetime)
    
    def test_step_completed_event_creation(self):
        event = StepCompletedEvent(
            recipe_id="r-1",
            step_number=1,
            step_description="Порезать лук",
            completed_at=datetime.now()
        )
        assert event.step_number == 1
    
    def test_ingredient_missing_event_creation(self):
        event = IngredientMissingEvent(
            recipe_id="r-1",
            missing_ingredient="соль",
            available_ingredients=["хлеб", "яйца"]
        )
        assert event.missing_ingredient == "соль"
        assert len(event.available_ingredients) == 2
