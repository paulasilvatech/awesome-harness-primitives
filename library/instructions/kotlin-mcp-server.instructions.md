---
applyTo: "**/*.kt,**/*.kts,**/build.gradle.kts,**/settings.gradle.kts"
description: "Enforces conventions for building Kotlin Model Context Protocol servers with the official io.modelcontextprotocol:kotlin-sdk library."
---

# Kotlin MCP Server Conventions — Official SDK Servers

These instructions apply to Kotlin MCP server source, Gradle Kotlin build files, and settings matched by `**/*.kt`, `**/*.kts`, `**/build.gradle.kts`, and `**/settings.gradle.kts`. They are authoritative for Kotlin SDK server setup, tool/resource/prompt registration, transports, coroutine usage, JSON schemas, Gradle dependencies, multiplatform configuration, resource lifecycle, testing, logging, configuration, and dependency injection; the MCP protocol and official `io.modelcontextprotocol:kotlin-sdk` APIs win where they define stricter behavior.

## Server Setup and Capabilities

Create an MCP server using the `Server` class:

```kotlin
import io.modelcontextprotocol.kotlin.sdk.server.Server
import io.modelcontextprotocol.kotlin.sdk.server.ServerOptions
import io.modelcontextprotocol.kotlin.sdk.Implementation
import io.modelcontextprotocol.kotlin.sdk.ServerCapabilities

val server = Server(
    serverInfo = Implementation(
        name = "my-server",
        version = "1.0.0"
    ),
    options = ServerOptions(
        capabilities = ServerCapabilities(
            tools = ServerCapabilities.Tools(),
            resources = ServerCapabilities.Resources(
                subscribe = true,
                listChanged = true
            ),
            prompts = ServerCapabilities.Prompts(listChanged = true)
        )
    )
) {
    "Server description goes here"
}
```

## Tool Handlers

Use `server.addTool()` to register tools with typed request/response handling:

```kotlin
import io.modelcontextprotocol.kotlin.sdk.CallToolRequest
import io.modelcontextprotocol.kotlin.sdk.CallToolResult
import io.modelcontextprotocol.kotlin.sdk.TextContent

server.addTool(
    name = "search",
    description = "Search for information",
    inputSchema = buildJsonObject {
        put("type", "object")
        putJsonObject("properties") {
            putJsonObject("query") {
                put("type", "string")
                put("description", "The search query")
            }
            putJsonObject("limit") {
                put("type", "integer")
                put("description", "Maximum results to return")
            }
        }
        putJsonArray("required") {
            add("query")
        }
    }
) { request: CallToolRequest ->
    val query = request.params.arguments["query"] as? String
        ?: throw IllegalArgumentException("query is required")
    val limit = (request.params.arguments["limit"] as? Number)?.toInt() ?: 10
    
    // Perform search
    val results = performSearch(query, limit)
    
    CallToolResult(
        content = listOf(
            TextContent(
                text = results.joinToString("\n")
            )
        )
    )
}
```

## Resource Handlers

Use `server.addResource()` to provide accessible data:

```kotlin
import io.modelcontextprotocol.kotlin.sdk.ReadResourceRequest
import io.modelcontextprotocol.kotlin.sdk.ReadResourceResult
import io.modelcontextprotocol.kotlin.sdk.TextResourceContents

server.addResource(
    uri = "file:///data/example.txt",
    name = "Example Data",
    description = "Example resource data",
    mimeType = "text/plain"
) { request: ReadResourceRequest ->
    val content = loadResourceContent(request.uri)
    
    ReadResourceResult(
        contents = listOf(
            TextResourceContents(
                text = content,
                uri = request.uri,
                mimeType = "text/plain"
            )
        )
    )
}
```

## Prompt Handlers

Use `server.addPrompt()` for reusable prompt templates:

```kotlin
import io.modelcontextprotocol.kotlin.sdk.GetPromptRequest
import io.modelcontextprotocol.kotlin.sdk.GetPromptResult
import io.modelcontextprotocol.kotlin.sdk.PromptMessage
import io.modelcontextprotocol.kotlin.sdk.Role

server.addPrompt(
    name = "analyze",
    description = "Analyze a topic",
    arguments = listOf(
        PromptArgument(
            name = "topic",
            description = "The topic to analyze",
            required = true
        )
    )
) { request: GetPromptRequest ->
    val topic = request.params.arguments?.get("topic") as? String
        ?: throw IllegalArgumentException("topic is required")
    
    GetPromptResult(
        description = "Analyze the given topic",
        messages = listOf(
            PromptMessage(
                role = Role.User,
                content = TextContent(
                    text = "Analyze this topic: $topic"
                )
            )
        )
    )
}
```

