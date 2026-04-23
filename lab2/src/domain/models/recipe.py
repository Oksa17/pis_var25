from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Recipe:
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    name: str = ""
    steps: list[str] = field(default_factory=list)
