---
name: "create-mcp-server"
description: "Create or extend the repository-native MCP ecosystem server with typed tools, validation, documentation, and client registration guidance."
argument-hint: "server_name=my-mcp-server language=TypeScript transport=HTTP tools_description='describe the tools'"
tools: ['read', 'search', 'edit', 'execute']
---

# /create-mcp-server

## Objective
Create a repository-native Model Context Protocol implementation by extending the existing TypeScript MCP ecosystem under `mcp-servers/` or, when explicitly requested, by scaffolding a separate MCP server with the same quality standards.

## When to Invoke
Invoke this when the team needs a new MCP tool module, resource surface, or server scaffold that will be developed in this repository and validated with the existing `mcp-servers` build workflow.

## Preconditions
- The requested server or tool name `${input:server_name:my-mcp-server}` is kebab-case or can be converted safely.
- The implementation language `${input:language:TypeScript}` is confirmed; this repository's existing MCP server is TypeScript.
- The desired transport `${input:transport:HTTP}` is known.
- Tool behavior is described in `${input:tools_description:describe each tool purpose and inputs}`.
- No new secrets, credentials, or private third-party data are required for scaffolding.

## Inputs the Team Must Provide
- `server_name`: Kebab-case MCP server or module name.
- `language`: Implementation language; prefer `TypeScript` for this repository.
- `transport`: MCP transport, typically `HTTP` for the existing `mcp-ecosystem` server.
- `tools_description`: Concrete description of each tool, inputs, validation rules, and output shape.

## What I Will Do
- Inspect `mcp-servers/package.json`, `mcp-servers/src/index.ts`, `mcp-servers/src/shared/server-factory.ts`, and existing files under `mcp-servers/src/tools/` before editing.
- Prefer adding a TypeScript tool module under `mcp-servers/src/tools/` and registering it in `mcp-servers/src/index.ts`.
- Use typed schemas with `zod`, structured responses, and clear tool names and descriptions.
- Update MCP documentation or client registration guidance only where it directly relates to the new tool or server.
- Validate with existing commands such as `cd mcp-servers && npm run build`.

## What I Will NOT Do
- I will not bind this prompt to an existing agent because no current Open Horizons agent owns MCP server creation end to end.
- I will not invent non-existent generator skills or scripts.
- I will not add Python or C# scaffolding inside `mcp-servers/` unless the team explicitly chooses a separate project path and accepts a new build workflow.
- I will not add tools that exfiltrate secrets, bypass repository content exclusions, or call unapproved third-party services.
- I will not edit agents, skills, instructions, workflows, or docs outside the prompt-requested MCP implementation scope.

## Output Format
Approved workspace edit. Modify only files required by the prompt scope, then return a chat summary with changed paths and validation evidence.

Return the scaffold or change summary in this shape:

````markdown
# MCP Server Change Summary

| Artifact | Path | Purpose | Status |
| --- | --- | --- | --- |
| Tool module | `mcp-servers/src/tools/<name>.ts` | typed MCP tools | Created |
| Registration | `mcp-servers/src/index.ts` | register tools | Updated |
| Validation | `mcp-servers/package.json` | `npm run build` | Pass |

## Tool Contract
```yaml
name: <tool-name>
description: <clear user-facing description>
input_schema:
  field: type and validation
output:
  content: text summary
  structured: JSON-compatible object
```

## Quick Start
```bash
cd mcp-servers
npm run build
npm start
```
````

## Definition of Done
- [ ] New MCP behavior is grounded in the existing `mcp-servers/` project structure.
- [ ] Tool inputs are validated with typed schemas.
- [ ] The new module is registered in `mcp-servers/src/index.ts` when extending `mcp-ecosystem`.
- [ ] Existing build commands are listed and, when possible, run successfully.
- [ ] Client registration guidance references declared MCP server keys from `.github/mcp.json` only.

## Prompt Body
Use the available tools directly; this prompt is intentionally agent-less because MCP server creation spans code generation and repository validation without matching one existing Open Horizons specialist agent.

**Step 1 - Inspect the MCP project.** Read `mcp-servers/package.json`, `mcp-servers/src/index.ts`, `mcp-servers/src/shared/server-factory.ts`, and similar modules in `mcp-servers/src/tools/` before writing code.

**Step 2 - Choose the implementation path.** If `${input:language:TypeScript}` fits the existing project, extend `mcp-ecosystem`. If another language is requested, explain the repository mismatch and create a separate scaffold only when the target path and validation commands are explicit.

**Step 3 - Define the tool contract.** Convert `${input:tools_description:describe each tool purpose and inputs}` into concrete tool names, descriptions, input schemas, and structured output. Do not proceed with vague or unsafe tool behavior.

**Step 4 - Implement and register.** Create or update TypeScript files under `mcp-servers/src/tools/`, register them in `mcp-servers/src/index.ts`, and preserve the HTTP server behavior implemented by `mcp-servers/src/shared/server-factory.ts`.

**Step 5 - Validate and document.** Run or recommend `cd mcp-servers && npm run build`, summarize created files, and provide registration guidance using only MCP server keys declared in `.github/mcp.json`.

## Invocation Example
```text
/create-mcp-server server_name=platform-docs language=TypeScript transport=HTTP tools_description="Search internal platform runbooks by title and return Markdown summaries."
```
