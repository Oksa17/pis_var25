from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CookingStep:
    """Value Object: Шаг приготовления (иммутабельный)"""
    order: int
    description: str
    duration_minutes: Optional[int] = None

    def __post_init__(self):
        if self.order < 1:
            raise ValueError("Номер шага должен быть положительным числом")
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Описание шага не может быть пустым")
        if self.duration_minutes is not None and self.duration_minutes <= 0:
            raise ValueError("Длительность шага должна быть положительной")

    def get_display_text(self) -> str:
        if self.duration_minutes:
            return f"{self.order}. {self.description} (⏱️ {self.duration_minutes} мин)"
        return f"{self.order}. {self.description}"
