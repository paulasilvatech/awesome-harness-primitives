---
name: "security-self-review"
description: "Self-review checklist for security and OWASP Top 10 issues in a newly built feature."
argument-hint: "context=<context> files=<Controller>.java,<Service>.java,<Entity>.java"
agent: "builder"
tools: ["read", "search", "edit"]
---
# /security-self-review

## Objective

Scan a newly built feature for common security issues aligned with the OWASP Top 10. The output is a prioritized report — the agent does not fix issues automatically; the team decides.

## When to Invoke

After a bounded context has been implemented (entities, services, controllers, tests) and before moving to Stage 4.

## Preconditions

- The feature code exists and compiles
- The team specifies which controller(s), service(s), and entity/entities to review

## Inputs the Team Must Provide

- The feature scope: which controller, service, and entity classes to review
- The bounded context name

## What I Will Do

- Scan for hardcoded secrets (strings that resemble keys, passwords, or tokens)
- Check for SQL injection vectors (string concatenation in queries)
- Check authentication/authorization annotations on endpoints
- Check input validation coverage
- Look for sensitive data in logs or error responses
- Identify missing rate limits on write endpoints
- Flag dependency areas where a real security scan should be run

## What I Will NOT Do

- Run a real security scanner (I perform static analysis by reading code)
- Fix problems automatically — the team reviews and decides what to fix
- Fabricate severity ratings — each rating is justified by the finding
- Guarantee completeness — this is a self-review, not a formal audit

## Output Format

A Markdown report at `03-implementation/security-review-[context].md`:

```markdown
# Security Self-Review — [Bounded Context]
## Summary
Findings: N total | High: N | Medium: N | Low: N
## Findings
| # | Severity | Category | File:Line | Description | Remediation |
## Areas Requiring External Scanning
## Approval
```

## Definition of Done

- [ ] Every controller endpoint was checked for authentication annotations
- [ ] Every query was checked for SQL injection
- [ ] No hardcoded secrets were found (or all are flagged)
- [ ] Input validation coverage is assessed for each endpoint
- [ ] The report has severity ratings justified by findings
- [ ] At least one "area requiring external scanning" is identified

## Prompt Body

You are the `@builder` performing a security self-review. This is not a formal audit — it is a quick check before the team moves to Stage 4.

**Step 1 — Scan for hardcoded secrets.**
Search the specified files for patterns that suggest hardcoded secrets:

- Strings containing "password", "secret", "key", "token", or "api_key" (case-insensitive)
- Strings that resemble Base64-encoded tokens (long alphanumeric strings)
- Properties or environment variable references defined with literal values instead of `${ENV_VAR}`
- Files named `.env` committed to the repository

For each finding: file path, line number, suspicious pattern (redacted if it appears to be a real secret), and severity (High).

**Step 2 — Check for SQL injection.**
Search for:

- String concatenation in SQL queries (`"SELECT..." + variable`)
- `@Query` annotations with string interpolation instead of named parameters
- Any use of `nativeQuery = true` (flag for manual review; do not reject automatically)
- Use of `JdbcTemplate` with string concatenation

For each finding: file, line, vulnerable pattern, and remediation (use named parameters or derived queries).

**Step 3 — Check authentication and authorization.**
For each `@RestController` endpoint:

- Check whether `@PreAuthorize`, `@Secured`, or method-level security is present
- Check whether the controller is under a path covered by Spring Security filter chains
- Flag any publicly accessible endpoint without an apparent justification

For each unprotected endpoint: file, line, endpoint method and path, and severity (High if it modifies data, Medium if read-only).

**Step 4 — Check input validation.**
For each endpoint that accepts a request body:

- Check whether `@Valid` is present on the parameter
- Check whether the request DTO has Bean Validation annotations
- Look for any `String` field without `@Size` or `@Pattern` constraints

For each gap: file, line, unvalidated field, and remediation.

**Step 5 — Check for sensitive data exposure.**
Search for:

- Logging statements that may emit sensitive fields (passwords, tokens, personal data)
- Error responses that expose stack traces or internal details
- Response DTOs that include fields such as `password`, `token`, or `ssn`

**Step 6 — Identify rate-limiting opportunities.**
Flag any write endpoint (POST, PUT, DELETE) without rate limiting. Note: the team may not implement rate limiting during the workshop, but it must be documented as a production concern.

**Step 7 — Compile the report.**
Write to `03-implementation/security-review-[context].md`, with all findings ordered by severity (High first). Include a summary count and a section listing areas where a real scanner (SAST/DAST) should be run.

This report does not block Stage 4 — it is informational. The team decides which findings to fix now and which to defer.

## Invocation Example

```
/security-self-review context=<context> files=<Controller>.java,<Service>.java,<Entity>.java
```
