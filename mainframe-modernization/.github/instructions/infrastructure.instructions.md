---
description: "Use when creating or reviewing infrastructure as code, Terraform, Bicep, Azure resource definitions, and environment configuration."
applyTo: "infra/**,**/*.tf,**/*.bicep,compose*.yml,compose*.yaml,docker-compose*.yml,docker-compose*.yaml"
---

# Infrastructure Conventions — Terraform and Compose

This file activates when you edit files under `infra/`, any `*.tf` or `*.bicep`, or a `compose`/`docker-compose` YAML file. It teaches how to provision Azure with Terraform (`azurerm ~> 3.x`, the primary tool) and how to keep local Compose parity safe. Prefer Terraform; use Bicep only where a module genuinely requires it. `infra/` is created by the team in Stage 3/4 — there is no inherited stack to copy.

## Provider and Versions

Pin the provider and the minimum Terraform version. Keep one `provider "azurerm"` block per configuration.

```hcl
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

## Module Layout

One module per Azure service area, so blast radius and ownership stay clear.

```text
infra/
├── networking/   # VNet, subnets, NSGs
├── compute/      # App Service / Container Apps
├── database/     # PostgreSQL Flexible Server
└── monitoring/   # Log Analytics, alerts
```

## Required Tags on Every Resource

Every resource carries `project`, `environment`, and `owner` (add `cost-center` where the team tracks it). Define them once in `locals` and spread them.

```hcl
locals {
  common_tags = {
    project     = var.project
    environment = var.environment
    owner       = var.owner
  }
}

resource "azurerm_resource_group" "main" {
  name     = "${var.project}-${var.environment}-rg-${var.location_short}"
  location = var.location
  tags     = local.common_tags
}
```

## Secrets

> [!WARNING]
> Secrets live only in `azurerm_key_vault_secret` — never in `locals`, `variables` defaults, `.tfvars`, or committed state. Mark secret inputs `sensitive = true` and inject them from the pipeline's OIDC session.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = var.db_password
  key_vault_id = azurerm_key_vault.main.id
  tags         = local.common_tags
}
```

## Managed Identity

Service-to-service authentication uses Managed Identity (`azurerm_user_assigned_identity` or a system-assigned identity), not connection strings with embedded passwords. Assign the identity and grant it Key Vault access via role assignment.

## Naming Convention

Resource names follow `{project}-{env}-{resource}-{region}`.

| Resource | Example |
|---|---|
| Resource group | `sifap-prod-rg-brs` |
| PostgreSQL server | `sifap-prod-psql-brs` |

## Formatting and Validation Gate

CI runs `terraform fmt -check -recursive`, then per module `terraform init -backend=false` followed by `terraform validate` (see [`ci.yml`](../workflows/ci.yml)). Before pushing, run `terraform fmt -recursive` and `terraform -chdir=<module> validate` locally. The [`iac-review`](../skills/iac-review/SKILL.md) skill owns drift detection and deeper module review.

## Docker Compose Parity

Compose is for local development only. Pin images by digest, keep secrets in a git-ignored `.env`, and never commit real credentials.

```yaml
services:
  db:
    image: postgres:16@sha256:<digest> # pin the digest
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD} # from .env, never hardcoded
```

## Conventions

| Rule | Rationale |
|---|---|
| `azurerm ~> 3.x`, pinned `required_version` | Reproducible plans across machines |
| One module per service area | Clear ownership, small blast radius |
| `project` + `environment` + `owner` tags on all resources | Cost, audit, and cleanup traceability |
| Secrets only in `azurerm_key_vault_secret` | No credentials in code or state |
| Managed Identity for service auth | No stored passwords between services |
| `fmt` + per-module `validate` clean | Matches the CI infra gate |

## Do / Do Not

| Do | Do not |
|---|---|
| Spread `local.common_tags` on every resource | Ship an untagged resource |
| Mark secret vars `sensitive = true` | Put a secret in a `variable` default or `.tfvars` |
| Pin Compose images by digest | Use `postgres:latest` |
| Authenticate via Managed Identity | Embed a password in a connection string |

## Checklist Before Opening a PR

- [ ] Provider is `azurerm ~> 3.x` with a pinned `required_version`
- [ ] Every resource carries `project`, `environment`, and `owner` tags
- [ ] No secret appears outside `azurerm_key_vault_secret`; secret vars are `sensitive`
- [ ] Service-to-service auth uses Managed Identity
- [ ] `terraform fmt -check -recursive` and per-module `validate` pass locally
- [ ] Compose files pin image digests and read secrets from a git-ignored `.env`
