---
name: foundry-agent-blueprint
description: "Use when designing an Azure AI Foundry Agent Service blueprint, including model deployments, connections, threads and runs, tools, MCP, file search, code interpreter, evaluation, tracing, and memory integration; produces a Foundry service map and build checklist. DO NOT USE FOR: general agent architecture trade-off analysis (use agentic-architecture-patterns), Redis cache design (use azure-managed-redis-cache), or hands-on Azure provisioning (use ai-foundry-operations). Triggers include \"design a Foundry agent\", \"map this agent to Foundry tools\", \"plan Foundry evaluation\"."
---

# Foundry Agent Blueprint

This workflow maps an agent use case to Azure AI Foundry Agent Service primitives: project, model deployments, connections, tools, threads, memory, evaluation, and tracing. It produces a Foundry blueprint that implementation agents can provision and validate.

> [!NOTE]
> This skill depends on current Azure AI Foundry documentation and may route provisioning details to installed Microsoft Foundry or Azure AI skills. Confirm feature names, model catalog availability, quotas, and limits on Microsoft Learn before implementation.

## When to invoke
- "Design a Foundry agent for a RAG workflow."
- "Map our agent tools to Azure AI Foundry capabilities."
- "Plan threads, memory, evaluation, and tracing for a Foundry agent."
- "Choose Foundry connections for Azure AI Search and Redis."

## Prerequisites and context
- Agent goal, users, tools, data sources, and safety requirements are known.
- Target Azure AI Foundry project or environment is identified.
- Model candidates and regional constraints are available or can be verified.
- Related repository paths exist: `foundry/agents-service/`, `foundry/k8s/`, and `terraform/modules/ai-foundry/`.
- User approval is available before creating blueprint artifacts or provisioning follow-ups.

## Procedure

### Step 1: Confirm agent blueprint scope
```text
Foundry blueprint summary:
- Agent goal:
- Models:
- Connections:
- Tools:
- Memory:
- Artifacts to create:
Proceed with creating or updating blueprint artifacts? (y/n)
```

> [!IMPORTANT]
> Only proceed with creating blueprint artifacts or initiating provisioning handoffs if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the blueprint recommendations and stop.

### Step 2: Map Foundry primitives
| Design area | Foundry primitive |
|---|---|
| Model routing | Model catalog deployments and an application or gateway router where needed. |
| Short-term memory | Threads and runs for conversation state. |
| Long-term memory | Azure AI Search or Azure Managed Redis connection. |
| Context curation | File search, Azure AI Search, or external RAG pipeline. |
| Tools | Function tools, OpenAPI tools, MCP tools, code interpreter, and file search. |
| Identity and guardrails | Managed identity, Entra Agent ID where applicable, Content Safety, and Prompt Shields. |
| Evaluation and observability | Foundry evaluators, tracing, App Insights, and OpenTelemetry GenAI conventions. |

### Step 3: Design connections and data boundaries
- [ ] Azure AI Search connection is scoped to the approved index and tenant boundary.
- [ ] Azure Managed Redis is used for semantic cache or vector memory when low-latency memory is required.
- [ ] Storage connection uses the correct Blob endpoint format when applicable.
- [ ] Tool credentials use managed identity or approved secret storage.
- [ ] Data classification determines whether public network access is acceptable.

### Step 4: Define tool surface
- [ ] Function tools have narrow schemas and deterministic side effects.
- [ ] OpenAPI tools use governed API endpoints.
- [ ] MCP tools are named, scoped, and least-privileged.
- [ ] Code interpreter is enabled only for trusted workloads with data boundaries.
- [ ] File search is grounded in approved files and retrieval limits.

### Step 5: Plan evaluation and tracing
- [ ] Define eval cases for task success, relevance, groundedness, coherence, safety, and refusal behavior.
- [ ] Define trace attributes for model, tokens, tool calls, cache outcome, latency, and cost.
- [ ] Gate production changes on evaluation thresholds and rollback criteria.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Tool can mutate sensitive systems without guardrails, or memory/retrieval leaks tenant data. |
| High | No evaluation gate, no traceability, unsupported model/region, or broad connection permissions. |
| Medium | Missing cache policy, unclear thread retention, or incomplete tool schemas. |
| Low | Naming, documentation, or handoff gaps. |

## Limits

- Do not use this skill for: general agent architecture trade-off analysis (use agentic-architecture-patterns), Redis cache design (use azure-managed-redis-cache), or hands-on Azure provisioning (use ai-foundry-operations).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Foundry capability is unclear | Verify current Microsoft Learn docs and state uncertainty. |
| Model quota is unavailable | Route quota validation to `ai-foundry-operations` and do not substitute silently. |
| Redis or search design is needed | Route detailed design to `azure-managed-redis-cache` or the relevant search skill. |
| Provisioning is requested | Produce the blueprint and route execution to `ai-foundry-operations`. |

## Output template

Return exactly this structure:
```markdown
# Foundry Agent Blueprint

## Scope
- Agent goal:
- Users:
- Runtime:

## Foundry Map
| Area | Decision | Rationale |
|---|---|---|

## Connections
| Connection | Purpose | Identity | Data Boundary |
|---|---|---|---|

## Tools
| Tool | Type | Scope | Risk |
|---|---|---|---|

## Evaluation And Tracing
- Eval set:
- Metrics:
- Rollback criteria:
```

## Quality gate
- [ ] Every model, connection, tool, memory, evaluation, and tracing decision is documented.
- [ ] Current Foundry capability and quota assumptions are sourced or labeled as assumptions.
- [ ] High-risk tools and data boundaries have mitigations.
- [ ] Provisioning execution is routed to the operations skill.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
