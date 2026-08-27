---
description: >-
  Promote approved SIFAP rule candidates into validated REQ-NNN requirements and a bounded
  architecture handoff.
argument-hint: "feature=<NNN-feature> rules=<approved-rule-artifact>"
---

<!-- Generated from harness/github-copilot/plugins/mainframe-natural-adabas-classic/prompts/sifap-classic-specify.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /sifap-classic-specify

## Objective

Create or update one bounded SIFAP specification from approved archaeology evidence, then validate its
legacy lineage before implementation planning.

## When to Invoke

Use during Stage 2 after rule candidates have domain approval and the feature scope is explicit.

## Preconditions

- Approved rule candidates and their legacy evidence exist.
- The feature destination under `specs/` is known and writable.
- The target repository contains the cited legacy files.
- The SIFAP context and traceability Skills are available.

Stop when approval status, evidence, or scope is unclear.

## Inputs the Team Must Provide

- `feature` - target feature identifier and folder.
- `rules` - approved rule-candidate artifact.
- The scope and out-of-scope decisions.

## What I Will Do

- Load SIFAP context, traceability, and workshop orchestration.
- Write atomic EARS requirements with `REQ-NNN`, real `source_legacy`, and Given/When/Then acceptance.
- Record explicit greenfield decisions and unresolved questions.
- Run the traceability validator and prepare the build handoff.

## What I Will NOT Do

- Promote unapproved or unsupported rule candidates.
- Use placeholder source paths or invent line ranges.
- Implement code or silently choose architecture trade-offs.
- Change identifiers outside the selected feature.

## Output Format

```markdown
## SIFAP specification update

**Status:** valid | needs-decision | blocked
**Feature:** <NNN-feature>

### Artifacts changed
- <spec, plan, ADR, or decision path>

### Traceability
| REQ-ID | Rule candidate | Source | Acceptance |
| --- | --- | --- | --- |

### Validation
- Traceability validator: <command and result>
- Open decisions: <items or none>
```

## Definition of Done

- [ ] Required SIFAP Skills were loaded.
- [ ] Only approved rule candidates were promoted.
- [ ] Every requirement is atomic and uses the `REQ-NNN` contract.
- [ ] Every source resolves or has a concrete greenfield justification.
- [ ] Acceptance criteria are testable Given/When/Then behavior.
- [ ] The traceability validator passes and open decisions are explicit.

## Prompt Body

1. **Validate inputs.** Confirm feature scope, approved rules, destination, and source files.
2. **Load SIFAP contracts.** Load context, traceability, and orchestration Skills.
3. **Promote rules.** Write one EARS behavior and acceptance set per approved candidate.
4. **Record decisions.** Keep greenfield choices and unresolved architecture questions explicit.
5. **Validate lineage.** Run the bundled traceability validator against the feature spec.
6. **Prepare handoff.** Return the bounded build scope, requirements, decisions, checks, and blockers.

## Invocation Example

```text
/sifap-classic-specify feature=001-payment-inspection rules=01-archaeology/business-rules-catalog.md
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `sifap-classic-architect` | agent | Owns requirements and architecture judgment. |
| `sifap-classic-build-slice` | prompt | Implements the approved bounded handoff. |
