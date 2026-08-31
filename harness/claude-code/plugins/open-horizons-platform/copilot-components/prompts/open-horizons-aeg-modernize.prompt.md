---
name: "open-horizons-aeg-modernize"
description: "Start an approved Open Horizons AEG modernization run for an existing repository."
argument-hint: "repository=<URL> outcome=<target state>"
agent: "open-horizons-aeg-concierge"
---

# /open-horizons-aeg-modernize

## Objective

Prepare and start one AEG modernization run for `${input:repositoryAndOutcome}` and return the result
in Chat without modifying the source repository.

## When to Invoke

Use when an existing repository needs a read-only AS-IS assessment followed by governed modernization.

## Preconditions

- `${input:repositoryAndOutcome}` includes a source repository and target outcome.
- The authenticated `open-horizons-aeg` MCP server is available.
- The user can explicitly approve run creation.

If a precondition is missing, identify it in Chat and stop before mutation.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Repository and outcome | `${input:repositoryAndOutcome}` | Yes | Require both values; do not invent either. |
| Selected constraints | `${selection}` | No | Use only explicit constraints present in the selection. |

## What I Will Do

- Fix the run intent to `modernization` and confirm source and target.
- Describe the read-only AS-IS assessment and first lifecycle artifacts.
- Start one approved run with worker engine `inherit` unless policy says otherwise.

## What I Will NOT Do

- Change the source repository, select a target architecture, or skip the AS-IS assessment.
- Supply model-authored actor identity or promise delivery dates.
- Treat run creation as approval of requirements, architecture, pull requests, or production.

## Output Format

```markdown
## AEG modernization start

**Status:** completed | blocked | approval-required
**Source:** <repository>
**Outcome:** <target outcome>
**Run:** <run-id or unavailable>

### First evidence
- <AS-IS assessment and next artifact>

### Next event
<expected artifact, gate, or blocker>
```

## Definition of Done

- [ ] Source repository and target outcome are explicit.
- [ ] Intent is `modernization` and the AS-IS assessment is read-only.
- [ ] Worker engine defaults to `inherit` unless approved policy overrides it.
- [ ] Run creation had explicit approval and server-derived identity.
- [ ] No source file or external deployment was changed.
- [ ] The response names the first evidence and next event.

## Prompt Body

1. Parse `${input:repositoryAndOutcome}` and use `${selection}` only for explicit constraints.
2. Invoke the `open-horizons-backstage-aeg-feature` skill and confirm intent `modernization`.
3. Explain the AS-IS assessment, `CONSTITUTION.md`, FRD/NFRD, ADR, tasks, and traceability sequence.
4. Show the exact run request, obtain explicit approval, and call `aeg_start_run` without actor fields.
5. Return the required output with evidence or the exact missing precondition or tool.

## Invocation Example

Run **Chat: Run Prompt**, choose `/open-horizons-aeg-modernize`, and enter
`repository=https://github.com/example/legacy-orders outcome=containerized service on the approved platform`.
Verify that no repository change occurs and the run is created only after approval.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `open-horizons-backstage-aeg-feature` | `skill` | Owns modernization inputs, lifecycle, and security boundaries. |