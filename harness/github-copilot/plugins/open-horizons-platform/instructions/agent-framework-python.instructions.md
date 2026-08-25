---
applyTo: "docs/microsoft-agent-framwork-example/python/**/*.py,docs/microsoft-agent-framwork-example/python/**/*.pyi,docs/microsoft-agent-framwork-example/python/**/pyproject.toml"
description: "Applies Microsoft Agent Framework Python monorepo conventions to the imported example tree. Use when changing its public API exports, package metadata, tests, or Python implementation."
---

# Microsoft Agent Framework Python

See [AGENTS.md](../../AGENTS.md) for project structure and package documentation.
Detailed conventions are in the agent skills under `.github/skills/`.

When changing the public root API surface (`agent_framework/__init__.py`), keep the lazy runtime export
registry, explicit runtime `__all__`, and `agent_framework/__init__.pyi` synchronized. Runtime deprecation
behavior for a public alias should live in the owning module, not as a special case in the root package.
