import hashlib
from typing import List, Optional
from .base import Message, Provider, ProviderError
from ..models import Completion


class MockProvider:
    name = "mock"

    # accepting timeout for interface parity. Mock is instantaneous and ignores it
    def complete(self, messages: List[Message], *, timeout: Optional[float] = None) -> Completion:
        user_message = next(
            (
                message["content"]
                for message in reversed(messages)
                if message["role"] == "user"
            ),
            "",
        )
        if not user_message:
            raise ProviderError("No user message found")
        digest = hashlib.sha256(user_message.encode()).hexdigest()
        return Completion(
            content=f"Mock response for {digest}. You asked: {user_message!r}. (Deterministic reply)",
            provider=self.name,
            model="mock-1.0",
        )
