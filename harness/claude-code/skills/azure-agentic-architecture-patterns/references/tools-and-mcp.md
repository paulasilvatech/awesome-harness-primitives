# Tools and MCP

Agents act through tools. The quality of tool descriptions and the discipline of the tool surface drive how reliably an agent selects and calls them.

## Tool design

- **Describe for selection.** Each tool needs a clear name, a one-line purpose, and typed parameters with descriptions. The model selects tools from these descriptions, so write them for a reader who cannot see the code.
- **Keep the surface small.** Every extra tool adds selection cost and error surface. Curate. Group rarely used tools behind a router tool or a separate agent.
- **Namespace.** Prefix tool names by domain to avoid collisions and to help selection.
- **Validate at the boundary.** Treat tool arguments from the model as untrusted input. Validate and sanitize before executing.
- **Return structured, compact results.** Large raw payloads waste context. Return what the agent needs, with a reference for the rest.

## Model Context Protocol (MCP)

MCP is the open standard for exposing tools, resources, and prompts to agents over a uniform protocol. Prefer MCP servers when a capability should be reusable across agents and hosts.

- Build MCP servers with the `mcp-builder` skill (Python FastMCP or TypeScript SDK).
- An MCP server exposes **tools** (actions), **resources** (readable context), and **prompts** (templates).
- Hosts that speak MCP (including GitHub Copilot and Foundry-based agents) can discover and call these without bespoke glue.

## Governance

Register tools and MCP servers in **Azure API Center** so they are discoverable, versioned, and governed (see `azure-api-center`). Front HTTP tool backends with **Azure API Management** for authN, rate limits, and observability (see `apim-ai-gateway`).

## Security checklist

- Authenticate every tool call. Prefer managed identity and Entra Agent ID over shared secrets (see guardrails-and-identity.md).
- Apply least privilege per tool. A read tool must not hold write scope.
- Guard against prompt injection that targets tools (a retrieved document instructing the agent to call a destructive tool). Use Prompt Shields and human approval for high-impact actions.
- Log every tool invocation with inputs, outputs, and identity for audit.

## Sources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Azure API Center](https://learn.microsoft.com/azure/api-center/)
- [Azure AI Foundry Agent Service tools](https://learn.microsoft.com/azure/ai-foundry/agents/)
