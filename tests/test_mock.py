from llm_lab.providers.mock import MockProvider
from llm_lab.api.app import app
from fastapi.testclient import TestClient
from llm_lab.providers.base import ProviderError

client = TestClient(app)

#mock deterministic response
def test_mock_provider():
    provider = MockProvider()

    msgs = [{'role': 'user', 'content': 'Hello, world!'}]
    ans1 = provider.complete(msgs, timeout=5.0)
    ans2 = provider.complete(msgs, timeout=5.0)
    assert ans1.content == ans2.content
    assert ans1 == ans2

def test_mock_provider_failure(monkeypatch):
    def boom(self, messages, *, timeout=None):
        raise ProviderError("Mock Failed")
    monkeypatch.setattr(MockProvider, "complete", boom)
    response = client.post(
        "/v1/query", json={"question": "What is the capital of France?", "timeout": 10, "provider": "mock"}
    )
    assert response.status_code == 502
    assert "Mock Failed" in response.json()["detail"]