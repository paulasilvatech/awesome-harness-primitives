---
name: create-architectural-decision-record
description: >-
  Create an Architectural Decision Record (ADR) as a structured Markdown document with front
  matter, coded consequences, alternatives, implementation notes, and references. Use when the
  user asks to document an architecture decision, create an ADR, capture alternatives and
  trade-offs, or save a decision under docs/adr.
argument-hint: decision title, context, chosen decision, alternatives, stakeholders
---

<!-- Generated from harness/github-copilot/plugins/mainframe-cobol-db2/skills/create-architectural-decision-record/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create architectural decision record

Turn a decision brief into a machine-parseable and human-readable ADR saved under `/docs/adr/` with sequential numbering, standardized front matter, positive and negative consequences, rejected alternatives, implementation notes, and references.

## When to invoke

- "Create an ADR for this architecture decision."
- "Document why we chose this database."
- "Write an architectural decision record with alternatives."
- "Save this decision under docs/adr."
- "Capture the consequences and implementation notes for this decision."

## Inputs

Use `$ARGUMENTS` and the conversation context to extract:

| Input | Required | Rule |
| --- | --- | --- |
| Decision title | Yes | Short noun phrase used in `ADR-NNNN: [Decision Title]` and the filename slug. |
| Context | Yes | Problem statement, constraints, business requirements, and environment. |
| Decision | Yes | The selected option and rationale. |
| Alternatives | Yes | At least one considered option with rejection rationale. |
| Stakeholders | Yes | Names, roles, or responsible teams for `authors`. |

If a required input cannot be determined, return `blocked` with the missing fields. In interactive environments, ask for the missing information before generating the ADR.

## ADR file rules

| Rule | Required format |
| --- | --- |
| Directory | `/docs/adr/` |
| Filename | `adr-NNNN-[title-slug].md` |
| Numbering | Use the next sequential 4-digit number, for example `adr-0001-database-selection.md`. |
| Status | Start as `Proposed` unless the user specifies `Accepted`, `Rejected`, `Superseded`, or `Deprecated`. |
| Language | Precise, unambiguous, direct prose. |
| Multi-item sections | Use coded bullets with 3-4 letter codes plus 3 digits. |
| Consequences | Include both positive and negative consequences. |
| Alternatives | Include description and rejection reason for each alternative. |
| References | Include related ADRs, external documentation, standards, or `None identified`. |

## Coded bullet taxonomy

| Code | Section | Example |
| --- | --- | --- |
| `POS-001` | Positive consequences | Benefit, quality improvement, operational advantage. |
| `NEG-001` | Negative consequences | Trade-off, limitation, complexity, risk. |
| `ALT-001` | Alternatives considered | Description or rejection reason for a considered option. |
| `IMP-001` | Implementation notes | Rollout, migration, monitoring, success criteria. |
| `REF-001` | References | Related ADR, external documentation, standard. |

## Procedure

1. Extract required inputs from `$ARGUMENTS` and context.
2. Inspect `/docs/adr/` if it exists and determine the next `adr-NNNN` number; use `0001` when no prior ADR exists.
3. Slugify the title with lowercase words separated by hyphens.
4. Generate front matter and body using the required ADR template below.
5. Fill every section with concrete decision content; do not leave placeholder text.
6. Save the file as `/docs/adr/adr-NNNN-[title-slug].md`.
7. Report the created path and any assumptions.

## ADR template

```md
---
title: "ADR-NNNN: [Decision Title]"
status: "Proposed"
date: "YYYY-MM-DD"
authors: "[Stakeholder Names/Roles]"
tags: ["architecture", "decision"]
supersedes: ""
superseded_by: ""
---

# ADR-NNNN: [Decision Title]

## Status

**Proposed** | Accepted | Rejected | Superseded | Deprecated

## Context

[Problem statement, technical constraints, business requirements, and environmental factors requiring this decision.]

## Decision

[Chosen solution with clear rationale for selection.]

## Consequences

### Positive

- **POS-001**: [Beneficial outcomes and advantages]
- **POS-002**: [Performance, maintainability, scalability improvements]
- **POS-003**: [Alignment with architectural principles]

### Negative

- **NEG-001**: [Trade-offs, limitations, drawbacks]
- **NEG-002**: [Technical debt or complexity introduced]
- **NEG-003**: [Risks and future challenges]

## Alternatives Considered

### [Alternative 1 Name]

- **ALT-001**: **Description**: [Brief technical description]
- **ALT-002**: **Rejection Reason**: [Why this option was not selected]

### [Alternative 2 Name]

- **ALT-003**: **Description**: [Brief technical description]
- **ALT-004**: **Rejection Reason**: [Why this option was not selected]

## Implementation Notes

- **IMP-001**: [Key implementation considerations]
- **IMP-002**: [Migration or rollout strategy if applicable]
- **IMP-003**: [Monitoring and success criteria]

## References

- **REF-001**: [Related ADRs]
- **REF-002**: [External documentation]
- **REF-003**: [Standards or frameworks referenced]
```

## Gotchas

- **Do not skip alternatives**: an ADR without rejected alternatives is only a decision memo.
- **Do not use unnumbered filenames**: `adr-NNNN-[title-slug].md` keeps chronology machine-sortable.
- **Do not omit negative consequences**: trade-offs make the decision reviewable later.
- **Do not leave placeholders**: if a field is unknown, block and request it rather than writing `[TBD]`.

## Legacy input aliases

If older automation passes `${input:DecisionTitle}`, `${input:Context}`, `${input:Decision}`, `${input:Alternatives}`, or `${input:Stakeholders}`, map those values into `$ARGUMENTS` fields. Preserve every `multi-item` section as coded bullets.

## Output template

```markdown
## ADR creation result

**Status:** created | blocked | failed
**ADR:** `docs/adr/adr-NNNN-<title-slug>.md`
**Decision:** <one-sentence summary>
**Authors:** <stakeholders>

### Inputs used
| Field | Value |
| --- | --- |
| Context | <summary> |
| Decision | <summary> |
| Alternatives | <count and names> |
| Stakeholders | <names/roles> |

### Validation
- Next ADR number selected: pass | fail
- Required sections populated: pass | fail
- Positive and negative consequences included: pass | fail
- Alternatives include rejection rationale: pass | fail
```

## Quality gate

- [ ] The ADR is saved under `/docs/adr/` with filename `adr-NNNN-[title-slug].md`.
- [ ] The next sequential 4-digit ADR number was determined from existing ADR files.
- [ ] Front matter includes `title`, `status`, `date`, `authors`, `tags`, `supersedes`, and `superseded_by`.
- [ ] Context, Decision, Consequences, Alternatives Considered, Implementation Notes, and References are populated.
- [ ] Positive and negative consequences use `POS-NNN` and `NEG-NNN` coded bullets.
- [ ] Alternatives include both description and rejection reason using `ALT-NNN` coded bullets.
- [ ] Implementation and reference items use `IMP-NNN` and `REF-NNN` coded bullets.
