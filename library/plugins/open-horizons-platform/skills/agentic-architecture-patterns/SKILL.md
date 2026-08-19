---
name: agentic-architecture-patterns
description: "Use when architecting or reviewing an AI agent or multi-agent system on GitHub or Azure AI Foundry; produces a decision record covering model routing, caching, memory, context, tools/MCP, identity, guardrails, evaluation, observability, and cost. DO NOT USE FOR: hands-on Foundry provisioning or RAG operations (use ai-foundry-operations or foundry-agent-blueprint), requirements writing (use requirements-engineer), story decomposition (use story-planning), or final diagrams (use azure-architecture-diagrams). Triggers include \"design an agent architecture\", \"review this multi-agent system\", \"choose a model routing and memory strategy\"."
---

# Agentic Architecture Patterns

This workflow turns an AI-native use case into a documented architecture decision record for Open Horizons, grounded in the seven agentic system decisions and the repository's L3 Context Platform Stack. It produces a service map, risk register, and implementation handoff for companion skills such as `foundry-agent-blueprint`, `azure-managed-redis-cache`, and `azure-architecture-diagrams`.

> [!NOTE]
> This skill depends on bundled references under `references/`, current Microsoft Learn and GitHub documentation, and authenticated MCP documentation or search tools when available. Resolve bundled paths relative to this `SKILL.md`; do not invent limits, prices, or model benchmarks.

## When to invoke
- "Design an agent architecture for our Open Horizons platform."
- "Review this multi-agent system for security, cost, and reliability risks."
- "Choose the right model routing, memory, cache, and RAG strategy."
- "Map this agent design to Azure AI Foundry, Redis, tools, and MCP."

## Prerequisites and context
- A use case, users, data sensitivity, runtime target, latency goal, and cost ceiling.
- Repository context available in `CODEMAP.md`, `backstage/server/agent-api/memory/context_store.py`, and `backstage/server/agent-api/memory/tiers.py`.
- Reference files available in `references/`.
- Current vendor documentation available for quoted limits, pricing, and model capability claims.

## Procedure

### Step 1: Confirm design scope
1. Identify the target runtime: Azure AI Foundry Agent Service, AKS service, GitHub Actions automation, or Backstage agent API.
2. Capture tenant boundaries, data sources, tool surfaces, expected traffic, quality bar, and compliance constraints.
3. Ask before writing architecture artifacts or ADRs.

```text
Scope summary:
- Runtime:
- Users and tenants:
- Data sensitivity:
- Latency and cost targets:
- Artifacts to create:
Proceed with creating or updating architecture artifacts? (y/n)
```

> [!IMPORTANT]
> Only proceed with creating or updating repository artifacts if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the design findings and stop.

### Step 2: Load the seven reference decisions
Read the applicable reference files before making recommendations:

| Decision | Repository reference |
|---|---|
| Model routing | `references/model-routing.md` |
| Caching | `references/caching.md` |
| Memory | `references/memory.md` |
| Context curation | `references/context-curation.md` |
| Tools and MCP | `references/tools-and-mcp.md` |
| Guardrails and identity | `references/guardrails-and-identity.md` |
| Evaluation, observability, and cost | `references/evaluation-observability-cost.md` |

### Step 3: Build the service map
- [ ] Route low-risk extraction and classification to the cheapest capable model tier.
- [ ] Reserve premium/frontier models for hard reasoning, synthesis, or high-risk decisions.
- [ ] Use prompt caching for stable prefixes and semantic caching for repeated user intents.
- [ ] Separate short-term thread state from long-term durable memory.
- [ ] Use Azure Managed Redis for cache, session state, and vector memory when low-latency access is required.
- [ ] Use retrieval ranking, compaction, and budget limits before expanding context windows.
- [ ] Keep tool surfaces narrow, namespaced, and least-privileged.
- [ ] Assign managed identity or Entra Agent ID instead of shared secrets.
- [ ] Define evaluation datasets, OpenTelemetry GenAI traces, cost budgets, and rollback criteria.

### Step 4: Classify risks
| Severity | Meaning |
|---|---|
| Critical | Unbounded tool access, cross-tenant data leakage, or missing identity controls that can expose sensitive systems. |
| High | No eval gate, no traceability, single expensive model path, or unscoped long-term memory in production. |
| Medium | Weak cache invalidation, incomplete observability, oversized context, or unclear model routing thresholds. |
| Low | Documentation gaps, naming inconsistencies, or missing optimization opportunities. |

### Step 5: Route implementation follow-ups
- Use `foundry-agent-blueprint` for Azure AI Foundry agent primitives.
- Use `azure-managed-redis-cache` for semantic cache, vector memory, or session store design.
- Use `azure-architecture-diagrams` for draw.io and SVG diagrams.
- Use `architecture-doc` to validate Mermaid architecture documents.

## Limits

- Do not use this skill for: hands-on Foundry provisioning or RAG operations (use ai-foundry-operations or foundry-agent-blueprint), requirements writing (use requirements-engineer), story decomposition (use story-planning), or final diagrams (use azure-architecture-diagrams).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Scope is unclear | State assumptions, ask only for missing facts, and avoid writing files. |
| Reference file is unavailable | Report the missing path and continue only with verified sources. |
| Vendor limit or price is needed | Fetch current official documentation and cite it, or label the number as an assumption. |
| Recommendation overlaps another skill | Stop at the design boundary and route to the companion skill. |

## Output template

Return exactly this structure:
```markdown
# Agentic Architecture Decision Record

## Scope
- Runtime:
- Users and tenants:
- Data sources:

## Seven Decisions
| Decision | Choice | Rationale | Source |
|---|---|---|---|
| Model routing |  |  |  |
| Caching |  |  |  |
| Memory |  |  |  |
| Context curation |  |  |  |
| Tools and MCP |  |  |  |
| Identity and guardrails |  |  |  |
| Evaluation, observability, and cost |  |  |  |

## Risk Register
| Severity | Finding | Evidence | Recommendation |
|---|---|---|---|

## Implementation Handoffs
- Foundry:
- Redis:
- Diagrams:
```

## Quality gate
- [ ] All seven decisions are resolved with rationale and source evidence.
- [ ] Risks are classified with concrete mitigations.
- [ ] No unsourced limits, prices, or benchmark claims are included.
- [ ] Handoffs point only to valid Open Horizons skills or repository paths.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
