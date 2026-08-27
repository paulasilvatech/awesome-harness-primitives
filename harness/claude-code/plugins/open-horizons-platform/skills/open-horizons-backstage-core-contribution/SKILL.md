---
name: open-horizons-backstage-core-contribution
description: >-
  Prepare, implement, validate, and document contributions to backstage/backstage or a close fork
  using targeted tests, exact root typechecking, formatting, linting, API reports, changesets,
  DCO, and Apache headers. Use when changing Backstage core packages, plugins, docs, or
  contributor workflows.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-core-contribution/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage core contribution

Follow the upstream repository's contributor contract and avoid commands that perform broad build
or release mutation.

## When to invoke

- "Make a change in backstage/backstage."
- "Validate this Backstage core PR."
- "Add a changeset or update API reports."
- "Fix a core plugin, package, or documentation issue."

## Positive detection

Use this skill only when repository evidence identifies `backstage/backstage` or a close fork with
the core package layout. Adopter apps use their own package scripts instead.

## Procedure

1. Read root `package.json`, `CONTRIBUTING.md`, `SECURITY.md`, package ownership, and affected
   package scripts.
2. Verify the exact checkout commit and Backstage version.
3. Establish a targeted baseline:

   ```bash
   yarn install
   CI=1 yarn test <path>
   yarn tsc
   ```

4. Make the smallest package-scoped change and preserve public API and compatibility contracts.
5. Format only changed files and run `yarn lint --fix` according to contributor guidance.
6. Rerun targeted tests and exact root `yarn tsc` without extra options.
7. Run `yarn build:api-reports` when public APIs change and review generated report diffs.
8. Add direct changeset files when published packages change.
9. Preserve Apache-2.0 headers, DCO sign-off, documentation, and test expectations.
10. Review the final diff for unrelated generated output or release mutations.

## Prohibited routine commands

- Root `yarn build`.
- `yarn release`.
- `changeset version` or equivalent version mutation.
- Repository-wide formatting when only changed files are required.
- Untargeted test suites when a package or path selector covers the change.

## Open Horizons integration

- Scope core contributions to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Backstage ownership, compatibility, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage core contribution result

**Commit:** <checkout commit>
**Packages:** <affected packages>

| Contributor gate | Command | Result |
| --- | --- | --- |

### Generated artifacts
- Changeset:
- API reports:
- Documentation:
```

## Quality gate

- [ ] Repository identity, commit, and affected package ownership are confirmed.
- [ ] Baseline and final targeted tests pass.
- [ ] Root typecheck ran only as exact `yarn tsc`.
- [ ] Formatting is limited to changed files and lint results are recorded.
- [ ] API reports and direct changesets are updated when required.
- [ ] DCO and Apache header requirements are satisfied.
- [ ] No root build, release, or changeset-version command ran.
