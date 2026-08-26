---
name: azure-managed-redis-cache
description: >-
  Azure Managed Redis Cache designs Redis as a cache, semantic cache, vector memory, session state, and agent memory backend. Use this skill when selecting Redis SKUs, Balanced or MemoryOptimized tiers, RedisVL, vector search, semantic caching, tenant isolation, Entra access, private networking, or the bundled Bicep sample.
---

# Azure Managed Redis Cache

Azure Managed Redis is the default in-memory engine for caching, semantic caching, vector memory, and session state in this workspace. This skill turns an agent's caching and memory needs into a concrete Redis design and a deployable Bicep.

> Important: **Azure Cache for Redis Enterprise is retired for new creations.** Use **Azure Managed Redis** SKUs. The resource type is still `Microsoft.Cache/redisEnterprise` (use a current API version such as `2025-07-01`), and `publicNetworkAccess` is a required property. Verify the current SKU list and API version on Microsoft Learn before deploying.

## When to invoke

- "Design Redis for semantic cache or vector memory."
- "Choose an Azure Managed Redis SKU and tier."
- "Use RedisVL or vector search for agent memory."
- "Plan Redis tenant isolation, Entra access, or private networking."
- "Adapt the Azure Managed Redis Bicep sample."

## Criteria

### When to use Redis in an agent

| Need | Redis role | Detail |
| --- | --- | --- |
| Cut repeated model cost and latency | semantic cache | vector similarity over prior requests, see `references/semantic-cache.md` |
| Long term agent memory | vector store | embeddings of facts and documents, see `references/vector-memory.md` |
| Conversation and run state | session store | short term thread state, see `references/session-store.md` |
| Hot data and rate state | key value cache | classic cache-aside and counters |

### SKU selection

Azure Managed Redis groups SKUs by profile. Pick by working set size and access pattern (verify exact names, sizes, and prices on Microsoft Learn):

- **Balanced (for example `Balanced_B1`)**: general purpose, balanced memory and vCPU. Good default for caches and small vector sets.
- **MemoryOptimized**: more memory per vCPU, for large caches and larger vector indexes.
- **ComputeOptimized**: more vCPU per memory, for high-throughput, compute-heavy access (heavy vector search).
- **FlashOptimized**: tiered memory plus flash for very large datasets at lower cost per GB.

Use the vector search and RediSearch capabilities (modules) for semantic cache and memory. Confirm module availability for the chosen tier.

### Access and security (best practice)

- **Use Entra (AAD) authentication with managed identity.** Prefer `DefaultAzureCredential` over access keys. Some tenant policies disable local auth, so design for AAD from the start. See `references/access-and-network.md`.
- **Tenant isolation.** Namespace every key by tenant and user (for example `t:{tenant}:u:{user}:...`) so a shared cache cannot leak across boundaries.
- **Private networking.** Use private endpoints and set `publicNetworkAccess` to disabled where data sensitivity requires it. Plan the VNet and DNS up front.
- **Encryption and TLS.** Require TLS for all connections.

### Provision

A minimal, idempotent Bicep is in `scripts/redis-managed.bicep`. It creates an Azure Managed Redis database with a chosen SKU and exposes the host. Review parameters, then deploy with the Azure CLI. Validate against Microsoft Learn for the latest API version and SKU names before applying.

### How to use this skill

1. Identify which roles Redis plays (semantic cache, vector memory, session, key value) from the agent design.
2. Size the working set and pick a SKU profile.
3. Choose AAD plus managed identity access and the network posture.
4. Adapt the Bicep, deploy, and wire the app with the appropriate client (RedisVL for semantic cache and vector memory).
5. Add key namespacing, time to live, and invalidation. Record the design in the architecture decision record.

## Output template

Return exactly this structure:

```markdown
Azure Managed Redis Design

**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the Redis design decision.

### Details
- Redis roles: semantic cache, vector memory, session store, key value cache, or a combination
- Chosen SKU and tier: profile, example tier when known, and justification
- Access model: Entra authentication, managed identity, TLS, and local auth considerations
- Network posture: private endpoint, `publicNetworkAccess`, VNet, and DNS notes
- Implementation notes: RedisVL, vector search, RediSearch modules, key namespace, TTL, invalidation, and Bicep path

### Validation
- SKU fit: PASS | FAIL with working set and access-pattern evidence
- Security fit: PASS | FAIL with tenant isolation, Entra, TLS, and private networking evidence
- Resource path check: PASS | FAIL with referenced `references/` and `scripts/` paths
```

## Limits

- Do not use this skill for general agent architecture.
- Use `azure-agentic-architecture-patterns` (`skill`) instead when designing broader model routing, tools, memory strategy, or guardrails.
- Do not use this skill for Foundry agent wiring.
- Use `foundry-agent-blueprint` (`skill`) instead when mapping Redis into Azure AI Foundry Agent Service connections or tools.
- Do not use this skill for Azure CLI or Terraform execution.
- Use `azure-cli` (`skill`) or `azure-terraform-cli` (`skill`) instead when commands must be run.

## Progressive disclosure and bundled resources

At discovery time, only `name` and `description` are loaded. Read bundled references only when the Redis role needs deeper implementation detail; use the script only when a Bicep sample is requested.

- `references/access-and-network.md`: Entra access, managed identity, private networking, and DNS considerations.
- `references/semantic-cache.md`: semantic cache design with RedisVL.
- `references/session-store.md`: conversation and run state patterns.
- `references/vector-memory.md`: long term memory and vector search design.
- `scripts/redis-managed.bicep`: minimal Azure Managed Redis Bicep sample.

External references to verify before deployment:

- [Azure Managed Redis](https://learn.microsoft.com/azure/redis/)
- [Azure Managed Redis vector search](https://learn.microsoft.com/azure/redis/redis-vector-search)
- [Authenticate with Microsoft Entra ID](https://learn.microsoft.com/azure/redis/entra-for-authentication)
- [RedisVL](https://redis.io/docs/latest/integrate/redisvl/)

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-agentic-architecture-patterns` | `skill` | Redis is part of a broader agent memory, cache, context, or guardrail design. |
| `foundry-agent-blueprint` | `skill` | Redis must be mapped into Foundry Agent Service connections or tools. |
| `azure-infrastructure` | `skill` | Network, identity, or private endpoint architecture needs broader Azure design. |
| `azure-cli` | `skill` | Azure CLI deployment or live resource inspection is required. |
| `azure-terraform-cli` | `skill` | Terraform plan or apply workflow is required. |

## Quality gate

- [ ] `name` matches the `azure-managed-redis-cache` directory.
- [ ] The Redis role, SKU profile, access model, and network posture are explicitly stated.
- [ ] Balanced, MemoryOptimized, ComputeOptimized, and FlashOptimized guidance is preserved when SKU selection is discussed.
- [ ] RedisVL, vector search, RediSearch modules, tenant key namespace, TTL, and invalidation are considered where relevant.
- [ ] Every bundled resource path referenced above exists.
- [ ] The response follows the output template with validation evidence.
