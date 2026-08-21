---
applyTo: "**/*.swift,**/Package.swift,**/Package.resolved"
description: "Enforces conventions for building Swift Model Context Protocol servers with the official MCP Swift SDK package."
---

# Swift MCP Server Conventions — Official SDK Servers

These instructions apply to Swift MCP server packages, executable targets, and package lockfiles matched by `**/*.swift`, `**/Package.swift`, and `**/Package.resolved`. They are authoritative for Swift SDK server setup, tool/resource/prompt handlers, transports, concurrency, JSON schema values, package configuration, lifecycle management, logging, testing, initialization hooks, content responses, strict clients, and request batching; the MCP protocol specification and the official `modelcontextprotocol/swift-sdk` APIs win where they define a stricter contract.

## Server Setup and Capabilities

Create an MCP server using the `Server` class with capabilities:

```swift
import MCP

let server = Server(
    name: "MyServer",
    version: "1.0.0",
    capabilities: .init(
        prompts: .init(listChanged: true),
        resources: .init(subscribe: true, listChanged: true),
        tools: .init(listChanged: true)
    )
)
```

## Tool Handlers

Use `withMethodHandler` to register tool handlers:

```swift
// Register tool list handler
await server.withMethodHandler(ListTools.self) { _ in
    let tools = [
        Tool(
            name: "search",
            description: "Search for information",
            inputSchema: .object([
                "properties": .object([
                    "query": .string("Search query"),
                    "limit": .number("Maximum results")
                ]),
                "required": .array([.string("query")])
            ])
        )
    ]
    return .init(tools: tools)
}

// Register tool call handler
await server.withMethodHandler(CallTool.self) { params in
    switch params.name {
    case "search":
        let query = params.arguments?["query"]?.stringValue ?? ""
        let limit = params.arguments?["limit"]?.intValue ?? 10
        
        // Perform search
        let results = performSearch(query: query, limit: limit)
        
        return .init(
            content: [.text("Found \(results.count) results")],
            isError: false
        )
        
    default:
        return .init(
            content: [.text("Unknown tool")],
            isError: true
        )
    }
}
```

## Resource Handlers and Subscriptions

Implement resource handlers for data access:

```swift
// Register resource list handler
await server.withMethodHandler(ListResources.self) { params in
    let resources = [
        Resource(
            name: "Data File",
            uri: "resource://data/example.txt",
            description: "Example data file",
            mimeType: "text/plain"
        )
    ]
    return .init(resources: resources, nextCursor: nil)
}

// Register resource read handler
await server.withMethodHandler(ReadResource.self) { params in
    switch params.uri {
    case "resource://data/example.txt":
        let content = loadResourceContent(uri: params.uri)
        return .init(contents: [
            Resource.Content.text(
                content,
                uri: params.uri,
                mimeType: "text/plain"
            )
        ])
        
    default:
        throw MCPError.invalidParams("Unknown resource URI: \(params.uri)")
    }
}

// Register resource subscribe handler
await server.withMethodHandler(ResourceSubscribe.self) { params in
    // Track subscription for notifications
    subscriptions.insert(params.uri)
    print("Client subscribed to \(params.uri)")
    return .init()
}
```

## Prompt Handlers

Implement prompt handlers for templated conversations:

```swift
// Register prompt list handler
await server.withMethodHandler(ListPrompts.self) { params in
    let prompts = [
        Prompt(
            name: "analyze",
            description: "Analyze a topic",
            arguments: [
                .init(name: "topic", description: "Topic to analyze", required: true),
                .init(name: "depth", description: "Analysis depth", required: false)
            ]
        )
    ]
    return .init(prompts: prompts, nextCursor: nil)
}

// Register prompt get handler
await server.withMethodHandler(GetPrompt.self) { params in
    switch params.name {
    case "analyze":
        let topic = params.arguments?["topic"]?.stringValue ?? "general"
        let depth = params.arguments?["depth"]?.stringValue ?? "basic"
        
        let description = "Analysis of \(topic) at \(depth) level"
        let messages: [Prompt.Message] = [
            .user("Please analyze this topic: \(topic)"),
            .assistant("I'll provide a \(depth) analysis of \(topic)")
        ]
        
        return .init(description: description, messages: messages)
        
    default:
        throw MCPError.invalidParams("Unknown prompt: \(params.name)")
    }
}
```

