---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/build.gradle"
  - "**/build.gradle.kts"
---

<!-- Generated from harness/github-copilot/instructions/java-mcp-server.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Best practices and patterns for building Model Context Protocol (MCP) servers in Java using the official MCP Java SDK with reactive streams, transports, Spring integration, validation, observability, and tests.

# Java MCP Server Conventions — Reactive SDK Servers

These instructions apply to Java source files and Maven or Gradle build files that implement Model Context Protocol servers with the official MCP Java SDK. They are authoritative for SDK dependency declaration, server builders, tools, resources, prompts, reactive and synchronous APIs, transports, Spring Boot integration, JSON schema, logging, lifecycle, and tests in matched files; project-wide Java style, security, deployment, and dependency-management rules win where they set stricter versions or operational controls.

## Dependencies and Build Files

Declare the MCP SDK in the build tool already used by the project, and keep the SDK version reviewable.

| Build file | Convention |
| --- | --- |
| `pom.xml` | Add `io.modelcontextprotocol.sdk:mcp:0.14.1` inside `<dependencies>` for Maven projects. |
| `build.gradle` / `build.gradle.kts` | Add `implementation("io.modelcontextprotocol.sdk:mcp:0.14.1")` for Gradle projects. |
| Spring Boot starter | Use `io.modelcontextprotocol.sdk:mcp-spring-boot-starter:0.14.1` when the server is integrated through Spring. |
| Versioning | Do not mix SDK versions across direct SDK and Spring starter dependencies. |

## Server Construction and Capabilities

Create MCP servers with the builder pattern and declare only the capabilities the server actually implements.

| API | Convention |
| --- | --- |
| `McpServerBuilder.builder()` | Use the builder as the primary construction path. |
| `serverInfo("my-server", "1.0.0")` | Set a stable server name and semantic version visible to clients; Spring samples may use `spring-server` for the same purpose. |
| `capabilities(capabilities -> capabilities.tools(true).resources(true).prompts(true))` | Enable `tools`, `resources`, and `prompts` only when handlers exist. |
| `McpServer server = ...build()` | Keep server construction separate from transport startup so tests can reuse it. |
| `StdioServerTransport` | Use for local subprocess communication and CLI-launched servers. |
| `server.start(transport).subscribe()` | Subscribe only when the host owns asynchronous startup and shutdown separately. |
| `server.start(transport).block()` | Use blocking startup only in blocking entry points. |

## Tool Handlers

Register tools with explicit schemas, narrow names, and result objects. Validate inputs before performing side effects.

| API or element | Convention |
| --- | --- |
| `Tool.builder()` | Define every tool with `name`, `description`, and `inputSchema`. |
| `ResourceHandler` | Use resource handler abstractions where the SDK or framework exposes them. |
| `ToolHandler` | Use handler abstractions where the framework requires a named handler class. |
| `server.addToolHandler("search", arguments -> { ... })` | Register handlers by the same stable tool name clients see. |
| `JsonSchema.object()` | Use schema builders for parameters rather than accepting arbitrary JSON. |
| `property("query", JsonSchema.string().description("Search query").required(true))` | Mark required parameters explicitly. |
| `property("limit", JsonSchema.integer().description("Maximum results").defaultValue(10))` | Give optional parameters safe defaults. |
| `arguments.get("query").asText()` | Read validated values by name. |
| `arguments.has("limit") ? arguments.get("limit").asInt() : 10` | Preserve default behavior in handlers as well as schema. |
| `performSearch(query, limit)` | Keep business logic outside the protocol handler when it grows. |
| `ToolResponse.success().addTextContent(...).build()` | Return success responses through MCP content builders. |
| `ToolResponse.error().message(...).build()` | Return validation and operational errors as MCP errors, not thrown raw exceptions. |

## Resources and Prompts

Use resource handlers for addressable data and prompt handlers for templated conversations. Keep URIs, MIME types, and arguments explicit.

