---
name: kotlin-mcp-server-generator
description: >-
  Generate a complete Kotlin Model Context Protocol server project using io.modelcontextprotocol:kotlin-sdk, Gradle, stdio or Ktor transport, typed tools, configuration, tests, and README documentation. Use when asked to create a Kotlin MCP server, scaffold MCP tools, build a Gradle MCP project, or generate a production-ready MCP server template.
---

# Kotlin MCP server generator

Generate a complete Kotlin MCP server project from a server name, package, tools, transport, and description. Produce a Gradle layout, MCP SDK wiring, typed tool schemas, coroutine-safe implementation, tests, and README instructions that can be copied into a repository.

## When to invoke

- "Generate a Kotlin MCP server project."
- "Create a Gradle MCP server using the Kotlin SDK."
- "Scaffold MCP tools with typed inputs and outputs."
- "Build a Kotlin stdio MCP server with tests and README."
- "Add Ktor SSE transport to a Kotlin MCP server."

## Project contract

| Area | Required output |
| --- | --- |
| Project structure | A Gradle Kotlin project with `build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`, `src/main/kotlin/...`, `src/test/kotlin/...`, and `README.md`. |
| Dependencies | Official `io.modelcontextprotocol:kotlin-sdk`, Ktor transport modules, `kotlinx-serialization-json`, `kotlinx-coroutines-core`, `kotlin-logging-jvm`, `logback-classic`, and `kotlinx-coroutines-test`. |
| Runtime | A `Main.kt` that loads config, creates a `Server`, connects `StdioServerTransport`, and logs startup. |
| Tools | At least two or three useful tools with JSON schemas built with `buildJsonObject`, required fields, validation, and typed inputs/outputs. |
| Error handling | Validate required parameters before tool execution and return clear failures through Kotlin exceptions or result types such as `Result/Either` when the project already uses them. |
| Testing | Include coroutine tests with `runTest`, a `test server creation` case, and a `test tool1 execution` case or equivalent. |
| Documentation | Explain requirements, build, run, configuration, tools, development, and license in `README.md`. |

Use placeholders only where generation truly needs user input: `PROJECT_NAME`, `PROJECT_DESCRIPTION`, `TOOL1_DESCRIPTION`, `SERVER_NAME`, `VERSION`, and `DESCRIPTION`.

## File layout

Create this structure, replacing `myserver` and `com/example/myserver/` with the requested project and package names:

```text
myserver/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── src/
│   ├── main/kotlin/com/example/myserver/
│   │   ├── Main.kt
│   │   ├── Server.kt
│   │   ├── config/Config.kt
│   │   └── tools/
│   │       ├── Tool1.kt
│   │       ├── Tool2.kt
│   │       └── ToolRegistry.kt
│   └── test/kotlin/com/example/myserver/ServerTest.kt
└── README.md
```

Keep package declarations consistent across every file. If the artifact name differs from the package, make `settings.gradle.kts` set `rootProject.name = "PROJECT_NAME"` and make `application.mainClass` point at the generated `MainKt` class.

## Gradle and dependencies

Use a JVM Gradle build unless the user explicitly asks for multiplatform. The baseline dependency set is:

```kotlin
plugins {
    kotlin("jvm") version "2.1.0"
    kotlin("plugin.serialization") version "2.1.0"
    application
}

dependencies {
    implementation("io.modelcontextprotocol:kotlin-sdk:0.7.2")
    implementation("io.ktor:ktor-server-netty:3.0.0")
    implementation("io.ktor:ktor-client-cio:3.0.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
    implementation("io.github.oshai:kotlin-logging-jvm:7.0.0")
    implementation("ch.qos.logback:logback-classic:1.5.12")
    testImplementation(kotlin("test"))
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.9.0")
}

application { mainClass.set("com.example.myserver.MainKt") }
tasks.test { useJUnitPlatform() }
kotlin { jvmToolchain(17) }
```

If the user asks for Kotlin Multiplatform, add `jvm()`, `js(IR) { nodejs() }`, `wasmJs()`, and put `implementation("io.modelcontextprotocol:kotlin-sdk:0.7.2")` in `commonMain.dependencies`. Do not claim multiplatform support in `README.md` unless the build actually configures it.

## Server and transport wiring

| File | Required content |
| --- | --- |
| `Config.kt` | A serializable `Config` with `name`, `version`, and `description`; `loadConfig()` reads `SERVER_NAME`, `VERSION`, and `DESCRIPTION`, falling back to `PROJECT_NAME`, `1.0.0`, and `PROJECT_DESCRIPTION`. |
| `Main.kt` | `runBlocking`, `KotlinLogging.logger {}`, `loadConfig()`, `createServer(config)`, `StdioServerTransport()`, and `server.connect(transport)`. |
| `Server.kt` | `Server`, `ServerOptions`, `Implementation`, `ServerCapabilities.Tools()`, optional `ServerCapabilities.Resources(subscribe = true, listChanged = true)`, optional `ServerCapabilities.Prompts(listChanged = true)`, and `server.registerTools()`. |
| `ToolRegistry.kt` | `fun Server.registerTools()` that calls every generated `registerToolN()` exactly once. |

