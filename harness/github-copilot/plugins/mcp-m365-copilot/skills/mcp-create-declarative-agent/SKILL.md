---
name: mcp-create-declarative-agent
description: >-
  Create a Microsoft 365 Copilot declarative agent backed by a Model Context Protocol server. Use when asked to scaffold or configure an MCP-based declarative agent, choose imported tools, configure OAuth 2.0 or SSO, set response semantics, or produce appPackage files for Microsoft 365 Agents Toolkit.
---

# MCP create declarative agent

Create a Microsoft 365 Copilot declarative agent that integrates a Model Context Protocol server, selected tools, authentication, response semantics, and deployment/testing instructions.

## When to invoke

- "Create a declarative agent for Microsoft 365 Copilot using my MCP server."
- "Configure an MCP action and imported tools for a Copilot agent."
- "Build the appPackage files for an MCP-backed declarative agent."
- "Add OAuth 2.0 or SSO authentication to my MCP declarative agent."
- "Set response semantics for MCP tool results in ai-plugin.json."

## Prerequisites and context

- Use Microsoft 365 Agents Toolkit project conventions and generated `appPackage/` files.
- The MCP server must expose server metadata, a tools listing endpoint, and tool execution endpoint.
- Test the finished agent in Microsoft 365 Copilot at `https://m365.cloud.microsoft/chat`.
- Store secrets in `.env.local` or `.env.dev`; never hard-code `OAUTH_REFERENCE_ID`, `CLIENT_ID`, or `CLIENT_SECRET` in manifests.

## Procedure

1. Scaffold a declarative agent with Microsoft 365 Agents Toolkit.
2. Add an MCP action pointing to the MCP server URL.
3. Fetch available tools from the MCP server and select only the functions the agent needs.
4. Configure authentication as OAuth 2.0 static registration or SSO.
5. Review and complete `appPackage/manifest.json`, `appPackage/declarativeAgent.json`, `appPackage/ai-plugin.json`, and `/.vscode/mcp.json`.
6. Add `.env.local` or `.env.dev` placeholders for credentials.
7. Provision, start debugging to sideload in Teams, authenticate when prompted, and test natural-language queries in Microsoft 365 Copilot.

## Project files

| File | Purpose | Required content |
| --- | --- | --- |
| `appPackage/manifest.json` | Teams app manifest with the declarative agent reference. | `$schema`, `manifestVersion`, `version`, `id`, `developer`, `name`, `description`, and `copilotAgents.declarativeAgents.file`. |
| `appPackage/declarativeAgent.json` | Agent definition. | `$schema`, `version`, `name`, `description`, `instructions`, `capabilities`, optional `WebSearch`, and MCP `file: "ai-plugin.json"`. |
| `appPackage/ai-plugin.json` | MCP plugin manifest. | `schema_version`, `name_for_human`, `description_for_human`, `description_for_model`, `contact_email`, `namespace`, `functions`, `runtimes`, and auth. |
| `/.vscode/mcp.json` | Local MCP server configuration. | `serverUrl` and `pluginFilePath`. |
| `.env.local` or `.env.dev` | Developer secrets and references. | `OAUTH_REFERENCE_ID=your-oauth-reference-id`, `CLIENT_ID=your-client-id`, `CLIENT_SECRET=your-client-secret`. |

### `appPackage/manifest.json`

```json
{"$schema":"https://developer.microsoft.com/json-schemas/teams/vDevPreview/MicrosoftTeams.schema.json","manifestVersion":"devPreview","version":"1.0.0","id":"...","developer":{"name":"...","websiteUrl":"...","privacyUrl":"...","termsOfUseUrl":"..."},"name":{"short":"Agent Name","full":"Full Agent Name"},"description":{"short":"Short description","full":"Full description"},"copilotAgents":{"declarativeAgents":[{"id":"declarativeAgent","file":"declarativeAgent.json"}]}}
```

### `appPackage/declarativeAgent.json`

```json
{"$schema":"https://aka.ms/json-schemas/copilot/declarative-agent/v1.0/schema.json","version":"v1.0","name":"Agent Name","description":"Agent description","instructions":"You are an assistant that helps with [specific domain]. Use the available tools to [capabilities].","capabilities":[{"name":"WebSearch","websites":[{"url":"https://learn.microsoft.com"}]},{"name":"MCP","file":"ai-plugin.json"}]}
```

### `appPackage/ai-plugin.json`

```json
{"schema_version":"v2.1","name_for_human":"Service Name","description_for_human":"Description for users","description_for_model":"Description for AI model","contact_email":"support@company.com","namespace":"serviceName","capabilities":{"conversation_starters":[{"text":"Example query 1"}]},"functions":[{"name":"functionName","description":"Function description","capabilities":{"response_semantics":{"data_path":"$","properties":{"title":"$.title","subtitle":"$.description"}}}}],"runtimes":[{"type":"MCP","spec":{"url":"https://{api-host}/mcp/"},"run_for_functions":["functionName"],"auth":{"type":"OAuthPluginVault","reference_id":"${{OAUTH_REFERENCE_ID}}"}}]}
```

### `/.vscode/mcp.json`

```json
{"serverUrl":"https://{api-host}/mcp/","pluginFilePath":"appPackage/ai-plugin.json"}
```


## Legacy source mapping

If converting an older prompt-shaped artifact, remove prompt frontmatter and invalid tool tokens such as `changes`, `search/codebase`, `edit/editFiles`, and `problems`; keep only the skill instructions. Preserve MCP terminology including `model-context-protocol`, `api-plugin`, `security/simplicity`, `auto-generated`, and user-facing capability boundaries such as `can/cannot`.

