---
description: "Apply Backstage Software Template schema, action, output, and safety conventions. Use when editing template YAML or template skeletons."
applyTo: "**/template.yaml,**/template.yml,templates/**,examples/template/**"
---

# Backstage Software Template Conventions

These instructions apply to Backstage Software Templates and their skeletons. They are
authoritative for parameter contracts, action IDs, step outputs, publication safety, and catalog
registration in matched files; repository-specific actions and policy win on conflict.

## Template Contracts

- Use `scaffolder.backstage.io/v1beta3` unless the installed version and repository require
  another supported API.
- Give parameters explicit types, validation, required fields, and safe defaults.
- Use stable camelCase custom action IDs. Kebab-case custom action IDs can break step-output
  expressions.
- Reference step outputs by stable step IDs and validate conditional steps.
- Keep repository publication, infrastructure provisioning, and catalog registration explicit.

## Safety and Permissions

- Validate repository hosts, owners, and destinations before publish actions.
- Keep credentials in integrations or secret providers, never template values.
- Require approval before actions that create repositories, deploy infrastructure, or incur cost.
- Make generated ownership and lifecycle values visible to the user.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep template steps idempotent where possible. | Retries should not duplicate resources. |
| Register generated components explicitly. | Templates should complete the catalog feedback loop. |
| Test custom actions with typed inputs and dry-run behavior. | Shell and network actions are high-risk boundaries. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Validate both template YAML and rendered skeleton output. | Validate only the outer YAML. |
| Use typed custom actions. | Shell out with unvalidated user input. |
| Expose links and entity refs in outputs. | Hide created resources from the result. |

## Checklist Before Opening a PR

- [ ] Parameters, validation, required fields, and defaults are intentional.
- [ ] Custom action IDs use camelCase and step-output references resolve.
- [ ] Publish, provision, and registration effects are approval-gated.
- [ ] Skeleton rendering and template validation pass.
- [ ] Generated files contain no secrets or unresolved placeholders.

## References

- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/)
- [Writing custom actions](https://backstage.io/docs/features/software-templates/writing-custom-actions/)
