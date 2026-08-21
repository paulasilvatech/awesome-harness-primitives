---
applyTo: '**/*.go,**/go.mod,**/go.sum'
description: 'Enforces Go conventions for building Model Context Protocol servers with github.com/modelcontextprotocol/go-sdk, including tools, resources, prompts, transports, errors, schema tags, testing, and module setup.'
---

# Go MCP Server Conventions — Official SDK Servers

These instructions apply to Go source and module files matched by `**/*.go`, `**/go.mod`, and `**/go.sum` when building Model Context Protocol servers with `github.com/modelcontextprotocol/go-sdk/mcp`. They are authoritative for server setup, tool/resource/prompt registration, transports, context handling, JSON schema tags, testing, module declarations, logging, configuration, and graceful shutdown; broader Go style, security, deployment, or repository-specific instructions win when they impose stricter requirements.

## Server Setup and Capabilities

Create servers with `mcp.NewServer`, an `mcp.Implementation`, and explicit `mcp.Options` when capabilities matter. Name and version come from configuration when possible instead of being scattered through handlers.

```go
server := mcp.NewServer(
    &mcp.Implementation{Name: "my-server", Version: "v1.0.0"},
    &mcp.Options{
        Capabilities: &mcp.ServerCapabilities{
            Tools:     &mcp.ToolsCapability{},
            Resources: &mcp.ResourcesCapability{Subscribe: true},
            Prompts:   &mcp.PromptsCapability{},
        },
    },
)
```

Use `mcp.ServerCapabilities` to advertise only features the server actually implements. Do not imply tools, resources, prompts, or subscriptions unless handlers are registered and tested.

## Tools, Resources, and Prompts

Use SDK registration helpers and typed input/output structs so schemas remain stable.

| MCP surface | Convention |
| --- | --- |
| Tools | Register with `mcp.AddTool`, describe with `mcp.Tool`, accept `context.Context`, `*mcp.CallToolRequest`, and a typed input, and return `*mcp.CallToolResult`, typed output, and `error` |
| Resources | Register with `mcp.AddResource`, describe with `mcp.Resource`, and return `*mcp.ReadResourceResult` containing `mcp.TextResourceContents` or another appropriate content type |
| Prompts | Register with `mcp.AddPrompt`, describe with `mcp.Prompt` and `mcp.PromptArgument`, and return `*mcp.GetPromptResult` with `mcp.PromptMessage` values |

Use struct tags such as ``json:"query" jsonschema:"the search query"`` and ``json:"limit,omitempty" jsonschema:"maximum results to return"`` on inputs and outputs. Include stable JSON names and `omitempty` only when omission is meaningful to clients.

## Transports and Runtime Lifecycle

Use `mcp.StdioTransport` for desktop integrations that communicate over stdin/stdout. Use `mcp.HTTPTransport` for HTTP-based servers, with `Addr`, TLS, and timeouts configured by the application when exposed beyond local development.

```go
if err := server.Run(ctx, &mcp.StdioTransport{}); err != nil {
    log.Fatal(err)
}

transport := &mcp.HTTPTransport{Addr: ":8080"}
if err := server.Run(ctx, transport); err != nil {
    log.Fatal(err)
}
```

Wire shutdown through `context.WithCancel`, `os.Signal`, `signal.Notify`, `os.Interrupt`, and `syscall.SIGTERM`. Pass the cancellation-aware `ctx` into `server.Run` and every operation that may block.

## Context, Errors, and Validation

Every handler respects context cancellation and returns typed zero values with errors when work cannot continue. Check `ctx.Err()` before expensive work and use `select` on `ctx.Done()` for long-running operations.

Validate inputs at the boundary. Return errors such as `fmt.Errorf("query cannot be empty")` for invalid inputs and wrap operational failures with `%w`, for example `fmt.Errorf("operation failed: %w", err)`. Do not log and swallow errors that need to reach the MCP client.

