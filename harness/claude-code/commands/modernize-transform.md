---
description: >-
  Transform a bounded legacy module into modernized code with behavior-pinning tests and
  validation evidence.
argument-hint: legacy module and target stack
---

<!-- Generated from harness/github-copilot/prompts/modernize-transform.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /modernize-transform

## Objective

Transform one bounded legacy module or behavior slice into modernized code under `modernized/**`, using relevant brief, assessment, rules, map, and design artifacts to preserve required behavior and produce behavior-pinning tests plus validation evidence.

## When to Invoke

Use this prompt after `modernize-reimagine` has defined the target architecture and before `modernize-harden` reviews the transformed module for security, behavior drift, testing, observability, and operations readiness.

## Preconditions

- The legacy module and target stack are identified.
- Relevant brief, assessment, rules, map, and design artifacts are available or explicitly absent.
- The legacy source remains read-only unless the user explicitly requests otherwise.
- Writing under `modernized/**` and the repository's test locations is permitted.
- The `code-modernization` skill is available.

## Inputs the Team Must Provide

- `target` — the legacy module and target stack to transform.
- The bounded behavior slice to implement.
- Relevant `analysis/<system>/BRIEF.md`, `analysis/<system>/ASSESSMENT.md`, `analysis/<system>/RULES.md`, `analysis/<system>/MAP.md`, and `analysis/<system>/DESIGN.md` when available.
- Test and validation constraints, including available commands.
- Ask the user for anything that is missing; stop if the behavior slice or target stack is undefined.

## What I Will Do

- Load the `code-modernization` skill before editing code.
- Confirm the legacy source remains read-only unless the user explicitly requests otherwise.
- Read the relevant brief, assessment, rules, map, and design artifacts.
- Select one bounded legacy module or behavior slice.
- Load `legacy-characterization-testing` to select the behavior oracle and define behavior-pinning tests.
- Implement the modernized module under `modernized/**`.
- Run available tests and compare behavior against legacy evidence or recorded cases.

## What I Will NOT Do

- Rewrite the whole system in one pass or expand beyond one bounded module or behavior slice.
- Modify legacy source unless the user explicitly requests it.
- Change required behavior without recording it as an intentional behavior change from `modernize-reimagine`.
- Skip behavior-pinning tests when behavior evidence exists.
- Treat compilation alone as behavior equivalence.
- Harden unrelated modules; `modernize-harden` owns the readiness review after transformation.

## Output Format

Return applied changes and evidence in this shape:

```markdown
## Modernize Transform Result

### Target
- Legacy module:
- Target stack:
- Behavior slice:

### Changed Files
- `modernized/...`

### Behavior-Pinning Tests
| Test | Legacy evidence or recorded case | Expected behavior |
| --- | --- | --- |

### Behavior Equivalence Evidence
- Source rule:
- Legacy evidence:
- Modernized result:

### Tests Run
| Command | Result | Notes |
| --- | --- | --- |

### Blockers
- 
```

## Definition of Done

- [ ] The `code-modernization` skill was loaded before editing code.
- [ ] Relevant brief, assessment, rules, map, and design artifacts were read or explicitly marked unavailable.
- [ ] Exactly one bounded legacy module or behavior slice was transformed.
- [ ] Modernized code is implemented under `modernized/**`.
- [ ] Behavior-pinning tests are defined and added when test edits are permitted.
- [ ] Available tests were run and compared against legacy evidence or recorded cases.
- [ ] The response returns only changed files, tests run, behavior equivalence evidence, validation status, and blockers.

## Prompt Body

Follow these steps in order. Preserve the legacy source unless the user explicitly requests legacy edits.

**Step 1 — Load the modernization workflow.**
Load the `code-modernization` skill before editing code. Confirm the legacy source remains read-only unless the user explicitly requests otherwise.

**Step 2 — Gather transformation inputs.**
Read `${input:target:legacy module and target stack}` plus the relevant brief, assessment, rules, map, and design artifacts.

**Step 3 — Bound the slice.**
Select one bounded legacy module or behavior slice. Reject requests that would transform the whole system in one pass.

**Step 4 — Define behavior-pinning tests.**
Load `legacy-characterization-testing` and identify behavior-pinning tests from rules, legacy evidence, recorded cases, and acceptance examples.

**Step 5 — Implement under the target tree.**
Create or update modernized code only under `modernized/**` and approved test locations. Keep implementation aligned with the target stack and design artifacts.

**Step 6 — Validate behavior.**
Run available tests and compare modernized behavior against legacy evidence or recorded cases. If tests cannot run, report the exact blocker and the command that should run.

**Step 7 — Prepare the hardening handoff.**
List changed files, behavior equivalence evidence, tests run, and blockers for `modernize-harden`.

**Step 8 — Report concisely.**
Return only changed files, tests run, behavior equivalence evidence, validation status, and blockers.

## Invocation Example

```
/modernize-transform target=legacy module and target stack
```
