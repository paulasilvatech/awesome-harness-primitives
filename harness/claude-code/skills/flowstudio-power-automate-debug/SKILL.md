---
name: flowstudio-power-automate-debug
description: >-
  Debug failing Power Automate cloud flow runs through FlowStudio MCP with action-level inputs,
  outputs, and root-cause evidence. Use when asked why a flow failed, to inspect failed run
  details, diagnose ActionFailed, InvalidTemplate, DynamicOperationRequestFailure, connector auth,
  timeout, expression, or HTTP errors, or fix and verify a broken cloud flow.
---

<!-- Generated from harness/github-copilot/skills/flowstudio-power-automate-debug/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# FlowStudio Power Automate debug

Diagnose a failed Power Automate cloud flow by locating the flow and run, reading the top-level failure, inspecting the root action's runtime inputs and outputs, walking backward through upstream data, applying a focused fix, and verifying with a resubmitted run.

## When to invoke

- "Debug this failed Power Automate flow run."
- "Why is this flow failing with ActionFailed?"
- "Inspect the action outputs for this run."
- "Find the root cause of an InvalidTemplate or connector error."
- "Fix this FlowStudio MCP Power Automate flow and verify it."

## Prerequisites and context

- A FlowStudio MCP subscription and reachable server are required: https://mcp.flowstudio.app. Also preserve the subscription URL without sentence punctuation: https://mcp.flowstudio.app
- Use `https://mcp.flowstudio.app/mcp`, `MCP_URL`, `MCP_TOKEN`, and a valid `YOUR_JWT_TOKEN`; never commit the token.
- Set `ENV` to the target `environment-id`, for example `Default-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- The MCP helper calls JSON-RPC `tools/call` with `x-api-key`, `application/json`, and `User-Agent: FlowStudio-MCP/1.0`.
- Surface HTTP helper failures as `RuntimeError` with the response body instead of hiding FlowStudio MCP errors.
- Call `list_skills` or `tool_search` first. Tool names and parameter schemas may change; real API responses beat this skill.

## Procedure

1. Locate the flow. Call `list_live_flows(environmentName=ENV)` and select the target by `displayName`; store the plain UUID in `FLOW_ID` and pass it as `flowName`.
2. Find the failing run. Call `get_live_flow_runs(environmentName=ENV, flowName=FLOW_ID, top=5)`, inspect newest-first entries with `name`, `status`, `startTime`, `endTime`, `triggerName`, and `error`, then store the failed `name` in `RUN_ID`.
3. Get the top-level error. Call `get_live_flow_run_error(environmentName=ENV, flowName=FLOW_ID, runName=RUN_ID)` to learn which actions failed. `failedActions` is ordered outer-to-inner; the ROOT cause is the LAST item, so set `root = err["failedActions"][-1]` and read `root["actionName"]`.
4. Inspect the failing action's runtime detail. ALWAYS call `get_live_flow_run_action_outputs` for `root_action`; never stop at `ActionFailed`, `NotSpecified`, `InternalServerError`, `InvalidTemplate`, or `BadRequest` because those are wrappers.
5. If the failing action sits inside a foreach, inspect all repetitions first, read `repetitionIndexes`, the zero-based `itemIndex`, and then pass `iterationIndex` for the suspicious item to avoid loading every repetition.
6. Read the definition with `get_live_flow`, inspect `properties.definition.actions`, and compare the action's `inputs` expression/URL/body with the runtime `outputs`.
7. Walk backward through referenced upstream actions by repeatedly calling `get_live_flow_run_action_outputs`; slice large payloads with `[:500]` before printing or reporting.
8. Apply a focused fix through `update_live_flow` only after the data path is proven. Reuse `conn_refs = defn["properties"]["connectionReferences"]`; success is `None` in `result.get("error")`.
9. Verify with `resubmit_live_flow_run(environmentName=ENV, flowName=FLOW_ID, runName=RUN_ID)` for ANY existing trigger type, wait about 30 seconds, then call `get_live_flow_runs(top=3)` and inspect `new_runs[0]["status"]`.

## Diagnostic rules

| Symptom | First tool | Then ALWAYS call | Evidence to capture |
| --- | --- | --- | --- |
| Flow shows `Failed` | `get_live_flow_run_error` | `get_live_flow_run_action_outputs` on the failing `actionName` | `outputs.statusCode`, `outputs.body`, and `error`. |
| Generic `ActionFailed` | `get_live_flow_run_error` | Action outputs for the LAST failed action | Nested action HTTP status and response body. |
| `NotSpecified` or `InternalServerError` | Action outputs | Parse nested JSON error strings into `err_detail` | Server message, stack trace, or API error JSON. |
| `InvalidTemplate` | Action outputs on the failing and prior action | Upstream action output | Null, missing, or wrong-type fields. |
| `BadRequest` | Action outputs | Inputs and outputs | Request body and rejection reason. |
| Flow never starts | `get_live_flow` | none | `properties.state` equals `Started`. |
| Action returns wrong data | `get_live_flow_run_action_outputs` | upstream action outputs | Actual output body versus expected shape. |

`get_live_flow_run_error` tells you which action failed; `get_live_flow_run_action_outputs` tells you why. This BOTH-call rule is CRITICAL.

## Root-cause patterns

| Pattern | What to inspect | Fix direction |
| --- | --- | --- |
| Expression/data issue | The action expression and its source outputs; for `split` on potentially-null data, inspect the field feeding the function. | Guard with `coalesce`, correct the path, or normalize upstream data. |
| Wrong field path | If `triggerBody()?['fieldName']` returns null, inspect the trigger output with actionName `<trigger-action-name>`. | Replace `fieldName` with the actual property path. |
| HTTP failure | Read `outputs.statusCode` and `outputs.body`, not just the wrapper code. | Fix URL, headers, body, auth, or the called service. |
| Nested JSON error | If `body["error"]` is a string, parse it before summarizing. | Report the parsed message, not the wrapper. |
| Foreach failure | Print `repetitionIndexes`, `itemIndex`, `status`, and `error` for `all_reps`; inspect `one_rep` with `iterationIndex`. | Fix the bad item or make the loop branch resilient. |
| Connection/auth failure | `ConnectionAuthorizationFailed` means the connection owner must match the service account running the flow. | Cannot fix via API; fix in Power Automate designer or recreate the connection. |
| Outlook user-picker failure | `DynamicListValuesUndefinedOrInvalid` on `GetEmailsV3` parameters `mailboxAddress`, `to`, `cc`, or `from` comes from broken `builtInOperation:AadGraph.GetUsers` listEnum metadata. | Do not retry AadGraph; use `shared_office365users.SearchUserV2` through `describe_live_connector`, `fallback`, `get_live_dynamic_options`, or `get_live_dynamic_properties`. |

Keep these diagnostic variable names meaningful in reports and snippets: `action_name` for an iterated action, `status_code` for HTTP status, `null` for missing JSON values, `null/wrong-type` for schema mismatches, `action/expression` for the definition field being investigated, and `expression/data` for fixes that change a Power Automate expression because runtime data proved it wrong. For array-processing actions, THIS is the critical evidence: inspect one representative item rather than flooding the transcript.

## Evidence and verification patterns

- Add `Compose_*_Request` before a risky connector and `Compose_*_Result` after it, with the result action allowed on `Succeeded` and `Failed`, when future debugging needs a payload snapshot. Do not include secrets or large binary payloads.
- Example HTTP evidence: wrapper `InternalServerError` tells little; action outputs may reveal HTTP 500 and `body: {"error": "Cannot read properties of undefined (reading 'toLowerCase') at getClientParamsFromConnectionString (storage.js:20)"}`.
- Example expression evidence: wrapper `BadRequest` plus `inputs: "body('HTTP_GetTokenFromStore')?['token']?['access_token']"` and empty `outputs` shows `access_token` moved from `body.token.access_token` to `body.access_token`.
- Use `trigger_live_flow` only for a `Request` HTTP trigger with a custom payload. Inspect `request_schema` from `definition.triggers` and Response action schemas first; `trigger_live_flow` handles AAD-authenticated triggers automatically.
- For testing a fix, `resubmit` / `resubmit_live_flow_run` is best because it replays the exact original trigger payload. It works for Recurrence, SharePoint "When an item is created", connector webhooks, Button triggers, and HTTP triggers. It is unavailable only for a brand-new flow that has never run.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `get_live_flow_run_error` only shows `ActionFailed` | Wrapper action failed because a nested action failed | Use the LAST item in `failedActions` and inspect that action's outputs. |
| `get_live_flow_run_action_outputs` returns multiple records | Action ran inside a foreach | Inspect `repetitionIndexes`, then call again with `iterationIndex`. |
| Output payload is huge | Array-processing action produced many items | Slice output with `[:500]` and inspect targeted fields only. |
| Fix deploys but run still fails | New run used different trigger data or old draft behavior | Resubmit `RUN_ID`, check `new_runs`, and publish draft agents before connector testing. |
| Flow state is stopped | Definition exists but scheduler will not run | Use the build skill's state guidance; check `properties.state`. |

## Progressive disclosure and bundled resources

- `references/common-errors.md`: `common-errors` mapping of Power Automate error codes, likely causes, and fixes.
- `references/debug-workflow.md`: `debug-workflow` decision tree for complex failures and step-by-step triage.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `flowstudio-power-automate-mcp` | skill | Connection setup, MCP helper, authentication, or tool discovery is missing. |
| `flowstudio-power-automate-build` | skill | The root cause requires rebuilding, creating, or deploying flow definitions. |

## Output template

```markdown
## FlowStudio debug result — <flow display name>

