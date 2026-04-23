from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class CookingTime:
    """Value Object: Время приготовления (иммутабельный)"""
    start_time: datetime
    estimated_duration_minutes: int

    def __post_init__(self):
        if self.estimated_duration_minutes <= 0:
            raise ValueError("Длительность приготовления должна быть положительной")

    def get_end_time(self) -> datetime:
        return self.start_time + timedelta(minutes=self.estimated_duration_minutes)

    def is_overtime(self) -> bool:
        return datetime.now() > self.get_end_time()
