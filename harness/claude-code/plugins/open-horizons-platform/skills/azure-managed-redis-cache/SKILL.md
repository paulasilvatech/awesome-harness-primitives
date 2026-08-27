---
name: azure-managed-redis-cache
description: >-
  Use when designing or provisioning Azure Managed Redis for cache, semantic cache, vector memory,
  session store, or agent memory in AI-native systems; produces SKU guidance, network and identity
  controls, Bicep deployment steps, and integration recommendations. DO NOT USE FOR: general agent
  architecture (use agentic-architecture-patterns), Foundry agent runtime design (use
  foundry-agent-blueprint), or general Azure infrastructure (use azure-infrastructure). Triggers
  include "design Redis semantic cache", "provision Azure Managed Redis", "add vector memory".
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/azure-managed-redis-cache/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Managed Redis Cache

This workflow turns an agent cache or memory requirement into an Azure Managed Redis design, including SKU profile, private networking, managed identity access, key isolation, TTL policy, and optional Bicep deployment. It produces a Redis design note and deployment checklist.

> [!NOTE]
> This skill may shell out to Azure CLI for Bicep deployment using bundled `scripts/redis-managed.bicep`. Resolve bundled paths relative to this `SKILL.md`. Verify current Azure Managed Redis SKUs, API versions, module support, and pricing on Microsoft Learn before provisioning.

## When to invoke
- "Design a Redis semantic cache for our agent gateway."
- "Provision Azure Managed Redis for vector memory."
- "Add session state for agent runs using Redis."
- "Choose the Redis SKU for cache, memory, and tenant isolation."

## Prerequisites and context
- Cache or memory role is known: key-value cache, semantic cache, vector memory, or session store.
- Target region, environment, network posture, and data sensitivity are known.
- Azure CLI is authenticated if deploying.
- Bicep file exists at `scripts/redis-managed.bicep`.
- Reference files exist under `references/`.

## Procedure

### Step 1: Classify the Redis role
| Need | Redis role | Reference |
|---|---|---|
| Reuse repeated prompts or intents | Semantic cache | `references/semantic-cache.md` |
| Store durable agent facts or embeddings | Vector memory | `references/vector-memory.md` |
| Hold conversation or run state | Session store | `references/session-store.md` |
| Secure access and network path | Identity and network | `references/access-and-network.md` |

### Step 2: Select SKU and controls
- [ ] Choose Balanced for general cache and small vector sets.
- [ ] Choose MemoryOptimized for larger working sets.
- [ ] Choose ComputeOptimized for high-throughput or vector-heavy workloads.
- [ ] Choose FlashOptimized only when very large datasets justify tiered storage.
- [ ] Use tenant and user key namespaces such as `t:<tenant>:u:<user>:<purpose>`.
- [ ] Require TLS and managed identity where supported.
- [ ] Prefer private endpoint and disabled public network access for sensitive workloads.

### Step 3: Confirm before provisioning
```text
Redis deployment summary:
- Name:
- Resource group:
- Location:
- SKU:
- Public network access:
- Data roles:
Proceed with Azure Managed Redis deployment or update? (y/n)
```

> [!IMPORTANT]
> Only proceed with Redis deployment, SKU changes, or paid resource updates if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the design and stop.

### Step 4: Deploy from the repository Bicep when approved
```bash
az deployment group create \
  --resource-group <resource-group> \
  --template-file scripts/redis-managed.bicep \
  --parameters name=<redis-name> location=<location> sku=Balanced_B1 publicNetworkAccess=Disabled
```

### Step 5: Validate integration decisions
- [ ] Application uses managed identity or Key Vault-managed connection secrets.
- [ ] Semantic cache threshold, TTL, invalidation, and embedding model are documented.
- [ ] Vector memory read/write policy prevents cross-tenant leakage.
- [ ] Session keys have expiration and bounded payload size.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Cross-tenant key leakage, public access for sensitive memory, or secrets committed to code. |
| High | No TTL/invalidation for semantic cache, no managed identity plan, or undersized production SKU. |
| Medium | Missing private DNS, unclear vector schema, or no cache observability. |
| Low | Naming, tagging, or documentation gaps. |

## Limits

- Do not use this skill for: general agent architecture (use agentic-architecture-patterns), Foundry agent runtime design (use foundry-agent-blueprint), or general Azure infrastructure (use azure-infrastructure).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| SKU is unavailable | Verify current regional SKU availability and choose an approved alternative. |
| Bicep deployment fails | Report the Azure error, resource group, and parameters; do not retry with different settings without approval. |
| Managed identity is unsupported by client path | Use Key Vault for secrets and document the migration path to identity. |
| Public access is required temporarily | Add an expiration, network restriction, and risk note. |

## Output template

Return exactly this structure:
```markdown
# Azure Managed Redis Design

## Scope
- Role:
- Environment:
- Region:

## SKU And Network
| Decision | Value | Rationale |
|---|---|---|

## Key Design
- Namespace:
- TTL:
- Invalidation:

## Deployment
```bash
az deployment group create --resource-group <resource-group> --template-file scripts/redis-managed.bicep --parameters name=<redis-name>
```

## Risks
| Severity | Finding | Mitigation |
|---|---|---|
```

## Quality gate
- [ ] Redis role, SKU, network posture, and identity model are documented.
- [ ] Paid deployment or SKU changes have explicit confirmation.
- [ ] Tenant isolation and TTL policy are defined.
- [ ] Bicep path and all references exist in the repository.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
