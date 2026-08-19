---
name: azure-infrastructure
description: "Use when designing Azure infrastructure patterns for Open Horizons, including hub-spoke networking, private endpoints, Workload Identity, naming, tagging, provider registration, and resource guardrails; produces an architecture pattern recommendation and implementation checklist. DO NOT USE FOR: Terraform CLI commands (use terraform-cli), Azure CLI operations (use azure-cli), or Kubernetes operations (use kubectl-cli). Triggers include \"design Azure infrastructure\", \"review private endpoint strategy\", \"define naming and tags\"."
---

# Azure Infrastructure

This workflow turns an Azure platform requirement into an Open Horizons infrastructure pattern: naming, tags, identity, network posture, private endpoints, diagnostics, and module alignment. It produces a recommendation and checklist rather than directly replacing Terraform module work.

> [!NOTE]
> This skill may reference Azure CLI and repository bootstrap scripts for context, including `.github/skills/azure-infrastructure/scripts/bootstrap.sh` and `.github/skills/azure-infrastructure/scripts/platform-bootstrap.sh`, but infrastructure changes should be implemented through `terraform/` or the deployment orchestration workflow.

## When to invoke
- "Design the Azure infrastructure pattern for a new Open Horizons environment."
- "Review our private endpoint and hub-spoke networking approach."
- "Define the naming and tagging strategy for Terraform modules."
- "Plan Workload Identity and managed identity access for AKS services."

## Prerequisites and context
- Target environment and region are known.
- Required Azure services and data sensitivity are identified.
- Terraform modules exist under `terraform/modules/` and environment files under `terraform/environments/`.
- Required tags are known: environment, project, owner, cost-center.
- User approval is available before running any bootstrap or provisioning script.

## Procedure

### Step 1: Confirm infrastructure scope
```text
Infrastructure design scope:
- Environment:
- Region:
- Services:
- Network posture:
- Identity model:
- Artifacts or scripts to run:
Proceed with creating artifacts or running provisioning scripts? (y/n)
```

> [!IMPORTANT]
> Only proceed with creating artifacts, running bootstrap scripts, or recommending paid resource creation as an action if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the design recommendation and stop.

### Step 2: Map services to repository modules
```bash
find terraform/modules -maxdepth 1 -mindepth 1 -type d | sort
find terraform/environments -maxdepth 1 -type f | sort
```

- [ ] AKS aligns to `terraform/modules/aks-cluster/`.
- [ ] Networking aligns to `terraform/modules/networking/`.
- [ ] Databases align to `terraform/modules/databases/`.
- [ ] ArgoCD aligns to `terraform/modules/argocd/`.
- [ ] Backstage aligns to `terraform/modules/backstage/`.
- [ ] AI Foundry aligns to `terraform/modules/ai-foundry/`.

### Step 3: Apply Azure landing-zone checks
- [ ] Naming follows `{project}-{environment}-{resource}-{region}` or module-specific Azure constraints.
- [ ] Tags include `environment`, `project`, `owner`, and `cost-center`.
- [ ] PaaS services use private endpoints for production-sensitive data.
- [ ] AKS uses Workload Identity rather than service principal secrets.
- [ ] Diagnostic settings route logs and metrics to the approved observability workspace.
- [ ] Network security groups and Kubernetes network policies follow least privilege.
- [ ] Resource locks are considered for production critical resources.

### Step 4: Use bootstrap scripts only as approved orchestration helpers
```bash
.github/skills/azure-infrastructure/scripts/platform-bootstrap.sh --horizon h1 --environment dev --dry-run
.github/skills/azure-infrastructure/scripts/bootstrap.sh express
```

Run dry-run first when available, and prefer `scripts/deploy-full.sh` for full platform orchestration.

### Step 5: Produce the implementation checklist
- Identify Terraform module changes, validation commands, and security controls.
- Route actual `terraform plan` and `terraform apply` execution to `terraform-cli` or `deploy-orchestration`.
- Route direct Azure discovery to `azure-cli`.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Public exposure of sensitive PaaS data, shared credentials, or missing tenant isolation. |
| High | No private endpoint, broad RBAC, unsupported region/SKU, or missing diagnostics for production. |
| Medium | Naming/tagging drift, incomplete module mapping, or unclear cost ownership. |
| Low | Documentation gaps or non-blocking optimization opportunities. |

## Limits

- Do not use this skill for: Terraform CLI commands (use terraform-cli), Azure CLI operations (use azure-cli), or Kubernetes operations (use kubectl-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Module does not exist | Report the missing module and propose a Terraform module task; do not invent paths. |
| Region or SKU unavailable | Use `azure-cli` discovery or official docs and record alternatives. |
| Bootstrap script scope is unclear | Run only `--dry-run` if available and ask for confirmation before mutation. |
| Requirement conflicts with policy | State the conflict and propose the least-privilege compliant option. |

## Output template

Return exactly this structure:
```markdown
# Azure Infrastructure Pattern Recommendation

## Scope
- Environment:
- Region:
- Services:

## Module Mapping
| Capability | Repository module | Notes |
|---|---|---|

## Controls
| Area | Decision | Rationale |
|---|---|---|

## Risks
| Severity | Finding | Mitigation |
|---|---|---|

## Implementation Checklist
- [ ] 
```

## Quality gate
- [ ] Every referenced repository path exists.
- [ ] Identity uses managed identity or Workload Identity.
- [ ] Private endpoint and diagnostic decisions are documented.
- [ ] Mutating scripts or paid resource actions require explicit confirmation.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
