# Unified SDD EARS quality gates

Apply every relevant check. Mark a check `PASS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE` and cite the artifact, requirement ID, source ID, or evidence used. A package passes only when no applicable check fails or remains blocked.

## G1. Scope and evidence

- [ ] G1.01 The operating mode and requested deliverables are explicit.
- [ ] G1.02 The project context and system boundary are identified.
- [ ] G1.03 Primary actors, permissions, and prohibited actions are known.
- [ ] G1.04 The primary outcome and scope boundary are known.
- [ ] G1.05 Existing repository artifacts and conventions were inspected.
- [ ] G1.06 Every source has a stable `SRC-###` ID and source class.
- [ ] G1.07 Assumptions have impact, owner, and confirmation state.
- [ ] G1.08 Unsupported targets, policies, or approvals remain visible blockers.
- [ ] G1.09 File creation occurred only when requested or explicitly authorized.

## G2. EARS requirements

- [ ] G2.01 Every normative requirement has a unique stable ID.
- [ ] G2.02 Every normative requirement records exactly one EARS classification.
- [ ] G2.03 Clause order matches the selected EARS pattern.
- [ ] G2.04 The statement uses `shall` and names the responsible system or component.
- [ ] G2.05 The statement has one observable response and no hidden compound behavior.
- [ ] G2.06 Preconditions, triggers, optionality, and unwanted conditions are explicit when applicable.
- [ ] G2.07 Functional requirements state behavior, not implementation.
- [ ] G2.08 Every requirement has a source, rationale, priority, acceptance signal, verification method, and status.
- [ ] G2.09 Every priority has an impact-based rationale.
- [ ] G2.10 Error, invalid-input, timeout, dependency-failure, and recovery paths are covered where applicable.
- [ ] G2.11 Lifecycle-dependent behavior has a state model and state-driven requirements.
- [ ] G2.12 Terms and units are defined consistently.

## G3. FRD readiness

- [ ] G3.01 Problem, desired outcomes, success signals, in-scope items, and non-goals are explicit.
- [ ] G3.02 Every actor participates in a requirement or is explicitly informational.
- [ ] G3.03 Requirements are grouped by domain and preserve stable IDs.
- [ ] G3.04 External interactions include contracts and failure behavior.
- [ ] G3.05 Summary rows match normative records exactly.
- [ ] G3.06 Delivery increments are dependency ordered and reviewable.
- [ ] G3.07 Every P0 requirement is justified as essential to the named increment.
- [ ] G3.08 Open questions identify owner and affected scope.

## G4. NFRD readiness

- [ ] G4.01 Every quality category has an applicability decision.
- [ ] G4.02 Every applicable category has requirements or an explicit blocker.
- [ ] G4.03 Every metric defines target, aggregation, window, workload, environment, instrumentation, and owner.
- [ ] G4.04 Every numeric target cites evidence or accountable-owner approval.
- [ ] G4.05 Every deployment context has coverage or a visible blocker.
- [ ] G4.06 Authentication, authorization, data protection, and abuse or failure behavior are covered when applicable.
- [ ] G4.07 Reliability requirements define detection, degradation, recovery, RTO, or RPO only when applicable and sourced.
- [ ] G4.08 Compliance is applicable, not applicable, or blocked with an owner.
- [ ] G4.09 Accessibility and localization scope is explicit for user-facing surfaces.
- [ ] G4.10 Data quality, lineage, migration, retention, and deletion are covered when applicable.
- [ ] G4.11 Technology constraints are sourced, justified, and have revisit triggers.

## G5. SDD artifact integrity

- [ ] G5.01 The existing repository constitution is reused or a justified governing artifact exists.
- [ ] G5.02 `SPECIFICATION.md` contains the canonical active requirements.
- [ ] G5.03 `ANALYSIS.md` records evidence, gaps, risks, and alternatives.
- [ ] G5.04 `DESIGN.md` covers architecture, data, interfaces, security, failures, and trade-offs required by scope.
- [ ] G5.05 Mermaid diagrams are present and valid when visual architecture, state, sequence, or data flow is material.
- [ ] G5.06 `TASKS.md` is dependency ordered and every task has an expected evidence result.
- [ ] G5.07 Every `[P]` task is independent in both dependencies and change surface.
- [ ] G5.08 `CHECKLIST.md` contains review, implementation, verification, and release gates applicable to scope.
- [ ] G5.09 `DECISIONS.md` records consequential choices, alternatives, consequences, evidence, and revisit triggers.
- [ ] G5.10 Optional artifacts exist only when repository conventions or risk justify them.

## G6. Traceability and lifecycle

- [ ] G6.01 Every active requirement has one explicit primary-source row.
- [ ] G6.02 Every active requirement maps to design, tasks, acceptance, and verification.
- [ ] G6.03 Every design element maps to one or more governing requirements.
- [ ] G6.04 Every implementation task maps to one or more requirements or a sourced governance obligation.
- [ ] G6.05 Every verification item maps to a requirement and acceptance signal.
- [ ] G6.06 No active requirement, design element, task, or verification item is orphaned.
- [ ] G6.07 Copied summaries do not redefine or contradict canonical normative statements.
- [ ] G6.08 Split, merged, transferred, superseded, and retired IDs have explicit dispositions.
- [ ] G6.09 Stable historical IDs are not silently bulk-renamed.
- [ ] G6.10 Cross-artifact counts and status values agree.

## G7. Readiness and handoff

- [ ] G7.01 Artifact statuses do not exceed available approval or execution evidence.
- [ ] G7.02 Failed and blocked checks include owner and corrective action.
- [ ] G7.03 The approved implementation scope is an explicit set of requirement IDs.
- [ ] G7.04 Dependencies and ordering are clear to an implementation agent.
- [ ] G7.05 Required validation evidence and stop conditions are explicit.
- [ ] G7.06 Current external behavior cites dated first-party evidence.
- [ ] G7.07 The handoff excludes unresolved blockers.
- [ ] G7.08 The delivery report follows the skill output template.

## Decision rule

- `PASS`: all applicable checks pass.
- `READY FOR REVIEW`: no blockers remain, but accountable approval is pending.
- `BLOCKED`: at least one required fact, decision, source, or mapping is absent.
- `FAIL`: an applicable artifact or requirement violates a check that can be corrected from available evidence.

Do not convert `BLOCKED` or `FAIL` into success-shaped wording.
