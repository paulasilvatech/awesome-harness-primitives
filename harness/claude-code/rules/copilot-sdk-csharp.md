---
paths:
  - "**/*.cs"
  - "**/*.csproj"
---

<!-- Generated from harness/github-copilot/instructions/copilot-sdk-csharp.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for building C# applications with the GitHub Copilot SDK, including client setup, sessions, permissions, streaming, custom tools, BYOK providers, and error handling.

# GitHub Copilot SDK C# Conventions — Client Sessions and Tools

These instructions apply to C# source and project files that use the technical-preview `GitHub.Copilot.SDK` package with .NET 10.0 or later and a GitHub Copilot CLI executable available on `PATH`. They are authoritative for SDK client construction, server lifecycle, sessions, permission handling, message delivery, streaming events, custom tools, BYOK provider configuration, errors, and cleanup in matched files; broader application architecture, product safety policy, and repository test conventions win where they define stricter rules.

## Package, Runtime, and Preview Boundaries

Treat the SDK as a preview integration surface: keep calls explicit, isolate SDK-facing code behind application services when possible, and avoid assuming undocumented behavior will remain stable.

| Concern | Convention |
| --- | --- |
| Package installation | Add the SDK with `dotnet add package GitHub.Copilot.SDK`; do not vendor SDK sources or reference unpublished assemblies. |
| Runtime | Target .NET 10.0 or later before introducing SDK code. |
| Emphasis | Do not rely on uppercase emphasis such as `ALWAYS`; enforce requirements through tests and reviewable rules. |
| CLI dependency | Require the GitHub Copilot CLI to be installed and available through `PATH`, unless `CopilotClientOptions.CliPath` or `CopilotClientOptions.CliUrl` deliberately overrides that. |
| Async model | Use `async`/`await` throughout SDK flows; preserve the original `async/await` guidance and avoid blocking on tasks with `.Result` or `.Wait()`. |
| Disposal | Treat `CopilotClient`, `CopilotSession`, and sessions as asynchronous resources and use `await using` or explicit `DisposeAsync()`. |

## Client Initialization and Server Lifecycle

Create clients with `CopilotClient` and configure process ownership with `CopilotClientOptions`. Start the client before use unless `AutoStart` is intentionally enabled, and stop the process you own when the host shuts down.

| API or option | Rule |
| --- | --- |
| `new CopilotClient()` | Use for default CLI discovery from `PATH`, default stdio transport, and automatic server management. |
| `CopilotClientOptions.CliPath` | Set only when the executable is not the default `copilot` command. |
| `CopilotClientOptions.CliArgs` | Use for extra arguments that must be prepended before SDK-managed flags. |
| `CopilotClientOptions.CliUrl` | Use for an existing CLI server such as `localhost:8080`; when provided, the client must not spawn a new process. |
| `CopilotClientOptions.Port` | Leave at `0` for a random port unless integration constraints require a fixed server port. |
| `CopilotClientOptions.UseStdio` | Keep the default `true` for local process integration unless TCP is required. |
| `CopilotClientOptions.LogLevel` | Set deliberately; the default is `info`. |
| `CopilotClientOptions.AutoStart` | Set `false` only when the application owns explicit `StartAsync()` timing. |
| `CopilotClientOptions.AutoRestart` | Keep `true` for resilient hosted scenarios unless crashes must fail fast. |
| `CopilotClientOptions.Cwd` | Set the CLI working directory to the repository or workspace the session should operate in. |
| `CopilotClientOptions.Environment` | Pass only required environment variables; never inject secrets into logs. |
| `CopilotClientOptions.Logger` | Provide an `ILogger` instance for SDK logging instead of writing ad hoc console diagnostics. |
| `StartAsync()` / `StopAsync()` | Use for normal manual lifecycle control. |
| `ForceStopAsync()` | Reserve for shutdown paths where `StopAsync()` takes too long. |
| `PingAsync("test message")` | Use as a connectivity check before reporting the integration ready. |
| `client.State` | Inspect connection state instead of guessing from previous calls. |

## Session Configuration and Operations

Create or resume sessions with explicit configuration so model choice, permissions, tools, streaming, system messages, provider settings, and tool filters are reviewable.

