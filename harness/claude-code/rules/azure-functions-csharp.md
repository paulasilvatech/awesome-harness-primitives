---
paths:
  - "**/*.cs"
  - "**/host.json"
  - "**/local.settings.json"
  - "**/*.csproj"
---

<!-- Generated from harness/github-copilot/instructions/azure-functions-csharp.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Azure Functions C# isolated worker conventions for host setup, triggers, bindings, dependency injection, configuration, retries, observability, performance, security, and testing.

# Azure Functions C# Conventions — Isolated Worker Services

These instructions apply to C# Azure Functions projects and related `host.json`, `local.settings.json`, and project files. They are authoritative for new .NET 6-or-later isolated worker Functions, trigger and binding choices, dependency injection, configuration, retries, observability, performance, security, and testing; repository-wide C#, security, and Azure deployment instructions win where they define stricter rules. Use the isolated worker model for new functions and keep trigger methods thin by delegating business logic to DI-registered services.

## Worker Model, Host Setup, and Structure

- Always use the isolated worker model, not the legacy in-process model, for new Azure Functions targeting .NET 6 or later.
- Use `FunctionsApplication.CreateBuilder(args)` or `HostBuilder` in `Program.cs` for host setup and dependency injection.
- Decorate function methods with `[Function("FunctionName")]` and strongly typed trigger and binding attributes.
- Keep function methods focused on one trigger responsibility.
- Never put business logic directly in the function method body; extract it into testable service classes registered through DI.
- Use `ILogger<T>` injected through the constructor instead of `ILogger` function parameters.
- Use `async/await` for I/O-bound operations; never block with `.Result` or `.Wait()`.
- Prefer `CancellationToken` parameters where supported.
- Use `Microsoft.Azure.Functions.Worker` and `Microsoft.Azure.Functions.Worker.Extensions.*` NuGet packages.
- Group related functions by domain concern, not trigger type.

## Configuration, Identity, and Clients

- Register services in `Program.cs` with `builder.Services.Add*` extension methods.
- Store local configuration in `local.settings.json`; use Azure App Configuration or Application Settings in deployed environments.
- Never hardcode connection strings or secrets in code.
- Read configuration through `IConfiguration`, environment variables, `IOptions<T>`, or `IOptionsMonitor<T>`.
- Use Key Vault references such as `@Microsoft.KeyVault(SecretUri=...)` in App Settings for deployed secrets.
- Use Managed Identity (`Managed Identity`) with `DefaultAzureCredential` for Azure services; avoid key-based connection strings where possible.
- Register external clients such as `BlobServiceClient`, `ServiceBusClient`, and `CosmosClient` as singletons using `services.AddAzureClients()` from `Azure.Extensions.AspNetCore.Configuration.Secrets` and `DefaultAzureCredential`.
- Register `HttpClient` instances through `IHttpClientFactory`.
- Avoid `static` state; shared state belongs in DI-registered services.

## Triggers and Bindings

| Trigger or binding | Convention |
| --- | --- |
| `HttpTrigger` | Use `AuthorizationLevel.Function` or higher in production; reserve `AuthorizationLevel.Anonymous` for justified public APIs. Use ASP.NET Core integration with `UseMiddleware` and `IActionResult` returns when using that model. |
| `TimerTrigger` | Use NCRONTAB expressions such as `"0 */5 * * * *"`; avoid `RunOnStartup = true` in production. |
| `QueueTrigger` / `ServiceBusTrigger` | Configure `MaxConcurrentCalls`, dead-letter policies, and `MaxDeliveryCount`; use `ServiceBusReceivedMessage` for advanced complete, abandon, or dead-letter control. |
| `BlobTrigger` | Prefer Event Grid-based, not polling-based, blob triggers with `Microsoft.Azure.Functions.Worker.Extensions.EventGrid` over polling blob triggers. |
| `EventHubTrigger` | Use `cardinality` set to `many` for batch processing and `EventData[]` or `string[]` parameter types; rely on `EventHubTriggerAttribute` built-in checkpointing. |
| `CosmosDBTrigger` | Use change feed processing and configure `LeaseContainerName` with leases separated from data containers. |
| Input bindings | Use declarative reads when bindings cover the use case. |
| Multiple outputs | Define a custom return type with attributes such as `[QueueOutput]`, `[BlobOutput]`, and `[HttpResult]`. |
| Blob bindings | Use `[BlobInput]` and `[BlobOutput]` for read/write scenarios; prefer `Stream` over `byte[]` for large blobs. |
| Cosmos input | Use `[CosmosDBInput]` for point reads and simple queries; inject `CosmosClient` for complex queries. |
| Service Bus output | Use `[ServiceBusOutput]` for single sends and `ServiceBusSender` for batching or advanced sends. |

