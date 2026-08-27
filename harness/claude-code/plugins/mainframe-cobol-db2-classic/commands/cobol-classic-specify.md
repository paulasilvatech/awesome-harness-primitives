---
description: >-
  Promote approved COBOL/DB2 rule candidates into REQ-NNN requirements with source lineage,
  decision records, and a dependency-ordered slice plan.
argument-hint: "candidates=<rule-card-path> destination=specs/<NNN>-<feature>"
---

<!-- Generated from harness/github-copilot/plugins/mainframe-cobol-db2-classic/prompts/cobol-classic-specify.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /cobol-classic-specify

## Objective

Convert approved rule candidates into normative requirements, recorded decisions, and a bounded slice plan.

## When to Invoke

Use during the architecture stage after the archaeology gate closed and candidates have owners.

## Preconditions

- Approved rule candidates with cited evidence exist.
- The specification destination is approved.
- The target stack baseline is recorded, or the gap is a known blocker.
- The `cobol-classic-context` and `sdd-requirements-engineer` skills are available.

Stop if candidates are unapproved or the destination is ambiguous.

## Inputs the Team Must Provide

- `candidates` - the approved rule cards with evidence paths.
- `destination` - the specification directory to write.
- Known constraints, the target stack decision, and the business priority order.

## What I Will Do

- Load the required Skills and read the graph and approved evidence.
- Write one active, testable requirement per behavior with Given/When/Then acceptance criteria.
- Attach a real source citation, or an explicit greenfield decision with justification.
- Record a decision for every binding technical choice, including precision and occurrence storage.
- Propose slice order from graph dependency evidence and note where business priority overrides it.

## What I Will NOT Do

- Promote an unapproved or unowned candidate.
- Write one requirement that hides two independent behaviors.
- Adjust a source citation to make a validator pass.
- Leave decimal precision, occurrence storage, or empty-result behavior to the implementer.
- Modify legacy source or implementation code.

## Output Format

```markdown
## COBOL/DB2 specification result

**Status:** ready | needs-decisions | blocked
**Destination:** <specs path>

### Requirements
| REQ-ID | Behavior | Source evidence | Acceptance |
| --- | --- | --- | --- |

### Decisions
| Decision | Choice | Alternatives | Rationale | Record |
| --- | --- | --- | --- | --- |

### Slice plan
| Order | Component | Depends on | Rationale |
| --- | --- | --- | --- |

### Open questions
| Question | Impact | Owner |
| --- | --- | --- |
```

## Definition of Done

- [ ] Required Skills were loaded and the graph was read.
- [ ] Every requirement has one behavior, a valid source or greenfield decision, and testable acceptance.
- [ ] Every binding technical choice has a published decision record.
- [ ] Slice order cites dependency evidence.
- [ ] Unresolved meaning is an open question with an owner, not a requirement.
- [ ] Only the approved destination was written.

## Prompt Body

1. **Validate inputs.** Confirm candidate approval and the destination; stop if either is unclear.
2. **Load context.** Load context, loop, and requirements Skills.
3. **Write requirements.** One behavior each, with acceptance criteria and a real source citation.
4. **Record decisions.** Capture precision, occurrence, null, and empty-result choices explicitly.
5. **Plan slices.** Order by graph dependency and mark business overrides.
6. **Deliver.** Write only the approved destination and report open questions.

## Invocation Example

```text
/cobol-classic-specify candidates=01-archaeology/rules/payment-duplicates.md destination=specs/001-payment-inspection
```

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `cobol-classic-architect` | agent | Owns requirement and design judgment. |
| `sdd-requirements-engineer` | skill | Supplies EARS requirement structure and lineage rules. |
| `cobol-classic-build-slice` | prompt | Implements the approved slice. |
