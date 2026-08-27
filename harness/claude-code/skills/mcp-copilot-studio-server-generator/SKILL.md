---
name: mcp-copilot-studio-server-generator
description: >-
  Generate a complete MCP server and Power Platform custom connector optimized for Microsoft
  Copilot Studio, including streamable HTTP, JSON-RPC 2.0, schema constraints,
  apiDefinition.swagger.json, apiProperties.json, script.csx, tools, resources-as-tool-outputs,
  deployment, and validation. Use when asked for a Power Platform MCP connector generator or
  Copilot Studio MCP integration.
---

<!-- Generated from harness/github-copilot/skills/mcp-copilot-studio-server-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Power Platform MCP connector generator

Generate a Microsoft Copilot Studio-compatible MCP implementation by combining a streamable HTTP MCP server with Power Platform custom connector files and schemas that avoid constructs Copilot Studio filters or misinterprets.

## When to invoke

- "Generate a Power Platform MCP connector."
- "Create an MCP server for Copilot Studio."
- "Build a custom connector with `x-ms-agentic-protocol`."
- "Scaffold `apiDefinition.swagger.json`, `apiProperties.json`, and `script.csx` for MCP."
- "Make my MCP tools compatible with Microsoft Copilot Studio."

## Inputs

Use `$ARGUMENTS` as the server purpose, target API, or tool list when provided. If details are missing, collect them before generating files.

| Context variable | Required | Examples |
| --- | --- | --- |
| Server Purpose | Yes | Customer data management and analysis. |
| Tools Needed | Yes | `searchCustomers`, `getCustomerDetails`, `analyzeCustomerTrends`. |
| Resources | Conditional | Customer profiles, analysis reports; expose as tool outputs. |
| Authentication | Yes | `none`, `api-key`, `oauth2`. |
| Host Environment | Yes | Azure Function, Express.js, FastAPI. |
| Target APIs | Conditional | CRM System REST API or another external API. |

## Copilot Studio MCP pattern

| Requirement | Implementation rule |
| --- | --- |
| Agentic protocol | Add `x-ms-agentic-protocol: mcp-streamable-1.0` to the connector definition. |
| Transport | Provide a streamable HTTP endpoint at POST `/mcp`. |
| Wire protocol | Support JSON-RPC 2.0 request and response messages. |
| Connector shape | Follow Power Platform connector structure with `apiDefinition.swagger.json`, `apiProperties.json`, and optional `script.csx`. |
| Tool descriptions | Write clear tool descriptions for Copilot Studio and Generative Orchestration. |

## Schema compliance requirements

| Constraint | Why | Rule |
| --- | --- | --- |
| No reference types | Copilot Studio filters reference types in tool inputs/outputs. | Inline schemas; do not rely on `$ref` for tool payloads. |
| Single type values only | Arrays of multiple types are not reliably interpreted. | Use one `type` per schema field. |
| Avoid enum inputs | Copilot Studio may treat enum as plain string. | Use `string` plus validation and description. |
| Primitive-compatible fields | Tool schemas must remain callable by the agent. | Use `string`, `number`, `integer`, `boolean`, `array`, and `object`. |
| Full URI endpoints | Relative or partial endpoints can break connector execution. | Return full URIs from endpoints and tools. |
| Resources | Copilot Studio can use resources only when surfaced through tools. | Include resources as structured tool outputs. |
| Prompts | Prompts are not yet supported in Copilot Studio. | Generate prompt code only as server-side MCP capability, not as a Copilot Studio dependency. |

## Generated file structure

```text
/apiDefinition.swagger.json  (Power Platform connector schema)
/apiProperties.json         (Connector metadata and configuration)
/script.csx                 (Custom code transformations and logic)
/server/                    (MCP server implementation)
/tools/                     (Individual MCP tools)
/resources/                 (MCP resource handlers)
```

