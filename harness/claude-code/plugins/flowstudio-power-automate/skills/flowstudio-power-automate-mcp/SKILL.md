---
name: flowstudio-power-automate-mcp
description: >-
  Foundation skill for Power Automate through the FlowStudio MCP server: authentication, JSON-RPC
  helper code, tool discovery with list_skills and tool_search, oversized response parsing, and
  workflow-skill routing. Use this skill when connecting an agent to Power Automate, setting up
  FlowStudio MCP, checking auth, discovering flow tools, or preparing build, debug, monitoring, or
  governance workflows.
---

<!-- Generated from harness/github-copilot/plugins/flowstudio-power-automate/skills/flowstudio-power-automate-mcp/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power Automate via FlowStudio MCP foundation

Connect an agent to the FlowStudio Power Automate MCP server, verify authentication, discover current tool schemas, choose the right workflow skill, and handle large MCP responses without flooding context.

## When to invoke

- "Connect GitHub Copilot to FlowStudio MCP for Power Automate."
- "Set up the MCP helper for Power Automate flows."
- "List the FlowStudio MCP tools and skill bundles."
- "My FlowStudio MCP auth is failing with 401 or 403."
- "How should I handle a huge get_live_flow or connector response?"

## Prerequisites and context

- Requires a FlowStudio MCP subscription or compatible Power Automate MCP server: https://mcp.flowstudio.app.
- MCP endpoint: `https://mcp.flowstudio.app/mcp`.
- API key / JWT token: send the plain token in the `x-api-key` header, not `Authorization: Bearer`.
- Token placeholder in examples: `<YOUR_JWT_TOKEN>`; keep `_TOKEN` semantics intact when adapting scripts.
- Power Platform environment name, usually `Default-<tenant-guid>`, found through `list_live_environments` or a `list_live_flows` response.
- Use a timeout of at least `120` seconds for large calls such as `get_live_flow_run_action_outputs`.

## Workflow skill routing

Pick by user intent, not by individual tool names. The same underlying MCP tools appear in multiple workflows.

| User intent | Skill to load |
| --- | --- |
| Make or change a flow, build a new flow, modify an existing flow, fix a bug, deploy | `flowstudio-power-automate-build` |
| Diagnose why a flow failed, perform root cause analysis on a failing run | `flowstudio-power-automate-debug` |
| See tenant-wide flow health, failure rates, asset inventory | `flowstudio-power-automate-monitoring` (Pro+) |
| Tag, audit, classify, score, or offboard flows | `flowstudio-power-automate-governance` (Pro+) |
| Connect, set up auth, write a helper, parse responses | this foundation skill |

`flowstudio-power-automate-build` and `flowstudio-power-automate-debug` can both call `update_live_flow`, `get_live_flow`, and run-error tools; build works forward from desired behavior, while debug works backward from a failed run. `flowstudio-power-automate-monitoring` and `flowstudio-power-automate-governance` both call Store tools; monitoring reads health, while governance writes metadata.

## Source of truth

| Priority | Source | Rule |
| --- | --- | --- |
| 1 | Real API response | Trust what the server actually returns. |
| 2 | `tool_search` / `list_skills` | Use for authoritative tool schemas, parameter names, types, and required flags. |
| 3 | SKILL docs and reference files | Use for workflow narrative, response shapes, and non-obvious behavior. |

If docs disagree with a live response, the API wins. Before invoking a tool you have not used recently, call `tool_search` to confirm the current schema.

## Tool discovery

FlowStudio MCP v1.1.5+ exposes non-billable meta-tools that avoid loading all 30+ schemas.

| Meta-tool query | Use when |
| --- | --- |
| `list_skills` | Cold start; list bundles such as `build-flow`, `create-flow`, `debug-flow`, `monitor-flow`, `discover`, and `governance`. |
| `tool_search` with `query: "skill:<name>"` | Load the full schema set for one bundle, such as `skill:debug-flow`. |
| `tool_search` with `query: "select:tool1,tool2"` | Load specific tools by name when chaining across bundles. |
| `tool_search` with free text | Search ambiguous intents such as `cancel run`. |

Current common bundles:

