---
applyTo: "terraform/**/*.tf,terraform/**/*.tf.example,terraform/**/*.tfvars.example"
description: "Use when editing Terraform that creates or changes Azure resource names, naming inputs, or required tags."
---

# Azure Resource Naming

`terraform/modules/naming/` is the authoritative local naming implementation. Use its inputs and outputs instead of recreating CAF abbreviations or ad hoc prefixes in consuming modules.

## Conventions

- Derive supported resource names from the naming module and keep the pattern `{resource-type}-{project}-{environment}-{region}-{instance}` where the service permits it.
- Use the module's hyphen-free and shortened outputs for globally unique or length-restricted resources such as storage accounts, registries, and Key Vault.
- Keep project, environment, location, instance, owner, and cost-center as explicit inputs; do not encode customer or personal data in names.
- Preserve the module's canonical tags: `environment`, `project`, `owner`, and `cost-center`; merge additional tags without replacing them.
- Validate service-specific length, character, start/end, and uniqueness constraints in the naming module rather than scattering truncation logic across callers.
- Treat changes to region codes, abbreviations, truncation, or output names as compatibility changes because environments consume those outputs.
- Document unavoidable legacy names or adoption exceptions in the owning environment without silently renaming live resources.

## Verification

- New Azure resources consume a suitable `module.naming` output or record a justified exception.
- Naming-module changes cover restricted-character, maximum-length, and deterministic-output cases.
- Examples contain sanitized values and match the current module interface.
