---
name: apim-ai-gateway
description: "Front model and tool backends with Azure API Management as an AI gateway: token rate limiting (token-per-minute and quota), multi-backend load balancing and circuit breaker across model deployments, semantic caching, token metric emission for cost attribution, managed identity to backends, and content safety integration. Use when designing the runtime gateway for an agentic platform, enforcing token budgets, load balancing across model endpoints, adding a semantic cache at the gateway, or governing tool API calls. Routes to the installed azure-aigateway skill for policy detail. Pairs with azure-api-center (governance), azure-managed-redis-cache (cache backend), and agentic-architecture-patterns."
argument-hint: "what to front, for example token-limited load balancing across two model deployments with semantic cache"
---

# APIM AI Gateway

Azure API Management as the **runtime gateway** for AI traffic. It sits between agents and model or tool backends and enforces budgets, balances load, caches, and attributes cost, without changing application code. For the full policy reference and worked examples, load the installed `azure-aigateway` skill and verify against Microsoft Learn.

> Verify current policy names and behaviors on Microsoft Learn. A note from experience: the Developer tier of API Management cannot be created with `publicNetworkAccess=Disabled`; create it enabled and harden later.

## What the AI gateway gives you

| Capability | Policy area | Why |
| --- | --- | --- |
| Token rate limiting | token limit per key or subscription | protect budgets and prevent runaway spend |
| Token quotas | renewable token quota | enforce per-tenant or per-feature ceilings |
| Load balancing | backend pool with weights and priority | spread load across model deployments and regions |
| Resilience | circuit breaker on backends | fail over when a deployment is throttled or down |
| Semantic caching | semantic cache lookup and store | reuse answers for similar prompts (see `azure-managed-redis-cache`) |
| Cost attribution | emit token metric | track usage by model, tenant, and feature |
| Identity | managed identity to backend | no keys in the app; AAD to the model service |
| Safety | content safety integration | screen requests at the edge |

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

## Design steps

1. **Define backends.** Register each model deployment as a backend. Group them into a load-balanced pool with weights and priorities.
2. **Set token controls.** Apply a token limit policy for rate, and a token quota policy for renewable ceilings. Key them by caller, tenant, or feature.
3. **Add resilience.** Configure circuit breaker rules so a throttled or failing deployment is bypassed.
4. **Add semantic cache.** Enable semantic cache lookup and store, backed by a vector store (Azure Managed Redis). Tune the similarity threshold conservatively.
5. **Attribute cost.** Emit the token metric with dimensions for model, tenant, and feature, and dashboard it in Azure Monitor.
6. **Secure.** Use managed identity from API Management to the model backend. Restrict callers with subscription keys or AAD. Harden networking per data sensitivity.

## How it fits

- **Governance vs runtime.** `azure-api-center` catalogs and governs APIs and tools; this gateway enforces and routes them at runtime.
- **Caching.** The semantic cache here is the lowest-change place to add caching; the app-level alternative is in `azure-managed-redis-cache`.
- **Routing.** Centralizing model calls behind the gateway makes the routing tiers in `agentic-architecture-patterns` enforceable in one place.

## References

- [Azure API Management AI gateway capabilities](https://learn.microsoft.com/azure/api-management/genai-gateway-capabilities)
- [Token limit policy](https://learn.microsoft.com/azure/api-management/llm-token-limit-policy)
- [Semantic caching policy](https://learn.microsoft.com/azure/api-management/azure-openai-semantic-cache-lookup-policy)
- [Load balancing and circuit breaker for backends](https://learn.microsoft.com/azure/api-management/backends)