| Capability | Convention |
| --- | --- |
| `server.addResourceListHandler(...)` | Return a list of `Resource` objects such as `Resource.builder().name("Data File").uri("resource://data/example.txt").description("Example data file").mimeType("text/plain").build()`. |
| `server.addResourceReadHandler(uri -> { ... })` | Validate URI strings such as `resource://data/example.txt`, load content, and return `ResourceContent.text(content, uri)`. |
| `ResourceNotFoundException(uri)` | Throw or map missing resources to a specific not-found error. |
| `server.addResourceSubscribeHandler(uri -> { ... })` | Track subscriptions and return `Mono.empty()` when subscription succeeds. |
| `server.addPromptListHandler(...)` | Return available `Prompt` definitions. |
| `Prompt.builder().name("analyze")` | Name prompts by the task they perform. |
| `PromptArgument.builder().name("topic").description("Topic to analyze").required(true).build()` | Mark required prompt arguments explicitly. |
| `PromptArgument.builder().name("depth").required(false).build()` | Keep optional prompt arguments optional in both schema and handler defaults. |
| `server.addPromptGetHandler((name, arguments) -> { ... })` | Build `PromptResult` only for known prompt names. |
| `PromptMessage.user(...)` / `PromptMessage.assistant(...)` | Use typed prompt messages instead of raw maps. |
| `PromptNotFoundException(name)` | Fail unknown prompts with a specific not-found error. |

## Reactive Streams and Blocking Work

The Java SDK uses Reactive Streams through Project Reactor. Return `Mono` for single results, use `Flux` when composing streams, and isolate blocking calls on bounded elastic schedulers.

| API | Convention |
| --- | --- |
| `Mono.just(...)` | Return already-computed single results. |
| `Mono.fromCallable(...)` | Wrap expensive or blocking operations. |
| `subscribeOn(Schedulers.boundedElastic())` | Move blocking I/O or CPU-heavy calls away from event-loop threads. |
| `Flux.fromIterable(getResources()).map(...).collectList()` | Compose streaming resource lists before returning the list expected by handlers. |
| `timeout(Duration.ofSeconds(30))` | Bound external calls and long-running operations. |
| `onErrorResume(TimeoutException.class, e -> Mono.just(ToolResponse.error().message("Operation timed out").build()))` | Convert expected failures into protocol errors. |
| `McpSyncServer syncServer = server.toSyncServer()` | Use the synchronous facade for blocking use cases and simple tests. |
| `syncServer.addToolHandler("greet", args -> { ... })` | Keep sync handlers small and deterministic. |

## Transport and Spring Boot Integration

Choose one transport model per server entry point and wire Spring servers through beans instead of manual singletons.

| Integration | Convention |
| --- | --- |
| `StdioServerTransport` | Use for local subprocess MCP servers. |
| `ServletServerTransport` | Use for HTTP-based servlet servers. |
| `McpServlet extends HttpServlet` | Keep servlet transport state in fields such as `private final McpServer server` and `private final ServletServerTransport transport`. |
| `doPost(HttpServletRequest req, HttpServletResponse resp)` | Delegate to `transport.handleRequest(server, req, resp).block()` in servlet entry points. |
| `@Configuration` | Use for Spring MCP configuration. |
| `McpServerConfigurer` | Configure Spring server info and capabilities in one bean. |
| `@Bean public McpServerConfigurer mcpServerConfigurer()` | Expose the configurer through Spring. |
| `@Component` handlers | Register tools as Spring beans such as `SearchToolHandler`. |
| `io.mcp.spring.ToolHandler` | Implement Spring handler contracts when using the starter. |
| `getName()` / `getTool()` / `handle(JsonNode arguments)` | Keep handler identity, schema, and execution behavior in one class. |

## JSON Schema, Content, and Serialization

Use the SDK schema and content builders so clients receive machine-readable contracts and typed content.

