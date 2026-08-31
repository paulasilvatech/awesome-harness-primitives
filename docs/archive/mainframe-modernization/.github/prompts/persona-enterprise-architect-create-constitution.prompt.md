---
name: "create-constitution"
description: "Write .specify/memory/constitution.md — the numbered, testable, non-negotiable rules for the feature."
argument-hint: "feature=NNN-feature-name"
agent: "enterprise-architect"
tools: ["read", "search", "edit"]
---
# /create-constitution

## Objective

Produce `.specify/memory/constitution.md` — a short (≤ 80 lines), numbered set of testable, non-negotiable rules grouped by category, each with a violation consequence and a mutable-or-immutable marker. ADRs make decisions; the constitution defines the boundaries those decisions cannot cross.

## When to Invoke

At the start of a feature (or the project), before ADRs and specs come to depend on shared constraints. Re-run it to amend the constitution through the documented process.

## Preconditions

- `specs/<NNN>-<feature>/` exists, or the project scope is agreed
- Organizational constraints are known (security baseline, Azure-only, OWASP Top 10, LGPD)
- Any parent constitution to inherit from is identified

## Inputs the Team Must Provide

- `feature=<NNN>-<feature>` (or `project`)
- The existing organizational constraints to encode
- Any parent constitution to inherit from
- The named approvers (enterprise architect, technical lead, InfoSec)
- Ask the user for anything that is missing.

## What I Will Do

- Inherit from the parent constitution and adapt it, with explicit justification
- Group rules by Stack, Security, Data, Operations, Process, and Compliance
- Make every rule testable and give it an ID (`C1`, `C2`, …)
- State the consequence of violating each rule
- Mark each rule mutable (relaxable via ADR + InfoSec sign-off) or immutable
- Date the file, version it with semver, and record the approvers
- Keep it at or under 80 lines

## What I Will NOT Do

- Write principles ("we value quality") instead of rules ("Java 21 only")
- Emit a rule without an ID or a violation consequence
- Exceed 80 lines — a constitution nobody can remember does not work
- Invent an organizational constraint or an approver — I ask the team
- Decide a specific design trade-off — that is an ADR via `/create-adr`

## Output Format

The deliverable is `.specify/memory/constitution.md`:

```markdown
# CONSTITUTION — 001-pagamento-beneficio

- **Version**: 1.0.0
- **Date**: 2026-04-29
- **Approvers**: @paula (enterprise architect), @morgan (technical lead), @infosec-lead
- **Scope**: rules applicable to this feature

## 1. Stack
| ID | Rule | Consequence |
|---|---|---|
| C1 | Backend runs only on Java 21 (Temurin) and Spring Boot 3.3. | Build fails. |
| C2 | Frontend runs on Next.js 15 with TypeScript `strict: true`. No `any`. | Lint blocks merge. |
| C3 | PostgreSQL 16 is the only system of record for SIFAP data. | InfoSec exception required. |

## 2. Security
| ID | Rule | Consequence |
|---|---|---|
| C4 | Service-to-service auth uses Azure Managed Identity. No client secrets in code or config. | PR blocked. |
| C5 | Secrets are read from Key Vault at runtime. No committed `.env`. | Gitleaks blocks merge. |
| C6 | OWASP Top 10 baseline: input validation, parameterized SQL, no string-built queries. | PR rejected. |

## 3. Data
| ID | Rule | Consequence |
|---|---|---|
| C7 | PII columns carry a `COMMENT` flagging them as PII. | DBA review blocks. |
| C8 | No production PII in `dev` or `stage`. Synthetic data only. | InfoSec finding, immediate revert. |

## 4. Operations
| ID | Rule | Consequence |
|---|---|---|
| C9 | Every public endpoint emits a structured log with `requestId`, `userId`, `latencyMs`. | Code review blocks. |
| C10 | Every user-facing endpoint has an SLO recorded in a `REQ-OPS-*`. | Spec review blocks. |

## 5. Process
| ID | Rule | Consequence |
|---|---|---|
| C11 | One branch per work item, cut from `develop` with the persona prefix per `00-GIT-WORKFLOW.md` (`spec/`, `impl/`, `infra/`, `docs/`, `agent/`). No direct commits to `develop` or `main`. | PR rejected. |
| C12 | Every requirement uses EARS notation and every test cites a `REQ-ID`. | Spec review blocks. |

## 6. Compliance
| ID | Rule | Consequence |
|---|---|---|
| C13 | LGPD subject-rights endpoints (read, delete, export) are covered by `REQ-COMP-*`. | Compliance review blocks release. |

## 7. Mutable vs immutable
- Mutable (relaxable via ADR + InfoSec sign-off): C9–C12.
- Immutable (constitutional change required): C1, C3, C4, C5, C6, C7, C8, C13.

## 8. Amendment process
Open a PR for this file. The architecture forum reviews it and bumps the version (`1.0.0` -> `1.1.0` minor, `-> 2.0.0` major). New approvers sign off.
```

## Definition of Done

- [ ] The file is ≤ 80 lines, excluding signatures
- [ ] Every rule has an ID and a violation consequence
- [ ] At least one rule exists per category (Stack, Security, Data, Operations, Process, Compliance)
- [ ] The mutable-versus-immutable distinction is stated
- [ ] The amendment process is documented
- [ ] It inherits from a parent constitution when one exists
- [ ] Approvers, date, and a semver version are recorded

## Prompt Body

You are the `@enterprise-architect`. The team needs the boundaries fixed before decisions and code depend on them.

**Step 1 — Inherit and adapt.**
Start from the project-level constitution. Tighten or relax it for this feature only, with explicit justification.

**Step 2 — Group rules by category.**
Stack, Security, Data, Operations, Process, Compliance.

**Step 3 — Make every rule testable.**
"Use Java 21" is testable (`mvnw --version`); "use modern Java" is not.

**Step 4 — Number the rules.**
`C1`, `C2`, … so reviewers can cite them.

**Step 5 — State the consequence.**
"Build fails", "PR rejected", or "InfoSec exception required" — never silence.

**Step 6 — Mark mutable or immutable.**
Some rules relax through an ADR with InfoSec sign-off; others require a new constitution.

**Step 7 — Date, version, and sign.**
Record the forum date, named approvers, and version `1.0.0`. Bump the version only when the constitution itself changes.

Keep it to rules, not principles, and keep it under 80 lines. A specific design trade-off belongs in an ADR via `/create-adr`, not in a constitutional rule.

## Invocation Example

```
/create-constitution feature=001-pagamento-beneficio
```
