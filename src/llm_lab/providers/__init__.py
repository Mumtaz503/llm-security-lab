from .base import Message, Provider, ProviderError
from .mock import MockProvider
from .real import RealHTTPProvider

def get_provider(name: str) -> Provider:
    name = (name or "").lower().strip()
    if name == "mock": return MockProvider()
    if name == "real": return RealHTTPProvider()
    raise ProviderError(f"Unknown provider: {name}")