---
name: 'create-architectural-decision-record'
description: 'Create an AI-optimized Architectural Decision Record for a documented technical decision.'
agent: 'agent'
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'githubRepo', 'openSimpleBrowser', 'problems', 'runTasks', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI']
argument-hint: 'DecisionTitle=<title>'
---

# /create-architectural-decision-record

## Objective

Create an AI-optimized Architectural Decision Record for a documented technical decision, including context, chosen decision, consequences, rejected alternatives, implementation notes, references, front matter, and coded bullets for machine parsing and human review.

## When to Invoke

Use this prompt after the team has made or proposed a technical decision that should be recorded before implementation, review, or future trade-off analysis.

## Preconditions

- `${input:DecisionTitle}` is provided.
- Context, decision, alternatives, and stakeholders are provided or available from the conversation.
- The `/docs/adr/` directory may be created or updated.
- The next sequential 4-digit ADR number can be determined from existing `adr-NNNN-[title-slug].md` files.

## Inputs the Team Must Provide

- `DecisionTitle` — the title of the decision.
- `Context` — `${input:Context}` with problem statement, constraints, business requirements, and environmental factors.
- `Decision` — `${input:Decision}` with the chosen solution and rationale.
- `Alternatives` — `${input:Alternatives}` with options considered and rejection rationale.
- `Stakeholders` — `${input:Stakeholders}` with names or roles.
- Ask the user for missing required inputs before generating the ADR.

## What I Will Do

- Create an ADR in `/docs/adr/` using `adr-NNNN-[title-slug].md` where `NNNN` is the next sequential 4-digit number.
- Use precise, unambiguous language and standardized ADR format with front matter.
- Include positive and negative consequences.
- Document alternatives with rejection rationale.
- Use coded bullets with 3–4 letter codes plus 3-digit numbers, such as `POS-001`, `NEG-001`, `ALT-001`, `IMP-001`, and `REF-001`.
- Structure the document for machine parsing and human reference.

## What I Will NOT Do

- Generate an ADR when context, decision, alternatives, or stakeholders are missing and cannot be determined.
- Record a decision that the team has not made or clearly proposed.
- Skip negative consequences or rejected alternatives.
- Use a non-sequential ADR number or a filename outside `/docs/adr/`.
- Leave placeholder text in the final ADR.

## Output Format

Create the ADR using this template:

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

## Definition of Done

- [ ] Required inputs were provided or explicitly confirmed from context.
- [ ] The ADR is saved in `/docs/adr/` as `adr-NNNN-[title-slug].md` with the next sequential 4-digit number.
- [ ] Front matter includes title, status, date, authors, tags, supersedes, and superseded_by.
- [ ] Status, Context, Decision, Consequences, Alternatives Considered, Implementation Notes, and References are complete.
- [ ] Positive and negative consequences are both documented.
- [ ] Alternatives include descriptions and rejection reasons.
- [ ] Multi-item sections use coded bullets with 3–4 letter codes plus 3-digit numbers.

## Prompt Body

Follow these steps in order.

**Step 1 — Validate required inputs.** Confirm `DecisionTitle`, `Context`, `Decision`, `Alternatives`, and `Stakeholders`. If any required input is missing and cannot be determined from conversation history, ask the user to provide it before generating the ADR.

**Step 2 — Determine the ADR number and path.** Inspect `/docs/adr/` for existing `adr-NNNN-[title-slug].md` files. Choose the next sequential 4-digit number. Slugify the title and create `/docs/adr/adr-NNNN-[title-slug].md`.

**Step 3 — Write front matter.** Set `title` to `ADR-NNNN: [Decision Title]`, `status` to `Proposed` unless the user provides another valid status, `date` to `YYYY-MM-DD`, `authors` to stakeholder names or roles, `tags` to `["architecture", "decision"]`, and empty `supersedes` and `superseded_by` unless known.

**Step 4 — Document context and decision.** Write the problem statement, technical constraints, business requirements, environmental factors, chosen solution, and clear rationale.

**Step 5 — Document consequences and alternatives.** Include positive consequences with `POS-001` numbering and negative consequences with `NEG-001` numbering. For each alternative, include coded description and rejection reason entries such as `ALT-001` and `ALT-002`.

**Step 6 — Add implementation notes and references.** Include key implementation considerations, migration or rollout strategy, monitoring and success criteria, related ADRs, external documentation, standards, or frameworks with `IMP-001` and `REF-001` style bullets.

**Step 7 — Validate the ADR.** Check precise language, machine-parseable structure, no placeholders, correct numbering, correct filename, and complete rationale.

## Invocation Example

```
/create-architectural-decision-record DecisionTitle="Adopt PostgreSQL for transactional storage"
```
