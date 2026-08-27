---
name: azure-terraform-cli
description: >-
  Terraform CLI operations manage Azure infrastructure as code through Terraform formatting,
  validation, initialization, planning, apply workflows, destroy workflows, state inspection,
  import workflows, module development, provider lock files, tfvars, and security scanning. Use
  this skill when working with terraform init, plan, apply, destroy, validate, fmt, state, import,
  or tfsec workflows.
---

<!-- Generated from harness/github-copilot/plugins/azure-cloud-development/skills/azure-terraform-cli/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Terraform CLI

Use this skill to turn Terraform infrastructure requests into ordered CLI workflows, preserve plan and state safety, and return formatting, validation, plan, scan, or read-only state evidence with exit codes and next-step recommendations.

## When to invoke

- "Validate or format Terraform configurations."
- "Run terraform init or create a Terraform plan."
- "Summarize resources to add, change, or destroy from a Terraform plan."
- "Inspect Terraform state without changing resources."
- "Run tfsec or Checkov against infrastructure code."

## Prerequisites and context

- Terraform >= 1.5.0 installed.
- Azure CLI authenticated.
- Backend storage account accessible.
- Environment variables: ARM_SUBSCRIPTION_ID, ARM_TENANT_ID.

## Procedure

1. Confirm the working directory, backend mode, environment, and tfvars file before running Terraform commands.
2. Run formatting and validation before planning when configuration changes are in scope.
3. Initialize with the appropriate backend mode for the requested workflow.
4. Create and inspect plans with saved plan files when planning changes.
5. Keep state operations read-only unless a separate approved workflow explicitly requires mutation.
6. Return the result using the output template.

### Format and validate

```bash
# Check formatting
terraform fmt -check -recursive -diff

# Apply formatting
terraform fmt -recursive

# Validate configuration
terraform init -backend=false
terraform validate
```

### Planning

```bash
# Initialize with backend
terraform init -reconfigure

# Create plan
terraform plan   -var-file=environments/${ENVIRONMENT}.tfvars   -out=tfplan   -detailed-exitcode

# Show plan in JSON
terraform show -json tfplan | jq '.resource_changes'
```

### Security scanning

```bash
# TFSec scan
tfsec . --format=json --out=tfsec-results.json

# Checkov scan
checkov -d . --output-file=checkov-results.json --output=json
```

### State operations (read-only)

```bash
# List resources
terraform state list

# Show resource details
terraform state show 'azurerm_kubernetes_cluster.main'
```

### Best practices

1. ALWAYS run `terraform fmt` before committing.
2. ALWAYS run `terraform validate` before planning.
3. NEVER commit .tfstate files.
4. ALWAYS use -out flag for plans to review.
5. Use workspaces for environment separation.
6. Enable state locking with Azure blob lease.

## Output template

Return exactly this structure:

```markdown
**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the formatting, validation, plan, scan, state, or infrastructure outcome.

### Details
1. Command executed: `<terraform, tfsec, or checkov command with full parameters>`
2. Exit code: `<0 success, 1 error, 2 changes pending, or tool-specific code>`
3. Workspace or environment: `<workspace, ENVIRONMENT, or tfvars file>`
4. Plan summary: `<resources to add/change/destroy or not applicable>`
5. Warnings or errors: `<line references, scan findings, backend issues, or none>`
6. Recommendations: `<next Terraform action or none>`

### Validation
- Formatting and validation: `<terraform fmt or validate evidence or reason not checked>`
- Plan or state evidence: `<terraform plan, show, state list, state show, scan output, or reason not checked>`
```

## Limits

- Do not use this skill for Azure CLI day-2 commands.
- Use `azure-cli` (`skill`) instead when the task is direct Azure resource queries, AKS credentials, ACR, Key Vault, account context, RBAC checks, or managed identity operations.
- Do not use this skill for Azure architecture design.
- Use `azure-infrastructure` (`skill`) instead when the task is architecture patterns, hub-spoke networking, private endpoints, naming, tagging, or Workload Identity design.
- Do not use this skill for Kubernetes operations.
- Use `azure-kubectl-cli` (`skill`) instead when the task is Kubernetes resource inspection, logs, events, manifests, rollout, or troubleshooting.
- Do not use this skill for Helm charts.
- Use `azure-helm-cli` (`skill`) instead when the task is chart values, repositories, templates, releases, upgrades, or rollbacks.
- Do not use this skill for full deployment orchestration.
- Use `open-horizons-deploy-orchestration` (`skill`) instead when the task spans prerequisites, Terraform apply sequencing, Kubernetes verification, and platform validation.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-terraform` | `agent` | Designing or implementing Terraform modules and infrastructure changes. |
| `open-horizons-security-reviewer` | `agent` | Reviewing Terraform security, compliance, or policy findings. |
| `open-horizons-deployment-operator` | `agent` | Coordinating approved Terraform execution as part of platform deployment. |
| `azure-cli` | `skill` | Verifying Azure account, resource, AKS, ACR, or Key Vault state outside Terraform. |
| `azure-infrastructure` | `skill` | Choosing Azure architecture patterns before encoding infrastructure. |
| `open-horizons-terraform-change` | `skill` | Repository-specific validation is required after Terraform changes. |

## Quality gate

- [ ] `name` is `azure-terraform-cli` and matches the parent directory.
- [ ] `terraform fmt` and `terraform validate` are run or explicitly marked not applicable before planning.
- [ ] Plans use `-out=tfplan` and report exit code semantics when a plan is created.
- [ ] State operations are read-only unless a separately approved mutating workflow is in scope.
- [ ] Security scan outputs preserve `tfsec-results.json` or `checkov-results.json` paths when scans run.
- [ ] `.tfstate` files are not committed or exposed in the response.
