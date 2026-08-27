---
name: azure-cost
description: >-
  Manage Azure cost by querying actual spend, forecasting future spending, and optimizing
  resources to reduce waste. Use when the user asks about Azure costs or bills, wants a cost
  breakdown, asks how much they are spending, wants to forecast spending, optimize or reduce
  spend, find orphaned resources, rightsize VMs, investigate a cost spike, or lower storage and
  AKS costs.
license: MIT
metadata:
  author: Microsoft
  version: 1.3.1
---

<!-- Generated from harness/github-copilot/plugins/azure-observability-operations/skills/azure-cost/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Cost Management Skill

Query historical costs, forecast future spending, optimize to reduce waste.

## When to invoke

- "How much am I spending on Azure this month?"
- "Give me a cost breakdown by resource group."
- "Forecast next quarter Azure spending."
- "Find waste and reduce our Azure bill."

## Routing

| User Intent | Workflow |
|-------------|----------|
| Understand current costs | [Cost Query](cost-query/workflow.md) |
| Reduce costs / find waste | [Cost Optimization](cost-optimization/workflow.md) |
| Project future costs | [Cost Forecast](cost-forecast/workflow.md) |

## Quick Reference

| Property | Value |
|----------|-------|
| **Query API** | `POST {scope}/providers/Microsoft.CostManagement/query?api-version=2023-11-01` |
| **Forecast API** | `POST {scope}/providers/Microsoft.CostManagement/forecast?api-version=2023-11-01` |
| **Required Role** | Cost Management Reader + Monitoring Reader + Reader (on target scope) |

## Scope Patterns

- Subscription: `/subscriptions/<id>`
- Resource Group: `/subscriptions/<id>/resourceGroups/<name>`
- Management Group: `/providers/Microsoft.Management/managementGroups/<id>`
- Billing Account: `/providers/Microsoft.Billing/billingAccounts/<id>`

## Service-Specific Optimization

- [Redis](cost-optimization/services/redis/azure-cache-for-redis.md)
- [Storage](cost-optimization/services/storage/azure-storage.md)

## References

- [MCP Tools, Best Practices, Safety](references/tools-and-best-practices.md)
- [SDK: Redis .NET](cost-optimization/sdk/azure-resource-manager-redis-dotnet.md)

## Output template

```markdown
## Cost analysis result

**Status:** reported | forecast | optimized
**Summary:** <one sentence covering scope and outcome>

### Details
Spend breakdown, forecast, or savings actions with amounts and scope.

### Validation
- <check performed>: <result and evidence>
```

## Quality gate

- [ ] Every figure came from a cost or pricing query, never an estimate from memory.
- [ ] The scope, currency, and time range are stated explicitly.
- [ ] The output follows `## Output template` exactly.
- [ ] Every reported check was performed and its evidence is shown.
- [ ] Irreversible Azure actions were confirmed with the user first.
