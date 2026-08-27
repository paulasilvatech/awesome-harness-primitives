---
name: sdd-requirements-engineer
description: >-
  Elicits, normalizes, validates, and traces requirements through a complete Spec-Driven
  Development workflow using EARS. Use when converting notes, PRDs, legacy evidence, or design
  inputs into FRD/NFRD, SPECIFICATION.md, architecture and task artifacts, traceability matrices,
  quality gates, or an implementation-ready SDD handoff.
---

<!-- Generated from harness/github-copilot/plugins/mainframe-cobol-db2-classic/skills/sdd-requirements-engineer/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# SDD EARS Requirements Engineer

Turn incomplete product intent or existing design evidence into atomic EARS requirements and a coherent Spec-Driven Development artifact set. Preserve provenance from the first source through design, tasks, verification, and implementation handoff.

## When to invoke

- "Turn these notes into an FRD and NFRD using EARS."
- "Run the complete SDD workflow for this feature."
- "Convert this design into traceable EARS requirements and tasks."
- "Review these requirements or SDD artifacts for gaps and orphaned work."
- "Prepare an implementation-ready handoff from this approved specification."

## Operating modes

| Mode | Starting point | Deliverable |
| --- | --- | --- |
| Requirements | Raw notes, PRD, issue, interview notes, or legacy evidence | Gap analysis plus FRD and NFRD |
| Full SDD | Raw or approved requirements | Requirements, specification, analysis, design, tasks, gates, decisions, verification, and traceability |
| Design-first | Architecture sketch, API contract, data model, or prototype | Recovered requirements, explicit assumptions, then the full SDD chain |
| Validation | Existing FRD, NFRD, specification, design, or task set | Severity-ranked findings, corrected EARS statements, and readiness decision |
| Handoff | Reviewed SDD artifacts | Bounded implementation package with gates, dependencies, and unresolved blockers |

Select the smallest mode that satisfies the request. Do not generate the full artifact set for a single-requirement review.

## Source and evidence policy

Use this precedence order:

1. User-approved goals, constraints, and decisions.
2. Repository evidence such as existing specifications, code, tests, schemas, ADRs, issues, and operational configuration.
3. Dated first-party documentation for external platform behavior that must be current.
4. Explicit assumptions with an owner, impact, and confirmation state.

Assign each source a stable `SRC-###` identifier. A derived artifact is not the primary source of a requirement when the original user, repository, or official source is available. Never invent a target, quota, price, benchmark, compliance obligation, or approval state.

## Procedure

1. Establish scope and action.
   - Inspect existing repository instructions, templates, specifications, and naming conventions before creating files.
   - Identify whether the request is requirements-first, design-first, validation-only, or handoff-only.
   - Record the requested output paths and whether the user already authorized file creation. If file creation was not requested, return drafts or review findings without writing.

2. Classify the project context.

   | Context | Required emphasis |
   | --- | --- |
   | Greenfield | Outcomes, success signals, non-goals, assumptions |
   | Brownfield | Current behavior, delta scope, compatibility, regression boundaries |
   | Modernization or migration | Source parity, data correctness, cutover, rollback, decommissioning |
   | API or platform | Consumers, contracts, versioning, rate limits, compatibility |
   | Mobile or edge | Connectivity states, supported platforms, synchronization, recovery |
   | Data or AI system | Data quality, lineage, model or schema evolution, evaluation, fallback |
   | SaaS or multi-tenant | Isolation, onboarding, entitlement, noisy-neighbor controls |
   | Internal tool or CLI | Identity context, distribution, installation, supportability |
   | Infrastructure | Access model, environments, reliability, observability, rollback |

3. Run the ambiguity and gap gate.
   - Classify each gap as `PRESENT`, `BLOCKER`, `HIGH-RISK ASSUMPTION`, or `NOT APPLICABLE`.
   - Treat actors and permissions, primary outcome, scope boundary, and authoritative source as blockers when absent.
   - Ask no more than three focused blocker questions, one at a time. Do not ask about facts that repository evidence answers.
   - Record unresolved high-risk items rather than replacing them with silent defaults.

