from abc import ABC, abstractmethod
from typing import List
from src.domain.models.recipe import Recipe


class GenerateRecipeUseCase(ABC):
    @abstractmethod
    def generate(self, user_id: str, ingredient_names: List[str]) -> Recipe:
        pass
