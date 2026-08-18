---
name: azure-managed-redis-cache
description: "Design and provision Azure Managed Redis as the cache, semantic cache, vector store, session store, and agent memory backend for AI-native systems. Use when an agent design needs caching, semantic caching, RedisVL, vector memory, short term session state, tenant isolation, Entra managed identity access, private networking, SKU selection, or a Bicep deployment for Azure Managed Redis."
argument-hint: "what to back with Redis, for example a semantic cache plus long term vector memory"
---

# Azure Managed Redis Cache

Turn an AI application's cache, semantic cache, vector memory, session state, and rate-state needs into an Azure Managed Redis design with SKU, identity, networking, key layout, and deployable Bicep choices.

## When to invoke

- "Design Redis for semantic cache and long term memory."
- "Which Azure Managed Redis SKU should this agent use?"
- "Provision Redis with private networking and managed identity."
- "Use RedisVL for vector search and semantic caching."
- "Store sessions and short term agent state in Redis."

## Inputs

Use `$ARGUMENTS` as the requested Redis role, workload shape, or deployment concern. If `$ARGUMENTS` is empty, infer roles from the agent design and ask only for missing sizing facts that block SKU or network selection.

## Prerequisites and context

- Verify current Azure Managed Redis SKU names, module support, and API version on Microsoft Learn before deployment.
- Azure Cache for Redis Enterprise is retired for new creations; use Azure Managed Redis SKUs even though the resource type remains `Microsoft.Cache/redisEnterprise`.
- `publicNetworkAccess` is required in the Bicep resource; set it intentionally rather than relying on defaults.
- Use the bundled Bicep `scripts/redis-managed.bicep` only after reviewing parameters for the target environment.

## Redis role selection

| Need | Redis role | Design rule | Bundled detail |
| --- | --- | --- | --- |
| Cut repeated model cost and latency | Semantic cache | Store embeddings of prompts/responses and match by vector similarity; add TTL and invalidation by model/version. | `references/semantic-cache.md` |
| Long term agent memory | Vector store | Store durable facts or document chunks with tenant and source metadata; separate recall from session state. | `references/vector-memory.md` |
| Conversation and run state | Session store | Keep short term thread state, resumable workflow state, and locks with explicit TTL. | `references/session-store.md` |
| Hot data and rate state | Key value cache | Use cache-aside, counters, and idempotency keys; define ownership of invalidation. | Inline design decision |

## SKU selection

| Profile | Example | Choose when | Watch |
| --- | --- | --- | --- |
| Balanced | `Balanced_B1` | in-memory General-purpose caches, small vector sets, and default development or moderate production workloads. | Validate exact size and price before deployment. |
| MemoryOptimized | Current Microsoft Learn SKU | Working set is memory-heavy or vector indexes are large relative to CPU demand. | Ensure index memory fits without eviction pressure. |
| ComputeOptimized | Current Microsoft Learn SKU | high-throughput, compute-heavy access or vector search CPU dominates memory size. | Benchmark query concurrency and latency. |
| FlashOptimized | Current Microsoft Learn SKU | Very large datasets need lower cost per GB with tiered memory plus flash. | Model flash latency against SLA before choosing. |

Confirm RediSearch/vector search module availability for the selected tier before committing to semantic cache or vector memory.

## Access, isolation, and network design

| Concern | Required decision |
| --- | --- |
| Authentication | Prefer Entra authentication with managed identity and `DefaultAzureCredential`; design for tenants where local auth is disabled. |
| Tenant isolation | Namespace every key by tenant and user, for example `t:{tenant}:u:{user}:...`; include role or data-class prefixes when a shared cache spans workloads. |
| Private networking | Use private endpoints and disable `publicNetworkAccess` for sensitive data paths; plan VNet and private DNS before deployment. |
| TLS | Require TLS for all clients and reject non-TLS examples. |
| TTL and invalidation | Assign TTL by data class: semantic cache entries expire by freshness/model version, sessions expire by inactivity, durable memory expires only by policy. |
| Observability | Capture hit rate, eviction rate, latency percentiles, memory pressure, vector query latency, and authentication failures. |

