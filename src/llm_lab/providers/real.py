import os
from typing import List, Optional
from .base import Message, Provider, ProviderError

class RealHTTPProvider:
    """kEY is real here never logged"""

    name = "real"
    
    def complete(self, messages: List[Message], *, timeout: float):
        api_key = os.environ.get("LLM_API_KEY")
        base_url = os.environ.get("LLM_BASE_URL")
        model = os.environ.get("LLM_MODEL")

        if not (api_key and base_url and model):
            # Must never fail silently. If the env vars are not set, we should raise an error.
            raise ProviderError("Real HTTP provider Keys Not configured yet. Set LLM_API_KEY, LLM_BASE_URL, and LLM_MODEL in environment variables.")
        
        raise ProviderError("Real HTTP provider not implemented yet")