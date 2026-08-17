---
name: "swift-mcp-server-generator"
description: >-
  Generate a complete Model Context Protocol server project in Swift using the official MCP Swift SDK
  package. Use this skill when the user asks for project generation.
---
# Swift MCP Server Generator

Generate a complete, production-ready MCP server in Swift using the official Swift SDK package.

## Project Generation

When asked to create a Swift MCP server, generate a complete project with this structure:

```
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

## Bundled Resources

- [Swift MCP server project templates](references/project-templates.md) — When creating the Swift project files, open this reference and copy/adapt the full templates verbatim.

## Generation Instructions

1. **Ask for project name and description**
2. **Generate all files** with proper naming
3. **Use actor-based state** for thread safety
4. **Include comprehensive logging** with swift-log
5. **Implement graceful shutdown** with ServiceLifecycle
6. **Add tests** for all handlers
7. **Use modern Swift concurrency** (async/await)
8. **Follow Swift naming conventions** (camelCase, PascalCase)
9. **Include error handling** with proper MCPError usage
10. **Document public APIs** with doc comments

## Build and Run

```bash
# Build
swift build

# Run
swift run

# Test
swift test

# Release build
swift build -c release

# Install
swift build -c release
cp .build/release/MyMCPServer /usr/local/bin/
```

## Integration with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "/path/to/MyMCPServer"
    }
  }
}
```
