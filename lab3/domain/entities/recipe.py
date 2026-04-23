from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from ..value_objects.ingredient import Ingredient
from ..value_objects.recipe_status import RecipeStatus
from ..value_objects.cooking_step import CookingStep


@dataclass
class Recipe:
    """Entity: Рецепт (имеет ID)"""
    user_id: str
    name: str
    ingredients: List[Ingredient]
    steps: List[CookingStep]
    id: str = field(default_factory=lambda: str(uuid4()))
    status: RecipeStatus = field(default=RecipeStatus.DRAFT)
    created_at: datetime = field(default_factory=datetime.now)
    rating: Optional[int] = None

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def generate(self) -> None:
        """Сгенерировать рецепт (инвариант: только из DRAFT)"""
        if self.status != RecipeStatus.DRAFT:
            raise ValueError(f"Нельзя сгенерировать рецепт в статусе {self.status.value}")
        if not self.ingredients:
            raise ValueError("Нельзя сгенерировать рецепт без ингредиентов")
        if not self.steps:
            raise ValueError("Нельзя сгенерировать рецепт без шагов приготовления")
        self.status = RecipeStatus.GENERATED

    def start_cooking(self) -> None:
        """Начать готовку (инвариант: только из GENERATED)"""
        if self.status != RecipeStatus.GENERATED:
            raise ValueError(f"Нельзя начать готовку рецепта в статусе {self.status.value}")
        self.status = RecipeStatus.COOKING

    def complete_cooking(self) -> None:
        """Завершить готовку (инвариант: только из COOKING)"""
        if self.status != RecipeStatus.COOKING:
            raise ValueError(f"Нельзя завершить готовку рецепта в статусе {self.status.value}")
        self.status = RecipeStatus.COMPLETED

    def fail_cooking(self, reason: str) -> None:
        """Провалить готовку (инвариант: только из COOKING)"""
        if self.status != RecipeStatus.COOKING:
            raise ValueError(f"Нельзя провалить готовку рецепта в статусе {self.status.value}")
        self.status = RecipeStatus.FAILED

    def archive(self) -> None:
        """Архивировать рецепт (инвариант: только из COMPLETED или FAILED)"""
        if self.status not in [RecipeStatus.COMPLETED, RecipeStatus.FAILED]:
            raise ValueError(f"Нельзя архивировать рецепт в статусе {self.status.value}")
        self.status = RecipeStatus.ARCHIVED

    def add_rating(self, rating: int) -> None:
        """Оценить рецепт (инвариант: только после завершения)"""
        if self.status != RecipeStatus.COMPLETED:
            raise ValueError(f"Нельзя оценить рецепт в статусе {self.status.value}")
        if not 1 <= rating <= 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        self.rating = rating
