---
applyTo: "**/*.terraform,**/*.tf,**/*.tfvars,**/*.tfstate,**/*.tflint.hcl,**/*.tf.json,**/*.tfvars.json"
description: "Enforces Azure Verified Modules Terraform discovery, source naming, version pinning, telemetry, validation, and PR readiness when authoring Terraform IaC."
---

# Azure Verified Modules Terraform Conventions — Registry Modules and PR Gates

These instructions apply to files matched by `**/*.terraform,**/*.tf,**/*.tfvars,**/*.tfstate,**/*.tflint.hcl,**/*.tf.json,**/*.tfvars.json`. They are authoritative for azure verified modules terraform code, configuration, examples, validation commands, API names, and runtime constraints in those files; stricter repository-specific security, deployment, testing, or platform primitives win on conflict. Treat the rules as passive conventions injected into matching files, not as a step-by-step workflow.

## Overview

Azure Verified Modules (AVM) are pre-built, tested, and validated Terraform and Bicep modules that follow Azure best practices. Use these modules to create, update, or review Azure Infrastructure as Code (IaC) with confidence.

## AVM Validation Gates

**IMPORTANT**: When GitHub Copilot Agent or GitHub Copilot Coding Agent is working on this repository, the following local unit tests MUST be executed to comply with PR checks. Failure to run these tests will cause PR validation failures:

```bash
./avm pre-commit
./avm tflint
./avm pr-check
```

