import pytest
from llm_lab.providers.real import RealHTTPProvider
from llm_lab.providers.base import ProviderError
from llm_lab.api.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

#monkeypatch is a pytest fixture that allows you to modify the environment variables.
#no env vars exposed during test
def test_real_err_unconfigured(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("LLM_BASE_URL", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    with pytest.raises(ProviderError) as e:
        RealHTTPProvider().complete(
            [{"role": "user", "content": "Hello, world!"}], timeout=5.0
        )
    assert "yet" in str(e.value)

def test_real_err_when_configured_unimplemented(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "test")
    monkeypatch.setenv("LLM_BASE_URL", "http://example.null")
    monkeypatch.setenv("LLM_MODEL", "test")
    with pytest.raises(ProviderError) as e:
        RealHTTPProvider().complete(
            [{"role": "user", "content": "Hello, world!"}], timeout=5.0
        )
    assert "not implemented" in str(e.value)

def test_real_provider_failure(monkeypatch):
    from auth_helpers import AUTH_HEADERS

    monkeypatch.setenv("LLM_API_KEY", "ABC-XYZ-123")
    monkeypatch.setenv("LLM_BASE_URL", "http://example.null")
    monkeypatch.setenv("LLM_MODEL", "test")
    response = client.post(
        "/v1/query",
        json={
            "question": "What is the capital of France?",
            "timeout": 10,
            "provider": "real",
        },
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 502
    assert "not implemented" in response.json()["detail"]
