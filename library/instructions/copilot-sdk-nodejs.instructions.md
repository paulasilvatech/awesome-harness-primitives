---
applyTo: "**/*.ts,**/*.js,**/package.json"
description: "Conventions for building Node.js and TypeScript applications with the GitHub Copilot SDK, including client setup, sessions, permissions, tools, streaming, lifecycle, and error handling."
name: "GitHub Copilot SDK Node.js Instructions"
---

# GitHub Copilot SDK Node.js Conventions — Client Sessions and Tools

These instructions apply to Node.js and TypeScript code that imports `@github/copilot-sdk` or configures package manifests for Copilot SDK applications. They are authoritative for SDK installation, `CopilotClient` lifecycle, `SessionConfig`, event handling, custom tools, streaming, system messages, BYOK providers, attachments, session management, and cleanup in matched files; stricter security, secret-management, test, or repository-specific runtime instructions win when they define a narrower rule.

## Runtime and Package Baseline

The GitHub Copilot SDK is in technical preview, so write integration code that expects breaking changes and isolates SDK usage behind small application adapters.

| Concern | Convention |
| --- | --- |
| Runtime | Require Node.js 18.0 or later. |
| CLI dependency | Require GitHub Copilot CLI installed and available in `PATH`, unless `cliPath` or `cliUrl` points elsewhere. |
| Language | Prefer TypeScript because the SDK provides full TypeScript type definitions. |
| Async model | Use `async`/`await` and Promises throughout; never block on SDK operations. |
| Package installation | Add `@github/copilot-sdk` with the package manager already used by the project. |

Use one of these commands when the dependency is missing from `package.json`: `npm install @github/copilot-sdk`, `pnpm add @github/copilot-sdk`, or `yarn add @github/copilot-sdk`.

## Client Initialization and Server Control

Create one `CopilotClient` per process boundary or explicit workflow, start it before creating sessions, and stop it in a `finally` block.

```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();
try {
  const session = await client.createSession({ onPermissionRequest: approveAll });
  await session.send({ prompt: "Hello" });
} finally {
  await client.stop();
}
```

Use `CopilotClientOptions` deliberately instead of scattering process assumptions through the application.

| Option | Use |
| --- | --- |
| `cliPath` | Set the path to the CLI executable when `copilot` is not resolved from `PATH`. |
| `cliArgs` | Prepend extra CLI arguments before SDK-managed flags. |
| `cliUrl` | Connect to an existing CLI server such as `localhost:8080`; when provided, the client does not spawn a process. |
| `port` | Choose the server port; use `0` for a random port. |
| `useStdio` | Prefer stdio transport unless TCP is required. |
| `logLevel` | Set logging intentionally; default is `debug`. |
| `autoStart` | Disable only when manual `client.start()` control is required. |
| `autoRestart` | Keep enabled unless crash loops must fail fast. |
| `cwd` | Set the CLI working directory; default is `process.cwd()`. |
| `env` | Pass the CLI environment; default is `process.env`. |

For manual server control, use `new CopilotClient({ autoStart: false })`, call `client.start()`, and call `client.stop()`. Use `forceStop()` only when `stop()` takes too long and normal shutdown has failed.

## Session Configuration and Operations

Create and resume sessions through the client; keep each session independent so concurrent work does not share mutable state accidentally.

| `SessionConfig` member | Convention |
| --- | --- |
| `sessionId` | Provide only when resuming or binding to an externally tracked session. |
| `model` | Set explicitly when behavior depends on a model, for example `gpt-5` or `claude-sonnet-4.5`. |
| `tools` | Pass custom `Tool[]` definitions created with `defineTool`. |
| `systemMessage` | Prefer append mode so SDK and CLI guardrails remain intact. |
| `availableTools` | Use as an allowlist of tool names. |
| `excludedTools` | Use as a blocklist of tool names. |
| `provider` | Use for BYOK through `ProviderConfig`. |
| `streaming` | Enable for interactive experiences that should show incremental output. |
| `mcpServers` | Pass `MCPServerConfig[]` when the session needs MCP servers. |
| `customAgents` | Pass `CustomAgentConfig[]` when the session needs custom agents. |
| `configDir` | Override configuration directory only for isolated test or embedded scenarios. |
| `skillDirectories` | Add skill directories intentionally. |
| `disabledSkills` | Disable skills explicitly when a scenario must suppress them. |
| `onPermissionRequest` | Always provide a `PermissionHandler`; do not rely on implicit approval behavior. |