## Transport Configuration

### Stdio Transport

For local subprocess communication:

```swift
import MCP
import Logging

let logger = Logger(label: "com.example.mcp-server")
let transport = StdioTransport(logger: logger)

try await server.start(transport: transport)
```

### HTTP Transport (Client Side)

For remote server connections:

```swift
let transport = HTTPClientTransport(
    endpoint: URL(string: "http://localhost:8080")!,
    streaming: true  // Enable Server-Sent Events
)

try await client.connect(transport: transport)
```

## Concurrency, Actors, and Shared State

The server is an actor, ensuring thread-safe access:

```swift
actor ServerState {
    private var subscriptions: Set<String> = []
    private var cache: [String: Any] = [:]
    
    func addSubscription(_ uri: String) {
        subscriptions.insert(uri)
    }
    
    func getSubscriptions() -> Set<String> {
        return subscriptions
    }
}

let state = ServerState()

await server.withMethodHandler(ResourceSubscribe.self) { params in
    await state.addSubscription(params.uri)
    return .init()
}
```

## Error Handling

Use Swift's error handling with `MCPError`:

```swift
await server.withMethodHandler(CallTool.self) { params in
    do {
        guard let query = params.arguments?["query"]?.stringValue else {
            throw MCPError.invalidParams("Missing query parameter")
        }
        
        let result = try performOperation(query: query)
        
        return .init(
            content: [.text(result)],
            isError: false
        )
    } catch let error as MCPError {
        return .init(
            content: [.text(error.localizedDescription)],
            isError: true
        )
    } catch {
        return .init(
            content: [.text("Unexpected error: \(error.localizedDescription)")],
            isError: true
        )
    }
}
```

## JSON Schema with `Value`

Use the `Value` type for JSON schemas:

```swift
let schema = Value.object([
    "type": .string("object"),
    "properties": .object([
        "name": .object([
            "type": .string("string"),
            "description": .string("User's name")
        ]),
        "age": .object([
            "type": .string("integer"),
            "minimum": .number(0),
            "maximum": .number(150)
        ]),
        "email": .object([
            "type": .string("string"),
            "format": .string("email")
        ])
    ]),
    "required": .array([.string("name")])
])
```

## Swift Package Manager Setup

Create your `Package.swift`:

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyMCPServer",
    platforms: [
        .macOS(.v13),
        .iOS(.v16)
    ],
    dependencies: [
        .package(
            url: "https://github.com/modelcontextprotocol/swift-sdk.git",
            from: "0.10.0"
        ),
        .package(
            url: "https://github.com/apple/swift-log.git",
            from: "1.5.0"
        )
    ],
    targets: [
        .executableTarget(
            name: "MyMCPServer",
            dependencies: [
                .product(name: "MCP", package: "swift-sdk"),
                .product(name: "Logging", package: "swift-log")
            ]
        )
    ]
)
```

## Graceful Shutdown with ServiceLifecycle

Use Swift Service Lifecycle for proper shutdown:

```swift
import MCP
import ServiceLifecycle
import Logging

struct MCPService: Service {
    let server: Server
    let transport: Transport
    
    func run() async throws {
        try await server.start(transport: transport)
        try await Task.sleep(for: .days(365 * 100))
    }
    
    func shutdown() async throws {
        await server.stop()
    }
}

let logger = Logger(label: "com.example.mcp-server")
let transport = StdioTransport(logger: logger)
let mcpService = MCPService(server: server, transport: transport)

let serviceGroup = ServiceGroup(
    services: [mcpService],
    configuration: .init(
        gracefulShutdownSignals: [.sigterm, .sigint]
    ),
    logger: logger
)

try await serviceGroup.run()
```

## Async/Await Patterns

All server operations use Swift concurrency:

```swift
await server.withMethodHandler(CallTool.self) { params in
    async let result1 = fetchData1()
    async let result2 = fetchData2()
    
    let combined = await "\(result1) and \(result2)"
    
    return .init(
        content: [.text(combined)],
        isError: false
    )
}
```

## Logging

Use swift-log for structured logging:

```swift
import Logging

