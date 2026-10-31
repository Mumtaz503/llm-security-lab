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

---
## HTTP API (dev auth)

The FastAPI app (`uvicorn llm_lab.api.app:app --reload`) protects
`POST /v1/query` with a **header-based** identity check.
`GET /health` stays open.

### Test users (insecure development only)

Two named lab users exist in code (`llm_lab.auth.config`):

| Name  | Role in lab                          |
|-------|--------------------------------------|
| alice | Example caller A                     |
| bob   | Example caller B                     |

Example tokens live only in `.env.example` (`TOKEN_ALICE`, `TOKEN_BOB`).
Copy them into a local `.env` — **never commit real secrets**.

> **Insecure development shortcut:** tokens in a request header are *not*
> real authentication (no sessions, OIDC, signatures, or expiry). This is a
> learning stub so we can practice trust boundaries. Do not use it outside
> this lab.

Identity is taken from the `X-API-Token` header via FastAPI
`Depends(get_current_user)`, **never** from the JSON body.

```bash
# valid (alice) → 200 with mock
curl -sS -X POST http://127.0.0.1:8000/v1/query \
  -H "Content-Type: application/json" \
  # only if env is loaded. else run this and start the server
  # export TOKEN_ALICE=dev-alice-token-123
  # export TOKEN_BOB=dev-bob-token-456
  # uvicorn llm_lab.api.app:app --reload
  -H "X-API-Token: $TOKEN_ALICE" \ 
  -d '{"question":"hi"}'

# missing header → 401
curl -sS -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question":"hi"}'
```

---
### Authn vs authz (lab note)

**Authentication (authn)** answers “who is calling?” — here, mapping
`X-API-Token` to alice or bob. **Authorization (authz)** answers “what may
they do?” (which docs, tools, or tenants). This exercise only does a thin
authn stub; it does not enforce per-user authz yet. A JSON field like
`user_id` is not proof of identity: the client can set any value, so the
server must establish identity from a verified channel (header/session/token
checked against a server-side allowlist), then apply authz separately.