Use `client.createSession({ ... })` for new sessions and `client.resumeSession("session-id", { tools: [myNewTool], onPermissionRequest: approveAll })` for existing sessions. Use `session.sessionId` for the identifier, `session.send({ prompt: "...", attachments: [...] })` for messages, `session.sendAndWait({ prompt: "..." }, timeout)` for synchronous request/response flows, `session.abort()` to cancel current processing, `session.getMessages()` to retrieve `SessionEvent[]`, and `session.destroy()` for cleanup.

## Event Handling and Streaming

Register event handlers before sending the message they observe, unsubscribe when the wait condition is met, and resolve work from `session.idle` rather than sleeping.

```typescript
await new Promise<void>((resolve, reject) => {
  const unsubscribe = session.on((event) => {
    if (event.type === "assistant.message") {
      console.log(event.data.content);
    } else if (event.type === "session.idle") {
      unsubscribe();
      resolve();
    } else if (event.type === "session.error") {
      unsubscribe();
      reject(new Error(event.data.message));
    }
  });

  session.send({ prompt: "What is 2+2?" });
});
```

Handle SDK events as discriminated unions with `switch` or type guards. Recognized event names include `user.message`, `assistant.message`, `assistant.message_delta`, `assistant.reasoning`, `assistant.reasoning_delta`, `tool.executionStart`, `tool.executionComplete`, `session.start`, `session.idle`, and `session.error`. When `streaming: true` is enabled, process delta events for progress and still handle final `assistant.message` and `assistant.reasoning` events because final events are always sent regardless of streaming.

## Custom Tools and Tool Results

Define tools with `defineTool` so names, parameter schemas, and handlers stay type-safe. Use JSON Schema objects or Zod schemas for parameters, and return JSON-serializable values unless the handler needs a full `ToolResultObject`.

```typescript
import { defineTool } from "@github/copilot-sdk";
import { z } from "zod";

const tool = defineTool({
  name: "get_weather",
  description: "Get weather for a location",
  parameters: z.object({
    location: z.string().describe("City name"),
    units: z.enum(["celsius", "fahrenheit"]).optional(),
  }),
  handler: async (args) => ({ temperature: 72, units: args.units || "fahrenheit" }),
});
```

A `ToolResultObject` may contain `textResultForLlm`, `resultType: "success" | "failure"`, `error`, and `toolTelemetry`. Keep internal error details in `error`; expose only the LLM-safe result text through `textResultForLlm`. The client automatically runs the handler, serializes the return value, and responds to the CLI.

## System Messages, Attachments, Delivery Modes, and Providers

Use `systemMessage.mode: "append"` by default because it preserves safety guardrails. Use `mode: "replace"` only when the application intentionally takes full control over instructions and accepts the risk of removing guardrails.

| Feature | Convention |
| --- | --- |
| System append | Set `systemMessage: { mode: "append", content: "..." }` for workflow-specific additions. |
| System replace | Set `systemMessage: { mode: "replace", content: "..." }` only for controlled applications. |
| File attachments | Send `{ type: "file", path: "/path/to/file.ts", displayName: "My File" }` in `attachments`. |
| Message delivery | Use `mode: "enqueue"` to queue and `mode: "immediate"` to process immediately. |
| Multiple sessions | Run independent sessions concurrently with `Promise.all` only when shared resources are safe. |
| BYOK | Configure `provider` with `type`, `baseUrl`, and `apiKey`; the common OpenAI base URL shape is `https://api.openai.com/v1`. |

