---
name: kubectl-cli
description: 'Use when operating Kubernetes resources on AKS or kind with kubectl: get, describe, logs, events, diff, dry-run, apply, delete, rollout, and namespace troubleshooting. Produces command plans, cluster evidence, health summaries, and remediation steps. DO NOT USE FOR: Helm charts (use helm-cli), ArgoCD sync (use argocd-cli), Azure resource provisioning (use azure-cli). Triggers include "check pod health", "apply these Kubernetes manifests", "delete this resource", and "debug the Backstage deployment".'
---

# Kubectl CLI

Use this skill for direct Kubernetes inspection and carefully approved resource changes in Open Horizons namespaces and manifests such as `backstage/k8s/`, `argocd/apps/`, and `foundry/k8s/`. It produces cluster evidence, a risk-ranked action plan, and post-change verification.

> [!NOTE]
> This skill depends on `kubectl`, a valid `KUBECONFIG`, `kubelogin` for Azure AKS authentication when applicable, and RBAC permissions for the target namespace. It does not use an MCP server by default.

## When to invoke

- "Check whether Backstage pods are healthy."
- "Apply the manifests under backstage/k8s."
- "Delete a failed Kubernetes job after confirming the namespace."
- "Show events for the monitoring namespace."
- "Debug image pull errors in the ai-services namespace."

## Prerequisites and context

- `kubectl version --client` succeeds.
- `kubectl config current-context` shows the intended AKS or kind cluster.
- The namespace is explicit for namespace-scoped resources.
- Manifest paths exist, for example `backstage/k8s/agent-identity.yaml`.
- The user has approved any apply, delete, scale, patch, or rollout restart action.

## Procedure

### Step 1: Confirm context and namespace

```bash
kubectl config current-context
kubectl get namespaces
kubectl get nodes -o wide
```

Never assume the namespace. If the user did not provide one, inspect likely Open Horizons namespaces and ask for confirmation before mutation.

### Step 2: Inspect current resource health

```bash
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
kubectl get pods -n backstage -o wide
kubectl get events -n backstage --sort-by='.lastTimestamp'
kubectl describe deployment -n backstage backstage
```

Use logs only for the named pod or label selector.

```bash
kubectl logs -n backstage deployment/backstage --tail=100
kubectl logs -n ai-services deployment/agent-api --tail=100
```

### Step 3: Validate manifests before mutation

```bash
kubectl apply -f backstage/k8s/ --dry-run=client -o yaml
kubectl diff -f backstage/k8s/
```

For generated manifests, render them first with the repo script and then inspect the output path produced by the script.

```bash
./scripts/render-k8s.sh
```

### Step 4: Classify Kubernetes risk

| Risk | Meaning |
| --- | --- |
| High | `delete`, `patch`, `scale`, `rollout restart`, namespace changes, or apply to production. |
| Medium | `apply` to non-production, changes to RBAC, NetworkPolicy, ServiceAccount, or ingress. |
| Low | `get`, `describe`, `logs`, `events`, `top`, `diff`, or client dry-run. |

### Step 5: User confirmation gate

```text
Kubernetes action: <apply|delete|patch|scale|rollout restart>
Cluster context: <context>
Namespace: <namespace>
Manifest or resource: <path-or-kind/name>
Risk: <High|Medium|Low>
Proceed with the Kubernetes mutation? (y/n)
```

> [!IMPORTANT]
> Only run mutating `kubectl` commands after an explicit affirmative response. On a negative, ambiguous, or missing response, do not mutate the cluster; output the dry-run or diff findings and stop.

### Step 6: Execute the approved action

```bash
kubectl apply -f backstage/k8s/ --server-side
kubectl rollout status deployment/backstage -n backstage --timeout=300s
```

For deletion, use an exact resource identity and namespace.

```bash
kubectl delete <kind>/<name> -n <namespace> --grace-period=30
```

### Step 7: Verify after mutation

```bash
kubectl get all -n backstage -o wide
kubectl get events -n backstage --sort-by='.lastTimestamp'
kubectl rollout status deployment/backstage -n backstage --timeout=300s
```

## Limits

- Do not use this skill for: Helm charts (use helm-cli), ArgoCD sync (use argocd-cli), Azure resource provisioning (use azure-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| No current context | Stop and ask the operator to configure AKS credentials. |
| Namespace not found | List namespaces and require explicit namespace selection before mutation. |
| Dry-run or diff fails | Report validation errors and skip mutation. |
| RBAC forbidden | Report required verb, resource, and namespace from the error. |
| Pods crash after apply | Collect `describe`, previous logs, and events; do not auto-delete resources. |

## Output template

Return exactly this structure:

```markdown
## Kubectl Operation Report

**Cluster context:** <context>
**Namespace:** <namespace>
**Action:** <get|describe|logs|diff|apply|delete>
**Risk:** <High|Medium|Low>

### Evidence
- Pods: <summary>
- Events: <summary>
- Rollout: <summary>

### Commands Run
- `<command>`

### Findings
- <finding>

### Next Steps
1. <next step>
```

## Quality gate

- [ ] Confirmed current Kubernetes context.
- [ ] Used explicit namespace for namespace-scoped resources.
- [ ] Verified manifest paths exist before referencing them.
- [ ] Ran dry-run or diff before apply.
- [ ] Received explicit approval before any mutating command.
- [ ] Verified rollout, pods, and events after mutation.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
