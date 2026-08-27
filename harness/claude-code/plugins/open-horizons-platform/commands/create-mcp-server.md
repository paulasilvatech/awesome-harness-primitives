---
description: >-
  Create or extend an approved MCP implementation under mcp-servers using the repository's MCP
  skills.
argument-hint: "approved_paths=<mcp-servers/...> behavior=<tool or server contract>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/prompts/create-mcp-server.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create MCP server

## Objective

Implement `${input:behavior}` only in the explicitly approved `${input:approved_paths}` under
`mcp-servers/`.

## When to Invoke

Use when an MCP tool, resource, prompt, transport, or server change has an approved repository-local
write scope.

## Preconditions

- `${input:approved_paths}` lists exact repository-relative paths, all beneath `mcp-servers/`.
- `${input:behavior}` defines the intended MCP contract and security boundary.
- The requested change does not require secrets in source.

If any precondition fails, report the blocker and do not edit.

## Inputs the Team Must Provide

- Approved write paths: `${input:approved_paths}`.
- Tool or server contract: `${input:behavior}`.
- Language and transport constraints: `${input:language_transport}`.
- Required validation: `${input:validation}`.

## What I Will Do

- Invoke the `mcp-builder` skill for implementation and security criteria.
- Invoke the `mcp-ecosystem` skill to ground current protocol, SDK, and ecosystem references.
- Inspect the actual root `mcp.json` before giving client registration guidance.
- Edit only approved `mcp-servers/` paths and run the supplied repository validation.

## What I Will NOT Do

- Edit root `mcp.json`, `.github/`, or any path outside `mcp-servers/`.
- Invent undeclared server keys, SDK APIs, credentials, or validation results.
- Add destructive MCP behavior without an explicit approval boundary.

## Output Format

Approved workspace edit limited to `${input:approved_paths}`, followed by:

```markdown
## MCP change result
- Changed paths: <paths>
- Contract and security boundary: <summary>
- Validation: <commands and actual results>
- Registration guidance: <root mcp.json evidence or not applicable>
- Blockers: <none or details>
```

## Definition of Done

- [ ] The `mcp-builder` and `mcp-ecosystem` skills were invoked.
- [ ] Every changed path was explicitly approved and is under `mcp-servers/`.
- [ ] The requested contract and security boundaries are implemented.
- [ ] Actual validation results and any root `mcp.json` evidence are reported.

## Prompt Body

Have `open-horizons-engineer` invoke `mcp-builder` and `mcp-ecosystem`, then
implement `${input:behavior}` within `${input:approved_paths}`. Use `${input:language_transport}` and
`${input:validation}` as constraints. Stop rather than widening the write scope.

## Invocation Example

Run **Chat: Run Prompt**, select `create-mcp-server`, set approved paths to
`mcp-servers/src/tools/platform-docs.ts,mcp-servers/src/index.ts`, and provide the tool contract,
transport, and validation command.
