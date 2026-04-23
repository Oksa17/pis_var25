from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Ingredient:
    """Value Object: Ингредиент (иммутабельный)"""
    name: str
    expiry_date: Optional[date] = None

    def __post_init__(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Название ингредиента не может быть пустым")
        if len(self.name) > 50:
            raise ValueError("Название ингредиента не может превышать 50 символов")

    def is_expired(self) -> bool:
        if self.expiry_date is None:
            return False
        return self.expiry_date < date.today()

    def is_available(self) -> bool:
        return not self.is_expired()
