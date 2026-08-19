---
name: helm-cli
description: 'Use when managing Helm packages for Kubernetes: repo add/update, template rendering, chart linting, install, upgrade, rollback, uninstall, and release inspection. Produces validated Helm commands, rendered manifests, release status, and rollback guidance. DO NOT USE FOR: kubectl operations (use kubectl-cli), ArgoCD sync (use argocd-cli), Terraform IaC (use terraform-cli). Triggers include "install this Helm chart", "upgrade the monitoring release", "rollback a Helm release", and "lint these Helm values".'
---

# Helm CLI

Use this skill to operate Helm charts for Open Horizons Kubernetes services, especially monitoring values in `deploy/helm/monitoring/values.yaml` and other chart values under `deploy/helm/`. It produces a safe command plan, dry-run output, release status, and the exact command to run after approval.

> [!NOTE]
> This skill depends on the `helm` CLI, `kubectl` access to the target AKS or kind cluster, configured Kubernetes credentials, and authenticated chart registry access when private charts are used. It does not use an MCP server by default.

## When to invoke

- "Install the kube-prometheus-stack chart with our repo values."
- "Upgrade the monitoring Helm release in the monitoring namespace."
- "Rollback the last Helm upgrade because Grafana is unhealthy."
- "Render the Helm templates before we deploy."
- "Check which Helm releases are installed in the cluster."

## Prerequisites and context

- `helm version` succeeds with Helm 3.x.
- `kubectl config current-context` points to the intended cluster.
- The target namespace is known and exists, or the user approved namespace creation.
- Values files exist, for example `deploy/helm/monitoring/values.yaml`.
- For external charts, the chart repository URL is known and reachable.

## Procedure

### Step 1: Confirm scope and current state

1. Identify the release name, namespace, chart, and values file.
2. Show the active cluster and namespace before any change:

```bash
kubectl config current-context
helm list -A
```

3. For monitoring work, verify the repo values file exists:

```bash
test -f deploy/helm/monitoring/values.yaml
```

### Step 2: Prepare chart repositories

Use explicit repository names and URLs. Keep repository setup separate from release mutation.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo prometheus-community/kube-prometheus-stack
```

### Step 3: Validate and render before mutation

Render templates and lint the chart or local chart path before install or upgrade.

```bash
helm lint prometheus-community/kube-prometheus-stack --values deploy/helm/monitoring/values.yaml
helm template monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring   --values deploy/helm/monitoring/values.yaml
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring   --values deploy/helm/monitoring/values.yaml   --dry-run
```

### Step 4: Classify release risk

| Risk | Meaning |
| --- | --- |
| High | Uninstall, rollback across major chart versions, CRD changes, or production namespace mutation. |
| Medium | Upgrade or install with persistent volumes, ingress, RBAC, or service account changes. |
| Low | Repository update, list, status, history, lint, template, or dry-run only. |

### Step 5: User confirmation gate

```text
Helm action: <install|upgrade|rollback|uninstall>
Release: <release>
Namespace: <namespace>
Cluster context: <context>
Values: deploy/helm/monitoring/values.yaml
Risk: <High|Medium|Low>
Proceed with the Helm mutation? (y/n)
```

> [!IMPORTANT]
> Only run `helm install`, `helm upgrade`, `helm rollback`, or `helm uninstall` after an explicit affirmative response. On a negative, ambiguous, or missing response, do not mutate the cluster; output the dry-run findings and stop.

### Step 6: Execute the approved operation

```bash
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring   --create-namespace   --values deploy/helm/monitoring/values.yaml   --wait --timeout 15m
```

For rollback, inspect history first and then run only the approved revision.

```bash
helm history monitoring --namespace monitoring
helm rollback monitoring <revision> --namespace monitoring --wait --timeout 10m
```

### Step 7: Verify release health

```bash
helm status monitoring --namespace monitoring
kubectl get pods -n monitoring
kubectl get events -n monitoring --sort-by='.lastTimestamp'
```

## Limits

- Do not use this skill for: kubectl operations (use kubectl-cli), ArgoCD sync (use argocd-cli), Terraform IaC (use terraform-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Helm repo is unreachable | Stop before mutation and report the failed URL and command output. |
| Values file is missing | Ask for the correct values path; do not substitute a default. |
| Dry-run fails | Report the template or schema error and skip mutation. |
| Release is stuck pending | Run `helm status`, `helm history`, and namespace events; recommend rollback only after approval. |
| Namespace is missing | Include `--create-namespace` only when the user approves namespace creation. |

## Output template

Return exactly this structure:

```markdown
## Helm Operation Report

**Release:** <release>
**Namespace:** <namespace>
**Cluster context:** <context>
**Action:** <lint|template|install|upgrade|rollback|uninstall>
**Risk:** <High|Medium|Low>

### Commands Run
- `<command>`

### Validation
- Lint: <passed|failed|not run>
- Dry-run: <passed|failed|not run>
- Release status: <status>

### Findings
- <finding>

### Next Steps
1. <next step>
```

## Quality gate

- [ ] Confirmed cluster context before any mutation.
- [ ] Verified every referenced values file exists.
- [ ] Ran `helm lint` or documented why lint was not applicable.
- [ ] Ran `helm template` or `helm upgrade --install --dry-run` before mutation.
- [ ] Received explicit approval before install, upgrade, rollback, or uninstall.
- [ ] Verified release status and pod health after approved mutation.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
