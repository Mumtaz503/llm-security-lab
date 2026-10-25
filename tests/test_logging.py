import logging
from llm_lab.cli import main

def test_logging_does_not_leak_api_keys(monkeypatch, caplog):
    monkeypatch.setenv("LLM_API_KEY", "test")
    monkeypatch.setenv("LLM_BASE_URL", "http://example.null")
    monkeypatch.setenv("LLM_MODEL", "test")
    caplog.set_level(logging.DEBUG)

    call = main(["--provider", "real", "Hello, world!"])
    assert call == 1

    #record of emitted events
    for record in caplog.records:
        assert "test" not in record.message
        assert "http://example.null" not in record.message
