# llm-security-lab

A small, offline-first CLI for exercising the **request path to an LLM API**:
CLI → messages → Provider → Completion → stdout/logs. The mock provider is
deterministic and needs no API key; the real provider is a stub that fails
loudly until HTTP support lands.

This repo is a **security lab**. Treat the model as a third party and its
output as untrusted. See [`docs/NEVER_LOG.md`](docs/NEVER_LOG.md) and
[`docs/DATA_FLOW.md`](docs/DATA_FLOW.md).

---

## Requirements

- **Python 3.9+** (tested on 3.9–3.12)
- No runtime dependencies. `pytest` is dev-only.

Check your interpreter:

```bash
python3 --version

```

---
## Setup (from an empty clone)
```bash

git clone <repo-url> llm-security-lab
cd llm-security-lab

# Optional but recommended: isolated environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Dev dependency only (needed for pytest; not for running the CLI)
pip install pytest

# Optional: install the package so `llm-lab` and tests find it without PYTHONPATH
pip install -e .
```

---
## Configuration
```bash
cp .env.example .env
# edit .env with placeholders only — never commit real values
```

---
## Running the CLI (mock)
```bash
# without installing packages
PYTHONPATH=src python3 -m llm_lab --provider mock "ping"

# Bad args fail with err code 2

PYTHONPATH=src python3 -m llm_lab
# usage: llm-lab [-h] [--provider PROVIDER] [--timeout TIMEOUT] [question]
# error: question is required
# exit code 2

PYTHONPATH=src python3 -m llm_lab --provider nope "ping"
# error: unknown provider: 'nope' (expected 'mock' or 'real')
# exit code 2

# Real provider stub fails loudly (Not yet implemented)

LLM_API_KEY=x LLM_BASE_URL=http://example.invalid LLM_MODEL=m \
  PYTHONPATH=src python3 -m llm_lab --provider real "ping"
# error: Real HTTP provider not implemented yet
# exit code 1
```

---
## Tests

Tests are offline: they use unittest.mock/monkeypatch, never network.
Expected: all pass.
```bash
# If you installed the package (pip install -e .):
pytest -q

# Otherwise:
PYTHONPATH=src pytest -q
```

