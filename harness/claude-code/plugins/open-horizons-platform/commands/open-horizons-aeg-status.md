---
description: Report evidence-based status and the next lifecycle event for one Open Horizons AEG run.
argument-hint: "run-id=<AEG run ID>"
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/prompts/open-horizons-aeg-status.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /open-horizons-aeg-status

## Objective

Retrieve `${input:runId}` and return its current AEG state, pending gate, latest transition, finding
back-edge, and next event in Chat.

## When to Invoke

Use when a user asks where an AEG run is, what blocks it, or which artifact or gate comes next.

## Preconditions

- `${input:runId}` is present and unambiguous.
- The authenticated `open-horizons-aeg` MCP server exposes `aeg_get_run`.

If either precondition fails, report the missing input or capability and stop.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Run ID | `${input:runId}` | Yes | Query exactly this run; do not substitute another run. |
| Selected context | `${selection}` | No | Use only to frame the question, never as live-state evidence. |

## What I Will Do

- Retrieve one run through the authenticated read-only tool.
- Cite the returned state, transition, gate, finding, and artifact fields.
- Return a compact status with the next expected event.

## What I Will NOT Do

- Start, approve, reject, cancel, edit, deploy, or publish anything.
- Infer live state from repository files or selected text.
- Hide missing fields or report an unavailable run as complete.

## Output Format

```markdown
## AEG run status

**Status:** completed | blocked
**Run:** <run-id>
**State:** <returned state or unavailable>

### Evidence
- Last transition: <value>
- Pending gate: <value or none>
- Finding back-edge: <value or none>

### Next event
<artifact, gate, transition, or blocker>
```

## Definition of Done

- [ ] Exactly one requested run was queried.
- [ ] Every status field cites the authenticated response.
- [ ] Missing fields are explicit rather than inferred.
- [ ] The next event names an artifact, gate, transition, or blocker.
- [ ] No mutation or workspace edit occurred.
- [ ] The result stays in Chat.

## Prompt Body

1. Validate `${input:runId}` and ignore selected context as a source of live state.
2. Invoke the `open-horizons-backstage-aeg-feature` skill and select run-management status mode.
3. Call `aeg_get_run` once for the exact run ID.
4. Extract the current state, last transition, pending gate, latest finding back-edge, and next event.
5. Return the required output or `blocked` with the unavailable tool or response field.

## Invocation Example

Run **Chat: Run Prompt**, choose `/open-horizons-aeg-status`, and enter `run-42`.
Verify that the response cites returned fields and performs no mutation.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `open-horizons-backstage-aeg-feature` | `skill` | Defines status evidence and lifecycle vocabulary. |
