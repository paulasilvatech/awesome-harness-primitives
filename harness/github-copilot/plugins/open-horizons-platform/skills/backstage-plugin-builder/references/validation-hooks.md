# Plugin Validation

Use this reference to run repository-native and package-local safety gates around Backstage plugin development.

## Standard Commands

Run what exists from the target plugin package directory:

```bash
yarn lint
yarn tsc
yarn test
yarn build
```

For publication preparation:

```bash
npm pack --dry-run
```

Do not run `yarn build` from the root of `backstage/backstage`. For core contributions, use targeted tests, exact root `yarn tsc`, changed-file formatting, `yarn lint --fix`, and `yarn build:api-reports` when the change requires API report updates.

## Repository Integration

- Reuse existing CI and repository task definitions instead of generating Git hooks.
- Do not change `core.hooksPath` or install a pre-commit hook as part of plugin scaffolding.
- Run only scripts declared by the target package and report skipped scripts explicitly.
- Keep network publication separate from validation.
- Treat CI as the source of truth for publication readiness.
