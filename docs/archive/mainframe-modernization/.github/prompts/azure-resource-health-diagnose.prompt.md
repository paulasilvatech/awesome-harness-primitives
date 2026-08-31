---
name: "azure-resource-health-diagnose"
description: "Diagnose an Azure resource's health from logs and telemetry and produce a remediation plan, deferring the workflow to the azure-resource-health-diagnose skill."
argument-hint: "resource=<name> rg=<resource-group>"
agent: "devops-engineer"
tools: ["read", "search", "execute"]
---
# /azure-resource-health-diagnose

## Objective

Assess the health of one Azure resource, diagnose issues from its logs and telemetry, and produce a prioritized remediation plan. The full workflow lives in the [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md) skill; this prompt applies it to the SIFAP 2.0 kit without restating it.

> [!NOTE]
> Diagnose before you change: classify issues by severity and confirm any fix against the Terraform in `infra/`.

## When to Invoke

During Stage 4 (Evolution), when a deployed Azure resource behaves unexpectedly and the team needs a structured diagnosis before acting.

## Preconditions

- The team is authenticated to Azure
- The resource is deployed and emitting logs/telemetry
- Diagnostic settings route logs to a reachable Log Analytics workspace

## Inputs the Team Must Provide

- `resource` — the resource name (and, if known, its resource group/subscription)
- The symptom observed and when it started
- Ask the user for anything that is missing.

## What I Will Do

- Follow the health-assessment and log-analysis workflow in the [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md) skill
- Focus first on the kit's resource types: Azure Database for PostgreSQL 16 and containerized Spring Boot services
- Classify issues (Critical/High/Medium/Low) and trace each to a root cause
- Produce a phased remediation plan with validation and rollback steps

## What I Will NOT Do

- Apply a remediation before diagnosis and team confirmation
- Recommend a manual change that diverges from the Terraform in `infra/`
- Ignore Managed Identity: I flag any resource still using shared keys or connection strings
- Overstate certainty when logs are missing (I note the limitation)

## Output Format

```markdown
### Health assessment — payment-db (Azure Database for PostgreSQL)
Status: Warning · Analyzed: <timestamp>

### Issues
| Severity | Issue | Root cause |
|---|---|---|
| High | Connection failures | Max connections exhausted |

### Remediation (phased)
1. Immediate — raise connection limit / add pooling
2. Short-term — right-size compute tier via Terraform
```

## Definition of Done

- [ ] Health status is stated with supporting metrics
- [ ] Issues are classified by severity with a root cause each
- [ ] The remediation plan is phased, with validation and rollback
- [ ] Any fix is expressed against the Terraform in `infra/`

## Prompt Body

The [`azure-resource-health-diagnose`](../skills/azure-resource-health-diagnose/SKILL.md) skill owns the resource-type-specific diagnostics and KQL queries — read it, then apply it to the target resource.

**Step 1 — Identify.**
Locate the resource, its type, and its dependencies.

**Step 2 — Apply the skill.**
Run the health checks and log/telemetry queries per the skill and recognize the failure patterns.

**Step 3 — Respect the kit rules.**
Prioritize PostgreSQL 16 and Spring Boot services, flag non-Managed-Identity auth, and tie fixes to `infra/` Terraform.

**Step 4 — Plan.**
Classify the issues and produce the phased remediation plan; wait for confirmation before acting.

## Invocation Example

```
/azure-resource-health-diagnose resource=payment-db rg=sifap-prod-rg
```
