---
name: azure-helm-cli
description: >-
  Helm CLI operations manage Kubernetes packages, charts, releases, repositories, values, upgrades, rollbacks, template rendering, release history, chart debugging, and package validation. Use this skill when working with helm install, helm upgrade, helm rollback, helm repo add, helm template, values.yaml, or chart validation.
---

# Azure Helm CLI

Use this skill to turn Helm chart and release requests into ordered CLI workflows, validate charts before deployment, preview rendered manifests, and return release, validation, template, or rollback evidence.

## When to invoke

- "Lint or validate a Helm chart."
- "Render Helm templates before deploying."
- "Install, upgrade, or roll back a Helm release."
- "Add, update, or search a Helm repository."
- "Debug chart values or release history."

## Prerequisites and context

- Helm 3.x installed.
- Kubernetes context configured.
- Access to chart repositories.

## Procedure

1. Confirm the chart path, release name, values file, namespace, and Kubernetes context.
2. Lint or template the chart before install or upgrade when chart changes are involved.
3. Run the narrowest repository or release command that satisfies the request.
4. Capture validation, template, release, or rollback output.
5. Return the result using the output template.

### Chart development

```bash
# Lint chart
helm lint ./chart

# Template rendering
helm template release-name ./chart -f values.yaml

# Dry-run install
helm install release-name ./chart -f values.yaml --dry-run
```

### Repository operations

```bash
# Add repository
helm repo add <name> <url>

# Update repositories
helm repo update

# Search charts
helm search repo <keyword>
```

### Release management

```bash
# List releases
helm list -A

# Install chart
helm install <release> <chart> -f values.yaml -n <namespace>

# Upgrade release
helm upgrade <release> <chart> -f values.yaml -n <namespace>

# Rollback release
helm rollback <release> <revision> -n <namespace>
```

### Best practices

1. ALWAYS lint charts before deploying.
2. Use --dry-run to preview changes.
3. Keep values.yaml files in version control.
4. Use semantic versioning for charts.
5. Document chart dependencies.

## Output template

Return exactly this structure:

```markdown
**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the chart validation, template rendering, repository, install, upgrade, or rollback outcome.

### Details
1. Command executed: `<helm command>`
2. Chart or release: `<chart path/name and release name>`
3. Namespace: `<namespace or all namespaces>`
4. Validation results: `<lint, dry-run, template, or not checked>`
5. Template output: `<summary or not applicable>`
6. Next steps: `<install, upgrade, rollback, inspect, or none>`

### Validation
- Chart check: `<helm lint, helm template, dry-run, or reason not checked>`
- Command result: `<exit code or observed helm output>`
```

## Limits

- Do not use this skill for kubectl cluster operations.
- Use `kubectl-cli` (`skill`) instead when the task is direct Kubernetes resource inspection, logs, events, rollout status, or manifest application.
- Do not use this skill for ArgoCD sync and app health.
- Use `argocd-cli` (`skill`) instead when the task is GitOps application sync, health, diff, or drift management.
- Do not use this skill for Terraform IaC.
- Use `terraform-cli` (`skill`) instead when the task is infrastructure provisioning, state, plans, modules, or provider locks.
- Do not use this skill for full platform deployment.
- Use `deploy-orchestration` (`skill`) instead when the task spans prerequisites, Terraform, Kubernetes, and platform-wide validation.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-deployment-operator` | `agent` | Coordinating approved Helm releases as part of platform deployment. |
| `backstage-expert` | `agent` | Managing Backstage chart values and portal deployment workflows. |
| `open-horizons-sre-investigator` | `agent` | Investigating release or rollout health issues. |
| `kubectl-cli` | `skill` | Inspecting Kubernetes resources created by Helm. |
| `argocd-cli` | `skill` | Managing GitOps applications that apply Helm-rendered workloads. |

## Quality gate

- [ ] `name` is `helm-cli` and matches the parent directory.
- [ ] `helm lint` is run or explicitly marked not applicable before deployment actions.
- [ ] Dry-run or template output is captured before applying chart changes when possible.
- [ ] Release, chart, namespace, and values file are included in the response when applicable.
- [ ] Rollback responses include the requested revision.
- [ ] Chart dependencies and versioning considerations are noted when they affect the command result.
