---
paths:
  - "**/*.go"
  - "**/go.mod"
---

<!-- Generated from harness/github-copilot/instructions/copilot-sdk-go.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Go conventions for applications that use the GitHub Copilot SDK, including client setup, sessions, events, tools, permissions, providers, and cleanup.

# GitHub Copilot SDK Go Conventions — Clients, Sessions, and Tools

These instructions apply to Go source files and Go module files that use `github.com/github/copilot-sdk/go`. They are authoritative for Copilot SDK client setup, session configuration, event handling, streaming, custom tools, system messages, attachments, message modes, BYOK provider configuration, lifecycle cleanup, and error handling in matched Go files; repository-wide Go style, security, and testing primitives win where they define stricter rules. The SDK is in technical preview, may introduce breaking changes, requires Go `1.21` or later, requires the GitHub Copilot CLI installed and in `PATH`, uses goroutines and channels for concurrent operations, and should not add external dependencies beyond the standard library unless the project already accepts them.

## Module and Client Lifecycle

Install the SDK through Go modules with `go get github.com/github/copilot-sdk/go`. Import it as `import "github.com/github/copilot-sdk/go"`, initialize with `copilot.NewClient(nil)` for defaults, start with `client.Start()`, and stop with `defer client.Stop()`. Use `ForceStop()` only when `Stop()` takes too long and the process must be terminated.

Configure `copilot.ClientOptions` when defaults are insufficient:

| Option | Convention |
| --- | --- |
| `CLIPath` | Set the CLI executable path when `copilot` is not discoverable from `PATH`. |
| `CLIUrl` | Point to an existing CLI server such as `localhost:8080`; when set, the client should not spawn a process. |
| `Port` | Use `0` for a random port unless a fixed port is required. |
| `UseStdio` | Prefer the default stdio transport (`true`) unless TCP is required. |
| `LogLevel` | Use the project logging convention; SDK default is `info`. |
| `AutoStart` | Use a pointer such as `boolPtr(true)` or `&autoStart`; set false for explicit server control. |
| `AutoRestart` | Use a pointer such as `boolPtr(true)` when crash recovery is desired. |
| `Cwd` | Set the working directory for the CLI process when session context depends on it. |
| `Env` | Pass CLI environment overrides as `[]string`; do not embed secrets in source. |

For manual server control, create `autoStart := false`, pass `&copilot.ClientOptions{AutoStart: &autoStart}`, call `client.Start()`, use the client, then call `client.Stop()`.

## Session Configuration and Permissions

Create sessions with `client.CreateSession(&copilot.SessionConfig{...})`, and resume with `client.ResumeSession("session-id", &copilot.ResumeSessionConfig{OnPermissionRequest: copilot.PermissionHandler.ApproveAll})` or `client.ResumeSessionWithOptions("session-id", &copilot.ResumeSessionConfig{...})` when additional options are needed. Treat `OnPermissionRequest: copilot.PermissionHandler.ApproveAll` as an explicit example permission handler, not a universal security default; choose a narrower handler when the application needs policy enforcement.

Preserve these `copilot.SessionConfig` fields and meanings:

| Field | Use |
| --- | --- |
| `SessionID` | Provide a custom session identifier when the caller needs stable identity. |
| `Model` | Select a model such as `gpt-5` or `claude-sonnet-4.5`. |
| `Tools` | Expose custom `[]copilot.Tool` handlers to the CLI. |
| `SystemMessage` | Customize system message behavior with `*copilot.SystemMessageConfig`. |
| `AvailableTools` | Allowlist tool names with `[]string{"tool1", "tool2"}`. |
| `ExcludedTools` | Blocklist tool names with `[]string{"tool3"}`. |
| `Provider` | Configure BYOK with `*copilot.ProviderConfig`. |
| `Streaming` | Enable streaming response chunks with `true`. |
| `MCPServers` | Register MCP server configurations. |
| `CustomAgents` | Register custom agent configurations. |
| `ConfigDir` | Override the CLI config directory. |
| `SkillDirectories` | Provide extra skill directories as `[]string`. |
| `DisabledSkills` | Disable skills by name as `[]string`. |