## Transport Configuration

### Stdio Transport

For communication over stdin/stdout:

```kotlin
import io.modelcontextprotocol.kotlin.sdk.server.StdioServerTransport

suspend fun main() {
    val transport = StdioServerTransport()
    server.connect(transport)
}
```

### SSE Transport with Ktor

For HTTP-based communication using Server-Sent Events:

```kotlin
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.modelcontextprotocol.kotlin.sdk.server.mcp

fun main() {
    embeddedServer(Netty, port = 8080) {
        mcp {
            Server(
                serverInfo = Implementation(
                    name = "sse-server",
                    version = "1.0.0"
                ),
                options = ServerOptions(
                    capabilities = ServerCapabilities(
                        tools = ServerCapabilities.Tools()
                    )
                )
            ) {
                "SSE-based MCP server"
            }
        }
    }.start(wait = true)
}
```

## Coroutine Usage

All MCP operations are suspending functions. Use Kotlin coroutines properly:

```kotlin
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.async

server.addTool(
    name = "parallel-search",
    description = "Search multiple sources in parallel"
) { request ->
    coroutineScope {
        val source1 = async { searchSource1(query) }
        val source2 = async { searchSource2(query) }
        
        val results = source1.await() + source2.await()
        
        CallToolResult(
            content = listOf(TextContent(text = results.joinToString("\n")))
        )
    }
}
```

## Error Handling

Use Kotlin's exception handling and provide meaningful error messages:

```kotlin
server.addTool(
    name = "validate-input",
    description = "Process validated input"
) { request ->
    try {
        val input = request.params.arguments["input"] as? String
            ?: throw IllegalArgumentException("input is required")
        
        require(input.isNotBlank()) { "input cannot be blank" }
        
        val result = processInput(input)
        
        CallToolResult(
            content = listOf(TextContent(text = result))
        )
    } catch (e: IllegalArgumentException) {
        CallToolResult(
            isError = true,
            content = listOf(TextContent(text = "Validation error: ${e.message}"))
        )
    }
}
```

## JSON Schema with kotlinx.serialization

Use kotlinx.serialization for type-safe JSON schemas:

```kotlin
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*

@Serializable
data class SearchInput(
    val query: String,
    val limit: Int = 10,
    val filters: List<String> = emptyList()
)

fun createToolSchema(): JsonObject = buildJsonObject {
    put("type", "object")
    putJsonObject("properties") {
        putJsonObject("query") {
            put("type", "string")
            put("description", "Search query")
        }
        putJsonObject("limit") {
            put("type", "integer")
            put("default", 10)
        }
        putJsonObject("filters") {
            put("type", "array")
            putJsonObject("items") {
                put("type", "string")
            }
        }
    }
    putJsonArray("required") {
        add("query")
    }
}
```

## Gradle Configuration

Set up your `build.gradle.kts` properly:

```kotlin
plugins {
    kotlin("jvm") version "2.1.0"
    kotlin("plugin.serialization") version "2.1.0"
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("io.modelcontextprotocol:kotlin-sdk:0.7.2")
    
    // For client transport
    implementation("io.ktor:ktor-client-cio:3.0.0")
    
    // For server transport
    implementation("io.ktor:ktor-server-netty:3.0.0")
    
    // For JSON serialization
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
    
    // For coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
}
```

## Multiplatform Support

The Kotlin SDK supports Kotlin Multiplatform (JVM, Wasm, iOS):

```kotlin
kotlin {
    jvm()
    js(IR) {
        browser()
        nodejs()
    }
    wasmJs()
    
    sourceSets {
        commonMain.dependencies {
            implementation("io.modelcontextprotocol:kotlin-sdk:0.7.2")
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
        }
    }
}
```

## Resource Lifecycle

Handle resource updates and subscriptions:

```kotlin
server.addResource(
    uri = "file:///dynamic/data",
    name = "Dynamic Data",
    description = "Frequently updated data",
    mimeType = "application/json"
) { request ->
    // Provide current state
    ReadResourceResult(
        contents = listOf(
            TextResourceContents(
                text = getCurrentData(),
                uri = request.uri,
                mimeType = "application/json"
            )
        )
    )
}

// Notify clients when resource changes
server.notifyResourceListChanged()
```

## Testing

Test your MCP tools using Kotlin coroutines test utilities:

```kotlin
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals

class ServerTest {
    @Test
    fun testSearchTool() = runTest {
        val server = createTestServer()
        
        val request = CallToolRequest(
            params = CallToolParams(
                name = "search",
                arguments = mapOf("query" to "test", "limit" to 5)
            )
        )
        
        val result = server.callTool(request)
        
        assertEquals(false, result.isError)
        assert(result.content.isNotEmpty())
    }
}
```

## Common Patterns

### Logging

Use structured logging with a Kotlin logging library:

```kotlin
import io.github.oshai.kotlinlogging.KotlinLogging

private val logger = KotlinLogging.logger {}

server.addTool(
    name = "logged-operation",
    description = "Operation with logging"
) { request ->
    logger.info { "Tool called with args: ${request.params.arguments}" }
    
    try {
        val result = performOperation(request)
        logger.info { "Operation succeeded" }
        result
    } catch (e: Exception) {
        logger.error(e) { "Operation failed" }
        throw e
    }
}
```

### Configuration

Use data classes for configuration:

```kotlin
import kotlinx.serialization.Serializable

@Serializable
data class ServerConfig(
    val name: String = "my-server",
    val version: String = "1.0.0",
    val port: Int = 8080,
    val enableTools: Boolean = true
)

fun loadConfig(): ServerConfig {
    // Load from environment or config file
    return ServerConfig(
        name = System.getenv("SERVER_NAME") ?: "my-server",
        version = System.getenv("VERSION") ?: "1.0.0"
    )
}
```

### Dependency Injection

Use constructor injection for testability:

```kotlin
class MyServer(
    private val dataService: DataService,
    private val config: ServerConfig
) {
    fun createServer() = Server(
        serverInfo = Implementation(
            name = config.name,
            version = config.version
        )
    ) {
        "MCP Server with DI"
    }.apply {
        addTool(
            name = "fetch-data",
            description = "Fetch data using injected service"
        ) { request ->
            val data = dataService.fetchData()
            CallToolResult(
                content = listOf(TextContent(text = data))
            )
        }
    }
}
```


## Good / Bad Examples

The examples below illustrate safe argument handling and coroutine-friendly tool execution.

**Good:**

```kotlin
server.addTool(
    name = "search",
    description = "Search for information",
    inputSchema = createToolSchema()
) { request: CallToolRequest ->
    val query = request.params.arguments["query"] as? String
        ?: throw IllegalArgumentException("query is required")

    coroutineScope {
        val source1 = async { searchSource1(query) }
        val source2 = async { searchSource2(query) }
        CallToolResult(
            content = listOf(TextContent(text = (source1.await() + source2.await()).joinToString("\n")))
        )
    }
}
```

Why: The handler declares a schema, validates the required argument, and keeps parallel work inside structured concurrency.

**Bad:**

```kotlin
server.addTool(name = "search", description = "Search") { request ->
    val query = request.params.arguments["query"] as String
    CallToolResult(content = listOf(TextContent(text = searchSource1(query).joinToString("\n"))))
}
```

Why: The handler omits an input schema, casts untrusted arguments directly, and leaves no clear validation error path.

## Conventions