| Original label | Rebuilt file |
| --- | --- |
| `appPackage/manifest.json**` | `appPackage/manifest.json` |
| `appPackage/declarativeAgent.json**` | `appPackage/declarativeAgent.json` |
| `appPackage/ai-plugin.json**` | `appPackage/ai-plugin.json` |
| `vscode/mcp.json**` | `/.vscode/mcp.json` |
| `mcp-create-adaptive-cards` | Adjacent primitive to use when the user explicitly asks for Adaptive Cards. |

## Authentication and response semantics

| Need | Configuration |
| --- | --- |
| OAuth 2.0 static registration | Use `"type": "OAuthPluginVault"`, `"reference_id": "${{OAUTH_REFERENCE_ID}}"`, `"authorization_url": "https://{auth-host}/authorize"`, `"client_id": "${{CLIENT_ID}}"`, `"client_secret": "${{CLIENT_SECRET}}"`, and minimal `"scope": "read write"`. |
| Single Sign-On | Use `"auth": { "type": "SSO" }` when the server supports SSO. |
| Response mapping | Use `response_semantics` with `data_path`, `properties.title`, `properties.subtitle`, and optional `properties.url`; for lists use `"data_path": "$.results"`, `"title": "$.name"`, `"subtitle": "$.description"`, `"url": "$.link"`. |
| Adaptive Cards | Add visual cards only when the user asks; keep this skill focused on MCP, manifests, auth, and response semantics. |

## Tool and server examples

| Server | URL | Tools | Auth |
| --- | --- | --- | --- |
| GitHub MCP Server | `https://api.githubcopilot.com/mcp/` | `search_repositories`, `search_users`, `get_repository` | OAuth 2.0 |
| Jira MCP Server | `https://your-domain.atlassian.net/mcp/` | `search_issues`, `create_issue`, `update_issue` | OAuth 2.0 |
| Custom Service | `https://{api-host}/mcp/` | Custom tools exposed by your service | OAuth 2.0 or SSO |

## Design rules

| Area | Rule |
| --- | --- |
| Tool design | Keep functions focused, use clear descriptions, import only needed tools, and prefer action-oriented function names. |
| Security | Use OAuth 2.0 for production, store secrets in environment variables, validate inputs on the MCP server side, limit scopes, and use reference IDs for OAuth registration. |
| Instructions | Be specific about purpose, capabilities, success behavior, error behavior, and when tools should be used. |
| Performance | Cache responses where appropriate, batch operations where possible, set timeouts for long-running operations, and paginate large datasets. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| MCP server not responding | Bad URL, connectivity issue, or missing endpoint. | Verify server URL, network access, server metadata, tools listing, and tool execution endpoints. |
| Authentication fails | OAuth credentials, reference ID, or scopes are wrong. | Verify credentials, check reference ID matches registration, confirm scopes, and test OAuth flow independently. |
| Tools not appearing | `mcp.json` or `ai-plugin.json` does not match selected tools. | Ensure `mcp.json` points to the server, verify function definitions, and re-fetch actions from MCP if the server changed. |
| Agent not understanding queries | Instructions, function descriptions, or `response_semantics` are too vague. | Review `declarativeAgent.json`, make function descriptions specific, verify data extraction, and test with more specific queries. |

## Output template

```markdown
## MCP declarative agent package

**Agent:** <agent name>
**MCP server:** <server MCP URL>
**Authentication:** OAuth 2.0 | SSO | none for local test only

### Files created or updated
| File | Status | Notes |
| --- | --- | --- |
| `appPackage/manifest.json` | created / updated | <schema and Copilot agent reference> |
| `appPackage/declarativeAgent.json` | created / updated | <instructions and capabilities> |
| `appPackage/ai-plugin.json` | created / updated | <functions, runtimes, auth, response_semantics> |
| `/.vscode/mcp.json` | created / updated | <serverUrl and pluginFilePath> |
| `.env.local` or `.env.dev` | created / updated | <required placeholders only> |

### Imported tools
- `<functionName>`: <description and response mapping>

### Validation
- Provisioning: pass | not run | blocked
- Local debug/sideload: pass | not run | blocked
- Microsoft 365 Copilot test at `https://m365.cloud.microsoft/chat`: pass | not run | blocked
```

## Quality gate

- [ ] The generated structure includes `appPackage/manifest.json`, `appPackage/declarativeAgent.json`, `appPackage/ai-plugin.json`, and `/.vscode/mcp.json`.
- [ ] `manifest.json` references `declarativeAgent.json` through `copilotAgents.declarativeAgents`.
- [ ] `declarativeAgent.json` references `ai-plugin.json` through an MCP capability.
- [ ] `ai-plugin.json` includes only selected tools and maps each runtime with `run_for_functions`.
- [ ] OAuth values use `OAUTH_REFERENCE_ID`, `CLIENT_ID`, and `CLIENT_SECRET` placeholders from `.env.local` or `.env.dev`.
- [ ] Response semantics use concrete JSON paths and do not assume fields that are absent from the tool response.
- [ ] Testing instructions include provisioning, Teams sideload/debug, authentication, and Microsoft 365 Copilot validation.

## References

- [Microsoft Teams manifest schema](https://developer.microsoft.com/json-schemas/teams/vDevPreview/MicrosoftTeams.schema.json)
- [Declarative agent schema](https://aka.ms/json-schemas/copilot/declarative-agent/v1.0/schema.json)
- [Microsoft 365 Copilot chat](https://m365.cloud.microsoft/chat)
