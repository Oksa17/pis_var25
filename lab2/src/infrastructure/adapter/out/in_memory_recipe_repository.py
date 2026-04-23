from typing import Dict
from src.domain.models.recipe import Recipe


class InMemoryRecipeRepository:
    def __init__(self):
        self._storage: Dict[str, Recipe] = {}

    def save(self, recipe: Recipe) -> Recipe:
        self._storage[recipe.id] = recipe
        return recipe
