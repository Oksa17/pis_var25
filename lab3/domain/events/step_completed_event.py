from dataclasses import dataclass
from datetime import datetime


@dataclass
class StepCompletedEvent:
    """Событие: Шаг приготовления завершён"""
    recipe_id: str
    step_number: int
    step_description: str
    completed_at: datetime
