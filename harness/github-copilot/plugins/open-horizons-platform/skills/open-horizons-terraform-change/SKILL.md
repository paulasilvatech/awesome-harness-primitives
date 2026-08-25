---
name: open-horizons-terraform-change
description: >-
  Implements and validates one bounded Open Horizons Terraform change in terraform/modules or an isolated terraform/environments root. Use when changing a module, environment root, provider constraint, backend declaration, import block, or state-aware Terraform contract without applying infrastructure.
argument-hint: "<module or environment root> <requested Terraform change>"
---

# Open Horizons Terraform change

Make one reviewable Terraform change while preserving provider, backend, import, and state boundaries.

## When to invoke

- Add, repair, or refactor a module under `terraform/modules/`.
- Change one isolated root under `terraform/environments/`.
- Update provider constraints, imports, variables, outputs, or module wiring.
- Prepare validation evidence or an explicitly approved remote plan without applying it.

## Inputs

Use `$ARGUMENTS` to identify the target module or environment root and requested behavior. Require
acceptance criteria, expected deployment context, and any known state or import relationship.
Require exact approval before a plan may contact a remote backend or provider API.

## Procedure

1. Resolve the smallest owning path. Classify it as a reusable module or one isolated environment
   root; do not silently widen work to the guarded greenfield root at `terraform/`.
2. Read the target's `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, callers, nearest
   `.terraform.lock.hcl`, backend declaration, import or moved blocks, and corresponding tests.
3. Record the Terraform version constraint, provider constraints, lock-file owner, backend mode,
   state owner, imported addresses, and whether any resource address could change.
4. Prefer an existing module and its public inputs or outputs over duplicating resources. Keep
   secrets outside Terraform source and variable files.
5. Preserve checked-in provider selections. Use `-lockfile=readonly` when the resolved root owns a
   lock file; never regenerate a lock file unless the requested change explicitly changes provider
   dependencies.
6. Treat backend, import, and address changes as state-sensitive. Use declarative `import` or
   `moved` blocks only when the requested adoption or address transition is explicit and reviewable;
   never mutate state to make configuration appear valid.
7. Format the bounded path, initialize only the resolved root with the backend disabled, and
   validate it:

   ```bash
   terraform fmt -check -recursive <target>
   terraform -chdir=<resolved-root> init -backend=false -input=false -lockfile=readonly
   terraform -chdir=<resolved-root> validate
   ```

   If the resolved root has no checked-in lock file, omit `-lockfile=readonly`, explain why, and do
   not commit an incidental lock file.
8. Select `terratest-module-testing` mode: `static` by default, `plan` only when plan behavior is
   acceptance-critical, or `integration` only through that skill's complete approval gate.
9. Run a remote plan only after approval names the exact root, environment, backend or state,
   variable inputs, command, and allowed network context. Save a plan only when requested; do not
   print secrets or treat the plan as deployment approval.
10. Report changed paths, versions, backend and state risk, validation, optional saved-plan
    identity, and security or deployment handoffs.

## Saved-plan identity

When a saved plan is approved, record its repository-relative path, SHA-256 digest, resolved root,
Terraform version, creation timestamp, sanitized command, target environment, and backend/state
identity. Never commit the plan or expose variable values embedded in it.

## Output template

```markdown
## Terraform change result

**Status:** completed | blocked
**Scope:** <module or isolated environment root>
**Terraform/provider versions:** <constraints and lock owner>
**Backend/state risk:** none | low | high - <reason>

### Changes
- `<path>`: <bounded behavior>

### Validation
| Command or check | Result | Evidence |
| --- | --- | --- |

### Saved plan
- Identity: <path, digest, root, environment, version, timestamp, or not created>

### Handoffs
- Security review: <required and reason | not required>
- Deployment operation: <immutable package needed | not requested>
```

## Limits

- Never run `terraform apply`, `destroy`, `state`, `force-unlock`, or `init -upgrade`.
- Never migrate a backend or state, import through a state command, or substitute a live workspace.
- Never infer remote-plan approval from a dry run, issue label, previous plan, or test result.
- Do not combine unrelated modules or environment roots into one change.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `terraform-cli` | `skill` | Exact safe Terraform CLI syntax or diagnostic handling is needed. |
| `terratest-module-testing` | `skill` | Tests must be created, repaired, or run in a selected mode. |
| `open-horizons-azure-readiness` | `skill` | Current Azure prerequisites require read-only assessment. |
| `open-horizons-security-reviewer` | `agent` | Identity, exposure, secrets, policy, or state risk needs independent review. |
| `open-horizons-deployment-operation` | `skill` | An immutable approved plan is ready for a separate deployment owner. |

## Quality gate

- [ ] The exact root or module, callers, version, lock, backend, import, and state boundaries are known.
- [ ] Existing modules and public contracts were preferred over duplicate infrastructure.
- [ ] Formatting, backend-disabled initialization, validation, and the selected Terratest mode are evidenced.
- [ ] Any remote plan had exact approval and any saved plan has a sanitized immutable identity.
- [ ] No apply, destroy, state mutation, backend migration, force unlock, or provider upgrade ran.
- [ ] Security and deployment handoffs are explicit.