| API or property | Convention |
| --- | --- |
| `CreateSessionAsync(new SessionConfig { ... })` | Use for new sessions and include `OnPermissionRequest` deliberately. |
| `ResumeSessionAsync(sessionId, new ResumeSessionConfig { ... })` | Use when continuing an existing `SessionId`; keep permission behavior explicit on resume. |
| `SessionId` | Persist only when callers need to resume or correlate sessions. |
| `SessionConfig.SessionId` | Set only when a caller owns the custom session identifier. |
| `SessionConfig.Model` | Use supported model names such as `gpt-5` or `claude-sonnet-4.5`; keep the value configurable when deployments differ. |
| `Tools` | Keep custom tool exposure visible on the session configuration. |
| `SessionConfig.Tools` | Register custom tools exposed to the CLI. |
| `SystemMessage` | Keep system-message customization explicit and reviewed. |
| `SessionConfig.SystemMessage` | Use `SystemMessageConfig` and prefer append mode unless the caller has a justified full replacement. |
| `SessionConfig.AvailableTools` | Use as an allowlist, for example `["tool1", "tool2"]`, when a session should have only specific tools. |
| `SessionConfig.ExcludedTools` | Use as a blocklist, for example `["tool3"]`, when most defaults are allowed but one tool is unsafe or irrelevant. |
| `Provider` | Configure custom API provider settings through `ProviderConfig`. |
| `SessionConfig.Provider` | Use `ProviderConfig` for BYOK scenarios. |
| `Streaming` | Treat as the session-level switch for response chunks. |
| `SessionConfig.Streaming` | Set `true` for interactive UX that benefits from response chunks; the default is `false`. |
| `PermissionHandler.ApproveAll` | Use only in controlled examples, test harnesses, or trusted automation; production code should apply the product's permission policy. |
| `session.SessionId` | Read for persistence, logging, and resume flows. |
| `session.SendAsync(new MessageOptions { Prompt = "..." })` | Send user work through `MessageOptions`; include attachments and delivery mode explicitly when needed. |
| `session.AbortAsync()` | Use to cancel current processing without deleting the session. |
| `events/messages` | Treat the event stream and stored messages as audit and recovery data. |
| `session.GetMessagesAsync()` | Use when a caller needs all events or messages for audit, display, or recovery. |
| `await session.DisposeAsync()` | Dispose sessions when they are no longer used. |
| `ListSessionsAsync()` | Use to enumerate session metadata and display `metadata.SessionId`. |
| `DeleteSessionAsync(sessionId)` | Use for intentional permanent cleanup of session state. |

## Message Delivery, Attachments, and Multiple Sessions

Use `MessageOptions` to keep message behavior explicit. Attachments must identify the file type and display name, and concurrent sessions must be treated as independent conversations.

| Feature | Convention |
| --- | --- |
| `MessageOptions.Prompt` | Provide the user instruction or application-generated task text. |
| `UserMessageDataAttachmentsItem` | Use for file attachments in user messages. |
| `MessageOptions.Attachments` | Use `List<UserMessageDataAttachmentsItem>` for files, with `Type = UserMessageDataAttachmentsItemType.File`, `Path = "/path/to/file.cs"`, and a clear `DisplayName` such as `My File`. |
| `"enqueue"` | Queue message processing behind current work. |
| `MessageOptions.Mode = "enqueue"` | Queue work when ordering behind current processing is required. |
| `"immediate"` | Process the message immediately instead of waiting. |
| `MessageOptions.Mode = "immediate"` | Use only when the message should be processed immediately instead of waiting. |
| Multiple sessions | Create separate sessions for independent work, for example one with `Model = "gpt-5"` and another with `Model = "claude-sonnet-4.5"`; never share per-turn state between them. |

## Events and Streaming

Subscribe with `session.On(...)`, keep the returned `IDisposable`, and wait for `SessionIdleEvent` with `TaskCompletionSource` when a send operation needs a completion signal.

| Event or API | Handling rule |
| --- | --- |
| `session.On(evt => { ... })` | Use pattern matching or switch expressions instead of fragile string comparisons. |
| `SetResult` | Use `SetResult` or `TrySetResult` to complete the waiter when `SessionIdleEvent` arrives. |
| `TaskCompletionSource` | Use to wait for `SessionIdleEvent` after `SendAsync`; complete it exactly once. |
| `IDisposable subscription` | Dispose event subscriptions when no longer needed to avoid duplicate handlers and leaks. |
| `UserMessageEvent` | Handle when the UI or log must show user messages. |
| `AssistantMessageEvent` | Handle final assistant content through `msg.Data.Content`; final events are always sent regardless of streaming. |
| `AssistantMessageDeltaEvent` | Handle incremental text through `delta.Data.DeltaContent` when `Streaming = true`. |
| `AssistantReasoningEvent` | Handle final reasoning content through `reasoning.Data.Content` only when the product is allowed to expose it. |
| `AssistantReasoningDeltaEvent` | Handle incremental reasoning through `reasoningDelta.Data.DeltaContent` only for model-dependent experiences that can show reasoning. |
| `ToolExecutionStartEvent` | Track tool start telemetry or progress. |
| `ToolExecutionCompleteEvent` | Track tool completion telemetry or results. |
| `SessionStartEvent` | Record that a session has begun. |
| `SessionIdleEvent` | Treat as processing complete for the current turn. |
| `SessionErrorEvent` | Surface `error.Data.Message` through user-safe error handling and logs. |

