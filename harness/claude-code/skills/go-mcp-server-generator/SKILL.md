---
name: go-mcp-server-generator
description: >-
  Generate a complete Go Model Context Protocol server project using
  github.com/modelcontextprotocol/go-sdk with module layout, typed tools, resources, config,
  graceful shutdown, tests, and README. Use when the user asks for a Go MCP server project
  generator, Go MCP tools, stdio transport, or a production-ready MCP server scaffold.
argument-hint: "[project name, module path, tools, resources, or description]"
---

<!-- Generated from harness/github-copilot/skills/go-mcp-server-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Go MCP server generator

Generate a complete Go MCP server project from a product/tool description by creating the module structure, typed handlers, configuration, documentation, and tests needed to run an official Go SDK server.

## When to invoke

- "Generate a Go MCP server project."
- "Create a production-ready MCP server in Go."
- "Scaffold Go tools using github.com/modelcontextprotocol/go-sdk."
- "Build a stdio MCP server with typed inputs and outputs."
- "Add config, tests, and README for a Go MCP server."

## Inputs

Use `$ARGUMENTS` when direct invocation supplies a project name, module path, tool list, resource list, or project description. If `$ARGUMENTS` is empty, infer the smallest useful server from the user's request and ask no follow-up unless required values cannot be safely inferred.

## Project skeleton

Create this directory tree, replacing `{{PROJECT_NAME}}` and `github.com/yourusername/{{PROJECT_NAME}}` with the actual project name and module path:

```text
myserver/
├── go.mod
├── go.sum
├── main.go
├── tools/
│   ├── registry.go
│   ├── tool1.go
│   └── tool2.go
├── resources/
│   └── resource1.go
├── config/
│   └── config.go
├── README.md
└── main_test.go
```

| File | Required content |
| --- | --- |
| `go.mod` | `module github.com/yourusername/{{PROJECT_NAME}}`, `go 1.23`, and `github.com/modelcontextprotocol/go-sdk v1.0.0`. |
| `main.go` | `context.WithCancel`, signal handling for `os.Interrupt` and `syscall.SIGTERM`, `mcp.NewServer`, `mcp.Implementation`, `mcp.Options`, `mcp.ServerCapabilities`, `mcp.ToolsCapability`, `mcp.ResourcesCapability`, `mcp.PromptsCapability`, `mcp.StdioTransport`, and `server.Run`. |
| `tools/tool1.go` | `Tool1Input`, `Tool1Output`, `Tool1Handler`, `RegisterTool1`, JSON and `jsonschema` tags, validation, context cancellation, and `mcp.AddTool`. |
| `tools/registry.go` | `RegisterTools(server *mcp.Server)` that calls `RegisterTool1(server)`, `RegisterTool2(server)`, and future registrations. |
| `config/config.go` | `Config`, `Load`, `getEnv`, `SERVER_NAME`, `VERSION`, and `LOG_LEVEL` defaults. |
| `main_test.go` | `TestTool1Handler` using `context.Background`, `tools.Tool1Input`, assertions for `Status`, nil `result`, and error handling. |
| `README.md` | Description, installation, usage, configuration, available tools, development commands, and license. |

## Core templates

Use these exact API names and placeholders when generating code: `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{TOOL1_DESCRIPTION}}`, `SERVER_NAME`, `VERSION`, and `LOG_LEVEL`.

```go
module github.com/yourusername/{{PROJECT_NAME}}

go 1.23

require (
    github.com/modelcontextprotocol/go-sdk v1.0.0
)
```

```go
server := mcp.NewServer(
    &mcp.Implementation{Name: cfg.ServerName, Version: cfg.Version},
    &mcp.Options{Capabilities: &mcp.ServerCapabilities{
        Tools: &mcp.ToolsCapability{}, Resources: &mcp.ResourcesCapability{}, Prompts: &mcp.PromptsCapability{},
    }},
)
tools.RegisterTools(server)
transport := &mcp.StdioTransport{}
if err := server.Run(ctx, transport); err != nil { log.Fatalf("Server error: %v", err) }
```

