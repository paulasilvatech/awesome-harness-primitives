---
applyTo: "**/*.rs"
description: "Enforces Rust Model Context Protocol server conventions for rmcp dependencies, handlers, tools, prompts, resources, transports, errors, tests, authentication, observability, and deployment."
---

# Rust MCP Server Conventions — rmcp Servers

These instructions apply to Rust source files that implement Model Context Protocol servers with the official `rmcp` SDK. They are authoritative for `rmcp` dependency shape, async server construction, `ServerHandler` behavior, tools, prompts, resources, transports, protocol errors, tests, OAuth wiring, tracing, and release packaging in matched `**/*.rs` files; project-specific architecture, security, and deployment primitives win where they define stricter requirements.

## Dependencies and Project Layout

### Cargo dependencies

Add the `rmcp` crate to your `Cargo.toml`:

```toml
[dependencies]
rmcp = { version = "0.8.1", features = ["server"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
tracing = "0.1"
tracing-subscriber = "0.3"
```

For macros support:

```toml
[dependencies]
rmcp-macros = "0.8"
schemars = { version = "0.8", features = ["derive"] }
```

### Project structure

Organize your Rust MCP server project:

```
my-mcp-server/
├── Cargo.toml
├── src/
│   ├── main.rs           # Server entry point
│   ├── handler.rs        # ServerHandler implementation
│   ├── tools/
│   │   ├── mod.rs
│   │   ├── calculator.rs
│   │   └── greeter.rs
│   ├── prompts/
│   │   ├── mod.rs
│   │   └── code_review.rs
│   └── resources/
│       ├── mod.rs
│       └── data.rs
└── tests/
    └── integration_tests.rs
```

## Server Runtime and Handler Shape

### Stdio server setup

Create a server with stdio transport:

```rust
use rmcp::{
    protocol::ServerCapabilities,
    server::{Server, ServerHandler},
    transport::StdioTransport,
};
use tokio::signal;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    
    let handler = MyServerHandler::new();
    let transport = StdioTransport::new();
    
    let server = Server::builder()
        .with_handler(handler)
        .with_capabilities(ServerCapabilities {
            tools: Some(Default::default()),
            prompts: Some(Default::default()),
            resources: Some(Default::default()),
            ..Default::default()
        })
        .build(transport)?;
    
    server.run(signal::ctrl_c()).await?;
    
    Ok(())
}
```

### ServerHandler implementation

Implement the `ServerHandler` trait:

```rust
use rmcp::{
    model::*,
    protocol::*,
    server::{RequestContext, ServerHandler, RoleServer},
    ErrorData,
};

pub struct MyServerHandler {
    tool_router: ToolRouter,
}

impl MyServerHandler {
    pub fn new() -> Self {
        Self {
            tool_router: Self::create_tool_router(),
        }
    }
    
    fn create_tool_router() -> ToolRouter {
        // Initialize and return tool router
        ToolRouter::new()
    }
}

#[async_trait::async_trait]
impl ServerHandler for MyServerHandler {
    async fn list_tools(
        &self,
        _request: Option<PaginatedRequestParam>,
        _context: RequestContext<RoleServer>,
    ) -> Result<ListToolsResult, ErrorData> {
        let items = self.tool_router.list_all();
        Ok(ListToolsResult::with_all_items(items))
    }
    
    async fn call_tool(
        &self,
        request: CallToolRequestParam,
        context: RequestContext<RoleServer>,
    ) -> Result<CallToolResult, ErrorData> {
        let tcc = ToolCallContext::new(self, request, context);
        self.tool_router.call(tcc).await
    }
}
```

## Tools and Routers

### Declarative tools

Use the `#[tool]` macro for declarative tool definitions:

```rust
use rmcp::tool;
use rmcp::model::Parameters;
use serde::{Deserialize, Serialize};
use schemars::JsonSchema;

#[derive(Debug, Deserialize, JsonSchema)]
pub struct CalculateParams {
    pub a: f64,
    pub b: f64,
    pub operation: String,
}

/// Performs mathematical calculations
#[tool(
    name = "calculate",
    description = "Performs basic arithmetic operations",
    annotations(read_only_hint = true)
)]
pub async fn calculate(params: Parameters<CalculateParams>) -> Result<f64, String> {
    let p = params.inner();
    match p.operation.as_str() {
        "add" => Ok(p.a + p.b),
        "subtract" => Ok(p.a - p.b),
        "multiply" => Ok(p.a * p.b),
        "divide" => {
            if p.b == 0.0 {
                Err("Division by zero".to_string())
            } else {
                Ok(p.a / p.b)
            }
        }
        _ => Err(format!("Unknown operation: {}", p.operation)),
    }
}
```

