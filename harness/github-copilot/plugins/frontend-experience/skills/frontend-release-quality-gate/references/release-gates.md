# Frontend release gates

## Severity

| Severity | Meaning | Default verdict impact |
| --- | --- | --- |
| Critical | Primary task impossible, severe data/security/access failure, or no viable workaround | Blocked |
| High | Core behavior, accessibility, contract, or recovery failure with material impact | Blocked |
| Medium | Important defect with a viable workaround and bounded scope | Follow-up only with explicit acceptance |
| Low | Limited polish or low-risk issue | Follow-up with owner |

## Evidence categories

Static, unit/component, mock, contract, real-service, E2E, visual, accessibility, performance, discoverability, mobile/desktop, installation, MCP, and prompt execution are separate categories. One cannot stand in for another.

## Follow-up contract

Every accepted follow-up records owner, severity, exact action, affected acceptance IDs, user impact, workaround, due/review date, and retest procedure.

Manual evidence records reviewer, environment, steps, expected, actual, date, and artifact reference. `Not-applicable` requires product or repository evidence.
