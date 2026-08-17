---
name: "iac-review"
description: "Use when reviewing Terraform, Bicep, or CloudFormation, checking drift, or hardening infrastructure code. Triggers include \"review terraform\", \"review bicep\", \"IaC review\", \"drift detection\", and \"state file\"."
---
# IaC review

## When to invoke

- "Review this Terraform module."
- "Why does our plan show drift?"
- "Is this Bicep ready for production?"

## Review checklist

### Structure

- [ ] Modules are **composable** and have a single responsibility (one module = one logical stack, not one resource).
- [ ] **No hard-coded values**: parameterize everything with sensible defaults.
- [ ] **Documented inputs** (`description`, `type`, and `validation` rules) and outputs.
- [ ] A **README** at the module root with a usage example.

### State and backends

- [ ] **Remote state** with locking (S3+DynamoDB, Azure Storage with a blob lease, GCS).
- [ ] State is **never committed** to Git; `.gitignore` covers `*.tfstate*`.
- [ ] State is separated by environment, with no implicit coupling between environments.
- [ ] IAM controls state access, not shared credentials.

### Security

- [ ] No secrets in code or variable defaults. Use Key Vault / Secrets Manager / SOPS.
- [ ] IAM follows least privilege, with no `*:*` or `Resource: "*"` unless justified.
- [ ] Encryption at rest and in transit is enabled for all data stores.
- [ ] Public access is explicitly denied unless intentional. Document intentional access in the module README.
- [ ] `tfsec` / `checkov` / `PSRule` report no findings, or exceptions are documented.

### Change safety

- [ ] `terraform plan` is included in PRs as a comment (Atlantis / tfcmt / GH Actions).
- [ ] `prevent_destroy` is set on stateful resources (databases, KV, storage accounts).
- [ ] Provider versions are **pinned** (`~>` with explicit major and minor versions).
- [ ] Module versions are pinned.
- [ ] Destructive diffs require a second approver.

### Drift

- [ ] Scheduled drift detection (`terraform plan -detailed-exitcode` daily, or Driftctl).
- [ ] Drift automatically creates a ticket and never remains silent.
- [ ] No manual console changes without subsequently codifying them.

## Common findings

- **`count` used for lists that can reorder** → use `for_each` with stable keys.
- **`depends_on` everywhere** → usually signals missing implicit dependencies; remove it unless truly necessary.
- **Data sources used for values available at plan time** → unnecessary API calls and unstable CI.
- **Environment differences through `terraform.workspace` string interpolation** → fragile; use tfvars or separate stacks.

## Output template

```markdown
## IaC review - <module or stack>

| Area | Finding | Severity | Recommendation |
|---|---|---|---|
| State | Local state, no locking | High | Move to a remote backend with locking |
| Security | Storage account allows public access | High | Set public_network_access_enabled = false |
| Change safety | Provider version unpinned | Medium | Pin with ~> major.minor |

**Blocking findings**: <count>
**Verdict**: approve / request changes
```

## Quality gate

- [ ] `terraform fmt` and `terraform validate` pass, and the plan is attached to the PR.
- [ ] No secrets appear in code, variables, or state; secrets use Key Vault or Secrets Manager.
- [ ] Provider and module versions are pinned; stateful resources set `prevent_destroy`.
- [ ] `tfsec` or `checkov` reports no findings, or every exception is documented.
- [ ] Every resource carries `project`, `environment`, and `owner` tags.

## References

- [Terraform Style Guide](https://developer.hashicorp.com/terraform/language/style)
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
- [tfsec](https://aquasecurity.github.io/tfsec/), [checkov](https://www.checkov.io/)