Use `session.SessionID` to read the session identifier. Send messages with `session.Send(copilot.MessageOptions{Prompt: "...", Attachments: []copilot.Attachment{...}})`, synchronous waits with `session.SendAndWait(options, timeout)`, cancellation with `session.Abort()`, history retrieval with `session.GetMessages()`, and cleanup with `session.Destroy()`.

## Event Handling and Streaming

Always use channels or another done signal to wait for session completion. Register handlers with `unsubscribe := session.On(func(evt copilot.SessionEvent) { ... })`, `defer unsubscribe()`, and close a `done := make(chan struct{})` channel on `copilot.SessionIdle`. Check pointer fields such as `evt.Data.Content`, `evt.Data.DeltaContent`, and `evt.Data.Message` for `nil` before dereferencing.

Handle events with type switches over `evt.Type`:

| Event type | Convention |
| --- | --- |
| `copilot.UserMessage` | Observe user messages when needed for logs or UI. |
| `copilot.AssistantMessage` | Read final assistant content from `evt.Data.Content`. |
| `copilot.AssistantMessageDelta` | Read incremental response chunks from `evt.Data.DeltaContent` when streaming. |
| `copilot.AssistantReasoning` | Read final reasoning content from `evt.Data.Content` only when the app intentionally displays or records it. |
| `copilot.AssistantReasoningDelta` | Read incremental reasoning chunks from `evt.Data.DeltaContent` only when appropriate for the UX. |
| `copilot.ToolExecutionStart` | Mark a tool invocation as started. |
| `copilot.ToolExecutionComplete` | Mark a tool invocation as completed. |
| `copilot.SessionStart` | Mark a session as started. |
| `copilot.SessionIdle` | Close the done channel or otherwise release waiters. |
| `copilot.SessionError` | Read `evt.Data.Message` and surface the runtime error. |

Enable streaming by setting `Streaming: true` in `copilot.SessionConfig`. Handle both delta events and final events because final `AssistantMessage` and `AssistantReasoning` events are always sent regardless of the streaming setting.

## Custom Tools and Tool Results

Define custom tools with `copilot.Tool{Name, Description, Parameters, Handler}`. Keep `Name` and `Description` descriptive, define JSON-schema-like `Parameters` with `type`, `properties`, and `required`, and assert `inv.Arguments` carefully before use. Return `copilot.ToolResult` with these fields:

| Field | Convention |
| --- | --- |
| `TextResultForLLM` | Provide the result text visible to the model, often plain text or JSON from `json.Marshal`. |
| `ResultType` | Use `success` or `failure`. |
| `Error` | Set internal error text when the tool fails and the LLM should not see raw details. |
| `ToolTelemetry` | Include non-sensitive telemetry in `map[string]interface{}{}`. |

The client runs the handler, converts the `ToolResult`, and responds to the CLI. Keep handlers bounded, deterministic, and safe for concurrent sessions. Example tool names and argument names such as `lookup_issue`, `id`, `get_user`, `user_id`, and fields such as `UserInfo`, `ID`, `Name`, `Email`, and `Role` should remain clear data contracts rather than placeholders when used in real code.

## System Messages, Attachments, and Message Modes

Customize system messages with `copilot.SystemMessageConfig`. Prefer `Mode: "append"` because it preserves guardrails while adding application workflow rules such as `<workflow_rules>`. Use `Mode: "replace"` only when the application explicitly needs full control and accepts that default guardrails are removed.

Attach files with `copilot.Attachment{Type: "file", Path: "/path/to/file.go", DisplayName: "My File"}` inside `copilot.MessageOptions{Prompt: "Analyze this file", Attachments: []copilot.Attachment{...}}`. Do not attach paths the application is not authorized to read.

Use `MessageOptions.Mode` deliberately: `"enqueue"` queues a message for processing, and `"immediate"` requests immediate processing. Keep multi-turn helpers explicit: send with `session.Send(copilot.MessageOptions{Prompt: prompt})`, wait for `SessionIdle`, capture `SessionError`, and unsubscribe after each bounded wait.

## Providers, Multiple Sessions, Connectivity, and Cleanup

