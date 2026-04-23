from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from ..entities.recipe import Recipe
from ..entities.user import User
from ..value_objects.cooking_step import CookingStep
from ..value_objects.cooking_time import CookingTime
from ..events.recipe_generated_event import RecipeGeneratedEvent
from ..events.cooking_started_event import CookingStartedEvent
from ..events.step_completed_event import StepCompletedEvent
from ..events.ingredient_missing_event import IngredientMissingEvent


@dataclass
class CookingSession:
    """Aggregate Root: Сессия приготовления"""
    id: str = field(default_factory=lambda: str(uuid4()))
    user: Optional[User] = None
    recipe: Optional[Recipe] = None
    cooking_time: Optional[CookingTime] = None
    completed_steps: List[int] = field(default_factory=list)
    _events: List = field(default_factory=list, repr=False)

    def __post_init__(self):
        self._events = []

    def _add_event(self, event) -> None:
        """Добавить доменное событие"""
        self._events.append(event)

    def get_events(self) -> List:
        """Получить и очистить события"""
        events = self._events.copy()
        self._events.clear()
        return events

    # ========== ИНВАРИАНТЫ И МЕТОДЫ ==========

    def generate_recipe(self, user: User, ingredients: List) -> Recipe:
        """
        Инвариант 1: Нельзя генерировать рецепт, если превышен лимит запросов
        Инвариант 2: Нельзя генерировать рецепт без ингредиентов
        Инвариант 3: Нельзя генерировать рецепт, если все ингредиенты просрочены
        """
        if not user.can_generate_recipe():
            raise ValueError(f"Превышен лимит запросов. Можно не более 10 в час")
        
        if not ingredients:
            raise ValueError("Нельзя генерировать рецепт без ингредиентов")
        
        fresh_ingredients = [i for i in ingredients if i.is_available()]
        if not fresh_ingredients:
            raise ValueError("Все ингредиенты просрочены!")
        
        # Симуляция генерации рецепта
        recipe = Recipe(
            user_id=user.id,
            name=f"Блюдо из {fresh_ingredients[0].name}",
            ingredients=fresh_ingredients,
            steps=[]
        )
        
        user.add_generation_request()
        self.user = user
        self.recipe = recipe
        
        # Доменное событие
        self._add_event(RecipeGeneratedEvent(
            recipe_id=recipe.id,
            user_id=user.id,
            ingredient_names=[i.name for i in fresh_ingredients]
        ))
        
        return recipe

    def start_cooking(self, recipe: Recipe, estimated_minutes: int) -> None:
        """
        Инвариант: Нельзя начать готовку, если рецепт не сгенерирован
        """
        if recipe.status.value != "сгенерирован":
            raise ValueError(f"Нельзя начать готовку рецепта в статусе {recipe.status.value}")
        
        self.recipe = recipe
        self.cooking_time = CookingTime(
            start_time=datetime.now(),
            estimated_duration_minutes=estimated_minutes
        )
        recipe.start_cooking()
        
        # Доменное событие
        self._add_event(CookingStartedEvent(
            recipe_id=recipe.id,
            user_id=recipe.user_id,
            estimated_minutes=estimated_minutes
        ))

    def complete_step(self, step_number: int) -> None:
        """
        Инвариант: Нельзя завершить шаг, который не существует
        Инвариант: Нельзя завершить шаг вне порядка
        """
        if not self.recipe:
            raise ValueError("Нет активной сессии готовки")
        
        if step_number in self.completed_steps:
            raise ValueError(f"Шаг {step_number} уже завершён")
        
        if step_number != len(self.completed_steps) + 1:
            raise ValueError(f"Шаги должны выполняться по порядку. Следующий шаг: {len(self.completed_steps) + 1}")
        
        if step_number > len(self.recipe.steps):
            raise ValueError(f"Шаг {step_number} не существует. Всего шагов: {len(self.recipe.steps)}")
        
        self.completed_steps.append(step_number)
        
        # Доменное событие
        self._add_event(StepCompletedEvent(
            recipe_id=self.recipe.id,
            step_number=step_number,
            step_description=self.recipe.steps[step_number - 1].description if self.recipe.steps else "",
            completed_at=datetime.now()
        ))
        
        # Проверка завершения всех шагов
        if len(self.completed_steps) == len(self.recipe.steps):
            self.recipe.complete_cooking()

    def handle_missing_ingredient(self, ingredient_name: str) -> None:
        """
        Инвариант: Нельзя обработать отсутствие ингредиента, если нет активного рецепта
        """
        if not self.recipe:
            raise ValueError("Нет активной сессии готовки")
        
        # Доменное событие
        self._add_event(IngredientMissingEvent(
            recipe_id=self.recipe.id,
            missing_ingredient=ingredient_name,
            available_ingredients=[i.name for i in self.recipe.ingredients]
        ))
