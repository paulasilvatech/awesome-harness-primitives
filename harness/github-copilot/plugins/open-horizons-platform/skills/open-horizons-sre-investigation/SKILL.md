---
name: open-horizons-sre-investigation
description: >-
  Investigates one Open Horizons reliability symptom or incident through read-only telemetry, timeline construction, causal hypothesis testing, ownership assignment, and verification planning. Use when investigating outages, latency, errors, unhealthy workloads, alerts, SLO breaches, or deployment regressions.
---

# Open Horizons SRE investigation

Turn one observed reliability symptom into tested hypotheses and an evidence-backed owner without changing workloads.

## When to invoke

- Investigate an Open Horizons outage, error spike, latency regression, or unhealthy workload.
- Analyze Prometheus, Grafana, Azure Monitor, Application Insights, Kubernetes events, or logs.
- Establish impact and likely root cause after a deployment.
- Define mitigation requirements, observability gaps, and post-fix verification.

## Prerequisites and context

Require the symptom, affected service/environment, time window, user impact, recent changes, and
available telemetry. Use read-only access and redact credentials, tokens, PII, and sensitive payloads.

## Procedure

1. Establish incident status, severity, impact, start time, affected services, and current mitigation.
2. Build a timeline from deployment, alert, metric, event, trace, and log timestamps.
3. Check service health and high-signal indicators before collecting broad logs.
4. Form two or three causal hypotheses and define one discriminating check for each.
5. Run targeted read-only queries, preserve query and time range, and record confirming or
   falsifying evidence.
6. Identify the most likely owning component and distinguish immediate mitigation from permanent fix.
7. Define post-fix verification, alert gaps, SLO impact, and runbook updates; return changes to owners.

## Criteria

| Conclusion | Requirement |
| --- | --- |
| Confirmed root cause | Evidence demonstrates mechanism and a discriminating check rules out alternatives |
| Likely cause | Strong evidence exists but one material dependency remains unverified |
| Hypothesis | Plausible explanation without sufficient evidence |
| Blocked | Required telemetry or authorization is unavailable |

## Output template

```markdown
## SRE investigation result

**Status:** INVESTIGATING | MITIGATED | ROOT-CAUSE-CONFIRMED | BLOCKED
**Impact:** <users/services/severity>
**Window:** <start/end and timezone>

### Hypotheses
| Hypothesis | Discriminating check | Evidence | Result |
| --- | --- | --- | --- |

### Outcome
- Most likely owner: <component/agent>
- Mitigation requirement: <action or none>
- Permanent-fix requirement: <action or unknown>
- Verification: <query/check>
- Observability gaps: <list or none>
```

## Limits

- Do not edit code, dashboards, alerts, SLOs, runbooks, manifests, or infrastructure.
- Do not restart, scale, roll back, delete, or reroute workloads.
- Do not treat temporal correlation as causation or expose sensitive telemetry.
- Do not make security conclusions; route indicators to the security reviewer.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-sre-investigator` | `agent` | A read-only incident owner should execute this method. |
| `observability-stack` | `skill` | Product-specific metric, dashboard, or alert references are needed. |
| `pipeline-diagnostics` | `skill` | Evidence points to CI/CD failure rather than runtime behavior. |
| `open-horizons-deployment-operator` | `agent` | An approved mitigation or rollback must execute. |

## Quality gate

- [ ] Impact, time window, and recent changes are explicit.
- [ ] Multiple hypotheses and discriminating checks were considered.
- [ ] Queries and evidence are timestamped and sanitized.
- [ ] No repository or workload state changed.
- [ ] Owner, mitigation, permanent-fix requirement, and verification are explicit.