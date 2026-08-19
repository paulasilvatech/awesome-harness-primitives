# Caching

Caching is the highest-leverage lever for latency and cost in agentic systems. Use two complementary layers.

## 1. Prompt caching (exact prefix reuse)

Providers can cache a stable prefix of the prompt (system instructions, tool schemas, long shared context) so repeated calls reuse it at a reduced rate. Characteristics:

- Keyed on an exact token prefix match. Put the stable content first and the variable content last.
- Cached reads are billed at a fraction of input rate and return faster. The exact discount and time to live depend on the provider; verify on the model card.
- High-cache-read workloads can show most input tokens served from cache, which dominates the bill, so structure prompts to maximize the stable prefix.

Design: keep one canonical system prompt and tool block, version it, and avoid per-request edits that break the prefix.

## 2. Semantic caching (similarity reuse)

Cache responses keyed by the meaning of the request, not exact text. On a new request, embed it, search the cache for a sufficiently similar prior request, and return the stored answer if similarity passes a threshold.

- Backed by a vector store. In this workspace use Azure Managed Redis with vector search (see `azure-managed-redis-cache`).
- Tune the similarity threshold to balance hit rate against wrong-answer risk. Start conservative.
- Scope the cache key by tenant, user, or tool context to avoid leaking answers across boundaries.
- Set a time to live and an invalidation path for data that changes.

### Where to run semantic cache

- **At the gateway.** Azure API Management has built-in semantic caching policies for model calls (see `apim-ai-gateway`). Lowest app change.
- **In the app or agent.** Use RedisVL or the Redis vector index directly for fine control over keys, scoping, and thresholds.

## Decision guide

| Situation | Use |
| --- | --- |
| Stable system prompt and tool schemas | prompt caching |
| Repeated or paraphrased user questions | semantic caching |
| FAQ-like or read-heavy traffic | semantic caching at the gateway |
| Strict correctness, low tolerance for stale or near-miss answers | prompt caching only, or high semantic threshold with validation |

## Risks

- Semantic cache can return a confidently wrong neighbor. Add a threshold and optional verification.
- Caches can leak across tenants if keys are not scoped. Always include an isolation dimension in the key.
- Stale answers. Set time to live and invalidate on source change.

## Sources

- [Azure API Management semantic caching policy](https://learn.microsoft.com/azure/api-management/azure-openai-semantic-cache-lookup-policy)
- [Azure Managed Redis vector search](https://learn.microsoft.com/azure/redis/)
- [RedisVL semantic cache](https://redis.io/docs/latest/integrate/redisvl/)
