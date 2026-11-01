from fastapi.testclient import TestClient
from llm_lab.api.app import app
from auth_helpers import ALICE_TOKEN, AUTH_HEADERS, BOB_TOKEN

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query():
    response = client.post(
        "/v1/query",
        json={"question": "What is the capital of France?", "timeout": 10},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    assert "deterministic" in response.json()["content"].lower()

# Test for missing question returns 422 (expected)
def test_missing_question():
    response = client.post(
        "/v1/query",
        json={"question": "", "timeout": 10},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("question" in err.get("loc", []) for err in detail)

# Test for oversize question returns 422 (expected)
def test_question_too_long():
    response = client.post(
        "/v1/query",
        json={"question": "a" * 4001, "timeout": 10},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("question" in err.get("loc", []) for err in detail)

# Test for unknown provider returns 400 (expected)
def test_unknown_provider():
    response = client.post(
        "/v1/query",
        json={
            "question": "What is the capital of France?",
            "timeout": 10,
            "provider": "unknown",
        },
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 400
    assert "Unknown provider" in response.json()["detail"]

# Test for invalid timeout returns 422 (expected)
def test_invalid_timeout():
    response = client.post(
        "/v1/query",
        json={"question": "What is the capital of France?", "timeout": -1},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("timeout" in err.get("loc", []) for err in detail)


def test_omit_timeout_defaults_ok():
    response = client.post(
        "/v1/query", json={"question": "hi"}, headers=AUTH_HEADERS
    )
    assert response.status_code == 200

# Test for missing auth header returns 401 (expected)
def test_query_without_header():
    response = client.post("/v1/query", json={"question": "hi"})
    assert response.status_code == 401
# Test for invalid auth header returns 401 (expected)
def test_query_with_invalid_auth():
    response = client.post(
        "/v1/query", json={"question": "hi"}, headers={"X-API-Token": "invalid"}
    )
    assert response.status_code == 401

# Test for valid query + auth returns 200 (expected)
def test_query_with_bob_token():
    response = client.post(
        "/v1/query", json={"question": "hi"}, headers={"X-API-Token": BOB_TOKEN}
    )
    assert response.status_code == 200


def test_query_with_alice_token():
    response = client.post(
        "/v1/query", json={"question": "hi"}, headers={"X-API-Token": ALICE_TOKEN}
    )
    assert response.status_code == 200


def test_query_with_garbage_token():
    response = client.post(
        "/v1/query", json={"question": "hi"}, headers={"X-API-Token": "garbage"}
    )
    assert response.status_code == 401

# Test for unexpected body shape returns 422 (expected)
def test_unexpected_body_shape():
    r = client.post(
        "/v1/query",
        json={"question": 123, "timeout": "nope"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 422


# Provider returned a non-Completion → API maps to 500
def test_provider_unexpected_response_shape(monkeypatch):
    from llm_lab.providers.mock import MockProvider

    def bad_shape(self, messages, *, timeout=None):
        return {"content": "not a Completion", "provider": "mock"}

    monkeypatch.setattr(MockProvider, "complete", bad_shape)
    r = client.post(
        "/v1/query",
        json={"question": "hi"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"
