from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel

@dataclass(frozen=True)
class Completion:
    content: str
    provider: str
    model: Optional[str] = None

class QueryRequest(BaseModel):
    question: str
    model: Optional[str] = None
    provider: Optional[str] = None
    timeout: Optional[int] = None