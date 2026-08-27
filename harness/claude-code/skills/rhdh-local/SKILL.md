---
name: rhdh-local
description: >-
  Use this skill when the user tests Red Hat Developer Hub plugins locally with rhdh-local-setup.
  Trigger for enabling or disabling plugins, switching customized and pristine modes, running
  local plugin tests, starting or stopping RHDH, health checks, backup and restore, environment
  variables, 504 errors, startup failures, and local troubleshooting.
---

<!-- Generated from harness/github-copilot/skills/rhdh-local/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# RHDH local

Operate local Red Hat Developer Hub through the `rhdh-local-setup` customization system, preserving generated-file boundaries while routing plugin enablement, mode switching, health checks, backup/restore, and troubleshooting to the correct bundled workflow or command.

## When to invoke

- "Enable this RHDH plugin locally."
- "Switch RHDH local to pristine mode."
- "Run a local plugin smoke test."
- "Start RHDH with Lightspeed and Orchestrator."
- "Debug a 504 or startup failure in rhdh-local."

## Prerequisites and context

- The repository must contain the `rhdh-local-setup` customization layout with `rhdh-customizations/` and generated `rhdh-local/` output.
- The `rhdh` local CLI must be available, including `rhdh local up`, `rhdh local down`, `rhdh local apply`, `rhdh local health`, `rhdh local backup`, and `rhdh local restore <archive>`.
- Plugin package definitions come from `rhdh-plugin-export-overlays` metadata; use `spec.dynamicArtifact` and do not construct OCI URLs manually.

## Operating principles

| Rule | Reason |
| --- | --- |
| Edit only under `rhdh-customizations/`. | `rhdh-local/` contains generated copies that are overwritten by apply/sync. |
| Run `rhdh local apply` after every configuration edit. | Generated runtime files must match customization sources. |
| Use `rhdh local up` and `rhdh local down`. | Direct `podman compose` bypasses shared-network handling for Lightspeed or Orchestrator. |
| Treat auth errors from plugin APIs as possible smoke-test success. | Local tests may lack real credentials; successful load plus attempted API calls still proves integration wiring. |
| Ask only for missing plugin name, package reference, or target mode. | Start, stop, health, and status requests are directly actionable. |

## Routing

| User intent | Action |
| --- | --- |
| Enable, add, install plugin | Read `workflows/enable-plugin.md`. |
| Disable, remove, turn off plugin | Read `workflows/disable-plugin.md`. |
| Switch mode, pristine, customized | Read `workflows/switch-mode.md`. |
| Test, verify, check plugin | Read `workflows/test-plugin.md`. |
| Status, list plugins, show enabled plugins | Inspect `rhdh-customizations/configs/dynamic-plugins/dynamic-plugins.override.yaml`. |
| Start, up, start RHDH | Run `rhdh local up`, adding `--lightspeed`, `--orchestrator`, or `--both` when requested. |
| Stop, down, stop RHDH | Run `rhdh local down`. |
| Health, check health, is RHDH running | Run `rhdh local health`. |
| Backup, save config, archive | Run `rhdh local backup`. |
| Restore backup | Run `rhdh local restore <archive>` and start with dry-run behavior. |
| Environment variables, `.env` | Read `references/env-reference.md`. |
| Troubleshoot, debug, 504, startup error | Read `references/troubleshooting.md`. |

## Validation rules

| Task | Required validation |
| --- | --- |
| Enable or disable plugin | Run `rhdh local apply`, then `rhdh local health`. |
| Plugin test | Capture plugin load status, visible UI route or card, and expected auth/API behavior. |
| Startup failure | Collect command output, then read `references/troubleshooting.md`. |
| Mode switch | Verify generated configuration reflects pristine or customized mode after apply. |
| Backup/restore | Report archive path and whether restore was dry-run or applied. |

## Progressive disclosure and bundled resources

| Resource | Use when |
| --- | --- |
| `workflows/enable-plugin.md` | Enabling or adding a local dynamic plugin. |
| `workflows/disable-plugin.md` | Disabling or removing a plugin. |
| `workflows/switch-mode.md` | Switching pristine/customized modes. |
| `workflows/test-plugin.md` | Testing plugin load and UI/API behavior. |
| `references/customization-system.md` | Understanding copy-sync, file mapping, and safe edit rules. |
| `references/env-reference.md` | Configuring environment variables and `.env`. |
| `references/troubleshooting.md` | Debugging local startup, 504s, shared network namespace, and comparative tests. |
| `scripts/fetch-plugin-metadata.py` | Fetching plugin metadata when package source lookup is needed. |
| `scripts/rhdh-local` and `rhdh_local/` | Bundled local helper implementation. |

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `overlay` | skill | Dynamic plugin YAML, export-overlay metadata, PR artifacts, or package source lookup is the primary task. |
| `rhdh` | skill | Global environment setup or repo path configuration is the primary task. |

## Gotchas

- **Do not edit generated `rhdh-local/` files**: changes disappear on the next apply.
- **Do not bypass the CLI with direct `podman compose`**: shared network services may be skipped or miswired.
- **Do not manually build OCI URLs**: `spec.dynamicArtifact` from overlay metadata is the authority.

## Output template

```markdown
### RHDH local result

**Status:** complete | needs input | blocked
**Action:** enable | disable | switch mode | test | status | start | stop | health | backup | restore | troubleshoot
**Mode:** pristine | customized | not applicable

| Step | Evidence |
| --- | --- |
| Resource or workflow used | `<workflow/reference/command>` |
| Configuration path | `<rhdh-customizations path>` |
| Apply result | `rhdh local apply`: pass | fail | not needed |
| Health result | `rhdh local health`: pass | fail | not run |
| Plugin signal | `<load status, route/card, auth/API behavior>` |

**Next action**
- `<follow-up or none>`
```

## Quality gate

- [ ] The requested local action was routed to the correct command, workflow, or reference.
- [ ] Configuration edits, if any, were made under `rhdh-customizations/` only.
- [ ] `rhdh local apply` was run after configuration edits.
- [ ] `rhdh local health` was run after enable/disable operations or start operations.
- [ ] Plugin package metadata uses `spec.dynamicArtifact` instead of handcrafted OCI URLs.
- [ ] Troubleshooting captures command output before applying fixes.
- [ ] Related primitive handoff is named without relative links between primitives.
