---
name: azure-managed-redis-cache
description: "Design and provision Azure Managed Redis as the cache, semantic cache, vector store, session store, and agent memory backend for AI-native systems. Covers SKU selection (Balanced, MemoryOptimized, ComputeOptimized, FlashOptimized), the fact that Redis Enterprise is retired for new creations, vector search and RedisVL for semantic caching and long term memory, session and short term state, tenant isolation, managed identity (Entra) access, private networking, and a Bicep sample. Use when an agent design needs caching, a semantic cache, a vector memory store, or session state on Redis. Pairs with agentic-architecture-patterns and apim-ai-gateway."
argument-hint: "what to back with Redis, for example a semantic cache plus long term vector memory"
---

# Azure Managed Redis Cache

Azure Managed Redis is the default in-memory engine for caching, semantic caching, vector memory, and session state in this workspace. This skill turns an agent's caching and memory needs into a concrete Redis design and a deployable Bicep.

> Important: **Azure Cache for Redis Enterprise is retired for new creations.** Use **Azure Managed Redis** SKUs. The resource type is still `Microsoft.Cache/redisEnterprise` (use a current API version such as `2025-07-01`), and `publicNetworkAccess` is a required property. Verify the current SKU list and API version on Microsoft Learn before deploying.

## When to use Redis in an agent

| Need | Redis role | Detail |
| --- | --- | --- |
| Cut repeated model cost and latency | semantic cache | vector similarity over prior requests, see [references/semantic-cache.md](references/semantic-cache.md) |
| Long term agent memory | vector store | embeddings of facts and documents, see [references/vector-memory.md](references/vector-memory.md) |
| Conversation and run state | session store | short term thread state, see [references/session-store.md](references/session-store.md) |
| Hot data and rate state | key value cache | classic cache-aside and counters |

## SKU selection

Azure Managed Redis groups SKUs by profile. Pick by working set size and access pattern (verify exact names, sizes, and prices on Microsoft Learn):

- **Balanced (for example `Balanced_B1`)**: general purpose, balanced memory and vCPU. Good default for caches and small vector sets.
- **MemoryOptimized**: more memory per vCPU, for large caches and larger vector indexes.
- **ComputeOptimized**: more vCPU per memory, for high-throughput, compute-heavy access (heavy vector search).
- **FlashOptimized**: tiered memory plus flash for very large datasets at lower cost per GB.

Use the vector search and RediSearch capabilities (modules) for semantic cache and memory. Confirm module availability for the chosen tier.

## Access and security (best practice)

- **Use Entra (AAD) authentication with managed identity.** Prefer `DefaultAzureCredential` over access keys. Some tenant policies disable local auth, so design for AAD from the start. See [references/access-and-network.md](references/access-and-network.md).
- **Tenant isolation.** Namespace every key by tenant and user (for example `t:{tenant}:u:{user}:...`) so a shared cache cannot leak across boundaries.
- **Private networking.** Use private endpoints and set `publicNetworkAccess` to disabled where data sensitivity requires it. Plan the VNet and DNS up front.
- **Encryption and TLS.** Require TLS for all connections.

## Provision

A minimal, idempotent Bicep is in [scripts/redis-managed.bicep](scripts/redis-managed.bicep). It creates an Azure Managed Redis database with a chosen SKU and exposes the host. Review parameters, then deploy with the Azure CLI. Validate against Microsoft Learn for the latest API version and SKU names before applying.

## How to use this skill

1. Identify which roles Redis plays (semantic cache, vector memory, session, key value) from the agent design.
2. Size the working set and pick a SKU profile.
3. Choose AAD plus managed identity access and the network posture.
4. Adapt the Bicep, deploy, and wire the app with the appropriate client (RedisVL for semantic cache and vector memory).
5. Add key namespacing, time to live, and invalidation. Record the design in the architecture decision record.

## References

- [Azure Managed Redis](https://learn.microsoft.com/azure/redis/)
- [Azure Managed Redis vector search](https://learn.microsoft.com/azure/redis/redis-vector-search)
- [Authenticate with Microsoft Entra ID](https://learn.microsoft.com/azure/redis/entra-for-authentication)
- [RedisVL](https://redis.io/docs/latest/integrate/redisvl/)