| Bundle | Use when |
| --- | --- |
| `create-flow` | Creating a brand-new flow; includes environment/connection discovery, connector description, dynamic options, and `update_live_flow`. |
| `build-flow` | Reading or modifying an existing flow definition. |
| `debug-flow` | Investigating failed runs and action-level inputs/outputs. |
| `monitor-flow` | Starting, stopping, triggering, cancelling, or resubmitting runs. |
| `discover` | Enumerating environments, flows, and connections. |
| `governance` | Pro+ cached-store tagging, maker audit, and metadata updates. |

```python
skills = mcp("list_skills", {})
debug_tools = mcp("tool_search", {"query": "skill:debug-flow"})
selected = mcp("tool_search", {"query": "select:get_live_flow,update_live_flow"})
```

## MCP helper patterns

Use Python with `urllib.request` when you want a dependency-free helper. Use Node.js 18+ when the repository is JavaScript or TypeScript and native `fetch`, `JSON.stringify`, and `JSON.parse` fit the stack. Avoid PowerShell for flow operations because `ConvertTo-Json -Depth` silently truncates nested definitions. Use cURL or Bash only for tiny smoke tests; nested JSON escaping is fragile.

### Python helper

```python
import json, urllib.request

TOKEN = "<YOUR_JWT_TOKEN>"
MCP = "https://mcp.flowstudio.app/mcp"

def mcp(tool, args, cid=1):
    payload = {"jsonrpc": "2.0", "method": "tools/call", "id": cid,
               "params": {"name": tool, "arguments": args}}
    req = urllib.request.Request(MCP, data=json.dumps(payload).encode(),
        headers={"x-api-key": TOKEN, "Content-Type": "application/json",
                 "User-Agent": "FlowStudio-MCP/1.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MCP HTTP {e.code}: {body[:200]}") from e
    raw = json.loads(resp.read())
    if "error" in raw:
        raise RuntimeError(f"MCP error: {json.dumps(raw['error'])}")
    text = raw["result"]["content"][0]["text"]
    return json.loads(text)
```

### Node.js helper

```js
const TOKEN = "<YOUR_JWT_TOKEN>";
const MCP = "https://mcp.flowstudio.app/mcp";

async function mcp(tool, args, cid = 1) {
  const payload = {
    jsonrpc: "2.0",
    method: "tools/call",
    id: cid,
    params: { name: tool, arguments: args },
  };
  const res = await fetch(MCP, {
    method: "POST",
    headers: {
      "x-api-key": TOKEN,
      "Content-Type": "application/json",
      "User-Agent": "FlowStudio-MCP/1.0",
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`MCP HTTP ${res.status}: ${body.slice(0, 200)}`);
  }
  const raw = await res.json();
  if (raw.error) throw new Error(`MCP error: ${JSON.stringify(raw.error)}`);
  return JSON.parse(raw.result.content[0].text);
}
```

For older Node.js, replace `fetch` with `https.request` from the standard library or install `node-fetch`.

## Connection verification and errors

```python
skills = mcp("list_skills", {})
print(f"Connected — {len(skills)} skill bundles available:",
      [s["name"] for s in skills])
```

Expected output:

```text
Connected — 6 skill bundles available: ['build-flow', 'create-flow', 'debug-flow', 'monitor-flow', 'discover', 'governance']
```

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| HTTP `401` or `403` | Token missing, expired, malformed, or prefixed incorrectly. | Get a fresh JWT from https://mcp.flowstudio.app and send it as `x-api-key`. |
| HTTP `400` | Malformed JSON-RPC payload. | Check `Content-Type: application/json`, `jsonrpc: "2.0"`, `method: "tools/call"`, and `params.name` / `params.arguments`. |
| `MCP error: {"code": -32602, ...}` | Wrong or missing tool arguments. | Call `tool_search` with `query: "select:<toolname>"` and use the returned schema. |
| Helper works but workflow tool is unavailable | Bundle not loaded or subscription tier missing. | Run `list_skills`, then `tool_search` for the relevant bundle; verify Pro+ for monitoring or governance. |

## Oversized responses

Some responses can overflow the agent context window.

| Tool | Typical size | Cause |
| --- | --- | --- |
| `describe_live_connector` | 100-600 KB | Full Swagger spec for a connector. |
| `get_live_dynamic_properties` | 50-500 KB | Dynamic connector field schemas such as SharePoint list columns. |
| `get_live_flow_run_action_outputs` without `actionName` | 50 KB-several MB | Top-level action outputs; foreach actions may return every repetition. |
| `get_live_flow` for large flows | 50-500 KB | Deeply nested branches. |
| `list_live_flows` in large tenants | 50-200 KB | Hundreds of flow records. |