## Custom Tools and Return Values

Define tools with `Microsoft.Extensions.AI.AIFunctionFactory.Create` so parameters are typed, described, and serializable. Give every tool a stable name, a concise description, and a return type the SDK can serialize.

| Tool element | Convention |
| --- | --- |
| `using System.ComponentModel` | Import `System.ComponentModel` when using `DescriptionAttribute` or `[Description]` on tool parameters. |
| `using Microsoft.Extensions.AI` | Import the SDK-compatible abstractions for tool creation. |
| `AIFunctionFactory.Create(...)` | Prefer this factory for type-safe custom tools. |
| `ComponentModel` | Keep component model annotations available for tool parameter descriptions. |
| `[Description("Issue ID")] string id` | Describe parameters so the model understands required inputs. |
| `lookup_issue` | Use snake_case tool names that describe one operation. |
| `FetchIssueAsync(id)` | Keep tool handlers asynchronous when they call I/O. |
| JSON-serializable return value | Return ordinary objects when automatic wrapping is sufficient. |
| `ToolResultAIContent` with `ToolResultObject` | Use only when full control over metadata and content wrapping is required. |
| Tool execution flow | Let the client run the handler, serialize the return value, and respond to the CLI; do not manually duplicate protocol responses. |

## System Messages and Provider Configuration

Use system messages and providers as policy-bearing configuration, not casual prompt strings. Preserve guardrails unless a reviewed integration explicitly requires full replacement.

| API or value | Convention |
| --- | --- |
| `SystemMessageConfig` | Store the customization in configuration so the mode and content are visible in review. |
| `SystemMessageMode.Append` | Prefer the default append mode because it preserves safety guardrails while adding workflow rules. |
| `<workflow_rules>` | Use structured content for durable local rules such as security checks or performance review prompts. |
| `SystemMessageMode.Replace` | Use only when the application intentionally takes full control and accepts that default guardrails are removed. |
| `ProviderConfig.Type = "openai"` | Use for a custom API provider when BYOK is required. |
| `ProviderConfig.BaseUrl = "https://api.openai.com/v1"` | Configure the provider endpoint explicitly; do not hardcode it where deployments differ. |
| `ProviderConfig.ApiKey` | Load from a secret store or environment configuration; never commit a real key or placeholder such as `your-api-key`. |

## Error Handling and Cleanup

Handle SDK, JSON-RPC, and session-level failures without losing cleanup. Use `try`/`finally` when `await using` is not possible.

| Scenario | Convention |
| --- | --- |
| `Console.Error.WriteLine` | Use only in samples or command-line utilities; production hosts should log through `ILogger`. |
| `StreamJsonRpc.RemoteInvocationException` | Catch for JSON-RPC failures and log `ex.Message` without exposing sensitive context. |
| General `Exception` | Catch only at integration boundaries; preserve stack traces in logs and return user-safe messages. |
| `SessionErrorEvent` | Monitor runtime session failures even when API calls themselves complete. |
| `await using var client = new CopilotClient()` | Prefer automatic async cleanup for clients. |
| `await using var session = await client.CreateSessionAsync(...)` | Prefer automatic async cleanup for sessions. |
| Manual cleanup | Wrap `StartAsync()` and session work in `try`/`finally` and call `StopAsync()` in the `finally` block. |

## Common Interaction Patterns

Use these patterns as conventions, not mandatory runbook steps.

| Pattern | Required shape |
| --- | --- |
| Simple query-response | Create `CopilotClient`, `StartAsync()`, create a session with `OnPermissionRequest` and `Model`, subscribe to `AssistantMessageEvent` and `SessionIdleEvent`, then `SendAsync(new MessageOptions { Prompt = "What is 2+2?" })`. |
| Multi-turn conversation | Reuse one session, implement a local `SendAndWait(string prompt)` helper, create a new `TaskCompletionSource` and subscription per turn, wait for idle, then `subscription.Dispose()`. |
| Tool with complex return type | Return an object with fields such as `Id`, `Name`, `Email`, and `Role` from an `AIFunctionFactory.Create` handler named `get_user`. |

## Good / Bad Examples

The examples below illustrate asynchronous lifecycle, event completion, and cleanup.

**Good:**

```csharp
await using var client = new CopilotClient();
await client.StartAsync();

await using var session = await client.CreateSessionAsync(new SessionConfig
{
    OnPermissionRequest = PermissionHandler.ApproveAll,
    Model = "gpt-5",
    Streaming = true
});

var done = new TaskCompletionSource();
using var subscription = session.On(evt =>
{
    switch (evt)
    {
        case AssistantMessageDeltaEvent delta:
            Console.Write(delta.Data.DeltaContent);
            break;
        case AssistantMessageEvent msg:
            Console.WriteLine(msg.Data.Content);
            break;
        case SessionIdleEvent:
            done.TrySetResult();
            break;
        case SessionErrorEvent error:
            done.TrySetException(new InvalidOperationException(error.Data.Message));
            break;
    }
});

await session.SendAsync(new MessageOptions { Prompt = "Tell me a story" });
await done.Task;
```

