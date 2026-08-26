---
name: "iac-module"
description: "Create or refactor one Terraform module for SIFAP 2.0 Azure infrastructure with standard tags, typed variables, outputs, and validation."
argument-hint: "name=<module> service=<azurerm_resource> reqs=REQ-NNN"
agent: "devops-engineer"
tools: ["read", "search", "edit", "execute"]
---
# /iac-module

## Objective

Produce or update a **single Terraform module** in `infra/modules/` for SIFAP 2.0, scoped to one Azure service area (networking, compute, database, monitoring, or security). The module carries the standard SIFAP tags on every taggable resource, keeps secrets out of code, uses managed identity for service-to-service auth, and passes `terraform fmt` and `terraform validate` (plus `tflint` and `checkov`) before commit — matching the infra gate in `.github/workflows/ci.yml`.

## When to Invoke

When a bounded context needs a new Azure service, or when an existing module must be hardened or extended. Module changes ship in their own PR, separate from feature code.

## Preconditions

- `.specify/memory/constitution.md` states the non-negotiable rules (managed identity, Key Vault, network access)
- The Azure service and the linked `REQ-ID` are known
- The target module path (`infra/modules/<name>/`) is either new or exists for update

## Inputs the Team Must Provide

- The module name and Azure service (for example `database` for `azurerm_postgresql_flexible_server`)
- The linked `REQ-ID` in `specs/<NNN>-<feature>/spec.md` (usually non-functional or operational)
- The target environments (`dev`, `stage`, `prod`) and any per-environment overrides
- Whether this creates a new module or modifies an existing one

Ask the user for anything that is missing.

## What I Will Do

- Read [`../skills/iac-review/SKILL.md`](../skills/iac-review/SKILL.md) and the constitution, and follow existing module patterns
- Write the five-file module skeleton with typed, documented variables
- Apply the standard SIFAP tag set to every taggable resource
- Keep secrets in `azurerm_key_vault_secret` — never in `locals`, `variables`, or `outputs`
- Use managed identity and private networking by default
- Add `examples/basic/` and validate locally with `fmt`, `validate`, `tflint`, and `checkov`

## What I Will NOT Do

- Invent a SKU price, a region's availability, or a SIFAP-specific value — unknown inputs are parameterized and confirmed by the team
- Author the pipeline (`/pipeline`), write application code (`@builder`), or change requirements (`@requirements-engineer`)
- Put a secret in a variable, a default, an output, or the state file when it can be avoided
- Set `public_network_access_enabled = true` without a documented exception in `.specify/memory/constitution.md`
- Put a `provider` block inside the module, or tag some resources but not others

## Output Format

A five-file module (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`) plus `examples/basic/`. The core files follow the repo's real `azurerm` house style:

```hcl
# infra/modules/database/versions.tf
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116"
    }
    random = { source = "hashicorp/random", version = "~> 3.6" }
  }
}

# infra/modules/database/main.tf
locals {
  tags = merge(var.tags, {
    project     = "sifap"
    environment = var.environment
    owner       = var.owner
    cost-center = var.cost_center
    module      = "database"
    managed-by  = "terraform"
  })
}

resource "random_password" "admin" {
  length  = 32
  special = true
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                          = "${var.project}-${var.environment}-psql-${var.location_short}"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  version                       = "16"
  administrator_login           = var.administrator_login
  administrator_password        = random_password.admin.result
  public_network_access_enabled = false # private endpoint only; no exception on file
  tags                          = local.tags
}

# Secret lives in Key Vault, never in variables, outputs, or logs.
resource "azurerm_key_vault_secret" "admin_password" {
  name         = "${var.environment}-psql-admin-password"
  value        = random_password.admin.result
  key_vault_id = var.key_vault_id
  tags         = local.tags
}

# infra/modules/database/outputs.tf
output "server_fqdn" {
  description = "PostgreSQL FQDN for callers; contains no secret."
  value       = azurerm_postgresql_flexible_server.this.fqdn
}
```

Accompany the module with a validation report (`fmt`, `validate`, `tflint`, `checkov` output) and a one-line monthly cost note per environment linking to Azure pricing.

## Definition of Done

- [ ] `terraform fmt -check`, `terraform validate`, `tflint`, and `checkov` all pass
- [ ] Every taggable resource carries `project`, `environment`, and `owner` (plus the standard extras)
- [ ] No secret appears in variables, outputs, or default values
- [ ] Public network access is disabled unless a constitution exception is referenced
- [ ] Managed identity is used; no service-principal credential appears in code
- [ ] A consumer in `examples/basic/` compiles and validates
- [ ] The README documents inputs, outputs, an example, and the linked `REQ-ID`

## Prompt Body

You are the `@devops-engineer`. The team needs one focused, reviewable module that respects the repo's Terraform rules.

**Step 1 — Read the constitution and the skill.**
Open `.specify/memory/constitution.md` for non-negotiable rules and [`../skills/iac-review/SKILL.md`](../skills/iac-review/SKILL.md) for the review checklist. Review existing modules for patterns to follow.

**Step 2 — Pin the provider.**
Use `azurerm ~> 3.x` (the repo standard) pinned through `required_providers`, and reference [Azure Verified Modules](https://aka.ms/avm) where applicable.

**Step 3 — Write the skeleton.**
`main.tf` (resources only, no `provider` block), `variables.tf` (every input typed and documented, with `validation` blocks where ranges matter), `outputs.tf` (IDs, names, FQDNs — never secrets), `versions.tf`, and `README.md`.

**Step 4 — Apply the standard tags.**
Merge `var.tags` with `project`, `environment`, `owner`, `cost-center`, `module`, and `managed-by`, and attach the map to every taggable resource.

**Step 5 — Enforce secrets, identity, and network discipline.**
Secrets flow through `azurerm_key_vault_secret` data sources or generated values stored in Key Vault — never variables, defaults, or outputs. Use system- or user-assigned managed identities for service-to-service auth. Keep `public_network_access_enabled = false` unless the constitution grants an exception.

**Step 6 — Add an example and validate.**
Write `examples/basic/main.tf` that consumes the module, then run `terraform fmt -check -recursive`, `terraform init -backend=false`, `terraform validate`, `tflint --recursive`, and `checkov -d . --soft-fail false`. All must pass.

`terraform fmt` and `terraform validate` must pass before commit, matching `.github/workflows/ci.yml`. Every taggable resource carries the mandatory tags. No secret ever lands in a variable, output, or default. Never enable public network access without a documented exception, and never invent a value the team must confirm.

## Invocation Example

```
/iac-module name=database service=azurerm_postgresql_flexible_server reqs=REQ-NNN
```
