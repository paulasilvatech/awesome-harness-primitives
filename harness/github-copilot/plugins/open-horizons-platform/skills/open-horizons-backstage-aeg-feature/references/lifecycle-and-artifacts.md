# AEG lifecycle and artifacts

## Lifecycle

| Stage | Primary evidence | Completion signal | Human boundary |
| --- | --- | --- | --- |
| N0 | `CONSTITUTION.md` | Scope, guardrails, and accountable owners are explicit. | The requester confirms intent and constraints. |
| L1 | `specs/FRD_*.md`, `specs/NFRD_*.md` | EARS requirements have stable IDs, sources, and acceptance criteria. | G1 accepts or rejects scope and requirement risk. |
| L2 | `docs/adr/ADR-*.md` | Decisions, alternatives, consequences, and requirement coverage are recorded. | G2 accepts or rejects architecture readiness. |
| L3 | `specs/tasks.yaml` | Approved work is decomposed with dependencies and validation. | G3 remains pull-request review in GitHub. |
| L4 | Tests, findings, and runtime evidence | Implementation evidence closes tasks or drives a bounded back-edge. | G4 remains deployment-environment approval. |
| N5 | `specs/traceability.yaml`, delivery report | Requirement-to-resource evidence is complete or explicitly blocked. | Reuse and closeout remain reviewable decisions. |

## Intent classes

| Intent | Required context |
| --- | --- |
| `greenfield` | Need, outcome, constraints, environment profile, and explicit greenfield confirmation. |
| `modernization` | Source repository, target outcome, read-only AS-IS assessment, and migration constraints. |
| `change` | Managed component, feature or bug-fix class, expected behavior, and reproduction evidence for defects. |
| `system` | System name, repository topology, dependency boundaries, and release-train policy when known. |

Use `worker_engine: inherit` unless an approved run policy selects a specific engine. A worker engine
is an execution choice, not the identity of the AEG lifecycle.

## Evidence invariants

- Every status claim comes from a run response or named artifact.
- Every active requirement has a stable ID and an observable acceptance criterion.
- Traceability follows requirement to ADR, task, test, resource, and delivery evidence.
- Findings preserve severity, source, owner, and the loop that must address them.
- Missing evidence produces `blocked` or an explicit gap; it never produces a synthetic success.
- Cost data names its billing unit, source period, and engine before comparison.
- Closed traceability is required before a run can support a reusable profile proposal.

## Gate packages

G1 includes scope, assumptions, out-of-scope items, FRD/NFRD coverage, EARS gaps, and the highest-risk
requirements. G2 includes ADRs, rejected alternatives, requirement-to-decision coverage, readiness of
tasks and traceability, cost assumptions, resolved conflicts, and open findings.

Rejection feedback is preserved verbatim as an actionable finding for the owning loop. Approval
advances only the named gate and never implies pull-request or production approval.
