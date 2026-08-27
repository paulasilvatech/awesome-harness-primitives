---
name: apim-ai-gateway
description: >-
  Design Azure API Management as the runtime AI gateway for model and tool traffic, including
  token-per-minute controls, token limits, quotas, multi-backend load-balanced backend pools,
  circuit breakers, semantic caching, token metrics, managed identity, and content safety. Use
  when fronting model deployments, enforcing token budgets, adding semantic cache, load balancing
  LLM endpoints, or governing tool API calls at runtime.
argument-hint: >-
  what to front, for example token-limited load balancing across two model deployments with
  semantic cache
---

<!-- Generated from harness/github-copilot/plugins/azure-ai-foundry/skills/apim-ai-gateway/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# APIM AI gateway

Design Azure API Management as the runtime gateway between agents, applications, model deployments, and tool APIs so traffic is governed, resilient, cached, metered, and secured without changing every caller.

## When to invoke

- "Put Azure API Management in front of our model deployments."
- "Design token limits and semantic caching for agent traffic."
- "Load balance Azure OpenAI backends with circuit breakers."
- "Govern tool API calls at runtime with an AI gateway."

## Inputs

Use `$ARGUMENTS` as the runtime gateway scenario: what callers invoke, which model or tool backends exist, tenant or feature dimensions, token budget goals, cache needs, and network/security constraints. If details are missing, state assumptions before designing.

## Prerequisites and context

- Verify current Azure API Management policy names and behavior on Microsoft Learn before committing exact XML policy syntax.
- The Developer tier of API Management cannot be created with `publicNetworkAccess=Disabled`; create it enabled and harden later if that tier is required.
- Use the installed `apim-ai-gateway` skill for deep policy examples when available; this skill defines the primitive design shape.

## Gateway capabilities

| Capability | Policy area | Why it matters |
| --- | --- | --- |
| Token rate limiting | token limit per key or subscription | Protect budgets and prevent runaway spend. |
| Token quotas | renewable token quota | Enforce per-tenant, per-user, or per-feature ceilings. |
| Load balancing | backend pool with weights and priority | Spread traffic across model deployments, models, and regions. |
| Resilience | circuit breaker on backends | Bypass throttled, unhealthy, or down deployments. |
| Semantic caching | semantic cache lookup and store | Reuse answers for similar prompts through a cache backend such as Azure Managed Redis. |
| Cost attribution | emit token metric | Track usage by model, tenant, feature, and caller in Azure Monitor. |
| Identity | managed identity to backend | Remove backend keys from application code and use AAD where supported. |
| Safety | content safety integration | Screen requests and responses at the edge. |

## Reference pattern

```text
Agents / GitHub Copilot / apps
        |
   Azure API Management (AI gateway)
   - authN (managed identity, subscription keys for callers)
   - token limit + quota
   - semantic cache lookup  --> hit returns cached response
   - load balance + circuit breaker
        |                 |
   Model deployment A   Model deployment B   (multi-region, multi-model)
        |
   emit token metric --> Azure Monitor (cost attribution)
```

## Procedure

1. Define backends. Register each model deployment or tool API as a backend. Group related model deployments into backend pools with weights and priorities.
2. Set token controls. Apply token limit policies for rate and token quota policies for renewable ceilings. Key limits by caller, tenant, subscription, feature, or product tier.
3. Add resilience. Configure backend circuit breaker rules so throttled or failing deployments are skipped before callers experience repeated failures.
4. Add semantic cache. Use semantic cache lookup before backend routing and semantic cache store after successful responses. Tune similarity thresholds conservatively to avoid unsafe reuse.
5. Attribute cost. Emit token metric dimensions such as model, deployment, tenant, caller, and feature to Azure Monitor dashboards and alerts.
6. Secure the path. Use managed identity from API Management to the model backend where supported. Restrict callers with subscription keys, AAD, networking, and content safety based on data sensitivity.
7. Validate with live probes. Test cache hit/miss behavior, token budget enforcement, backend failover, and metric emission before documenting the gateway as production-ready.

## Design boundaries

| Boundary | Decision rule |
| --- | --- |
| Governance vs runtime | `azure-api-center` catalogs APIs, tools, and MCP servers; APIM enforces and routes calls at runtime. |
| Caching | Gateway semantic caching is the lowest-change option; app-level caching belongs in `azure-managed-redis-cache`. |
| Routing | Centralizing model calls behind APIM makes routing tiers from `azure-agentic-architecture-patterns` enforceable in one place. |
| Tool calls | Treat governed tool APIs like any other backend: authenticate callers, enforce quotas, monitor errors, and document ownership. |

## Gotchas

- **Semantic cache correctness is a safety issue**: overly loose similarity thresholds can return plausible but wrong answers across tenants or tasks.
- **Token limits need dimensions**: a global limit protects the service but does not control per-tenant cost.
- **Circuit breakers need health evidence**: failover without metrics can hide systemic backend failure.
- **Managed identity support varies by backend**: verify the target service before promising keyless auth.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `apim-ai-gateway` | skill | You need exact APIM AI policy syntax or current Microsoft Learn examples. |
| `azure-api-center` | skill | You need catalog, governance, discovery, or linter rules rather than runtime enforcement. |
| `azure-managed-redis-cache` | skill | You need the cache backend design behind semantic caching. |
| `azure-agentic-architecture-patterns` | skill | You need agent routing and tool-use architecture decisions. |

## Output template

```markdown
## APIM AI gateway design

**Scenario:** <what is fronted>
**Gateway role:** runtime enforcement for model traffic | tool traffic | both

| Concern | Design decision | Policy or service area | Validation |
| --- | --- | --- | --- |
| Token budget | <limit/quota dimensions> | token limit, token quota | <test> |
| Routing | <backend pool, weights, priority> | backends | <failover test> |
| Cache | <lookup/store and threshold> | semantic cache | <hit/miss test> |
| Identity | <caller and backend auth> | managed identity, subscription keys, AAD | <auth test> |
| Cost | <dimensions> | emit token metric, Azure Monitor | <dashboard or query> |

### Risks and mitigations
- <risk>: <mitigation>
```

## Quality gate

- [ ] Current APIM AI gateway policy names and limitations were verified against Microsoft Learn.
- [ ] Token limits and quotas are scoped by caller, tenant, subscription, feature, or another explicit dimension.
- [ ] Backend pools, priorities, weights, and circuit breaker behavior are defined.
- [ ] Semantic cache lookup and store behavior includes a conservative threshold and tenant-safe keying.
- [ ] Managed identity, caller authentication, network hardening, and content safety are addressed.
- [ ] Token metric emission includes dimensions for cost attribution.
- [ ] The Developer tier `publicNetworkAccess=Disabled` limitation is considered when relevant.

## References

- [Azure API Management AI gateway capabilities](https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities)
- [Token limit policy](https://learn.microsoft.com/azure/api-management/llm-token-limit-policy)
- [Semantic caching policy](https://learn.microsoft.com/azure/api-management/azure-openai-semantic-cache-lookup-policy)
- [Load balancing and circuit breaker for backends](https://learn.microsoft.com/azure/api-management/backends)
