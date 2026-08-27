# Terraform Patterns

Alternative-path patterns for AppOnboard scaffold. Used when `.tf` files detected or user overrides `iacFormat`. Per-resource config comes from `mcp_azure_mcp_azureterraformbestpractices` at runtime — this file covers layout, provider, naming, state, tagging, and wiring.

## File Structure

### Default (greenfield or user override)

```
infra/
├── main.tf              # Root module — provider, resource group, module calls
├── variables.tf         # Input variables (all configurable values)
├── outputs.tf           # Exported values (endpoints, resource IDs)
├── backend.tf           # State backend config (local default, Azure Storage for prod)
├── terraform.tfvars     # Default variable values (from prepare-plan.json)
└── modules/
    ├── app-service/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── container-app/
    ├── sql-database/
    ├── key-vault/
    ├── log-analytics/
    └── ...
```

### Non-Azure IaC coexistence (GCP/AWS TF already in repo)

When `detectedInfraProvider.terraform` is `"gcp"`, `"aws"`, or `"multi"` (without `azurerm`), write Azure TF to a **separate directory** from existing non-Azure TF. Never overwrite or modify existing IaC files.

**Output directory rule:** If existing TF is NOT at `infra/`, write to `infra/`. If existing TF IS at `infra/` (or any path containing `infra`), write to `infra-azure/`. Same module structure as default layout.

Each Azure service gets its own module. `main.tf` orchestrates resource group + module calls.

## Provider Configuration

```hcl
terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id                 = var.subscription_id
  resource_provider_registrations = "none"
}
```

> ⛔ Never pin to exact patch versions (e.g., `= 4.1.0`). Use `~> 4.0` to allow minor/patch updates. `azurerm` manages API versions internally — if a resource isn't available in `azurerm`, use `azapi_resource` with the latest stable ARM API version.

> **Conditional access (AADSTS530084):** `azurerm` provider re-requests tokens that violate device-binding policies. Fix: (1) switch to Bicep, or (2) use service principal auth (`ARM_CLIENT_ID` + `ARM_CLIENT_SECRET` + `ARM_TENANT_ID`).

## variables.tf

Required variables: `environment_name` (string, default "dev"), `location` (string, default "eastus"), `subscription_id` (string), `session_id` (string), `deployed_by` (string). All configurable values MUST be variables — no hardcoded regions, names, or SKUs.

## terraform.tfvars

Populate from `prepare-plan.json`: `environment_name`, `location`, `subscription_id`, `session_id`. See naming-patterns.md for naming convention.

## Backend

Local backend by default: `backend "local" { path = "terraform.tfstate" }`. Recommend Azure Storage backend in `postDeployRecommendations[]` for production.

## Resource Group

Use `rg-${var.project_name}-${var.environment_name}-${random_string.suffix.result}` with `tags = local.tags`. Suffix prevents collisions across AppOnboard sessions.

## Naming Convention

```hcl
resource "random_string" "suffix" {
  length  = 4
  special = false
  upper   = false
}

locals {
  # Pattern: {type}-{appname}-{env}-{suffix}
  app_name    = "app-${var.environment_name}-${random_string.suffix.result}"
  kv_name     = "kv-${var.environment_name}-${random_string.suffix.result}"
  sql_name    = "sql-${var.environment_name}-${random_string.suffix.result}"
  # Storage/ACR: alphanumeric only, no hyphens
  storage_name = "st${replace(var.environment_name, "-", "")}${random_string.suffix.result}"
  acr_name     = "cr${replace(var.environment_name, "-", "")}${random_string.suffix.result}"
}
```

Cross-reference naming with [prepare/references/naming-patterns.md](../prepare/naming-patterns.md) — Terraform names must match `prepare-plan.json.naming.resources[]`.

## Resource Tags — Mandatory

Apply all 5 AppOnboard tags via `local.tags` — see [iac-generation-rules.md § Session Tags](iac-generation-rules.md) for tag names and values.

```hcl
locals {
  tags = {
    "app-onboard-skill"       = "true"
    "app-onboard-session-id"  = var.session_id
    "created-at"      = timestamp()
    "environment"     = var.environment_name
    "deployed-by"     = var.deployed_by
  }
}
```

> ⚠️ `timestamp()` changes on every plan. Add `lifecycle { ignore_changes = [tags["created-at"]] }` on every resource.

## Secrets — random_password, Not random_string

```hcl
resource "random_password" "db_password" {
  length  = 32
  special = true
  lifecycle { ignore_changes = [result] }
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = random_password.db_password.result
  key_vault_id = azurerm_key_vault.kv.id
}
```

> ⛔ NEVER use `random_string` for secrets — it is not marked `sensitive` in state. Always use `random_password`.

## Container Apps — Two-Phase Wiring

Same circular dependency as Bicep — see [bicep-container-apps.md](bicep-container-apps.md). Phase 1: placeholder image, no ACR/KV refs. Phase 2: build + push, assign AcrPull, update via `az containerapp update --image` outside Terraform.

```hcl
# Phase 1: Placeholder image
resource "azurerm_container_app" "app" {
  template {
    container {
      name   = "app"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
  identity {
    type = "SystemAssigned"
  }
}
```

## outputs.tf

Export: `resource_group_name`, `app_url` (https://${hostname}), `resource_ids` (list of all deployed resource IDs for deploy-result.json).

## Security Defaults

Apply same security rules as Bicep — see [bicep-patterns-security.md](bicep-patterns-security.md). Terraform-specific syntax:

| Rule | Terraform HCL |
|------|---------------|
| Managed identity | `identity { type = "SystemAssigned" }` |
| ⛔ No SQL admin password | `azuread_authentication_only = true`. Never generate `administrator_login_password` |
| Key Vault RBAC | `enable_rbac_authorization = true` on `azurerm_key_vault` |
| KV secret reference | `app_settings = { KEY = "@Microsoft.KeyVault(VaultName=..;SecretName=..)" }` |
| HTTPS only | `https_only = true`, `minimum_tls_version = "1.2"` |
| Storage | `https_traffic_only_enabled = true`, `allow_nested_items_to_be_public = false`, `min_tls_version = "TLS1_2"` |
| ⛔ Cosmos DB RBAC | `azurerm_cosmosdb_sql_role_assignment`, NOT `azurerm_role_assignment` — see [rbac-roles.md](rbac-roles.md) |
| RBAC assignments | `principal_type = "ServicePrincipal"` REQUIRED — see [rbac-roles.md](rbac-roles.md) |
| SCM/FTP auth | `scm.allow: true` (scaffold), `ftp.allow: false` (always) — use `azapi_resource` |
