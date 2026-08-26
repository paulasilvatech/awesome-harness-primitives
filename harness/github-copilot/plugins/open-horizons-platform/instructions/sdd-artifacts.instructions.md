---
applyTo: ".specs/**/*.md,.specs/**/*.yaml,.specs/**/*.json"
description: "Use when editing tracked SDD artifacts that require naming, EARS, traceability, evidence, or status conventions."
---

# Specification-Driven Development Artifacts

The `sdd-spec-engineer` skill owns lifecycle and generation procedures. These instructions own only the durable shape of files under `.specs/`.

## Conventions

- Name feature directories with a zero-padded numeric prefix and kebab-case slug, matching the `feature_id` in artifact frontmatter.
- Use the established uppercase artifact names such as `SPECIFICATION.md`, `DESIGN.md`, `TASKS.md`, `SOURCE_TRACEABILITY.md`, `VERIFICATION.md`, and `DECISIONS.md`.
- Give every normative requirement a unique stable ID and one observable EARS response using `SHALL`; do not reuse retired IDs for different behavior.
- Give acceptance criteria stable IDs tied to their parent requirement.
- Preserve bidirectional traceability from source and decision through requirement, design, task, test, verification, and evidence.
- Distinguish requested, brownfield, official, repository-constraint, and greenfield claims; greenfield behavior requires an explicit decision.
- Treat live-state claims as dated evidence with source, scope, result, and freshness limits. Plans and expected output are not proof of execution.
- Keep status, implementation state, blockers, and verification results truthful; use `PENDING` or `BLOCKED` when evidence is absent.
- Redact credentials, personal data, private tenant details, and sensitive command output from evidence.

## Verification

- Required artifacts, metadata, IDs, and cross-references are internally consistent.
- Every active requirement maps to acceptance, implementation, and verification evidence or an explicit blocker.
- Artifact-only validation is not reported as implementation success.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Preserve stable IDs, explicit source classes, and bidirectional traceability. | Reuse retired IDs or present plans as executed evidence. |
| Keep unknown status and missing evidence visible. | Invent metrics, live state, acceptance, or verification results. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Requirement, acceptance, decision, task, test, and evidence IDs resolve.
- [ ] Status and blockers match available evidence.
- [ ] Sensitive data is redacted from traceability and verification artifacts.
- [ ] Artifact checks pass without claiming implementation success.
