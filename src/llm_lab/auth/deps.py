from __future__ import annotations
from llm_lab.auth.config import User, TOKEN_MAP, USERS
from fastapi import Header, HTTPException


_TOKEN_TO_USER = {token: user for user, token in TOKEN_MAP.items() if token}


def get_current_user(
    token: str | None = Header(default=None, alias="X-API-Token"),
) -> User:
    if not token or not token.strip():
        raise HTTPException(status_code=401, detail="Missing Credentials")

    username = _TOKEN_TO_USER.get(token.strip())
    if username is None or username not in USERS:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return USERS[username]