**Status:** fixed | root cause found | blocked
**Environment:** `<environment-id>`
**Flow ID:** `<FLOW_ID>`
**Run ID:** `<RUN_ID>`

| Step | Evidence | Result |
| --- | --- | --- |
| Flow | `list_live_flows` match | `<displayName>` |
| Run | `get_live_flow_runs` failed run | `<status>` |
| Top-level error | `get_live_flow_run_error` | `<code and failed action>` |
| Action detail | `get_live_flow_run_action_outputs` | `<real cause from inputs/outputs>` |
| Fix | `update_live_flow` or manual action | `<change>` |
| Verification | `resubmit_live_flow_run` and `get_live_flow_runs` | pass | fail | skipped |

**Root cause:** <one sentence with action name and bad data or service error>
**Next action:** <none, manual connection fix, publish agent, or follow-up build change>
```

## Quality gate

- [ ] `tool_search` or `list_skills` was called before FlowStudio MCP calls.
- [ ] The target flow and failed run were identified with `FLOW_ID` and `RUN_ID`.
- [ ] `get_live_flow_run_error` and `get_live_flow_run_action_outputs` were both called for the root action.
- [ ] The root cause is based on action-level `inputs`, `outputs`, `outputs.body`, `outputs.statusCode`, or `error`, not a wrapper code alone.
- [ ] Foreach failures used `repetitionIndexes` and `iterationIndex` when needed.
- [ ] Large payloads were sliced or summarized without leaking secrets.
- [ ] Any `update_live_flow` fix reused existing `connectionReferences` and checked `error == null`.
- [ ] Verification used `resubmit_live_flow_run` for existing runs unless a custom HTTP `trigger_live_flow` payload was required.

## References

- [FlowStudio MCP subscription](https://mcp.flowstudio.app)
- [FlowStudio MCP endpoint](https://mcp.flowstudio.app/mcp)
- [Expression error in child flow](https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/fix-expression-error.md)
- [Data entry, not a flow bug](https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/data-not-flow.md)
- [Null value crashes child flow](https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/null-child-flow.md)
