# SIFAP workshop flow

| Stage | Outcome | Gate before handoff |
| --- | --- | --- |
| 1. Archaeology | Inventory, dependency map, rule candidates, and open questions | Claims cite inspected legacy evidence; unresolved meaning remains open. |
| 2. Architecture | Approved scope, `REQ-NNN` requirements, ADRs, and modular-monolith plan | Every approved requirement has a valid source and testable acceptance criteria. |
| 3. Build | Bounded implementation slices and behavior-equivalence tests | Relevant tests and builds pass; intentional behavior changes are recorded. |
| 4. Quality | Requirement verification, Adabas-to-PostgreSQL mapping, and reconciliation numbers | Every requirement is verified and every in-scope legacy file reconciles or is explicitly excluded. |
| 5. Operations | Hardened delivery, reviewed delegation, IaC, runbook, and retrospective | No blind merge or deployment; evidence and human approvals are recorded. |

Branch intent for the workshop is `spec/<NNN>-<feature>`, `impl/<NNN>-<feature>`,
`infra/<component>`, `docs/<topic>`, and `agent/<issue-NN>`. Confirm the target repository's actual
branch policy before creating a branch or making GitHub mutations.

Stage agents guide decisions and handoffs. Reusable procedures live in skills, and `sifap-loop` runs a
stage as a bounded correction loop with an observable gate. Persona agents are optional workshop aids and
must not duplicate the stage workflow or domain references.
