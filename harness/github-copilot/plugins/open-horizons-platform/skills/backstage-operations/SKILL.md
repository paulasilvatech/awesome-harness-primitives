---
name: backstage-operations
description: "Operate, monitor, troubleshoot, and harden production Backstage services, databases, schedulers, integrations, health endpoints, logs, and deployments. Use when handling startup failures, readiness problems, database errors, provider refresh issues, performance incidents, or production runbooks."
---

# Backstage operations

Diagnose from evidence before restarting or redeploying, and preserve clear ownership between the
Backstage service and its infrastructure.

## When to invoke

- "Backstage will not start or is not ready."
- "Catalog refreshes or scheduled tasks are failing."
- "Diagnose database, memory, or latency problems."
- "Create a production operations checklist."

## Procedure

1. Detect adopter, core development, Open Horizons, RHDH, or unknown mode and select the real
   runtime boundary.
2. Capture deployment version, config selection, database client, recent changes, health status,
   resource limits, and error evidence.
3. Inspect application logs and traces with sensitive values redacted.
4. Classify the failure as configuration, identity, integration, database, scheduler, plugin,
   dependency, network, resource, or deployment.
5. Reproduce safely with the narrowest health endpoint, package test, or local startup path.
6. Fix the root cause in the owning package or configuration layer.
7. Require approval before restarts, rollouts, database changes, traffic changes, or production
   mutations.
8. Validate readiness, liveness, login, catalog, templates, TechDocs, critical plugins, and
   scheduled tasks after remediation.
9. Record rollback, residual risk, and infrastructure handoffs.

## Operational evidence

- Backstage and package versions.
- Effective environment and configuration files.
- Health endpoint result.
- Database connectivity and migration state without credentials.
- Recent error signatures and affected plugin.
- Resource saturation, scheduler backlog, provider throttling, or integration failures.

## Output template

```markdown
## Backstage operations report

**Environment:** <environment>
**Version:** <version>
**Impact:** <users and capabilities>

| Evidence | Finding | Action | Result |
| --- | --- | --- | --- |

### Approval-gated operations
- <operation and status>

### Rollback
- <verified rollback or blocker>
```

## Quality gate

- [ ] Runtime mode, environment, version, and user impact are evidenced.
- [ ] Logs and telemetry are redacted and tied to a root-cause hypothesis.
- [ ] No restart or redeploy occurred before diagnosis and approval.
- [ ] Critical Backstage capabilities are revalidated after the fix.
- [ ] Database and integration mutations include rollback.
- [ ] Infrastructure-only issues are handed to the owning platform workflow.