When a harness spills output to a file such as `tool-results/mcp-flowstudio-describe_live_connector-NNNN.txt`, parse the double-wrapped payload before filtering:

```python
import json
with open(path) as f:
    raw = json.loads(f.read())
payload = json.loads(raw[0]["text"])
```

```powershell
$payload = ((Get-Content $path -Raw | ConvertFrom-Json)[0].text) | ConvertFrom-Json
```

Rules of thumb:

1. Extract one `operationId`, one action's outputs, or the specific fields needed; do not echo whole connector Swagger documents.
2. Always pass `actionName` to `get_live_flow_run_action_outputs`; add `iterationIndex` for foreach actions when you need one repetition.
3. Reuse a spill file within a session instead of refetching the same connector swagger.
4. Do not grep spill files directly for JSON keys such as `"OperationId":`; strings are JSON-escaped as `\"OperationId\":`. Parse first, then filter.
5. Summarize `name + state + trigger` for flow lists and `actionName + status + code` for run errors unless the user asks for raw JSON.

```python
conn = mcp("describe_live_connector", {"environmentName": ENV, "connectorName": "shared_sharepointonline"})
op = conn["properties"]["swagger"]["paths"]["/datasets/{dataset}/tables/{table}/items"]["get"]
print(op["operationId"], "—", op.get("summary"))
```

## Progressive disclosure and bundled resources

Read bundled references only when the current task needs them.

- `references/MCP-BOOTSTRAP.md`: endpoint, auth, JSON-RPC request/response format; read first for setup.
- `references/tool-reference.md`: response shapes and behavioral notes; use `tool_search` for current parameters.
- `references/action-types.md`: Power Automate action type patterns.
- `references/connection-references.md`: connector reference guide.


## FlowStudio vocabulary and aliases

Keep these operational phrases recognizable when discussing FlowStudio MCP: `oversized-response`, `use-case`, `most-likely-needed`, `request-response`, `built-in`, `async/await`, `JavaScript/TypeScript`, `pip install`, `smoke-test`, `error-prone`, `top-level`, `inputs/outputs`, `Starting/stopping`, `tools/list`, `query: "<keywords>"`, `"cancel run"`, `select:<toolname>`, `401/403`, `x-api-key: <JWT>`, `get_live_flow_runs`, and `get_live_flow_run_error`.

## Output template

```markdown
## FlowStudio MCP foundation result

**Status:** connected | needs auth | blocked
**Endpoint:** `https://mcp.flowstudio.app/mcp`
**Environment:** `<Default-tenant-guid or unknown>`

### Discovery
- `list_skills`: <bundle count> bundles found
- `tool_search`: `<query>` → <tool count> schemas loaded

### Helper
- Language: Python | Node.js
- Auth header: `x-api-key`
- Timeout: `<seconds>`

### Next workflow
- Skill: `<flowstudio-power-automate-build|flowstudio-power-automate-debug|flowstudio-power-automate-monitoring|flowstudio-power-automate-governance>`
- Reason: <user intent matched>
```

## Quality gate

- [ ] The MCP endpoint is `https://mcp.flowstudio.app/mcp`.
- [ ] The token is sent as `x-api-key`, not `Authorization: Bearer`.
- [ ] `list_skills` or `tool_search` was used before relying on a workflow tool schema.
- [ ] The helper uses JSON-RPC `tools/call` with `params.name` and `params.arguments`.
- [ ] Large outputs are parsed, filtered, and summarized instead of echoed wholesale.
- [ ] Workflow routing is based on user intent and notes Pro+ requirements for monitoring or governance.

## References

- FlowStudio MCP: https://mcp.flowstudio.app
- FlowStudio MCP endpoint: https://mcp.flowstudio.app/mcp
- FlowStudio MCP subscription page: https://mcp.flowstudio.app.
- Expression error in child flow: https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/fix-expression-error.md
- Data entry, not a flow bug: https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/data-not-flow.md
- Null value crashes child flow: https://github.com/ninihen1/power-automate-mcp-skills/blob/main/examples/null-child-flow.md
