---
name: foundry-agent-blueprint
description: >-
  Foundry agent blueprint maps agent designs to Azure AI Foundry Agent Service models, connections, tools, memory, evaluation, and tracing. Use this skill when designing Foundry agent runtimes, model catalog choices, Azure AI Search or Redis connections, Bing connections, OpenAPI tools, MCP tools, code interpreter, file search, threads, runs, or evaluation plans.
---

# Foundry Agent Blueprint

How to design an agent on **Azure AI Foundry Agent Service** and map the agentic decisions to Foundry primitives. This skill is the design layer; for hands-on provisioning, CLI, and SDK detail, load the installed `microsoft-foundry`, `azure-ai`, and `vscode-microsoft-foundry` skills, and verify against Microsoft Learn.

> Service capabilities and names evolve. Confirm the current Foundry Agent Service features, model catalog entries, and limits on Microsoft Learn before locking a recommendation. Do not quote limits or prices without a source.

## When to invoke

- "Design an agent on Azure AI Foundry Agent Service."
- "Map model, memory, tools, and guardrails to Foundry primitives."
- "Choose Foundry model catalog deployments and connections."
- "Plan Foundry tools such as OpenAPI, MCP, code interpreter, or file search."
- "Create a Foundry evaluation and tracing blueprint."

## Criteria

### Foundry primitives, mapped to the seven decisions

| Agentic decision | Foundry primitive |
| --- | --- |
| Model routing | Model catalog deployments; a model router where available; the gateway in front (see `apim-ai-gateway`) |
| Caching | Prompt caching on supported models; semantic cache at the gateway or in app (see `azure-managed-redis-cache`) |
| Short term memory | Threads and runs (managed conversation state) |
| Long term memory | Connections to Azure AI Search or Azure Managed Redis vector store |
| Context curation | File search tool, Azure AI Search connection, your own RAG pipeline |
| Tools and MCP | Function tools, OpenAPI tools, MCP tools, code interpreter, file search |
| Identity and guardrails | Microsoft Entra Agent ID, managed identity, Content Safety, Prompt Shields |
| Evaluation and observability | Foundry evaluation framework and tracing, App Insights, OpenTelemetry |

### Blueprint steps

1. **Project and models.** Create a Foundry project. Pick models from the catalog for each routing tier (a small model for routing and extraction, a workhorse for general steps, a premium or frontier model for hard steps). Create deployments.
2. **Connections.** Add the connections the agent needs: Azure AI Search for retrieval, Azure Managed Redis for cache and memory, storage for files, and any other data source. Use managed identity on connections where supported.
   - Note from prior experience: a Foundry `AzureStorageAccount` connection target must be the Blob URI (`https://<account>.blob.core.windows.net`), not the ARM resource id.
3. **Agent definition.** Define the agent with its instructions, model, and tools. Keep the tool surface small and well described (see tools and MCP in `agentic-architecture-patterns`).
4. **Threads.** Use threads for short term memory. Add long term memory through a retrieval tool or connection, scoped by tenant and user.
5. **Guardrails and identity.** Give the agent an Entra Agent ID, use managed identity for service access, and enable Content Safety and Prompt Shields.
6. **Evaluation.** Build an eval set and run the Foundry evaluators (relevance, groundedness, coherence, safety, task success). Gate changes in CI.
7. **Observability.** Enable tracing and route telemetry to App Insights with OpenTelemetry GenAI conventions.

### Tools available in Foundry agents

- **Function tools** for your own code.
- **OpenAPI tools** to call governed HTTP APIs (register them in `azure-api-center`, front them with `apim-ai-gateway`).
- **MCP tools** to attach Model Context Protocol servers (build them with `mcp-builder`).
- **File search** for grounded retrieval over uploaded documents.
- **Code interpreter** for computation and data tasks.

### Provisioning and quotas

- For provisioning steps, identity setup, and SDK usage, route to `microsoft-foundry` and `azure-ai`.
- For model and Cognitive Services quota, the `az quota list` path can return a bad request; raise a support quota request for Cognitive Services instead. New subscriptions may need `Microsoft.ContainerRegistry` registered before creating an ACR for hosted-agent demos.

### References

- [Azure AI Foundry Agent Service](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Azure AI Foundry model catalog](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview)
- [Foundry tools](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/overview)
- [Evaluate generative AI with Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai)

## Output template

Return exactly this structure:

```markdown
Foundry Agent Blueprint

**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the recommended Foundry agent design.

### Details
- Agent purpose: target runtime and task scope
- Models and routing: catalog deployments, tiers, and rationale
- Connections: Azure AI Search, Azure Managed Redis, storage, Bing, or other data sources
- Tools: function, OpenAPI, MCP, file search, code interpreter, and governance notes
- Memory and context: threads, runs, retrieval, tenant and user scoping
- Guardrails and identity: Entra Agent ID, managed identity, Content Safety, Prompt Shields
- Evaluation and observability: eval set, evaluators, tracing, App Insights, OpenTelemetry

### Validation
- Decision coverage: PASS | FAIL with evidence for the seven decisions
- Currentness check: PASS | FAIL | SKIPPED with Microsoft Learn verification status
- Handoff check: PASS | FAIL with provisioning, Redis, or architecture primitives needed next
```

## Limits

- Do not use this skill for provisioning Foundry infrastructure.
- Use `ai-foundry-operations` (`skill`) instead when the task requires resource creation, deployment commands, identity setup, or SDK operations.
- Do not use this skill for general agent architecture tradeoffs.
- Use `agentic-architecture-patterns` (`skill`) instead when the platform-independent architecture decisions come first.
- Do not use this skill for Redis implementation details.
- Use `azure-managed-redis-cache` (`skill`) instead when choosing Redis SKU, vector search, RedisVL, tenant isolation, Entra access, or private networking details.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `ai-foundry-operations` | `skill` | The blueprint must become Foundry provisioning, model deployment, RAG, or endpoint operations. |
| `agentic-architecture-patterns` | `skill` | The design needs broader agent architecture decisions before Foundry mapping. |
| `azure-managed-redis-cache` | `skill` | Cache, semantic cache, vector memory, or session state needs Redis design detail. |
| `azure-infrastructure` | `skill` | The Foundry design depends on Azure networking, identity, private endpoints, or topology. |
| `open-horizons-architect` | `agent` | The blueprint is part of a larger architecture decision or design review. |

## Quality gate

- [ ] `name` matches the `foundry-agent-blueprint` directory.
- [ ] The seven decisions are covered: model routing, caching, short term memory, long term memory, context curation, tools and MCP, identity and guardrails, and evaluation and observability.
- [ ] Service capabilities, model catalog entries, limits, and prices are verified against Microsoft Learn before final recommendations quote them.
- [ ] Foundry-specific primitives are mapped without inventing services, SKUs, API versions, or model names.
- [ ] Provisioning, Redis, and broader architecture handoffs are called out when needed.
- [ ] The response follows the output template with validation evidence.
