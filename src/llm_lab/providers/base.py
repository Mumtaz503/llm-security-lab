from typing import Protocol, TypedDict, List, Optional
from ..models import Completion


# Provider interface
class Message(TypedDict):
    role: str
    content: str


class Provider(Protocol):
    name: str

    # caller must call with timeout=5.0 etc to prevent accidental args mixup
    def complete(
        self, messages: List[Message], *, timeout: Optional[float] = None
    ) -> "Completion":
        # """Return a string response to the given messages. Raise ProviderError if the provider fails to complete the request."""
        ...


class ProviderError(Exception):
    """Exception raised when a provider fails to complete the request."""
