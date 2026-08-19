---
name: mcp-ecosystem
description: 'Use when querying the local MCP Ecosystem reference server for live upstream documentation, methodology, templates, Backstage resources, GitHub Copilot customization, Microsoft Learn, Azure CAF/WAF, VS Code docs, GitHub docs, Anthropic docs, or SDD/spec-kit guidance. Produces sourced reference lookups, tool selection, server health checks, and AI Chat wiring guidance. DO NOT USE FOR: general web search, live cloud or repository operations, infra MCP servers such as Azure/GitHub/Terraform/Kubernetes/Helm, or non-reference queries. Triggers include "search Microsoft Learn through MCP", "use the ecosystem server", "ground this in Backstage docs", and "list MCP ecosystem tools".'
---

# MCP Ecosystem

Use this skill to operate the Open Horizons local MCP Ecosystem reference server implemented in `mcp-servers/src/tools/`. The server exposes 79 documentation tools across 17 modules and helps agents ground SDD, Backstage, GitHub, Microsoft Learn, Azure CAF/WAF, VS Code, and Anthropic answers in upstream sources.

> [!NOTE]
> This skill depends on the MCP Ecosystem server at `http://localhost:3100/mcp`, Node.js, Docker when using `mcp-servers/` local compose workflows, optional `GH_TOKEN` for higher GitHub API limits, and `.github/mcp.json` registration. It does not perform live cloud mutations.

## When to invoke

- "Search Microsoft Learn through the MCP Ecosystem server."
- "Ground this Backstage template answer in official docs."
- "List the tools exposed by mcp-ecosystem."
- "Check whether AI Chat can call the ecosystem tools."
- "Use spec-kit methodology from the local MCP server."

## Prerequisites and context

- `mcp-servers/src/tools/` exists and contains the registered tool modules.
- `.github/mcp.json` includes `mcp-ecosystem` with URL `http://localhost:3100/mcp`.
- For local runtime, `mcp-servers/README.md`, `mcp-servers/USAGE.md`, and `mcp-servers/ARCHITECTURE.md` exist.
- Optional `GH_TOKEN` is configured when GitHub-backed documentation tools need higher rate limits.
- The query is a reference/documentation task, not a cloud operation.

## Procedure

### Step 1: Confirm this is a reference lookup

Use this server for documentation and methodology. Do not use it for Azure, GitHub, Terraform, Kubernetes, or Helm operations that need live state.

### Step 2: Verify server registration and health

```bash
test -f .github/mcp.json
test -d mcp-servers/src/tools
curl -s http://localhost:3100/health
```

If the server is not running locally, use the repo's documented workflow.

```bash
cd mcp-servers
make up
make health
```

### Step 3: Select the narrowest tool family

| Need | Tool family |
| --- | --- |
| SDD and spec-kit | `speckit_*` |
| Backstage docs, catalog, templates, plugins, UI | `backstagedocs_*`, `backstageplugins_*`, `backstageui_*` |
| Microsoft Learn, CAF, WAF | `mslearn_*`, `caf_*`, `waf_*` |
| GitHub docs and Copilot customization | `ghdocs_*`, `copilotdocs_*` |
| VS Code docs | `vscode_*` |
| Anthropic and Claude docs | `anthropicdocs_*`, `anthropics_*` |

### Step 4: Call list or search before fetching a page

List all tools with JSON-RPC over HTTP.

```bash
curl -s http://localhost:3100/mcp   -H 'Content-Type: application/json'   -H 'Accept: application/json, text/event-stream'   -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Call a specific tool only after selecting the narrowest match.

```bash
curl -s http://localhost:3100/mcp   -H 'Content-Type: application/json'   -H 'Accept: application/json, text/event-stream'   -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"speckit_get_phases","arguments":{}}}'
```

### Step 5: Classify reference confidence

| Confidence | Meaning |
| --- | --- |
| High | Fetched directly from an official upstream source through a targeted ecosystem tool. |
| Medium | Search result snippet from an official source that needs a follow-up fetch. |
| Low | Server unavailable, stale cache, or query answered without ecosystem grounding. |

### Step 6: Wire AI Chat only with existing anchors

Use the existing client at `backstage/server/agent-api/tools/mcp_ecosystem.py`. In-cluster runtime uses the `mcp-ecosystem` service described in `mcp-servers/ARCHITECTURE.md`.

## Limits

- Do not use this skill for: general web search, live cloud or repository operations, infra MCP servers such as Azure/GitHub/Terraform/Kubernetes/Helm, or non-reference queries.
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Server health check fails | Start with `cd mcp-servers && make up`, then rerun `make health`. |
| Tool is not found | Call `tools/list` and select an available tool; do not invent tool names. |
| GitHub rate limit is hit | Set `GH_TOKEN` and retry after cache or rate-limit recovery. |
| Cache may be stale | Report cache staleness and fetch the specific page again when possible. |
| Query needs live infrastructure state | Stop and route to the appropriate CLI skill instead. |

## Output template

Return exactly this structure:

```markdown
## MCP Ecosystem Lookup Report

**Query:** <query>
**Server:** `http://localhost:3100/mcp`
**Tools used:** <tool names>
**Confidence:** <High|Medium|Low>

### Sources
- <source URL or tool result reference>

### Answer
<grounded answer>

### Gaps
- <missing source or follow-up>
```

## Quality gate

- [ ] Confirmed the task is reference lookup, not live operations.
- [ ] Verified `.github/mcp.json` and `mcp-servers/src/tools/` anchors.
- [ ] Used `tools/list` when the exact tool was unclear.
- [ ] Cited official upstream sources returned by the tool.
- [ ] Reported cache or server availability limitations.
- [ ] Kept counts aligned with source: 17 modules and 79 tools.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
