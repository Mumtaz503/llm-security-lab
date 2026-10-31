import os
from pydantic import BaseModel


class User(BaseModel):
    id: str
    display_name: str

USERS = {
    "alice": User(id="alice12284", display_name="Alice"),
    "bob": User(id="bob123", display_name="Bob"),
}

TOKEN_MAP = {
    username: os.getenv(f"TOKEN_{username.upper()}") for username in USERS
}
