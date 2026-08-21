---
applyTo: "**/*.cs,**/host.json,**/local.settings.json,**/*.csproj"
description: "Enforces Azure Durable Functions C# isolated-worker conventions for deterministic orchestrators, activities, entities, configuration, storage, observability, reliability, and testing."
---

# Azure Durable Functions C# Conventions — Isolated Worker Orchestrations

These instructions apply to C# Azure Durable Functions code, `host.json`, `local.settings.json`, and project files. They are authoritative for isolated worker Durable Task usage, deterministic orchestrators, activity boundaries, entities, configuration, retries, timers, instance management, observability, storage, and tests; project-specific Azure, security, or deployment primitives win when they define stricter environment, identity, or release requirements.

## Project Model and Structure

Use the isolated worker model with `Microsoft.Azure.Functions.Worker.Extensions.DurableTask` for new projects. Use `Microsoft.DurableTask` namespaces and types such as `TaskOrchestrationContext` and `TaskActivityContext`. Register support in `Program.cs` with `builder.Services.AddDurableTaskClient()` and `builder.ConfigureFunctionsWorkerDefaults(x => x.UseDurableTask())`.

Separate orchestrators, activities, entities, and starter functions into distinct classes or files. Organize by feature folders such as `/Orchestrations/OrderProcessing/`, not by function type. Name orchestrators with `Orchestrator`, activities with `Activity`, and entities with `Entity`. Use constants or static readonly strings for names passed to `CallActivityAsync`, `CallSubOrchestratorAsync`, and `GetEntityStateAsync`.

## Deterministic Orchestrators and Activities

Orchestrators coordinate and activities do work. Orchestrator code must be deterministic and replay-safe: do not use `DateTime.Now`, `DateTime.UtcNow`, `Guid.NewGuid()`, `Random`, direct HTTP calls, non-deterministic I/O, `Task.Delay`, or `Thread.Sleep` inside orchestrators. Use `context.CurrentUtcDateTime`, `context.CreateTimer`, and `context.CreateReplaySafeLogger(nameof(OrchestratorName))`. Do not inject `ILogger<T>` directly into orchestrators because replay duplicates logs. Use `async Task` or `async Task<T>`, never `async void`.

Activities perform I/O such as database reads/writes, HTTP calls, and queue sends. Keep them focused, idempotent when possible, serializable in inputs/outputs, and free of domain entities with navigation properties. Inject `IRepository`, `IHttpClientFactory`, and other services through constructor DI, not `[FromServices]` inside methods. Activities use `TaskActivityContext` and injected `ILogger<T>`.

## Configuration and Storage

`local.settings.json` needs `AzureWebJobsStorage` for Durable Functions state, `FUNCTIONS_WORKER_RUNTIME` set to `dotnet-isolated`, and local storage such as `UseDevelopmentStorage=true` or Azurite. Never commit real `local.settings.json`; commit `local.settings.json.example` with placeholders. Use Azure Key Vault references such as `@Microsoft.KeyVault(...)` for sensitive values when needed. Netherite or MSSQL providers need provider connection strings such as `EventHubsConnection`.

Configure Durable settings under `extensions.durableTask` in `host.json`. Set `hubName` to an environment-specific value such as `MyAppProd`, `MyAppDev`, or `MyTaskHub`. Tune `maxConcurrentActivityFunctions`, `maxConcurrentOrchestratorFunctions`, and `maxQueuePollingInterval`. Enable `extendedSessionsEnabled` on Premium or Dedicated plans for long-running orchestrations when replay overhead matters. Configure `storageProvider` with `type` `netherite` or `mssql` for high-scale scenarios. Configure Application Insights sampling under `logging.applicationInsights.samplingSettings`.

Use separate storage accounts or Task Hub names per environment. Avoid payloads greater than 64KB in orchestration inputs/outputs; store large data in Blob Storage and pass a URL or ID.

## Orchestration Patterns

