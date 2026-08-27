---
name: mcp-cli
description: >-
  Use the MCP CLI to discover Model Context Protocol servers, inspect tool schemas, grep tool
  names, and call MCP tools with JSON, raw text, or stdin arguments. Use when the user asks to
  list MCP servers, inspect a server/tool schema, call an MCP tool from the command line, or
  script MCP access with --json or --raw output.
---

<!-- Generated from harness/github-copilot/plugins/mcp-development/skills/mcp-cli/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# MCP CLI

Discover available MCP servers, inspect each tool's JSON input schema, then execute external tools, APIs, data sources, filesystems, databases, or GitHub integrations from the command line with explicit arguments and parseable output.

## When to invoke

- "List the MCP servers available in this environment."
- "Show the schema for this MCP tool."
- "Call an MCP tool from the command line with JSON arguments."
- "Search MCP tools by name."
- "Pipe MCP CLI JSON output into another command."

## Prerequisites and context

- The `mcp-cli` executable must be installed and configured for the current environment.
- MCP server availability depends on the active MCP configuration and credentials; missing servers are configuration problems, not code problems.
- Use the CLI when shell scripting, schema discovery, or direct server/tool invocation is the desired interface.

## Command reference

| Command | Purpose | Notes |
| --- | --- | --- |
| `mcp-cli` | List all configured servers and tool names. | Add `-d` to include descriptions. |
| `mcp-cli <server>` | Show the tools exposed by one server with parameters. | Use before calling an unfamiliar tool. |
| `mcp-cli <server> -d` | Show the server tools with descriptions. | More verbose; useful for discovery. |
| `mcp-cli <server>/<tool>` | Print the full JSON schema for one tool. | Inspect required fields, types, enums, and defaults. |
| `mcp-cli <server>/<tool> '<json>'` | Call a tool with inline JSON arguments. | Quote JSON safely; prefer stdin for complex text. |
| `mcp-cli grep "<glob>"` | Search tools by name. | Use shell-style patterns such as `*file*`. |
| `mcp-cli <server>/<tool> --json` | Emit JSON output for scripting. | Pipe to `jq`, Python, or other parsers. |
| `mcp-cli <server>/<tool> --raw` | Emit raw text content. | Use only when the downstream command expects plain text. |

## Procedure

1. Discover servers with `mcp-cli` unless the server/tool is already known.
2. Explore the candidate server with `mcp-cli <server>`; add `-d` when names alone are ambiguous.
3. Inspect the exact schema with `mcp-cli <server>/<tool>` before constructing arguments.
4. Execute with `mcp-cli <server>/<tool> '<json>'`, stdin, or piped JSON; use `--json` when automation needs structured output.
5. Interpret the exit code and tool result separately: a successful CLI invocation can still return a domain-level error from the MCP tool.

## Argument patterns

| Pattern | Use | Example |
| --- | --- | --- |
| Inline JSON | Short, simple argument objects | `mcp-cli filesystem/read_file '{"path": "./README.md"}'` |
| Heredoc stdin | JSON containing quotes, newlines, or generated content | `mcp-cli server/tool <<EOF` followed by `{"content": "Text with 'quotes' inside"}` and `EOF` |
| Pipe from file | Reusable argument payloads | `cat args.json | mcp-cli server/tool` |
| Parseable output | Machine processing | `mcp-cli filesystem/read_file '{"path": "./README.md"}' --json` |
| Tool search | Unknown capability name | `mcp-cli grep "*file*"` |

## Examples

```bash
# List all servers and tool names
mcp-cli

# See all tools with parameters
mcp-cli filesystem

# Include descriptions
mcp-cli filesystem -d

# Get JSON schema for a specific tool
mcp-cli filesystem/read_file

# Call the tool
mcp-cli filesystem/read_file '{"path": "./README.md"}'

# Search for tools
mcp-cli grep "*file*"

# JSON output for parsing
mcp-cli filesystem/read_file '{"path": "./README.md"}' --json

# Complex JSON with quotes through stdin
mcp-cli server/tool <<EOF
{"content": "Text with 'quotes' inside"}
EOF

# Pipe from a file or command
cat args.json | mcp-cli server/tool

# Find TypeScript files, extract the first path, then read it
mcp-cli filesystem/search_files '{"path": "src/", "pattern": "*.ts"}' --json | jq -r '.content[0].text' | head -1 | xargs -I {} sh -c 'mcp-cli filesystem/read_file "{"path": "{}"}"'
```

## Options

| Flag | Purpose |
| --- | --- |
| `-j, --json` | JSON output for scripting; equivalent in intent to long-form JSON output. |
| `-r, --raw` | Raw text content for consumers that do not want structured envelopes. |
| `-d` | Include descriptions, for example `mcp-cli filesystem -d`. |

Use discovery to move from `servers/tools` lists to specific schemas, and pipe from a `file/command` when arguments are generated outside the shell.
## Exit codes

| Code | Meaning | Response |
| --- | --- | --- |
| `0` | Success | Read the returned content and continue. |
| `1` | Client error: bad arguments or missing config | Re-inspect the schema and server configuration. |
| `2` | Server error: the MCP tool failed | Report the tool error and retry only after changing inputs or context. |
| `3` | Network error | Check connectivity, server process state, credentials, or proxy settings. |

## Gotchas

- **Inspect schemas before execution**: guessing JSON fields causes `1` client errors and can hide required nested objects.
- **Use stdin for complex JSON**: shell quoting corrupts payloads that contain quotes, backslashes, or newlines.
- **Do not confuse tool discovery with authorization**: a listed tool can still fail because the backing service lacks credentials.
- **Prefer `--json` for scripts**: parsing human text output is brittle when descriptions or formatting change.

## Output template

```markdown
## MCP CLI result — <server/tool or discovery target>

**Status:** success | client error | server error | network error | blocked
**Command:** `<mcp-cli command>`
**Exit code:** 0 | 1 | 2 | 3 | not run

### Result
<server list, schema summary, or tool output>

### Follow-up
- <next command, schema fix, credential check, or none>
```

## Quality gate

- [ ] Server discovery or a known server/tool name was established before execution.
- [ ] `mcp-cli <server>/<tool>` schema was inspected before constructing non-trivial JSON.
- [ ] JSON arguments were valid and safely quoted, sent by heredoc, or piped through stdin.
- [ ] `--json` or `--raw` was used only when the downstream consumer required that format.
- [ ] Exit code `0`, `1`, `2`, or `3` was interpreted and reported with the command that produced it.