Never hard-code real API keys. Treat `apiKey: "your-api-key"` as a placeholder and load actual credentials from the approved secret source for the project.

## Session Lifecycle, Connectivity, and Cleanup

Use the client session-management APIs instead of maintaining parallel registries: `client.listSessions()`, `client.deleteSession(sessionId)`, `client.getLastSessionId()`, `client.resumeSession(lastId, { onPermissionRequest: approveAll })`, and `client.getState()`. Expected client states are `"disconnected"`, `"connecting"`, `"connected"`, and `"error"`. Use `client.ping("health check")` to verify server connectivity and inspect `response.timestamp` only for diagnostics.

Always pair clients and sessions with cleanup:

```typescript
async function withClient<T>(fn: (client: CopilotClient) => Promise<T>): Promise<T> {
  const client = new CopilotClient();
  try {
    await client.start();
    return await fn(client);
  } finally {
    await client.stop();
  }
}

async function withSession<T>(
  client: CopilotClient,
  fn: (session: CopilotSession) => Promise<T>,
): Promise<T> {
  const session = await client.createSession({ onPermissionRequest: approveAll });
  try {
    return await fn(session);
  } finally {
    await session.destroy();
  }
}
```

## Error Handling and TypeScript Safety

Catch errors around `client.createSession`, `session.send`, and helper functions, and monitor `session.error` for runtime failures after a send succeeds. In TypeScript, import `SessionEvent` and `AssistantMessageEvent` when handlers need explicit narrowing, and use helpers such as `waitForEvent<T extends SessionEvent["type"]>(session, eventType)` when repeated event waits would otherwise duplicate logic.

## Identifier Inventory

Keep these SDK names, event names, command names, placeholders, and configuration keys visible when refactoring examples: `AccountStatus`, `AssistantMessageEvent`, `BYOK`, `CopilotClient`, `CopilotClientOptions`, `CopilotSession`, `CustomAgentConfig`, `DataverseConfig`, `MCPServerConfig`, `PATH`, `PermissionHandler`, `Promise`, `ProviderConfig`, `SessionConfig`, `SessionEvent`, `Tool`, `ToolResultObject`, `UserInfo`, `Zod`, `approveAll`, `apiKey`, `attachments`, `autoRestart`, `autoStart`, `availableTools`, `baseUrl`, `cliArgs`, `cliPath`, `cliUrl`, `configDir`, `cwd`, `defineTool`, `disabledSkills`, `displayName`, `env`, `excludedTools`, `forceStop`, `getLastSessionId`, `getMessages`, `getState`, `listSessions`, `logLevel`, `mcpServers`, `model`, `mode`, `onPermissionRequest`, `ping`, `port`, `provider`, `resumeSession`, `sendAndWait`, `sessionId`, `skillDirectories`, `streaming`, `systemMessage`, `toolTelemetry`, `tools`, `useStdio`, `withClient`, and `withSession`.

Additional preserved vocabulary from the baseline: `"enqueue"`, `"immediate"`, `${metadata.sessionId}: ${metadata.summary}`, `ALWAYS`, `Error: ${error.message}`, `Error: ${event.data.message}`, `Server responded at ${new Date(response.timestamp)}`, `Session Error: ${event.data.message}`, `Total length: ${event.data.content.length} chars`, `async/await`, `await session.abort()`, `await session.destroy()`, `await session.getMessages()`, `await session.send({ prompt: "...", attachments: [...] })`, `await session.sendAndWait({ prompt: "..." }, timeout)`, `built-in`, `compile-time`, `events/messages`, `get_user`, `lookup_issue`, `model-dependent`, `npm/pnpm/yarn`, `on()`, `session.sessionId`, `try-finally`, `workflow_rules`, `SendAndWait`, `SystemMessageConfig`.

