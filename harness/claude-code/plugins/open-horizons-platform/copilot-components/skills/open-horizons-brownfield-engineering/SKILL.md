---
name: open-horizons-brownfield-engineering
description: >-
  Implements focused changes in an existing repository through evidence-driven diagnosis,
  minimal edits, immediate checks, and proportionate regression validation. Use when handling
  bug fixes, features, improvements, refactoring, modernization, tests, and documentation updates.
---

# Open Horizons Brownfield Engineering

Evolve an existing codebase without discarding its working contracts, local conventions, or
unrelated user changes.

## When to invoke

- "Fix this failing behavior in the existing project."
- "Add a feature to this service or application."
- "Improve, refactor, or modernize this implementation."
- "Add tests or documentation for an existing capability."

## Prerequisites and context

- Start from a file, symbol, failure, command, test, or nearest owning implementation.
- Read applicable repository instructions before changing matched files.
- Treat the dirty worktree as user-owned unless a change is known to come from this task.
- Identify specialist boundaries before editing infrastructure, security, deployment, or provider
  configuration.

## Procedure

1. Classify the intent as `bugfix`, `feature`, `improvement`, `modernization`, `testing`, or
   `documentation`; record acceptance criteria and protected behavior.
2. Inspect the smallest local path that directly computes, mutates, or controls the behavior.
3. State one falsifiable hypothesis and one cheap check that can disprove it.
4. Make the smallest grounded edit. Do not widen scope before running the focused check.
5. Run the focused behavior test, unit test, compile, lint, or typecheck immediately.
6. If the check exposes a local defect consistent with the hypothesis, repair that slice and rerun
   the same check. If it falsifies the hypothesis, move one ownership boundary closer to the real
   control point before editing again.
7. Add or update tests according to blast radius and preserve existing public APIs unless the task
   explicitly changes them.
8. Run final focused validation plus any repository gate required by the changed artifact type.
9. Report changed paths, actual checks, unrun checks, residual risk, and specialist handoffs.

## Output template

Return exactly this structure:

```markdown
## Brownfield engineering result

**Status:** completed | blocked
**Intent:** bugfix | feature | improvement | modernization | testing | documentation
**Summary:** <implemented behavior and rationale>

### Changes
- <path and behavior changed>

### Validation
- `<command or test>`: PASS | FAIL | NOT RUN - <evidence>

### Residual risk
- <risk, handoff, or none>
```

## Limits

- Do not replace an existing subsystem merely because greenfield code would be easier.
- Do not perform deployment, publication, destructive operations, live RBAC changes, or state
  mutation; use the relevant specialist and approval workflow.
- Do not fix unrelated defects encountered during validation, but report them when material.

## Gotchas

- A nearby registration or wrapper may not own behavior; step to the direct computation before
  editing.
- Generated files and lockfiles should change only when the owning tool or dependency operation
  requires them.
- Broad validation can hide the first useful failure; start narrow and expand after the local check
  passes.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-engineer` | `agent` | A general repository implementation owner should run this skill. |
| `open-horizons-orchestration` | `skill` | Multiple domains or agents require coordinated ownership. |
| `test-coverage` | `skill` | Coverage or quality-gate analysis is the primary task. |
| `pipeline-diagnostics` | `skill` | CI infrastructure or workflow failure owns the defect. |

## Quality gate

- [ ] Intent and acceptance criteria are explicit.
- [ ] The edit is grounded in an owning code path and falsifiable hypothesis.
- [ ] A focused executable check ran immediately after the first substantive edit.
- [ ] Tests scale with the blast radius and preserve unrelated behavior.
- [ ] Unrelated user changes remain intact.
- [ ] Final validation evidence and unrun checks are reported honestly.