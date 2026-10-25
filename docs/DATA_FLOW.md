# Data Flow and Trust Boundaries

Request path from CLI to stdout. `[untrusted]` = do not trust for
authorization. `[secret]` = env-only, header-only. `[third party]` = provider
sees the full payload.

## Mermaid

```mermaid
flowchart LR
    U["User / CLI args<br/>[untrusted]"] --> M["messages[]"]
    M --> P["Provider.complete(messages, timeout)"]
    P -->|"env: LLM_API_KEY<br/>[secret]"| H["HTTPS request<br/>auth header"]
    H -->|"DNS + TLS"| S["Provider service<br/>[third party]"]
    S -->|"JSON body<br/>[untrusted]"| R["Response parse"]
    R --> C["Completion<br/>[untrusted]"]
    C --> O["stdout"]
    C --> L["logs<br/>metadata only"]
```

## ASCII

```
user text [untrusted]
        │
        ▼
  messages[] ──► Provider.complete(messages, *, timeout)
                        │
        env LLM_API_KEY [secret] ──► auth header only
                        │
                        ▼
              HTTPS  ──►  Provider service [third party]
                        │
                        ▼
              JSON body [untrusted]
                        │
                        ▼
              Completion [untrusted]
                   │           │
                   ▼           ▼
                stdout       logs (metadata only)
```