---
name: open-horizons-backstage-aeg-feature
description: >-
  Operates and integrates the Open Horizons Agentic Engineering Graph (AEG) through Backstage with authenticated run management, G1/G2 decisions, traceability analytics, and golden-path harvesting. Use this skill when starting or inspecting AEG runs, reviewing gates, analyzing AEG evidence, proposing reusable profiles, or wiring the AEG feature into the Open Horizons portal.
user-invocable: true
---

# Open Horizons Backstage AEG feature

Use one portable workflow for the AEG feature while keeping repository engineering, application
runtime, identity, and approval boundaries explicit. The procedure does not pin or assume a model.

## When to invoke

- "Start an AEG modernization run for this repository."
- "Show the status and traceability gaps for AEG run run-123."
- "Present the G2 package and record my decision."
- "Find completed AEG runs that can become a golden path."
- "Integrate the AEG feature into our Open Horizons Backstage portal."

## AEG responsibility map

| Request | Primary agent | Capability |
| --- | --- | --- |
| Start a run or report status | `open-horizons-aeg-concierge` | Run classification and lifecycle status |
| Review or decide G1/G2 | `open-horizons-aeg-gatekeeper` | Human decision package and recorded outcome |
| Analyze traceability, metrics, cost, or findings | `open-horizons-aeg-analyst` | Read-only evidence analysis |
| Propose a reusable stack profile | `open-horizons-aeg-harvester` | Evidence-backed draft proposal |
| Change Backstage implementation | `open-horizons-backstage-expert` | Portal and backend engineering |
| Coordinate cross-domain repository work | `open-horizons-orchestrator` | Repository-agent delegation |

AEG is an application capability. It must not be conflated with the GitHub Copilot repository-agent
orchestrator or the seven Microsoft Agent Framework application agents.

## Procedure

1. Classify the request as `run-management`, `gate-decision`, `analysis`, `harvesting`, or
   `portal-integration` and select exactly one primary owner from the responsibility map.
2. Confirm that an authenticated MCP server named `open-horizons-aeg` exposes the required tool.
   If it is unavailable, return `blocked` with the missing server or tool; do not substitute an
   unapproved direct HTTP request or invent live state.
3. Read only the bundled reference needed for the selected operation:
   - [Lifecycle and artifacts](references/lifecycle-and-artifacts.md) for stage and evidence rules.
   - [Role workflows](references/role-workflows.md) for operation-specific inputs and output.
   - [Identity and tool contract](references/identity-and-tool-contract.md) before any tool call.
4. For a mutating operation, restate the requested effect and require the host or safety hook to
   obtain explicit human approval. A successful validation or tool call is not approval.
5. Send only domain inputs. Never supply `initiated_by`, `decided_by`, `proposed_by`, roles, or
   tenant identity as model-authored arguments; the authenticated server derives the actor.
6. Validate the response against the expected run, gate, traceability, or proposal schema. Preserve
   unknown and unavailable fields rather than estimating them.
7. Return the operation, evidence source, result, next lifecycle event, and any unresolved gate.

## Tool classification

| Tool | Class | Required handling |
| --- | --- | --- |
| `aeg_get_run` | Read-only | Cite the returned run ID and state fields. |
| `aeg_list_runs` | Read-only | Preserve server-side filtering and bounded results. |
| `aeg_get_gate_package` | Read-only | Show mandatory risk and coverage fields. |
| `aeg_get_traceability` | Read-only | Report broken or missing links explicitly. |
| `aeg_get_metrics` | Read-only | Name the source and avoid unsupported comparisons. |
| `aeg_start_run` | Mutating | Confirm intent and require explicit approval. |
| `aeg_decide_gate` | Mutating | Record only the authenticated approver's decision. |
| `aeg_propose_profile` | Mutating | Create a draft only; publication remains a reviewed PR. |

The target API shape is bundled as [the AEG OpenAPI contract](assets/openapi-aeg.json). It is a
portable integration contract, not evidence that a particular deployment is reachable.

## Identity and approval boundaries

- Backstage or the MCP server authenticates the caller and enforces authorization.
- The chat surface presents decisions; it is never the enforcement point.
- G1 and G2 may be recorded through AEG after explicit human action.
- G3 pull-request approval and G4 production promotion remain in GitHub and the deployment system.
- Tool visibility does not grant permission to invoke a mutating operation.
- Responses and diagnostics must not expose credentials, bearer material, private prompts, or raw
  provider errors.

## Limits

- Do not self-approve a gate or act for another identity.
- Do not deploy, publish a golden path, mutate production, or bypass GitHub approval controls.
- Do not treat cost figures from different billing units as directly comparable without a documented
  conversion and source.
- Use `open-horizons-portal-integration` (skill) for implementation changes after the AEG workflow
  and trust boundaries are established.

## Progressive disclosure and bundled resources

- `references/lifecycle-and-artifacts.md`: AEG stages, gates, artifacts, and evidence invariants.
- `references/role-workflows.md`: concierge, gatekeeper, analyst, and harvester workflows.
- `references/identity-and-tool-contract.md`: authentication, authorization, tool availability, and
  request/response rules.
- `assets/openapi-aeg.json`: model-neutral target API contract for an AEG adapter or Backstage action.
- `scripts/validate_aeg_contract.py`: deterministic contract safety and operation validation.
- `evals/eval_set.json`: positive and negative discovery prompts for description review.

## Output template

```markdown
## AEG operation result

**Status:** completed | blocked | approval-required
**Operation:** run-management | gate-decision | analysis | harvesting | portal-integration
**Run:** <run-id or not-applicable>

### Evidence
- <tool response field, artifact, gate package, or missing evidence>

### Result
<bounded result with no invented status, metrics, identity, or approval>

### Next event
<next artifact, gate, handoff, or blocker>
```

## Quality gate

- [ ] One AEG operation and one primary owner are explicit.
- [ ] The required authenticated MCP tool was available or the result is `blocked`.
- [ ] Actor identity came from the authenticated server, never model-authored input.
- [ ] Every mutation had explicit approval and stayed within its gate boundary.
- [ ] Status, traceability, metrics, and cost claims cite returned evidence.
- [ ] G3/G4 and publication remain outside chat mutation.
- [ ] The output follows the template and names the next event or blocker.
- [ ] `python3 scripts/validate_aeg_contract.py` passes when the contract changes.