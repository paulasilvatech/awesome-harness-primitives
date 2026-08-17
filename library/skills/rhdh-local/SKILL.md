---
name: rhdh-local
description: "Test Red Hat Developer Hub plugins locally with rhdh-local-setup. Use for enabling or disabling plugins, switching customized and pristine modes, running local plugin tests, starting or stopping RHDH, health checks, backup and restore, environment variables, 504 errors, startup failures, and local troubleshooting."
---

# RHDH Local

Use this skill for local Red Hat Developer Hub testing through the `rhdh-local-setup` customization system.

## First Step

Identify the requested local action. Ask only if the plugin name, package reference, or target mode is missing. If the user clearly asks to start, stop, check health, or inspect status, run the matching command.

## Operating Principles

- Edit configuration only under `rhdh-customizations/`, never directly in `rhdh-local/`.
- After every configuration edit, run `rhdh local apply` to sync generated copies.
- Use `rhdh local up` and `rhdh local down`. Do not bypass the tool with direct `podman compose` commands when Lightspeed or Orchestrator shared-network services are enabled.
- Fetch plugin package definitions from `rhdh-plugin-export-overlays` metadata. Use `spec.dynamicArtifact`; do not construct OCI URLs manually.
- Auth errors from plugin APIs can be expected in local tests without real credentials. Treat successful plugin load plus attempted API calls as a useful smoke-test signal.

## Routing

| User intent | Action |
| --- | --- |
| Enable, add, install plugin | Read [workflows/enable-plugin.md](workflows/enable-plugin.md). |
| Disable, remove, turn off plugin | Read [workflows/disable-plugin.md](workflows/disable-plugin.md). |
| Switch mode, pristine, customized | Read [workflows/switch-mode.md](workflows/switch-mode.md). |
| Test, verify, check plugin | Read [workflows/test-plugin.md](workflows/test-plugin.md). |
| Status, list plugins, show enabled plugins | Inspect `rhdh-customizations/configs/dynamic-plugins/dynamic-plugins.override.yaml`. |
| Start, up, start RHDH | Run `rhdh local up`, adding `--lightspeed`, `--orchestrator`, or `--both` when requested. |
| Stop, down, stop RHDH | Run `rhdh local down`. |
| Health, check health, is RHDH running | Run `rhdh local health`. |
| Backup, save config, archive | Run `rhdh local backup`. |
| Restore backup | Run `rhdh local restore <archive>` and start with dry-run behavior. |
| Environment variables, `.env` | Read [references/env-reference.md](references/env-reference.md). |
| Troubleshoot, debug, 504, startup error | Read [references/troubleshooting.md](references/troubleshooting.md). |

## References

| File | Use when |
| --- | --- |
| [references/customization-system.md](references/customization-system.md) | Understanding copy-sync, file mapping, and safe edit rules. |
| [references/env-reference.md](references/env-reference.md) | Configuring environment variables. |
| [references/troubleshooting.md](references/troubleshooting.md) | Debugging local startup, 504s, shared network namespace, and comparative tests. |
| [../overlay/references/rhdh-local.md](../overlay/references/rhdh-local.md) | Dynamic plugin YAML and OCI package metadata patterns. |

## Companion Skills

- Use `overlay` for export-overlay metadata, PR artifacts, and package source lookup.
- Use `rhdh` for global environment setup and repo path configuration.

## Validation

- After enabling or disabling a plugin, run `rhdh local apply` and then `rhdh local health`.
- For plugin tests, capture the plugin load status, visible UI route or card, and expected auth or API behavior.
- If local RHDH fails to start, collect the command output and then read [references/troubleshooting.md](references/troubleshooting.md).