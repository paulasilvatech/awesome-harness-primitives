# Dynamic Plugin Strategy

Backstage core plugin development and dynamic plugin packaging are separate concerns.

## Rules

- Keep dynamic loading runtime-neutral unless the user names a specific runtime.
- For generic Backstage, first build a correct package and app integration.
- For dynamic loading, document the target runtime, packaging format, loader, and compatibility constraints.
- Keep dynamic packaging as a deployment strategy, not as the architecture of the plugin itself.

## Strategy Questions

- Is the target an internal Backstage app, a private package, or a dynamic runtime?
- Does the runtime support frontend, backend, or both dynamically?
- What package format is accepted?
- Who owns compatibility testing after Backstage upgrades?
- How are configs, secrets, and permissions supplied?

## Out Of Scope

Vendor-specific dynamic plugin packaging belongs in a runtime-specific skill or implementation guide. This skill should first produce a correct Backstage plugin package, then document the runtime-neutral packaging requirements and handoff points.