## JSON Schema, Configuration, and Logging

Document struct fields with `jsonschema` tags so clients can render useful forms and validate inputs.

```go
type Input struct {
    Name   string   `json:"name" jsonschema:"required,description=User's name"`
    Age    int      `json:"age" jsonschema:"minimum=0,maximum=150"`
    Email  string   `json:"email,omitempty" jsonschema:"format=email"`
    Tags   []string `json:"tags,omitempty" jsonschema:"uniqueItems=true"`
    Active bool     `json:"active" jsonschema:"default=true"`
}
```

Use structured logging with `log/slog`, for example `logger.Info("tool called", "name", req.Params.Name, "args", req.Params.Arguments)`, while avoiding secrets or oversized payloads. Load configuration from environment variables or config files into a `Config` struct with fields such as `ServerName`, `Version`, and `Port`; use environment keys such as `SERVER_NAME` deliberately and document defaults.

## Module Setup and Testing

Initialize modules with `go mod init github.com/yourusername/yourserver` and add the official SDK with `go get github.com/modelcontextprotocol/go-sdk@latest` unless the repository already pins dependencies. A Go MCP server module should declare an appropriate Go version and require the SDK, for example:

```go
module github.com/yourusername/yourserver

go 1.23

require github.com/modelcontextprotocol/go-sdk v1.0.0
```

Test handlers directly with standard Go tests. Use `context.Background()`, typed inputs, explicit assertions on typed outputs, and error checks with `t.Fatalf` or `t.Error`. Keep tool logic factored so `SearchTool`, `MyTool`, and similar handlers can be exercised without starting a transport.


## Preserved SDK API Vocabulary

Keep these API names and sample paths when condensing examples because they identify real SDK surfaces or configuration contracts.

| Vocabulary | Convention |
| --- | --- |
| `struct-based` | Use struct-based input and output for MCP tools rather than untyped maps. |
| `GetResource`, `ResourceContents`, `TextResourceContents`, `data/example.txt`, and `text/plain` | Preserve them in resource examples that return text content with a URI and MIME type. |
| `PromptInput`, `AnalyzePrompt`, `TextContent`, and `RoleUser` | Preserve them in prompt examples that create `mcp.PromptMessage` values for user-role prompts. |
| `MyInput`, `MyOutput`, and `LongRunningTool` | Use them for generic context-cancellation examples. |
| `TestSearchTool` | Keep direct handler tests named after the tool behavior. |
| `LoadConfig`, `SERVER_NAME`, `VERSION`, and `PORT` | Preserve these names in configuration examples that load `ServerName`, `Version`, and `Port` from environment variables. |
| `stdin/stdout` | Use this exact phrase when explaining stdio transport behavior. |
| ``json:"results" jsonschema:"list of search results"`` and ``json:"count" jsonschema:"number of results found"`` | Keep output schema tags descriptive for client integration. |
| ``json:"topic" jsonschema:"the topic to analyze"`` | Keep prompt argument schema tags descriptive for reusable prompt templates. |

## Good / Bad Examples

The examples below illustrate typed handlers and context-aware errors.

**Good:**

```go
func SearchTool(ctx context.Context, req *mcp.CallToolRequest, input ToolInput) (*mcp.CallToolResult, ToolOutput, error) {
    if err := ctx.Err(); err != nil {
        return nil, ToolOutput{}, err
    }
    if input.Query == "" {
        return nil, ToolOutput{}, fmt.Errorf("query cannot be empty")
    }

    results, err := performSearch(ctx, input.Query, input.Limit)
    if err != nil {
        return nil, ToolOutput{}, fmt.Errorf("operation failed: %w", err)
    }

    return nil, ToolOutput{Results: results, Count: len(results)}, nil
}
```

Why: The handler uses the SDK signature, honors cancellation, validates input, wraps errors, and returns typed output.

**Bad:**

