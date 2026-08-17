---
applyTo: "k8s/**/*.yaml,k8s/**/*.yml,manifests/**/*.yaml,manifests/**/*.yml,deploy/**/*.yaml,deploy/**/*.yml,charts/**/templates/**/*.yaml,charts/**/templates/**/*.yml"
description: "Enforces Kubernetes manifest conventions for labels, annotations, security contexts, pod security, resources, probes, rollout strategy, HA, validation, and secrets."
---

# Kubernetes Manifest Conventions — Secure Reliable YAML

These instructions apply to Kubernetes YAML manifests and Helm chart templates under the matched paths. They are authoritative for labels, annotations, pod security, security contexts, resource requests and limits, probes, rollout strategy, high availability, validation commands, rollback, secrets, and NetworkPolicy conventions; environment-specific platform, cluster, and deployment primitives win when they define stricter namespace, policy, or admission requirements.

## Labels and Annotations

Apply Kubernetes recommended labels to every workload and related resource: `app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/version`, `app.kubernetes.io/component`, `app.kubernetes.io/part-of`, and `app.kubernetes.io/managed-by`. Add operational labels such as `environment`, `team`, and `cost-center` when the organization uses them. Use annotations for documentation, ownership, monitoring, and change tracking. Prometheus annotations include `prometheus.io/scrape`, `prometheus.io/port`, and `prometheus.io/path`.

## Security Contexts and Pod Security

Use Pod Security Admission at the namespace level. Prefer Restricted for production and Baseline only when Restricted is not yet compatible. Pod-level security context should set `runAsNonRoot: true`, explicit `runAsUser`, explicit `runAsGroup`, `fsGroup` where filesystem ownership needs it, and `seccompProfile.type: RuntimeDefault`. Container-level security context should set `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true` with tmpfs or writable mounts for required paths, and `capabilities.drop: [ALL]`, adding back only the capabilities actually required.

## Resources, Probes, and Images

Define CPU and memory requests and limits for every production container. Requests provide scheduling guarantees; limits prevent exhaustion. Choose QoS intentionally: Guaranteed when requests equal limits for critical apps, Burstable when requests are lower than limits, and avoid BestEffort in production. Configure liveness probes to restart unhealthy containers, readiness probes to control routing, and startup probes for slow-starting applications. Tune delays, periods, timeouts, and thresholds to the application. Pin images to specific tags or digests; never use `:latest`.

## Rollout, High Availability, and Shutdown

Use `RollingUpdate` for Deployments with explicit `maxSurge` and `maxUnavailable`; set `maxUnavailable: 0` when zero downtime is required. Run at least 2-3 replicas for production services. Add a Pod Disruption Budget (PDB), anti-affinity rules to spread pods across nodes or zones, and a Horizontal Pod Autoscaler (HPA) for variable load. Set `terminationGracePeriodSeconds` and implement graceful shutdown so in-flight requests can finish.

## Secrets, Config, and Network Boundaries

Store sensitive values in Kubernetes Secrets, not ConfigMaps. Use ConfigMaps for non-sensitive configuration. Add least-privilege NetworkPolicy when the cluster enforces network policy, and keep ingress/egress rules as narrow as the workload permits.

## Validation and Operations Commands

Validate manifests before deployment:

```bash
kubectl apply --dry-run=client -f manifest.yaml
kubectl apply --dry-run=server -f manifest.yaml
kubeconform -strict manifest.yaml
helm template ./chart | kubeconform -strict
```

Use OPA Conftest, Kyverno, or Datree for policy validation when available. Deploy and operate with `kubectl apply -f manifest.yaml`, `kubectl rollout status deployment/NAME`, `kubectl rollout undo deployment/NAME`, `kubectl rollout undo deployment/NAME --to-revision=N`, `kubectl rollout history deployment/NAME`, and `kubectl rollout restart deployment/NAME`.

## Technical Vocabulary

Preserve these source terms when they apply to edits in this domain: `helm template ./chart | kubeconform -strict` `kubeconform -strict manifest.yaml` `kubectl apply --dry-run=client -f manifest.yaml` `kubectl apply --dry-run=server -f manifest.yaml` `nodes/zones` `production-ready` `surge/unavailable` `zero-downtime`.

Use `SecurityContext` settings consistently at pod and container scope.

## Good / Bad Examples

The examples below show secure container defaults.

**Good:**

```yaml
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: [ALL]
```

Why: The container blocks privilege escalation, avoids writable root filesystem assumptions, and drops Linux capabilities by default.

**Bad:**

```yaml
image: example/app:latest
resources: {}
```

Why: The image is not reproducible and the pod can be unschedulable or noisy without resource requests and limits.

## Conventions

| Rule | Rationale |
|---|---|
| Apply standard `app.kubernetes.io/*` labels and ownership annotations | Operators and tools can discover, group, and monitor resources consistently |
| Use Restricted-compatible security contexts by default | Least privilege reduces container escape and host impact risk |
| Define requests, limits, and intentional QoS | Scheduling and resource isolation need explicit constraints |
| Configure liveness, readiness, and startup probes | Kubernetes needs separate signals for restart, routing, and slow startup |
| Pin images and avoid `:latest` | Deployments stay reproducible and rollbacks are possible |
| Use PDB, anti-affinity, HPA, replicas, and graceful shutdown for production | Availability survives node disruption, rollout, and load variation |
| Validate with dry-run, schema, and policy tools | Invalid or non-compliant manifests fail before cluster mutation |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `runAsNonRoot`, `RuntimeDefault`, dropped capabilities, and read-only root filesystems | Run privileged containers by default |
| Put secrets in Secret resources | Put credentials in ConfigMaps or plain annotations |
| Set `maxUnavailable: 0` where zero downtime is required | Accept avoidable outage during rolling updates |
| Use `kubectl apply --dry-run=server` and `kubeconform -strict` | Apply unvalidated YAML directly to production |
| Use HPA for variable load | Hardcode a single replica count for changing traffic |
| Add NetworkPolicy for least-privilege traffic | Leave every pod open to every other pod when policy is supported |

## Checklist Before Opening a PR

- [ ] Standard labels, ownership annotations, monitoring annotations, and change-tracking metadata are present.
- [ ] Pod and container security contexts include non-root, seccomp, no privilege escalation, dropped capabilities, and read-only root filesystem where possible.
- [ ] Requests, limits, QoS choice, image tags, and secrets/config separation are explicit.
- [ ] Liveness, readiness, and startup probes have tuned delays, periods, timeouts, and thresholds.
- [ ] RollingUpdate, replicas, PDB, anti-affinity, HPA, and graceful shutdown settings match production availability needs.
- [ ] NetworkPolicy is least-privilege where supported.
- [ ] `kubectl apply --dry-run=client`, `kubectl apply --dry-run=server`, `kubeconform -strict`, Helm rendering, and policy validation pass where applicable.
- [ ] Rollout, rollback, history, and restart commands remain documented for the changed deployment.
