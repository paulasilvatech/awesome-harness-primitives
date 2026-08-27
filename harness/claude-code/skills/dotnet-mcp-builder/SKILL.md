---
name: dotnet-mcp-builder
description: >-
  Build and debug C#/.NET MCP servers and clients with current ModelContextProtocol 2.x packages.
  Use when the user mentions ModelContextProtocol, McpServerTool, MapMcp,
  WithStdioServerTransport, Streamable HTTP, STDIO, prompts, resources, tools, completions,
  elicitation, MCP Apps, Tasks, OAuth, reverse proxy deployment, or .NET MCP errors.
---

<!-- Generated from harness/github-copilot/skills/dotnet-mcp-builder/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Building MCP servers in .NET

Write production-quality MCP servers and basic clients in C#/.NET using the official `ModelContextProtocol` 2.x packages, current transport behavior, modern primitives, and the 2026-07-28 spec rules.

## When to invoke

- "Build an MCP server in C# or .NET."
- "Add a McpServerTool and register it."
- "Fix MapMcp, STDIO, or Streamable HTTP errors."
- "Use WithStdioServerTransport or HTTP transport."
- "Expose this prompt, resource, elicitation flow, MCP App, or Task in .NET."

## Prerequisites and context

- Use official packages from the `ModelContextProtocol` NuGet profile, maintained by Microsoft and the MCP project.
- Target the stable 2.x line unless an existing project is pinned for a documented reason.
- Default new projects to .NET 10 when the user does not specify a target.
- Run `dotnet build` for non-trivial changes.
- Skip this skill for MCP work in other languages.

## Mental model

A .NET MCP server is a normal `Microsoft.Extensions.Hosting` or `WebApplication` app that wires an MCP server through dependency injection.

```csharp
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()      // OR .WithHttpTransport(...)
    .WithToolsFromAssembly()
    .WithPrompts<MyPrompts>()
    .WithResources<MyResources>();
```

Primitives are C# methods on attributed classes: `[McpServerToolType]` plus `[McpServerTool]`, `[McpServerPromptType]` plus `[McpServerPrompt]`, and `[McpServerResourceType]` plus `[McpServerResource]`. Parameters bind from JSON-RPC through `System.Text.Json`; descriptions become part of the JSON Schema the LLM sees.

## Reference routing

Always load `references/packages.md` when creating a new project or when the package version is uncertain.

| Task | Load |
| --- | --- |
| New STDIO server | `references/transport-stdio.md` |
| New HTTP Streamable server | `references/transport-http.md` |
| Add or modify a tool | `references/tool-primitive.md` |
| Add or modify a prompt | `references/prompt-primitive.md` |
| Add or modify a resource | `references/resource-primitive.md` |
| Ask the user a question mid-tool | `references/elicitation.md` |
| Call the client's LLM from a tool | `references/sampling.md` |
| Read the user's project roots | `references/roots.md` |
| Return an interactive UI | `references/mcp-apps.md` |
| Argument completions, progress, filters, instructions | `references/server-features.md` |
| Write a .NET MCP client | `references/client.md` |
| MCP Inspector, in-memory tests, mocks, CI | `references/testing.md` |

For multi-primitive tasks, load all matching references. For trivial edits in an existing file, apply the cardinal rules without loading every reference.

## Cardinal rules

| Rule | Why it matters |
| --- | --- |
| Pin current stable 2.x packages: `ModelContextProtocol`, `ModelContextProtocol.AspNetCore`, `ModelContextProtocol.Core`. | Stale `0.x-preview`, `0.3-preview`, `0.4-preview`, and 1.x-era samples have breaking API differences. |
| STDIO servers must not write to stdout. | Stdout is the JSON-RPC channel; use stderr logging with `LogToStandardErrorThreshold = LogLevel.Trace`. |
| HTTP defaults to stateless in 2.x. | In 1.x HTTP was stateful by default; in 2.x `Stateless` defaults to `true`. |
| The 2026-07-28 revision has no HTTP sessions. | `Stateless = false` serves current clients only through legacy `initialize` fallback. |
| Use Streamable HTTP, not SSE-only. | SSE is deprecated; enable `EnableLegacySse = true` only for old clients. |
| Do not design new servers around deprecated capabilities. | Roots, sampling, and MCP-channel logging are `[Obsolete]` and warn `MCP9005`. |
| Always add `[Description]` to tools and parameters. | Vague schema descriptions are the main reason tools are not selected. |
| Show the registration line for every primitive. | A primitive class without `.WithToolsFromAssembly()`, `.WithTools<T>()`, `.WithPrompts<...>()`, `.WithPromptsFromAssembly()`, or resource registration is invisible. |
| Do not invent APIs. | Check the API reference before using uncertain methods, especially `ModelContextProtocol.Extensions.Tasks` and `ModelContextProtocol.Extensions.Apps`. |

## Transport decisions

| Transport | Use when | Key constraints |
| --- | --- | --- |
| STDIO | Local tools, editor-integrated servers, simple process launch. | No stdout writes; logs to stderr; avoid banners and `Console.WriteLine`. |
| Streamable HTTP stateless | Web-hosted servers and current-protocol clients. | Use `app.MapMcp()` or `app.MapMcp("/mcp")`; no current HTTP sessions. |
| Stateful HTTP legacy path | Legacy elicitation, sampling, roots, pushed notifications. | Set `Stateless = false` only with a documented compatibility reason. |
| Legacy SSE | Old clients that cannot use Streamable HTTP. | Enable only with `EnableLegacySse = true` and call out deprecation. |