let logger = Logger(label: "com.example.mcp-server")

await server.withMethodHandler(CallTool.self) { params in
    logger.info("Tool called", metadata: [
        "name": .string(params.name),
        "args": .string("\(params.arguments ?? [:])")
    ])
    
    // Process tool call
    
    logger.debug("Tool completed successfully")
    
    return .init(content: [.text("Result")], isError: false)
}
```

## Testing

Test your server with async/await:

```swift
import XCTest
@testable import MyMCPServer

final class ServerTests: XCTestCase {
    func testToolCall() async throws {
        let server = createTestServer()
        
        // Test tool call logic
        let params = CallTool.Params(
            name: "search",
            arguments: ["query": .string("test")]
        )
        
        // Verify behavior
        XCTAssertNoThrow(try await processToolCall(params))
    }
}
```

## Initialize Hook

Validate client connections with an initialize hook:

```swift
try await server.start(transport: transport) { clientInfo, clientCapabilities in
    // Validate client
    guard clientInfo.name != "BlockedClient" else {
        throw MCPError.invalidRequest("Client not allowed")
    }
    
    // Check capabilities
    if clientCapabilities.sampling == nil {
        logger.warning("Client doesn't support sampling")
    }
    
    logger.info("Client connected", metadata: [
        "name": .string(clientInfo.name),
        "version": .string(clientInfo.version)
    ])
}
```

## Common Patterns

### Content Types

Handle different content types:

```swift
return .init(
    content: [
        .text("Plain text response"),
        .image(imageData, mimeType: "image/png", metadata: [
            "width": 1024,
            "height": 768
        ]),
        .resource(
            uri: "resource://data",
            mimeType: "application/json",
            text: jsonString
        )
    ],
    isError: false
)
```

### Strict Configuration

Use strict mode to fail fast on missing capabilities:

```swift
let client = Client(
    name: "StrictClient",
    version: "1.0.0",
    configuration: .strict
)

// Will throw immediately if capability not available
try await client.listTools()
```

### Request Batching

Send multiple requests efficiently:

```swift
var tasks: [Task<CallTool.Result, Error>] = []

try await client.withBatch { batch in
    for i in 0..<10 {
        tasks.append(
            try await batch.addRequest(
                CallTool.request(.init(
                    name: "process",
                    arguments: ["id": .number(Double(i))]
                ))
            )
        )
    }
}