Choose either binding-based I/O or DI-injected SDK clients for the same resource; avoid mixing both patterns for one resource.

## Retry, Error Handling, and Observability

- Tune `host.json` per trigger type with `maxConcurrentCalls`, `batchSize`, and retry policies.
- Configure built-in retries in `host.json` using `"retry"` / `retry` with `fixedDelay` or `exponentialBackoff`.
- Use `Microsoft.Extensions.Http.Resilience` or Polly v8 `ResiliencePipeline` for code-level retry, circuit breaker, and timeout strategies.
- Catch specific exceptions, log structured context such as correlation ID and input identifier, then re-throwing, rethrow, or dead-lettering as appropriate.
- Use dead-letter queues for messages that fail after all retries.
- Never silently swallow exceptions in function handlers.
- For HTTP triggers, return `IActionResult` types such as `BadRequestObjectResult` and `NotFoundObjectResult` for expected errors.
- Configure Application Insights with `builder.Services.AddApplicationInsightsTelemetryWorkerService()` and `builder.Logging.AddApplicationInsights()`.
- Use `TelemetryClient` for custom events, metrics, and dependency tracking.
- Set log levels in `host.json` under `"logging"` / `logging` to control telemetry cost.
- Use `Activity` and `ActivitySource` from `System.Diagnostics` for distributed tracing.
- Avoid logging PII, secrets, connection strings, or sensitive request bodies.

## Performance, Security, and Testing

- Keep startup time minimal by deferring expensive initialization to lazy-loaded singletons, not constructors.
- Use Consumption for event-driven unpredictable workloads; use Premium or Dedicated for low-latency, low latency, high-throughput, high throughput, or VNet integration.
- For CPU-intensive work, use Durable Functions or other background processing rather than blocking the host thread.
- Batch where possible with `IEnumerable<EventData>` or `ServiceBusReceivedMessage[]`.
- Tune `FUNCTIONS_WORKER_PROCESS_COUNT` and `maxConcurrentCalls` for the plan and throughput.
- Enable `WEBSITE_RUN_FROM_PACKAGE=1` for faster cold starts from deployment packages.
- Validate and sanitize HTTP trigger inputs with FluentValidation or Data Annotations.
- Use `AuthorizationLevel.Function` with function keys in Key Vault for internal API-to-API calls.
- Put Azure API Management (APIM) in front of public-facing HTTP-triggered functions for auth, rate limiting, and routing.
- Restrict inbound access with IP restrictions and Private Endpoints for sensitive functions.
- Unit-test service classes independently of the host with xUnit/NUnit, xUnit, or NUnit and mocked dependencies.
- Integration-test functions with `Azurite`, `TestServer`, Azure Functions Core Tools, and `Microsoft.Azure.Functions.Worker.Testing` helpers where available.
- Focus tests on extracted business logic rather than trigger plumbing.

## Existing Code Review Guidance

- If a project uses legacy in-process APIs such as `FunctionsStartup` or `IWebJobsStartup`, recommend migration to the isolated worker model and the `dotnet-isolated-process-guide` migration path.
- If hardcoded connection strings or storage account keys appear in code or config, replace them with `DefaultAzureCredential` and Key Vault references.
- If `RunOnStartup = true` appears on a production `TimerTrigger`, flag it and prefer deployment slots or feature flags.
- If `async void` appears in a function, replace it with `async Task`.
- If retry logic uses `Thread.Sleep` or ad hoc `Task.Delay` in a function, replace it with host-level retry policies or Polly resilience pipelines.

## Good / Bad Examples

The examples below illustrate thin function methods and DI-based logic.

**Good:**

```csharp
[Function("ProcessOrder")]
public async Task RunAsync(
    [ServiceBusTrigger("orders")] ServiceBusReceivedMessage message,
    CancellationToken cancellationToken)
{
    await orderProcessor.ProcessAsync(message, cancellationToken);
}
```

