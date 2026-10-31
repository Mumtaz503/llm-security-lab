import pytest
import llm_lab.auth.deps as auth_deps
from auth_helpers import ALICE_TOKEN, BOB_TOKEN


@pytest.fixture(autouse=True)
def auth_tokens(monkeypatch):
    monkeypatch.setattr(
        auth_deps,
        "_TOKEN_TO_USER",
        {BOB_TOKEN: "bob", ALICE_TOKEN: "alice"},
    )
