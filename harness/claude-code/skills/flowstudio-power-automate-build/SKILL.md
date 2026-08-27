---
name: flowstudio-power-automate-build
description: >-
  Build, scaffold, update, deploy, verify, and test Power Automate cloud flows through FlowStudio
  MCP. Use when asked to create a flow, build a flow definition, scaffold a workflow, deploy or
  PATCH an existing flow, wire connector connectionReferences, add actions, update
  triggers/actions, or generate Power Automate JSON without using the portal.
---

<!-- Generated from harness/github-copilot/skills/flowstudio-power-automate-build/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# FlowStudio Power Automate build

Build or update a Power Automate cloud flow by discovering the live FlowStudio MCP tool schema, resolving authenticated connections, constructing the workflow definition JSON, deploying it with `update_live_flow`, and verifying the resulting flow before any side-effecting test.

## When to invoke

- "Create a Power Automate flow with FlowStudio MCP."
- "Build a new flow definition and deploy it."
- "Patch this existing cloud flow's actions."
- "Wire SharePoint, Outlook, Teams, or Approvals connections into a flow JSON."
- "Generate a workflow definition from scratch."

## Prerequisites and context

- A FlowStudio MCP subscription and reachable server are required: https://mcp.flowstudio.app. Also preserve the subscription URL without sentence punctuation: https://mcp.flowstudio.app
- Use the MCP endpoint `https://mcp.flowstudio.app/mcp` with a valid JWT in `MCP_TOKEN`; never commit `YOUR_JWT_TOKEN`.
- Set `ENV` to the target `environment-id`, for example `Default-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- Discover the live MCP schema first with `list_skills` or `tool_search`; tool names and parameters may change, and the API response wins over this skill.
- The Python helper shape is JSON-RPC `tools/call` with `x-api-key: MCP_TOKEN`, `Content-Type: application/json`, and `User-Agent: FlowStudio-MCP/1.0`; define `MCP_URL`, `MCP_TOKEN`, and call `mcp(tool, **kwargs)`.

## Procedure

1. Load current tools. Query `tool_search` with `skill:create-flow` for brand-new flows or `skill:build-flow` for existing edits; if needed, query `select:get_live_dynamic_properties`. The create bundle includes `list_live_environments`, `list_live_connections`, `describe_live_connector`, `get_live_dynamic_options`, and `update_live_flow`.
2. Look before building. Call `list_live_flows(environmentName=ENV, mode="owner", search="<display name>", top=20)`, inspect the returned `{ "flows": [...] }`, and set `FLOW_ID` to the plain UUID from the match. For large environments, pass `continuationUrl` with the same `mode`; use `mode="admin"` only when the MCP identity has admin rights.
3. Resolve connections. Call `list_live_connections(environmentName=ENV)` before asking the user for anything. Keep only `statuses[0].status == "Connected"`, build `conn_map = {connectorName: id}`, and use `search="shared_sharepointonline"` or another connector API name for paste-ready `connectionReferenceTemplate` and `hostTemplate` values.
4. Build `connection_references` and `host_templates`. `connectionReferences[connector].connectionName` holds the GUID from `list_live_connections`; each action's `inputs.host.connectionName` or `host.connectionName` uses the map key such as `shared_teams`. If a connection is missing, `STOP` and ask the user to create it through OAuth, then re-run `list_live_connections`.
5. Construct the workflow definition with `$schema: "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#"`, `contentVersion: "1.0.0.0"`, `triggers`, `actions`, and optional `definition["description"]`.
6. Deploy with `update_live_flow`. Omit `flowName` to create; provide `flowName=FLOW_ID` to PATCH an existing flow. Pass `definition`, `connectionReferences=connection_references`, and `displayName`. `update_live_flow` always returns `result["error"]`; success is `null` / Python `None`, so test `result.get("error") is not None`.
7. Verify with `get_live_flow(environmentName=ENV, flowName=FLOW_ID)`. Confirm `properties.state` is `Started`, inspect `properties.definition.actions`, and use `set_live_flow_state(state: "Started")` instead of `update_live_flow` when state is stopped.
8. Test only after explicit user confirmation because flows can send email, post Teams messages, write SharePoint items, start approvals, or call external APIs. Prefer `resubmit_live_flow_run` for existing flows; use `trigger_live_flow` only for HTTP custom payloads or a brand-new temporary HTTP twin.

## Flow definition and connector rules

| Subject | Rule |
| --- | --- |
| Schema | Keep `$schema` at `schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json`; model `triggers/actions` as normal Logic Apps workflow JSON. |
| No connectors | Recurrence + Compose + HTTP-only flows may omit `connectionReferences`. |
| Common connector API names | SharePoint `shared_sharepointonline`, Outlook `shared_office365`, Teams `shared_teams`, Approvals `shared_approvals`, OneDrive `shared_onedriveforbusiness`, Excel `shared_excelonlinebusiness`, Dataverse `shared_commondataserviceforapps`, Forms `shared_microsoftforms`. |
| Connector-backed operations | Use `describe_live_connector(environmentName=ENV, search="send email", top=5)` or specify `connectorName` and `operationId`; do not hand-write shapes when the server can return hints, variants, inputs/outputs, and examples. |
| Variants | Request authored variants such as `variant="flowbot_chat"`; store returned examples in variables like `teams_chat`. |
| Dynamic options | Use `get_live_dynamic_options` with `connectionName=conn_map[connector]`, `operationId`, `parameterName`, and `dynamicMetadata` for dropdown IDs such as SharePoint sites/lists and Teams teams/channels. |
| Dynamic properties | Use `get_live_dynamic_properties` for schema/field shapes such as SharePoint list item columns; pass `parameters={"dataset": "<site-url>", "table": "<list-id>"}` and metadata from `sp_op`. |
| Reference copying | For existing flows, copy `properties.connectionReferences` from `get_live_flow` when the connectors match. |
| Description | Put text in `definition["description"]`; the server appends `#flowstudio-mcp` for tracking. Do not pass top-level `description` unless `tool_search` shows it. |
| Operation metadata | Preserve existing `metadata.operationMetadataId`; add stable GUIDs for new connector actions to keep Designer/run-only UI consistent. |

