from abc import ABC, abstractmethod

class AIServicePort(ABC):
    @abstractmethod
    def generate_recipe(self, ingredients):
        pass
