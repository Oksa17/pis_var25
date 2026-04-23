from typing import List
from src.domain.models.recipe import Recipe
from src.application.port.in.generate_recipe_use_case import GenerateRecipeUseCase


class RecipeService(GenerateRecipeUseCase):
    def __init__(self, repository, ai_service):
        self._repository = repository
        self._ai_service = ai_service

    def generate(self, user_id: str, ingredient_names: List[str]) -> Recipe:
        # TODO: реализовать
        raise NotImplementedError("TODO")