| API | Convention |
| --- | --- |
| `io.mcp.json.JsonSchema` | Build object, string, integer, and array schemas fluently. |
| `minLength(1)` / `maxLength(100)` | Bound string inputs such as names. |
| `minimum(0)` / `maximum(150)` | Bound numeric inputs such as age. |
| `format("email")` | Use standard formats for values such as email addresses. |
| `items(JsonSchema.string())` / `uniqueItems(true)` | Define array item types and uniqueness. |
| `additionalProperties(false)` | Reject unexpected fields where the protocol shape is fixed. |
| `ObjectMapper` | Customize JSON serialization centrally. |
| `JavaTimeModule` | Register Java time support when serializing dates or times. |
| `McpServerBuilder.builder().objectMapper(mapper)` | Attach custom serialization to the server builder. |
| `Content` | Use content builders for multi-content responses. |
| `addTextContent("Plain text response")` | Return human-readable text content. |
| `addImageContent(imageBytes, "image/png")` | Return image bytes with MIME type. |
| `addResourceContent("resource://data", "application/json", jsonData)` | Return resource-backed JSON content. |

## Errors, Logging, Observability, and Lifecycle

Return protocol errors for expected failures, log unexpected failures with context, and shut down the server gracefully.

| Concern | Convention |
| --- | --- |
| `ValidationException` | Convert invalid user input to `ToolResponse.error().message("Invalid input: " + e.getMessage()).build()`. |
| Unexpected `Exception` | Log the exception and return a generic `Internal error occurred` message. |
| SLF4J | Use `Logger` and `LoggerFactory.getLogger(MyMcpServer.class)`; do not use `System.out` for server diagnostics. |
| `log.info("Tool called: process, args: {}", args)` | Log tool invocation at appropriate levels without leaking secrets. |
| `log.debug("Processing completed successfully")` | Keep detailed success diagnostics at debug level. |
| `doOnError(error -> log.error("Processing failed", error))` | Attach reactive error logging. |
| Reactor `Context` | Use `Mono.deferContextual(ctx -> { String traceId = ctx.get("traceId"); ... })` to propagate observability data. |
| `Disposable serverDisposable = server.start(transport).subscribe()` | Keep the disposable when startup is asynchronous. |
| `Runtime.getRuntime().addShutdownHook(new Thread(...))` | Register graceful shutdown for standalone servers. |
| `serverDisposable.dispose()` and `server.stop().block()` | Dispose the subscription and stop the MCP server during shutdown. |

## Testing and Request Validation

Test protocol behavior through the synchronous facade where possible and validate requests before reaching business logic.

| Test or validation API | Convention |
| --- | --- |
| `McpServerTest` | Keep server behavior tests focused on MCP-visible responses. |
| `@Test` | Use JUnit tests for handler behavior. |
| `assertThat(response.isError()).isFalse()` | Assert success or error status explicitly. |
| `assertThat(response.getContent()).hasSize(1)` | Assert response content shape, not only nullness. |
| `objectMapper.createObjectNode().put("query", "test")` | Build test arguments with Jackson rather than string concatenation. |
| `syncServer.callTool("search", args)` | Exercise handlers through MCP server APIs. |
| `if (!args.has("required_field"))` | Validate required fields before processing. |
| `processRequest(args)` | Delegate validated work to focused application logic. |
| `ConcurrentHashMap` cache | Use thread-safe caches for resource content when caching is warranted. |
| `cache.computeIfAbsent(uri, this::loadResource)` | Cache resources by URI and return `ResourceContent.text(content, uri)`. |

## Java Naming and Structure

Follow Java conventions so protocol code remains idiomatic and navigable.

| Element | Convention |
| --- | --- |
| Classes | Use `PascalCase`, for example `McpServlet`, `McpConfiguration`, and `SearchToolHandler`. |
| Methods and variables | Use `camelCase`, for example `createMcpServer`, `performSearch`, `loadResourceContent`, and `traceId`. |
| Handlers | Keep each handler focused on one MCP tool, resource, or prompt responsibility. |
| Side effects | Validate before mutation and keep blocking calls behind `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())`. |

## Good / Bad Examples

The examples below illustrate safe handling of blocking work and protocol errors.

**Good:**