Use sequential `await context.CallActivityAsync<T>(nameof(ActivityName), input)` for function chaining. For fan-out/fan-in, collect `List<Task<T>>`, cap parallelism with batching, and await `Task.WhenAll(tasks)`. For HTTP API and human interaction flows, call `client.ScheduleNewOrchestrationInstanceAsync`, return `await client.CreateCheckStatusResponseAsync(req, instanceId)`, use `context.WaitForExternalEvent<T>("EventName", timeout)`, race it with `context.CreateTimer(deadline, CancellationToken)`, `Task.WhenAny`, and cancel the timer with a `CancellationTokenSource` when the event wins.

For monitoring and polling, use a `while` loop with `context.CreateTimer(context.CurrentUtcDateTime.Add(interval), CancellationToken.None)` and a clear exit condition. For eternal workflows, use `context.ContinueAsNew(newInput)` to reset history and drain pending external events before `ContinueAsNew` when using `isKeepRunning` patterns. For sub-orchestrations, use `context.CallSubOrchestratorAsync<T>(nameof(SubOrchestrator), instanceId, input)`, provide explicit `instanceId` for correlation or idempotency, and avoid excessive nesting.

## Entities, Reliability, and Instance Management

Define entities with class-based syntax implementing `TaskEntity<TState>`. Access state only through entity operations and `entity.State`; never read or write entity storage directly. Use `context.Entities.CallEntityAsync<T>` when a return value is needed and `context.Entities.SignalEntityAsync` for fire-and-forget operations. Use entities for distributed counters, distributed locks, aggregators, and per-user or per-session state. Keep entity state small and serializable.

Handle `TaskFailedException` in orchestrators and call compensating activities for saga behavior. Use `RetryPolicy` via `new TaskOptions(new RetryPolicy(maxRetries, firstRetryInterval))` for transient failures. Fail fast and compensate for validation or authorization failures. Terminate unrecoverable stuck instances with Durable management APIs.

Use deterministic `instanceId` values such as `$"order-{orderId}"` when correlating to business entities. Check `client.GetInstanceMetadataAsync(instanceId)` before scheduling singleton workflows. Use `client.TerminateInstanceAsync`, `client.SuspendInstanceAsync`, `client.ResumeInstanceAsync`, `client.PurgeInstanceAsync`, and bulk purge to manage lifecycle and storage growth.

## Observability and Testing

Log `instanceId` in orchestrators and starters. Use Application Insights Durable Functions integration for lifecycle events, activity durations, failures, and health. Monitor with Durable Functions HTTP management API endpoints such as `/runtime/webhooks/durabletask/instances` or the Durable Functions Monitor VS Code extension. Control concurrency with `durableTask.maxConcurrentOrchestratorFunctions` and `durableTask.maxConcurrentActivityFunctions`.

Test activities as regular methods with mocked dependencies. Test orchestrator logic by mocking `context.CallActivityAsync`, `context.CreateTimer`, and `context.WaitForExternalEvent`, using `Microsoft.Azure.Functions.Worker.Extensions.DurableTask.Tests` if available. Do not test the Durable runtime's event sourcing or replay. Use Azurite or isolated Azure Storage for integration tests, deterministic test instance IDs such as `$"test-{Guid.NewGuid()}"`, `client.GetInstanceMetadataAsync`, `client.WaitForInstanceCompletionAsync`, `context.Entities.SignalEntityAsync`, and `client.ReadEntityStateAsync`. Force activity failures to verify compensation.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: ` NuGet package (if available) or manually mock ` `"MyAppDev"` `"MyAppProd"` `"UseDevelopmentStorage=true"` `"dotnet-isolated"` `"extendedSessionsEnabled": true` `"extensions": { "durableTask": { "hubName": "MyTaskHub" } }` `"extensions": { "durableTask": { ... } }` `"hubName"` `"maxConcurrentActivityFunctions"` `"maxConcurrentOrchestratorFunctions"` `"maxQueuePollingInterval"` `"mssql"` `"storageProvider": { "type": "netherite" }` `.gitignore` `CallEntityAsync` `CancellationTokenSource` `CartEntity` `ChargePaymentActivity` `List<Task<T>>` `Premium/Dedicated` `ProcessOrderOrchestrator` `SignalEntityAsync` `Task.WhenAll(tasks)` `Task.WhenAny(externalEventTask, timerTask)` `URL/ID` `activity/orchestrator/entity` `approval/callback` `await client.CreateCheckStatusResponseAsync(req, instanceId)` `client.ScheduleNewOrchestrationInstanceAsync` `compensation/error` `completed/failed` `context.ContinueAsNew(input)` `context.ContinueAsNew(newInput)` `context.CreateReplaySafeLogger(nameof(Orchestrator))` `context.CreateTimer(deadline, CancellationToken)` `context.CreateTimer(fireAt, CancellationToken)` `context.WaitForExternalEvent<T>("EventName", timeout)` `cross-environment` `dev/staging/prod` `end-to-end` `fail-fast` `feature-based` `high-throughput` `isKeepRunning` `long-lived` `mid-workflow` `per-user/per-session` `provider-specific` `retry/compensation` `self-resolve` `step-by-step` `sub-orchestration` `timer-triggered` `try/catch`.

