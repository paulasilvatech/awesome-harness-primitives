---
name: azure-agentic-architecture-patterns
description: >-
  Provides a decision framework for production multi-agent and AI-native systems on GitHub and
  Azure AI Foundry. Use this skill when designing model routing, prompt caching, semantic caching,
  memory, context curation, RAG, tools, MCP, identity, guardrails, evaluation, observability, or
  cost controls.
allowed-tools: >-
  mcp__com_microsoft_azure__cloudarchitect, mcp__com_microsoft_azure__documentation,
  mcp__com_microsoft_azure__foundry, mcp__com_microsoft_azure__get_azure_bestpractices
---

<!-- Generated from harness/github-copilot/skills/azure-agentic-architecture-patterns/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Agentic Architecture Patterns

This skill turns an AI-native use case into concrete architecture decisions for routing, caching, memory, context, tools, identity, guardrails, evaluation, observability, and cost, with reference files loaded only when depth is needed.

## When to invoke

- "Design an agentic architecture for this use case."
- "Choose model routing, caching, memory, RAG, tools, and guardrails for a multi-agent system."
- "Review this agent design for reliability, security, observability, and cost."
- "Map GitHub and Azure AI Foundry services for an AI-native workload."

## Prerequisites and context

- Read the use case and constraints: scale, latency, cost ceiling, data sensitivity, and runtime location.
- Never invent limits, prices, or benchmarks. Verify service limits and pricing against Microsoft Learn and the vendor model card, and cite them.
- Where a number has no source, state it as an explicit assumption.

## Criteria

### Seven architecture decisions

- [ ] **Model routing**: match each task to the cheapest model that meets quality. See `references/model-routing.md`.
- [ ] **Caching**: cut latency and cost with prompt caching and semantic caching. See `references/caching.md`.
- [ ] **Memory**: separate short term thread state from long term durable memory. See `references/memory.md`.
- [ ] **Context curation**: retrieve, rank, compact, and budget the context window (RAG). See `references/context-curation.md`.
- [ ] **Tools and MCP**: expose capabilities as well-described tools and Model Context Protocol servers. See `references/tools-and-mcp.md`.
- [ ] **Identity and guardrails**: agent identity, least privilege, content safety, prompt shields. See `references/guardrails-and-identity.md`.
- [ ] **Evaluation, observability, and cost**: measure quality, trace runs, and govern spend. See `references/evaluation-observability-cost.md`.

### Reference architecture target

```text
User / GitHub Copilot / GitHub Actions
        |
   API Management (AI gateway): authN, token limit, load balance, semantic cache
        |
   Agent runtime (Azure AI Foundry Agent Service, Container Apps, or AKS)
   |          |              |                 |
 Model      Memory        Context           Tools / MCP
 router    (Redis +      (RAG: AI Search   (API Center registry,
 (tiers)    vector)       + rerank)          MCP servers)
        |
 Guardrails (Content Safety, Prompt Shields) + Identity (Entra Agent ID, managed identity)
        |
 Observability (App Insights + OpenTelemetry GenAI) + Evaluation (Foundry evals)
```

### Decision record expectations

- [ ] Each decision records the chosen option, rationale, and source.
- [ ] Cache, semantic cache, vector store, or memory store decisions are identified for Redis follow-up.
- [ ] Agent runtime, model catalog, threads, and tools decisions are identified for Foundry follow-up.
- [ ] API and tool or MCP governance decisions are identified for API governance follow-up.
- [ ] Model gateway policy decisions include token limit, load balance, and semantic cache where relevant.
- [ ] Diagram-ready service mapping is produced when a diagram deliverable follows.

### Sources to preserve

- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure Well-Architected for AI workloads](https://learn.microsoft.com/azure/well-architected/ai/)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GitHub Models](https://docs.github.com/github-models)

## Output template

Return exactly this structure:

```markdown
# Agentic architecture decision record

**Status:** completed | blocked
**Summary:** <one-sentence architecture recommendation>
**Use case:** <short use-case name>

### Details
- Model routing: <decision and rationale>
- Caching: <decision and rationale>
- Memory: <decision and rationale>
- Context curation: <decision and rationale>
- Tools and MCP: <decision and rationale>
- Identity and guardrails: <decision and rationale>
- Evaluation, observability, and cost: <decision and rationale>

### Validation evidence
- Sources checked: <links or documents used>
- Assumptions: <explicit assumptions or none>
- Risks and trade-offs: <list>
- Follow-up primitives: <skills or agents to use next>
```

## Limits

- Do not use this skill for Azure AI Foundry provisioning.
- Use `foundry-agent-blueprint` (`skill`) instead when the task is a Foundry agent service blueprint.
- Do not use this skill for Redis implementation details.
- Use `open-horizons-architect` (`agent`) instead when the task is diagram rendering.
- Do not invent limits, prices, benchmarks, or citations.

## Gotchas

- One frontier model for every task is an anti-pattern; route by task class and reserve frontier for the hardest steps.
- No caching on stable system prompts or repeated retrievals wastes high-leverage cost levers.
- Unbounded context is unsafe; always budget the window and compact history.
- Tool sprawl is not free; each tool adds selection cost, so curate and namespace tools.
- Shared secrets are not a substitute for managed identity and agent identity.
- Shipping without evals or tracing prevents governance.

## Progressive disclosure and bundled resources

At discovery time, only `name` and `description` are loaded. Read the relevant reference file for each decision that needs depth.

- `references/model-routing.md`: model tiering and routing decisions.
- `references/caching.md`: prompt caching and semantic caching decisions.
- `references/memory.md`: short term and long term memory decisions.
- `references/context-curation.md`: RAG, ranking, compaction, and context-window budgeting.
- `references/tools-and-mcp.md`: tool and MCP design decisions.
- `references/guardrails-and-identity.md`: agent identity, least privilege, and safety controls.
- `references/evaluation-observability-cost.md`: evaluation, tracing, and spend governance.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `foundry-agent-blueprint` | `skill` | The architecture needs an Azure AI Foundry Agent Service blueprint. |
| `azure-infrastructure` | `skill` | The design needs Azure infrastructure patterns beyond agentic decisions. |
| `open-horizons-architect` | `agent` | The decision record needs a professional diagram. |
| `cloud-architecture-best-practices-docs` | `skill` | The architecture Markdown deliverable needs compliance validation. |
| `open-horizons-architect` | `agent` | A persistent architecture agent should own the broader design. |

## Quality gate

- [ ] The seven decisions are addressed in order.
- [ ] Each decision includes an option, rationale, and source or explicit assumption.
- [ ] Limits, prices, and benchmarks are verified against authoritative sources or omitted.
- [ ] Anti-patterns were checked and flagged when present.
- [ ] Follow-up primitives are named for provisioning, implementation detail, diagrams, or validation.
- [ ] The response follows `## Output template` exactly.
- [ ] Every bundled resource referenced above exists.
