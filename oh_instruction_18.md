---
applyTo: "backstage/server/agent-api*/*.py,backstage/server/agent-api*/**/*.py,docs/aeg-feature-scaffold/orchestrator/**/*.py"
description: "Use when editing Python agent runtimes, FastAPI boundaries, orchestration, tools, or their tests."
---

# Python Agent Runtimes

These rules intentionally exclude general repository utilities and skill scripts.

## Conventions

- Use Python 3.11+ syntax, complete type hints, and explicit Pydantic models at API, event, checkpoint, and tool boundaries.
- Keep FastAPI routes thin; place routing, policy, tools, memory, and provider adapters behind testable interfaces.
- Preserve asynchronous execution end to end and move unavoidable blocking work off the event loop.
- Read configuration from validated settings and use managed or workload identity; never hardcode credentials, tenant endpoints, or tokens.
- Use stable structured event names and correlation IDs. Redact prompts, tool arguments, credentials, personal data, and provider payloads.
- Catch expected exceptions narrowly and return safe external errors; broad boundary catches must log redacted context and preserve causes.
- Treat JSON, MCP responses, model output, checkpoint state, and remote API data as untrusted until validated.
- Keep unit tests deterministic and independent of live Azure, GitHub, Kubernetes, or Backstage services.
- Preserve pre/post tool governance and authorization around every execution path.

## Verification

- The owning runtime's pytest suite covers success, denial, malformed input, timeout, and dependency failure.
- Async routes contain no unbounded synchronous network, subprocess, or file work.
- Type and lint checks use the owning manifest and Python version.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use typed boundaries, bounded async work, and the owning dependency manifest. | Block the event loop, invent dependency versions, or bypass tool governance. |
| Test success, denial, malformed input, timeout, and dependency failure. | Report a static check as runtime behavior. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Type, lint, and focused pytest checks use the owning Python version.
- [ ] Async paths contain no unbounded synchronous work.
- [ ] Authorization and pre/post tool governance remain intact.
- [ ] No secret, raw provider payload, or unrelated edit was introduced.
