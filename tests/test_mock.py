from llm_lab.providers.mock import MockProvider

#mock deterministic response
def test_mock_provider():
    provider = MockProvider()

    msgs = [{'role': 'user', 'content': 'Hello, world!'}]
    ans1 = provider.complete(msgs, timeout=5.0)
    ans2 = provider.complete(msgs, timeout=5.0)
    assert ans1.content == ans2.content
    assert ans1 == ans2