for (index, task) in tasks.enumerated() {
    let result = try await task.value
    print("\(index): \(result.content)")
}
```


## Good / Bad Examples

The examples below illustrate safe argument validation and MCP error results in a Swift tool handler.

**Good:**

```swift
await server.withMethodHandler(CallTool.self) { params in
    guard params.name == "search" else {
        return .init(content: [.text("Unknown tool")], isError: true)
    }

    guard let query = params.arguments?["query"]?.stringValue else {
        return .init(content: [.text("Missing query parameter")], isError: true)
    }

    let results = try await performOperation(query: query)
    return .init(content: [.text(results)], isError: false)
}
```

Why: The handler validates the tool name and required argument before calling domain work, preserves async flow, and returns an MCP-visible error instead of crashing the server.

**Bad:**

```swift
await server.withMethodHandler(CallTool.self) { params in
    let query = params.arguments!["query"]!.stringValue!
    let results = performSearch(query: query, limit: 10)
    return .init(content: [.text("Found \(results.count) results")], isError: false)
}
```

Why: The handler force-unwraps untrusted client input, assumes synchronous work is safe, and cannot return a clear `MCPError.invalidParams` or `isError: true` result when arguments are missing.

## Conventions

| Rule | Rationale |
|---|---|
| Create servers with `Server`, explicit `name`, `version`, and declared `capabilities` for `prompts`, `resources`, and `tools` | Clients discover only the capabilities the server advertises |
| Register protocol behavior with `await server.withMethodHandler` for `ListTools`, `CallTool`, `ListResources`, `ReadResource`, `ResourceSubscribe`, `ListPrompts`, and `GetPrompt` | The Swift SDK routes MCP methods through typed handlers |
| Build tool schemas with `Value.object`, `Value.string`, `Value.number`, and `Value.array` entries for `type`, `properties`, and `required` | JSON schema stays explicit and client-validated |
| Use `StdioTransport` for local subprocess servers and `HTTPClientTransport(endpoint:streaming:)` only for client-side remote connections such as `http://localhost:8080` | Transports match MCP deployment mode and avoid protocol confusion |
| Keep mutable state in an `actor` such as `ServerState` and call it with `await` | Server handlers are concurrent and shared dictionaries or sets need isolation |
| Return `isError: true` for handled tool failures and throw `MCPError.invalidParams` or `MCPError.invalidRequest` for protocol-invalid inputs | Clients receive structured failures instead of transport crashes |
| Define `Package.swift` with `swift-tools-version: 6.0`, `.macOS(.v13)`, `.iOS(.v16)`, `https://github.com/modelcontextprotocol/swift-sdk.git`, and `https://github.com/apple/swift-log.git` when those platform targets fit the package | The executable target resolves the `MCP` and `Logging` products consistently |
| Use `ServiceLifecycle`, `Service`, `ServiceGroup`, `.sigterm`, and `.sigint` for graceful shutdown when the server must run as a service | Shutdown drains the transport and calls `server.stop()` instead of abandoning clients |
| Log with `swift-log` `Logger` metadata and avoid logging secrets from `params.arguments` | Structured logs aid debugging without leaking client data |
| Test handlers with `XCTest`, `async throws`, `CallTool.Params`, and focused functions such as `processToolCall` | Tests validate MCP behavior without requiring a live client |
| Use the initialize hook to inspect `clientInfo` and `clientCapabilities` before accepting a connection | Unsupported or blocked clients fail before invoking tools |
| Return content with `.text`, `.image`, and `.resource` using correct `mimeType` values such as `text/plain`, `application/json`, and `image/png` | MCP clients need accurate content typing to render responses |
| Use `Client(configuration: .strict)` and `client.withBatch` only when client capability checks and batched `CallTool.request` calls are intentional | Strict mode and batching change failure behavior and should be deliberate |

## Do / Do Not

| Do | Do not |
|---|---|
| Declare `prompts`, `resources`, and `tools` capabilities before registering matching handlers | Register handlers for capabilities the server does not advertise |
| Validate `params.name`, `params.arguments`, and resource or prompt names before doing work | Force-unwrap client-provided arguments or assume a known tool name |
| Use `MCPError.invalidParams("Unknown resource URI: \(params.uri)")` or an `isError: true` result for invalid client input | Let invalid resource URIs or missing fields crash the process |
| Keep subscriptions in an actor-backed `Set<String>` | Mutate shared subscription state from concurrent handlers directly |
| Use `StdioTransport(logger:)` for local MCP server processes | Treat client-side `HTTPClientTransport` as a server transport |
| Use `async let`, `Task`, and `await` for independent asynchronous work | Block Swift concurrency with synchronous waits inside handlers |
| Mark package dependencies on `swift-sdk` and `swift-log` explicitly | Rely on undeclared transitive products in `Package.swift` |
| Install a service lifecycle when long-running shutdown behavior matters | Depend on `Task.sleep(for: .days(365 * 100))` without a shutdown path |

## Checklist Before Opening a PR

- [ ] The server declares accurate `Server` metadata and MCP capabilities.
- [ ] Tool, resource, prompt, subscribe, and initialize handlers validate names and arguments before work starts.
- [ ] JSON schemas use `Value` and include `type`, `properties`, and `required` where needed.
- [ ] Transport choice matches the deployment mode: `StdioTransport` for local servers and `HTTPClientTransport` only for remote clients.
- [ ] Shared mutable state is actor-isolated and accessed with `await`.
- [ ] Errors return `MCPError` or `isError: true` content that clients can display.
- [ ] `Package.swift` declares the MCP and logging dependencies and compatible platform targets.
- [ ] Service shutdown handles `.sigterm` and `.sigint` when the executable runs as a daemon.
- [ ] Logging is structured and avoids sensitive argument values.
- [ ] Async XCTest coverage exercises at least one successful tool call and one failure path.

## References

- Swift MCP SDK package: https://github.com/modelcontextprotocol/swift-sdk.git
- Swift Log package: https://github.com/apple/swift-log.git