### Tool routers

Use `#[tool_router]` and `#[tool_handler]` macros:

```rust
use rmcp::{tool_router, tool_handler};

pub struct ToolsHandler {
    tool_router: ToolRouter,
}

#[tool_router]
impl ToolsHandler {
    #[tool]
    async fn greet(params: Parameters<GreetParams>) -> String {
        format!("Hello, {}!", params.inner().name)
    }
    
    #[tool(annotations(destructive_hint = true))]
    async fn reset_counter() -> String {
        "Counter reset".to_string()
    }
    
    pub fn new() -> Self {
        Self {
            tool_router: Self::tool_router(),
        }
    }
}

#[tool_handler]
impl ServerHandler for ToolsHandler {
    // Other handler methods...
}
```

### Tool annotations

Use annotations to provide hints about tool behavior:

```rust
#[tool(
    name = "delete_file",
    annotations(
        destructive_hint = true,
        read_only_hint = false,
        idempotent_hint = false
    )
)]
pub async fn delete_file(params: Parameters<DeleteParams>) -> Result<(), String> {
    // Delete file logic
}

#[tool(
    name = "search_data",
    annotations(
        read_only_hint = true,
        idempotent_hint = true,
        open_world_hint = true
    )
)]
pub async fn search_data(params: Parameters<SearchParams>) -> Vec<String> {
    // Search logic
}
```

### Rich content

Return structured content from tools:

```rust
use rmcp::model::{ToolResponseContent, TextContent, ImageContent};

#[tool]
async fn analyze_code(params: Parameters<CodeParams>) -> ToolResponseContent {
    ToolResponseContent::from(vec![
        TextContent::text(format!("Analysis of {}:", params.inner().filename)),
        TextContent::text("No issues found."),
    ])
}
```

## Prompts

### Prompt handlers

Implement prompt handlers:

```rust
use rmcp::model::{Prompt, PromptArgument, PromptMessage, GetPromptResult};

async fn list_prompts(
    &self,
    _request: Option<PaginatedRequestParam>,
    _context: RequestContext<RoleServer>,
) -> Result<ListPromptsResult, ErrorData> {
    let prompts = vec![
        Prompt {
            name: "code-review".to_string(),
            description: Some("Review code for best practices".to_string()),
            arguments: Some(vec![
                PromptArgument {
                    name: "language".to_string(),
                    description: Some("Programming language".to_string()),
                    required: Some(true),
                },
            ]),
        },
    ];
    
    Ok(ListPromptsResult { prompts })
}

async fn get_prompt(
    &self,
    request: GetPromptRequestParam,
    _context: RequestContext<RoleServer>,
) -> Result<GetPromptResult, ErrorData> {
    match request.name.as_str() {
        "code-review" => {
            let language = request.arguments
                .as_ref()
                .and_then(|args| args.get("language"))
                .ok_or_else(|| ErrorData::invalid_params("language required"))?;
            
            Ok(GetPromptResult {
                description: Some("Code review prompt".to_string()),
                messages: vec![
                    PromptMessage::user(format!(
                        "Review this {} code for best practices and suggest improvements",
                        language
                    )),
                ],
            })
        }
        _ => Err(ErrorData::invalid_params("Unknown prompt")),
    }
}
```

## Resources

### Resource handlers

Implement resource handlers:

```rust
use rmcp::model::{Resource, ResourceContents, ReadResourceResult};

async fn list_resources(
    &self,
    _request: Option<PaginatedRequestParam>,
    _context: RequestContext<RoleServer>,
) -> Result<ListResourcesResult, ErrorData> {
    let resources = vec![
        Resource {
            uri: "file:///data/config.json".to_string(),
            name: "Configuration".to_string(),
            description: Some("Server configuration".to_string()),
            mime_type: Some("application/json".to_string()),
        },
    ];
    
    Ok(ListResourcesResult { resources })
}

async fn read_resource(
    &self,
    request: ReadResourceRequestParam,
    _context: RequestContext<RoleServer>,
) -> Result<ReadResourceResult, ErrorData> {
    match request.uri.as_str() {
        "file:///data/config.json" => {
            let content = r#"{"version": "1.0", "enabled": true}"#;
            Ok(ReadResourceResult {
                contents: vec![
                    ResourceContents::text(content.to_string())
                        .with_uri(request.uri)
                        .with_mime_type("application/json"),
                ],
            })
        }
        _ => Err(ErrorData::invalid_params("Unknown resource")),
    }
}
```

