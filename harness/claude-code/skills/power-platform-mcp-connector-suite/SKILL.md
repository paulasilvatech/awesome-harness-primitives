---
name: power-platform-mcp-connector-suite
description: >-
  Generate and validate Power Platform custom connectors that expose Model Context Protocol
  servers to Microsoft Microsoft Copilot Studio, including Swagger, apiProperties.json,
  script.csx, JSON-RPC 2.0 handling, schema compliance, OAuth hardening, certification
  preparation, and troubleshooting. Use when asked for MCP capabilities in Microsoft Copilot
  Studio, a custom connector for MCP tools/resources, or paconn/pac connector validation.
---

<!-- Generated from harness/github-copilot/skills/power-platform-mcp-connector-suite/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power Platform MCP connector suite

Generate complete Power Platform custom connector assets for MCP integration in Microsoft Copilot Studio, then validate schema, authentication, JSON-RPC handling, and deployment readiness.

## When to invoke

- "Create a Microsoft Copilot Studio custom connector for my MCP server."
- "Validate this Power Platform connector schema for MCP tools."
- "Troubleshoot why Microsoft Copilot Studio filtered my MCP tools."
- "Add MCP capabilities to an existing connector."
- "Prepare this MCP connector for Microsoft certification."

## MCP support model

| Capability | Microsoft Copilot Studio support | Implementation rule |
| --- | --- | --- |
| Tools | Supported | Expose callable functions through the MCP endpoint with user approval semantics. |
| Resources | Supported as tool outputs | Return file-like data through tools; do not model resources as separate top-level entities. |
| Prompts | Not yet supported | Do not emit prompt entities; leave the connector structure ready for future support only if requested. |

## Connector assets

| File | Required content |
| --- | --- |
| `apiDefinition.swagger.json` | Swagger 2.0, POST `/mcp`, full URI endpoints, `x-ms-agentic-protocol: mcp-streamable-1.0`, primitive-only schemas, `McpResponse`, and `McpErrorResponse`. |
| `apiProperties.json` | Connector metadata, `iconBrandColor`, authentication, policy templates for MCP request/response transformations. |
| `script.csx` | C# transformations for JSON-RPC 2.0 messages, MCP protocol compliance, error handling, token checks, and request/response shaping. |
| `readme.md` | Connector purpose, setup, examples, Microsoft Copilot Studio integration steps, validation commands, and troubleshooting. |
| `settings.json` | Product and service metadata for certification preparation when requested. |

## Schema compliance rules

| Rule | Why it matters | Fix |
| --- | --- | --- |
| No `$ref` in tool inputs or outputs | Microsoft Copilot Studio filters tools with unsupported reference types. | Inline schema shapes with primitive properties. |
| Single type values only | Type arrays such as `["string", "number"]` are rejected. | Use one of `string`, `number`, `integer`, `boolean`, `array`, or `object` and validate alternatives in `script.csx`. |
| Resources are tool outputs | Microsoft Copilot Studio supports Resources through tool calls. | Add resource payloads to the corresponding tool response. |
| Full URI endpoints | Connector import and runtime need resolvable endpoints. | Emit absolute URLs for host operations and callback references. |
| JSON-RPC 2.0 compliance | MCP calls must preserve `jsonrpc`, `id`, `method`, `params`, `result`, and `error` semantics. | Validate envelopes in `script.csx` and emit `McpErrorResponse` for failures. |
| Generative Orchestration compatibility | Agents need clear tool descriptions and predictable schemas. | Write concise descriptions and avoid polymorphic input contracts. |

## Generation modes

| Mode | Use when | Produce |
| --- | --- | --- |
| Complete New Connector | Starting from server purpose, tools, resources, and auth. | All core files plus validation guidance. |
| Schema Validation | Existing Swagger or connector fails import or tools are missing. | Finding list and patched schema recommendations. |
| Integration Troubleshooting | Runtime calls fail in Microsoft Copilot Studio. | Diagnosis across protocol header, JSON-RPC, auth, endpoint URI, and resource shape. |
| Hybrid Connector | Existing Power Platform connector needs MCP endpoint. | Minimal additive changes while preserving existing operations. |
| Certification Preparation | Connector is headed for Microsoft certification. | Metadata, icon, documentation, privacy, validation, and security checklist. |
| OAuth Security Hardening | OAuth 2.0 connector handles MCP calls. | Audience validation, state protection, HTTPS enforcement, and confused deputy prevention. |

