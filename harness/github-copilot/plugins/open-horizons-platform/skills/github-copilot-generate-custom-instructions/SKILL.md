---
name: github-copilot-generate-custom-instructions
description: >-
  Generates path-scoped GitHub Copilot migration instructions from actual branch, commit, tag, or release diffs. Use when handling framework upgrades, architecture refactors, technology migrations, dependency updates, API changes, and obsolete-pattern prevention.
argument-hint: "MIGRATION_TYPE=<type> SOURCE_REFERENCE=<ref> TARGET_REFERENCE=<ref>"
---

# Generate custom instructions from codebase

Extract deterministic before/after rules from real repository history and write a scoped `.instructions.md` file.

## When to invoke

- Preserve conventions established by an upgrade or refactor.
- Generate API correspondence guidance from a migration diff.
- Prevent reintroduction of obsolete patterns.
- Encode repeatable dependency or configuration transformations.

## Inputs

Parse `$ARGUMENTS` and require `MIGRATION_TYPE`, `SOURCE_REFERENCE`, and `TARGET_REFERENCE`.

| Input | Allowed values or purpose |
| --- | --- |
| `MIGRATION_TYPE` | Framework Version, Architecture Refactoring, Technology Migration, Dependencies Update, Pattern Changes |
| `SOURCE_REFERENCE` | Before branch, commit, tag, or release |
| `TARGET_REFERENCE` | After branch, commit, tag, or release |
| `ANALYSIS_SCOPE` | Entire project, specific folder, or modified files only |
| `CHANGE_FOCUS` | Breaking changes, conventions, obsolete patterns, APIs, configuration |
| `AUTOMATION_LEVEL` | Conservative, Balanced, or Aggressive |
| `GENERATE_EXAMPLES` | true or false |
| `VALIDATION_REQUIRED` | true or false |

## Procedure

1. Resolve source and target references to immutable commits and record them.
2. Compare structure, moved/deleted files, configuration, dependencies, source, and tests in scope.
3. Group repeated transformations by migration type and focus.
4. Create an automatic rule only when the old pattern has a reliable trigger and the replacement is deterministic.
5. Put ambiguous transformations under validation with concrete tests or compatibility checks.
6. Build API correspondences from actual old/new symbols and examples.
7. Escalate complex cases, architecture decisions, security changes, and business impact for human review.
8. Write `.github/instructions/<migration-slug>.instructions.md` with a narrow `applyTo` glob.
9. Test the instructions against representative source and target examples.

Transformation shape:

```text
BEFORE (<SOURCE_REFERENCE>)
<old code from repository>

AFTER (<TARGET_REFERENCE>)
<new code from repository>

RULE
When <reliable trigger> appears under <applyTo>, use <new pattern> and run <validation>.
```

## Output template

```markdown
## Copilot migration instructions result

**Status:** GENERATED | VALIDATION-REQUIRED | BLOCKED
**References:** <source SHA> -> <target SHA>
**Output:** `.github/instructions/<slug>.instructions.md`

| Rule | Evidence | Automation | Validation |
| --- | --- | --- | --- |

### Escalations
- <complex case, architecture decision, security/business impact, or none>
```

## Limits

- Do not generate rules from generic migration advice or memory.
- Do not automate a transformation without a reliable trigger and deterministic replacement.
- Do not hide exceptions or force architecture/business decisions into mechanical rules.
- Do not write the unsupported `.github/copilot-migration-instructions.md` path.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `brownfield-engineering` | `skill` | The migration rules guide implementation in existing code. |
| `context-map` | `skill` | The changed surface and dependencies need mapping first. |
| `validation-scripts` | `skill` | Generated instructions need repository-level validation. |

## Quality gate

- [ ] Source and target resolve to immutable commits.
- [ ] Every rule cites actual before/after evidence.
- [ ] Automatic replacements are deterministic and scoped.
- [ ] Validation-required changes name concrete checks.
- [ ] Architecture, security, and business-impact decisions are escalated.
- [ ] The generated instruction has a narrow `applyTo` and passes primitive validation.