Connector discovery examples that must remain available: `search` `SendEmailV2` on `shared_office365`; inspect SharePoint `GetItems`; set `sp_conns` from `list_live_connections(search="shared_sharepointonline")`; keep a `connectors_needed` list; build fallback IDs as `/providers/Microsoft.PowerApps/apis/<connector>` so `Microsoft.PowerApps` and `PowerApps` connector paths are explicit. If `urllib` raises an HTTP error, surface a `RuntimeError` with the response body.

## Deployment and testing patterns

| Scenario | Use | Notes |
| --- | --- | --- |
| Create | `update_live_flow` without `flowName` | Capture `FLOW_ID = result["created"]`. |
| Update | `update_live_flow` with `flowName=FLOW_ID` | PATCH the existing flow. |
| Verify state | `get_live_flow` then `set_live_flow_state` | Do not use `update_live_flow` for state changes. |
| Existing flow, ANY trigger type | `get_live_flow_runs(top=1)` then `resubmit_live_flow_run` | Works for Recurrence, SharePoint, connector-triggered, Button/Skills, and HTTP. |
| HTTP flow with different payload | `trigger_live_flow(body={...})` | Inspect the Request trigger schema before calling. |
| Brand-new non-HTTP flow | Temporarily set `production_trigger = definition["triggers"]`, replace with a `Request` HTTP trigger, test with `trigger_live_flow.body`, then restore `production_trigger`. |
| Failed test run | `get_live_flow_runs` then `get_live_flow_run_error` | Read the root failed action before editing. |
| Copilot/Skills solution discovery | `add_live_flow_to_solution(solutionId=...)` | Copilot Studio may not discover a flow as an agent tool unless it is in the target solution. |

## Gotchas

| Mistake | Consequence | Prevention |
| --- | --- | --- |
| Missing `connectionReferences` | 400 `missing from connectionReferences` or "Supply connectionReferences" | Always call `list_live_connections`; use the `connectionReferences` key, not a raw GUID, in `host.connectionName`. |
| `ConnectionAuthorizationFailed` or 403 | Connection belongs to another user or another `x-api-key` principal | Re-run connection discovery and select an authorized active connection. |
| `ConnectionNotConfigured` | GUID is invalid or expired | Re-check `list_live_connections`. |
| `InvalidTemplate` or `InvalidDefinition` | Syntax, `runAfter`, expression, or action type error | Validate JSON and action spellings before redeploying. |
| Missing `"operationOptions"` on Foreach | Parallel writes and races | Set `"operationOptions": "Sequential"` and preserve the literal `"Sequential"`. |
| `union(old_data, new_data)` | First-wins semantics keep stale values | Use `union(new_data, old_data)`. |
| `split()` on a potentially-null string | Runtime `InvalidTemplate` | Wrap with `coalesce(field, '')`. |
| Teams `PostMessageToConversation` recipient as `{"to": "user@contoso.com"}` | 400 `GraphUserDetailNotFound` | For Chat with Flow bot, set `body/recipient` to plain `"user@contoso.com;"`; for Channel, use `{"groupId": "...", "channelId": "..."}` with `groupId` and `channelId`. |
| Placeholder Excel `scriptId` | Dynamic validation fails at save time | Resolve the real Office Script ID before deploying. |
| SharePoint `PatchItem` omits required fields | Save can fail even when not changing those fields | Echo unchanged required fields such as `item/Title`. |
| Button/Skills trigger used for MCP testing | MCP cannot directly fire the production trigger | Test the same actions through a temporary HTTP twin, then swap back before testing/resubmitting. |
| Copilot Studio connector calls a draft agent | Invocation can fail or use stale behavior | Publish the agent before testing or resubmitting. |