## Inputs

Collect these context variables before generating files. Ask for missing required values or use placeholders only in a planning output, never in final connector JSON.

| Variable | Meaning |
| --- | --- |
| Connector Name | Display name for the connector. |
| Server Purpose | What the MCP server accomplishes. |
| Tools Needed | MCP tools to expose. |
| Resources | Resource payloads returned by tools. |
| Authentication | `none`, `api-key`, `oauth2`, or `basic`. |
| Host Environment | Azure Function, Express.js, or another HTTP host. |
| Target APIs | External APIs the MCP server integrates with. |

## Validation and security

| Area | Check |
| --- | --- |
| paconn | `paconn validate --api-def apiDefinition.swagger.json` passes without errors. |
| pac CLI | Connector can be created or updated with `pac connector create` or `pac connector update`. |
| Script upload | `script.csx` passes automatic validation during PAC CLI upload. |
| Package validation | `ConnectorPackageValidator.ps1` runs successfully when preparing certification. |
| OAuth 2.0 | Use standard OAuth 2.0 plus MCP audience validation to prevent passthrough attacks. |
| CSRF | Protect OAuth state parameters. |
| HTTPS | Production endpoints use HTTPS only. |
| Auth config | Authentication type, token handling, and custom security logic match the selected mode. |
| Certification | `settings.json`, PNG icon in 230x230 or 500x500, privacy policy, and documentation are complete. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Tools filtered | `$ref` or unsupported schema shape in inputs/outputs. | Inline schemas and use primitive single types. |
| Type errors | Multi-type values or polymorphic fields. | Use one type and validate alternatives in `script.csx`. |
| Resources unavailable | Resources modeled separately. | Return resources as tool outputs. |
| Connection failures | Missing or wrong `x-ms-agentic-protocol` value or non-full URI. | Set `x-ms-agentic-protocol: mcp-streamable-1.0` on POST `/mcp` and verify endpoint URLs. |
| OAuth works but wrong tenant/resource is accepted | Missing token audience validation. | Add enhanced validation in `script.csx`. |

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `McpResponse/McpErrorResponse`
- `POST /mcp`
- `REST`
- `Request/response`
- `created/updated`
- `inputs/outputs`

## Output template

```markdown
## Power Platform MCP connector — <Connector Name>

**Status:** generated | validation fixes required | blocked
**Mode:** Complete New Connector | Schema Validation | Integration Troubleshooting | Hybrid Connector | Certification Preparation | OAuth Security Hardening

### Files
| File | Status | Notes |
| --- | --- | --- |
| `apiDefinition.swagger.json` | <created/updated/planned> | <MCP endpoint and schema notes> |
| `apiProperties.json` | <created/updated/planned> | <auth and metadata notes> |
| `script.csx` | <created/updated/planned> | <JSON-RPC and security notes> |
| `readme.md` | <created/updated/planned> | <setup and examples> |

### Validation
- `paconn validate --api-def apiDefinition.swagger.json`: <pass/fail/not run>
- `pac connector create/update`: <ready/not ready>
- `ConnectorPackageValidator.ps1`: <pass/fail/not run>

### Open decisions
- <missing endpoint, auth, tool, resource, or certification decision>
```

## Quality gate

- [ ] POST `/mcp` uses `x-ms-agentic-protocol: mcp-streamable-1.0`.
- [ ] Tool input/output schemas contain no `$ref` and no multi-type arrays.
- [ ] Resources are represented as tool outputs; Prompts are not emitted as supported runtime entities.
- [ ] `McpResponse`, `McpErrorResponse`, and JSON-RPC 2.0 envelope handling are covered.
- [ ] Auth configuration includes HTTPS, state protection, and token audience validation when OAuth 2.0 is used.
- [ ] Validation commands and certification requirements are reported with pass/fail/not-run status.
