---
applyTo: "**/*.yaml,**/*.yml"
description: "Enforces Kubernetes manifest conventions for Pods, Deployments, Services, Ingress, configuration, health checks, resources, scaling, security, observability, rollout strategy, and troubleshooting."
---

# Kubernetes Deployment Conventions — Reliable Manifests

These instructions apply to Kubernetes YAML manifests and workload configuration. They are authoritative for production-ready manifest shape, workload controllers, service exposure, configuration, probes, resource controls, scaling, security context, observability, deployment strategy, and operational troubleshooting; platform-specific cluster policy, admission controls, and environment runbooks win when they impose stricter requirements.

## Workload Controllers and Pod Design

Do not deploy standalone Pods for application workloads. Use higher-level controllers that preserve availability and rollout behavior.

| Resource | Convention | Rationale |
| --- | --- | --- |
| `Pod` | Run one primary container, plus only tightly coupled sidecars; define `resources`, `livenessProbe`, and `readinessProbe`. | Pods are the smallest deployable unit and need health and resource boundaries. |
| `Deployment` | Use for stateless applications; set `replicas`, `selector`, `template`, and `strategy.rollingUpdate.maxSurge` / `maxUnavailable`. | Deployments provide rolling updates and rollbacks. |
| `StatefulSet` | Use for workloads that require stable identity or ordered storage semantics. | Stateful applications need guarantees a Deployment does not provide. |
| Labels and selectors | Keep `metadata.labels`, `spec.selector.matchLabels`, and Pod template labels consistent. | Services and controllers route and manage Pods through labels. |

## Services, Ingress, and Traffic

Expose workloads with explicit network resources.

- Use `ClusterIP` for internal services, `LoadBalancer` for cloud internet-facing applications, and `NodePort` only when the platform design requires it.
- Use `ExternalName` only for DNS-style external service aliases.
- Ensure each Service `selector` matches Pod labels exactly.
- Use `Ingress` for HTTP/HTTPS routing, host/path rules, backend service references, and TLS termination through `tls.secretName`.
- Configure Ingress controller behavior deliberately when using blue/green or canary traffic splitting.

## Configuration, Secrets, and External Secret Managers

Separate non-sensitive configuration from secrets.

| Data type | Convention |
| --- | --- |
| `ConfigMap` | Store non-sensitive key-value configuration, environment variables, command-line arguments, or mounted files; do not store credentials. |
| `Secret` | Store API keys, passwords, database credentials, and TLS certificates; prefer volume mounts over environment variables for sensitive values. |
| External secret managers | Use HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or an External Secrets Operator for production secret lifecycle. |
| etcd | Enable encryption at rest where cluster policy allows it. |

## Health Checks and Probes

Define probes for every long-running container.

| Probe | Use | Key fields |
| --- | --- | --- |
| `livenessProbe` | Detect a stuck or dead container and restart it. | `httpGet`, `tcpSocket`, or `exec`; `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`, `successThreshold`. |
| `readinessProbe` | Remove a Pod from Service endpoints until it can serve traffic. | Use startup and dependency checks that reflect real serving readiness. |
| Startup behavior | Give slow applications realistic initial delays or use startup probes when available. | Prevents premature restarts during normal startup. |

## Resource Management and Scaling

Set resource boundaries before relying on scheduling or autoscaling.

- Define CPU and memory `requests` and `limits` for every container to avoid `BestEffort` workloads and noisy-neighbor failures.
- Understand Kubernetes QoS classes: `Guaranteed`, `Burstable`, and `BestEffort`.
- Use Horizontal Pod Autoscaler (`HPA`) for stateless applications with fluctuating load; set `minReplicas`, `maxReplicas`, and `targetCPUUtilizationPercentage` or custom metrics.
- Use Vertical Pod Autoscaler (`VPA`) to recommend or adjust CPU and memory requests over time.
- Use `nodeSelector`, tolerations, and affinity only when scheduling requirements are intentional and documented.

## Security Controls

Apply least privilege at workload, network, and API boundaries.

