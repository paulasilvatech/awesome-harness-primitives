---
name: foundry-hosted-agent-copilotkit
description: >-
  Guide ongoing development of CopilotKit frontends connected over AG-UI to Microsoft Agent Framework agents and Azure AI Foundry hosted agents. Use when adding or gating tools, wiring human-in-the-loop approval, building generative UI, synchronizing shared state, debugging AG-UI event streams, upgrading preview packages, or deploying hosted agent updates.
---

# CopilotKit and Azure AI Foundry hosted agents

Work inside an existing React or Next.js CopilotKit app that talks AG-UI to a Microsoft Agent Framework agent running locally, in-process, or as an Azure AI Foundry hosted agent; identify the wiring first, then change tools, approvals, UI, state, dependencies, or deployment loops without assuming hosted agents speak AG-UI natively.

## When to invoke

- "Wire human-in-the-loop approval onto this existing agent tool."
- "Debug why my CopilotKit AG-UI stream is not rendering tool calls."
- "Add a Microsoft Agent Framework tool and show it in generative UI."
- "Upgrade CopilotKit, AG-UI, or Agent Framework packages safely."
- "Deploy an Azure AI Foundry hosted agent update and verify approvals."

## Prerequisites and context

- The application must be an `EXISTING` `React/Next.js` application; do not scaffold a new app with the CopilotKit CLI or `azd ai agent init` from this skill.
- Azure AI Foundry hosted agents are a paid Azure service; live verification can incur costs.
- Every layer is pre-1.0 or preview. Verify current API names against installed packages and live documentation before changing code.
- Preferred docs sources: Microsoft Docs for Microsoft Agent Framework and Azure AI Foundry (`/agent-framework/integrations/ag-ui/`, `/azure/foundry/`, `agent-framework/integrations/ag-ui/`, `azure/foundry/`), CopilotKit docs for hooks and runtime, AG-UI docs for event semantics. Inspect installed `@copilotkit/*` declarations when docs and local package versions differ.

## Architecture decision

A deployed Foundry hosted agent endpoint does not speak `ag-ui` by default. The original architecture question is `WHERE` AG-UI is produced; answer that before changing code. It exposes no `read-only` AG-UI facade by default. A deployed Foundry hosted agent endpoint does not speak AG-UI by default. It exposes an OpenAI Responses endpoint such as `.../protocols/openai/responses` and/or a raw `.../protocols/invocations` endpoint. AG-UI must be produced by the app, by the hosted agent container, or by a bridge.

| Wiring | Evidence in code | AG-UI producer | Consequence |
| --- | --- | --- | --- |
| Architecture A: in-process AG-UI endpoint | Python `add_agent_framework_fastapi_endpoint(...)` or .NET `MapAGUI(...)` wraps the agent. | The app service hosting the Microsoft Agent Framework agent. | Native AG-UI interaction patterns are available closest to the agent. |
| Architecture B: hosted container serves AG-UI | `agent.yaml` declares `protocol: invocations` and the container exposes an AG-UI route. | The deployed hosted-agent container. | Local and deployed behavior can match, but deployment versioning matters. |
| Runtime route | `agents: { <name>: new HttpAgent({ url }) }` in TypeScript config connects CopilotKit Runtime to the AG-UI endpoint. | Keep the runtime URL and agent name aligned before testing hooks. |
| Architecture C: translation bridge | Code references `previous_response_id`, `mcp_approval_response`, a Foundry `conversation` object, or `/responses`. | A separate bridge translates Responses protocol to AG-UI. | Human-in-the-loop and state patterns require explicit synthesis work. |

The frontend agent name must align across the runtime `agents` config, the `agent` prop on `<CopilotKit>`, and the hosted agent name in `agent.yaml`.

## Procedure

1. Identify the architecture by inspecting the AG-UI endpoint, hosted agent manifest, and frontend runtime configuration.
2. Verify current API names in live docs and installed declarations. Current CopilotKit hook names include `useFrontendTool`, `useHumanInTheLoop`, `useRenderToolCall`, and `useCoAgent`; `useCopilotAction` is legacy.
3. Load the matching bundled reference before editing: architecture, patterns, HITL, troubleshooting, upgrading, or deploy loop.
4. Make the smallest stack-consistent change, keeping frontend names, tool names, schemas, and hosted agent deployment names aligned.
5. Verify at the lowest failing layer first, then through the real UI, and finally against the deployed endpoint when deployment changed.

