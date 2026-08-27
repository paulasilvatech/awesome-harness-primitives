---
description: >-
  Capture a modernization brief with scope, drivers, constraints, non-goals, risks, and success
  criteria.
argument-hint: legacy system folder or modernization initiative
---

<!-- Generated from harness/github-copilot/prompts/modernize-brief.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /modernize-brief

## Objective

Create the entry brief for a modernization initiative from a legacy system folder or business request, capturing scope, drivers, stakeholders, constraints, non-goals, risks, compliance needs, data sensitivity, runtime constraints, timeline, success criteria, and open questions before the rest of the staged workflow begins.

## When to Invoke

Use this prompt first in the seven-stage modernization workflow, before `modernize-assess`, `modernize-extract-rules`, `modernize-map`, `modernize-reimagine`, `modernize-transform`, and `modernize-harden` refine or implement the modernization plan.

## Preconditions

- The target legacy system folder or modernization initiative is identified.
- The workspace may contain existing business, technical, or operational context for the system.
- Writing to `analysis/brief.md` or `analysis/<system>/BRIEF.md` is permitted.
- Business context that cannot be inferred from files can be requested from the user.
- The `code-modernization` skill is available as the authoritative modernization workflow reference.

## Inputs the Team Must Provide

- `target` — the legacy system folder or modernization initiative to brief.
- Known business driver, stakeholder, timeline, compliance, runtime, and success-criteria context.
- Preferred output location when both `analysis/brief.md` and `analysis/<system>/BRIEF.md` are plausible.
- Ask the user for anything that is missing and cannot be inferred from files; stop if the missing context would change scope or commitments.

## What I Will Do

- Load the `code-modernization` skill before drafting or editing artifacts.
- Inspect available files only as needed to ground the brief.
- Identify scope, business driver, stakeholders, constraints, non-goals, and success criteria.
- Record known risks, compliance requirements, data sensitivity, runtime constraints, and timeline.
- Write `analysis/brief.md` for a portfolio-level initiative or `analysis/<system>/BRIEF.md` for a system-specific initiative.
- Include open questions for business and technical owners.

## What I Will NOT Do

- Perform a full inventory, complexity analysis, dependency review, or security audit; `modernize-assess` owns that work.
- Extract detailed business rules from code; `modernize-extract-rules` owns cited rule cards.
- Design target architecture, map migration boundaries, transform code, or harden a module.
- Invent stakeholder decisions, compliance obligations, data classifications, timelines, or success metrics.
- Edit legacy source code or modernized code while creating the brief.

## Output Format

Write or return this artifact shape:

```markdown
# Modernization Brief — <system-or-initiative>

## Scope
- In scope:
- Out of scope:

## Business Drivers
- Driver:
- Expected value:

## Stakeholders
| Role | Name or group | Decision area | Open question |
| --- | --- | --- | --- |

## Constraints and Non-Goals
### Constraints
- Runtime:
- Compliance:
- Data sensitivity:
- Timeline:

### Non-Goals
- 

## Risks
| Risk | Impact | Likelihood | Mitigation | Owner |
| --- | --- | --- | --- | --- |

## Success Criteria
- 

## Assumptions
- 

## Open Questions
| Question | Owner | Needed by | Blocks |
| --- | --- | --- | --- |
```

## Definition of Done

- [ ] The `code-modernization` skill was loaded before the artifact was drafted.
- [ ] Scope, business drivers, stakeholders, constraints, non-goals, risks, and success criteria are captured.
- [ ] Compliance requirements, data sensitivity, runtime constraints, and timeline are recorded or explicitly marked unknown.
- [ ] The brief is written to `analysis/brief.md` or `analysis/<system>/BRIEF.md`.
- [ ] Open questions identify whether business or technical owners must answer them.
- [ ] The response returns only the artifact path, assumptions, open questions, and validation status.

## Prompt Body

Follow these steps in order. Ask only for missing business context that cannot be inferred from files.

**Step 1 — Load the modernization workflow.**
Load the `code-modernization` skill and use it as the shared vocabulary for the rest of the staged workflow.

**Step 2 — Establish the target.**
Resolve `${input:target:legacy system folder or modernization initiative}` to either a portfolio-level initiative or one legacy system. If the target is ambiguous, ask for clarification before writing.

**Step 3 — Gather brief evidence.**
Inspect available README files, planning notes, deployment notes, code comments, or folder names only as needed to identify scope, business driver, stakeholders, constraints, non-goals, success criteria, known risks, compliance requirements, data sensitivity, runtime constraints, and timeline.

**Step 4 — Separate facts from assumptions.**
Record inspected facts as facts. Record inferred or user-provided items as assumptions when evidence is incomplete. Do not turn guesses into commitments.

**Step 5 — Write the brief.**
Write `analysis/brief.md` for a cross-system initiative. Write `analysis/<system>/BRIEF.md` when the brief applies to one named system.

**Step 6 — Prepare the handoff.**
List open questions for business and technical owners. State that `modernize-assess` should consume the brief next to inventory the system and identify risks.

**Step 7 — Report concisely.**
Return only the artifact path, assumptions, open questions, and validation status.

## Invocation Example

```
/modernize-brief target=legacy system folder or modernization initiative
```
