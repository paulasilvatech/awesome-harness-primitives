---
name: "api-validate"
description: "Validate an API implementation against its OpenAPI/AsyncAPI contract and report every drift with an explicit fix location."
argument-hint: "contract=<openapi.yaml|asyncapi.yaml> impl=<controllers path>"
agent: "software-architect"
tools: ["read", "search"]
---
# /api-validate

## Objective

Compare an API implementation with its OpenAPI/AsyncAPI contract and expose all
drift. The deliverable is a classified drift report — breaking, additive, or
metadata — with an explicit fix location (contract or code) for each finding. Full
coverage is the bar: every contract operation and every implementation endpoint is
checked.

## When to Invoke

After a controller or handler changes, before merging, or during review when the
implementation and its published contract might disagree.

## Preconditions

- A contract file exists (`openapi.yaml` or `asyncapi.yaml`)
- The implementation exists (controllers or message handlers created by the team)
- The REST conventions in [`../instructions/backend.instructions.md`](../instructions/backend.instructions.md) are the reference for paths and status codes

## Inputs the Team Must Provide

- The path to the contract file
- The path to the implementation (controllers, handlers)
- Example request/response payloads, if available

Ask the user for anything that is missing.

## What I Will Do

- Load the contract and enumerate every operation
- For each operation, check path, method, request schema, response schema, error codes, and auth scheme against the code
- For each implementation endpoint, check whether the contract documents it (find undocumented endpoints)
- Validate request and response schemas against real examples when provided
- Classify each drift as breaking, additive, or metadata, and name the fix location

## What I Will NOT Do

- Edit the contract or the code — I report drift and propose fixes; the owner applies them
- Invent operations, fields, or status codes that neither side declares
- Treat an additive optional field as breaking — I triage by real impact
- Decide an irreversible contract change beyond naming the cheaper, safer side — that is redirected to the [`../skills/adr-draft/SKILL.md`](../skills/adr-draft/SKILL.md) skill

## Output Format

A Markdown table presented for review. Example (illustrative):

```markdown
## API drift — orders-service

| Endpoint | Drift Type | Severity | Fix Location |
|----------|-----------|----------|--------------|
| GET /api/v1/orders/{id} | Response field `status` missing in code | Breaking | code |
| POST /api/v1/orders | Undocumented 409 returned by code | Additive | contract |
| GET /api/v1/orders | Description mismatch | Metadata | contract |
```

## Definition of Done

- [ ] Every contract operation has been checked (100% coverage)
- [ ] Every implementation endpoint has been checked against the contract
- [ ] Breaking drift is listed separately from additive drift
- [ ] The fix location (contract vs. code) is explicit for each item
- [ ] Undocumented endpoints are reported

## Prompt Body

You are the `@software-architect`. The team wants to know whether an API and its
contract still agree.

**Step 1 — Load both sides.**
Read the contract (`openapi.yaml` / `asyncapi.yaml`) and the implementation
(controllers, handlers). Ask for either path if it is missing.

**Step 2 — Check each contract operation.**
For every operation in the contract, verify against the code: path, HTTP method,
request schema, response schema, declared error codes, and the authentication
scheme. Record any mismatch.

**Step 3 — Check for undocumented endpoints.**
For every endpoint in the implementation, confirm the contract declares it. Flag
any endpoint the contract does not document.

**Step 4 — Validate with examples.**
When the team provides example payloads, validate them against both the declared
request and response schemas. Note where a real example violates the contract.

**Step 5 — Classify and locate the fix.**
Classify each drift as breaking (removes or changes a field, method, or status),
additive (new optional field or undocumented-but-compatible behavior), or metadata
(description only). For each, state whether the correct fix belongs in the contract
or the code.

Report the table without editing either side. Do not downgrade a breaking change
to additive to make the report look cleaner.

## Invocation Example

```
/api-validate contract=backend/src/main/resources/openapi.yaml impl=backend/src/main/java/app/orders
```