For stdio, use:

```kotlin
val transport = StdioServerTransport()
server.connect(transport)
```

For SSE transport with Ktor, show the shape without mixing it into the stdio entry point unless requested:

```kotlin
embeddedServer(Netty, port = 8080) {
    mcp { Server(/* ... */) { "Description" } }
}.start(wait = true)
```

## Tool implementation rules

| Concern | Rule |
| --- | --- |
| Schema | Build JSON schema with `buildJsonObject`, `putJsonObject("properties")`, `putJsonArray("required")`, `put("type", ...)`, and field descriptions. |
| Request | Type handler parameters as `CallToolRequest` when using the SDK callback signature. |
| Required input | Extract `param1` or real required fields from `request.params.arguments`; throw `IllegalArgumentException("param1 is required")` or a domain-specific message when absent. |
| Optional input | Convert `param2` or numeric optional fields safely with `(value as? Number)?.toInt() ?: 0`. |
| Result | Return `CallToolResult(content = listOf(TextContent(text = result)))` for text tools; use typed serialization for structured results when needed. |
| Async work | Use suspending functions for I/O and coroutine-friendly APIs; keep blocking work isolated. |
| Type safety | Prefer data classes, sealed classes for result states, null safety, and `kotlinx.serialization`. |
| Testability | Put business logic in private or injectable functions such as `performTool1Logic(param1, param2)`, not inline in the registration lambda. |
| Documentation | Add KDoc comments for public APIs and meaningful tool descriptions. |

Name test fixtures explicitly, for example `test-server`, and document typed `inputs/outputs` for every generated tool. Use `kotlin-logging` consistently so dependency names and imports stay aligned.

## README content

The `README.md` must include this concrete operating information:

| Section | Required detail |
| --- | --- |
| Requirements | Java 17 or higher and the Kotlin version configured by Gradle. |
| Installation | `./gradlew build`. |
| Usage | `./gradlew run`; optionally `./gradlew installDist` and `./build/install/PROJECT_NAME/bin/PROJECT_NAME`. |
| Configuration | `SERVER_NAME`, `VERSION`, and `DESCRIPTION` environment variables. |
| Available Tools | Each tool name, `TOOL1_DESCRIPTION`, inputs such as `param1` and `param2`, and output shape. |
| Development | `./gradlew test`, `./gradlew build`, and `./gradlew run --continuous` for auto-reload development; the install task writes launch scripts under `build/install/`. |
| License | State the chosen license, for example MIT, only if the user requested or accepted it. |

## Gotchas

- **Keep SDK examples version-consistent**: `io.modelcontextprotocol:kotlin-sdk:0.7.2`, `ktor-server-netty`, and `ktor-client-cio` examples should compile together with the selected Kotlin version.
- **Do not register phantom tools**: every call in `tools/ToolRegistry.kt` must have a matching implementation file.
- **Do not advertise multiplatform unless configured**: JVM-only builds should not claim JVM, Wasm, and iOS support.
- **Do not leave placeholders in generated code**: replace `PROJECT_NAME`, `PROJECT_DESCRIPTION`, and `TOOL1_DESCRIPTION` before final output unless the user explicitly requested a template.

## Output template

```markdown
## Kotlin MCP server project

**Status:** generated | blocked
**Project:** `<PROJECT_NAME>`
**Package:** `<package.name>`
**Transport:** stdio | SSE | both

### Files
| Path | Purpose |
| --- | --- |
| `build.gradle.kts` | Gradle Kotlin build with MCP, Ktor, serialization, coroutines, logging, and test dependencies |
| `src/main/kotlin/<package>/Main.kt` | Server entry point |
| `src/main/kotlin/<package>/Server.kt` | MCP `Server` configuration and capabilities |
| `src/main/kotlin/<package>/config/Config.kt` | Environment-backed configuration |
| `src/main/kotlin/<package>/tools/ToolRegistry.kt` | Tool registration |
| `src/test/kotlin/<package>/ServerTest.kt` | Coroutine tests |
| `README.md` | Build, run, configuration, and tool usage |

### Commands
- `./gradlew build`
- `./gradlew test`
- `./gradlew run`

### Notes
- <remaining setup note or "none">
```

## Quality gate

- [ ] `name` is `kotlin-mcp-server-generator` and matches the parent directory.
- [ ] The project layout includes all required Gradle, source, test, tools, config, and `README.md` files.
- [ ] `build.gradle.kts` includes the MCP SDK, Ktor, serialization, coroutines, logging, and testing dependencies.
- [ ] `Main.kt`, `Server.kt`, `Config.kt`, and `tools/ToolRegistry.kt` compile together with consistent packages and imports.
- [ ] Every generated tool has a JSON schema, validation, implementation, and `CallToolResult` output.
- [ ] Environment variables `SERVER_NAME`, `VERSION`, and `DESCRIPTION` are documented and used.
- [ ] Tests use coroutine test utilities and include server creation plus at least one tool execution path.
- [ ] The README commands and paths match the generated project name.
