# Copilot plugins

This directory packages the kit's curated Copilot **skills** and **agents** as
named plugins, and exposes them through a local plugin **marketplace** so they
can be declared in [`.github/copilot/settings.json`](../copilot/settings.json).

## What lives here

- Ten plugin directories, each with a `plugin.json` manifest and a `README.md`.
- [`marketplace.json`](marketplace.json) — a local **directory marketplace**
  named `datacorp-mm-team-kit` that lists all ten plugins.

The actual skill and agent content is **not** duplicated here. It is maintained
once at the repository level under [`.github/skills/`](../skills/) and
[`.github/agents/`](../agents/). Each `plugin.json` references that shared
content with relative paths such as `../../skills/<name>/` and
`../../agents/<name>.agent.md`.

## Two layers, one source of truth

1. **Native discovery (in this repository).** Copilot automatically loads every
   skill under `.github/skills/` and every agent under `.github/agents/`. In
   this repository those components already work without installing anything.
2. **Plugin packaging (for naming and reuse).** The plugins group the shared
   components into themed bundles and publish them through the official
   marketplace / `enabledPlugins` mechanism.

## Catalog

| Plugin | Bundles | Status |
|--------|---------|--------|
| [`arch`](arch/) | — | catalog-only (no components in this kit) |
| [`azure-cloud-development`](azure-cloud-development/) | 3 skills | enabled |
| [`chromium-control-canvas`](chromium-control-canvas/) | — | catalog-only (no components in this kit) |
| [`context-engineering`](context-engineering/) | 1 skill | enabled |
| [`copilot-sdk`](copilot-sdk/) | 1 skill | enabled |
| [`database-data-management`](database-data-management/) | 2 skills | enabled |
| [`frontend-web-dev`](frontend-web-dev/) | 1 agent, 1 skill | enabled |
| [`java-development`](java-development/) | 4 skills | enabled |
| [`software-engineering-team`](software-engineering-team/) | 1 agent | enabled |
| [`testing-automation`](testing-automation/) | 2 skills | enabled |

These manifests were adapted from the `github/awesome-copilot` catalog. Of the
48 component references in the original manifests, 16 resolve to content that
exists in this kit and are kept; the other 32 point at skills, agents, or
extensions that are not part of this kit and were removed. Each plugin README
lists exactly what it dropped.

## How plugins are enabled

The declarative configuration lives in
[`.github/copilot/settings.json`](../copilot/settings.json):

```json
{
  "extraKnownMarketplaces": {
    "datacorp-mm-team-kit": {
      "source": { "source": "directory", "path": ".github/plugins" }
    }
  },
  "enabledPlugins": {
    "java-development@datacorp-mm-team-kit": true
  }
}
```

- `extraKnownMarketplaces` registers the local directory marketplace. The value
  shape (`{ "source": { "source": "directory", "path": ... } }`) is exactly what
  the CLI writes when you register a directory marketplace.
- `enabledPlugins` keys are plugin **specs** in `name@marketplace` form — never
  bare names or filesystem paths. Only the eight component-bearing plugins are
  enabled; the two catalog-only entries are listed in the marketplace but not
  enabled, because enabling them would load nothing.

To register the marketplace on demand from the repository root, use the
command the CLI supports for a directory source (the explicit `./` prefix is
required so the path is not read as a GitHub `owner/repo` spec):

```bash
copilot plugin marketplace add ./.github/plugins
copilot plugin marketplace browse datacorp-mm-team-kit
```

## Honest limitations

- **In this repository the plugins add no new capability.** Everything they
  reference is already loaded by native discovery of `.github/skills/` and
  `.github/agents/`. The plugin layer is documentation and packaging: it records
  which shared components form each bundle and exposes them through the official
  marketplace mechanism.
- **Installed plugins copy only their own directory.** When a plugin is
  installed from a marketplace, Copilot copies that plugin's directory — not the
  repository root. Because these manifests point at shared content **outside**
  the plugin directory (`../../skills/...`, `../../agents/...`), those components
  are not copied on install and will not appear in another repository or a
  global install. This was verified empirically: installing such a plugin
  reports success but bundles zero skills. To ship a self-contained plugin, the
  referenced content must be vendored into the plugin directory. This kit
  deliberately does not duplicate that content, because it is maintained once at
  the repository root.
- **Headless `copilot -p` runs did not apply the repository
  `extraKnownMarketplaces`.** In a non-interactive prompt session only the
  default marketplaces loaded. The declarative settings are documented for
  interactive and agent sessions; the reliable, verified way to register the
  local marketplace is the `copilot plugin marketplace add ./.github/plugins`
  command above.

## Validation

```bash
# every manifest and settings file parses as JSON
python3 -c "import json,glob; [json.load(open(f)) for f in \
  glob.glob('.github/plugins/*/plugin.json') + \
  ['.github/copilot/settings.json', '.github/plugins/marketplace.json']]"

# markdown lint (uses the root .markdownlint-cli2.jsonc)
npx --yes markdownlint-cli2 ".github/plugins/**/*.md"
```

## References

- Copilot CLI plugins:
  <https://docs.github.com/copilot/concepts/agents/copilot-cli/about-cli-plugins>
- Creating plugins:
  <https://docs.github.com/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating>
- Copilot CLI reference:
  <https://docs.github.com/copilot/how-tos/copilot-cli>
- Upstream catalog: <https://github.com/github/awesome-copilot>
