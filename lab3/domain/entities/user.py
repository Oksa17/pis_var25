from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class User:
    """Entity: Пользователь (имеет ID)"""
    id: str
    email: str
    name: str
    role: str = "user"
    created_at: datetime = field(default_factory=datetime.now)
    _request_timestamps: List[datetime] = field(default_factory=list, repr=False)

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def can_generate_recipe(self, limit: int = 10, window_minutes: int = 60) -> bool:
        """Проверка лимита запросов (инвариант)"""
        now = datetime.now()
        cutoff = now - timedelta(minutes=window_minutes)
        self._request_timestamps = [ts for ts in self._request_timestamps if ts > cutoff]
        return len(self._request_timestamps) < limit

    def add_generation_request(self) -> None:
        """Фиксация запроса"""
        self._request_timestamps.append(datetime.now())

    def get_requests_count_last_hour(self) -> int:
        now = datetime.now()
        cutoff = now - timedelta(minutes=60)
        return len([ts for ts in self._request_timestamps if ts > cutoff])