| Control | Convention |
| --- | --- |
| Network policies | Use deny-by-default `NetworkPolicies` and allow only required Pod-to-Pod or Pod-to-external traffic. |
| RBAC | Define granular `Roles`, `ClusterRoles`, `RoleBindings`, and `ClusterRoleBindings` for `ServiceAccounts`, users, or groups. |
| Pod security context | Set `runAsNonRoot: true`, non-root `runAsUser`, appropriate `fsGroup`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true` where possible, and `capabilities.drop: [ALL]`. |
| Image security | Use trusted minimal images such as distroless or alpine, avoid `:latest`, scan with Trivy, Clair, or Snyk, and use image signing and verification where available. |
| API server | Use strong authentication such as client certificates or OIDC, enforce RBAC, and enable API auditing. |

## Observability and Operations

Make workloads observable through standard Kubernetes and platform tools.

- Write application logs to `STDOUT` and `STDERR` for centralized collection.
- Deploy logging agents such as Fluentd, Logstash, or Loki to ELK Stack, Splunk, Datadog, or the platform logging backend.
- Collect metrics with Prometheus, `kube-state-metrics`, `node-exporter`, application exporters, and Grafana dashboards.
- Configure Prometheus Alertmanager rules for high error rates, low resource availability, Pod restarts, and unhealthy probes.
- Use OpenTelemetry, Jaeger, or Zipkin for distributed tracing across services.

## Rollouts, Rollbacks, and Troubleshooting

Prefer predictable rollout strategies with explicit rollback paths.

| Scenario | Convention |
| --- | --- |
| Rolling update | Use Deployment rolling updates with `maxSurge` and `maxUnavailable`; this is the default minimal-downtime strategy. |
| Blue/green | Run two identical environments and switch traffic through an external load balancer or Ingress controller feature. |
| Canary | Use a service mesh such as Istio or Linkerd, or an Ingress controller with traffic splitting, to expose a subset of users first. |
| Rollback | Keep previous image versions available and use `kubectl rollout undo` for Deployments. |
| Pending or `CrashLoopBackOff` Pods | Check `kubectl describe pod <pod_name>`, `kubectl logs <pod_name> -c <container_name>`, resources, image pull errors, and mounted ConfigMaps or Secrets. |
| Service unavailable | Check `readinessProbe`, container listen ports, and `kubectl describe service <service_name>` endpoints. |
| OOMKilled | Increase `memory.limits`, optimize memory, and review VPA recommendations. |
| Performance issues | Use `kubectl top pod`, Prometheus, logs, traces, and database metrics. |

## Good / Bad Examples

The examples below illustrate a secure container baseline.

**Good:**

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
```

Why: The container avoids root, privilege escalation, writable root filesystem assumptions, and Linux capabilities it does not need.

**Bad:**

```yaml
containers:
  - name: app
    image: my-repo/my-app:latest
```

Why: The workload has no security context, resource controls, probes, or immutable image version.

## Manifest Vocabulary and Review Terms

Retain these Kubernetes review terms because they identify schema fields, examples, or operating modes: `apps/v1`, `networking.k8s.io/v1`, `my-app-deployment`, `my-app-container`, `my-app-service`, `my-app-ingress`, `my-app-tls-secret`, `labels`, `selectors`, `type`, `strategy`, `rollingUpdate`, `ImagePullPolicy`, `requests/limits`, `CPU/memory`, `ConfigMaps/Secrets`, `capabilities`, `capabilities: drop: [ALL]`, `command-based`, `tolerations`, `users/groups`, `application-specific`, `rule-based`, `fine-grained`, `end-to-end`, `zero-downtime`, `cloud-native`, `Blue/Green`, `Vertical Pod Autoscaler`, and `Jaeger/Zipkin`.

## Conventions

| Rule | Rationale |
|---|---|
| Use Deployments or StatefulSets instead of direct Pods | Controllers provide reconciliation, rollout, and rollback behavior |
| Define `resources`, `livenessProbe`, and `readinessProbe` for every container | Scheduling, restarts, and Service routing need explicit signals |
| Keep labels and selectors consistent | Controllers and Services cannot manage Pods they cannot select |
| Store secrets in `Secret` or an external secret manager, not `ConfigMap` | ConfigMaps are not secret storage |
| Apply least privilege with RBAC, NetworkPolicies, and security contexts | Compromise blast radius stays bounded |
| Send logs to `STDOUT`/`STDERR` and expose metrics/traces | Operations teams need centralized observability |
| Avoid mutable image tags such as `:latest` | Rollbacks and audits require reproducible images |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `ClusterIP` internally and `LoadBalancer` or Ingress for external traffic | Expose every service with `NodePort` by default |
| Set `maxSurge` and `maxUnavailable` for controlled rollouts | Rely on unspecified rollout behavior for critical workloads |
| Use readiness probes to remove unavailable Pods from endpoints | Route traffic to containers that are still starting or degraded |
| Use external secret operators for production secret lifecycle | Hardcode API keys, passwords, or TLS material in manifests |
| Scan, sign, and pin images | Deploy unscanned images from untrusted sources |

## Checklist Before Opening a PR

- [ ] `apiVersion`, `kind`, and `metadata.name` are correct and descriptive.
- [ ] Labels and selectors match across controllers, templates, and Services.
- [ ] Workloads use controllers rather than direct Pods where appropriate.
- [ ] Every container defines CPU and memory requests and limits.
- [ ] Liveness and readiness probes are configured with realistic timing.
- [ ] Services and Ingress resources use the intended exposure model and TLS configuration.
- [ ] Sensitive values are in Secrets or an external secret manager, not ConfigMaps.
- [ ] Security contexts set non-root execution, no privilege escalation, read-only root filesystem where possible, and dropped capabilities.
- [ ] RBAC and NetworkPolicies follow least privilege.
- [ ] Images are pinned, scanned, and avoid `:latest`.
- [ ] Logs go to `STDOUT`/`STDERR`, metrics and alerts are defined, and traces are considered for distributed flows.
- [ ] Rollout and rollback behavior is explicit and previous image versions remain available.
