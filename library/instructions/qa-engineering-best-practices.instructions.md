---
applyTo: "**"
description: "Enforces QA engineering conventions for test strategy, naming, assertions, data, automation, CI/CD evidence, bug reports, and coverage across any stack."
---

# QA Engineering Conventions — Test Strategy and Evidence

These instructions apply to test code, QA documentation, automation, defect reports, and CI/CD quality gates in any technology stack. They are authoritative for QA engineering practices, test pyramid decisions, naming, assertions, test data, mocks, API/UI/performance testing, coverage interpretation, and defect evidence; language-specific test primitives and project CI definitions win when they set stricter framework syntax or required commands.

## Core Testing Principles

- Test early and test often; write tests alongside code so defects are cheaper to isolate.
- Test one behavior at a time; each case should verify one logical assertion or one coherent outcome.
- Treat tests as first-class code; apply the same readability, naming, refactoring, and review standards used for production code.
- Fail fast with clear, actionable failure messages that point to the broken behavior.
- Keep tests deterministic by removing randomness, timing dependencies, shared mutable state, and environment leakage.
- Keep tests independent so they can run in isolation and in any order.

## Test Pyramid and Coverage Priorities

| Layer | Scope | Quantity | Speed | Use for |
| --- | --- | --- | --- | --- |
| Unit | Single function or class | Many, roughly 60–70 % | Milliseconds | Business logic, edge cases, pure rules |
| Integration | Module boundaries, DB, API contracts | Moderate, roughly 20–30 % | Seconds | Service contracts, persistence, adapters |
| End-to-End | Full user journey across UI and backend | Few, roughly 5–10 % | Minutes | Critical user paths and smoke suites |

Aim for meaningful coverage instead of a percentage target. Prioritize critical paths, complex logic, and previously buggy areas; use line coverage, branch coverage, and mutation scores to find edge cases rather than to game metrics.

## Test Naming and Structure

Use Given / When / Then or `should_doX_whenY` consistently. Group related tests in `describe` or `context` blocks named after the unit under test, and use `it` or `test` for cases that read as standalone sentences.

**Good:** `test('should return 404 when product id does not exist')` and `test('given an expired token, when the user calls /me, then it returns 401')`.

**Bad:** `test('test1')` and `test('check user')` hide the scenario, action, and expected result.

## Assertions, Exceptions, and Data

- Prefer one logical assertion per test where practical; group related property checks only when the same behavior is being verified.
- Use specific matchers such as `toContain`, `toBeGreaterThan`, and `toMatchObject` instead of broad equality or truthiness checks.
- Assert exact expected values, for example `expect(result).toBe(42)`, not `expect(result).toBeTruthy()`.
- For exception testing, assert both exception type and message.
- Prefer positive assertions on the happy path; use negative assertions only when absence is the contract.
- Create data with factories or builders, keep it minimal, use unique identifiers per run, and reset or isolate state with in-memory DBs, transactions rolled back, or mocked dependencies.
- Never use production data or PII in tests.

## Mocking, Stubbing, and Boundaries

Mock at external boundaries such as HTTP clients, DB adapters, message queues, clocks, and third-party services. Prefer real implementations for pure functions and simple value objects. Use stubs for controlled return data and mocks when interaction verification is the point of the test. Reset all mocks between tests and document non-obvious mocking decisions.

## API, UI, and End-to-End Testing

| Area | Convention |
| --- | --- |
| API assertions | Validate status code, response schema, headers, response time, and consistent error response bodies. |
| HTTP methods | Cover every exposed method: GET, POST, PUT, PATCH, DELETE. |
| Auth paths | Cover valid token, expired token, missing token, and wrong role. |
| Boundary values | Include empty string, null, max length, special characters, and Unicode. |
| Idempotency | Assert idempotency for PUT and DELETE operations. |
| UI behavior | Test user-visible behavior, not CSS classes or internal state. |
| Selectors | Prefer role, then label, then test-id, then text. |
| Waits | Use explicit waits for visible, enabled, and network idle states; do not use `sleep`, `Thread.Sleep`, or fixed waits. |
| Evidence | Capture screenshots and traces on failure. |

