from abc import ABC, abstractmethod

class RecipeRepository(ABC):
    @abstractmethod
    def save(self, recipe):
        pass