4. Author or normalize requirements.
   - Read the [EARS notation reference](references/ears-notation.md) before writing normative requirements.
   - Use the [FRD template](references/frd-template.md) and [NFRD template](references/nfrd-template.md) when those artifacts are in scope.
   - Assign stable IDs such as `FR-AUTH-001`, `NFR-SECURITY-001`, and `AC-FR-AUTH-001-01`.
   - Write one observable system response per EARS statement. Split compound behavior.
   - Keep functional requirements implementation-neutral. Put genuine technology constraints in the NFRD with rationale and source evidence.
   - Give every requirement a priority, source, rationale, acceptance signal, verification method, and lifecycle status.
   - Express numeric NFRs with measurement context: metric, target, workload, percentile or aggregation, observation window, environment, and evidence owner. If any required value is unknown, keep a visible blocker.
   - Add a state model when behavior depends on an entity lifecycle.

5. Build the SDD artifact chain.
   - Read the [SDD artifact templates](references/spec-templates.md).
   - Reuse the repository-level constitution when one exists. Do not create a conflicting feature-local constitution.
   - For full SDD, create or update the applicable specification, analysis, design, tasks, checklist, cross-analysis, verification, decisions, and source-traceability artifacts.
   - Add `IMPLEMENTATION_PLAN.md`, `TEST_PLAN.md`, or a machine-readable test manifest only when repository conventions or risk justify separate artifacts.
   - Use Mermaid for concise vendor-neutral logical views. When a design names Microsoft, Azure, or GitHub products or needs an editable professional diagram, use `azure-draw-io-diagram-generator` (`skill`) and require official assets, icon provenance, accessible labels, and editable `.drawio` source.
   - Mark a task `[P]` only when it has no unmet dependency and cannot conflict on files, state, schema, or environment.
   - Use sequential feature folders such as `001-feature-name` only when starting or following that repository convention.

6. Enforce end-to-end traceability.
   - Give every active requirement one explicit row in `SOURCE_TRACEABILITY.md`.
   - Map each active requirement to design components, tasks, acceptance criteria, and planned or executed verification in `CROSS_ANALYSIS.md`.
   - Reject orphan requirements, orphan design elements, orphan tasks, and tests with no governing requirement.
   - Record transferred, superseded, split, merged, or retired IDs in a disposition table. Never silently renumber stable requirements.
   - Preserve the same normative meaning across FRD/NFRD, specification, design, tasks, and tests. Link by ID instead of copying text that can drift.

7. Validate and hand off.
   - Apply every applicable check in the [unified quality gates](references/quality-gates.md).
   - Use the [anti-pattern catalog](references/anti-patterns.md) to repair defects before delivery.
   - Keep artifacts `Draft` or `Ready for review` until an accountable reviewer approves them.
   - Use `Implemented` or `Verified` only when repository or execution evidence supports the claim.
   - Hand off only the approved scope, artifact paths, dependency order, gate results, and unresolved blockers. Do not start implementation as part of this skill.

## EARS requirement contract

Every normative requirement record contains:

| Field | Rule |
| --- | --- |
| ID | Stable, unique, domain-scoped |
| Pattern | Exactly one of ubiquitous, event-driven, state-driven, optional, unwanted, or complex |
| Statement | Canonical EARS clause order with `shall` and one observable response |
| Priority | P0, P1, P2, or P3 with release-impact rationale |
| Source | `SRC-###` evidence or an explicit greenfield assumption |
| Rationale | Why the behavior or quality constraint is needed |
| Acceptance | At least one pass/fail signal |
| Verification | Planned test, inspection, analysis, demonstration, or measurement |
| Status | Proposed, ready for review, approved, implemented, verified, or retired |

Prioritize from evidenced release impact: P0 blocks the named increment; P1 loses material value or risk reduction but has an approved workaround; P2 is deferrable without violating the increment objective; P3 has no material release impact. Split an increment when its P0 set is not reviewable.