Why: The trigger method is thin, asynchronous, cancellable, and delegates business behavior to an injected service.

**Bad:**

```csharp
[Function("ProcessOrder")]
public void Run([ServiceBusTrigger("orders")] string message)
{
    Thread.Sleep(1000);
    File.WriteAllText("secret.txt", message);
}
```

Why: The function blocks the host thread, mixes business and infrastructure logic, lacks DI, and risks leaking sensitive data.


- Use `Microsoft.Azure.Functions.Worker.Testing` to create mock `FunctionContext` instances; preserve the literal binding token ` in ` when comparing legacy text.

- Use structured logging calls such as `LogInformation` with properties such as `MessageId` when logging message processing.
## Conventions

| Rule | Rationale |
| --- | --- |
| Use isolated worker with `FunctionsApplication.CreateBuilder(args)` or `HostBuilder` | New .NET Functions avoid legacy in-process coupling |
| Keep functions thin and move business logic to DI services | Services can be tested without the Functions host |
| Use constructor-injected `ILogger<T>`, `IConfiguration`, `IOptions<T>`, and Azure clients | Dependencies stay structured and mockable |
| Prefer Managed Identity, `DefaultAzureCredential`, and Key Vault references | Secrets and keys do not live in code or config |
| Configure triggers, bindings, concurrency, `batchSize`, and retries in `host.json` | Runtime behavior is visible and centrally tuned |
| Use binding-based I/O or SDK clients consistently per resource | Mixed access patterns cause duplicated behavior and confusion |
| Use Application Insights, `TelemetryClient`, `Activity`, and `ActivitySource` without logging sensitive data | Operations teams get traceable telemetry without leaks |
| Tune `FUNCTIONS_WORKER_PROCESS_COUNT`, `maxConcurrentCalls`, and `WEBSITE_RUN_FROM_PACKAGE=1` deliberately | Scale and cold-start behavior match the hosting plan |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `[Function("FunctionName")]` with strongly typed trigger attributes | Use legacy `FunctionsStartup` or `IWebJobsStartup` for new projects |
| Return `BadRequestObjectResult` or `NotFoundObjectResult` for expected HTTP errors | Throw exceptions for normal validation outcomes |
| Use `Stream` for large blob bindings | Load large blobs into `byte[]` unnecessarily |
| Use `ServiceBusSender` for batching or advanced sends | Force complex send scenarios through single-message bindings |
| Dead-letter messages after retries fail | Swallow handler exceptions silently |
| Use APIM, IP restrictions, and Private Endpoints for sensitive HTTP functions | Expose public endpoints with unjustified `AuthorizationLevel.Anonymous` |
| Test services with xUnit or NUnit and integration-test with `Azurite` or Core Tools | Spend effort testing trigger plumbing instead of business logic |

## Checklist Before Opening a PR

- [ ] New functions use the isolated worker model with `Microsoft.Azure.Functions.Worker` packages.
- [ ] Host setup uses `FunctionsApplication.CreateBuilder(args)` or `HostBuilder` in `Program.cs`.
- [ ] Function methods use `[Function("FunctionName")]`, async `Task`, `CancellationToken` where supported, and no `.Result`, `.Wait()`, or `async void`.
- [ ] Business logic is extracted into DI-registered services with constructor-injected `ILogger<T>`.
- [ ] Secrets use Key Vault references, Managed Identity, and `DefaultAzureCredential`; no connection strings or keys are hardcoded.
- [ ] `host.json` configures trigger-level and trigger-specific concurrency, `batchSize`, logging, and retry policies.
- [ ] Trigger and binding choices match the data size, batching, and advanced-control requirements.
- [ ] Application Insights, structured logging, correlation, `Activity`, and sensitive-data exclusions are configured.
- [ ] Performance settings such as `FUNCTIONS_WORKER_PROCESS_COUNT`, `maxConcurrentCalls`, and `WEBSITE_RUN_FROM_PACKAGE=1` are justified.
- [ ] Security controls for HTTP triggers, APIM, Key Vault, IP restrictions, Private Endpoints, and validation are in place where needed.
- [ ] Unit or integration tests cover extracted behavior using xUnit, NUnit, `Azurite`, `TestServer`, Core Tools, or Worker testing helpers as appropriate.
