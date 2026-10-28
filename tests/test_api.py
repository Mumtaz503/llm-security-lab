from fastapi.testclient import TestClient
from llm_lab.api.app import app
from llm_lab.providers.base import ProviderError
from llm_lab.providers.mock import MockProvider

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query():
    response = client.post(
        "/v1/query", json={"question": "What is the capital of France?", "timeout": 10}
    )
    assert response.status_code == 200
    assert "deterministic" in response.json()["content"].lower()


def test_missing_question():
    response = client.post("/v1/query", json={"question": "", "timeout": 10})
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("question" in err.get("loc", []) for err in detail)


def test_question_too_long():
    response = client.post("/v1/query", json={"question": "a" * 4001, "timeout": 10})
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("question" in err.get("loc", []) for err in detail)


def test_unknown_provider():
    response = client.post(
        "/v1/query",
        json={
            "question": "What is the capital of France?",
            "timeout": 10,
            "provider": "unknown",
        },
    )
    assert response.status_code == 400
    assert "Unknown provider" in response.json()["detail"]


def test_invalid_timeout():
    response = client.post(
        "/v1/query", json={"question": "What is the capital of France?", "timeout": -1}
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("timeout" in err.get("loc", []) for err in detail)

def test_omit_timeout_defaults_ok():
    response = client.post("/v1/query", json={"question": "hi"})
    assert response.status_code == 200