```go
func SearchTool(ctx context.Context, req *mcp.CallToolRequest, input map[string]any) (*mcp.CallToolResult, map[string]any, error) {
    results := performSearch(context.Background(), input["query"].(string), 0)
    log.Println(results)
    return nil, map[string]any{"results": results}, nil
}
```

Why: The handler drops the caller context, uses untyped maps and unsafe assertions, hides failures, and logs instead of returning a complete typed response.

## Conventions

| Rule | Rationale |
|---|---|
| Create servers with `mcp.NewServer`, `mcp.Implementation`, and accurate `mcp.Options` | Clients receive truthful server identity and capabilities |
| Register tools, resources, and prompts with `mcp.AddTool`, `mcp.AddResource`, and `mcp.AddPrompt` | SDK registration keeps schemas and handlers discoverable |
| Use typed structs for tool inputs and outputs | Compile-time checks prevent schema drift and unsafe casts |
| Add `json` and `jsonschema` tags to exposed fields | MCP clients can generate useful forms and validation |
| Use `mcp.StdioTransport` for desktop stdio and `mcp.HTTPTransport` for HTTP servers | The transport matches the integration model |
| Respect `context.Context`, `ctx.Err()`, and `ctx.Done()` in every handler | Cancellation and deadlines propagate correctly |
| Validate inputs and wrap operational errors with `%w` | Clients receive actionable failures and callers can inspect causes |
| Test handlers directly with Go's `testing` package | Tool behavior is verified without transport overhead |
| Use `log/slog` and configuration structs for runtime concerns | Operational output stays structured and configurable |
| Handle `os.Interrupt` and `syscall.SIGTERM` through cancellation | Servers shut down gracefully without orphaned work |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `github.com/modelcontextprotocol/go-sdk/mcp` and SDK helper functions | Invent parallel registration mechanisms |
| Return typed outputs such as `ToolOutput` with `Results` and `Count` | Return ad hoc `map[string]any` payloads from tool handlers |
| Document fields with `jsonschema:"required,description=..."`, `minimum`, `maximum`, `format=email`, `uniqueItems`, or `default` where appropriate | Leave client-facing schemas undescribed |
| Pass the request `ctx` into downstream work | Replace it with `context.Background()` inside handlers |
| Configure `SERVER_NAME`, `Version`, and `Port` through a `Config` loader | Hardcode runtime identity and ports throughout handlers |
| Use `go test` against handler functions | Depend only on manual MCP client testing |
| Pin or intentionally update `github.com/modelcontextprotocol/go-sdk` in `go.mod` | Leave dependency changes unexplained |

## Checklist Before Opening a PR

- [ ] The server is created with `mcp.NewServer`, `mcp.Implementation`, and accurate capabilities.
- [ ] Tools use `mcp.AddTool`, typed input and output structs, and the `*mcp.CallToolRequest` handler signature.
- [ ] Resources use `mcp.AddResource`, `mcp.Resource`, `*mcp.ReadResourceRequest`, and `*mcp.ReadResourceResult` with appropriate contents.
- [ ] Prompts use `mcp.AddPrompt`, `mcp.Prompt`, `mcp.PromptArgument`, `*mcp.GetPromptRequest`, `*mcp.GetPromptResult`, and `mcp.PromptMessage`.
- [ ] Exposed fields have stable `json` names and useful `jsonschema` tags.
- [ ] Handlers validate inputs, respect `ctx.Err()` or `ctx.Done()`, and wrap operational errors.
- [ ] The selected `mcp.StdioTransport` or `mcp.HTTPTransport` matches the deployment model.
- [ ] Graceful shutdown cancels the server on `os.Interrupt` and `syscall.SIGTERM`.
- [ ] `go.mod` declares the intended Go version and `github.com/modelcontextprotocol/go-sdk` dependency.
- [ ] Go tests exercise handler behavior with `context.Background()` and typed assertions.
