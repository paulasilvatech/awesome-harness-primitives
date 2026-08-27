---
paths:
  - "**/*.cs"
  - "**/*.csproj"
---

<!-- Generated from harness/github-copilot/instructions/csharp-mcp-server.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces C# Model Context Protocol server conventions for SDK packages, transports, tool attributes, prompts, sampling, DI, logging, errors, and testing. Use when building MCP servers with the C# SDK.

# C# MCP Server Conventions — ModelContextProtocol SDK

These instructions apply to C# source and project files that build Model Context Protocol servers or low-level MCP clients with the C# SDK. They are authoritative for `ModelContextProtocol` package selection, stdio and HTTP server setup, tool and prompt attributes, dependency injection, sampling, protocol errors, logging, and testing in matched files; repository security policy and transport-specific deployment rules win where they define stricter requirements.

## Packages, Hosting, and Transports

| Concern | Convention |
| --- | --- |
| Default SDK | Use the `ModelContextProtocol` NuGet package for most projects: `dotnet add package ModelContextProtocol --prerelease`. |
| HTTP servers | Use `ModelContextProtocol.AspNetCore` for HTTP-based MCP servers. |
| Minimal dependencies | Use `ModelContextProtocol.Core` for client-only or low-level server APIs. |
| Hosting | Structure projects with `Microsoft.Extensions.Hosting` for dependency injection and lifecycle management. |
| Stdio transport | Use `WithStdioServerTransport()` when building stdio servers. |
| Tool discovery | Use `WithToolsFromAssembly()` to auto-discover and register all tools from the current assembly. |
| Logging | Configure console logging with `LogToStandardErrorThreshold = LogLevel.Trace` so stdout remains reserved for stdio protocol messages. |

## Tools, Prompts, and Descriptions

- Put `[McpServerToolType]` on classes containing MCP tools.
- Put `[McpServerTool]` on methods exposed as tools.
- Use `[Description]` from `System.ComponentModel` to document tools and parameters.
- Keep tool methods focused and single-purpose with meaningful names that clearly indicate their function.
- Provide detailed descriptions explaining what the tool does, what parameters it expects, and what it returns.
- Tool methods can be synchronous or async and may return `Task` or `Task<T>`.
- Return simple types such as `string` and `int`, or complex objects that serialize cleanly to JSON.
- Expose prompts with `[McpServerPromptType]` on classes and `[McpServerPrompt]` on methods.

## Dependency Injection, Sampling, and Cancellation

Use the built-in DI container to manage lifetimes and dependencies.

| Need | Convention |
| --- | --- |
| Tool dependencies | Inject `McpServer`, `HttpClient`, or other services as method parameters when tools need them. |
| Sampling | Use `McpServer.AsSamplingChatClient()` to make sampling requests back to the client from within tools. |
| Async cancellation | Accept `CancellationToken` parameters in async tools. |
| Input validation | Validate parameters before executing work and return meaningful errors. |
| External resources | Consider security implications before exposing tools that access files, networks, or services. |

## Protocol Errors and Fine-Grained Control

Use fine-grained control through `McpServerOptions` with handlers such as `ListToolsHandler` and `CallToolHandler` only when attribute discovery is not sufficient. Throw `McpProtocolException` for protocol-level failures and choose appropriate `McpErrorCode` values such as `McpErrorCode.InvalidParams` for invalid inputs. Keep structured logging on stderr so diagnostics do not pollute MCP stdout.

## Testing

Test MCP servers with `McpClient` from the same SDK or another compliant MCP client. Test tools individually before integrating with LLMs, including valid inputs, invalid inputs, cancellation, serialization, and dependency-injected behavior.

## Good / Bad Examples

The examples below illustrate stdio-safe hosting, tool discovery, descriptions, DI, and cancellation.

**Good**

```csharp
var builder = Host.CreateApplicationBuilder(args);
builder.Logging.AddConsole(options =>
    options.LogToStandardErrorThreshold = LogLevel.Trace);
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();
await builder.Build().RunAsync();

[McpServerToolType]
public static class MyTools
{
    [McpServerTool, Description("Fetches data from a URL")]
    public static async Task<string> FetchData(
        HttpClient httpClient,
        [Description("The URL to fetch")] string url,
        CancellationToken cancellationToken) =>
        await httpClient.GetStringAsync(url, cancellationToken);
}
```

Why: logging goes to stderr, tools are discovered by assembly, descriptions guide clients, and cancellation flows through async work.

**Bad**

```csharp
Console.WriteLine("debug");

public static async Task<string> FetchData(string url)
{
    using var httpClient = new HttpClient();
    return await httpClient.GetStringAsync(url);
}
```

Why: stdout debug output can corrupt stdio transport, the tool lacks MCP attributes and descriptions, manually constructs dependencies, and ignores cancellation.

## Conventions

| Rule | Rationale |
| --- | --- |
| Choose `ModelContextProtocol`, `ModelContextProtocol.AspNetCore`, or `ModelContextProtocol.Core` based on server shape. | Projects carry only the SDK surface they need. |
| Use `Microsoft.Extensions.Hosting`, `AddMcpServer()`, `WithStdioServerTransport()`, and `WithToolsFromAssembly()` for stdio servers. | Hosting, DI, lifecycle, transport, and tool registration stay consistent. |
| Annotate tool and prompt classes and methods with MCP attributes and `Description`. | MCP clients and LLMs can discover callable capabilities accurately. |
| Inject dependencies and accept `CancellationToken` in async tools. | Tools remain testable, lifecycle-safe, and cancellable. |
| Use `McpServer.AsSamplingChatClient()` only when a tool needs client-side sampling with `ChatMessage`, `ChatRole.User`, and `GetResponseAsync`; replace placeholder names such as `ToolName` with meaningful tool names. | Sampling stays explicit and reviewable. |
| Throw `McpProtocolException` with appropriate `McpErrorCode` for protocol-level errors. | Clients receive standard MCP error semantics. |
| Test with `McpClient` or a compliant MCP client before relying on LLM integration. | Protocol and tool behavior are verified independently. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Run `dotnet add package ModelContextProtocol --prerelease` for the default SDK package. | Mix unrelated MCP SDK packages without a transport or API reason. |
| Set `LogToStandardErrorThreshold = LogLevel.Trace` for stdio servers. | Write diagnostics to stdout when using stdio transport. |
| Use `[McpServerToolType]`, `[McpServerTool]`, `[McpServerPromptType]`, and `[McpServerPrompt]`. | Expose unannotated methods and assume clients will discover them. |
| Use `McpServerOptions`, `ListToolsHandler`, and `CallToolHandler` for custom control. | Reimplement handlers when attribute discovery is sufficient. |
| Return JSON-serializable simple or complex objects. | Return framework-specific types that clients cannot serialize. |

## Checklist Before Opening a PR

- [ ] Project references the correct `ModelContextProtocol` package for stdio, HTTP, low-level, or client-only use.
- [ ] Server setup uses hosting, DI, and the appropriate transport registration.
- [ ] Stdio logging writes diagnostics to stderr and preserves stdout for protocol messages.
- [ ] Tools and prompts use MCP attributes and comprehensive `Description` metadata.
- [ ] Async tools accept `CancellationToken` and use injected dependencies.
- [ ] Protocol errors use `McpProtocolException` and appropriate `McpErrorCode` values.
- [ ] Tool outputs are JSON-serializable and security-sensitive tools validate inputs.
- [ ] `McpClient` or another compliant client verifies the server and individual tools.
