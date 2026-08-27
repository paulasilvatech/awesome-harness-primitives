---
description: Evaluate completed Open Horizons AEG runs and create one approved draft golden-path proposal.
argument-hint: "runs=<comma-separated completed run IDs>"
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/prompts/open-horizons-aeg-harvest.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /open-horizons-aeg-harvest

## Objective

Evaluate `${input:evidenceRuns}` for a repeated, traceable stack pattern and create one approved draft
proposal without publishing catalog assets.

## When to Invoke

Use when completed AEG runs may support a reusable stack profile or Backstage Software Template.

## Preconditions

- `${input:evidenceRuns}` contains at least two completed run IDs.
- Each candidate exposes closed traceability and unresolved-finding status.
- The user can explicitly approve draft creation.

If a precondition fails, return the evidence gap and stop before mutation.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Evidence run IDs | `${input:evidenceRuns}` | Yes | Require at least two distinct run IDs. |
| Selected pattern hypothesis | `${selection}` | No | Test it against evidence; do not treat it as proof. |

## What I Will Do

- Verify completion, closed traceability, and unresolved findings for every candidate.
- Identify repeated stacks, ADRs, tests, gates, and controls across at least two runs.
- Create one draft proposal only after explicit approval.

## What I Will NOT Do

- Harvest a one-off run, ignore broken traceability, or invent supporting evidence.
- Publish a golden path, edit live catalog assets, or approve the platform-team review.
- Supply model-authored proposer identity.

## Output Format

```markdown
## AEG harvest proposal

**Status:** completed | blocked | approval-required
**Evidence runs:** <run IDs>
**Draft:** <returned location or unavailable>

### Repeated pattern
- <stack, ADRs, tests, gates, and controls with evidence>

### Remaining decisions
- <platform-team review item, traceability gap, or none>
```

## Definition of Done

- [ ] At least two distinct completed runs support the pattern.
- [ ] Traceability is closed and blocking findings are resolved.
- [ ] Every proposed element cites run evidence.
- [ ] Draft creation had explicit approval and server-derived identity.
- [ ] No live catalog or template was published.
- [ ] Remaining review decisions are explicit.

## Prompt Body

1. Parse and deduplicate `${input:evidenceRuns}`; require at least two run IDs.
2. Invoke the `open-horizons-backstage-aeg-feature` skill and inspect each run and traceability view.
3. Test `${selection}` when present and identify only patterns repeated across eligible runs.
4. Show the proposed draft, obtain explicit approval, and call `aeg_propose_profile` without actor fields.
5. Return the required output with evidence, draft location, remaining decisions, or blocker.

## Invocation Example

Run **Chat: Run Prompt**, choose `/open-horizons-aeg-harvest`, and enter
`run-18,run-27,run-31`. Verify that one-off patterns are excluded and publication does not occur.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `open-horizons-backstage-aeg-feature` | `skill` | Defines harvestability, proposal mutation, identity, and publication boundaries. |
