---
name: open-horizons-azure-readiness
description: >-
  Assesses read-only Azure readiness for one Open Horizons deployment scope using current subscription, provider, quota, SKU, identity, network, and resource evidence. Use when needed before Terraform planning or deployment when Azure prerequisites may block the requested components.
---

# Open Horizons Azure readiness

Produce a current readiness verdict without modifying Azure, local credentials, kubeconfig, or Terraform state.

## When to invoke

- Validate a subscription and region before an Open Horizons plan.
- Check providers, quota, SKUs, identities, networking prerequisites, or naming collisions.
- Assess AKS, ACR, Key Vault, PostgreSQL, Managed Redis, AI Search, or Microsoft Foundry readiness.
- Recheck a previously blocked Azure prerequisite.

## Prerequisites and context

Require the target tenant/subscription, environment, region, requested components, expected
capacity, resource group when known, and data-residency constraints. Use Reader-equivalent access
and query only metadata required for the verdict.

## Procedure

1. Confirm tenant, subscription, environment, region, requested components, and expected capacity.
2. Inspect the owning Terraform root or module to derive providers, resource types, SKU families,
   identities, network dependencies, and naming requirements.
3. Verify the active Azure context before resource queries.
4. Query provider registration state, regional usage and quota, SKU availability, deployment slots,
   identities, private-network prerequisites, naming collisions, and existing resource metadata.
5. Avoid secret values and do not acquire AKS credentials; Azure resource metadata is sufficient.
6. Classify every requested component and return blockers to the correct owner.

## Criteria

| Verdict | Meaning |
| --- | --- |
| PASS | Current evidence satisfies the requested prerequisite |
| FAIL | Current evidence proves the prerequisite is not satisfied |
| BLOCKED | Required evidence cannot be obtained safely or permissions are insufficient |
| NOT REQUESTED | Component is outside the supplied scope |

## Output template

```markdown
## Azure readiness result

**Status:** PASS | FAIL | BLOCKED
**Context:** <tenant / subscription / environment / region / timestamp>

### Components
| Component | Required state | Evidence | Verdict | Owner |
| --- | --- | --- | --- | --- |

### Blockers
- <provider, quota, SKU, identity, network, collision, permission, or none>

### Follow-up
- <open-horizons-terraform | open-horizons-security-reviewer | deployment operator | none>
```

## Limits

- Do not register providers, request quota, create resources, change policy, set subscriptions,
  retrieve secrets, run `az aks get-credentials`, mutate kubeconfig, or run Terraform.
- Do not hardcode a preferred region, AKS version, SKU, or quota as current availability.
- Do not reuse stale evidence without a timestamp and unchanged target context.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-azure-readiness` | `agent` | A read-only readiness owner should execute this procedure. |
| `azure-cli` | `skill` | A narrow read-only Azure command and output shape are needed. |
| `open-horizons-terraform` | `agent` | Readiness findings require Terraform changes. |
| `open-horizons-security-reviewer` | `agent` | Identity or exposure requires independent review. |

## Quality gate

- [ ] Target context and timestamp are explicit.
- [ ] Requirements are derived from the requested repository scope.
- [ ] Every component has current evidence and a verdict.
- [ ] No cloud or local access state changed.
- [ ] Every blocker names an owner and safe next step.