## Good / Bad Examples

The examples below illustrate safe lifecycle handling, event waiting, and cleanup.

**Good:**

```typescript
await withClient(async (client) => {
  await withSession(client, async (session) => {
    const response = await session.sendAndWait({ prompt: "What is 2+2?" }, 60000);
    if (response) console.log(response.data.content);
  });
});
```

Why: The client and session are cleaned up, the request waits through the SDK API, and the code avoids leaked subscriptions.

**Bad:**

```typescript
const client = new CopilotClient();
const session = await client.createSession({ onPermissionRequest: approveAll });
session.on((event) => console.log(event.type));
session.send({ prompt: "risky operation" });
```

Why: The client is not explicitly started or stopped, the session is never destroyed, the subscription is never disposed, and errors are ignored.

## Conventions

| Rule | Rationale |
| --- | --- |
| Require Node.js 18.0 or later and install `@github/copilot-sdk` through the project package manager | Runtime and dependency assumptions stay explicit. |
| Start `CopilotClient` before session use and stop it in `finally` | CLI processes and transports do not leak. |
| Provide `onPermissionRequest` and configure `availableTools` or `excludedTools` intentionally | Tool access remains explicit and reviewable. |
| Use Promises, `session.idle`, and `session.error` for event-driven waits | Code avoids sleeps, missed events, and silent failures. |
| Use `streaming: true` only when incremental output improves UX and still handle final events | Streaming code remains correct in both delta and non-delta modes. |
| Define custom tools with `defineTool` and JSON Schema or Zod parameters | Tool contracts are validated and type-safe. |
| Prefer `systemMessage.mode: "append"` | Safety guardrails remain in place. |
| Destroy sessions and unsubscribe handlers when work completes | Long-running applications avoid memory leaks and duplicate handlers. |
| Keep API keys out of source code | BYOK integrations do not expose credentials. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `npm install @github/copilot-sdk`, `pnpm add @github/copilot-sdk`, or `yarn add @github/copilot-sdk` | Vendor SDK files manually or assume the package exists. |
| Configure `CopilotClientOptions` such as `cliPath`, `cliUrl`, `cwd`, and `env` where runtime assumptions matter | Hard-code process behavior in scattered call sites. |
| Use `createSession`, `resumeSession`, `send`, `sendAndWait`, `abort`, `getMessages`, and `destroy` through the SDK | Track session state with unrelated custom protocols. |
| Register event handlers before `session.send` and dispose the returned unsubscribe function | Leave permanent listeners for one-shot waits. |
| Return JSON-serializable tool results or a deliberate `ToolResultObject` | Return process-local objects that cannot serialize. |
| Use `client.ping("health check")` and `client.getState()` for diagnostics | Infer connectivity from arbitrary timeouts. |
| Load `provider.apiKey` from approved secrets | Commit real BYOK credentials. |

## Checklist Before Opening a PR

- [ ] `@github/copilot-sdk` is declared in the package manifest when SDK imports are introduced.
- [ ] Runtime assumptions mention Node.js 18.0 or later and the GitHub Copilot CLI path or server URL.
- [ ] Every `CopilotClient` is started, stopped, and guarded by `try`/`finally` or equivalent cleanup helpers.
- [ ] Every session is destroyed or intentionally resumed by `sessionId`.
- [ ] Event waits handle `assistant.message`, `session.idle`, and `session.error` without sleeps.
- [ ] Streaming code handles `assistant.message_delta`, `assistant.reasoning_delta`, and final message or reasoning events when enabled.
- [ ] Custom tools use `defineTool` with JSON Schema or Zod parameters and serializable results.
- [ ] System-message replacement is justified; append mode is used otherwise.
- [ ] Attachments, delivery `mode`, MCP servers, custom agents, skills, and tool allowlists are configured explicitly when used.
- [ ] No API keys, tokens, or secrets are committed.
