---
paths:
  - "**/*.{json,csx,md}"
---

<!-- Generated from harness/github-copilot/instructions/power-platform-mcp-development.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Power Platform MCP custom connector conventions for JSON-RPC, Copilot Studio schema constraints, authentication, scripts, Swagger, resources, errors, testing, and certification. Use when developing MCP connectors for Microsoft Copilot Studio.

# Power Platform MCP Connector Conventions — Copilot Studio Integration

These instructions apply to JSON, custom script, and Markdown files that define Power Platform custom connectors with Model Context Protocol integration for Microsoft Copilot Studio. They are authoritative for JSON-RPC 2.0, `x-ms-agentic-protocol: mcp-streamable-1.0`, schema flattening, authentication, `script.csx`, Swagger 2.0, resource transformation, connection parameters, errors, testing, and certification documentation in matched files; tenant security and connector certification policy win where they define stricter requirements.

## MCP Protocol and Copilot Studio Compatibility

- Implement JSON-RPC 2.0 for MCP communication.
- Use the `x-ms-agentic-protocol: mcp-streamable-1.0` header for Copilot Studio compatibility.
- Structure endpoints to support both standard REST operations and MCP tool invocation.
- Transform responses to comply with Copilot Studio constraints: no reference types and single types only.
- Design for standard MCP server compatibility, including common methods such as `tools/list`, `tools/call`, and `resources/list`.
- Handle streaming responses appropriately for the `mcp-streamable-1.0` protocol.
- Implement protocol negotiation and capability detection where connector behavior depends on server capabilities.

## Schema, Swagger, and Resource Design

| Area | Convention |
| --- | --- |
| JSON schemas | Remove `$ref` and other reference types because Copilot Studio cannot handle them. |
| Types | Use single types instead of arrays of types. |
| Composition | Flatten `anyOf` and `oneOf` constructs into single schemas. |
| Tool inputs | Ensure all tool input schemas are self-contained without external references. |
| Swagger | Use Swagger 2.0 for Power Platform compatibility. |
| Operations | Implement clear `operationId` values for every endpoint. |
| Parameters | Define parameter schemas with appropriate types and descriptions. |
| Responses | Include comprehensive success and error response schemas, HTTP status codes, and response headers. |
| Resources | Structure MCP resources as Copilot Studio tool outputs with proper MIME type declarations, audience annotations, and priority annotations. |

## Authentication, Connection Parameters, and Security

Implement OAuth 2.0 with MCP security best practices inside Power Platform constraints. Use connection parameter sets for flexible authentication configuration. Validate token audience to prevent passthrough attacks. Add MCP-specific security headers. Support OAuth standard, OAuth enhanced, and API key fallback when the deployment requires multiple authentication methods. Use enum dropdowns for OAuth version and security level selection, clear descriptions and constraints, validation rules, default values, and dynamic configuration through connection parameter values.

## Custom Script, Errors, Logging, and Testing

Handle JSON-RPC transformation in the custom script `script.csx`. Implement JSON-RPC error response format, token validation, audience checking, response transformation for Copilot Studio compatibility, and dynamic security behavior from connection parameters. Add detailed logging for authentication, validation, and transformation steps without leaking secrets. Provide clear troubleshooting messages and align HTTP status codes with error conditions.

Test with actual MCP server implementations. Validate schema transformations in Copilot Studio, verify every supported authentication parameter set, test connection parameter configurations and dynamic behavior, and ensure proper error handling for failure scenarios. Validate tool definitions, resource access, and tool invocation from the Copilot Studio interface.

## Certification and Documentation

Include comprehensive connector documentation such as `readme.md` and `CUSTOMIZE.md`. Provide setup and configuration instructions, document authentication options and security considerations, include publisher and stack owner information, and comply with Power Platform connector certification standards. Confirm transformed schemas produce expected conversational behavior in Copilot Studio.

## Good / Bad Examples

The examples below illustrate Copilot Studio-compatible schema flattening.

**Good**

```json
{
  "type": "object",
  "properties": {
    "query": { "type": "string", "description": "Search query" }
  },
  "required": ["query"]
}
```

Why: the schema is self-contained, uses a single type, and has no `$ref`, `anyOf`, or `oneOf`.

**Bad**

```json
{
  "$ref": "#/definitions/SearchRequest",
  "anyOf": [
    { "type": "string" },
    { "type": "object" }
  ]
}
```

Why: Copilot Studio cannot handle reference types or multi-shape schema composition for tool inputs.

## Conventions

| Rule | Rationale |
| --- | --- |
| Implement JSON-RPC 2.0 and `x-ms-agentic-protocol: mcp-streamable-1.0`. | Copilot Studio can route MCP traffic and streaming correctly. |
| Flatten schemas by removing `$ref`, reference types, type arrays, `anyOf`, and `oneOf`. | Copilot Studio requires self-contained single-type schemas. |
| Use Swagger 2.0 with clear `operationId`, parameters, responses, status codes, and headers. | Power Platform connector import and review need explicit contracts. |
| Validate OAuth token audience and support parameterized authentication methods. | Connectors resist passthrough attacks and fit multiple deployment scenarios. |
| Implement JSON-RPC transformation, error handling, and response shaping in `script.csx`. | MCP servers and Copilot Studio constraints are reconciled at the connector boundary. |
| Test MCP methods, schema transformations, authentication flows, resources, and Copilot Studio conversations. | Compatibility is proven across protocol, connector, and agent layers. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Support `tools/list`, `tools/call`, and `resources/list` where the server exposes them. | Assume a nonstandard MCP subset without negotiation. |
| Use connection parameters for OAuth version, security level, defaults, and validation rules. | Hardcode authentication behavior that varies by deployment. |
| Add MIME type, audience, and priority annotations to resources when useful. | Return raw resources that Copilot Studio cannot consume as tool outputs. |
| Log authentication, validation, and transformation decisions. | Log secrets, tokens, or sensitive payloads. |
| Include `readme.md`, `CUSTOMIZE.md`, publisher, stack owner, and certification details. | Ship a connector without setup, customization, or security documentation. |

## Checklist Before Opening a PR

- [ ] MCP endpoints implement JSON-RPC 2.0 and use `x-ms-agentic-protocol: mcp-streamable-1.0` for Copilot Studio.
- [ ] Schemas remove `$ref`, reference types, arrays of types, `anyOf`, and `oneOf` where Copilot Studio consumes them.
- [ ] Swagger 2.0 operations include clear `operationId`, parameters, response schemas, status codes, and headers.
- [ ] Authentication validates token audience, supports required OAuth/API key parameter sets, and uses MCP-specific security headers.
- [ ] `script.csx` handles JSON-RPC transformation, error responses, token validation, audience checking, and Copilot Studio response shaping.
- [ ] Resources include MIME type declarations and relevant audience or priority annotations.
- [ ] Tests cover actual MCP servers, schema transformations, authentication flows, connection parameters, errors, and Copilot Studio tool invocation.
- [ ] `readme.md`, `CUSTOMIZE.md`, publisher, stack owner, setup, authentication, and security documentation are complete.
