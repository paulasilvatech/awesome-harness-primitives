---
name: azure-cost-optimize
description: >-
  Analyzes Azure IaC and current Azure cost or utilization evidence to identify, quantify, and
  prioritize savings. Use when reviewing Azure spend, right-sizing resources, reducing waste, or
  preparing evidence-based cost optimization issues.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/azure-cost-optimize/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure cost optimization

Turn Azure IaC plus validated cost and utilization evidence into prioritized, reviewable savings recommendations.

## When to invoke

- Reduce Azure spend or identify unused resources.
- Right-size deployed Azure services from observed usage.
- Compare current and target SKU cost.
- Prepare cost-optimization findings or GitHub issues.

## Prerequisites and context

- Confirm subscription, billing scope, time window, currency, and target environments.
- Read only Azure IaC: `**/*.bicep`, `**/*.tf`, `**/main.json`, and ARM template JSON.
- Stop when no relevant IaC exists; do not infer architecture from arbitrary application files.
- Obtain current cost and utilization evidence before calculating savings.

## Procedure

1. Confirm scope, currency, cost period, business criticality, and excluded resources.
2. Inspect IaC for resource types, regions, SKUs, capacity, redundancy, retention, and scaling.
3. Query current cost from Cost Management or another approved billing source and record the period.
4. Query utilization or service metrics needed to justify each optimization; mark missing evidence.
5. Compare current state with supported lower-cost configurations and operational constraints.
6. Calculate current monthly cost, target monthly cost, monthly savings, and implementation effort.
7. Rank findings using the deterministic score below; do not invent cost or utilization values.
8. Present findings for approval. Create issues only when explicitly approved; otherwise return Markdown.

## Criteria

| Pattern | Evidence required | Typical recommendation |
| --- | --- | --- |
| Idle resource | No meaningful use during agreed window | Stop, delete, or schedule after approval |
| Over-sized compute | Sustained utilization below agreed threshold | Right-size after performance validation |
| Excess retention | Retention exceeds policy or recovery need | Reduce retention with rollback analysis |
| Redundant premium tier | Feature set is unused | Select supported lower tier |
| Unbounded scale | Capacity lacks budget or usage guard | Add scaling and budget controls |
| Commitment opportunity | Stable long-term baseline exists | Compare reservation or savings option |

Use:

$$
\text{priority score} = \frac{\text{business value} \times \text{monthly savings}}{\text{risk} \times \text{implementation days}}
$$

State every scale and assumption used in the score.

## Output template

```markdown
## Azure cost optimization summary

**Status:** COMPLETE | BLOCKED
**Scope:** <subscription/resource groups/time window/currency>

| Priority | Resource | Evidence | Current/month | Target/month | Savings/month | Risk | Action |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |

### Assumptions and missing evidence
- <item or none>

### Issue creation
- Approval: <granted/not granted>
- Created issues: <links or none>
```

## Limits

- Do not fabricate prices, utilization, savings, or ROI.
- Do not change SKUs, scale, retention, reservations, budgets, or resources from this skill.
- Do not recommend deletion without ownership, dependency, backup, and rollback evidence.
- Use current Azure pricing and billing sources; region and offer availability vary.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-pricing` | `skill` | Current retail prices or SKU comparisons are required. |
| `azure-cli` | `skill` | Read-only resource or metric discovery is required. |
| `open-horizons-terraform` | `agent` | An approved recommendation needs IaC implementation. |
| `open-horizons-security-reviewer` | `agent` | Savings may weaken security, resilience, or compliance. |

## Quality gate

- [ ] Scope, period, currency, and exclusions are explicit.
- [ ] Every recommendation references IaC and current evidence.
- [ ] Current cost, target cost, and monthly savings show their source.
- [ ] Risk, effort, dependencies, and rollback are considered.
- [ ] Issue creation or Azure mutation did not occur without approval.

## References

- [Azure Cost Management documentation](https://learn.microsoft.com/azure/cost-management-billing/)
- [Azure Advisor cost recommendations](https://learn.microsoft.com/azure/advisor/advisor-cost-recommendations)
