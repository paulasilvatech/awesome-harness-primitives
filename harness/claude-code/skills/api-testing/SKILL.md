---
name: api-testing
description: >-
  Test REST, GraphQL, and gRPC APIs at the contract and behavior level with schema validation,
  authentication and authorization coverage, error-path assertions, pagination and idempotency
  checks, and CI-ready suites. Use when the user asks to test an API, validate responses against
  OpenAPI or a GraphQL schema, cover auth and error cases, or build an integration suite for
  endpoints.
license: MIT
---

<!-- Generated from harness/github-copilot/skills/api-testing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# API testing

Verify that an API honors its contract, enforces its authorization rules, and fails correctly, without depending on a browser or a full end-to-end environment.

## When to invoke

- "Write integration tests for these endpoints."
- "Validate responses against our OpenAPI spec."
- "Test authentication and authorization on this API."
- "Our API returns 200 with an error body; how do we test that?"
- "Add API tests to CI."

## Test the contract, then the behavior

| Layer | Question | Typical assertion |
| --- | --- | --- |
| Transport | Did the call succeed at HTTP level? | Status code, headers, content type |
| Schema | Does the payload match the declared shape? | Validate against OpenAPI or GraphQL schema |
| Semantics | Is the value correct for this input? | Field values, computed results |
| Authorization | Can the wrong caller reach it? | 401 without token, 403 with wrong role |
| Side effects | Did state change as promised? | Re-read, or verify emitted event |

Testing only the happy path with a 200 assertion is the most common and least useful API suite.

## Validate against the schema, not hand-written shapes

Hand-written expected payloads drift from the spec. Assert against the source of truth.

```javascript
// Validate the response against the OpenAPI schema itself
const valid = ajv.validate(schema.components.schemas.User, response.body);
expect(valid, JSON.stringify(ajv.errors)).toBe(true);
```

For GraphQL, run introspection or load the SDL and validate both the query and the response. A query that requests a removed field must fail the build, not silently return null.

## Authorization is a test matrix, not a single case

Every protected endpoint needs coverage for each meaningful caller:

- **No credentials** — expect 401.
- **Valid credentials, wrong role** — expect 403.
- **Valid credentials, correct role, another tenant's resource** — expect 403 or 404, and be deliberate about which.
- **Expired or malformed token** — expect 401, never 500.

The cross-tenant case is where real breaches occur and where suites are usually silent.

## Error paths deserve explicit assertions

- Assert the **status code and the error body shape**, including a stable machine-readable code.
- Confirm the error **does not leak** stack traces, SQL, internal hostnames, or credentials.
- Verify **validation errors identify the offending field**.
- Check that an unexpected server error returns 5xx rather than a 200 with an error payload.

## Pagination, ordering, and idempotency

- **Pagination:** assert page size, that cursors advance, and that the final page terminates. Verify no duplicates or gaps across pages under a stable sort.
- **Ordering:** if order is part of the contract, assert it; if not, do not assert it, or the test becomes flaky.
- **Idempotency:** replay PUT and DELETE and confirm the same terminal state. For POST with an idempotency key, replay must not create a second resource.

## Test data and isolation

- Create the data each test needs and clean it up, or use a transaction rolled back per test.
- Never depend on records that another test created; ordering dependencies cause intermittent failures.
- Parameterize identifiers so parallel runs do not collide.
- Keep credentials in the environment or a secret store, never in the repository or in assertions.

## Gotchas

- **Asserting the whole response body** breaks on every additive field. Assert the fields under test plus schema validity.
- **Time and timezone leak into assertions.** Freeze or inject clocks rather than comparing to `now`.
- **Retries can hide flakiness and non-idempotent bugs.** If a retry makes it pass, investigate before adding the retry.
- **Recorded fixtures go stale silently.** Re-record on a schedule or verify against a live contract.
- **Rate limits fail CI unpredictably.** Use a dedicated test tenant or account with known limits.

## Output template

```markdown
## API test result

**Status:** pass | fail | blocked
**Summary:** <endpoints covered and outcome>

### Details
| Endpoint | Case | Expected | Result |
| --- | --- | --- | --- |
| <method path> | <happy, auth, error, pagination> | <status and shape> | <pass or fail> |

Schema source: <OpenAPI or GraphQL SDL used for validation>
Authorization matrix covered: <cases exercised>

### Validation
- Schema validation performed: <checked and result>
- Cross-tenant access case covered: <checked and result>
```

## Quality gate

- [ ] Responses are validated against the declared schema, not hand-written shapes.
- [ ] Every protected endpoint covers unauthenticated, wrong-role, and cross-tenant cases.
- [ ] Error paths assert status, stable error code, and absence of sensitive leakage.
- [ ] Pagination assertions cover advance and termination without duplicates or gaps.
- [ ] Ordering is asserted only when it is part of the contract.
- [ ] Tests create and clean their own data and can run in parallel.
- [ ] No credentials appear in the repository, logs, or assertions.
- [ ] Retries are not used to mask non-deterministic behavior.

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [GraphQL specification](https://spec.graphql.org/)
- [JSON Schema](https://json-schema.org/specification)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