Preserve these exact compatibility notes when editing: the API's `connectionName` field is overloaded; connector-backed actions need live metadata; do not use hand-written JSON when a live descriptor exists; `union()` is first-wins; `location` controls Teams recipient shape; `state: "Started"` is a state-tool concern; `solutionId` is required for solution adds; expressions such as `triggerBody()` and `triggerOutputs()` need representative test payloads; testing/resubmitting flows is side-effecting; the old docs used the emphatic words `MANDATORY`, `MUST`, `EVERY`, and `ONLY` for side-effecting or connection rules; success means `error != null` is false, written as `!= null` in diagnostics.

## Progressive disclosure and bundled resources

Read bundled references only when the current flow needs that pattern; they provide step-by-step (`by-step`) templates without loading every catalog upfront.

- `references/flow-schema.md`: full `flow-schema` JSON structure.
- `references/trigger-types.md`: `trigger-types` and trigger templates.
- `references/action-patterns-core.md`: `action-patterns-core`, variables, control flow, expressions, and `ACTION-PATTERNS` core examples.
- `references/action-patterns-data.md`: `action-patterns-data`, arrays, HTTP, parsing, and ready-to-use data actions.
- `references/action-patterns-connectors.md`: `action-patterns-connectors`, SharePoint, Outlook, Teams, and Approvals copy-paste connector patterns.
- `references/build-patterns.md`: `build-patterns` complete definitions such as Recurrence + SharePoint + Teams and HTTP examples.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `flowstudio-power-automate-mcp` | skill | The FlowStudio MCP connection, authentication, or tool discovery setup is missing. |
| `flowstudio-power-automate-debug` | skill | A deployed flow fails and you need action-level diagnostics. |

## Output template

```markdown
## FlowStudio build result — <flow display name>

**Status:** created | updated | verified | blocked
**Environment:** `<environment-id>`
**Flow ID:** `<FLOW_ID or none>`

| Step | Evidence | Result |
| --- | --- | --- |
| Tool schema | `tool_search` query and bundle loaded | pass | 
| Existing flow check | `list_live_flows` mode/search/top or `continuationUrl` | found | not found |
| Connections | `list_live_connections` connector keys | pass | missing `<connector>` |
| Definition | `$schema`, trigger names, action names | pass | fail |
| Deployment | `update_live_flow` result where `error` is `null` | pass | fail |
| Verification | `get_live_flow` state and action list | pass | fail |
| Test | `resubmit_live_flow_run` or `trigger_live_flow` after confirmation | pass | skipped | blocked |

**Next action:** <manual OAuth connection, solution add, publish agent, or none>
```

## Quality gate

- [ ] `tool_search` or `list_skills` was called before using FlowStudio MCP tools.
- [ ] Existing flows were searched before creation to avoid duplicates.
- [ ] `connectionReferences` came from live `list_live_connections`, not user-provided GUIDs.
- [ ] Every connector action's `host.connectionName` points to a key in `connectionReferences`.
- [ ] Connector operations and dynamic values were discovered with `describe_live_connector`, `get_live_dynamic_options`, or `get_live_dynamic_properties` when applicable.
- [ ] `update_live_flow` success was checked by verifying `error == null`, not by checking whether the `error` key exists.
- [ ] Deployment was verified with `get_live_flow`, and stopped flows used `set_live_flow_state`.
- [ ] No side-effecting `trigger_live_flow` or `resubmit_live_flow_run` call was made without explicit user confirmation.
- [ ] Every referenced bundled resource exists and was used only on demand.

## References

- [FlowStudio MCP subscription](https://mcp.flowstudio.app)
- [FlowStudio MCP endpoint](https://mcp.flowstudio.app/mcp)
- [Logic Apps workflow definition schema](https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#)
