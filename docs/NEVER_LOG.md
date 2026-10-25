# Logging in the Context of LLM Security Practices

A plain `print("Calling Provider...")` is unparseable. Logging with a defined
logger name (see `src/llm_lab/logging_setup.py`), a level, and `key=value`
fields (via `extra={...}` or `%s` interpolation) lets us filter and redact
later — and is the difference between an incident you can reconstruct and one
you can't.

> **Rule of thumb:** log *events and metadata*, never *content or secrets*.
> If you'd be uncomfortable pasting it into a public issue tracker, don't log
> it.

## What must never be logged, and why

Secrets live in `.env` / environment variables and must never reach a log line.

| Never log | Why | Do this instead |
|---|---|---|
| `LLM_API_KEY` | It's a private credential tied to your account and billing. | Log presence only: `api_key_set=true`. |
| Full auth headers | Exposes credentials and bearer tokens in plaintext across log storage and monitoring. | Log `auth=redacted`. |
| Full request bodies | Exposes user's personal content to logs and monitoring systems. | Log `chars=<len>`, never the text. |
| Full response bodies | The model's output may contain sensitive user content, or an injected instruction that changes app behaviour if surfaced elsewhere. | Log `chars=<len>` and `provider`/`model`. |
| Tracebacks with env dumps | Hands an attacker a blueprint of the app's infrastructure: env variables, internal file paths. | Log `error_type=<cls>` and a truncated message. |

## What is safe to log

- Provider name (`provider=mock`)
- Model name (`model=mock-1`)
- Request/response **character counts** (`req_chars=42`, `res_chars=180`)
- Elapsed time (`elapsed_ms=112`)
- Error **type and message** (`error_type=ProviderError`, `error=...`)
- Event names (`start`, `success`, `failure`)

These are generally safe **unless** they contain content from the table above.
Metadata about a request is safe; the request itself is not.