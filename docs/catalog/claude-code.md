# Claude Code Primitives Catalog

Generated inventory for `harness/claude-code/`.

[Catalog hub](README.md) · [Plugin versus standalone](../USAGE.md) ·
[Repository home](../../README.md)

## Catalog pages

| Page | Contents | Entries |
| --- | --- | --- |
| [Subagents](claude-code/subagents.md) | Specialist personas with isolated context and tool scope. | 228 |
| [Rules](claude-code/rules.md) | Passive project guidance, optionally scoped by paths. | 196 |
| [Skills](claude-code/skills.md) | Reusable procedures with optional bundled resources. | 490 |
| [Commands](claude-code/commands.md) | Explicit legacy-compatible slash-command actions. | 48 |
| [Plugin Components](claude-code/plugin-components.md) | Every component bundled by a plugin, listed separately with its runtime support. | 1004 |
| [Plugins](claude-code/plugins.md) | Installable, self-contained Claude Code packages. | 139 |
| [Hooks](claude-code/hooks.md) | Reusable deterministic lifecycle automation packages. | 8 |

## Maintenance contract

- Do not hand-edit the index or generated catalog pages.
- Regenerate with `python3 harness/claude-code/scripts/generate_catalog.py`.
- Change canonical primitive content under `harness/github-copilot/`, then run
  `harness/claude-code/scripts/convert_from_copilot.py`.
- Plugin components use qualified `plugin:item` names and distinguish native
  Claude runtime components from compatibility payloads.
