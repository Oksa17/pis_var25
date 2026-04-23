from dataclasses import dataclass


@dataclass(frozen=True)
class CompleteStepCommand:
    """Команда: завершить шаг приготовления"""
    session_id: str
    step_number: int
