---
applyTo: "deploy/**/*.yaml,argocd/**/*.yaml,backstage/k8s/*.yaml,backstage/k8s/templates/*.yaml.tmpl,**/kubernetes/**,**/k8s/**,**/helm/**"
description: "Use when editing Kubernetes, Helm, Kustomize, ArgoCD, and AKS deployment manifests for Open Horizons."
---

# Kubernetes Conventions — AKS Manifests, Helm Values, and ArgoCD Apps

This file activates when you edit manifests under `backstage/k8s/`, `deploy/`, `argocd/`, `kubernetes/`, `k8s/`, or `helm/`. It teaches Open Horizons conventions for AKS workloads, ArgoCD applications, Helm values, labels, probes, resources, security contexts, service accounts, RBAC, and network policies. It does **not** cover Azure infrastructure provisioning, which belongs to the `terraform` instructions, image construction, which belongs to the `dockerfile` instructions, local-only Compose services, which belong to the `docker-compose` instructions, shell manifest rendering scripts, which belong to the `shell` instructions, or application code, which belongs to the `python` instructions and the `typescript` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: "deploy/**/*.yaml,argocd/**/*.yaml,backstage/k8s/*.yaml,backstage/k8s/templates/*.yaml.tmpl,**/kubernetes/**,**/k8s/**,**/helm/**"` for existing local patterns.
2. This `kubernetes` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for kubernetes conventions — aks manifests, helm values, and argocd apps. Use the `kubectl-cli` skill for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!IMPORTANT]
> Kubernetes manifests are the production runtime contract for Open Horizons on AKS. Keep security, resources, identity, probes, and labels explicit.

## Metadata and Labels

Use standard Kubernetes labels consistently. Existing agent identity manifests label name, instance, version, component, part-of, and managed-by.

```yaml
# Wrong: missing standard labels used by selectors, dashboards, and policies.
metadata:
  name: agent-api-chat
  labels:
    app: chat
```

```yaml
metadata:
  name: agent-api-chat
  namespace: ai-services
  labels:
    app.kubernetes.io/name: agent-api-chat
    app.kubernetes.io/instance: open-horizons
    app.kubernetes.io/version: "2.0.0"
    app.kubernetes.io/component: ai-agent
    app.kubernetes.io/part-of: open-horizons
    app.kubernetes.io/managed-by: argocd
```

## Images and Tags

Use pinned image tags from the release cadence. Do not use `latest`; the MCP ecosystem and Foundry-related services may use their own tag variable separate from the Backstage image tag.

```yaml
# Wrong: mutable deployment image.
image: ghcr.io/ohorizons/ohorizons-agent-api:latest
```

```yaml
image: __AGENT_API_IMAGE__:__IMAGE_TAG__
imagePullPolicy: IfNotPresent
```

> [!WARNING]
> Never commit Kubernetes Secret values. Use External Secrets Operator, Key Vault integration, or secret references rendered from approved templates.

## Workload Security

Run containers as non-root, disable privilege escalation, drop capabilities, and use `RuntimeDefault` seccomp. Service accounts must be dedicated per workload or per agent role.

```yaml
# Wrong: root-capable pod with the default service account.
spec:
  containers:
    - name: agent-api
      securityContext:
        privileged: true
```

```yaml
spec:
  serviceAccountName: agent-api-chat
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: agent-api
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

## Resources and Probes

Every long-running workload needs requests, limits, liveness probes, and readiness probes. Align probe paths with the service contract, such as FastAPI `/health` or Backstage readiness paths.

```yaml
# Wrong: scheduler and rollout controller have no signal.
containers:
  - name: agent-api
    image: ghcr.io/ohorizons/ohorizons-agent-api:v7.2.6
```

```yaml
containers:
  - name: agent-api
    image: ghcr.io/ohorizons/ohorizons-agent-api:v7.2.6
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 512Mi
    livenessProbe:
      httpGet:
        path: /health
        port: http
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /health
        port: http
      periodSeconds: 5
```

> [!NOTE]
> Use startup probes for services with intentionally slow boot, rather than inflating liveness probe delays for every rollout.

## RBAC and Network Policies

Use dedicated ServiceAccounts, scoped Roles, and RoleBindings. NetworkPolicies should express required traffic, as the agent API policy allows Backstage ingress and controlled DNS/HTTPS egress.

```yaml
# Wrong: cluster-wide admin for a namespace-local agent.
kind: ClusterRoleBinding
roleRef:
  kind: ClusterRole
  name: cluster-admin
```

```yaml
kind: Role
metadata:
  name: agent-read
  namespace: ai-services
rules:
  - apiGroups: [""]
    resources: ["configmaps", "services", "endpoints"]
    verbs: ["get", "list", "watch"]
```

## ArgoCD and Helm Values

Keep ArgoCD applications declarative and point them at repository paths that exist. Helm values should override configuration, resources, ingress, service monitors, and secrets references without replacing upstream charts wholesale.

```yaml
# Wrong: destination namespace is ambiguous and path is not in this repo.
source:
  path: manifests
```

```yaml
source:
  repoURL: https://github.com/ohorizons/open-horizons-platform
  path: foundry/k8s
  targetRevision: HEAD
destination:
  namespace: ai-services
```

## Conventions

| Rule | Rationale |
|---|---|
| Use `app.kubernetes.io/*` labels on every resource | ArgoCD, selectors, dashboards, and policies need consistent metadata. |
| Pin image tags and use template variables where render scripts substitute versions | Releases must be reproducible and avoid mutable `latest`. |
| Configure requests and limits for every container | AKS scheduling, cost, and reliability depend on explicit resources. |
| Configure liveness and readiness probes for long-running workloads | Rollouts and services need accurate health signals. |
| Run as non-root, drop capabilities, and disable privilege escalation | Meets platform security baseline and reduces container escape risk. |
| Use dedicated ServiceAccounts, scoped RBAC, and NetworkPolicies | Agent identity and least privilege require per-workload boundaries. |
| Keep secrets out of Git and reference External Secrets or Key Vault-backed mechanisms | Secret material belongs in managed stores, not manifests. |

## Do / Do Not

| Do | Do not |
|---|---|
| Add or preserve `app.kubernetes.io/name`, `component`, `part-of`, and `managed-by` | Use only ad-hoc `app:` labels. |
| Use namespace-scoped Role/RoleBinding when cluster scope is not required | Bind agents to `cluster-admin`. |
| Put operational differences in overlays or Helm values | Fork upstream charts unnecessarily. |
| Validate rendered templates with repository scripts | Edit generated manifests and forget the template. |

## Checklist Before Opening a PR

- [ ] Every workload has labels, requests, limits, probes, and a non-root security context.
- [ ] Images are pinned to approved tags or template variables, never `latest`.
- [ ] ServiceAccounts, RBAC, and NetworkPolicies are least-privilege.
- [ ] Secrets are referenced, not committed.
- [ ] ArgoCD paths and Helm values reference files that exist in the repo.
- [ ] Template changes have been rendered or validated with the existing scripts.