```java
server.addToolHandler("async", args -> {
    if (!args.has("required_field")) {
        return Mono.just(ToolResponse.error()
            .message("Missing required_field")
            .build());
    }

    return Mono.fromCallable(() -> callExternalApi(args))
        .timeout(Duration.ofSeconds(30))
        .map(result -> ToolResponse.success().addTextContent(result).build())
        .onErrorResume(TimeoutException.class, e -> Mono.just(ToolResponse.error()
            .message("Operation timed out")
            .build()))
        .subscribeOn(Schedulers.boundedElastic());
});
```

Why: The handler validates input, bounds external latency, converts expected timeout failures to MCP errors, and isolates blocking work on `Schedulers.boundedElastic()`.

**Bad:**

```java
server.addToolHandler("async", args -> {
    String result = callExternalApi(args);
    System.out.println(result);
    return Mono.just(ToolResponse.success().addTextContent(result).build());
});
```

Why: The handler blocks the reactive path, skips validation and timeout handling, and uses `System.out` instead of SLF4J.

## Conventions

| Rule | Rationale |
|---|---|
| Declare `io.modelcontextprotocol.sdk:mcp:0.14.1` or `mcp-spring-boot-starter:0.14.1` in the active build tool | SDK usage is reproducible and reviewable |
| Build servers with `McpServerBuilder`, explicit `serverInfo`, and only implemented capabilities | Clients receive accurate protocol metadata |
| Define tools, resources, and prompts with builders and schemas | MCP clients can discover and validate server capabilities |
| Return `Mono` or `Flux` compositions and isolate blocking work with `Schedulers.boundedElastic()` | Reactive servers remain responsive under load |
| Use `McpSyncServer` for blocking cases and tests | Test code stays simple without weakening production reactive design |
| Choose `StdioServerTransport`, `ServletServerTransport`, or Spring Boot integration deliberately | Server entry points match deployment shape |
| Build JSON schemas with constraints such as `required`, `defaultValue`, `format`, and `additionalProperties(false)` | Invalid client inputs fail early and predictably |
| Use SLF4J and Reactor `Context` for logs and trace propagation | Observability works across asynchronous chains |
| Stop servers with `Disposable`, shutdown hooks, and `server.stop().block()` | Processes do not leak and clients observe clean shutdown |
| Follow Java `camelCase` and `PascalCase` naming | MCP code remains idiomatic for Java maintainers |

## Do / Do Not

| Do | Do not |
|---|---|
| Use Maven or Gradle dependencies for the official SDK | Copy SDK classes or mix incompatible SDK versions |
| Enable `tools(true)`, `resources(true)`, and `prompts(true)` only when implemented | Advertise capabilities that have no handlers |
| Validate `query`, `limit`, `topic`, `depth`, and `required_field` inputs | Read arbitrary JSON fields without schema or handler checks |
| Return `ToolResponse.success()` or `ToolResponse.error()` | Throw raw exceptions for expected protocol failures |
| Use `Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())` for blocking work | Block directly inside reactive handlers |
| Use `LoggerFactory` and structured SLF4J messages | Use `System.out` for diagnostics |
| Test handlers with `server.toSyncServer()` and `callTool` | Test only private helper methods while skipping MCP behavior |
| Register graceful shutdown hooks for standalone servers | Leave `server.start(...).subscribe()` without a retained `Disposable` |

## Checklist Before Opening a PR

- [ ] Build files declare the MCP SDK or Spring Boot starter with one consistent version.
- [ ] Server construction uses `McpServerBuilder`, `serverInfo`, and accurate capabilities.
- [ ] Tool, resource, and prompt handlers have names, descriptions, schemas, defaults, and validation.
- [ ] Reactive handlers return `Mono` or `Flux` and move blocking work to `Schedulers.boundedElastic()`.
- [ ] Transport choice matches the deployment: stdio, servlet HTTP, or Spring Boot.
- [ ] JSON schema constraints cover required fields, bounds, formats, array items, uniqueness, and additional properties where relevant.
- [ ] Expected validation failures return MCP error responses; unexpected failures are logged without leaking secrets.
- [ ] Logging uses SLF4J and trace context where needed.
- [ ] Lifecycle code disposes asynchronous startup subscriptions and stops the server gracefully.
- [ ] Tests exercise handlers through `McpSyncServer` or the server API, not only private helper methods.