| Rule | Rationale |
|---|---|
| Create servers with `Server`, `Implementation`, `ServerOptions`, and `ServerCapabilities` for `tools`, `resources`, and `prompts` | MCP clients discover only declared capabilities |
| Register tools with `server.addTool`, `CallToolRequest`, `CallToolResult`, `TextContent`, and a `buildJsonObject` input schema | Tool handlers remain typed and client-validated |
| Register resources with `server.addResource`, `ReadResourceRequest`, `ReadResourceResult`, and `TextResourceContents` using stable URI and `mimeType` values | Resource reads stay discoverable and renderable |
| Register prompts with `server.addPrompt`, `GetPromptRequest`, `GetPromptResult`, `PromptMessage`, `PromptArgument`, and `Role.User` | Prompt templates expose required arguments and return structured messages |
| Use `StdioServerTransport` for stdin/stdout servers and Ktor `embeddedServer(Netty, port = 8080)` with `mcp` for SSE-based HTTP servers | Transports match local subprocess and HTTP deployment modes |
| Keep all MCP work suspendable and use `coroutineScope`, `async`, and `await` for parallel operations | Structured concurrency prevents leaked work and preserves cancellation |
| Return `CallToolResult(isError = true, ...)` for handled validation failures and use `require` or `IllegalArgumentException` for invalid arguments | Clients receive meaningful failures instead of ambiguous crashes |
| Build schemas with `kotlinx.serialization`, `@Serializable`, `JsonObject`, `buildJsonObject`, `putJsonObject`, and `putJsonArray` | Schemas and configuration stay type-safe and maintainable |
| Configure Gradle with Kotlin `2.1.0`, `io.modelcontextprotocol:kotlin-sdk:0.7.2`, Ktor `3.0.0`, `kotlinx-serialization-json:1.7.3`, and `kotlinx-coroutines-core:1.9.0` when those versions match the project baseline | Runtime and build dependencies align with the documented SDK examples |
| Use multiplatform source sets only when the server must target JVM, JS, Wasm, or iOS | Multiplatform configuration adds complexity and should match deployment needs |
| Notify subscribers with `server.notifyResourceListChanged()` after dynamic resource lists change | Clients with resource subscriptions need change notifications |
| Test suspend handlers with `kotlinx.coroutines.test.runTest`, `kotlin.test.Test`, and `assertEquals` | Tests execute coroutine code deterministically |
| Log with a structured logger such as `KotlinLogging` and avoid leaking sensitive `request.params.arguments` values | Logs remain useful without exposing client input |
| Load `ServerConfig` from environment variables such as `SERVER_NAME` and `VERSION` with safe defaults | Configuration is deployable without hardcoding server identity |
| Use constructor injection for services and config in classes such as `MyServer` | Handlers are testable without constructing real infrastructure |

## Do / Do Not

| Do | Do not |
|---|---|
| Declare `ServerCapabilities.Tools`, `ServerCapabilities.Resources`, and `ServerCapabilities.Prompts` for supported features | Register features that clients cannot discover |
| Validate `request.params.arguments` with safe casts and defaults | Cast arguments with `as String` without checking presence or type |
| Use `buildJsonObject` schemas with `type`, `properties`, and `required` | Leave tool inputs undocumented or client-unvalidated |
| Use `StdioServerTransport()` for local MCP subprocesses | Mix stdio and SSE assumptions in one entry point |
| Keep parallel operations inside `coroutineScope` | Launch untracked coroutines from a handler |
| Return `isError = true` with `TextContent` for recoverable validation errors | Throw generic exceptions for user-correctable input mistakes |
| Keep Gradle dependencies explicit in `build.gradle.kts` | Rely on undeclared transitive Kotlin, Ktor, or serialization artifacts |
| Cover handlers with `runTest` and direct request objects | Depend only on manual MCP client testing |
| Inject `DataService` and `ServerConfig` through constructors | Create production services directly inside handlers |

## Checklist Before Opening a PR

- [ ] `Server` metadata and `ServerCapabilities` match the tools, resources, and prompts actually registered.
- [ ] Tool schemas use `buildJsonObject` and mark required arguments.
- [ ] Resource and prompt handlers return typed SDK results with correct URI, role, and `mimeType` values.
- [ ] Transport setup is either stdio or Ktor SSE and matches the deployment target.
- [ ] Coroutine work is suspendable, structured, cancellable, and free of untracked launches.
- [ ] Validation failures produce clear `IllegalArgumentException` or `CallToolResult(isError = true)` behavior.
- [ ] Gradle dependencies and Kotlin plugin versions are explicit and consistent with the project baseline.
- [ ] Resource change notifications are sent when subscribed resource lists change.
- [ ] `runTest` coverage exercises successful and failing tool calls.
- [ ] Logging, configuration, and dependency injection avoid hardcoded secrets and production-only construction.
