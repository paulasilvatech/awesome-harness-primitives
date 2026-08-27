---
name: backstage-upgrade
description: >-
  Plan, execute, and validate Backstage application or plugin dependency upgrades with
  release-aware package alignment, migrations, config review, changesets, and rollback. Use when
  bumping Backstage versions, resolving package skew, adopting new systems, or preparing an
  upgrade PR.
---

<!-- Generated from harness/github-copilot/plugins/backstage-expert/skills/backstage-upgrade/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage upgrade

Upgrade Backstage as a coordinated package and behavior change, not as independent dependency
bumps.

## When to invoke

- "Upgrade this Backstage app."
- "Align mismatched @backstage package versions."
- "Plan an upgrade to the new frontend or backend system."
- "Validate a Backstage version bump."

## Inputs

- Current and target versions.
- Adopter app, plugin package, or Backstage core mode.
- Frontend compatibility mode: `new`, `legacy`, or `dual`.
- Required migration guides and allowed breaking changes.
- Deployment and rollback constraints.

## Procedure

1. Establish a green baseline with current package-local tests and typechecking.
2. Read `backstage.json`, dependency manifests, lockfile policy, config, and current release notes.
3. Select a target version supported by the repository's Node.js and package-manager policy.
4. Present dependency, migration, config, database, and deployment impact before changing versions.
5. Obtain explicit approval for the version change.
6. Use the repository's supported Backstage version-bump workflow instead of editing packages
   independently.
7. Apply required API, config, frontend, backend, database, and plugin migrations in small slices.
8. Keep all `@backstage/*` packages aligned with the target release policy.
9. Run install integrity, config validation, typecheck, targeted tests, package builds, and app
   startup checks.
10. For published packages, add direct changeset files according to repository policy.
11. Document rollback to the previous manifest and lockfile state plus any irreversible database
   migration caveats.

## Limits

- Do not use Backstage core release commands in an adopter application.
- Do not run `yarn release` or `changeset version` as routine Backstage core validation.
- Do not combine a broad frontend migration with an unrelated dependency upgrade without an
  explicit plan.

## Output template

```markdown
## Backstage upgrade result

**From:** <version>
**To:** <version>
**Mode:** adopter | plugin | core
**Frontend:** new | legacy | dual | not applicable

| Migration area | Change | Validation | Result |
| --- | --- | --- | --- |

### Rollback
- <steps and irreversible caveats>
```

## Quality gate

- [ ] Current and target versions are evidenced from first-party release information.
- [ ] Baseline validation passed before version edits.
- [ ] The version change was explicitly approved.
- [ ] Backstage package versions and lockfile remain aligned.
- [ ] Required config, API, database, frontend, and backend migrations are complete.
- [ ] Tests, typecheck, config validation, builds, and startup checks are recorded.
- [ ] Rollback and changeset requirements are documented.
