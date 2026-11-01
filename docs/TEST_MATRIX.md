# API test matrix

Provider unit tests call `complete()` directly; `/v1/query` tests use FastAPI `TestClient` (integration).

| Layer | What it exercises | Examples |
|-------|-------------------|----------|
| Unit (provider) | `MockProvider` / `RealHTTPProvider.complete()` only | `tests/test_mock.py` happy path; `tests/test_real.py` unconfigured / not-implemented |
| Integration (API) | HTTP → auth dependency → validation → provider → status codes | `tests/test_api.py`; API failure paths in `test_mock` / `test_real` via `TestClient` |
| Integration (API) | Provider returns non-`Completion` (patched `complete`) → **500** safe detail | `test_provider_unexpected_response_shape` |

All tests stay offline (monkeypatch / stub; no live network).
