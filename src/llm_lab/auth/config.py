from __future__ import annotations

import os
from typing import Dict

from pydantic import BaseModel


class User(BaseModel):
    id: str
    display_name: str


USERS = {
    "alice": User(id="alice12284", display_name="Alice"),
    "bob": User(id="bob123", display_name="Bob"),
}


def token_to_username() -> Dict[str, str]:
    """Build token -> username from current env (call per request)."""
    mapping: Dict[str, str] = {}
    for username in USERS:
        token = os.getenv(f"TOKEN_{username.upper()}")
        if token:
            mapping[token] = username
    return mapping

