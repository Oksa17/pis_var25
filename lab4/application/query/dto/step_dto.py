from dataclasses import dataclass


@dataclass
class StepDTO:
    """DTO для шага приготовления"""
    order: int
    description: str
    duration_minutes: int
    is_completed: bool
