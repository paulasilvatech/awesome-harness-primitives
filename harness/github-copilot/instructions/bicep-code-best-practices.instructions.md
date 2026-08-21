---
applyTo: "**/*.bicep"
description: "Enforces Azure Bicep conventions for naming, parameters, variables, resources, child resources, security, modules, outputs, and documentation."
name: "Bicep Code Best Practices"
---

# Bicep Code Conventions — Azure Infrastructure Hygiene

These instructions apply to Azure Bicep infrastructure files. They are authoritative for Bicep naming, declaration order, parameter design, variable usage, resource references, child resources, outputs, and security hygiene in matched files; deployment-specific architecture, resource inventory, policy, and environment requirements win when they impose stricter Azure constraints.

## Naming and Symbolic References

Use names that describe the Bicep symbol, not only the deployed Azure name.

| Element | Convention |
| --- | --- |
| Parameters | Use `lowerCamelCase` and describe the deployment setting they control. |
| Variables | Use `lowerCamelCase`; do not add suffixes only to distinguish variables from parameters. |
| Resources | Use resource-type descriptive symbolic names such as `storageAccount`, not `storageAccountName`. |
| Modules | Use `lowerCamelCase` names that describe the module purpose. |
| Outputs | Use `lowerCamelCase` names that describe the exported value. |

Avoid `name` in a symbolic resource name because the symbol represents the resource, not the resource's deployed name.

## Structure and Declarations

Keep Bicep files navigable by grouping declarations consistently.

- Declare parameters at the top of the file.
- Add descriptive `@description` decorators for every parameter.
- Specify minimum and maximum character length decorators for naming parameters when Azure resource constraints require them.
- Use the latest stable API version for each resource type supported by the target environment.
- Keep helpful `//` comments for non-obvious infrastructure intent, dependencies, or policy constraints.
- Use modules when a resource group grows into repeatable or independently owned infrastructure.

## Parameters and Variables

Use parameters for values that change between deployments and variables for derived expressions.

| Practice | Reason |
| --- | --- |
| Set safe defaults for test environments | Safe low-cost pricing tiers reduce accidental spend during validation. |
| Use `@allowed` sparingly | Overly narrow allowed lists block valid future deployments. |
| Do not default secrets | Secrets should come from secure deployment inputs or Key Vault references. |
| Let variables infer type from resolved values | Bicep already infers variable types and avoids redundant declarations. |
| Move complex expressions into variables | Resource bodies stay readable and repeated logic stays consistent. |

## Resource Names and Dependencies

Create meaningful resource names without sacrificing uniqueness.

- Use template expressions with `uniqueString()` when a resource name must be globally or regionally unique.
- Add a prefix before `uniqueString()` output because some Azure resources do not allow names that start with numbers.
- Reference resources through symbolic names and properties such as `resourceA.id`.
- Create implicit dependencies through symbolic references instead of explicit `dependsOn` unless Bicep cannot infer the dependency.
- Prefer the `existing` keyword for accessing existing resources instead of passing values through outputs.
- Avoid `reference()` and `resourceId()` when a symbolic name or existing resource reference can express the relationship.

## Child Resources, Outputs, and Security

Model child resources with Bicep syntax rather than hand-built names.

- Avoid excessive nesting of child resources when it makes the file harder to scan.
- Use the `parent` property or nested resource syntax instead of constructing child resource names manually.
- Output only values needed by callers or other modules.
- Never include secrets, keys, connection strings, or credentials in outputs.
- Use resource properties directly in outputs, for example `storageAccount.properties.primaryEndpoints`.

## Good / Bad Examples

The examples below illustrate symbolic names, safe naming, implicit dependencies, and non-secret outputs.

**Good:**

```bicep
@description('Deployment environment name.')
param environmentName string

@description('Base name for the storage account.')
@minLength(3)
@maxLength(18)
param storageBaseName string

var storageAccountName = '${storageBaseName}${uniqueString(resourceGroup().id, environmentName)}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: resourceGroup().location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

output storageEndpoints object = storageAccount.properties.primaryEndpoints
```

Why: The symbol describes the resource, names use `lowerCamelCase`, parameters are described and constrained, uniqueness has a prefix, and the output exposes endpoints rather than keys.

**Bad:**

```bicep
param name string = 'prodstore'

resource storageAccountName 'Microsoft.Storage/storageAccounts@2021-01-01' = {
  name: uniqueString(resourceGroup().id)
  location: resourceGroup().location
}

output key string = storageAccountName.listKeys().keys[0].value
```

Why: The parameter is vague, the symbolic name represents a name instead of a resource, the generated name can start with a number, the API version is stale, and the output exposes a secret key.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use `lowerCamelCase` for parameters, variables, resources, modules, and outputs | Bicep files remain idiomatic and consistent. |
| Use resource-type descriptive symbolic names without a `name` suffix | Symbols represent resources and make references readable. |
| Put parameters first and document each with `@description` | Deployment inputs are discoverable and reviewable. |
| Use safe test defaults and reserve `@allowed` for true platform constraints | Templates stay easy to validate without blocking legitimate environments. |
| Put complex expressions in variables | Resource declarations remain focused on Azure shape. |
| Use symbolic references, `existing`, and implicit dependencies | Bicep can type-check dependencies and avoid brittle string IDs. |
| Prefix `uniqueString()` outputs for resource names | Generated names satisfy Azure resources that cannot start with numbers. |
| Keep secrets and keys out of outputs | Deployment logs and downstream state do not leak credentials. |
| Add comments only where infrastructure intent is non-obvious | Documentation improves readability without duplicating the code. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Name a storage resource symbol `storageAccount` | Name the resource symbol `storageAccountName`. |
| Use `resourceA.id` to create dependencies | Add explicit `dependsOn` when a symbolic reference is enough. |
| Use `existing` for resources managed elsewhere | Pass existing resource values through unrelated outputs. |
| Use `parent` or nested syntax for child resources | Construct child names manually from strings. |
| Output `storageAccount.properties.primaryEndpoints` when callers need endpoints | Output secrets, keys, or connection strings. |
| Use latest stable API versions | Pin old API versions without a compatibility reason. |
| Use `//` comments for non-obvious decisions | Add comments that repeat each property name. |

## Checklist Before Opening a PR

- [ ] Names use `lowerCamelCase` and resource symbols describe resource types.
- [ ] Parameters appear at the top and include descriptive `@description` decorators.
- [ ] Naming parameters include minimum and maximum length constraints where Azure requires them.
- [ ] Defaults are safe for test environments and no secret has a default value.
- [ ] `@allowed` is used only for true deployment constraints.
- [ ] Complex expressions are stored in variables.
- [ ] Resource relationships use symbolic names, `resourceA.id`, `existing`, and implicit dependencies where possible.
- [ ] Resource names using `uniqueString()` include a nonnumeric prefix.
- [ ] Child resources use `parent` or nesting rather than manually constructed names.
- [ ] Outputs contain only required non-secret values.
