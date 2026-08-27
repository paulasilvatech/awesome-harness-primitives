---
name: kubernetes
description: Use when editing tracked AKS, Kubernetes, Helm, Kustomize, or generated GitOps manifests.
paths:
  - backstage/k8s/*.yaml
  - deploy/helm/**/*.yaml
  - docs/aeg-feature-scaffold/integration/open-horizons/examples/k8s/*.yaml
  - scripts/golden-paths/**/deploy/*.yaml
  - scripts/golden-paths/**/base/*.yaml
  - scripts/golden-paths/**/overlays/**/*.yaml
  - scripts/golden-paths/**/argocd-app.yaml
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/kubernetes.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Kubernetes and Helm

## Conventions

- Use explicit versioned image tags; never use `latest`.
- Apply standard `app.kubernetes.io/*` labels consistently to workloads, services, selectors, monitoring, and policy targets.
- Set realistic resource requests and limits plus startup, readiness, and liveness probes that match the service contract.
- Run as non-root, disallow privilege escalation, drop capabilities, use `RuntimeDefault` seccomp, and prefer a read-only root filesystem.
- Use dedicated service accounts, namespace-scoped RBAC, Workload Identity, and least-privilege network policies.
- Reference secrets through External Secrets or approved Key Vault integration; never commit a Kubernetes Secret value.
- Keep namespaces, selectors, ports, service names, and Helm value keys consistent across related manifests.
- Keep generated GitOps examples under `scripts/golden-paths/`; no root `argocd/` path is assumed.
- Preserve rollout safety with disruption budgets, topology constraints, and graceful termination where availability requires them.

## Verification

- YAML, Helm, and Kustomize rendering produce valid resources with no unresolved tokens.
- Policy checks cover tags, resources, non-root execution, privilege, and registry restrictions.
- Rendered workloads have immutable images, probes, resources, identity, and secret references.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Render manifests and enforce identity, resources, probes, and policy controls. | Apply unrendered files or weaken controls to make a deployment pass. |
| Use immutable images and external secret references. | Use floating tags or commit secret values. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] YAML, Helm, and Kustomize rendering pass without unresolved tokens.
- [ ] Policy checks cover identity, privilege, network, resources, and registry rules.
- [ ] Workloads use immutable images, probes, and external secret references.
- [ ] No unrelated edits or unresolved placeholders remain.
