# Reference: RHDH Local Customization System

The copy-sync system for managing RHDH Local configuration without modifying the upstream `rhdh-local/` git repository.

> **Setup:** `rhdh-local-setup/` is a workspace directory containing your `rhdh-local` git clone and customizations.
> `rhdh-customizations/` holds your override files. The `rhdh local apply`, `rhdh local up`, and `rhdh local down`
> commands handle copy-sync and compose orchestration directly via Python - no shell scripts required.
> The standalone CLI entry point is at `skills/rhdh-local/scripts/rhdh-local`.
> See `scripts/NOTICE` for attribution.

<architecture>
**Workspace layout:**

```
rhdh-local-setup/
├── rhdh-local/                    # Upstream git repo - NEVER edit directly
│   ├── compose.yaml
│   ├── default.env
│   └── configs/
│       ├── app-config/app-config.yaml
│       └── dynamic-plugins/dynamic-plugins.default.yaml
└── rhdh-customizations/           # Your overrides - ALWAYS edit here
    ├── .env
    ├── compose.override.yaml
    └── configs/
        ├── app-config/app-config.local.yaml
        ├── dynamic-plugins/dynamic-plugins.override.yaml
        ├── catalog-entities/users.override.yaml
        └── extra-files/github-app-credentials.yaml

# CLI commands:
# rhdh local apply   → copies files into rhdh-local/
# rhdh local remove  → deletes copies from rhdh-local/
# rhdh local up      → applies customizations + starts containers
# rhdh local down    → stops containers + removes customizations
```

**The copy-sync invariant:**

- `rhdh-customizations/` is the single source of truth for all configuration
- `rhdh local apply` copies files into `rhdh-local/`
- Containers read files from `rhdh-local/` (they cannot access paths outside their mount)
- `rhdh local remove` deletes the copies, restoring pristine state
- `rhdh-local/` git status should always be "working tree clean" - the copied files are gitignored
</architecture>

<file_mapping>
**Source → Destination** (what `rhdh local apply` copies):

| Edit here (`rhdh-customizations/`) | Copied to (`rhdh-local/`) |
|------------------------------------|---------------------------|
| `compose.override.yaml` | `compose.override.yaml` |
| `.env` | `.env` |
| `configs/app-config/app-config.local.yaml` | `configs/app-config/app-config.local.yaml` |
| `configs/dynamic-plugins/dynamic-plugins.override.yaml` | `configs/dynamic-plugins/dynamic-plugins.override.yaml` |
| `configs/catalog-entities/*.override.yaml` | `configs/catalog-entities/*.override.yaml` |
| `configs/extra-files/*` | `configs/extra-files/*` |
| `developer-lightspeed/configs/app-config/app-config.lightspeed.local.yaml` | same relative path |
</file_mapping>

<configuration_layers>
**Precedence (lowest → highest):**

1. **Layer 1 - Defaults:** `rhdh-local/` version-controlled files
   - `default.env`, `app-config.yaml`, `dynamic-plugins.default.yaml`
2. **Layer 2 - Overrides:** Files copied from `rhdh-customizations/`
   - `.env`, `app-config.local.yaml`, `dynamic-plugins.override.yaml`
3. **Layer 3 - app-config.local.yaml:** Loads last, highest precedence among config files
4. **Environment variables** from `.env` override `default.env`
</configuration_layers>

<edit_rules>
**ALWAYS:**

- Edit customization files in `rhdh-customizations/` directory
- Run `rhdh local apply` after every edit
- Verify pristine state: `cd rhdh-local && git status` → "working tree clean"
- Use `rhdh local up` / `rhdh local down` for container lifecycle

**NEVER:**

- Modify files in `rhdh-local/` for customization purposes
- Manually copy files (use `rhdh local apply`)
- Commit `*.local.yaml`, `*.override.yaml`, or `.env` to the rhdh-local repository
- Edit the copied files in `rhdh-local/` - they get overwritten on the next `rhdh local apply`
</edit_rules>

<quick_reference>
**What to edit and where:**

| Change | File |
|--------|------|
| App configuration | `rhdh-customizations/configs/app-config/app-config.local.yaml` |
| Plugin enable/disable | `rhdh-customizations/configs/dynamic-plugins/dynamic-plugins.override.yaml` |
| Environment variables | `rhdh-customizations/.env` |
| Extra services (Jenkins etc.) | `rhdh-customizations/compose.override.yaml` |
| Catalog entities | `rhdh-customizations/configs/catalog-entities/components.override.yaml` |
| Credentials | `rhdh-customizations/configs/extra-files/github-app-credentials.yaml` |
| Lightspeed config | `rhdh-customizations/developer-lightspeed/configs/app-config/app-config.lightspeed.local.yaml` |

**Standard change workflow:**

```bash
# 1. Edit the file in rhdh-customizations/
# 2. Sync into rhdh-local/ and restart
rhdh local apply
rhdh local down && rhdh local up --customized [--lightspeed|--orchestrator|--both]
```

**Update rhdh-local from upstream:**

```bash
rhdh local down
cd rhdh-local-setup/rhdh-local && git pull && cd ../..
rhdh local up --customized [flags]
```

</quick_reference>