These commands must be run before any pull request is created or updated to ensure compliance with the Azure Verified Modules standards and prevent CI/CD pipeline failures.
More details on the AVM process can be found in the [Azure Verified Modules Contribution documentation](https://azure.github.io/Azure-Verified-Modules/contributing/terraform/contribution-flow/).

**Failure to run these tests will cause PR validation failures and prevent successful merges.**

## Module Discovery

### Terraform Registry

- Search for "avm" + resource name
- Filter by "Partner" tag to find official AVM modules
- Example: Search "avm storage account" → filter by Partner

### Official AVM Index

>**Note:** The following links always point to the latest version of the CSV files on the main branch. As intended, this means the files may change over time. If you require a point-in-time version, consider using a specific release tag in the URL.

- **Terraform Resource Modules**: `https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformResourceModules.csv`
- **Terraform Pattern Modules**: `https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformPatternModules.csv`
- **Terraform Utility Modules**: `https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformUtilityModules.csv`


## Terraform Module Usage

### From Examples

- Copy the example code from the module documentation
- Replace `source = "../../"` with `source = "Azure/avm-res-{service}-{resource}/azurerm"`
- Add `version = "~> 1.0"` (use latest available)
- Set `enable_telemetry = true`

### From Scratch

- Copy the Provision Instructions from module documentation
- Configure required and optional inputs
- Pin the module version
- Enable telemetry

### Example Usage

```hcl
module "storage_account" {
  source  = "Azure/avm-res-storage-storageaccount/azurerm"
  version = "~> 0.1"

  enable_telemetry    = true
  location            = "East US"
  name                = "mystorageaccount"
  resource_group_name = "my-rg"

  # Additional configuration...
}
```

## Naming Conventions

### Module Types

- **Resource Modules**: `Azure/avm-res-{service}-{resource}/azurerm`
  - Example: `Azure/avm-res-storage-storageaccount/azurerm`
- **Pattern Modules**: `Azure/avm-ptn-{pattern}/azurerm`
  - Example: `Azure/avm-ptn-aks-enterprise/azurerm`
- **Utility Modules**: `Azure/avm-utl-{utility}/azurerm`
  - Example: `Azure/avm-utl-regions/azurerm`

### Service Naming

- Use kebab-case for services and resources
- Follow Azure service names (e.g., `storage-storageaccount`, `network-virtualnetwork`)

## Version Management

### Check Available Versions

- Endpoint: `https://registry.terraform.io/v1/modules/Azure/{module}/azurerm/versions`
- Example: `https://registry.terraform.io/v1/modules/Azure/avm-res-storage-storageaccount/azurerm/versions`

### Version Pinning Best Practices

- Use pessimistic version constraints: `version = "~> 1.0"`
- Pin to specific versions for production: `version = "1.2.3"`
- Always review changelog before upgrading

## Module Sources

### Terraform Registry

- **URL Pattern**: `https://registry.terraform.io/modules/Azure/{module}/azurerm/latest`
- **Example**: `https://registry.terraform.io/modules/Azure/avm-res-storage-storageaccount/azurerm/latest`

### GitHub Repository

- **URL Pattern**: `https://github.com/Azure/terraform-azurerm-avm-{type}-{service}-{resource}`
- **Examples**:
  - Resource: `https://github.com/Azure/terraform-azurerm-avm-res-storage-storageaccount`
  - Pattern: `https://github.com/Azure/terraform-azurerm-avm-ptn-aks-enterprise`

## Development Best Practices

### Module Usage

- **Always** pin module and provider versions
- **Start** with official examples from module documentation
- **Review** all inputs and outputs before implementation
- **Enable** telemetry: `enable_telemetry = true`
- **Use** AVM utility modules for common patterns
- **Follow** AzureRM provider requirements and constraints

### Code Quality

- **Always** run `terraform fmt` after making changes
- **Always** run `terraform validate` after making changes
- **Use** meaningful variable names and descriptions
- **Add** proper tags and metadata
- **Document** complex configurations

### Validation Requirements

Before creating or updating any pull request:

```bash
# Format code
terraform fmt -recursive

# Validate syntax
terraform validate

# AVM-specific validation (MANDATORY)
./avm pre-commit
./avm tflint
./avm pr-check
```

## Tool Integration

### Use Available Tools

- **Deployment Guidance**: Use `azure_get_deployment_best_practices` tool
- **Service Documentation**: Use `microsoft.docs.mcp` tool for Azure service-specific guidance
- **Schema Information**: Use `azure_get_schema_for_Bicep` for Bicep resources

### GitHub Copilot Integration

When working with AVM repositories:

- Always check for existing modules before creating new resources
- Use the official examples as starting points
- Run all validation tests before committing
- Document any customizations or deviations from examples

## Common Patterns

### Resource Group Module

```hcl
module "resource_group" {
  source  = "Azure/avm-res-resources-resourcegroup/azurerm"
  version = "~> 0.1"

  enable_telemetry = true
  location         = var.location
  name            = var.resource_group_name
}
```

### Virtual Network Module

```hcl
module "virtual_network" {
  source  = "Azure/avm-res-network-virtualnetwork/azurerm"
  version = "~> 0.1"

  enable_telemetry    = true
  location            = module.resource_group.location
  name                = var.vnet_name
  resource_group_name = module.resource_group.name
  address_space       = ["10.0.0.0/16"]
}
```

## Troubleshooting

### Common Issues

- **Version Conflicts**: Always check compatibility between module and provider versions
- **Missing Dependencies**: Ensure all required resources are created first
- **Validation Failures**: Run AVM validation tools before committing
- **Documentation**: Always refer to the latest module documentation

### Support Resources

- **AVM Documentation**: `https://azure.github.io/Azure-Verified-Modules/`
- **GitHub Issues**: Report issues in the specific module's GitHub repository
- **Community**: Azure Terraform Provider GitHub discussions

## AVM Submission Readiness

Before submitting any AVM-related code:

- [ ] Module version is pinned
- [ ] Telemetry is enabled
- [ ] Code is formatted (`terraform fmt`)
- [ ] Code is validated (`terraform validate`)
- [ ] AVM pre-commit checks pass (`./avm pre-commit`)
- [ ] TFLint checks pass (`./avm tflint`)
- [ ] AVM PR checks pass (`./avm pr-check`)
- [ ] Documentation is updated
- [ ] Examples are tested and working

## Good / Bad Examples

The examples below show the boundary between an acceptable convention and the closest common anti-pattern.

**Good:**

```hcl
module "storage_account" {
  source  = "Azure/avm-res-storage-storageaccount/azurerm"
  version = "~> 0.1"
  enable_telemetry = true
}
```

Why: The module uses the AVM registry source, a pinned version, and telemetry.

**Bad:**

```hcl
module "storage_account" {
  source = "../../"
}
```

Why: The module keeps a relative example source and omits AVM runtime expectations.

## Conventions

| Rule | Rationale |
| --- | --- |
| Prefer AVM Terraform modules before raw AzureRM resources and use `Azure/avm-res-{service}-{resource}/azurerm`, `Azure/avm-ptn-{pattern}/azurerm`, or `Azure/avm-utl-{utility}/azurerm` sources. | AVM modules carry tested Azure defaults and consistent interfaces. |
| Pin module and provider versions with `version = "~> 1.0"` or exact production versions. | Pinned versions prevent unreviewed registry changes. |
| Run `terraform fmt -recursive`, `terraform validate`, `./avm pre-commit`, `./avm tflint`, and `./avm pr-check`. | These gates match AVM PR validation. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Prefer AVM Terraform modules before raw AzureRM resources and use `Azure/avm-res-{service}-{resource}/azurerm`, `Azure/avm-ptn-{pattern}/azurerm`, or `Azure/avm-utl-{utility}/azurerm` sources. | Do not ignore this rule: Prefer AVM Terraform modules before raw AzureRM resources and use `Azure/avm-res-{service}-{resource}/azurerm`, `Azure/avm-ptn-{pattern}/azurerm`, or `Azure/avm-utl-{utility}/azurerm` sources. |
| Pin module and provider versions with `version = "~> 1.0"` or exact production versions. | Do not ignore this rule: Pin module and provider versions with `version = "~> 1.0"` or exact production versions. |
| Run `terraform fmt -recursive`, `terraform validate`, `./avm pre-commit`, `./avm tflint`, and `./avm pr-check`. | Do not ignore this rule: Run `terraform fmt -recursive`, `terraform validate`, `./avm pre-commit`, `./avm tflint`, and `./avm pr-check`. |

## Checklist Before Opening a PR

- [ ] The change stays inside the matched `applyTo` scope.
- [ ] The authoritative conventions above are applied to new or modified code.
- [ ] Named commands, paths, API names, configuration keys, and version constraints remain intact.
- [ ] Relevant validation, linting, build, or test commands from this instruction pass.
- [ ] No secrets, unsupported APIs, placeholder prompt references, or relative primitive links were added.

## References

- https://azure.github.io/Azure-Verified-Modules/
- https://azure.github.io/Azure-Verified-Modules/contributing/terraform/contribution-flow/
- https://github.com/Azure/terraform-azurerm-avm-ptn-aks-enterprise
- https://github.com/Azure/terraform-azurerm-avm-res-storage-storageaccount
- https://github.com/Azure/terraform-azurerm-avm-{type}-{service}-{resource}
- https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformPatternModules.csv
- https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformResourceModules.csv
- https://raw.githubusercontent.com/Azure/Azure-Verified-Modules/refs/heads/main/docs/static/module-indexes/TerraformUtilityModules.csv
- https://registry.terraform.io/modules/Azure/avm-res-storage-storageaccount/azurerm/latest
- https://registry.terraform.io/modules/Azure/{module}/azurerm/latest
- https://registry.terraform.io/v1/modules/Azure/avm-res-storage-storageaccount/azurerm/versions
- https://registry.terraform.io/v1/modules/Azure/{module}/azurerm/versions
