from abc import ABC, abstractmethod

class GetRecipeHistoryUseCase(ABC):
    @abstractmethod
    def get_history(self, user_id: str):
        pass
