from __future__ import annotations

from fastapi import Header, HTTPException

from llm_lab.auth.config import USERS, User, token_to_username


def get_current_user(
    token: str | None = Header(default=None, alias="X-API-Token"),
) -> User:
    if not token or not token.strip():
        raise HTTPException(status_code=401, detail="Missing Credentials")

    username = token_to_username().get(token.strip())
    if username is None or username not in USERS:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return USERS[username]