## Procedure

1. Identify every Redis role in the design: semantic cache, vector memory, session store, or key value cache.
2. Estimate working set, item size, vector dimensions, query concurrency, retention, and latency target.
3. Select a SKU profile and verify exact current SKU names and vector module availability on Microsoft Learn.
4. Choose Entra managed identity access, tenant key namespace, TLS requirements, and public/private network posture.
5. Adapt `scripts/redis-managed.bicep`; set `Microsoft.Cache/redisEnterprise`, current API version such as `2025-07-01`, SKU parameters, and `publicNetworkAccess` explicitly.
6. Wire clients with RedisVL where semantic cache or vector memory is required, then record TTL, invalidation, agentic-architecture-patterns, apim-ai-gateway handoff context, and isolation rules in the architecture decision record.

## Progressive disclosure and bundled resources

- `references/semantic-cache.md`: semantic cache architecture, RedisVL matching, TTL, and cache-key guidance.
- `references/vector-memory.md`: long term vector memory schema and retrieval rules.
- `references/session-store.md`: session and short term state patterns.
- `references/access-and-network.md`: Entra, managed identity, private endpoint, and network posture details.
- `scripts/redis-managed.bicep`: minimal idempotent Azure Managed Redis deployment sample.

## Gotchas

- **Retirement naming is confusing**: do not provision retired Azure Cache for Redis Enterprise for new creations; Azure Managed Redis still uses `Microsoft.Cache/redisEnterprise`.
- **Vector support is tier-dependent**: confirm modules before promising RedisVL semantic cache or vector memory.
- **Shared caches leak without namespacing**: never store unscoped keys in multi-tenant systems.
- **Disabling public access requires DNS planning**: private endpoint deployment without private DNS produces hard-to-debug client timeouts.

## Output template

```markdown
### Azure Managed Redis design

**Status:** complete | needs sizing | blocked
**Redis roles:** semantic cache | vector memory | session store | key value cache
**Recommended SKU profile:** Balanced | MemoryOptimized | ComputeOptimized | FlashOptimized

| Decision | Value | Evidence or reason |
| --- | --- | --- |
| Resource type | `Microsoft.Cache/redisEnterprise` | Azure Managed Redis deployment model |
| API version checked | `<version>` | `<Microsoft Learn URL/date>` |
| `publicNetworkAccess` | enabled | disabled | `<network reason>` |
| Auth | Entra managed identity with `DefaultAzureCredential` | `<identity/client reason>` |
| Key namespace | `t:{tenant}:u:{user}:...` | tenant isolation |
| Client pattern | RedisVL | Redis client | `<role reason>` |

**Validation**
- SKU/module availability checked: pass | fail
- Bicep reviewed: `scripts/redis-managed.bicep`
```

## Quality gate

- [ ] `$ARGUMENTS` was consumed or the Redis roles were inferred from the design.
- [ ] Azure Cache for Redis Enterprise retirement was accounted for.
- [ ] Current SKU names, API version, and module availability were verified before deployment guidance.
- [ ] `publicNetworkAccess` is set deliberately.
- [ ] Entra managed identity and `DefaultAzureCredential` are preferred over access keys unless a constraint is documented.
- [ ] Tenant and user key namespacing is specified.
- [ ] TTL, invalidation, and observability requirements are recorded.
- [ ] Every referenced bundled resource exists and is used on demand.

## References

- [Azure Managed Redis](https://learn.microsoft.com/azure/redis/)
- [Azure Managed Redis vector search](https://learn.microsoft.com/en-us/azure/redis/overview-vector-similarity)
- [Authenticate with Microsoft Entra ID](https://learn.microsoft.com/azure/redis/entra-for-authentication)
- [RedisVL](https://redis.io/docs/latest/integrate/redisvl/)
