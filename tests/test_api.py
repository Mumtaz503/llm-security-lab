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


def test_missing_question():
    response = client.post(
        "/v1/query",
        json={"question": "", "timeout": 10},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("question" in err.get("loc", []) for err in detail)


def test_question_too_long():
    response = client.post(
        "/v1/query",
        json={"question": "a" * 4001, "timeout": 10},
        headers=AUTH_HEADERS,
    )
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
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 400
    assert "Unknown provider" in response.json()["detail"]


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


def test_query_without_header():
    response = client.post("/v1/query", json={"question": "hi"})
    assert response.status_code == 401


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