| File or folder | Must contain |
| --- | --- |
| `apiDefinition.swagger.json` | POST `/mcp`, `x-ms-agentic-protocol: mcp-streamable-1.0`, compliant inline schema definitions, `McpResponse`, `McpErrorResponse`, and the paired `McpResponse/McpErrorResponse` contract. |
| `apiProperties.json` | Connector metadata, branding, authentication configuration, and policy templates if needed. |
| `script.csx` | C# transformations, JSON-RPC message handling glue, validation, processing, error handling, and logging. |
| `server/` | JSON-RPC 2.0 request/response handler, tool registration and execution, resource management, compatibility checks. |
| `tools/` | Individual tool implementations accepting primitive inputs/outputs and returning structured outputs. |
| `resources/` | MCP resource handlers whose content is surfaced through tool outputs when used by Copilot Studio. |

## MCP component rules

| Component | Copilot Studio support | Generation rule |
| --- | --- | --- |
| Tools | Supported in Copilot Studio. | Generate every requested business operation as a tool with primitive input schema and structured output. |
| Resources | Supported only when accessible through tools. | Return file-like data outputs from tools; do not rely on separate resource browsing. |
| Prompts | Not yet supported in Copilot Studio. | Include predefined templates only for MCP clients that support prompts; label the limitation. |

## Validation checklist

- [ ] No reference types in schemas.
- [ ] All `type` fields are single types.
- [ ] Enum handling uses `string` with validation.
- [ ] Resources are available through tool outputs.
- [ ] Endpoints return full URIs.
- [ ] JSON-RPC 2.0 compliance is implemented.
- [ ] `x-ms-agentic-protocol: mcp-streamable-1.0` is present.
- [ ] `McpResponse` and `McpErrorResponse` schemas are defined.
- [ ] Tool descriptions are clear for Copilot Studio.
- [ ] Generative Orchestration compatibility is checked.

## Example input

```yaml
Server Purpose: Customer data management and analysis
Tools Needed:
  - searchCustomers
  - getCustomerDetails
  - analyzeCustomerTrends
Resources:
  - Customer profiles
  - Analysis reports
Authentication: oauth2
Host Environment: Azure Function
Target APIs: CRM System REST API
```

## Gotchas

- **Do not use `$ref` for tool payloads**: Copilot Studio can filter reference types and make the tool unusable.
- **Do not model enum inputs as OpenAPI enums**: write `string` with validation and a description of accepted values.
- **Do not expose resources only through MCP resource APIs**: return them through tool outputs for Copilot Studio.
- **Do not promise prompt support in Copilot Studio**: prompts may exist in the MCP server but are not yet a Copilot Studio integration surface.

## Output template

```markdown
## Copilot Studio MCP connector

**Status:** generated | requirements needed | blocked
**Server purpose:** <purpose>
**Host environment:** Azure Function | Express.js | FastAPI | other
**Authentication:** none | api-key | oauth2

### Files
| Path | Purpose |
| --- | --- |
| `apiDefinition.swagger.json` | Connector schema with POST `/mcp` and `x-ms-agentic-protocol: mcp-streamable-1.0` |
| `apiProperties.json` | Connector metadata and authentication |
| `script.csx` | Custom transformations and JSON-RPC handling |
| `server/` | MCP server implementation |
| `tools/` | Individual MCP tools |
| `resources/` | Resource handlers exposed through tool outputs |

### Tools
| Tool | Inputs | Output | Copilot Studio notes |
| --- | --- | --- | --- |
| `searchCustomers` | primitive schema | structured object | no `$ref`, no enum inputs |

### Validation
- No reference types: pass | fail
- Single type fields: pass | fail
- JSON-RPC 2.0: pass | fail
- `McpResponse` / `McpErrorResponse`: pass | fail
```

## Quality gate

- [ ] Server Purpose, Tools Needed, Resources, Authentication, Host Environment, and Target APIs are known or explicitly marked not applicable.
- [ ] `apiDefinition.swagger.json`, `apiProperties.json`, `script.csx`, `server/`, `tools/`, and `resources/` are generated when requested.
- [ ] POST `/mcp` uses streamable HTTP and JSON-RPC 2.0.
- [ ] `x-ms-agentic-protocol: mcp-streamable-1.0` appears in the connector definition.
- [ ] Tool input/output schemas avoid reference types, multi-type values, and enum inputs.
- [ ] `McpResponse` and `McpErrorResponse` are present.
- [ ] Resources are surfaced as tool outputs and prompts are labeled as not yet supported in Copilot Studio.
- [ ] All endpoints return full URIs and tool descriptions are clear for Generative Orchestration.
