# GitHub Copilot Harness Sources

This directory is the canonical source tree for the repository's GitHub Copilot customizations and
installable plugin packages.

[Browse the catalog](../../docs/catalog/github-copilot.md) ·
[Choose plugin or standalone](../../docs/USAGE.md#plugin-versus-standalone) ·
[Read the harness contract](../../docs/COPILOT-HARNESS-SPEC.md)

The directory name identifies the target harness, not authorship or provenance. Individual primitives and
plugins retain their own author, repository, license, and upstream metadata.

## Layout

| Path | Responsibility |
| --- | --- |
| `agents/` | Canonical custom-agent sources |
| `instructions/` | Canonical repository and path-specific instruction sources |
| `skills/` | Canonical Agent Skill packages |
| `prompts/` | Canonical VS Code prompt sources; prompts are not Agent Host or Copilot CLI primitives |
| `hooks/` | Canonical reusable hook packages |
| `plugins/` | Self-contained flat GitHub Copilot packages with direct component directories |
| `manifests/` | Repository distribution and canonical-source ownership manifests |
| `scripts/` | Validation, audit, generation, import, and synchronization tooling |

The repository-level `.github/` tree remains the installed runtime surface. Generate it from this source
tree with `scripts/sync_installed_primitives.py`; do not maintain both locations independently.

`manifests/plugin-sources.json` records whether packaged components come from shared canonical sources
or are owned by the plugin. Distributed `plugin.json` files contain only GitHub Copilot metadata and
direct component paths.

The generated [Plugin Components catalog](../../docs/catalog/github-copilot/plugin-components.md)
lists every declared plugin runtime item separately and labels shared library copies versus
plugin-owned content.
