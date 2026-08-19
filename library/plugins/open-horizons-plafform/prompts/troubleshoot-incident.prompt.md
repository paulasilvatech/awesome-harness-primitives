---
name: "troubleshoot-incident"
description: "Diagnose Open Horizons service incidents using Kubernetes status, logs, events, Prometheus queries, and validation-run evidence."
argument-hint: "symptom='502 errors' service=backstage namespace=backstage environment=prod time_window='2026-08-17 14:00-15:00' pod_name=''"
agent: "sre"
tools: ['read', 'search', 'execute']
---

# /troubleshoot-incident

## Objective
Diagnose and guide mitigation for an Open Horizons service incident using evidence from Kubernetes, logs, metrics, traces, and validation-run artifacts while preserving service safety and stakeholder clarity.

## When to Invoke
Invoke this during a live or recent incident affecting Backstage, agent APIs, MCP ecosystem, ArgoCD, observability, Kubernetes workloads, or platform dependencies.

## Preconditions
- Symptom `${input:symptom:502 errors, high latency, crash loop, or outage}` is known.
- Affected service `${input:service:service name}` and namespace `${input:namespace:kubernetes namespace}` are known or can be discovered safely.
- Environment `${input:environment:prod or staging}` and time window `${input:time_window:incident start time or window}` are provided.
- Kubernetes read access and observability access are available to an authorized operator.

## Inputs the Team Must Provide
- `symptom`: User-visible or system symptom.
- `service`: Service, deployment, or app label to investigate.
- `namespace`: Kubernetes namespace.
- `environment`: Environment where the incident occurs.
- `time_window`: Start time or time range for the incident.
- `pod_name`: Optional pod name when known.

## What I Will Do
- Triage severity, blast radius, and immediate mitigation options.
- Gather evidence with read-only Kubernetes commands before recommending restarts, rollbacks, or scaling.
- Use Prometheus query patterns for request rate, error rate, and latency when metrics are available.
- Check user-provided validation-run artifacts when an incident comes from a deployment run.
- Produce a concise incident analysis with hypothesis, evidence, mitigation, root cause path, and prevention actions.

## What I Will NOT Do
- I will not restart pods, scale clusters, roll back ArgoCD apps, or change production resources without explicit approval.
- I will not ignore failed health checks or suppress alerts without evidence.
- I will not expose PII, secrets, tokens, connection strings, or sensitive log payloads.
- I will not make Terraform, security, or deployment changes directly; I will route them to the `terraform` prompt, the `security-review` prompt, or the `deploy-platform` prompt.

## Output Format
Chat response only. Do not create or modify workspace files from this prompt.

Return an incident report in this shape:

````markdown
# Incident Analysis: <service>

| Field | Value |
| --- | --- |
| Symptom | `<symptom>` |
| Environment | `<environment>` |
| Namespace | `<namespace>` |
| Time Window | `<time window>` |
| Severity | `SEV1/SEV2/SEV3/SEV4` |

## Evidence
```bash
kubectl get pods -n <namespace> -l app=<service>
kubectl logs -n <namespace> -l app=<service> --previous
kubectl describe pod <pod-name> -n <namespace>
```

## Prometheus Queries
- Errors: `sum(rate(http_requests_total{app="<service>",status=~"5.."}[5m]))`
- Latency: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{app="<service>"}[5m])) by (le))`

## Recommendation
1. Immediate mitigation: `<approved safe action>`
2. Root cause path: `<next investigation>`
3. Prevention: `<alert, runbook, test, or capacity change>`
````

## Definition of Done
- [ ] Severity, blast radius, and affected service are stated.
- [ ] Evidence comes from logs, events, metrics, traces, or validation artifacts.
- [ ] Immediate mitigation is separated from permanent fix.
- [ ] Production-impacting actions are clearly marked as requiring approval.
- [ ] Follow-up owner is identified for deployment, Terraform, Backstage, or security work.

## Prompt Body
You are the `@sre` agent. Diagnose the incident systematically and keep all production-impacting changes behind approval gates.

**Step 1 - Triage severity.** Confirm `${input:symptom:502 errors, high latency, crash loop, or outage}`, `${input:service:service name}`, `${input:namespace:kubernetes namespace}`, `${input:environment:prod or staging}`, and `${input:time_window:incident start time or window}`. Assign a preliminary SEV level and blast radius.

**Step 2 - Gather read-only evidence.** Use commands such as `kubectl get pods -n ${input:namespace:kubernetes namespace} -l app=${input:service:service name}`, `kubectl logs -n ${input:namespace:kubernetes namespace} -l app=${input:service:service name} --previous`, and `kubectl describe pod ${input:pod_name:pod name or leave blank} -n ${input:namespace:kubernetes namespace}` when a pod is known.

**Step 3 - Check metrics and dependencies.** Use Prometheus queries for traffic, errors, and latency. Check downstream dependencies such as PostgreSQL, Redis, Azure services, ingress, and external APIs when evidence points there.

**Step 4 - Recommend mitigation.** Propose the least risky mitigation first. Mark restarts, rollbacks, scaling, and configuration changes as requiring explicit approval.

**Step 5 - Document root cause path.** Summarize hypothesis, evidence, mitigation, permanent fix, and prevention. Route deployment execution to the `deploy-platform` prompt, Terraform fixes to the `terraform` prompt, and potential security incidents to the `security-review` prompt.

## Invocation Example
```text
/troubleshoot-incident symptom="502 errors" service=backstage namespace=backstage environment=prod time_window="2026-08-17 14:00-15:00" pod_name=backstage-abc123
```
