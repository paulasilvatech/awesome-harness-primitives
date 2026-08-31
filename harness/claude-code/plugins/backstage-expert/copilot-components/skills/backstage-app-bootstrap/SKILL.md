---
name: backstage-app-bootstrap
description: "Create or assess a standalone Backstage adopter application with version-aware prerequisites, package layout, first-run configuration, and baseline validation. Use when starting a Backstage app, reinstalling an app shell, or checking whether a repository is a valid adopter app."
---

# Backstage app bootstrap

Create the smallest viable Backstage adopter application while preserving an existing repository
and keeping app creation approval-gated.

## When to invoke

- "Create a new Backstage app."
- "Bootstrap an internal developer portal with Backstage."
- "Validate this freshly generated Backstage repository."
- "Set up the Backstage app and backend packages."

## Inputs

- Target directory and whether it must be empty.
- Package scope and app name.
- Target Backstage release policy.
- Package manager and supported Node.js version.
- Development database and initial sign-in mode.

## Procedure

1. Confirm the target is an adopter app, not `backstage/backstage`, Open Horizons, or RHDH.
2. Read the current official getting-started page and record the verification date.
3. Inspect the destination for existing files, symlinks, or unrelated work.
4. Present the exact create-app command, destination, network downloads, and files it will create.
5. Obtain explicit approval before running `@backstage/create-app`.
6. Run the current official scaffolder command without embedding credentials.
7. Inspect `backstage.json`, root scripts, `packages/app`, `packages/backend`, and config layers.
8. Run the generated repository's existing install, typecheck, test, and start validation as
   applicable. Do not invent replacement scripts.
9. Record the generated Backstage version, Node.js requirement, package manager, config files, and
   next authentication or catalog steps.

## Safety

- Dry-run the destination assessment before app creation.
- Never scaffold over a non-empty directory without explicit user approval.
- Do not use the Backstage core contributor workflow for an adopter app.
- Keep production credentials and provider secrets out of generated files.

## Output template

```markdown
## Backstage bootstrap result

**Status:** planned | created | validated | blocked
**Destination:** <path>
**Backstage version:** <version and source>

| Check | Result |
| --- | --- |

### Next configuration
- <auth, catalog, database, or deployment step>
```

## Quality gate

- [ ] The target is positively identified as an adopter application.
- [ ] Current first-party create-app guidance was checked.
- [ ] The destination and network effects were approved before scaffolding.
- [ ] Generated package and config layout was inspected.
- [ ] Existing validation commands ran or the blocker is explicit.
- [ ] No credentials or unrelated files were overwritten.
