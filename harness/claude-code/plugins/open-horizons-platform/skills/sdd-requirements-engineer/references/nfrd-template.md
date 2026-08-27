# Non-Functional Requirements Document template

Use this template for measurable quality constraints. Normative statements follow the [EARS notation](./ears-notation.md). Never fill a target with an industry-sounding default when workload evidence, policy, or an accountable owner has not supplied it.

```markdown
---
title: "<Project or Feature> Non-Functional Requirements Document"
description: "Measurable quality constraints and verification envelopes."
date: "<YYYY-MM-DD>"
version: "0.1.0"
status: "Draft"
companion_frd: "<relative path or not-created>"
---

# Non-Functional Requirements Document: <Project or Feature>

## 1. Document control

| Field | Value |
| --- | --- |
| Owner | <accountable owner> |
| Reviewers | <roles or names> |
| Status | Draft |
| Governing sources | <SRC-IDs> |
| Last reviewed | <YYYY-MM-DD or not-reviewed> |

## 2. Applicability

| Category | Applies | Rationale | Owner |
| --- | --- | --- | --- |
| Performance and capacity | yes/no/unknown | <reason> | <owner> |
| Security and identity | yes/no/unknown | <reason> | <owner> |
| Reliability and recovery | yes/no/unknown | <reason> | <owner> |
| Privacy and compliance | yes/no/unknown | <reason> | <owner> |
| Observability and supportability | yes/no/unknown | <reason> | <owner> |
| Accessibility and localization | yes/no/unknown | <reason> | <owner> |
| Testability and maintainability | yes/no/unknown | <reason> | <owner> |
| Delivery and operability | yes/no/unknown | <reason> | <owner> |
| Data quality, retention, and migration | yes/no/unknown | <reason> | <owner> |
| Cost and resource efficiency | yes/no/unknown | <reason> | <owner> |

## 3. Deployment and measurement contexts

| Context | Workload and data shape | Region or topology | Dependencies | Measurement tooling | Owner |
| --- | --- | --- | --- | --- | --- |
| <context> | <users, rate, payload, dataset> | <scope> | <services> | <tool or BLOCKED> | <owner> |

## 4. Quality requirements

### NFR-<DOMAIN>-001: <Short title>

- Pattern: <EARS pattern>
- Priority: <P0|P1|P2|P3>
- Status: Proposed
- Source: <SRC-###>
- Rationale: <why the constraint is needed>
- Applies to: <contexts>
- Owner: <accountable owner>

> <Canonical EARS statement with an approved measurable constraint, or a statement whose unresolved target is explicitly blocked.>

**Measurement envelope**

| Field | Value |
| --- | --- |
| Metric | <metric> |
| Target | <approved target or BLOCKED> |
| Aggregation | <p95, maximum, rate, count, percentage, or other> |
| Observation window | <duration or BLOCKED> |
| Workload | <load and data shape or BLOCKED> |
| Environment | <context or BLOCKED> |
| Instrumentation | <source of evidence or BLOCKED> |

**Acceptance signals**
- AC-NFR-<DOMAIN>-001-01: <observable pass/fail result under the measurement envelope>

**Verification**
- <test|inspection|analysis|demonstration|measurement>: <planned evidence>

<Repeat for every applicable quality category.>

## 5. Security and compliance decisions

| Decision | Requirement IDs | Source or policy | Owner | State |
| --- | --- | --- | --- | --- |
| Authentication method | NFR-SECURITY-... | SRC-... | <owner> | decided/blocked |
| Authorization model | NFR-SECURITY-... | SRC-... | <owner> | decided/blocked |
| Data classification and protection | NFR-PRIVACY-... | SRC-... | <owner> | decided/blocked |
| Compliance applicability | NFR-COMPLIANCE-... | SRC-... | <owner> | applicable/not-applicable/blocked |

## 6. Technology constraints

| Constraint | Rationale | Source | Requirement IDs | Revisit trigger |
| --- | --- | --- | --- | --- |
| <technology or platform constraint> | <why it is mandatory> | SRC-... | NFR-... | <condition> |

<If no technology is mandated, state "No approved technology constraints." Do not promote preferences into requirements.>

## 7. Requirement summary

| ID | Category | Priority | Contexts | Target state | Source | Status |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-<DOMAIN>-001 | <category> | P0 | <contexts> | defined/blocked | SRC-001 | Proposed |

## 8. Blockers and open questions

| ID | Missing fact or decision | Affected requirement IDs | Owner | Resolution evidence |
| --- | --- | --- | --- | --- |
| BLK-001 | <unknown target or policy> | NFR-... | <owner> | <expected evidence> |

## 9. Review record

| Reviewer | Decision | Date | Evidence or comments |
| --- | --- | --- | --- |
| <reviewer> | pending | <date> | <notes> |
```

## Template checks

- Every applicable category has at least one requirement or an explicit rationale for having none.
- Every numeric target has a source, owner, workload, environment, and observation method.
- Every deployment context is covered by measurable requirements or a visible blocker.
- Security identifies authentication, authorization, protection, and failure behavior when applicable.
- Compliance is explicitly applicable, not applicable, or blocked; it is never silently assumed.
- Technology constraints have evidence and a revisit trigger.
- Approval status is not pre-populated.
