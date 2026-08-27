---
name: open-horizons-backstage-app-configuration
description: >-
  Design, edit, validate, and troubleshoot Backstage app configuration, environment overlays,
  schemas, secrets, integrations, and frontend visibility. Use when working with app-config YAML,
  BACKSTAGE_ENV, config:check, deployment overrides, or configuration errors.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-app-configuration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage app configuration

Manage Backstage configuration as a layered, schema-validated contract rather than a collection of
untracked environment values.

## When to invoke

- "Configure app-config.production.yaml."
- "Why is this Backstage config key not loading?"
- "Add an integration without committing its secret."
- "Validate Backstage config before deployment."

## Configuration model

- `app-config.yaml` holds shared defaults.
- Additional `app-config.<environment>.yaml` files or explicit config arguments provide overrides.
- `BACKSTAGE_ENV` selects the conventional environment-specific config layer when supported by the
  target repository.
- Environment variables and approved secret providers supply sensitive values.
- Frontend-visible configuration is bundled into the browser and must never contain secrets.

## Procedure

1. Detect repository mode, Backstage version, launch command, and actual config load order.
2. Inventory config files, environment selection, schemas, and `${ENV_VAR}` references.
3. Classify each requested value as shared default, environment override, secret, or
   frontend-visible configuration.
4. Update the smallest config layer and matching schema or documentation.
5. Preserve integration boundaries and avoid duplicating the same key in unrelated layers.
6. Run the repository's current equivalent of:

   ```bash
   yarn backstage-cli config:check
   ```

7. If startup still fails, inspect the effective config and error without printing secret values.
8. Report the resolved layer, schema result, required environment names, and deployment handoff.

## Gotchas

- Later config layers override earlier values; they do not merge every nested shape identically.
- A valid YAML document can still fail Backstage schema validation.
- Config available to the frontend is public to browser users.
- Sign-in credentials and GitHub integration credentials have different purposes.

## Open Horizons integration

- Scope configuration changes to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Backstage ownership, managed-identity, AKS, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage configuration result

**Environment:** <name>
**Load order:** <files and selectors>

| Key family | Source | Visibility | Validation |
| --- | --- | --- | --- |

### Required external values
- `<ENV_NAME>`: <purpose, not value>
```

## Quality gate

- [ ] Config load order and target environment are evidenced.
- [ ] Secrets remain external and are not printed.
- [ ] Frontend-visible values contain no credentials.
- [ ] Changed keys are covered by current schemas.
- [ ] `config:check` or the repository equivalent passes.
- [ ] Deployment-specific overrides are documented.
