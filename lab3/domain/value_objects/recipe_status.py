from enum import Enum


class RecipeStatus(Enum):
    """Value Object: Статус рецепта"""
    DRAFT = "черновик"
    GENERATED = "сгенерирован"
    COOKING = "готовится"
    COMPLETED = "завершён"
    FAILED = "провален"
    ARCHIVED = "архивирован"

    def can_transition_to(self, new_status: 'RecipeStatus') -> bool:
        """Правила переходов между статусами"""
        transitions = {
            RecipeStatus.DRAFT: [RecipeStatus.GENERATED],
            RecipeStatus.GENERATED: [RecipeStatus.COOKING, RecipeStatus.ARCHIVED],
            RecipeStatus.COOKING: [RecipeStatus.COMPLETED, RecipeStatus.FAILED],
            RecipeStatus.COMPLETED: [RecipeStatus.ARCHIVED],
            RecipeStatus.FAILED: [RecipeStatus.ARCHIVED],
            RecipeStatus.ARCHIVED: []
        }
        return new_status in transitions.get(self, [])
