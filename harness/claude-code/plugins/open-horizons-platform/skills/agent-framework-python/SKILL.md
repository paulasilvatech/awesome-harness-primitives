---
name: agent-framework-python
description: >-
  Applies Microsoft Agent Framework Python monorepo conventions to the imported example tree. Use
  when changing its public API exports, package metadata, tests, or Python implementation.
paths:
  - docs/microsoft-agent-framwork-example/python/**/*.py
  - docs/microsoft-agent-framwork-example/python/**/*.pyi
  - docs/microsoft-agent-framwork-example/python/**/pyproject.toml
user-invocable: false
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/instructions/agent-framework-python.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Microsoft Agent Framework Python

Use the installed `AGENTS.md` for project structure and package documentation. Use the
`microsoft-agent-framework` and matching Python skills for ordered procedures.

When changing the public root API surface (`agent_framework/__init__.py`), keep the lazy runtime export
registry, explicit runtime `__all__`, and `agent_framework/__init__.pyi` synchronized. Runtime deprecation
behavior for a public alias should live in the owning module, not as a special case in the root package.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep runtime exports, `__all__`, and type stubs synchronized. | Import and typing behavior must expose one public contract. |
| Resolve supported APIs and dependency versions from the owning manifest. | Imported examples can target a different SDK version than another runtime. |
| Keep deprecation behavior in the module that owns the public alias. | Root-package special cases drift from the implementation lifecycle. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Follow the owning manifest and execute focused import and typing checks. | Assume another Agent Framework runtime uses the same dependency version. |
| Keep edits inside the imported Python example tree. | Turn passive conventions into an unrequested migration workflow. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Runtime exports, `__all__`, and type stubs agree.
- [ ] Tests use dependencies resolved from the owning manifest.
- [ ] Focused import, type, and package checks pass or blockers are recorded.
- [ ] No unrelated edits or unresolved placeholders remain.
