---
name: open-horizons-backstage-framework
description: >-
  Choose and implement Backstage framework extension points, core backend services, frontend
  blueprints, service refs, modules, lifecycle, auth, permissions, schedulers, tracing, metrics,
  and generated API references. Use when designing plugin architecture or selecting supported
  framework APIs.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-framework/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage framework

Choose public services and extension points from the target Backstage version instead of coupling
plugins to implementation internals.

## When to invoke

- "Which Backstage core service should this plugin use?"
- "Create a backend module for an extension point."
- "Use a frontend blueprint or service ref."
- "Find the supported API in the generated framework reference."

## Procedure

1. Confirm Backstage version, adopter or core mode, frontend mode, and plugin boundary.
2. Start from the generated framework index and stable API documentation for that exact release.
3. Map the requirement to:
   - a core backend service,
   - a plugin-specific extension point,
   - a frontend blueprint or utility API,
   - an app module,
   - or a separate plugin boundary.
4. Prefer `coreServices` and public service refs for config, logging, URL reading, databases,
   discovery, auth, HTTP auth, lifecycle, health, schedulers, metrics, tracing, and user info.
5. Use `createBackendModule` only to extend one plugin through an exported extension point.
6. Keep service dependencies explicit in registration and inject test doubles in unit tests.
7. Treat alpha APIs as version-sensitive and document the exact target version.
8. Validate startup ordering, lifecycle cleanup, permission and auth propagation, scheduled-task
   uniqueness, and error handling.

## Open Horizons integration

- Scope framework decisions to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Backstage ownership, platform compatibility, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage framework decision

**Backstage version:** <version>

| Requirement | Public API | Stability | Package | Test strategy |
| --- | --- | --- | --- | --- |

### Rejected coupling
- <internal API or boundary and reason>
```

## Quality gate

- [ ] The selected API exists in the target release's generated reference.
- [ ] Core services and extension points replace internal imports.
- [ ] Alpha or deprecated APIs are clearly labeled.
- [ ] Lifecycle, auth, permissions, scheduler, and observability behavior is covered.
- [ ] Service dependencies are injectable and unit tested.
- [ ] Package boundaries contain no cycles or app-specific leakage.

## References

- [Backstage framework index](https://backstage.io/docs/framework/generated-index)
- [Stable API reference](https://backstage.io/api/stable)
- [Core backend service APIs](https://backstage.io/docs/backend-system/core-services/)
