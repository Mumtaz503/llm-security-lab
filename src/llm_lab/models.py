from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field

@dataclass(frozen=True)
class Completion:
    content: str
    provider: str
    model: Optional[str] = None

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    model: Optional[str] = None
    provider: Optional[str] = None
    timeout: Optional[int] = Field(default=None, gt=0, le=300)

class QueryResponse(BaseModel):
    content: str
    provider: str
    model: Optional[str] = None