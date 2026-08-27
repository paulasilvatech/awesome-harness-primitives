---
name: azure-kubectl-cli
description: >-
  kubectl CLI operations inspect and manage AKS and Kubernetes resources directly, including
  health checks, manifests, rollout status, logs, events, namespaces, pod troubleshooting, service
  debugging, secrets inspection by name, and network policy validation. Use this skill when
  working with kubectl get, describe, logs, apply, diff, exec, top, or rollout workflows.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/azure-kubectl-cli/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure kubectl CLI

Use this skill to turn Kubernetes operations requests into ordered `kubectl` workflows, verify context and namespace safety, and return resource status, log, event, diff, apply, or troubleshooting evidence.

## When to invoke

- "Check cluster health or node status with kubectl."
- "Apply, diff, or inspect Kubernetes manifests."
- "Troubleshoot pods with describe, logs, events, or exec."
- "Inspect services, deployments, namespaces, or resource usage."
- "Validate network policy or secret references by name."

## Prerequisites and context

- kubectl installed and configured.
- KUBECONFIG set to valid config.
- kubelogin for Azure AD authentication.
- Appropriate RBAC permissions.

## Procedure

1. Confirm the Kubernetes context and namespace before resource operations.
2. Use dry-run or diff before applying manifests when changes are in scope.
3. Run the narrowest cluster health, resource management, troubleshooting, or query command that satisfies the request.
4. Capture status, warning, error, log, event, or usage evidence.
5. Return the result using the output template.

### Cluster health

```bash
# Cluster info
kubectl cluster-info

# Node status
kubectl get nodes -o wide

# System pods
kubectl get pods -n kube-system

# Unhealthy pods across all namespaces
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
```

### Resource management

```bash
# Dry-run before apply
kubectl apply -f manifest.yaml --dry-run=client -o yaml

# Diff changes
kubectl diff -f manifest.yaml

# Apply with recording
kubectl apply -f manifest.yaml --record

# Delete with grace
kubectl delete -f manifest.yaml --grace-period=30
```

### Troubleshooting

```bash
# Describe pod
kubectl describe pod <pod-name> -n <namespace>

# Pod logs (current)
kubectl logs -f <pod-name> -n <namespace>

# Pod logs (previous crash)
kubectl logs <pod-name> -n <namespace> --previous

# Events by time
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Exec into pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
```

### Resource queries

```bash
# Get all resources in namespace
kubectl get all -n <namespace> -o wide

# Get resource as YAML
kubectl get deployment <name> -n <namespace> -o yaml

# Resource usage
kubectl top pods -n <namespace>
kubectl top nodes
```

### Best practices

1. ALWAYS use --dry-run=client before apply.
2. ALWAYS specify namespace with -n.
3. Use labels for selection: -l app=myapp.
4. Check events when pods fail.
5. Use kubectl diff for change preview.
6. NEVER delete without explicit namespace.

## Output template

Return exactly this structure:

```markdown
**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the Kubernetes health, apply, diff, log, event, query, or troubleshooting outcome.

### Details
1. Command executed: `<kubectl command>`
2. Context and namespace: `<current context and namespace>`
3. Resource status summary: `<pods, nodes, deployment, service, event, or manifest status>`
4. Warnings or errors: `<kubectl warnings, RBAC errors, unhealthy resources, or none>`
5. Recommended actions: `<next kubectl action or none>`

### Validation
- Change preview: `<dry-run, diff, or reason not checked>`
- Command result: `<exit code or observed kubectl output>`
```

## Limits

- Do not use this skill for Helm chart management.
- Use `helm-cli` (`skill`) instead when the task is chart repositories, values, template rendering, release upgrades, or rollbacks.
- Do not use this skill for ArgoCD GitOps sync.
- Use `argocd-cli` (`skill`) instead when the task is GitOps app sync, health, diff, drift, or repository credential workflows.
- Do not use this skill for Azure resource provisioning.
- Use `azure-cli` (`skill`) or `terraform-cli` (`skill`) instead when the task is Azure resource provisioning, resource group management, or infrastructure state.
- Do not use this skill for full deployment orchestration.
- Use `deploy-orchestration` (`skill`) instead when the task spans prerequisites, Terraform, Kubernetes verification, and platform rollout sequencing.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-deployment-operator` | `agent` | Coordinating approved Kubernetes operations as part of an end-to-end deployment. |
| `backstage-expert` | `agent` | Validating Backstage workloads and portal runtime behavior on Kubernetes. |
| `open-horizons-sre-investigator` | `agent` | Troubleshooting pods, services, events, or resource saturation. |
| `helm-cli` | `skill` | Managing Helm releases that create Kubernetes resources. |
| `argocd-cli` | `skill` | Managing GitOps applications that own Kubernetes resources. |
| `azure-cli` | `skill` | Acquiring AKS credentials before kubectl operations. |

## Quality gate

- [ ] `name` is `kubectl-cli` and matches the parent directory.
- [ ] Context and namespace are confirmed or explicitly reported as unknown.
- [ ] `--dry-run=client` or `kubectl diff` is used before apply when manifest changes are in scope.
- [ ] Delete operations include an explicit namespace and grace period when applicable.
- [ ] Troubleshooting responses include describe, logs, events, or resource status evidence as appropriate.
- [ ] Secret handling is limited to names unless a safe explicit value retrieval is required.
