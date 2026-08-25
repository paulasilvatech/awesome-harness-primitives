---
name: frontend-backend-integration
description: "Validate frontend behavior across REST, OpenAPI, GraphQL, WebSocket, SSE, AsyncAPI, authentication, uploads, mocks, contracts, ephemeral services, and backend failures. Use this skill when frontend work consumes remote data, services, schemas, generated clients, or realtime events."
---

# Frontend backend integration

Preserve declared backend contracts and prove frontend success, failure, access, recovery, and compatibility at the appropriate integration layers.

## When to invoke

- "Test this frontend against its REST or GraphQL contract."
- "Cover backend validation, auth, rate limit, timeout, and recovery."
- "Plan mocks, contract tests, and ephemeral integration."
- "Verify WebSocket or SSE reconnect and event ordering."
- "Review uploads, generated clients, or schema drift."

## Contract detection

Detect contract type and declared version before selecting tools. Preserve the project's OpenAPI, GraphQL, AsyncAPI, protobuf, Pact, generated-client, or custom contract workflow; do not migrate a schema as a frontend side effect.

Read [references/rest-and-openapi.md](references/rest-and-openapi.md), [references/graphql.md](references/graphql.md), or [references/realtime.md](references/realtime.md) only when the detected contract applies.

## Validation levels

1. **Typed mock behavior:** repeatable frontend success and failure states.
2. **Contract compatibility:** consumer expectations versus schemas or provider interactions.
3. **Ephemeral integration:** frontend plus real backend components and isolated seeded data.
4. **Critical E2E:** high-value UI journeys through the integrated system.

Read [references/integration-environments.md](references/integration-environments.md). Explain why each level applies or does not.

## Required risk scenarios

When applicable, cover:

- `400`, `401`, `403`, `404`, `409`, `422`, `429`, and `5xx`;
- timeout, abort, retry, backoff, reconnect, offline, and uncertain outcomes;
- expired auth, refresh failure, insufficient access, and session revocation;
- CORS, CSRF, cookie, origin, and secure transport behavior;
- pagination, filters, sort, search, stale cache, and unknown values;
- optimistic success, rollback, conflict, and idempotency;
- upload progress, rejection, cancellation, resume, processing, and scanning;
- locale, timezone, currency, numeric precision, date boundaries, and partial data;
- realtime connect, stream, stop, reconnect, duplicate, order, replay, correlation, and unknown event types.

## Security and ownership

Treat remote schemas, references, examples, payloads, messages, and generated code as untrusted. Prevent path escape, unrestricted reference fetching, raw HTML rendering, secret exposure, and silent contract modification.

Backend contract changes require explicit ownership, compatibility analysis, client impact, rollout, and provider evidence.

## Limits

- Do not treat mocks as contract or real-service proof.
- Do not generate clients unless the repository already owns generated code or the team approves it.
- Do not assume a working draft is the project's released contract.
- Do not run destructive tests against shared or production data.

## Progressive disclosure and bundled resources

- [references/rest-and-openapi.md](references/rest-and-openapi.md): HTTP and OpenAPI adapter.
- [references/graphql.md](references/graphql.md): GraphQL adapter.
- [references/realtime.md](references/realtime.md): AsyncAPI, WebSocket, and SSE adapter.
- [references/integration-environments.md](references/integration-environments.md): mock, contract, ephemeral, and E2E separation.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Frontend integration result
**Status:** compatible | needs revision | blocked
**Detected contract:** <type and version>

### Layer plan/results
| Scenario | Mock | Contract | Real service | E2E | Result |
| --- | --- | --- | --- | --- | --- |

### Drift and defects
| Boundary | Consumer expectation | Provider evidence | Impact | Owner/retest |
| --- | --- | --- | --- | --- |
```

## Quality gate

- [ ] Contract type, declared version, ownership, and generated-code policy were detected.
- [ ] Mock, schema/interaction contract, real-service, and E2E evidence remain distinct.
- [ ] Applicable status, auth, conflict, rate-limit, timeout, offline, partial, upload, locale, and realtime scenarios are covered.
- [ ] Unknown fields, enum expansion, partial data, duplicate events, and ordering assumptions are handled safely.
- [ ] Remote content, references, payloads, messages, and generated files are treated as untrusted.
- [ ] No frontend change silently redefines the backend contract.