## Tool and UI patterns

| Task | Backend rule | Frontend rule | Verification |
| --- | --- | --- | --- |
| Add or modify a tool | Define `@tool` in Python or `AIFunctionFactory.Create` in .NET with typed, described parameters. | Add `useRenderToolCall` when the tool needs custom UI. | Trigger through chat and confirm `TOOL_CALL_*` events plus final message snapshot. |
| Gate a side-effecting tool | Use `approval_mode="always_require"` or `ApprovalRequiredAIFunction`. | Register approval UI with `useHumanInTheLoop`. | Test approve, reject, and a follow-up turn in the same thread. |
| Build generative UI | Return compact model-consumable data, not rich formatting. | Render rich content in `useRenderToolCall` or the CopilotKit render map. | Confirm rendering while streaming and after stream end. |
| Share agent state | Prefer native AG-UI state patterns in Architecture A/B. | Use `useCoAgent` only when the backend emits compatible state events. | Check state after reload and after follow-up turns. |
| Debug stream failures | `curl -N` the AG-UI endpoint with a minimal `RunAgentInput` body. | Inspect browser console and network after backend stream is proven good. | Compare raw SSE events with rendered UI state. |

Keep tool docstrings grounding-safe: do not include concrete example values for model-derived fields because models often copy literal examples. Use placeholders and validate inside the tool.

## Progressive disclosure and bundled resources

Read bundled references on demand; each file is self-contained.

| Resource | Use when |
| --- | --- |
| `references/architecture.md` | Choosing Architecture A/B/C, local-vs-deployed behavior, or bridge responsibilities. |
| `references/patterns.md` | Implementing frontend tools, backend rendering, HITL, generative UI, shared state, or predictive state. |
| `references/hitl.md` | Adding or debugging approvals, especially the duplicate-execution and `re-execution` hazard. |
| `references/troubleshooting.md` | Matching exact symptoms to root causes and fixes across layers. |
| `references/upgrading.md` | Bumping CopilotKit, AG-UI, Microsoft Agent Framework, or hosting protocol packages. |
| `references/deploy-loop.md` | Running `azd ai agent run`, deploying with `azd deploy`, and verifying deployed agent versions. |

## Gotchas

- **Hosted Foundry endpoint is not AG-UI by default**: do not point CopilotKit directly at `/responses` and expect AG-UI events.
- **One successful chat reply is not proof**: approvals, final snapshots, and follow-up turns often fail after a basic response works.
- **Do not bump one preview package alone**: runtime, AG-UI client, agent-framework line, hosting protocol, and manifest version must stay compatible.
- **Restart local hosted agents between stateful verification passes**: `azd ai agent run` can retain stale in-memory state.
- **Approval rejection must prevent server-side execution**: a UI cancel button is insufficient if the tool already ran.


- Preserve `JSON` payload shape when parameters are renamed or `re-typed`; any workaround removal must be `re-validated` against the tracked upstream issue.

## Output template

```markdown
## CopilotKit hosted-agent result

**Status:** complete | needs verification | blocked
**Architecture:** A in-process AG-UI | B hosted AG-UI | C Responses bridge | unknown
**Changed area:** tools | HITL | generative UI | shared state | debugging | upgrade | deploy

### Evidence
- `<file/config/endpoint>`: <what was verified>
- `<event or command>`: <observed result>

### Validation
- UI read/query path: pass | fail | not run
- Approval approve path: pass | fail | not applicable
- Approval reject path: pass | fail | not applicable
- Follow-up turn after approval: pass | fail | not applicable
- Deployed endpoint verification: pass | fail | not applicable
```

## Quality gate

- [ ] The architecture is identified before code changes.
- [ ] The frontend agent name, runtime `agents` key, and `agent.yaml` hosted agent name are consistent.
- [ ] Live docs or installed declarations were checked for preview API names.
- [ ] `approval-gated` side-effecting tools require approval and were tested for approve and reject.
- [ ] A follow-up turn after approval did not silently re-execute the gated tool.
- [ ] Tool rendering works at stream end, not only during streaming.
- [ ] Deployed changes were verified against the deployed endpoint, not only locally.
