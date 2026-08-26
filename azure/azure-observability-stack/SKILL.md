---
name: azure-observability-stack
description: >-
  Deploys and operates Prometheus, Grafana, Loki, and Alertmanager for Open Horizons observability. Use this skill when deploying the monitoring stack, configuring dashboards, validating alert rules, checking metrics, reviewing SLO signals, or troubleshooting observability behavior.
---

# Azure Observability Stack

Use platform observability intent and cluster access to deploy, validate, and operate Prometheus, Grafana, Loki, and Alertmanager with concrete command evidence.

## When to invoke

- "Deploy the observability stack for Open Horizons."
- "Configure monitoring for platform components."
- "Create or manage Grafana dashboards."
- "Configure alerting rules and notification channels."
- "Troubleshoot platform metrics, targets, alerts, or logs."

## Prerequisites and context

- kubectl access to target cluster.
- Helm 3.12+ installed.
- AKS cluster deployed (H1 Foundation).

## Procedure

### Installation and deployment

#### 1. Deploy kube-prometheus-stack
```bash
# Add Helm repos
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create namespace
kubectl create namespace monitoring

# Install kube-prometheus-stack with project values
helm install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring   --values deploy/helm/monitoring/values.yaml   --wait --timeout 15m

# Verify all pods are running
kubectl get pods -n monitoring
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=monitoring -n monitoring --timeout=600s
```

#### 2. Deploy Custom Dashboards
```bash
# Create ConfigMap from project dashboards
kubectl create configmap grafana-dashboards   --namespace monitoring   --from-file=grafana/dashboards/   --dry-run=client -o yaml | kubectl apply -f -

# Label for Grafana sidecar auto-discovery
kubectl label configmap grafana-dashboards   --namespace monitoring   grafana_dashboard=1
```

#### 3. Deploy Custom Alert Rules
```bash
# Apply Prometheus alerting rules
kubectl apply -f prometheus/alerting-rules.yaml -n monitoring

# Apply recording rules
kubectl apply -f prometheus/recording-rules.yaml -n monitoring

# Validate rules syntax
promtool check rules prometheus/alerting-rules.yaml
promtool check rules prometheus/recording-rules.yaml
```

#### 4. Verify Installation
```bash
# Check all components
kubectl get pods -n monitoring

# Port-forward Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

# Port-forward Prometheus
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090

# Check Prometheus targets
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets | length'

# Verify Grafana datasources
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:?Set GRAFANA_PASSWORD from your secret store}"
curl -s -u "${GRAFANA_USER}:${GRAFANA_PASSWORD}" http://localhost:3000/api/datasources | jq '.[].name'
```

### Day-2 operations

#### Prometheus Operations
```bash
# Check Prometheus status
kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus

# Port forward Prometheus
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090

# Query Prometheus API
curl -s http://localhost:9090/api/v1/query?query=up | jq '.data.result'

# Check targets
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets | length'
```

#### Grafana Operations
```bash
# Check Grafana status
kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana

# Port forward Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

# List data sources
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:?Set GRAFANA_PASSWORD from your secret store}"
curl -s -u "${GRAFANA_USER}:${GRAFANA_PASSWORD}" http://localhost:3000/api/datasources | jq '.[].name'
```

#### Alert Management
```bash
# Check alertmanager
kubectl get pods -n monitoring -l app.kubernetes.io/name=alertmanager

# List active alerts
curl -s http://localhost:9093/api/v2/alerts | jq '.[].labels.alertname'

# Validate Prometheus rules
promtool check rules prometheus/alerting-rules.yaml
```

## Output template

Return exactly this structure:

```markdown
# Observability stack result

**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing monitoring readiness or the issue found.

### Component status
| Component | Namespace | Result | Evidence |
| --- | --- | --- | --- |
| Prometheus | monitoring | PASS | Pod, target, or API evidence |
| Grafana | monitoring | PASS | Pod or datasource evidence |
| Alertmanager | monitoring | PASS | Pod or alert evidence |

### Details
- Commands executed or recommended.
- Dashboards, rules, or values files validated.
- Active alerts, scrape errors, or log findings.

### Validation evidence
- Pods: PASS | FAIL with `kubectl` summary.
- Rules: PASS | FAIL with `promtool` summary.
- Datasources or targets: PASS | FAIL with API summary.
```

## Limits

- Do not use this skill for application logging code.
- Use `azure-terraform-cli` (`skill`) instead when the task is Terraform IaC for observability infrastructure.
- Use `azure-kubectl-cli` (`skill`) instead when the task is direct Kubernetes inspection outside observability workflows.
- Use `github-pipeline-diagnostics` (`skill`) instead when the task is CI/CD pipeline diagnostics.

## Progressive disclosure and bundled resources

- `references/project-reference.md`: project file paths and observability best practices.
- `references/troubleshooting.md`: Prometheus, Grafana, and scrape-error troubleshooting commands.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `azure-kubectl-cli` | `skill` | Kubernetes inspection or namespace operations are the primary task. |
| `azure-helm-cli` | `skill` | Helm install, upgrade, rollback, or values operations are the primary task. |
| `azure-terraform-cli` | `skill` | Terraform changes to the observability module are required. |
| `open-horizons-deploy-orchestration` | `skill` | Script-based post-deploy validation is required. |
| `github-pipeline-diagnostics` | `skill` | The problem is a GitHub Actions or CI/CD failure. |
| `open-horizons-sre-investigator` | `agent` | Reliability investigation, SLOs, alerts, or incidents need ownership. |
| `open-horizons-deployment-operator` | `agent` | Observability deployment is part of an approved full platform rollout. |

## Quality gate

- [ ] Helm, kubectl, and cluster prerequisites are verified before install or operation.
- [ ] Pod readiness is checked for monitoring components.
- [ ] Prometheus targets or API queries provide evidence for metrics readiness.
- [ ] Grafana datasources or dashboards are verified when Grafana is in scope.
- [ ] Prometheus alerting and recording rules are checked when rule files are in scope.
- [ ] Secrets such as `GRAFANA_PASSWORD` are read from the secret store or environment, not written into output.
