---
name: azure-infrastructure
description: >-
  Azure infrastructure patterns guide landing-zone, networking, identity, naming, tagging, and private connectivity decisions. Use this skill when designing hub-spoke networks, private endpoint patterns, Workload Identity, naming conventions, tag strategies, AKS architecture, Key Vault access, or secure PaaS topology.
---

# Azure Infrastructure

Convert Azure infrastructure planning needs into opinionated Open Horizons patterns for naming, tagging, security posture, and platform resource design without executing deployment commands.

## When to invoke

- "Plan Azure infrastructure for Open Horizons."
- "Design a hub-spoke network or private endpoint pattern."
- "Define Workload Identity and managed identity access."
- "Create naming conventions and tag strategy."
- "Review AKS, Key Vault, or secure PaaS topology."

## Prerequisites and context

- Azure subscription access.
- Terraform knowledge.
- Understanding of Azure services.
- Use bundled scripts only when infrastructure bootstrap automation is explicitly needed.

## Criteria

### Reference patterns

#### Resource Group Naming

```
rg-<project>-<environment>-<region>
Example: rg-3horizons-prod-eastus2
```

#### AKS Cluster Naming

```
aks-<project>-<environment>-<region>
Example: aks-3horizons-prod-eastus2
```

#### Key Vault Naming

```
kv-<project>-<environment>-<region>
Example: kv-3horizons-prod-eus2
```

#### Storage Account Naming

```
st<project><environment><region>
Example: st3horizonsprodeus2
```

### Required Tags

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
  }
}
```

### Security Patterns

- Use Workload Identity (not service principals).
- Enable private endpoints for PaaS services.
- Configure NSGs with deny-all default.
- Enable Azure Defender for Cloud.

### Best practices

1. Use Azure Verified Modules when available.
2. Follow CAF naming conventions.
3. Enable diagnostic settings.
4. Configure resource locks for production.
5. Use managed identities.

## Output template

Return exactly this structure:

```markdown
Azure Infrastructure Recommendation

**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the recommended Azure infrastructure pattern.

### Details
- Scope: landing zone, network, identity, naming, tagging, AKS, Key Vault, or PaaS topology
- Recommended pattern: selected pattern and rationale
- Naming and tags: required names and tag block or deviations
- Security posture: Workload Identity, private endpoints, NSGs, Defender, diagnostics, and locks

### Validation
- Pattern fit: PASS | FAIL with evidence from the request and repository context
- Security check: PASS | FAIL | SKIPPED with managed identity and private connectivity evidence
- Handoff check: PASS | FAIL with any required `azure-cli`, `terraform-cli`, or `deploy-orchestration` boundary
```

## Limits

- Do not use this skill for running `az` commands.
- Use `azure-cli` (`skill`) instead when command execution or live Azure resource changes are required.
- Do not use this skill for writing Terraform plans.
- Use `terraform-cli` (`skill`) instead when the task needs Terraform command execution or plan output.
- Do not use this skill for Kubernetes operations.
- Use `kubectl-cli` (`skill`) instead when inspecting or mutating Kubernetes resources.
- Do not use this skill for full deployment sequencing.
- Use `deploy-orchestration` (`skill`) instead when coordinating H1, H2, or H3 deployment order.

## Progressive disclosure and bundled resources

At discovery time, only `name` and `description` are loaded. Read or run bundled resources only when the requested task needs bootstrap automation.

- `scripts/bootstrap.sh`: infrastructure bootstrap script.
- `scripts/platform-bootstrap.sh`: platform bootstrap script.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-terraform` | `agent` | Azure infrastructure guidance must become Terraform module code or review. |
| `open-horizons-security-reviewer` | `agent` | The infrastructure design needs security posture, RBAC, or compliance review. |
| `open-horizons-azure-readiness` | `agent` | Azure provider registration, quotas, resource inventory, or portal validation is needed. |
| `azure-cli` | `skill` | The next step is executing Azure CLI operations. |
| `deploy-orchestration` | `skill` | The task needs end-to-end platform deployment sequencing. |

## Quality gate

- [ ] `name` matches the `azure-infrastructure` directory.
- [ ] The recommendation uses existing naming patterns, required tags, and security patterns.
- [ ] Workload Identity, private endpoints, NSG posture, and Defender are considered when relevant.
- [ ] No live `az`, Terraform, or Kubernetes operation is presented as completed unless actually run by the owning primitive.
- [ ] Every bundled resource path referenced above exists.
- [ ] The response follows the output template with validation evidence.
