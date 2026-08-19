---
name: argocd-cli
description: "Use when operating ArgoCD GitOps workflows for Open Horizons, including install, bootstrap, repository credentials, application sync, diff, health checks, and troubleshooting; produces commands, sync status, drift findings, and next actions. DO NOT USE FOR: Helm chart management (use helm-cli), Kubernetes operations (use kubectl-cli), or full platform deployment orchestration (use deploy-orchestration). Triggers include \"sync an ArgoCD app\", \"bootstrap ArgoCD\", \"troubleshoot ArgoCD drift\"."
---

# ArgoCD CLI

This workflow performs focused ArgoCD operations for Open Horizons GitOps. It produces safe command sequences, app health and sync evidence, and remediation steps while keeping full environment deployment in `deploy-orchestration`.

> [!NOTE]
> This skill shells out to `argocd`, `kubectl`, and sometimes `helm`. The cluster context must already target the intended AKS or local cluster, and Git credentials must be available for private repositories.

## When to invoke
- "Sync the Backstage ArgoCD application and show the drift first."
- "Bootstrap ArgoCD app-of-apps for Open Horizons."
- "Troubleshoot why an ArgoCD app is OutOfSync."
- "Configure ArgoCD repository credentials for this repo."

## Prerequisites and context
- `kubectl config current-context` points to the target cluster.
- ArgoCD namespace and CLI access are available, or Helm is installed for first-time install.
- Repository manifests exist under `argocd/apps/`, `argocd/app-of-apps/root-application.yaml`, and `argocd/sync-policies.yaml`.
- Helm values exist at `deploy/helm/argocd/values.yaml` if installing ArgoCD.
- Approval is available before sync, prune, force, or credential changes.

## Procedure

### Step 1: Verify cluster and ArgoCD access
```bash
kubectl config current-context
kubectl get ns argocd
argocd version --client
argocd app list
```

- [ ] The cluster is the intended environment.
- [ ] The ArgoCD CLI is logged in to the expected server.
- [ ] App names match manifests under `argocd/apps/`.

### Step 2: Install or bootstrap only when requested
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd
helm install argocd argo/argo-cd --namespace argocd --values deploy/helm/argocd/values.yaml --wait --timeout 10m
kubectl apply -f argocd/app-of-apps/root-application.yaml
kubectl apply -f argocd/sync-policies.yaml
```

Use repository credentials only from approved secret management paths:

```bash
kubectl apply -f argocd/repo-credentials.yaml
```

### Step 3: Inspect before mutating
```bash
argocd app get <app-name>
argocd app diff <app-name>
argocd app resources <app-name>
```

- [ ] Diff is reviewed before every sync.
- [ ] Prune and force risks are identified.
- [ ] External Secrets and Gatekeeper dependencies are healthy when relevant.

### Step 4: Confirm sync or bootstrap actions
```text
ArgoCD operation summary:
- Cluster context:
- Application or manifest:
- Operation: sync | prune | force | bootstrap | credential update
- Expected resource changes:
Proceed with the ArgoCD mutation? (y/n)
```

> [!IMPORTANT]
> Only proceed with sync, prune, force, bootstrap, install, or credential changes if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the diff and stop.

### Step 5: Execute and verify
```bash
argocd app sync <app-name>
argocd app get <app-name>
argocd app resources <app-name>
kubectl get events -n argocd --sort-by='.lastTimestamp'
```

Use `--prune` or `--force` only when explicitly approved and after documenting the resources affected.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Sync or prune would delete production resources, replace secrets, or target the wrong cluster. |
| High | App is degraded, repo credentials fail, or force sync is requested without resource-level evidence. |
| Medium | OutOfSync drift exists but health is stable, or dependencies are not ready. |
| Low | Cosmetic diff, stale cache, or missing labels/annotations. |

## Limits

- Do not use this skill for: Helm chart management (use helm-cli), Kubernetes operations (use kubectl-cli), or full platform deployment orchestration (use deploy-orchestration).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Not logged in to ArgoCD | Use `argocd login <server>` and verify context before any app operation. |
| App not found | Check manifests under `argocd/apps/` and the app-of-apps root before creating anything. |
| Diff command fails | Stop and report auth, repo, or cluster errors; do not sync blindly. |
| Sync fails | Collect `argocd app get`, `argocd app resources`, controller logs, and recent events. |

## Output template

Return exactly this structure:
```markdown
# ArgoCD Operation Report

## Scope
- Cluster context:
- ArgoCD server:
- Application:

## Preflight
| Check | Result |
|---|---|

## Diff Summary
```text
<paste summarized diff>
```

## Result
| Command | Outcome |
|---|---|

## Next Actions
- 
```

## Quality gate
- [ ] Cluster and ArgoCD contexts are verified before mutation.
- [ ] `argocd app diff` is reviewed before sync.
- [ ] Explicit confirmation is captured before install, sync, prune, force, or credential changes.
- [ ] Final app health and sync status are reported.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
