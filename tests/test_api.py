from fastapi.testclient import TestClient
from llm_lab.api.app import app

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
