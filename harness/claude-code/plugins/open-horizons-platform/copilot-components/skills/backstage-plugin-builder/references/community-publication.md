# Community Publication

Use this when the user wants to publish or contribute a plugin to the official Backstage community ecosystem.

## Important Limit

This skill can prepare a plugin package, issue, PR plan, metadata, docs, tests, and checklist. It cannot guarantee acceptance. Official publication depends on community maintainer review.

## Official Direction

The `backstage/community-plugins` repository is designed as a collaborative space for Backstage community members to host and manage plugins. Contributing there means following its guidelines and standardized release process.

## Readiness Checklist

- Plugin is generic and useful beyond one company.
- Existing community plugins were checked for overlap.
- Package names follow Backstage conventions.
- README explains purpose, setup, config, permissions, and screenshots when UI exists.
- `catalog-info.yaml` exists and is accurate.
- License is present.
- Tests, lint, typecheck, and build pass.
- No secrets, internal URLs, customer names, or private data are present.
- Maintainer expectations are documented.

## Suggested Flow

1. Search existing plugins and issues.
2. Open an issue or discussion describing the plugin and intended ownership.
3. Prepare the package in a fork or branch.
4. Run validation.
5. Open a PR following the repository's contributing guide.
6. Iterate with maintainers.
