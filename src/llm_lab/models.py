from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Completion:
    content: str
    provider: str
    model: Optional[str] = None
