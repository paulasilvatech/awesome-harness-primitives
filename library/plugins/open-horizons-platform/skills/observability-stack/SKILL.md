---
name: observability-stack
description: 'Use when deploying or operating the Open Horizons observability stack: Prometheus, Grafana, Alertmanager, Loki-adjacent logging checks, dashboards, service monitors, alert rules, and day-2 monitoring diagnostics. Produces deployment plans, Helm/Kubernetes commands, dashboard and alert validation, and health reports. DO NOT USE FOR: application logging code, Terraform IaC (use terraform-cli), CI/CD pipelines (use deploy-orchestration). Triggers include "deploy monitoring", "configure Grafana dashboards", "check Prometheus targets", and "troubleshoot alerts".'
---

# Observability Stack

Use this skill to deploy, validate, and troubleshoot Open Horizons monitoring assets using `deploy/helm/monitoring/values.yaml`, `deploy/helm/service-monitors.yaml`, `deploy/helm/sre-alerts.yaml`, `grafana/dashboards/`, and `terraform/modules/observability/`. It produces a risk-ranked plan, approved commands, and a health report.

> [!NOTE]
> This skill depends on `kubectl`, `helm`, cluster credentials, access to the monitoring namespace, and Grafana or Prometheus credentials from the approved secret store. It does not use an MCP server by default.

## When to invoke

- "Deploy the observability stack to the cluster."
- "Check whether Prometheus targets are healthy."
- "Load the dashboards from grafana/dashboards."
- "Validate the SRE alert rules."
- "Troubleshoot why Grafana is not reachable."

## Prerequisites and context

- `kubectl config current-context` points to the intended cluster.
- `helm version` succeeds.
- `deploy/helm/monitoring/values.yaml` exists.
- `deploy/helm/service-monitors.yaml` and `deploy/helm/sre-alerts.yaml` exist when applying Open Horizons monitoring resources.
- `grafana/dashboards/` exists for dashboard inventory.

## Procedure

### Step 1: Inspect current monitoring state

```bash
kubectl get namespaces
kubectl get pods -n monitoring
helm list -n monitoring
kubectl get pods -n observability
```

Use whichever namespace exists. Do not create or mutate namespaces until the confirmation gate.

### Step 2: Validate repository monitoring assets

```bash
test -f deploy/helm/monitoring/values.yaml
test -f deploy/helm/service-monitors.yaml
test -f deploy/helm/sre-alerts.yaml
test -d grafana/dashboards
```

### Step 3: Preview Helm deployment

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring   --values deploy/helm/monitoring/values.yaml   --dry-run
```

### Step 4: Preview Kubernetes monitoring resources

```bash
kubectl apply -f deploy/helm/service-monitors.yaml --dry-run=client -o yaml
kubectl apply -f deploy/helm/sre-alerts.yaml --dry-run=client -o yaml
kubectl diff -f deploy/helm/service-monitors.yaml
kubectl diff -f deploy/helm/sre-alerts.yaml
```

### Step 5: Classify observability risk

| Risk | Meaning |
| --- | --- |
| High | Installing or upgrading monitoring stack, changing alert routes, deleting PVCs, or modifying production alerts. |
| Medium | Applying ServiceMonitor, PrometheusRule, dashboard ConfigMap, or scrape configuration changes. |
| Low | Reading pods, targets, dashboards, logs, events, or rendering dry-runs. |

### Step 6: User confirmation gate

```text
Observability action: <install|upgrade|apply-rules|apply-dashboards>
Cluster context: <context>
Namespace: <monitoring|observability>
Assets: deploy/helm/monitoring/values.yaml, deploy/helm/service-monitors.yaml, deploy/helm/sre-alerts.yaml, grafana/dashboards/
Risk: <High|Medium|Low>
Proceed with observability mutation? (y/n)
```

> [!IMPORTANT]
> Only install, upgrade, apply, delete, or modify observability resources after an explicit affirmative response. On a negative, ambiguous, or missing response, do not mutate the cluster; output dry-run findings and stop.

### Step 7: Execute approved deployment or update

```bash
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring   --create-namespace   --values deploy/helm/monitoring/values.yaml   --wait --timeout 15m
kubectl apply -f deploy/helm/service-monitors.yaml
kubectl apply -f deploy/helm/sre-alerts.yaml
```

### Step 8: Verify health and targets

```bash
kubectl get pods -n monitoring
kubectl get servicemonitor -A
kubectl get prometheusrule -A
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Then query Prometheus locally when the port-forward is running.

```bash
curl -s 'http://localhost:9090/api/v1/targets'
```

## Limits

- Do not use this skill for: application logging code, Terraform IaC (use terraform-cli), CI/CD pipelines (use deploy-orchestration).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Monitoring namespace is absent | Treat install as High risk and require approval before creating it. |
| Helm dry-run fails | Report values or chart errors and stop before mutation. |
| CRDs are missing | Install or upgrade kube-prometheus-stack only after approval. |
| Prometheus targets are down | Report target labels, scrape URL, and last error. |
| Grafana credentials are unavailable | Do not guess credentials; request retrieval from the approved secret store. |

## Output template

Return exactly this structure:

```markdown
## Observability Report

**Cluster context:** <context>
**Namespace:** <namespace>
**Action:** <inspect|install|upgrade|apply|troubleshoot>
**Risk:** <High|Medium|Low>

### Asset Validation
- `deploy/helm/monitoring/values.yaml`: <present|missing>
- `deploy/helm/service-monitors.yaml`: <present|missing>
- `deploy/helm/sre-alerts.yaml`: <present|missing>
- `grafana/dashboards/`: <present|missing>

### Health
- Prometheus: <status>
- Grafana: <status>
- Alertmanager: <status>
- Targets: <summary>

### Findings
- <finding>
```

## Quality gate

- [ ] Confirmed cluster context and monitoring namespace.
- [ ] Verified all referenced monitoring files and directories exist.
- [ ] Ran Helm dry-run before install or upgrade.
- [ ] Ran Kubernetes dry-run or diff before applying rules or monitors.
- [ ] Received explicit approval before mutating monitoring resources.
- [ ] Verified pods, ServiceMonitors, PrometheusRules, and targets after mutation.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
