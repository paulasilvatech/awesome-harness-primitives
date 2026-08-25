---
name: backstage-software-templates
description: "Design, implement, validate, and troubleshoot Backstage Software Templates, custom actions, Golden Paths, skeleton rendering, repository publication, and catalog registration. Use when working with template.yaml, scaffolder actions, parameters, step outputs, or template execution failures."
---

# Backstage Software Templates

Build self-service workflows with typed inputs, explicit effects, deterministic skeletons, and
visible outputs.

## When to invoke

- "Create a Golden Path template."
- "Add or test a custom scaffolder action."
- "Fix a broken template step output."
- "Publish a generated repository and register it in the catalog."

## Procedure

1. Detect Backstage version, installed scaffolder modules, available actions, and template
   conventions.
2. Define the user outcome, owner, generated component type, external effects, and rollback.
3. Model parameters with types, validation, required fields, pickers, and safe defaults.
4. Use stable step IDs and camelCase custom action IDs. Do not use kebab-case custom action IDs
   because step-output expressions can fail.
5. Render a minimal skeleton with explicit values and no embedded credentials.
6. Keep repository publication, workflow dispatch, infrastructure provisioning, and catalog
   registration as separate visible steps.
7. Add typed custom action schemas, input validation, permissions, dry-run behavior, and tests.
8. Render the template with representative inputs and inspect every generated file.
9. Require approval before creating repositories, dispatching provisioning, deploying, or
   incurring cost.
10. Validate catalog registration and return links or entity references in template outputs.

## Failure handling

- Stop on unknown actions, missing integrations, unresolved step outputs, invalid repository
  hosts, or ambiguous ownership.
- Do not report success when publication succeeded but catalog registration failed.
- Preserve the task log needed for diagnosis while redacting secrets.

## Output template

```markdown
## Software Template result

**Template:** <name>
**Effects:** <repositories, workflows, infrastructure, catalog>

| Step | Action | Validation | Result |
| --- | --- | --- | --- |

### Approval-gated actions
- <action and status>
```

## Quality gate

- [ ] Parameters, required fields, validation, and defaults are intentional.
- [ ] Custom action IDs use camelCase and step-output references resolve.
- [ ] Skeleton rendering is tested with representative inputs.
- [ ] External effects are visible, least-privilege, and approval-gated.
- [ ] Catalog registration and result links are validated.
- [ ] Generated content contains no secrets or unresolved template expressions.
