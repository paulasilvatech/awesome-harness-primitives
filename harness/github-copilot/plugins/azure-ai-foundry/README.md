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
| `agentic-eval` | Design evaluator-optimizer, reflection, rubric, LLM-as-judge, and test-driven refinement loops for AI agent outputs. |
| `apim-ai-gateway` | Design Azure API Management as the runtime AI gateway for model and tool traffic, including token-per-minute controls, token limits, quotas, multi-backend load-balanced backend pools, circuit breakers, semantic caching, token metrics, managed identity, and content safety. |
| `azure-agentic-architecture-patterns` | Provides a decision framework for production multi-agent and AI-native systems on GitHub and Azure AI Foundry. |
| `azure-ai` | Build on Azure AI services including AI Search, Speech, Azure OpenAI, and Document Intelligence, covering keyword, vector, hybrid, and semantic search, speech-to-text, text-to-speech, transcription, and OCR. |
| `azure-api-center` | Design Azure API Center as the enterprise inventory and governance plane for APIs, agent tools, OpenAPI definitions, environments, deployments, metadata, linting, and MCP server discovery. |
| `azure-managed-redis-cache` | Use when designing or provisioning Azure Managed Redis for cache, semantic cache, vector memory, session store, or agent memory in AI-native systems; produces SKU guidance, network and identity controls, Bicep deployment steps, and integration recommendations. DO NOT USE FOR: general agent architecture (use agentic-architecture-patterns), Foundry agent runtime design (use foundry-agent-blueprint), or general Azure infrastructure (use azure-infrastructure). Triggers include \"design Redis semantic cache\", \"provision Azure Managed Redis\", \"add vector memory\". |
| `entra-agent-user` | Create Agent Users in Microsoft Entra ID from Agent Identities, enabling AI agents to act as digital workers with user identity capabilities in Microsoft 365 and Azure environments. |
| `foundry-agent-sync` | Create, register, deploy, update, and synchronize prompt-based Azure AI Foundry agents from a local JSON manifest using the Agent Service REST API. |
| `foundry-hosted-agent-copilotkit` | Guide ongoing development of CopilotKit frontends connected over AG-UI to Microsoft Agent Framework agents and Azure AI Foundry hosted agents. |
| `microsoft-agent-framework` | Create, update, refactor, explain, or review Microsoft Agent Framework applications, agents, workflows, and migrations in .NET or Python. |
| `semantic-kernel` | Create, update, refactor, explain, or review Semantic Kernel applications, plugins, function-calling flows, and AI integrations in .NET or Python. |

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
