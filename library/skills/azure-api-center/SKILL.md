---
name: azure-api-center
description: "Govern APIs and agent tools at enterprise scale with Azure API Center: a central catalog of APIs, versions, definitions (OpenAPI), environments, and deployments, plus registration of agent tools and MCP servers for discovery and reuse. Use when designing API governance for an agentic platform, building a tool or MCP registry for agents, enforcing API standards with the API Center linter, or making backend APIs discoverable to agent builders. Pairs with apim-ai-gateway (runtime gateway), foundry-agent-blueprint (tool consumption), and agentic-architecture-patterns (tools and MCP)."
argument-hint: "what to govern, for example a central tool and MCP catalog for agent builders"
---

# Azure API Center

Azure API Center is the **inventory and governance** plane for APIs and agent tools. Where API Management is the runtime gateway, API Center is the catalog: every API, version, definition, environment, and deployment in one governed place, including the tools and MCP servers that agents call.

> Confirm current API Center capabilities (MCP registration, linting rules, portal features) on Microsoft Learn before committing a design. Do not assert a feature without a source.

## Why it matters for agents

Agents act through tools. As an agentic platform grows, tools and MCP servers proliferate. API Center gives you:

- A **single catalog** of APIs and tools, versioned and searchable.
- **Governance**: enforce naming, security, and documentation standards with the linter and metadata.
- **Discovery**: agent builders find approved tools instead of reinventing or calling ungoverned endpoints.
- **Lifecycle**: track environments (dev, staging, production) and deployments per API.

## Core concepts

| Concept | Purpose |
| --- | --- |
| API | A logical API entry, with one or more versions |
| Version | A specific version of an API |
| Definition | The contract, typically an OpenAPI document |
| Environment | A deployment environment (for example Azure API Management, a Kubernetes cluster) |
| Deployment | A runtime location where a version is available |
| Metadata | Custom properties used to enforce and report governance |

## Design steps

1. **Model the catalog.** Decide the metadata schema (owner, classification, lifecycle stage, data sensitivity, cost center). This drives governance and reporting.
2. **Register APIs and tools.** Import OpenAPI definitions for backend APIs and for HTTP tools the agents call. Register MCP servers so agents can discover them.
3. **Link environments and deployments.** Connect API Management instances and other runtimes so the catalog reflects where each API actually runs.
4. **Govern.** Apply the linter and required metadata. Fail registration that misses security or documentation standards.
5. **Publish discovery.** Expose the API Center portal (or the VS Code extension) so agent builders can browse approved tools.

## How it fits the platform

```text
Backend APIs / Tools / MCP servers
        |  register definitions and metadata
   Azure API Center  (inventory + governance + discovery)
        |  reference governed APIs
   Azure API Management  (runtime AI gateway: authN, token limit, cache)
        |
   Agents (Foundry, Container Apps) select and call governed tools
```

- Pair with `apim-ai-gateway` for the runtime path: API Center governs and catalogs, API Management enforces and routes.
- Pair with `agentic-architecture-patterns` (tools and MCP) for tool design quality.
- Agents in `foundry-agent-blueprint` consume the cataloged APIs as OpenAPI or MCP tools.

## References

- [Azure API Center](https://learn.microsoft.com/azure/api-center/)
- [Register APIs in API Center](https://learn.microsoft.com/azure/api-center/register-apis)
- [API governance and linting](https://learn.microsoft.com/azure/api-center/enable-api-analysis-linting)
- [API Center and API Management](https://learn.microsoft.com/azure/api-center/)
