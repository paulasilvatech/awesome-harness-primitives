---
name: "backstage-change"
description: "Implement and validate a focused Backstage change after detecting repository mode, version, frontend compatibility, and approval-gated effects."
argument-hint: "goal=<requested change> frontend_mode=new|legacy|dual|not-applicable"
agent: "backstage-expert"
tools: ["read", "search", "edit", "execute", "web"]
---

# /backstage-change

## Objective

Implement `${input:goal:the requested Backstage change}` with frontend mode
`${input:frontend_mode:new, legacy, dual, or not-applicable}` and return changed paths plus
validation evidence.

## When to Invoke

Use after the requested Backstage behavior and write scope are clear and the team wants an
implementation rather than a read-only assessment.

## Preconditions

- The active workspace is a positively identified Backstage repository.
- The goal and writable scope are explicit.
- Frontend mode is selected when frontend code is involved.
- Approval is available before app creation, version changes, identity changes, publication,
  deployment, release, or destructive data operations.

If a precondition is not met, report it and stop before changing files.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Goal | `${input:goal}` | Yes | Use as the exact implementation boundary. |
| Frontend mode | `${input:frontend_mode}` | Yes | Accept `new`, `legacy`, `dual`, or `not-applicable`; never infer compatibility. |
| Repository context | Active workspace | Yes | Detect mode, version, config, scripts, and protected files. |
| Selected context | `${selection}` | No | Treat empty selection as absent. |

## What I Will Do

- Detect repository mode and Backstage version before editing.
- Select the narrowest installed Backstage skill for the goal.
- Verify version-sensitive APIs against first-party evidence.
- Make focused changes and run package-local or repository-approved validation.
- Report exact changed paths, checks, approvals, and remaining blockers.

## What I Will NOT Do

- Apply Open Horizons or RHDH assumptions to a generic repository.
- Run Backstage core root build, release, or changeset-version commands as routine validation.
- Commit secrets, print provider credentials, or bypass permission policy.
- Perform approval-gated operations without explicit approval.
- Modify files outside the requested Backstage scope.

## Output Format

```markdown
## Backstage change result

**Mode:** adopter | core | legacy | dual | open-horizons | rhdh
**Version:** <version and evidence>
**Frontend mode:** new | legacy | dual | not-applicable

### Changed files
| Path | Purpose |
| --- | --- |

### Validation
| Check | Result |
| --- | --- |

### Approval-gated operations
- <operation and status>

### Follow-up
- <remaining action or None>
```

## Definition of Done

- [ ] Repository mode, version, and frontend compatibility are explicit.
- [ ] Only requested Backstage files and behavior changed.
- [ ] Approval-gated operations are approved or remain unexecuted.
- [ ] Version-sensitive APIs cite first-party evidence.
- [ ] Relevant validation passed or failures are reported accurately.
- [ ] The final diff contains no secrets, placeholders, or unrelated edits.

## Prompt Body

Follow these steps in order:

1. **Validate the request.** Confirm `${input:goal}`, repository mode, Backstage version, writable
   scope, and `${input:frontend_mode}`.
2. **Select the procedure.** Use the narrowest Backstage skill for the requested subsystem and
   inspect only required files.
3. **Check current APIs.** Verify version-sensitive behavior against first-party sources.
4. **Gate side effects.** Stop for approval before app creation, version or production identity
   changes, publication, deployment, release, or destructive data actions.
5. **Implement.** Make the smallest complete change while preserving package, config, auth,
   permission, and compatibility boundaries.
6. **Validate.** Run package-local or repository-approved checks. In Backstage core, do not run
   root `yarn build`, release, or changeset-version commands.
7. **Report.** Use the required output format with changed paths, exact results, approvals, and
   remaining work.

## Invocation Example

1. Run **Chat: Run Prompt** and select `/backstage-change`.
2. Enter `Install and configure MCP Actions for read-only Catalog tools` for goal.
3. Enter `not-applicable` for frontend mode.
4. Review approval prompts and verify only scoped files changed.

## Related Primitives

- `backstage-expert` (agent): owns mode detection and Backstage decisions.
- `backstage-assess` (prompt): performs a read-only assessment before implementation.