Run independent sessions concurrently only when the application can manage their lifecycles. Sessions created with `session1, _ := client.CreateSession(...)` and `session2, _ := client.CreateSession(...)` are independent and may target different models such as `gpt-5` and `claude-sonnet-4.5`. Avoid ignoring errors in production even when examples use `_` for brevity.

Configure BYOK providers with `copilot.ProviderConfig{Type: "openai", BaseURL: "https://api.openai.com/v1", APIKey: "your-api-key"}` only through secure configuration. Never commit real API keys. Check connection state with `client.GetState()`, which returns `disconnected`, `connecting`, `connected`, or `error`. Test connectivity with `client.Ping("test message")` and inspect `resp.Timestamp` when successful.

Always pair client and session creation with cleanup. Use `defer client.Stop()` after successful `Start()` and `defer session.Destroy()` after successful session creation. If manual cleanup is required, call `session.Destroy()`, then `errors := client.Stop()`, and log each cleanup error with `log.Printf("Cleanup error: %v", err)`.

## SDK API Names and Struct Tags

Keep SDK API names exact when refactoring Go examples: `Attachment`, `MessageOptions`, `session.Abort()`, `session.GetMessages()`, `session.SendAndWait(options, timeout)`, `events/messages`, `ToolInvocation`, and `defer`. Preserve JSON tags such as `json:"id"`, `json:"name"`, `json:"email"`, and `json:"role"` on struct fields that serialize tool results. Treat `ALWAYS` from older examples as emphasis only; write new prose in direct imperative voice. Mention `model-dependent` reasoning chunks only when a selected model can emit them, and prefer SDK `built-in` helpers such as `SendAndWait` where they simplify waiting.

## Error Handling Patterns

Check every SDK-returned error. Use `log.Fatalf("Failed to create session: %v", err)` or return wrapped errors from libraries rather than continuing after failed client or session setup. Handle `session.Send` failures immediately, monitor `copilot.SessionError` events for runtime failures, and propagate event errors from helper functions after `<-done`.

Use `fmt.Fprintf(os.Stderr, "Session Error: %s\n", *evt.Data.Message)` only after verifying `evt.Data.Message != nil`. Avoid `fmt.Errorf(*evt.Data.Message)` with dynamic strings in new code; prefer `fmt.Errorf("session error: %s", *evt.Data.Message)` so formatting directives inside model-supplied text are not interpreted.

## Good / Bad Examples

The examples below illustrate safe lifecycle management, event waiting, nil checks, and cleanup.

**Good:**

```go
client := copilot.NewClient(nil)
if err := client.Start(); err != nil {
    log.Fatal(err)
}
defer client.Stop()

session, err := client.CreateSession(&copilot.SessionConfig{
    OnPermissionRequest: copilot.PermissionHandler.ApproveAll,
    Model:               "gpt-5",
    Streaming:           true,
})
if err != nil {
    log.Fatal(err)
}
defer session.Destroy()

done := make(chan struct{})
unsubscribe := session.On(func(evt copilot.SessionEvent) {
    switch evt.Type {
    case copilot.AssistantMessageDelta:
        if evt.Data.DeltaContent != nil {
            fmt.Print(*evt.Data.DeltaContent)
        }
    case copilot.SessionError:
        if evt.Data.Message != nil {
            fmt.Fprintf(os.Stderr, "Session Error: %s\n", *evt.Data.Message)
        }
    case copilot.SessionIdle:
        close(done)
    }
})
defer unsubscribe()

if _, err := session.Send(copilot.MessageOptions{Prompt: "What is 2+2?", Mode: "enqueue"}); err != nil {
    log.Printf("Failed to send: %v", err)
}
<-done
```

Why: The code starts and stops the client, destroys the session, subscribes and unsubscribes from events, checks nil event data, handles streaming and errors, and waits for `SessionIdle`.

**Bad:**

```go
client := copilot.NewClient(nil)
client.Start()
session, _ := client.CreateSession(&copilot.SessionConfig{Model: "gpt-5"})
session.Send(copilot.MessageOptions{Prompt: "Hello"})
```