Why: The client and session are asynchronously disposed, the turn completes on `SessionIdleEvent`, streaming deltas and final messages are both handled, and errors reach the waiter.

**Bad:**

```csharp
var client = new CopilotClient();
var session = client.CreateSessionAsync(new SessionConfig()).Result;
session.SendAsync(new MessageOptions { Prompt = "Hello" }).Wait();
```

Why: The code blocks async work, omits permission policy, never starts or disposes resources explicitly, and has no event subscription for completion or errors.

## Conventions

| Rule | Rationale |
|---|---|
| Install `GitHub.Copilot.SDK` through NuGet and target .NET 10.0 or later | Preview SDK behavior remains traceable to a supported package and runtime |
| Configure `CopilotClientOptions` explicitly when defaults do not match the host | CLI process ownership, transport, logs, working directory, and environment stay reviewable |
| Use `await using`, `DisposeAsync()`, `StartAsync()`, `StopAsync()`, and `ForceStopAsync()` according to ownership | SDK processes and sessions do not leak |
| Create and resume sessions with explicit `SessionConfig` or `ResumeSessionConfig` | Model, tools, permissions, system message, provider, streaming, and filters are visible |
| Wait for turn completion with `TaskCompletionSource` and `SessionIdleEvent` | Callers do not race against asynchronous event delivery |
| Handle `AssistantMessageDeltaEvent`, `AssistantReasoningDeltaEvent`, `AssistantMessageEvent`, and `AssistantReasoningEvent` consistently when streaming | Interactive UIs receive chunks while final content remains authoritative |
| Define custom tools with `AIFunctionFactory.Create`, `Description`, and JSON-serializable return values | Tool schemas are understandable, type-safe, and protocol-compatible |
| Prefer `SystemMessageMode.Append` and use `SystemMessageMode.Replace` only with reviewed justification | Default safety guardrails remain in place unless intentionally replaced |
| Catch `StreamJsonRpc.RemoteInvocationException` and monitor `SessionErrorEvent` | Transport failures and runtime session failures are both surfaced |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `dotnet add package GitHub.Copilot.SDK` | Copy SDK sources into the application |
| Set `CliPath`, `CliArgs`, `CliUrl`, `Port`, `UseStdio`, `LogLevel`, `AutoStart`, `AutoRestart`, `Cwd`, `Environment`, and `Logger` only when needed | Hide host-specific process assumptions in scattered code |
| Use `await using var client = new CopilotClient()` and `await using var session = ...` | Leave clients, sessions, or event subscriptions undisposed |
| Use `PermissionHandler.ApproveAll` only in trusted samples, tests, or automation | Treat approve-all permission handling as a safe production default |
| Use `MessageOptions` with `Prompt`, `Attachments`, and `Mode` | Send ambiguous messages without delivery or attachment metadata |
| Use `AvailableTools` and `ExcludedTools` to constrain sessions | Expose unnecessary tools to every session |
| Dispose the `IDisposable` returned by `On()` | Accumulate duplicate event handlers across turns |
| Load `ProviderConfig.ApiKey` from secret configuration | Commit a real BYOK key or print it in logs |
| Use `PingAsync("test message")` for readiness checks | Infer readiness from object construction alone |

## Checklist Before Opening a PR

- [ ] The project references `GitHub.Copilot.SDK` through NuGet and targets .NET 10.0 or later.
- [ ] Copilot CLI discovery is explicit through `PATH`, `CliPath`, or `CliUrl`.
- [ ] Client lifecycle uses `StartAsync()`, `StopAsync()`, `ForceStopAsync()`, `await using`, or `DisposeAsync()` according to ownership.
- [ ] Sessions use explicit `SessionConfig` or `ResumeSessionConfig` for model, permissions, tools, tool filters, provider, system message, and streaming.
- [ ] Message sending uses `MessageOptions` with appropriate `Prompt`, `Attachments`, and `Mode`.
- [ ] Event handling covers completion through `SessionIdleEvent`, errors through `SessionErrorEvent`, and final messages even when streaming is enabled.
- [ ] Custom tools use `AIFunctionFactory.Create`, clear parameter `Description` attributes, stable names, and serializable results.
- [ ] BYOK configuration uses `ProviderConfig` and keeps `ApiKey` out of source, logs, and examples.
- [ ] Connectivity or readiness is verified with `PingAsync("test message")` when the host reports the SDK integration available.
- [ ] Tests or samples avoid blocking `.Result` and `.Wait()` in SDK paths.

## References

- OpenAI-compatible provider endpoint example: https://api.openai.com/v1
