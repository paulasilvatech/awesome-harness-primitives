---
name: backstage-kubernetes
description: >-
  Install, configure, authorize, and troubleshoot Backstage Kubernetes frontend and backend
  plugins, cluster discovery, entity annotations, authentication, permissions, proxies, custom
  resources, and service-owner views. Use when working with Kubernetes tabs, clusters, pods, or
  integration errors.
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/skills/backstage-kubernetes/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage Kubernetes

Expose workload health to service owners without turning Backstage into a cluster-administration
console.

## When to invoke

- "Add the Kubernetes tab to catalog entities."
- "Configure cluster discovery and authentication."
- "Fix missing workloads or cluster access."
- "Restrict Kubernetes resources and proxy permissions."

## Procedure

1. Confirm Backstage version, frontend mode, cluster topology, and security boundary.
2. Install `@backstage/plugin-kubernetes` in the app and
   `@backstage/plugin-kubernetes-backend` in the backend.
3. Register the backend plugin and confirm frontend feature discovery or explicit installation.
4. Choose a service locator and cluster locator based on tenancy and catalog ownership.
5. Configure cluster authentication with the least privilege needed for read-only service views.
6. Link entities to workloads using supported annotations or catalog relations.
7. Keep service-account tokens out of catalog entity annotations.
8. Configure custom resources, metrics lookup, TLS verification, and failure behavior explicitly.
9. Enable pod deletion only when required, permission-protected, and approved.
10. Apply the permission framework for clusters, resources, and proxy access.
11. Validate multiple clusters, missing annotations, partial locator failures, denied users, and
    representative workloads.

## Permission surface

- `kubernetes.clusters.read`
- `kubernetes.resources.read`
- `kubernetes.proxy`

Treat proxy access as higher risk because it can forward arbitrary Kubernetes API requests.

## Output template

```markdown
## Backstage Kubernetes result

| Cluster source | Auth | Service locator | Entity mapping | Validation |
| --- | --- | --- | --- | --- |

### Permissions
- Clusters:
- Resources:
- Proxy:
```

## Quality gate

- [ ] Frontend and backend packages match the target version.
- [ ] Locator and tenancy choices are documented.
- [ ] Tokens and credentials are external to catalog entities.
- [ ] TLS and metrics behavior are explicit.
- [ ] Cluster, resource, and proxy permissions are least-privilege.
- [ ] Positive, missing, partial-failure, and denied-access paths are tested.

## References

- [Backstage Kubernetes](https://backstage.io/docs/features/kubernetes/)
- [Kubernetes configuration](https://backstage.io/docs/features/kubernetes/configuration)
