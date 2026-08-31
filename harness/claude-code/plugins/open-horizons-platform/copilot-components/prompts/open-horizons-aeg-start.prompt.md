---
name: "open-horizons-aeg-start"
description: "Classify an engineering need and start one approved Open Horizons AEG run."
argument-hint: "need=<outcome and constraints>"
agent: "open-horizons-aeg-concierge"
---

# /open-horizons-aeg-start

## Objective

Classify `${input:need}` as an AEG run, collect only missing required inputs, and return the approved
run result in Chat without modifying workspace files.

## When to Invoke

Use when a user wants to start a greenfield, modernization, change, or system AEG run.

## Preconditions

- `${input:need}` identifies an outcome or problem to solve.
- The authenticated `open-horizons-aeg` MCP server is available.
- The user can explicitly approve run creation.

If a precondition is missing, report it in Chat and stop before mutation.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Engineering need | `${input:need}` | Yes | Use as the run objective; ask for it and stop if absent. |
| Selected context | `${selection}` | No | Treat an empty selection as absent and never infer hidden repository facts. |

## What I Will Do

- Classify the intent and ask at most three questions for required missing context.
- Default the worker engine to `inherit` and show the exact proposed mutation.
- Start one run only after explicit approval and report returned evidence.

## What I Will NOT Do

- Supply actor identity, roles, or tenant claims as model-authored inputs.
- Decide gates, modify files, deploy, or infer live AEG state.
- Claim run creation when the authenticated tool was unavailable or failed.

## Output Format

```markdown
## AEG run start

**Status:** completed | blocked | approval-required
**Intent:** greenfield | modernization | change | system
**Run:** <run-id or unavailable>

### Evidence
- <returned fields or missing capability>

### Next event
<first artifact, gate, or blocker>
```

## Definition of Done

- [ ] The intent and required inputs are explicit.
- [ ] The worker engine defaults to `inherit` unless policy overrides it.
- [ ] Run creation had explicit approval.
- [ ] Actor identity came from the authenticated service.
- [ ] The result stays in Chat and no workspace file changed.
- [ ] Returned status and next event cite tool evidence.

## Prompt Body

1. Validate `${input:need}` and use `${selection}` only when it contains relevant evidence.
2. Invoke the `open-horizons-backstage-aeg-feature` skill and classify the run intent.
3. Ask at most three questions for required missing fields, then show the proposed run inputs.
4. Obtain explicit approval and call `aeg_start_run` once without actor fields.
5. Return the required output with the run ID, links, first artifact, next gate, or exact blocker.

## Invocation Example

Run **Chat: Run Prompt**, choose `/open-horizons-aeg-start`, and enter
`Create a managed claims application for the operations team with Azure as the approved cloud`.
Verify that the proposed mutation is shown before the tool call and no workspace file changes.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `open-horizons-backstage-aeg-feature` | `skill` | Owns classification, identity, lifecycle, and output procedure. |