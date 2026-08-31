# Catalog hub

Browse by target harness or by package membership.

| Catalog | Contents |
| --- | --- |
| [GitHub Copilot](github-copilot.md) | Canonical standalone primitives, installable plugins, and every declared plugin runtime component. |
| [Claude Code](claude-code.md) | Generated standalone primitives, installable plugins, and every Claude runtime or compatibility component. |

## How entries are classified

- **Standalone** entries can be copied directly from a harness library.
- **Plugin components** use the qualified form `plugin:item` and link to the exact bundled source.
- **Shared library copy** means the plugin materializes a canonical standalone primitive.
- **Plugin-owned** means the component is maintained inside the plugin package.
- **Compatibility payload** is bundled data used by a publisher but not discovered as a native primitive.

The plugin-component inventories are intentionally explicit: aggregate package counts are not considered sufficient catalog coverage.

## Credits and provenance

Multiple catalog entries are adapted from
[github/awesome-copilot](https://github.com/github/awesome-copilot). They have
been updated and improved here for stricter validation, packaging, discovery,
and GitHub Copilot plus Claude Code compatibility. Applicable plugin rows link
to their upstream source.

## Choose a delivery model

Use a [plugin](../USAGE.md#choose-a-plugin) for a cohesive suite or a [standalone primitive](../USAGE.md#choose-a-standalone-primitive) for one focused capability.
