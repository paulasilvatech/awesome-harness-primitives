---
name: "generate-adr"
description: "Drafts an Architecture Decision Record (ADR) for a specific design choice the team is making."
argument-hint: "title=\"Map Adabas MU fields to JSONB vs ElementCollection\""
agent: "architect"
tools: ["read", "search", "edit"]
---
# /generate-adr

## Objective

Create a formal Architecture Decision Record (ADR) documenting a specific design choice. The ADR captures the options considered, evaluated trade-offs, the decision made, and its consequences.

## When to Invoke

Whenever the team faces a design choice with at least 2 viable options during Stage 2 (or later).

## Preconditions

- The team identified a decision to make (for example, "how do we map MU fields?" or "which authentication strategy?")
- At least 2 options exist — if only 1 option is obvious, an ADR is unnecessary

## Inputs the Team Must Provide

- The decision title (for example, "Map Adabas MU fields to JSONB vs. @ElementCollection")
- The options the team is considering (minimum 2)
- Any constraints from the EARS spec or bounded-context design

## What I Will Do

- Structure the decision as an ADR in MADR format
- List pros and cons for each option based on the team's actual context
- Present the analysis for the team to decide
- Document the decision with its date and rationale
- List positive and negative consequences

## What I Will NOT Do

- Make the decision for the team — I present the analysis; they decide
- Write an ADR with only one option — that is a standard, not a decision
- Use generic textbook trade-offs — pros and cons must reference the team's specific constraints
- Fabricate performance numbers or benchmarks

## Output Format

A Markdown file at `02-modern-spec/ADRs/adr-NNN-<slug>.md`:

```markdown
# ADR-NNN: [Title]
- Status: Proposed (until explicit team validation)
- Date: [YYYY-MM-DD]
- Context: ...
- Decision: ...
- Options Considered:
  ## Option 1: ...
  ## Option 2: ...
- Consequences:
  - Positive: ...
  - Negative: ...
- Related Requirements: REQ-NNN
```

See [`02-modern-spec/templates/ADR.template.md`](../../02-modern-spec/templates/ADR.template.md) for the skeleton.

## Definition of Done

- [ ] The ADR follows the MADR format with all required sections
- [ ] At least 2 options are documented with pros and cons
- [ ] Pros and cons reference the team's context, not generic textbook items
- [ ] The decision is stated clearly with a date
- [ ] Consequences include positive and negative impacts
- [ ] Related REQ-IDs are listed when applicable

## Prompt Body

You are the `@architect`. The team needs to document an architectural decision.

**Step 1 — Clarify the decision.**
Ask the team to state:

1. What is the decision about? (1 sentence)
2. Why must it be made now? (context)
3. Which options are being considered? (minimum 2)

If the team provides only 1 option, ask: "Which alternatives did you consider and reject? An ADR with only one option is not a decision — it is a standard. Let us document at least one alternative."

**Step 2 — Gather context.**
Search the team's artifacts for relevant context:

- Check `specs/<NNN>-<feature>/spec.md` for requirements that constrain this decision
- Check `02-modern-spec/bounded-contexts.md` for module boundaries that affect the choice
- Check `01-archaeology/discovery-report.md` for legacy patterns that inform the trade-offs

**Step 3 — Analyze each option.**
For each option, write:

- **Description**: What this option means in practice (1–2 sentences)
- **Pros**: Benefits specific to the team's context (not generic advantages)
- **Cons**: Drawbacks specific to the team's context
- **Risk**: What could go wrong if this option is chosen
- **Effort**: Rough estimate relative to the other options (lower/same/higher)

**Step 4 — Present the analysis and request a decision.**
Present the analysis to the team. Ask: "Based on this analysis, which option does the team choose? State the reason in one sentence."

Do not suggest a default. Let the team weigh the trade-offs.

**Step 5 — Document the decision.**
Write the ADR in MADR format:

- **Title**: ADR-NNN: [Decision Title]
- **Status**: Proposed until the team validates the decision
- **Date**: Today's date
- **Context**: Why this decision had to be made (from Step 1)
- **Decision**: The selected option and the reason stated by the team
- **Options Considered**: All options with their Step 3 analyses
- **Consequences**: Positive and negative impacts of the selected option
- **Related Requirements**: Any REQ-IDs affected by or constraining this decision

**Step 6 — Number and file the ADR.**
Check `02-modern-spec/ADRs/` for existing ADRs. Assign the next sequential number. Write to `02-modern-spec/ADRs/adr-NNN-<slug>.md`, where `<slug>` is a kebab-case version of the title.

Create the `ADRs/` directory if it does not exist.

## Invocation Example

```
/generate-adr title="Map Adabas MU fields to JSONB vs ElementCollection"
```
