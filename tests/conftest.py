import pytest
from auth_helpers import ALICE_TOKEN, BOB_TOKEN


@pytest.fixture(autouse=True)
def auth_tokens(monkeypatch):
    monkeypatch.setenv("TOKEN_ALICE", ALICE_TOKEN)
    monkeypatch.setenv("TOKEN_BOB", BOB_TOKEN)