## Good / Bad Examples

The examples below show replay-safe orchestration behavior.

**Good:**

```csharp
var logger = context.CreateReplaySafeLogger(nameof(ProcessOrderOrchestrator));
var deadline = context.CurrentUtcDateTime.AddMinutes(30);
await context.CreateTimer(deadline, CancellationToken.None);
```

Why: The code uses replay-safe logging, deterministic time, and durable timers.

**Bad:**

```csharp
_logger.LogInformation("Running");
await Task.Delay(TimeSpan.FromMinutes(30));
var id = Guid.NewGuid();
```

Why: Injected logging replays, `Task.Delay` is not durable, and `Guid.NewGuid()` is non-deterministic in orchestrators.

## Conventions

| Rule | Rationale |
|---|---|
| Use isolated worker Durable Task packages and `Microsoft.DurableTask` types | New C# projects should use the current worker model |
| Keep orchestrators deterministic and activities side-effectful | Replay correctness depends on deterministic orchestration history |
| Use replay-safe logging in orchestrators | Replays otherwise duplicate log entries |
| Configure Task Hub, concurrency, storage provider, and telemetry explicitly | Production defaults rarely match scale, cost, or isolation needs |
| Use durable timers, external events, `ContinueAsNew`, and sub-orchestrations intentionally | Long-running workflows need bounded history and durable waiting |
| Keep activities and entity state serializable and idempotent | Retries and replay can otherwise duplicate side effects or fail serialization |
| Test business logic, compensation, and integration paths without testing the runtime itself | Tests stay stable and focused on code you own |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `context.CurrentUtcDateTime` | Use `DateTime.UtcNow` or `DateTime.Now` inside orchestrators |
| Move HTTP calls and random values into activities | Call `HttpClient.GetAsync`, `Guid.NewGuid()`, or `Random` inside orchestrators |
| Use `context.CreateTimer` | Use `Task.Delay` or `Thread.Sleep` inside orchestrators |
| Use `RetryPolicy` for transient activity failures | Retry validation or authorization failures blindly |
| Store large payloads in Blob Storage and pass references | Put >64KB payloads in orchestration input/output |
| Use `ContinueAsNew` for eternal workflows | Let orchestration history grow without bound |

## Checklist Before Opening a PR

- [ ] Project uses isolated worker Durable Task packages, registration, and `Microsoft.DurableTask` namespaces.
- [ ] Orchestrators contain no non-deterministic time, GUID, random, direct I/O, HTTP, `Task.Delay`, or `Thread.Sleep` calls.
- [ ] Activities are focused, DI-backed, serializable, and idempotent where retries can occur.
- [ ] `host.json` and local settings define Task Hub, storage, runtime, concurrency, telemetry, and provider choices safely.
- [ ] Timers, external events, fan-out/fan-in, sub-orchestrations, entities, retries, and compensation are implemented with Durable APIs.
- [ ] Observability includes replay-safe logs, `instanceId`, Application Insights, management endpoints, and concurrency settings.
- [ ] Tests cover activities, orchestrator decisions, timeout branches, compensation, entities, and integration workflows where relevant.
