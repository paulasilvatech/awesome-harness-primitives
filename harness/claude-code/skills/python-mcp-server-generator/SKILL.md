---
name: python-mcp-server-generator
description: >-
  Generate a complete Python Model Context Protocol server project using uv, mcp[cli], FastMCP,
  typed tools, optional resources and prompts, stdio or streamable-http transport, error handling,
  and testing instructions. Use when the user asks to generate a Python MCP server, create an MCP
  tool server, scaffold FastMCP, or build a streamable HTTP MCP service.
---

<!-- Generated from harness/github-copilot/skills/python-mcp-server-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Python MCP server generator

Create a production-ready Python MCP server project with `uv`, `mcp[cli]`, `FastMCP`, typed tools, validation, transport configuration, and runnable testing instructions.

## When to invoke

- "Generate a Python MCP server."
- "Create a FastMCP tool server with uv."
- "Scaffold an MCP server using streamable-http."
- "Add resources and prompts to a Python MCP server."
- "Build a typed MCP tool with error handling."

## Project structure

| File or element | Required | Purpose |
| --- | --- | --- |
| `pyproject.toml` | Yes | `uv init project-name` creates Python project metadata. |
| `mcp[cli]` dependency | Yes | `uv add "mcp[cli]"` installs the MCP SDK and CLI helpers. |
| `server.py` | Yes | Main server using `FastMCP` from `mcp.server.fastmcp`. |
| `.gitignore` | Yes | Python cache, virtualenv, build, and local env exclusions. |
| `if __name__ == "__main__"` | Yes | Allows direct execution. |
| README or usage notes | Yes | Shows run, inspect, and install commands. |

## Setup commands

```bash
uv init project-name
cd project-name
uv add "mcp[cli]"
```

Create the server entry point, commonly `server.py`, and configure direct execution.

## Server configuration

| Choice | Recommendation |
| --- | --- |
| Server class | Use `FastMCP` from `mcp.server.fastmcp`. |
| Server name | Set a clear name and optional instructions. |
| Local transport | Use stdio by default for local desktop or CLI clients. |
| Remote transport | Use `streamable-http` for remote clients. |
| HTTP options | Configure host, port, `stateless_http=True` for scalability, `json_response=True` when JSON responses are required, and CORS only for trusted browser clients. |
| ASGI integration | Mount to existing Starlette or FastAPI apps when the server is part of a larger web service. |

For HTTP testing, connect clients to `http://localhost:PORT/mcp`.

## Tool implementation rules

| Rule | Why |
| --- | --- |
| Decorate tools with `@mcp.tool()` | Registers callable MCP tools. |
| Type every parameter and return value | Type hints generate schemas automatically. |
| Write clear docstrings | Docstrings become tool descriptions. |
| Use Pydantic models or TypedDicts for structured output | Keeps responses schema-safe. |
| Use async functions for I/O-bound work | Avoids blocking the server. |
| Validate inputs early | Produces clear errors and safer tools. |
| Raise or return clear errors | Helps clients remediate failures. |
| Log to stderr or use Context logging | Avoids stdout pollution in stdio servers. |
| Clean up resources with context managers or lifespan hooks | Prevents leaked connections. |

## Optional MCP capabilities

| Capability | Decorator or API | Use when |
| --- | --- | --- |
| Resources | `@mcp.resource()` | Clients need read-only data exposed by URI. |
| Dynamic resources | URI templates such as `resource://{param}` | Resource identity depends on a parameter. |
| Prompts | `@mcp.prompt()` | Reusable prompt templates help clients invoke workflows. |
| Context | Context logging, progress, and notifications | Long-running or observable operations need status. |
| Sampling | LLM sampling | A tool intentionally delegates generation to a model. |
| Elicitation | User input elicitation | A workflow needs interactive user input. |
| Lifespan | Lifespan management | Shared databases, connections, or clients must be initialized and closed. |
| Image handling | `Image` class | Tools return or process images. |
| Completion | Completion support | Better UX for constrained or discoverable arguments. |

## Tool ideas

- Data processing and transformation.
- File system read, analyze, or search operations.
- External API integrations.
- Database queries.
- Text analysis or generation with sampling.
- System information retrieval.
- Math or scientific calculations.

## Testing and installation

| Scenario | Command |
| --- | --- |
| Run stdio server directly | `python server.py` or `uv run server.py` |
| Run MCP Inspector | `uv run mcp dev server.py` |
| Install to Claude Desktop | `uv run mcp install server.py` |
| Run HTTP server | `python server.py`, then connect to `http://localhost:PORT/mcp` |

Test tools independently before relying on LLM integration. Include example tool invocations in the generated README.

## Gotchas

- **Type hints are not optional**: missing hints produce weak or missing schemas.
- **Do not print logs to stdout in stdio mode**: stdout is protocol traffic; use stderr or Context logging.
- **Do not make every operation sync**: I/O-bound APIs and databases should use async/await.
- **Do not skip cleanup**: shared clients and database connections need context managers or lifespan management.

The optional `Resource/Prompt` section can use URI templates like `"resource://{param}"`. HTTP servers can mount into `Starlette/FastAPI`; I/O code should use `async/await`.

## Output template

```markdown
## Python MCP server generated

**Status:** complete | blocked
**Project:** `<project-name>`
**Transport:** `stdio | streamable-http`

### Files created
| File | Purpose |
| --- | --- |
| `pyproject.toml` | `<dependencies and metadata>` |
| `server.py` | `<FastMCP server and tools>` |
| `.gitignore` | `<Python ignores>` |
| `README.md` | `<run/test/install instructions>` |

### Validation
- `uv run mcp dev server.py`: `<pass/fail/not run>`
- Direct run: `<pass/fail/not run>`
- Example tool invocation: `<pass/fail/not run>`
```

## Quality gate

- [ ] Project was initialized with `uv init project-name` or equivalent `uv` structure.
- [ ] `mcp[cli]` was added with `uv add "mcp[cli]"`.
- [ ] Server uses `FastMCP` from `mcp.server.fastmcp`.
- [ ] Transport is explicitly stdio or `streamable-http`.
- [ ] At least one useful `@mcp.tool()` has type hints, docstring, validation, and error handling.
- [ ] Optional `@mcp.resource()` and `@mcp.prompt()` are included only when useful.
- [ ] Structured outputs use Pydantic models or TypedDicts when appropriate.
- [ ] Logs avoid stdout pollution in stdio mode.
- [ ] README or final notes include `uv run mcp dev server.py`, `uv run mcp install server.py`, and direct run instructions.
