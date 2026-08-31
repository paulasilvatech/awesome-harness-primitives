# Copilot Primitives Catalog

This is the generated index of every canonical Copilot primitive package in
this repository. Each primitive type has its own page listing every entry with
a concise purpose, a typical use case, and a link to its source.

## Catalog pages

| Page | What the type does | Typical use cases | Canonical source |
| --- | --- | --- | --- |
| [Agents](docs/catalog/agents.md) | Defines a specialist persona, judgment boundary, and tool posture. | Delegated implementation, review, diagnosis, architecture, or domain-specific decisions. | `harness/github-copilot/agents/` |
| [Instructions](docs/catalog/instructions.md) | Applies passive conventions to matching files or repository work. | Coding standards, governance, path-specific rules, and verification requirements. | `harness/github-copilot/instructions/` |
| [Skills](docs/catalog/skills.md) | Packages a reusable workflow with optional scripts, references, and assets. | Repeatable procedures that need ordered steps, domain knowledge, or bundled resources. | `harness/github-copilot/skills/` |
| [VS Code Prompts](docs/catalog/prompts.md) | Defines an explicit action a user runs from VS Code Chat. | Guided generation, transformation, review, and interactive workspace tasks. | `harness/github-copilot/prompts/` |
| [Plugins](docs/catalog/plugins.md) | Bundles installable Copilot capabilities and optional MCP, hook, or client-extension surfaces. | Distributing cohesive capability suites through a plugin or marketplace. | `harness/github-copilot/plugins/` |
| [Hooks](docs/catalog/hooks.md) | Runs deterministic checks or automation at Copilot lifecycle events. | Guardrails, compliance checks, logging, and opt-in session automation. | `harness/github-copilot/hooks/` |

## Summary

| Primitive type | Entries |
| --- | --- |
| [Agents](docs/catalog/agents.md) | 228 |
| [Instructions](docs/catalog/instructions.md) | 196 |
| [Skills](docs/catalog/skills.md) | 490 |
| [VS Code Prompts](docs/catalog/prompts.md) | 48 |
| [Plugins](docs/catalog/plugins.md) | 139 |
| [Hooks](docs/catalog/hooks.md) | 8 |

## Maintenance contract

- Do not hand-edit the index or any catalog page. Regenerate them with
  `python3 harness/github-copilot/scripts/generate_catalog.py`.
- Regenerate after changing canonical agents, instructions, skills, prompts,
  plugins, or hooks under `harness/github-copilot/`.
- CI runs `python3 harness/github-copilot/scripts/generate_catalog.py --check` and blocks a stale index or page.
- Shared primitives copied into plugins or `.github/` are listed once at their
  canonical source. Plugin rows summarize bundled capabilities without
  duplicating generated copies.
