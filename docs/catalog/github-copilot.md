# Copilot Primitives Catalog

This is the generated index of every canonical Copilot primitive package in
this repository. Each primitive type has its own page listing every entry with
a concise purpose, a typical use case, and a link to its source.

[Catalog hub](README.md) · [Plugin versus standalone](../USAGE.md) ·
[Repository home](../../README.md)

## Credits and provenance

This catalog includes multiple plugins, components, and references adapted from
[github/awesome-copilot](https://github.com/github/awesome-copilot). They have been updated and
improved for current harness contracts, stricter validation, self-contained
packaging, and GitHub Copilot plus Claude Code compatibility. Applicable plugin
rows link back to the upstream repository.

## Catalog pages

| Page | What the type does | Typical use cases | Canonical source |
| --- | --- | --- | --- |
| [Agents](github-copilot/agents.md) | Defines a specialist persona, judgment boundary, and tool posture. | Delegated implementation, review, diagnosis, architecture, or domain-specific decisions. | `harness/github-copilot/agents/` |
| [Instructions](github-copilot/instructions.md) | Applies passive conventions to matching files or repository work. | Coding standards, governance, path-specific rules, and verification requirements. | `harness/github-copilot/instructions/` |
| [Skills](github-copilot/skills.md) | Packages a reusable workflow with optional scripts, references, and assets. | Repeatable procedures that need ordered steps, domain knowledge, or bundled resources. | `harness/github-copilot/skills/` |
| [VS Code Prompts](github-copilot/prompts.md) | Defines an explicit action a user runs from VS Code Chat. | Guided generation, transformation, review, and interactive workspace tasks. | `harness/github-copilot/prompts/` |
| [Plugin Components](github-copilot/plugin-components.md) | Lists every runtime component declared by every plugin as an individually discoverable item. | Finding a specific agent, skill, hook, MCP or LSP server, output style, or client extension without browsing package trees. | `harness/github-copilot/plugins/*/` |
| [Plugins](github-copilot/plugins.md) | Bundles installable Copilot capabilities and optional MCP, hook, or client-extension surfaces. | Distributing cohesive capability suites through a plugin or marketplace. | `harness/github-copilot/plugins/` |
| [Hooks](github-copilot/hooks.md) | Runs deterministic checks or automation at Copilot lifecycle events. | Guardrails, compliance checks, logging, and opt-in session automation. | `harness/github-copilot/hooks/` |

## Summary

| Primitive type | Entries |
| --- | --- |
| [Agents](github-copilot/agents.md) | 228 |
| [Instructions](github-copilot/instructions.md) | 196 |
| [Skills](github-copilot/skills.md) | 490 |
| [VS Code Prompts](github-copilot/prompts.md) | 48 |
| [Plugin Components](github-copilot/plugin-components.md) | 919 |
| [Plugins](github-copilot/plugins.md) | 139 |
| [Hooks](github-copilot/hooks.md) | 8 |

## Maintenance contract

- Do not hand-edit the index or any catalog page. Regenerate them with
  `python3 harness/github-copilot/scripts/generate_catalog.py`.
- Regenerate after changing canonical agents, instructions, skills, prompts,
  plugins, or hooks under `harness/github-copilot/`.
- CI runs `python3 harness/github-copilot/scripts/generate_catalog.py --check` and blocks a stale index or page.
- Standalone pages list shared primitives once at their canonical source.
- The Plugin Components page intentionally repeats package membership with
  qualified `plugin:item` names so every bundled runtime item is discoverable.
