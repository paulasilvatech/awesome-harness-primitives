---
name: azure-well-architected-review
description: >-
  Reviews Azure workload IaC and current resource evidence against all five Azure Well-Architected Framework pillars. Use when assessing reliability, security, cost optimization, operational excellence, or performance efficiency and preparing prioritized findings.
---

# Azure Well-Architected review

Perform an evidence-based five-pillar review and return prioritized, IaC-first findings.

## When to invoke

- Review an Azure workload against the Well-Architected Framework.
- Assess Azure IaC before production or a major change.
- Compare deployed resources with intended IaC and identify drift.
- Prepare WAF findings or an approved issue backlog.

## Prerequisites and context

Confirm subscription/resource-group scope, environments, business criticality, workload owners,
recovery objectives, data classification, cost constraints, and review time window.

## Procedure

1. Confirm scope and load current Microsoft WAF guidance plus service-specific recommendations.
2. Inspect `**/*.bicep`, `**/*.tf`, and ARM template JSON for the intended architecture.
3. Collect approved read-only live inventory and compare it with IaC; flag unmanaged drift.
4. Review every pillar using the criteria below and record evidence or missing evidence.
5. Classify findings by demonstrated impact and likelihood, not generic best-practice language.
6. Present a summary and obtain explicit approval before creating GitHub issues.
7. For approved findings, create one issue per root cause plus an optional tracking epic.

## Criteria

| Pillar | Review focus |
| --- | --- |
| Reliability | Availability zones, failure isolation, backup/restore, recovery objectives, health checks, capacity and dependency failures |
| Security | Identity, least privilege, secrets, network boundaries, encryption, policy, threat detection, secure delivery |
| Cost Optimization | Validated spend, utilization, scale, tier, retention, commitment, ownership and budgets |
| Operational Excellence | IaC ownership, deployment safety, observability, incident response, runbooks, drift and change control |
| Performance Efficiency | Service/SKU fit, scaling, quotas, caching, data path, latency, throughput and load evidence |

Severity:

- **High:** credible security exposure, unrecoverable data risk, single critical failure, or inability to restore.
- **Medium:** material reliability, cost, operational, or performance risk with a plausible trigger.
- **Low:** bounded optimization or maintainability gap with limited immediate impact.

## Output template

```markdown
## Azure Well-Architected review result

**Status:** COMPLETE | BLOCKED
**Scope:** <subscription/resource groups/environments>

| Severity | Pillar | Finding | Evidence | Impact | IaC remediation | Validation |
| --- | --- | --- | --- | --- | --- | --- |

### Drift and missing evidence
- <item or none>

### Issue creation
- Approval: <granted/not granted>
- Issues: <links or none>
```

## Limits

- Do not claim compliance or pillar maturity without evidence.
- Do not create issues, deploy, or modify Azure resources without approval.
- Prefer IaC remediation; CLI commands are validation or recovery guidance, not the source of truth.
- Do not fabricate availability, cost, performance, or recovery metrics.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-infrastructure` | `skill` | A finding needs an Azure architecture pattern. |
| `azure-pricing` | `skill` | Cost evidence requires current pricing. |
| `open-horizons-architect` | `agent` | Findings require a cross-domain architecture decision. |
| `open-horizons-security-reviewer` | `agent` | A security finding needs independent validation. |

## Quality gate

- [ ] Scope and workload quality attributes are explicit.
- [ ] All five pillars were reviewed.
- [ ] Findings cite IaC or current read-only evidence.
- [ ] Drift and missing evidence are visible.
- [ ] Severity, owner, remediation, and validation are actionable.
- [ ] Issues were created only after explicit approval.

## References

- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)