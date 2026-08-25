---
applyTo: "backstage/examples/template/**,backstage/examples/demo-template.yaml,docs/aeg-feature-scaffold/backstage/**/template.yaml,docs/aeg-feature-scaffold/backstage/**/skeleton/**,scripts/golden-paths/**/skeleton/**"
description: "Use when editing Backstage Software Templates or generated skeletons that require safe, portable scaffolding."
---

# Backstage Software Templates

## Conventions

- Keep template metadata, ownership, lifecycle, parameters, steps, and outputs valid for the installed scaffolder version.
- Use stable action IDs and reference prior step output with explicit expressions; do not rely on implicit ordering or undocumented fields.
- Validate repository, owner, branch, environment, and destination inputs before actions that publish or mutate external systems.
- Never request or render secrets into generated files, task logs, URLs, or catalog entities.
- Keep skeletons runnable after rendering: remove authoring placeholders, preserve executable bits where required, and use portable relative paths.
- Point generated catalog locations and source annotations at the repository actually created by the template.
- Keep `scripts/golden-paths/` as the repository source for Golden Path skeletons; do not claim a root `golden-paths/` tree exists.
- Make optional features explicit in parameters and ensure omitted options do not leave invalid configuration.

## Verification

- Template linting accepts the schema and referenced action IDs.
- Representative rendering leaves no unresolved template tokens or sensitive values.
- Generated manifests and package files pass their owning domain checks.
