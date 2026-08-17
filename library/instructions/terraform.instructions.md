---
applyTo: "**/*.tf"
description: "Enforces Terraform conventions for secure, modular, maintainable, formatted, documented, tested, and version-controlled infrastructure code."
---

# Terraform Conventions — Secure Modular Infrastructure

These instructions apply to Terraform files matched by `**/*.tf`. They are authoritative for generic Terraform security, modularity, maintainability, style, documentation, validation, and testing; provider-specific platform instructions and repository infrastructure policies win when they define stricter requirements. Use Terraform to provision and manage infrastructure through version-controlled HCL, with secrets, state, and provider behavior handled conservatively.

## Security and State

- Use the latest stable Terraform version and stable provider versions allowed by the project.
- Regularly update Terraform configurations for security patches and provider improvements.
- Store sensitive information in secure systems such as AWS Secrets Manager or SSM Parameter Store.
- Use AWS environment variables to reference values stored in AWS Secrets Manager or SSM Parameter Store when that keeps secrets out of configuration.
- Rotate credentials and secrets regularly, and automate rotation where possible.
- Never commit AWS credentials, API keys, passwords, certificates, `.tfstate`, or other sensitive files.
- Use `.gitignore` to exclude files containing sensitive information.
- Mark sensitive variables and secret-bearing outputs with `sensitive = true`.
- Use IAM roles and policies with least privilege.
- Use security groups and network ACLs to control network access.
- Deploy resources in private subnets whenever possible; use public subnets only for resources requiring direct internet access, such as load balancers or NAT gateways.
- Encrypt sensitive data at rest and in transit, including EBS volumes, S3 buckets, RDS instances, and TLS service communication.
- Review and audit Terraform with tools such as `trivy`, `tfsec`, or `checkov`.

## Modularity and Composition

- Use separate projects for major infrastructure components when it reduces complexity, improves maintainability, speeds `plan` and `apply`, enables independent deployment, and reduces accidental changes.
- Use modules to encapsulate related resources and avoid duplication.
- Avoid circular dependencies between modules.
- Avoid modules for single resources and avoid excessive nesting; keep module hierarchy shallow.
- Use `output` blocks only for information another module or user needs.
- Avoid exposing sensitive information in outputs; mark required sensitive outputs with `sensitive = true`.

## Maintainability and Data Sources

- Prioritize readability, clarity, and maintainability over clever HCL.
- Use comments to explain complex configurations and why specific design decisions were made.
- Avoid hard-coded values; use variables and appropriate defaults for configurable inputs.
- Use data sources to retrieve existing up-to-date resources instead of requiring manual IDs.
- Avoid data sources for resources created in the same configuration; use direct references or outputs.
- Remove unnecessary data sources because they slow down `plan` and `apply`.
- Use `locals` for values used multiple times so expressions stay consistent.

## Style, Ordering, and Formatting

- Follow Terraform best practices and the Terraform Style Guide.
- Use descriptive, consistent names for resources, variables, and outputs.
- Use 2 spaces for each indentation level.
- Group related resources in consistent files such as `providers.tf`, `variables.tf`, `network.tf`, `ecs.tf`, and `mariadb.tf`.
- Place `depends_on` blocks at the very beginning of resource definitions and use them only when necessary.
- Place `for_each` and `count` blocks near the beginning of resources, after `depends_on` when present.
- Place `lifecycle` blocks at the end of resource definitions.
- Alphabetize providers, variables, data sources, resources, and outputs within each file when doing so improves navigation.
- Place required attributes before optional attributes, group related attributes, separate logical sections with blank lines, and alphabetize attributes within sections where practical.
- Run `terraform fmt` to format configurations.
- Run `terraform validate` to check syntax and validity.
- Run `tflint` regularly to catch style and best-practice issues early.

## Documentation and Tests

- Include `description` and `type` attributes for variables and outputs.
- Use appropriate types such as `string`, `number`, `bool`, `list`, and `map`.
- Keep comments useful; avoid redundant comments that repeat resource names.
- Include a `README.md` in each project explaining purpose, structure, setup, and usage.
- Use `terraform-docs` to generate documentation when the project expects generated module docs.
- Write Terraform tests with the `.tftest.hcl` extension.
- Cover positive and negative scenarios.
- Keep tests idempotent so they can run repeatedly without side effects.

## Good / Bad Examples

The examples below illustrate typed variables, sensitive outputs, and stable ordering.

**Good:**

```hcl
variable "database_password" {
  description = "Password stored in the configured secret backend."
  sensitive   = true
  type        = string
}
```

Why: The input is typed, documented, and protected from normal plan and apply output.

**Bad:**

```hcl
variable "database_password" {
  default = "Password123!"
}
```

Why: The secret is hardcoded, untyped, undocumented, and likely to leak into version control and state.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep Terraform configurations in version control but never commit secrets or state | Infrastructure history remains reviewable without leaking credentials |
| Store secrets in AWS Secrets Manager or SSM Parameter Store and reference them through environment variables where appropriate | Sensitive values stay out of HCL and state output |
| Use least-privilege IAM, private subnets, security groups, network ACLs, encryption, and TLS | Cloud resources default to secure access patterns |
| Use modules for related resources, not single-resource wrappers or deep hierarchies | Modules reduce duplication without hiding simple infrastructure |
| Use variables, data sources, outputs, and `locals` deliberately | Configurations remain adaptable and readable |
| Put `depends_on`, `for_each`, `count`, and `lifecycle` in consistent positions | Resource behavior is visible during review |
| Run `terraform fmt`, `terraform validate`, and `tflint` | Formatting, syntax, and provider hygiene fail before review |
| Document variables and outputs and test with `.tftest.hcl` | Consumers understand modules and behavior stays idempotent |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use stable Terraform and provider versions | Float blindly to untested provider behavior |
| Mark secrets with `sensitive = true` | Expose passwords, certificates, API keys, or state in version control |
| Use modules for cohesive infrastructure areas | Create circular module dependencies or wrap single resources unnecessarily |
| Use data sources for existing resources | Use data sources for resources created in the same configuration |
| Use `locals` for repeated expressions | Copy-paste repeated computed values |
| Run `trivy`, `tfsec`, or `checkov` for security scanning | Rely on review alone for security vulnerabilities |
| Generate docs with `terraform-docs` when expected | Leave module inputs and outputs unexplained |
| Write idempotent `.tftest.hcl` tests | Ship configurations that cannot be validated repeatedly |

## Checklist Before Opening a PR

- [ ] Terraform and provider versions are stable and compatible with the project.
- [ ] Secrets, AWS credentials, API keys, passwords, certificates, and state are not committed.
- [ ] Sensitive variables and outputs use `sensitive = true`.
- [ ] IAM, security groups, network ACLs, subnet placement, encryption, and TLS follow least-privilege security expectations.
- [ ] Modules encapsulate related resources without circular dependencies or unnecessary nesting.
- [ ] Variables, outputs, data sources, and `locals` are typed, described, and used only where appropriate.
- [ ] Resource block ordering follows `depends_on`, `for_each` / `count`, required attributes, optional attributes, and `lifecycle` conventions.
- [ ] `terraform fmt`, `terraform validate`, `tflint`, and relevant `trivy`, `tfsec`, or `checkov` scans pass.
- [ ] `README.md`, `terraform-docs`, and `.tftest.hcl` coverage are updated where the module requires them.