Why: Errors are ignored, no permission handler or lifecycle cleanup is defined, there is no event subscription, and the program can exit before the session reaches idle.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use Go modules and require Go `1.21` or later for `github.com/github/copilot-sdk/go`. | The SDK contract depends on modern Go and module resolution. |
| Start clients explicitly and stop them with `defer client.Stop()`. | CLI server processes and transports do not leak. |
| Destroy every created session with `defer session.Destroy()`. | Session resources are released even when later work fails. |
| Configure `ClientOptions` and `SessionConfig` fields by name. | SDK behavior stays readable as preview APIs evolve. |
| Use channels or done signals and wait for `copilot.SessionIdle`. | Asynchronous event processing completes before callers proceed. |
| Call unsubscribe functions returned by `On()`. | Event handlers do not accumulate across turns or sessions. |
| Check pointer fields in `SessionEvent` data before dereferencing. | Event payloads can omit `Content`, `DeltaContent`, or `Message`. |
| Handle both delta and final events when `Streaming` is enabled. | UI and logs receive incremental feedback without losing final content. |
| Return `ToolResult` with `TextResultForLLM`, `ResultType`, optional `Error`, and `ToolTelemetry`. | Tool responses stay compatible with the CLI and understandable to the model. |
| Prefer `SystemMessageConfig` `Mode: "append"`; use `replace` only with explicit safety acceptance. | Default guardrails remain active unless intentionally replaced. |
| Keep provider keys, CLI environment values, and attachment paths secure. | SDK integrations can otherwise leak credentials or local files. |
| Test connectivity with `Ping` and inspect `GetState()` before diagnosing higher-level failures. | Transport issues are separated from session or model behavior. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Run `go get github.com/github/copilot-sdk/go` for installation. | Vendor or copy SDK code into the application manually. |
| Use `copilot.NewClient(nil)` for defaults. | Recreate client setup logic without `ClientOptions`. |
| Set `AutoStart` and `AutoRestart` with bool pointers when overriding defaults. | Pass plain bool values where the SDK expects pointers. |
| Use `CreateSession`, `ResumeSession`, or `ResumeSessionWithOptions` with explicit config structs. | Hide session policy in positional or unreviewable helpers. |
| Use `SendAndWait` for simple synchronous interactions. | Reimplement synchronous waiting incorrectly for every call. |
| Use `session.On` with type switches. | Poll `GetMessages()` as the primary event mechanism. |
| Use `AvailableTools` and `ExcludedTools` to shape tool access. | Expose every possible tool by default. |
| Use `ProviderConfig` with secure runtime configuration. | Commit an `APIKey` literal for `https://api.openai.com/v1`. |
| Use `Mode: "enqueue"` or `Mode: "immediate"` intentionally. | Leave message delivery behavior ambiguous in multi-turn flows. |
| Log or return SDK errors with context. | Ignore errors from `Start`, `CreateSession`, `Send`, `Ping`, `Destroy`, or `Stop`. |

## Checklist Before Opening a PR

- [ ] Go code imports `github.com/github/copilot-sdk/go` through Go modules and remains compatible with Go `1.21` or later.
- [ ] `CopilotClient` setup uses `copilot.NewClient`, named `ClientOptions` when needed, `Start()`, and `Stop()` or `ForceStop()` cleanup.
- [ ] Sessions use named `SessionConfig` or `ResumeSessionConfig` fields, including an intentional `OnPermissionRequest` policy.
- [ ] Message sends use `copilot.MessageOptions` with explicit `Prompt`, optional `Attachments`, and intentional `Mode` when queuing matters.
- [ ] Event handlers use `session.On`, type switches, nil checks, unsubscribe functions, and a done signal closed on `SessionIdle`.
- [ ] Streaming sessions handle `AssistantMessageDelta`, `AssistantReasoningDelta`, `AssistantMessage`, and `AssistantReasoning` as appropriate.
- [ ] Custom tools define descriptive `Name`, `Description`, `Parameters`, safe `Handler` logic, and complete `ToolResult` fields.
- [ ] System message customization uses `append` unless replacing guardrails is a reviewed requirement.
- [ ] BYOK provider configuration, `Env`, and attachments do not commit secrets or unauthorized paths.
- [ ] Connectivity and lifecycle errors from `Ping`, `GetState`, `Start`, `CreateSession`, `Send`, `Destroy`, and `Stop` are handled.

## References

- OpenAI-compatible provider base URL example: https://api.openai.com/v1
