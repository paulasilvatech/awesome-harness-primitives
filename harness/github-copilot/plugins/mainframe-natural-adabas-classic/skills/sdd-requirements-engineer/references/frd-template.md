# Functional Requirements Document template

Use this template after gap analysis. Normative statements follow the [EARS notation](./ears-notation.md). Keep the document `Draft` or `Ready for review` until an accountable reviewer records approval.

```markdown
---
title: "<Project or Feature> Functional Requirements Document"
description: "Implementation-neutral functional scope and observable behavior."
date: "<YYYY-MM-DD>"
version: "0.1.0"
status: "Draft"
project_context: "<greenfield|brownfield|modernization|migration|api|mobile|data|saas|internal-tool|cli|infrastructure>"
companion_nfrd: "<relative path or not-created>"
---

# Functional Requirements Document: <Project or Feature>

## 1. Document control

| Field | Value |
| --- | --- |
| Owner | <accountable owner> |
| Reviewers | <roles or names> |
| Status | Draft |
| Governing sources | <SRC-IDs> |
| Last reviewed | <YYYY-MM-DD or not-reviewed> |

## 2. Problem and outcomes

### 2.1 Problem
<Observed problem and affected actors.>

### 2.2 Desired outcomes
| Outcome ID | Observable outcome | Source |
| --- | --- | --- |
| OUT-001 | <business or user outcome> | SRC-001 |

### 2.3 Success signals
| Signal | Measure | Target or blocker | Evidence owner |
| --- | --- | --- | --- |
| <signal> | <how observed> | <approved target or BLOCKED> | <owner> |

## 3. Scope

### 3.1 In scope
- <bounded capability>

### 3.2 Out of scope
- <explicit exclusion and rationale>

### 3.3 Assumptions and blockers
| ID | Type | Statement | Impact if wrong | Owner | State |
| --- | --- | --- | --- | --- | --- |
| ASM-001 | assumption | <statement> | <impact> | <owner> | open |
| BLK-001 | blocker | <missing decision> | <blocked work> | <owner> | open |

## 4. Actors and permissions

| Actor | Goal | Allowed actions | Prohibited actions | Source |
| --- | --- | --- | --- | --- |
| <role> | <goal> | <actions> | <boundaries> | SRC-001 |

## 5. Domain model and lifecycle

| Domain term | Definition | Source |
| --- | --- | --- |
| <term> | <unambiguous definition> | SRC-001 |

<Add a Mermaid state diagram when an entity has a lifecycle. Otherwise state "No lifecycle-dependent entity identified.">

## 6. Functional requirements

### FR-<DOMAIN>-001: <Short title>

- Pattern: <EARS pattern>
- Priority: <P0|P1|P2|P3>
- Status: Proposed
- Source: <SRC-###>
- Rationale: <why the behavior is needed>
- Dependencies: <requirement IDs or none>

> <Canonical EARS statement with one observable response.>

**Acceptance signals**
- AC-FR-<DOMAIN>-001-01: <observable pass/fail outcome>

**Verification**
- <test|inspection|analysis|demonstration>: <planned evidence>

**Failure and recovery**
- <linked unwanted-behavior requirement IDs or not applicable>

<Repeat by domain. Do not organize requirements by UI screen or implementation layer.>

## 7. External interactions

| Interaction | Direction | Contract or event | Failure behavior | Requirement IDs |
| --- | --- | --- | --- | --- |
| <system> | inbound/outbound | <contract> | <observable response> | FR-... |

## 8. Requirement summary

| ID | Domain | Pattern | Priority | Source | Status |
| --- | --- | --- | --- | --- | --- |
| FR-<DOMAIN>-001 | <domain> | <pattern> | P0 | SRC-001 | Proposed |

## 9. Delivery increments

| Increment | Objective | Requirement IDs | Dependencies | Exit signal |
| --- | --- | --- | --- | --- |
| 1 | <reviewable outcome> | FR-... | <IDs or none> | <observable signal> |

## 10. Open questions

| ID | Question | Blocks | Owner | Due |
| --- | --- | --- | --- | --- |
| Q-001 | <question> | <requirement or artifact> | <owner> | <date or TBD> |

## 11. Review record

| Reviewer | Decision | Date | Evidence or comments |
| --- | --- | --- | --- |
| <reviewer> | pending | <date> | <notes> |
```

## Template checks

- Every actor is referenced by at least one requirement or explicitly declared informational.
- Every P0 requirement has a release-impact rationale.
- Error and recovery behavior is explicit for each primary action.
- Requirements remain implementation-neutral and atomic.
- Summary rows exactly match the normative requirement records.
- Approval status is not pre-populated.
