# Fabric MCP setup

The `fabric-agentic-plugin` package registers two Agent Plugins 1.0 MCP servers in its root `mcp.json`:

| Server | Purpose |
| --- | --- |
| `FabricIQ` | Fabric AI Hub and Power BI data exploration. |
| `fabric-sqlendpoint` | SQL endpoint query execution. |

Confirm the concrete tool names in the active session before invoking them. If a server is unavailable, use a specialist guide's documented REST, Azure CLI, Fabric CLI, or TDS fallback. Do not invent a fallback or silently change from a read-only path to a write path.

Authentication is supplied by the compatible host and target tenant. This package stores no token, connection string, or client secret.
