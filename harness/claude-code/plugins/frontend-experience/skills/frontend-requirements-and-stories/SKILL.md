---
name: frontend-requirements-and-stories
description: >-
  Convert frontend intent and repository evidence into INVEST-shaped user stories, Given/When/Then
  acceptance criteria, journey and state maps, and story-to-test traceability. Use this skill when
  feature discovery, acceptance criteria, Definition of Done, or an implementation handoff is
  needed.
---

<!-- Generated from harness/github-copilot/plugins/frontend-experience/skills/frontend-requirements-and-stories/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend requirements and stories

Produce stable, observable frontend requirements that engineering and QA can implement and verify without inventing product facts.

## When to invoke

- "Write user stories and acceptance criteria for this frontend feature."
- "Map this UI journey, states, and failure paths."
- "Create a Definition of Done for this screen."
- "Turn this product request into testable frontend requirements."
- "Build a story-to-test traceability matrix."

## Story contract

Each story includes:

- stable `US-NNN` identifier;
- evidence-backed actor, goal, and user value;
- scope and explicit non-goals;
- preconditions, access rights, primary path, alternatives, failures, and recovery;
- `AC-NNN` Given/When/Then criteria describing observable behavior;
- surface, accessibility, data, backend, localization, and analytics considerations when supplied;
- scenario and evidence mapping.

Read [references/invest-and-gherkin.md](references/invest-and-gherkin.md) for splitting and wording rules. Use [assets/user-story.md](assets/user-story.md) and [assets/traceability-matrix.md](assets/traceability-matrix.md) when the project has no existing format.

## Procedure

1. Inventory approved requirements, repository behavior, product language, schemas, tests, and known constraints.
2. Separate verified facts, inferences, unknowns, non-goals, and decisions needed.
3. Split work by independently valuable user outcome; do not split only by component or technical layer.
4. Assign stable story and acceptance IDs and describe success, applicable failure, access, cancellation, offline, and recovery behavior.
5. Add responsive, input, accessibility, localization, and backend expectations only when relevant.
6. Map each acceptance ID to at least one `SC-NNN` scenario and a proposed automated layer or manual procedure.
7. Review every criterion for observability and remove adjectives such as "modern", "clean", "fast", or "intuitive" unless quantified.

## Acceptance states

Consider, but do not force, these states: initial, loading, empty, partial, success, invalid, unauthorized, forbidden, not found, conflict, rate limited, unavailable, timeout, offline, cancelled, retried, stale, and recovered.

Mark a state `not applicable` only with product, repository, or contract evidence.

## Limits

- Do not invent personas, analytics, metrics, permissions, business rules, research, or hidden backend behavior.
- Do not prescribe a framework or implementation detail as an acceptance criterion unless it is an approved constraint.
- Do not mark a criterion complete; implementation and QA evidence own completion.

## Progressive disclosure and bundled resources

- [references/invest-and-gherkin.md](references/invest-and-gherkin.md): story splitting and observable acceptance rules.
- [assets/user-story.md](assets/user-story.md): fallback story template.
- [assets/traceability-matrix.md](assets/traceability-matrix.md): fallback story-to-scenario-to-evidence template.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Frontend requirements result
**Status:** ready | needs decision | blocked

### Evidence and unknowns
| Item | Classification | Source / owner |
| --- | --- | --- |

### Stories
#### US-001 — <user value>
- Actor / goal / value:
- Scope / non-goals:
- Preconditions / access:
- Paths and states:
- AC-001: Given ... When ... Then ...

### Traceability
| Story | Acceptance | Scenario | Risk | Proposed evidence |
| --- | --- | --- | --- | --- |
```

## Quality gate

- [ ] Story IDs and acceptance IDs are stable and unique.
- [ ] Actors, value, product language, and rules are evidence-backed.
- [ ] Criteria describe observable behavior in Given/When/Then form.
- [ ] Applicable success, failure, access, adaptation, accessibility, and recovery states are covered.
- [ ] Every acceptance ID maps to a scenario and proposed evidence.
- [ ] Unknowns and decisions are explicit; no implementation preference masquerades as behavior.
