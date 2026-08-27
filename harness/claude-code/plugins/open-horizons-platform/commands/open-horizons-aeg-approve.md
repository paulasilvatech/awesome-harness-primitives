---
description: Present an Open Horizons AEG G1 or G2 package and record one authenticated human decision.
argument-hint: "run-id=<ID> gate=<G1|G2>"
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/prompts/open-horizons-aeg-approve.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /open-horizons-aeg-approve

## Objective

Present the complete `${input:gate}` package for `${input:runId}`, collect an explicit human decision,
and record it through the authenticated AEG service.

## When to Invoke

Use when an authorized reviewer needs to approve or reject AEG gate G1 or G2.

## Preconditions

- `${input:runId}` identifies one run and `${input:gate}` is exactly G1 or G2.
- The authenticated AEG service returns the full decision package.
- The human reviewer can explicitly approve the mutation.

If a precondition fails, report it and stop before recording a decision.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Run ID | `${input:runId}` | Yes | Use exactly this run. |
| Gate | `${input:gate}` | Yes | Accept only G1 or G2. |
| Decision and feedback | Chat response after package review | Yes | Accept `approve` or `reject`; rejection requires actionable feedback. |

## What I Will Do

- Retrieve and present every mandatory package field and material risk.
- Ask for one explicit `approve` or `reject` decision.
- Record the approved mutation without model-authored actor fields.

## What I Will NOT Do

- Self-approve, decide for another person, or soften rejection feedback.
- Hide risks, omit required package fields, or reinterpret ambiguous wording as approval.
- Record G3 pull-request or G4 production decisions.

## Output Format

```markdown
## AEG gate decision

**Status:** completed | blocked | approval-required
**Run:** <run-id>
**Gate:** G1 | G2
**Decision:** approve | reject | pending

### Package and risks
- <mandatory evidence and material risks>

### Effect
<next stage, rejection back-edge, authorization denial, or blocker>
```

## Definition of Done

- [ ] The run and gate are explicit and limited to G1 or G2.
- [ ] Mandatory package fields and risks are visible before the decision.
- [ ] Rejection has actionable feedback preserved verbatim.
- [ ] The decision had explicit approval and server-derived actor identity.
- [ ] The recorded effect cites the AEG response.
- [ ] G3 and G4 remain outside the chat decision path.

## Prompt Body

1. Validate `${input:runId}` and `${input:gate}`; reject any gate other than G1 or G2.
2. Invoke the `open-horizons-backstage-aeg-feature` skill and retrieve the complete package.
3. Present mandatory evidence and risks, then ask for `approve` or `reject` and required feedback.
4. Restate the exact mutation, obtain explicit approval, and call `aeg_decide_gate` without actor fields.
5. Return the required output with the recorded effect, denial, or blocker.

## Invocation Example

Run **Chat: Run Prompt**, choose `/open-horizons-aeg-approve`, enter `run-42` and `G2`, review the
package, then provide one explicit decision. Verify that no decision is recorded before confirmation.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `open-horizons-backstage-aeg-feature` | `skill` | Defines package contents, identity, approval, and gate boundaries. |
