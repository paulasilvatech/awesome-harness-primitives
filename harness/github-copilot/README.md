# GitHub Copilot Harness Sources

This directory is the canonical source tree for the repository's GitHub Copilot customizations and
installable plugin packages.

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
| `plugins/` | Self-contained Agent Plugins 1.0 packages and generated component copies |
| `manifests/` | Repository distribution manifests |
| `scripts/` | Validation, audit, generation, import, and synchronization tooling |

The repository-level `.github/` tree remains the installed runtime surface. Generate it from this source
tree with `scripts/sync_installed_primitives.py`; do not maintain both locations independently.

`componentSource: "library"` in managed plugin metadata is retained as a layout-version-1 compatibility
value. In repository documentation, use **shared canonical source** rather than “library-owned.”
