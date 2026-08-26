# Workflow: Disable a Plugin in Local RHDH

<required_reading>

- `references/customization-system.md` - copy-sync rules, file locations
- `references/troubleshooting.md` - restart patterns and network namespace rules
</required_reading>

<process>
## Step 1: Read Current Plugin Configuration

```bash
cat rhdh-customizations/configs/dynamic-plugins/dynamic-plugins.override.yaml
```

Identify the package entries for the plugin to disable.

---

## Step 2: Disable or Remove the Plugin

**Option A - Set `disabled: true`** (preserves config for later re-enabling):

```yaml
plugins:
  - package: 'oci://ghcr.io/...'
    disabled: true
```

**Option B - Remove entries entirely** (cleaner, use when permanently removing):
Remove the plugin's package entries from the `plugins:` list.

> **Do NOT** remove the `includes:` block - it loads default plugins and is required.

---

## Step 3: Clean Up Related Configuration (if removing permanently)

If the plugin added configuration to `rhdh-customizations/configs/app-config/app-config.local.yaml`, remove the corresponding section.

If the plugin required environment variables in `rhdh-customizations/.env`, remove or comment those out.

---

## Step 4: Apply and Restart

```bash
rhdh local apply
rhdh local down && rhdh local up --customized
```

Add `--lightspeed`, `--orchestrator`, or `--both` flags if those components are enabled.

</process>

<success_criteria>

- [ ] Plugin entry shows `disabled: true` or is removed from `dynamic-plugins.override.yaml`
- [ ] `rhdh local apply` ran without errors
- [ ] RHDH starts cleanly - no errors referencing the disabled plugin
- [ ] Plugin no longer appears in the Extensions Catalog or entity pages
</success_criteria>
