---
name: rust-mcp-server-generator
description: >-
  Generate a complete Rust Model Context Protocol server project using the official rmcp SDK,
  including transports, tools, prompts, resources, state, tests, and client configuration. Use
  this skill when the user asks to create a Rust MCP server, rmcp project, MCP tool server,
  stdio/SSE/HTTP transport server, or project requirements for a Rust MCP implementation.
---

<!-- Generated from harness/github-copilot/skills/rust-mcp-server-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Rust MCP server generator

Collect the server requirements, read the bundled Rust MCP reference when implementing files, and generate a complete Rust project that builds, tests, and runs as an MCP server.

## When to invoke

- "Generate a Rust MCP server project."
- "Create an rmcp server with tools and prompts."
- "Build a stdio MCP tool server in Rust."
- "Add SSE and HTTP transports to a Rust MCP server."
- "Give me project requirements for a Rust MCP implementation."

## Inputs

Use `$ARGUMENTS` as the initial project brief. Extract project name, server description, transport type, tools, prompts, and resources from it. If any required detail is missing and interactive follow-up is unavailable, choose safe defaults and mark assumptions in the output.

## Prerequisites and context

- Generate Rust code against the official `rmcp` SDK patterns described in the bundled reference.
- `cargo` must be available to build and test the generated project.
- Supported transports are `stdio`, `sse`, `http`, or `all`.
- Stdio is the safest default when the user does not specify a transport.

## Project requirements

Ask or infer these fields before generating files:

| Requirement | Examples | Default when absent |
| --- | --- | --- |
| Project name | `my-mcp-server` | Kebab-case name derived from the request. |
| Server description | `A weather data MCP server` | One sentence based on the requested domain. |
| Transport type | `stdio`, `sse`, `http`, `all` | `stdio`. |
| Tools to include | `weather lookup`, `forecast`, `alerts` | One simple health or echo tool. |
| Prompts and resources | Include or omit prompt/resource modules | Include only when requested. |

## Project structure

Generate this directory tree, adding prompt and resource modules only when enabled:

```text
{project-name}/
├── Cargo.toml
├── .gitignore
├── README.md
├── src/
│   ├── main.rs
│   ├── handler.rs
│   ├── tools/
│   │   ├── mod.rs
│   │   └── {tool_name}.rs
│   ├── prompts/
│   │   ├── mod.rs
│   │   └── {prompt_name}.rs
│   ├── resources/
│   │   ├── mod.rs
│   │   └── {resource_name}.rs
│   └── state.rs
└── tests/
    └── integration_test.rs
```

## Implementation rules

| Area | Rule |
| --- | --- |
| rmcp macros | Use `#[tool]`, `#[tool_router]`, and `#[tool_handler]` where the reference shows they simplify routing. |
| Type safety | Use `schemars::JsonSchema` for every tool parameter type. |
| Errors | Return `Result` values with clear messages instead of panics. |
| Async | Make all handlers async. |
| Shared state | Use `Arc<RwLock<T>>` for mutable shared state. |
| Logging | Use `tracing` macros: `info!`, `debug!`, `warn!`, and `error!`. |
| Documentation | Add doc comments to public items. |
| Tests | Include unit tests for tools and integration tests for handlers. |

## Procedure

1. Resolve the project requirements and transport choice.
2. Read `references/templates-development-patterns.md` before writing Rust files or implementing tool patterns.
3. Create the project structure, `Cargo.toml`, `.gitignore`, `README.md`, source modules, and tests.
4. Add usage commands for the selected transports:
   - Stdio: `cargo run`
   - SSE: `cargo run --features http -- --transport sse`
   - HTTP: `cargo run --features http -- --transport http`
5. Add MCP client configuration examples for release binaries and local builds.
6. Run `cargo build` and `cargo test` when dependencies are available; report failures with exact output summaries.

## Progressive disclosure and bundled resources

- `references/templates-development-patterns.md`: Rust MCP server templates, development guidance, and tool implementation patterns. Read it before generating source files or deciding macro usage.

## Rust MCP terminology

Describe the result as `production-ready` only when build, test, error handling, tracing, and README instructions are present. Name `rmcp-macros` when explaining macro usage, and preserve the `Async/Await**` implementation concern as async handlers with awaited operations. Include the release path form `path/to/target/release/{project-name}` for clients that reference a built binary directly.

## Output template

```markdown
## Rust MCP server generation

**Status:** generated | blocked
**Project:** `{project-name}`
**Transport:** stdio | sse | http | all
**Assumptions:** <none or list>

### Files created
```text
{project-name}/
<generated tree>
```

### Usage
```bash
cd {project-name}
cargo build
cargo test
cargo run
cargo run --features http -- --transport sse
cargo run --features http -- --transport http
```

### MCP client configuration
```json
{
  "mcpServers": {
    "{project-name}": {
      "command": "path/to/{project-name}/target/release/{project-name}",
      "args": []
    }
  }
}
```

### Validation
- `cargo build`: pass | fail | not run
- `cargo test`: pass | fail | not run
```

## Quality gate

- [ ] Project name is valid kebab-case and used consistently in paths, package metadata, README, and MCP client configuration.
- [ ] Transport handling covers `stdio`, `sse`, `http`, or `all` as requested.
- [ ] Every tool has typed parameters with `schemars::JsonSchema` and async handlers returning `Result`.
- [ ] Shared mutable state uses `Arc<RwLock<T>>` when needed.
- [ ] Logging uses `tracing` macros rather than `println!` for server diagnostics.
- [ ] Unit and integration tests are generated and validation commands are reported.
- [ ] The bundled reference file was read before source generation.
