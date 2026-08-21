# Semantic Cache on Azure Managed Redis

A semantic cache returns a stored answer when a new request is close enough in meaning to a prior one. It is the highest-leverage cost lever for read-heavy or repetitive agent traffic.

## How it works

1. Embed the incoming request to a vector.
2. Search the Redis vector index for the nearest stored request.
3. If similarity passes the threshold, return the stored response (a hit). Otherwise call the model and store the new pair (a miss).

## Build with RedisVL

RedisVL provides a `SemanticCache` abstraction over a Redis vector index. The shape:

- Configure the embedding model (use an Azure AI Foundry embeddings deployment).
- Set a distance or similarity threshold. Start conservative (high similarity required) and loosen with evidence.
- Set a time to live so stale answers expire.
- Scope the cache key by tenant and user so answers never cross boundaries.

## Threshold tuning

- Too loose returns confident wrong neighbors. Too tight gives a low hit rate.
- Measure hit rate and a quality score on held-out traffic. Adjust the threshold to the point where quality stays above the bar.
- For high-stakes answers, verify a hit (a cheap model check) before returning it.

## Where to run it

- **At the gateway.** Azure API Management has semantic caching policies for model calls and can use a Redis-backed vector store. Lowest application change. See `apim-ai-gateway`.
- **In the app or agent.** Use RedisVL directly for fine control over keys, scoping, thresholds, and invalidation.

## Invalidation

- Time to live for natural expiry.
- Explicit purge by key prefix when a source document changes.
- Version the cache namespace to drop the whole cache on a model or prompt change.

## Sources

- [Azure Managed Redis vector search](https://learn.microsoft.com/azure/redis/redis-vector-search)
- [RedisVL semantic cache](https://redis.io/docs/latest/integrate/redisvl/user_guide/llmcache/)
- [Azure API Management semantic caching policy](https://learn.microsoft.com/azure/api-management/azure-openai-semantic-cache-lookup-policy)