Run end-to-end suites against stable, isolated environments, not shared staging. Keep scenarios short and focused; compose long journeys from smaller reusable steps.

## Performance, Reliability, and CI/CD

Define SLOs before writing performance tests: p50, p95, p99 latency, throughput, and error rate. Include ramp-up, steady state, and ramp-down phases; distinguish load testing, stress testing, and soak testing. Use realistic data volumes and track results over time to detect performance regressions.

Fast tests such as unit tests and lint must run on every commit. Slow integration and E2E suites should run on PR merge, nightly, or another explicit gate. CI output must include test name, failure reason, and relevant logs; archive JUnit XML, coverage HTML, traces, and other artefacts. Configure flaky test detection with one retry and flag tests as flaky after repeated inconsistency.

## Bug Reporting Standards

A defect report must include title, environment, steps to reproduce, expected result, actual result, severity, and attachments. Titles should name component, action, and symptom, for example `[Checkout] Order total is incorrect when coupon is applied`. Severity values are Critical, High, Medium, and Low, and they must map to business impact.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `auto-retry` `browser/runtime` `environment-specific` `implementation-focused` `label` `main/trunk` `p50/p95/p99` `role` `text`.

## Good / Bad Examples

The examples below show precise assertions and user-visible behavior.

**Good:**

```typescript
expect(response.status).toBe(200);
expect(response.body.items).toHaveLength(3);
expect(response.body.items[0]).toMatchObject({ status: 'active' });
```

Why: The assertions identify the expected status, collection size, and relevant object shape.

**Bad:**

```typescript
expect(response).toBeTruthy();
expect(response.body).not.toBeNull();
```

Why: Truthiness only proves that something exists; it does not prove the required behavior.

## Conventions

| Rule | Rationale |
|---|---|
| Keep tests deterministic, independent, and runnable in any order | Reliable suites isolate defects instead of creating false failures |
| Match each test to the cheapest pyramid layer that proves the risk | Fast feedback remains affordable while critical paths stay covered |
| Name tests with scenario, action, and expected result | Failure output remains understandable without opening the implementation |
| Use exact, specific assertions and exception checks | Diagnostics show what broke and why |
| Use factories, builders, unique identifiers, and isolated state | Test data stays minimal and avoids cross-test collisions |
| Mock only at boundaries and reset mocks between tests | Business logic remains exercised and mock state does not leak |
| Prefer accessible selectors and explicit waits in UI tests | Tests follow user behavior and avoid timing flakes |
| Archive reports, coverage, screenshots, traces, and logs in CI | Failures remain reproducible after the CI job ends |

## Do / Do Not

| Do | Do not |
|---|---|
| Write tests beside or with the behavior they protect | Add tests only after defects reach QA |
| Use unit tests for business logic and edge cases | Push simple logic coverage into slow E2E suites |
| Use integration tests for DB, API contracts, and adapters | Mock every layer until contracts are untested |
| Reserve E2E tests for critical journeys and smoke coverage | Build long, brittle E2E scripts for every branch |
| Assert `expect(result).toBe(42)` | Assert `expect(result).toBeTruthy()` when a value matters |
| Use role, label, test-id, then text selectors | Assert internal state or CSS implementation details |
| Include deterministic reproduction steps in bug reports | File vague defects without environment or evidence |
| Treat coverage as a risk signal | Treat 100 % line coverage as proof of quality |

## Checklist Before Opening a PR

- [ ] New behavior is covered at the appropriate pyramid level.
- [ ] Tests are named clearly with the project convention.
- [ ] Assertions check exact outcomes, exception types, messages, schemas, headers, or timings as applicable.
- [ ] Test data is minimal, isolated, unique per run, and free of production data or PII.
- [ ] Mocks are boundary-level, documented when non-obvious, and reset between tests.
- [ ] UI and E2E tests avoid `sleep`, `Thread.Sleep`, arbitrary timeouts, and implementation-only selectors.
- [ ] API tests cover methods, auth paths, boundary values, error schemas, and idempotency where relevant.
- [ ] CI publishes actionable failure output and archives reports, coverage, traces, and logs.
