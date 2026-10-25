import pytest
from llm_lab.cli import main

#capsys is a pytest fixture that captures stdout/stderr.
def test_cli_empty_question(capsys):
    args = ([])
    assert main(args) == 2
    err = capsys.readouterr().err
    assert "Error: A question is required" in err

def test_unknown_provider(capsys):
    args = (["--provider", "blah", "Hello, world!"])
    assert main(args) == 2
    err = capsys.readouterr().err
    assert "Error: Unknown provider: blah" in err

def test_mock_provider_logs(capsys):
    args = (["--provider", "mock", "Hello, world!"])
    assert main(args) == 0
    out = capsys.readouterr().out
    assert out.startswith("Mock response for")
