from src.domain.models.recipe import Recipe


class FakeAIService:
    def generate_recipe(self, ingredients):
        return Recipe(name="Гренки", steps=["Порежь хлеб", "Обжарь"])