For current-protocol HTTP mid-tool questions, prefer multi-round-trip `InputRequiredException` over legacy `ElicitAsync`.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| STDIO server hangs or client cannot parse JSON-RPC | Something writes to stdout. | Remove `Console.WriteLine`, banners, and stdout log sinks; configure stderr logging. |
| HTTP 404 | Path mismatch. | Remember `app.MapMcp()` maps root and `app.MapMcp("/mcp")` maps `/mcp`. |
| Tool not appearing | Missing `[McpServerToolType]` or registration. | Add class attribute and `.WithToolsFromAssembly()` or `.WithTools<T>()`. |
| Arguments not bound | JSON-RPC `arguments` keys do not match parameter names or complex type shape. | Align names and verify `System.Text.Json` binding. |
| Sampling, elicitation, or roots fail | Legacy server-to-client calls on current-protocol stateless HTTP, or client lacks capability. | Use `InputRequiredException`, or documented `Stateless = false` legacy path; verify advertised capability. |
| `MCP9005` warnings after upgrade | Deprecated roots, sampling, or logging APIs. | Migrate; suppress only temporarily with documented transition plan. |

## Working style

- Make minimal, additive changes; add methods to existing primitive classes before restructuring.
- Confirm transport, .NET version, and primitives before scaffolding when context is unclear.
- For OAuth, reverse-proxy, and per-session HTTP wiring, read `references/transport-http.md` before coding.
- For MCP Apps or Tasks, read `references/mcp-apps.md` or package docs before using extension APIs.
- Point to the `EverythingServer` sample when a feature interaction remains unclear.

## Progressive disclosure and bundled resources

- `references/packages.md`: current packages and version guidance.
- `references/transport-stdio.md`: STDIO server setup and stdout/stderr traps.
- `references/transport-http.md`: Streamable HTTP, OAuth, reverse proxy, stateful/stateless wiring.
- `references/tool-primitive.md`: tools, `[McpServerToolType]`, `[McpServerTool]`, descriptions, schemas.
- `references/prompt-primitive.md`: prompts and registration.
- `references/resource-primitive.md`: resources and registration.
- `references/elicitation.md`: `InputRequiredException`, URL mode, and legacy `ElicitAsync`.
- `references/sampling.md`: deprecated sampling guidance.
- `references/roots.md`: deprecated roots guidance.
- `references/mcp-apps.md`: interactive MCP Apps.
- `references/server-features.md`: completions, progress, filters, server instructions.
- `references/client.md`: basic .NET MCP client.
- `references/testing.md`: MCP Inspector, in-memory tests, mocks, and CI.

## SDK vocabulary

Remember `stateless-by-default` HTTP behavior, `discovery-first` negotiation, `input_required`, `down-level` fallback, `server-to-client` (`to-client`) calls through `IMcpServer`, `ILogger` for normal logging, and `highest-frequency` breakage prevention. Legacy `roots/sampling/logging`, `sampling/roots`, `sampling/roots/log`, `Sampling/elicitation/roots`, and `now-deprecated` capabilities require transition notes. Load references for `Add/modify` tasks, `Apps/Tasks`, `log/progress`, and `prompt/resource/elicitation/MCP` work.

## Output template

```markdown
## .NET MCP result

**Status:** complete | needs changes | blocked
**Transport:** STDIO | Streamable HTTP | stateful HTTP | legacy SSE
**Packages:** `ModelContextProtocol` <version>, `ModelContextProtocol.AspNetCore` <version>
**Target framework:** `<TFM>`

| Primitive or feature | Registration | Reference used | Notes |
| --- | --- | --- | --- |
| Tool | `.WithToolsFromAssembly()` | `references/tool-primitive.md` | <description/schema note> |

### Validation
- `dotnet build`: pass | fail | not run (<reason>)
- STDIO stdout check: pass | fail | not applicable
- HTTP route check: pass | fail | not applicable
- Deprecated API check (`MCP9005`): pass | fail | not applicable
```

## Quality gate

- [ ] Current stable 2.x packages are used or any non-2.x version is justified.
- [ ] Transport choice is explicit: STDIO, Streamable HTTP, stateful HTTP legacy, or legacy SSE.
- [ ] STDIO servers write no logs, banners, or tool output to stdout.
- [ ] HTTP routing uses `app.MapMcp()` or `app.MapMcp("/mcp")` intentionally.
- [ ] New tools, prompts, and resources include both attributes and registration lines.
- [ ] Tool and parameter `[Description]` attributes are present and useful.
- [ ] Deprecated roots, sampling, and MCP-channel logging are avoided for new work or documented with `MCP9005` handling.
- [ ] `dotnet build` was run for non-trivial code changes or a concrete blocker is reported.

## References

- [ModelContextProtocol NuGet profile](https://www.nuget.org/profiles/ModelContextProtocol)
- [ModelContextProtocol API reference](https://csharp.sdk.modelcontextprotocol.io/api/ModelContextProtocol.html)
- [EverythingServer sample](https://github.com/modelcontextprotocol/csharp-sdk/tree/main/samples/EverythingServer)