## Transports

### Stdio transport

Standard input/output transport for CLI integration:

```rust
use rmcp::transport::StdioTransport;

let transport = StdioTransport::new();
let server = Server::builder()
    .with_handler(handler)
    .build(transport)?;
```

### SSE transport

HTTP-based SSE transport:

```rust
use rmcp::transport::SseServerTransport;
use std::net::SocketAddr;

let addr: SocketAddr = "127.0.0.1:8000".parse()?;
let transport = SseServerTransport::new(addr);

let server = Server::builder()
    .with_handler(handler)
    .build(transport)?;

server.run(signal::ctrl_c()).await?;
```

### Streamable HTTP transport

HTTP streaming transport with Axum:

```rust
use rmcp::transport::StreamableHttpTransport;
use axum::{Router, routing::post};

let transport = StreamableHttpTransport::new();
let app = Router::new()
    .route("/mcp", post(transport.handler()));

let listener = tokio::net::TcpListener::bind("127.0.0.1:3000").await?;
axum::serve(listener, app).await?;
```

### Custom transports

Implement custom transports (TCP, Unix Socket, WebSocket):

```rust
use rmcp::transport::Transport;
use tokio::net::TcpListener;

// See examples/transport/ for TCP, Unix Socket, WebSocket implementations
```

## Error Handling and Result Boundaries

### MCP errors

Return proper MCP errors:

```rust
use rmcp::ErrorData;

fn validate_params(value: &str) -> Result<(), ErrorData> {
    if value.is_empty() {
        return Err(ErrorData::invalid_params("Value cannot be empty"));
    }
    Ok(())
}

async fn call_tool(
    &self,
    request: CallToolRequestParam,
    context: RequestContext<RoleServer>,
) -> Result<CallToolResult, ErrorData> {
    validate_params(&request.name)?;
    
    // Tool execution...
    
    Ok(CallToolResult {
        content: vec![TextContent::text("Success")],
        is_error: Some(false),
    })
}
```

### Application errors

Use `anyhow` for application-level errors:

```rust
use anyhow::{Context, Result};

async fn load_config() -> Result<Config> {
    let content = tokio::fs::read_to_string("config.json")
        .await
        .context("Failed to read config file")?;
    
    let config: Config = serde_json::from_str(&content)
        .context("Failed to parse config")?;
    
    Ok(config)
}
```

## Testing

### Unit tests

Write unit tests for tools and handlers:

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_calculate_add() {
        let params = Parameters::new(CalculateParams {
            a: 5.0,
            b: 3.0,
            operation: "add".to_string(),
        });
        
        let result = calculate(params).await.unwrap();
        assert_eq!(result, 8.0);
    }
    
    #[tokio::test]
    async fn test_divide_by_zero() {
        let params = Parameters::new(CalculateParams {
            a: 5.0,
            b: 0.0,
            operation: "divide".to_string(),
        });
        
        let result = calculate(params).await;
        assert!(result.is_err());
    }
}
```

### Integration tests

Test complete server interactions:

```rust
#[tokio::test]
async fn test_server_list_tools() {
    let handler = MyServerHandler::new();
    let context = RequestContext::default();
    
    let result = handler.list_tools(None, context).await.unwrap();
    
    assert!(!result.tools.is_empty());
    assert!(result.tools.iter().any(|t| t.name == "calculate"));
}
```

## Progress Notifications

### Progress reporting

Send progress notifications during long-running operations:

```rust
use rmcp::model::ProgressNotification;

#[tool]
async fn process_large_file(
    params: Parameters<ProcessParams>,
    context: RequestContext<RoleServer>,
) -> Result<String, String> {
    let total = 100;
    
    for i in 0..=total {
        // Do work...
        
        if i % 10 == 0 {
            context.notify_progress(ProgressNotification {
                progress: i,
                total: Some(total),
            }).await.ok();
        }
    }
    
    Ok("Processing complete".to_string())
}
```

## OAuth Authentication

### OAuth configuration

Implement OAuth for secure access:

```rust
use rmcp::oauth::{OAuthConfig, OAuthProvider};

