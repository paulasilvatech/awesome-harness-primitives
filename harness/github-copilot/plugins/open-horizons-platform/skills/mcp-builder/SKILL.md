---
name: mcp-builder
description: >-
  Designs, implements, reviews, and evaluates Model Context Protocol servers
  in TypeScript or Python. Use when creating MCP tools, resources, prompts,
  transports, authentication, schemas, pagination, or server evaluations for
  an external API or service.
license: Complete terms in LICENSE.txt
---

# MCP Server Builder

Build MCP servers with small, typed, discoverable tool surfaces and explicit
security boundaries. Verify version-sensitive SDK behavior against official
Model Context Protocol and SDK documentation before generating code.

## When to invoke

- Create an MCP server for an API, data source, or internal service.
- Add or redesign MCP tools, resources, prompts, or transports.
- Review MCP schemas, authentication, pagination, errors, or annotations.
- Build evaluations that prove an agent can use the server effectively.

## Procedure

1. Establish the service boundary.
   - Identify user workflows, API ownership, authentication, rate limits, and
     destructive operations.
   - Treat service responses as untrusted data and keep credentials outside
     prompts, tool results, source control, and logs.
2. Verify current protocol and SDK behavior.
   - Start from the official MCP specification and the official SDK repository
     for the selected language.
   - Record the retrieved version or date for volatile APIs.
3. Select the implementation surface.
   - Prefer TypeScript and Streamable HTTP for remote stateless services.
   - Use stdio for local servers.
   - Use Python when the target repository or service is Python-native.
4. Design the tool inventory.
   - Prefer a cohesive set of composable API tools over duplicate convenience
     wrappers.
   - Use action-oriented names with a stable service prefix.
   - Keep descriptions concise and include bounded inputs, pagination, and
     structured outputs.
   - Set `readOnlyHint`, `destructiveHint`, `idempotentHint`, and
     `openWorldHint` from actual behavior.
5. Implement shared infrastructure.
   - Centralize authentication, HTTP clients, retries, pagination, error
     translation, redaction, and response-size limits.
   - Validate inputs with Zod in TypeScript or Pydantic in Python.
   - Return structured content where the selected SDK supports it.
6. Test and evaluate.
   - Compile or type-check the server and run focused unit/integration tests.
   - Exercise the server with MCP Inspector when available.
   - Create independent, stable, read-only evaluation questions whose answers
     are verified from the target service.

## Security criteria

- Default deny for unknown tools, operations, scopes, paths, and destinations.
- Require explicit approval for destructive or irreversible operations.
- Use short-lived workload or service identity credentials where supported.
- Bound pagination, result bytes, retries, timeouts, and tool-call concurrency.
- Do not expose raw upstream errors, secrets, tokens, or sensitive payloads.
- Separate catalog visibility from runtime authorization.

## Output template

```markdown
# MCP builder result

**Status:** completed | blocked
**Language:** TypeScript | Python
**Transport:** Streamable HTTP | stdio
**Summary:** <one-sentence outcome>

### Tool inventory
| Tool | Behavior | Mutability | Input/output contract |
| --- | --- | --- | --- |

### Validation evidence
- Build/typecheck: <command and result>
- Tests: <command and result>
- Inspector: <result or not run>
- Evaluations: <path and result or not generated>
- Security boundaries: <identity, allowlist, limits, approvals>
```

## Limits

- Do not invent SDK methods, protocol fields, or transport behavior.
- Do not expose every upstream endpoint when it creates an unsafe or unusable
  tool surface.
- Do not create evaluation questions that mutate data or depend on unstable
  answers.
- Do not deploy or publish without explicit approval.

## Progressive disclosure and bundled resources

- `reference/mcp_best_practices.md`: protocol-wide design guidance.
- `reference/node_mcp_server.md`: TypeScript SDK patterns and examples.
- `reference/python_mcp_server.md`: Python and FastMCP patterns and examples.
- `reference/evaluation.md`: evaluation design and XML contract.
- `scripts/evaluation.py`: evaluation runner.
- `scripts/connections.py`: evaluation connection helper.
- `scripts/example_evaluation.xml`: example evaluation fixture.

Read only the resources needed for the chosen language and phase.

## Quality gate

- [ ] Official protocol and selected SDK behavior were checked for currentness.
- [ ] Tool names, descriptions, schemas, annotations, and outputs are explicit.
- [ ] Authentication, authorization, redaction, limits, and destructive-action
      approval are enforced outside model instructions.
- [ ] Pagination, retries, timeouts, partial failures, and actionable errors are
      tested.
- [ ] Build or typecheck and focused tests pass.
- [ ] Evaluations are independent, read-only, realistic, stable, and verified.
- [ ] The response follows `## Output template` exactly.
- [ ] Every referenced bundled resource exists.
