---
paths:
  - "**/*.tf"
---

<!-- Generated from harness/github-copilot/instructions/generate-modern-terraform-code-for-azure.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Conventions for modern Terraform code targeting Azure, including provider choice, modules, variables, outputs, state, idempotency, documentation, validation, and testing.

# Modern Terraform for Azure Conventions — Provider and Module Hygiene

These instructions apply to Terraform files matched by the `applyTo` glob. They are authoritative for modern Azure Terraform layout, provider selection, variables, outputs, modules, state, idempotency, documentation, diagrams, validation, and test expectations; organization-specific infrastructure policy, security baselines, and deployment pipelines win where they define stricter provider, version, or resource rules.

## Versioning and Provider Selection

Always target stable Terraform and Azure provider releases that the project can support, and specify versions in code so the toolchain is reproducible. Prefer the `azurerm` provider for most Azure resources because it is stable and broad. Use `azapi` only for the latest Azure features or resources not yet supported in `azurerm`, and document that choice in a code comment. Both providers may be used together, but default to `azurerm` when in doubt.

Avoid adding additional providers or external modules beyond project scope without confirmation. If a special provider such as `random` or `tls` is needed, explain why in a comment and keep the dependency narrow. Keep tool versions and documentation up-to-date.

## File Layout and Formatting

Structure configurations by responsibility:

| File | Purpose |
| --- | --- |
| `main.tf` | Resources |
| `variables.tf` | Inputs |
| `outputs.tf` | Outputs |
| `locals.tf` | Shared computed values when useful |
| `terraform.tf` | `terraform {}` block, required Terraform version, and provider requirements |

Run `terraform fmt` so formatting stays consistent. Keep names and layout predictable enough that future modules can be compared quickly.

## Modules, Variables, and Outputs

- Encapsulate reusable infrastructure components in modules.
- Create a module with its own variables and outputs for resource sets used in multiple contexts.
- Reference modules instead of duplicating resource blocks.
- Parameterize configurable values with variables.
- Give every variable a type and description.
- Provide defaults only for optional values.
- Use outputs to expose key resource attributes required by callers or other modules.
- Mark sensitive variables and outputs as `sensitive = true`; avoid outputting secrets where possible.

## Idempotency and Drift

Write configurations that can be applied repeatedly with the same result. Avoid scripts that run on every apply, resources that conflict when created twice, and side effects outside Terraform state. Test idempotency by applying twice when safe; the second `terraform apply` should produce zero changes. Use lifecycle settings or conditional expressions only when they intentionally handle drift or externally managed changes.
Treat any non-idempotent action as an exception that requires a documented reason.

## State Management

Use a remote backend, such as Azure Storage with state locking, for shared Terraform state. Never commit state files to source control. Treat state as Terraform-managed data, not a document to edit by hand. Remote state prevents team conflicts and reduces the risk of leaked infrastructure details.

## Documentation, Diagrams, and Automation

- Keep infrastructure documentation up to date.
- Update `README.md` when variables, outputs, variables/outputs tables, usage instructions, or module behavior change.
- Consider `terraform-docs` for automated variable and output documentation.
- Update architecture diagrams after significant infrastructure changes.
- Consider CI pipelines and pre-commit hooks for formatting, linting, validation, and plan checks.

## Validation and Testing

Run `terraform validate` and review `terraform plan` before applying changes. Use automated checks where the project supports them. Prefer fast local validation before opening a PR, then rely on CI for broader environment checks.

## Good / Bad Examples

The examples below illustrate provider intent and typed variables.

**Good:**

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

variable "location" {
  type        = string
  description = "Azure region for the resources."
}
```

Why: Versions are explicit, the stable AzureRM provider is preferred, and the variable has a type and description.

**Bad:**

```hcl
resource "azurerm_resource_group" "rg" {
  name     = "example"
  location = "eastus"
}
```

Why: The configurable location is hardcoded and provider or Terraform version requirements are not shown.

## Conventions

| Rule | Rationale |
|---|---|
| Specify required Terraform and provider versions | Reproducible infrastructure avoids accidental upgrades |
| Prefer `azurerm`; use `azapi` only for unsupported or latest Azure features and document the reason | Stable providers reduce maintenance risk while preserving access to new Azure APIs |
| Split Terraform into `main.tf`, `variables.tf`, `outputs.tf`, `locals.tf`, and `terraform.tf` where applicable | Files remain navigable by responsibility |
| Encapsulate reusable resource sets in modules with typed variables and useful outputs | Infrastructure stays reusable and consistent |
| Keep provider and module dependencies minimal and justified | Lean stacks are easier to audit and maintain |
| Ensure idempotency and verify a second `terraform apply` reports zero changes when safe | Repeated deployments must converge |
| Use remote state such as Azure Storage with locking and never commit state files | Team collaboration remains safe and state does not leak |
| Update `README.md`, diagrams, and generated docs such as `terraform-docs` output when behavior changes | Consumers understand variables, outputs, and architecture |
| Run `terraform fmt`, `terraform validate`, and review `terraform plan` | Formatting, syntax, and unintended changes are caught early |

## Do / Do Not

| Do | Do not |
|---|---|
| Use `azurerm` for ordinary Azure resources | Reach for `azapi` without a feature-gap reason |
| Add a comment for special providers such as `random` or `tls` | Add providers or modules outside scope without confirmation |
| Parameterize configurable values | Hardcode environment-specific values into resources |
| Mark secrets and secret-bearing outputs `sensitive = true` | Output secrets as ordinary values |
| Store state in a remote backend with locking | Commit Terraform state files |
| Use lifecycle settings for deliberate drift handling | Hide unmanaged drift without documenting intent |
| Review `terraform plan` before apply | Apply changes without understanding planned modifications |

## Checklist Before Opening a PR

- [ ] Required Terraform and Azure provider versions are specified and stable.
- [ ] `azurerm` is used by default, and any `azapi`, `random`, `tls`, or external provider/module use is justified.
- [ ] Files are organized as `main.tf`, `variables.tf`, `outputs.tf`, `locals.tf`, and `terraform.tf` where applicable.
- [ ] Variables are typed and described, optional defaults are deliberate, and outputs expose only needed attributes.
- [ ] Sensitive values are marked `sensitive = true` and secrets are not output unnecessarily.
- [ ] Modules replace duplicated reusable resource sets.
- [ ] Configuration is idempotent and safe repeated applies converge.
- [ ] Remote state with locking is used and no state file is committed.
- [ ] `README.md`, `terraform-docs` output, and diagrams are updated when infrastructure behavior changes.
- [ ] `terraform fmt`, `terraform validate`, and `terraform plan` have been run or are covered by CI.
