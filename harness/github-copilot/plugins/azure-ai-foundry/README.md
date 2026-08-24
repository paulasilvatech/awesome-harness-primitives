# Azure AI Foundry Plugin

Azure AI Foundry agent development toolkit covering Agent Service synchronization, hosted agents with AG-UI frontends, Microsoft Agent Framework and Semantic Kernel, gateway and API governance, semantic caching, agent identity, and evaluation loops.

## Installation

```bash
copilot plugin install azure-ai-foundry@copilot-primitives
```

## What's Included

### Skills

| Skill | Description |
|-------|-------------|
| `foundry-agent-sync` | Create, register, deploy, update, and synchronize prompt-based Foundry agents from a local manifest through the Agent Service REST API. |
| `foundry-hosted-agent-copilotkit` | Build CopilotKit frontends over AG-UI against Microsoft Agent Framework agents and Foundry hosted agents, including human-in-the-loop approval and the deploy loop. |
| `microsoft-agent-framework` | Create, refactor, and review Microsoft Agent Framework agents, workflows, and migrations in .NET or Python. |
| `semantic-kernel` | Build Semantic Kernel applications, plugins, and function-calling flows with Azure OpenAI and Foundry connectors. |
| `apim-ai-gateway` | Put API Management in front of Foundry inference endpoints with token limits, managed identity, backend pools, and content safety. |
| `azure-api-center` | Govern the API and MCP catalog that agents discover and call. |
| `azure-managed-redis-cache` | Design semantic cache, vector memory, and agent session state on Azure Managed Redis. |
| `entra-agent-user` | Create Microsoft Entra agent users so agents can act with a user-backed identity. |
| `agentic-eval` | Run evaluator-optimizer, rubric, and LLM-as-judge loops over agent output. |

## Related primitives outside this package

GitHub Copilot plugin manifests support `agents`, `skills`, `commands`, `hooks`, `extensions`,
`mcpServers`, and `lspServers`. Repository instructions and VS Code prompt files are not plugin
components, so the following Foundry assets ship through their own repository discovery paths
instead of this package:

| Primitive | Type | Where it lives |
|-----------|------|----------------|
| `microsoft-foundry` | instructions | `.github/instructions/` — Foundry Python SDK v2 agent conventions |
| `azure-apim-ai-gateway` | instructions | `.github/instructions/` — APIM AI gateway policy conventions |
| `design-agentic-system` | prompt | `.github/prompts/` — VS Code-only guided design workflow |

## Source

Skills in this package are generated copies of canonical shared sources under
`harness/github-copilot/skills/`. Edit the canonical source and run
`python3 harness/github-copilot/scripts/sync_plugin_components.py`.
