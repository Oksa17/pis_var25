from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GetUserHistoryQuery:
    """Запрос: получить историю рецептов пользователя"""
    user_id: str
    status_filter: Optional[str] = None  # "completed", "failed", None
    limit: int = 20
    offset: int = 0
