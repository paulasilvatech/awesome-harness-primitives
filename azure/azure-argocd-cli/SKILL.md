---
name: azure-argocd-cli
description: >-
  ArgoCD CLI operations manage GitOps installation, bootstrap, synchronization, drift detection, rollback checks, and day-2 application workflows. Use this skill when working with argocd login, app create, app sync, app health, ApplicationSet, ArgoCD troubleshooting, GitOps drift, or repository credential configuration.
---

# Azure ArgoCD CLI

Use this skill to turn ArgoCD GitOps requests into ordered CLI and Kubernetes actions, preserve the required project manifests, and return command results with sync, health, drift, and follow-up evidence.

## When to invoke

- "Install ArgoCD on an AKS cluster."
- "Bootstrap the app-of-apps pattern."
- "Manage ArgoCD applications and repository credentials."
- "Verify sync status, health, or GitOps drift."
- "Troubleshoot an ArgoCD application or controller issue."

## Prerequisites and context

- kubectl access to target cluster.
- Helm 3.12+ installed.
- ArgoCD CLI installed for day-2 operations.
- GitHub credentials for repository access.

## Procedure

1. Confirm the target cluster, namespace, ArgoCD server, repository, and application name before running mutating commands.
2. Read `references/commands.md` when the task needs installation, bootstrap, repository credentials, sync, health, troubleshooting, project file paths, or best practices.
3. Use the project files reference in `references/commands.md` to choose the manifest or values file that owns the requested workflow.
4. Run the narrowest relevant command sequence from `references/commands.md`.
5. Capture sync, health, drift, or log evidence after every install, bootstrap, sync, or troubleshooting action.
6. Return the result using the output template.

### Installation and bootstrap

Use `references/commands.md` for the preserved Helm, kubectl, and argocd commands to install ArgoCD, retrieve the initial admin password, configure repository credentials, bootstrap app-of-apps, and configure External Secrets integration.

### Day-2 operations

Use `references/commands.md` for the preserved authentication, application operations, health and status, and troubleshooting commands.

### Project files reference and best practices

Use `references/commands.md` for the preserved project file paths and operational best practices, including diff-before-sync, production-sensitive prune usage, health verification, projects, notifications, and sync waves.

## Output template

Return exactly this structure:

```markdown
**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the ArgoCD install, bootstrap, sync, health, drift, or troubleshooting outcome.

### Details
1. Command executed: `<argocd or kubectl or helm command>`
2. Application or component: `<app-name or argocd component>`
3. Sync status: `<Synced, OutOfSync, or not checked>`
4. Health status: `<Healthy, Progressing, Degraded, or not checked>`
5. Drift detected: `<yes, no, or not checked>`
6. Recommended actions: `<next ArgoCD action or none>`

### Validation
- Command result: `<exit code or observed CLI output>`
- Evidence: `<argocd app get, argocd app list, kubectl logs, kubectl events, or kubectl wait evidence>`
```

## Limits

- Do not use this skill for Helm package management.
- Use `azure-helm-cli` (`skill`) instead when the task is chart packaging, Helm values, repository management, release upgrades, or rollback operations outside ArgoCD control.
- Do not use this skill for kubectl cluster inspection.
- Use `azure-kubectl-cli` (`skill`) instead when the task is direct Kubernetes resource inspection or pod troubleshooting not tied to an ArgoCD app.
- Do not use this skill for full platform deployment orchestration.
- Use `open-horizons-deploy-orchestration` (`skill`) instead when the task spans prerequisites, Terraform, Kubernetes verification, and platform-wide rollout sequencing.

## Progressive disclosure and bundled resources

- `references/commands.md`: use when the task needs preserved ArgoCD installation, bootstrap, day-2, troubleshooting, project file, or best-practice command details.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-deployment-operator` | `agent` | Coordinating an approved end-to-end platform deployment that includes ArgoCD. |
| `open-horizons-sre-investigator` | `agent` | Investigating runtime incidents, degraded applications, or day-2 operational issues. |
| `azure-helm-cli` | `skill` | Managing Helm charts and releases that ArgoCD deploys. |
| `azure-kubectl-cli` | `skill` | Inspecting Kubernetes resources behind ArgoCD application health. |
| `open-horizons-deploy-orchestration` | `skill` | Sequencing ArgoCD with Terraform, validation, and other platform stages. |

## Quality gate

- [ ] `name` is `azure-argocd-cli` and matches the parent directory.
- [ ] The response includes the command executed and sync or health status when an application is involved.
- [ ] `argocd app diff <app-name>` evidence is captured before sync when drift or changes are in scope.
- [ ] Health is verified after sync, install, or bootstrap actions.
- [ ] Any use of `--prune` is explicitly called out as production-sensitive.
- [ ] Every referenced project path is preserved exactly in `references/commands.md`.
