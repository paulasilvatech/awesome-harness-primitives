---
name: swift-mcp-server-generator
description: >-
  Generate a complete Swift Model Context Protocol server project with the official MCP Swift SDK package. Use this skill when asked to create a Swift MCP server, scaffold tools/resources/prompts, add actor-based state, wire swift-log and ServiceLifecycle, or produce Claude Desktop integration.
---

# Swift MCP server generator

Generate a complete Swift package for a production-ready Model Context Protocol server, using the bundled templates for project files and adapting names, handlers, tests, logging, concurrency, and integration instructions to the user's requested server.

## When to invoke

- "Generate a Swift MCP server project."
- "Create an MCP server in Swift with tools and resources."
- "Scaffold a Swift package using the MCP Swift SDK."
- "Add Claude Desktop config for this Swift MCP server."
- "Build handlers with actor-based state and async/await."

## Inputs

Use the user's requested project name, executable name, server description, tools, resources, prompts, and target clients. If project name or server purpose is missing, ask for the minimum missing detail; otherwise choose a safe placeholder such as `my-mcp-server` and make the seam explicit.

## Project structure

Generate this directory tree, replacing `my-mcp-server` and `MyMCPServer` with Swift-safe names derived from the user's project name:

```text
my-mcp-server/
├── Package.swift
├── Sources/
│   └── MyMCPServer/
│       ├── main.swift
│       ├── Server.swift
│       ├── Tools/
│       │   ├── ToolDefinitions.swift
│       │   └── ToolHandlers.swift
│       ├── Resources/
│       │   ├── ResourceDefinitions.swift
│       │   └── ResourceHandlers.swift
│       └── Prompts/
│           ├── PromptDefinitions.swift
│           └── PromptHandlers.swift
├── Tests/
│   └── MyMCPServerTests/
│       └── ServerTests.swift
└── README.md
```

## Generation rules

| Area | Requirement |
| --- | --- |
| Templates | Read `references/project-templates.md` and copy/adapt the full templates verbatim when creating project files. |
| Package | Use the official MCP Swift SDK package and add `swift-log` for logging. |
| Lifecycle | Implement graceful shutdown with `ServiceLifecycle`. |
| Concurrency | Use modern Swift concurrency with `async`/`await` (async/await); keep shared mutable state inside an `actor`. |
| Errors | Use proper `MCPError` handling and return structured failures instead of trapping. |
| Names | Follow Swift naming conventions: `camelCase` for values and functions, `PascalCase` for types. |
| Documentation | Add doc comments to public APIs that clients or downstream maintainers will read. |
| Tests | Add tests for all handler paths, including success and failure cases. |
| README | Include build, run, test, release, install, and client integration instructions. |

## Build and run commands

```bash
swift build
swift run
swift test
swift build -c release
swift build -c release
cp .build/release/MyMCPServer /usr/local/bin/
```

Replace `MyMCPServer` with the generated executable name before showing installation commands.

## Claude Desktop integration

Add the generated executable to `claude_desktop_config.json` when the user asks for local desktop integration:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "/path/to/MyMCPServer"
    }
  }
}
```

## Progressive disclosure and bundled resources

- `references/project-templates.md`: full Swift package templates for `Package.swift`, `main.swift`, `Server.swift`, tool definitions and handlers, resource definitions and handlers, prompt definitions and handlers, tests, and README content. Read it before creating files.

## Gotchas

- **Do not hand-write a thin scaffold when templates exist**: the bundled templates are the source of truth for file content.
- **Do not use global mutable state**: MCP servers process concurrent requests; isolate state in an `actor`.
- **Do not omit tests for empty handlers**: even placeholder tools/resources/prompts need validation that registration and error paths work.
- **Do not hard-code `/usr/local/bin/` as the only install path**: show it as an example and preserve the actual build artifact path.

## Output template

```markdown
## Swift MCP server generated

**Status:** generated | partially generated | blocked
**Project:** `<my-mcp-server>`
**Executable:** `<MyMCPServer>`

### Files created
| Path | Purpose |
| --- | --- |
| `Package.swift` | <package dependencies and targets> |
| `Sources/<Module>/Server.swift` | <server wiring> |
| `Tests/<Module>Tests/ServerTests.swift` | <handler validation> |

### Commands
- `swift build`: pass | not run | fail
- `swift test`: pass | not run | fail
- `swift run`: pass | not run | fail

### Client config
```json
<claude_desktop_config.json snippet when requested>
```
```

## Quality gate

- [ ] Project name, module name, and executable name are Swift-safe and consistently applied.
- [ ] The generated tree includes `Package.swift`, `Sources/`, `Tests/`, and `README.md`.
- [ ] `references/project-templates.md` was read and adapted rather than ignored.
- [ ] The server uses actor-based state, `async`/`await`, `swift-log`, `ServiceLifecycle`, and `MCPError` handling.
- [ ] Tool, resource, and prompt definitions are separated from handlers.
- [ ] Tests cover all generated handlers.
- [ ] Build, run, test, release, install, and `claude_desktop_config.json` instructions are present.