```go
type Tool1Input struct {
    Param1 string `json:"param1" jsonschema:"required,description=First parameter"`
    Param2 int    `json:"param2,omitempty" jsonschema:"description=Optional second parameter"`
}

type Tool1Output struct {
    Result string `json:"result" jsonschema:"description=The result of the operation"`
    Status string `json:"status" jsonschema:"description=Operation status"`
}

func Tool1Handler(ctx context.Context, req *mcp.CallToolRequest, input Tool1Input) (*mcp.CallToolResult, Tool1Output, error) {
    if input.Param1 == "" { return nil, Tool1Output{}, fmt.Errorf("param1 is required") }
    if ctx.Err() != nil { return nil, Tool1Output{}, ctx.Err() }
    return nil, Tool1Output{Result: fmt.Sprintf("Processed: %s", input.Param1), Status: "success"}, nil
}
```

## Procedure

1. Initialize Module: create `go.mod` with the module path, `go 1.23`, and the official SDK dependency.
2. Structure: create `main.go`, `tools/`, `resources/`, `config/`, `README.md`, and `main_test.go` exactly once.
3. Server Setup: keep `main.go` minimal; load config, create cancellation context, handle graceful shutdown, build `mcp.NewServer`, register tools, and run stdio transport.
4. Tools: create at least 2-3 useful tools with typed input/output structs, JSON schema documentation, focused names, single-purpose handlers, and descriptive errors.
5. Error Handling: validate inputs, check `ctx.Err()`, wrap or return useful errors, and avoid panics in handlers.
6. Documentation: document installation with `go mod download` and `go build -o {{PROJECT_NAME}}`, usage with `./{{PROJECT_NAME}}`, available tools, inputs, outputs, and configuration.
7. Testing: include at least one test per tool and run `go test ./...`; build with `go build -o {{PROJECT_NAME}}`.

## Generation rules

| Area | Rule |
| --- | --- |
| Type Safety | Use structs with JSON schema tags for every tool input and output. |
| Configuration | Use environment variables through `getEnv`; document `SERVER_NAME`, `VERSION`, and `LOG_LEVEL`. |
| Logging | Prefer structured logging with `log/slog`; basic `log` is acceptable in minimal scaffolds. |
| Transport | Default to stdio and document alternatives instead of adding unrequested network listeners. |
| Resources | Add `resources/resource1.go` only when the generated server exposes MCP resources. |
| Tests | Test tool handlers directly without starting an external client. |
| Exports | Document all exported functions and keep package names descriptive. |
| README | Include `{{PROJECT_DESCRIPTION}}`, `{{TOOL1_DESCRIPTION}}`, install, usage, config, development, and MIT license sections. |

## SDK import and field names

Generated files import `github.com/modelcontextprotocol/go-sdk/mcp` where code references `mcp`. Keep package examples explicit about `os/signal`, handler inputs/outputs, JSON fields `param1`, `param2`, and `status`, and config struct field `LogLevel`.

## Output template

```markdown
## Go MCP server scaffold - <project name>

**Status:** generated | needs input | blocked
**Module:** `github.com/<owner>/<project>`
**SDK:** `github.com/modelcontextprotocol/go-sdk`

| File | Purpose | Notes |
| --- | --- | --- |
| `go.mod` | Module and dependencies | `go 1.23`, SDK pinned |
| `main.go` | Server bootstrap | stdio transport and graceful shutdown |
| `tools/<tool>.go` | Tool handlers | typed input/output and validation |
| `config/config.go` | Environment config | `SERVER_NAME`, `VERSION`, `LOG_LEVEL` |
| `main_test.go` | Handler tests | `go test ./...` |
| `README.md` | Usage documentation | install, run, config, tools |

### Commands
- `go mod download`
- `go test ./...`
- `go build -o <project>`

### Validation
- `go test ./...`: pass | fail
- `go build -o <project>`: pass | fail
```

## Quality gate

- [ ] `go.mod` uses the actual module path, `go 1.23`, and `github.com/modelcontextprotocol/go-sdk v1.0.0`.
- [ ] `main.go` creates an `mcp.NewServer`, registers tools, uses `mcp.StdioTransport`, and handles `os.Interrupt` plus `syscall.SIGTERM`.
- [ ] At least 2-3 useful tools exist and each has typed structs, JSON schema tags, validation, context cancellation, and tests.
- [ ] `config.Load` reads `SERVER_NAME`, `VERSION`, and `LOG_LEVEL` with defaults.
- [ ] `README.md` includes installation, usage, configuration, available tools, development commands, and license.
- [ ] `go test ./...` and `go build -o {{PROJECT_NAME}}` were run or the blocker is reported.