let oauth_config = OAuthConfig {
    authorization_endpoint: "https://auth.example.com/authorize".to_string(),
    token_endpoint: "https://auth.example.com/token".to_string(),
    client_id: env::var("CLIENT_ID")?,
    client_secret: env::var("CLIENT_SECRET")?,
    scopes: vec!["read".to_string(), "write".to_string()],
};

let oauth_provider = OAuthProvider::new(oauth_config);
// See examples/servers/complex_auth_sse.rs for complete implementation
```

## Performance and State

### Async operations

Use async/await for non-blocking operations:

```rust
#[tool]
async fn fetch_data(params: Parameters<FetchParams>) -> Result<String, String> {
    let client = reqwest::Client::new();
    let response = client
        .get(&params.inner().url)
        .send()
        .await
        .map_err(|e| e.to_string())?;
    
    let text = response.text().await.map_err(|e| e.to_string())?;
    Ok(text)
}
```

### Shared state

Use `Arc` and `RwLock` for shared state:

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct ServerState {
    counter: Arc<RwLock<i32>>,
}

impl ServerState {
    pub fn new() -> Self {
        Self {
            counter: Arc::new(RwLock::new(0)),
        }
    }
    
    pub async fn increment(&self) -> i32 {
        let mut counter = self.counter.write().await;
        *counter += 1;
        *counter
    }
}
```

## Logging and Tracing

### Tracing setup

Configure tracing for observability:

```rust
use tracing::{info, warn, error, debug};
use tracing_subscriber;

fn init_logging() {
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::DEBUG)
        .with_target(false)
        .with_thread_ids(true)
        .init();
}

#[tool]
async fn my_tool(params: Parameters<MyParams>) -> String {
    debug!("Tool called with params: {:?}", params);
    info!("Processing request");
    
    // Tool logic...
    
    info!("Request completed");
    "Done".to_string()
}
```

## Packaging and Deployment

### Binary distribution

Build optimized release binaries:

```bash
cargo build --release --target x86_64-unknown-linux-gnu
cargo build --release --target x86_64-pc-windows-msvc
cargo build --release --target x86_64-apple-darwin
```

### Cross-compilation

Use cross for cross-platform builds:

```bash
cargo install cross
cross build --release --target aarch64-unknown-linux-gnu
```

### Docker deployment

Create a Dockerfile:

```dockerfile
FROM rust:1.75 as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates
COPY --from=builder /app/target/release/my-mcp-server /usr/local/bin/
CMD ["my-mcp-server"]
```
## Good / Bad Examples

The examples below illustrate tool implementation that preserves async execution, typed parameters, annotations, and MCP error boundaries.

**Good:**

```rust
#[tool(name = "calculate", annotations(read_only_hint = true, idempotent_hint = true))]
pub async fn calculate(params: Parameters<CalculateParams>) -> Result<f64, String> {
    let p = params.inner();
    match p.operation.as_str() {
        "divide" if p.b == 0.0 => Err("Division by zero".to_string()),
        "divide" => Ok(p.a / p.b),
        "add" => Ok(p.a + p.b),
        _ => Err(format!("Unknown operation: {}", p.operation)),
    }
}
```

Why: The tool is asynchronous, uses `Parameters<CalculateParams>`, declares read-only and idempotent behavior, and returns a typed success or explicit error.

**Bad:**

```rust
fn calculate(operation: String) -> f64 {
    if operation == "divide" { 1.0 / 0.0 } else { 0.0 }
}
```

Why: The function is not an MCP `#[tool]`, has no schema-bearing parameter type, hides failure semantics, and cannot be routed through `ToolRouter` or `ServerHandler`.

## Conventions