## Limits
- Do not implement product code, mutate infrastructure, or deploy resources.
- Do not claim stakeholder approval, compliance, performance, or verification without evidence.
- Do not overwrite an existing constitution, requirement ID scheme, or artifact convention without an explicit compatibility decision.
- Do not use a design-first route to bypass requirements, acceptance signals, or source traceability.
- Do not force every optional artifact into small changes when a lighter, traceable artifact set is sufficient.

## Gotchas
- User stories express intent but are not normative EARS requirements.
- A requirement and its acceptance signal must agree, but should not duplicate conflicting normative text.
- `shall` belongs in the EARS statement; descriptive prose may use ordinary language.
- A technology named by a stakeholder is not automatically a functional requirement. Classify it as a sourced constraint or an unresolved design preference.
- A task can be parallel only when both dependency and change-surface conflicts are absent.

## Related primitives
- `azure-draw-io-diagram-generator` (`skill`): create and validate editable professional diagrams with permitted official assets and provenance after the SDD design scope is established.

## Progressive disclosure and bundled resources

- [EARS notation](references/ears-notation.md): syntax, classification, examples, defects, and academic references.
- [FRD template](references/frd-template.md): functional scope, actors, domain requirements, acceptance, and phased delivery.
- [NFRD template](references/nfrd-template.md): measurable quality constraints and measurement envelopes.
- [SDD artifact templates](references/spec-templates.md): complete artifact responsibilities and concise templates.
- [Unified quality gates](references/quality-gates.md): detailed readiness, EARS, traceability, and handoff checks.
- [Anti-pattern catalog](references/anti-patterns.md): requirement and SDD defects with corrective action.

## Output template

Return exactly this structure:

```markdown
## SDD EARS result

**Status:** completed | ready-for-review | blocked
**Mode:** requirements | full-sdd | design-first | validation | handoff
**Project context:** <classification>
**Summary:** <one-sentence outcome>

### Artifacts
| Artifact | Path or result | Status |
| --- | --- | --- |
| <name> | <path, draft, or not requested> | <draft|ready-for-review|blocked> |

### Requirements and gaps
- Functional requirements: <count>
- Non-functional requirements: <count>
- Blockers: <IDs and reason, or none>
- High-risk assumptions: <IDs and owner, or none>

### EARS and traceability evidence
- EARS validation: <passed count>/<applicable count>
- Source coverage: <covered requirements>/<active requirements>
- Cross-artifact coverage: <covered requirements>/<active requirements>
- Orphans or lifecycle dispositions: <none or summary>

### Quality gates
- Result: <pass|fail>
- Failed checks: <gate IDs and fixes, or none>
- Approval state: <draft|ready-for-review|approved with evidence>

### Handoff
- Ready for implementation: <yes|no>
- Approved scope: <requirement IDs or none>
- Dependencies: <ordered summary>
- Open questions: <questions or none>
```

## Quality gate

- [ ] The selected operating mode is the smallest one that satisfies the request.
- [ ] Source precedence, assumptions, blockers, and file-write authorization are explicit.
- [ ] Every normative requirement satisfies the EARS requirement contract.
- [ ] FRD and NFRD content is complete for every applicable category.
- [ ] SDD artifacts are internally consistent and proportional to scope.
- [ ] Vendor-specific architecture diagrams use official permitted assets, provenance, accessible labels, and editable source through `azure-draw-io-diagram-generator`.
- [ ] Every active requirement traces from source through design, tasks, acceptance, and verification.
- [ ] Requirement lifecycle changes preserve IDs or include explicit dispositions.
- [ ] No metric, approval, compatibility claim, current platform fact, or vendor asset status is fabricated.
- [ ] Every applicable detailed check in the [unified quality gates](references/quality-gates.md) passes or is reported as a blocker.
- [ ] The response follows `## Output template` exactly.
- [ ] Every bundled resource referenced by this skill exists.
