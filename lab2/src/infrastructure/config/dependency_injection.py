from src.infrastructure.adapter.out.in_memory_recipe_repository import InMemoryRecipeRepository
from src.infrastructure.adapter.out.fake_ai_service import FakeAIService


def setup_dependencies():
    repository = InMemoryRecipeRepository()
    ai_service = FakeAIService()
    return repository, ai_service