| Rule | Rationale |
| --- | --- |
| Declare `rmcp = { version = "0.8.1", features = ["server"] }`, `tokio`, `serde`, `serde_json`, `anyhow`, `tracing`, and `tracing-subscriber` in `Cargo.toml` for SDK servers; add `rmcp-macros` and `schemars` when using macros. | Explicit dependencies keep server, macro, schema, async runtime, and observability behavior reproducible. |
| Keep `src/main.rs`, `handler.rs`, `tools/`, `prompts/`, `resources/`, and `tests/integration_tests.rs` separated by MCP concern. | Routing, protocol handling, and feature implementations remain navigable as servers grow. |
| Build servers with `Server::builder()`, `StdioTransport::new()`, `ServerCapabilities`, `ServerHandler`, `RequestContext<RoleServer>`, and `ErrorData`. | The handler advertises only supported capabilities and returns protocol-correct failures. |
| Define tools with `#[tool]`, `Parameters<T>`, `JsonSchema`, and `ToolRouter`; use `#[tool_router]` and `#[tool_handler]` when macro routing fits. | Clients receive accurate schemas and the server avoids hand-written dispatch drift. |
| Set tool annotations such as `read_only_hint`, `destructive_hint`, `idempotent_hint`, and `open_world_hint` truthfully. | Hosts use these hints to protect users from unsafe or surprising tool execution. |
| Use `Prompt`, `PromptArgument`, `PromptMessage`, `GetPromptResult`, `Resource`, `ResourceContents`, and `ReadResourceResult` for prompts and resources. | Prompt and resource responses stay compatible with the MCP model. |
| Choose `StdioTransport`, `SseServerTransport`, `StreamableHttpTransport`, or custom `Transport` based on the hosting boundary. | CLI, HTTP, Axum, TCP, Unix Socket, and WebSocket deployments have different lifecycle and security needs. |
| Return `ErrorData::invalid_params` for protocol validation failures and `anyhow::Context` for application setup failures. | Clients receive actionable MCP errors while internal operations keep diagnostic context. |
| Cover tool behavior and server interactions with `#[tokio::test]` unit and integration tests. | Async behavior, routing, and list/call handlers fail before release. |
| Use `ProgressNotification`, OAuth `OAuthConfig`/`OAuthProvider`, `Arc<RwLock<_>>`, and `tracing` only when the server behavior requires them. | Long-running, authenticated, stateful, and observable servers need explicit primitives rather than ad hoc globals. |
| Build release artifacts with `cargo build --release`, `cross build --release`, or a Docker multi-stage build. | Distribution targets remain optimized and reproducible. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `async`/`await` throughout tool, prompt, resource, and transport handlers. | Block the runtime or hide async work behind synchronous wrappers. |
| Advertise only implemented `tools`, `prompts`, and `resources` in `ServerCapabilities`. | Claim capabilities that the `ServerHandler` does not implement. |
| Return `ToolResponseContent` with `TextContent` or `ImageContent` when a tool needs rich content. | Flatten structured results into ambiguous strings when the model supports richer responses. |
| Validate parameters and return `ErrorData` or `Result<_, String>` with clear messages. | Panic, unwrap untrusted input, or return empty success for failed operations. |
| Use `context.notify_progress(ProgressNotification { progress, total })` for long-running tools. | Leave users without feedback during large file or network operations. |
| Read `CLIENT_ID` and `CLIENT_SECRET` from the environment for OAuth examples. | Hardcode credentials, token endpoints, or client secrets in source. |
| Use `VS`-independent Rust tests and target-specific release builds. | Ship an untested debug binary as the server artifact. |

## Checklist Before Opening a PR

- [ ] `Cargo.toml` contains the required `rmcp`, async runtime, serialization, error, tracing, macro, and schema dependencies used by the server.
- [ ] Server capabilities match the implemented `ServerHandler` methods for tools, prompts, and resources.
- [ ] Tool parameters derive `Deserialize` and `JsonSchema`, use `Parameters<T>`, and expose truthful annotations.
- [ ] Prompt and resource handlers validate names and URIs and return `ErrorData::invalid_params` for unknown requests.
- [ ] Transport selection matches the deployment boundary: stdio for CLI, SSE or streamable HTTP for networked servers, custom `Transport` only when needed.
- [ ] Long-running operations use async I/O, progress notifications when useful, and shared state through `Arc<RwLock<_>>` or another safe primitive.
- [ ] OAuth configuration reads `CLIENT_ID` and `CLIENT_SECRET` from the environment and preserves the configured authorization and token endpoints.
- [ ] Unit tests and integration tests cover tool success, tool errors, and server list/call behavior.
- [ ] Release, cross-compilation, or Docker packaging commands have been run for the intended target.

## References

- [rmcp Documentation](https://docs.rs/rmcp)
- [rmcp-macros Documentation](https://docs.rs/rmcp-macros)
- [Examples Repository](https://github.com/modelcontextprotocol/rust-sdk/tree/main/examples)
- [MCP Specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [Rust Async Book](https://rust-lang.github.io/async-book/)
- OAuth authorization example endpoint: https://auth.example.com/authorize
- OAuth token example endpoint: https://auth.example.com/token
