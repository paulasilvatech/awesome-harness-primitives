# Prompts Index

This directory contains the GitHub Copilot prompt files for the workshop.

> Important: keep `*.prompt.md` files directly in `.github/prompts/`. The workspace location documented by Copilot is flat (`.github/prompts/*.prompt.md`). Stage/persona organization is represented by the filename prefix and this index.

## Naming Convention

| Prefix | Use |
| --- | --- |
| `stage-<agent>-<task>.prompt.md` | Prompts for stage agents (`archaeologist`, `architect`, `builder`, `evolution`). |
| `persona-<persona>-<task>.prompt.md` | Prompts for persona kits (`product-owner`, `developer`, `qa-engineer`, etc.). |

## Stage Prompts

| Agent | Files |
| --- | --- |
| `archaeologist` | `stage-archaeologist-*.prompt.md` |
| `architect` | `stage-architect-*.prompt.md` |
| `builder` | `stage-builder-*.prompt.md` |
| `evolution` | `stage-evolution-*.prompt.md` |

## Persona Prompts

| Persona | Files |
| --- | --- |
| Product Owner | `persona-product-owner-*.prompt.md` |
| Requirements Engineer | `persona-requirements-engineer-*.prompt.md` |
| Enterprise Architect | `persona-enterprise-architect-*.prompt.md` |
| Software Architect | `persona-software-architect-*.prompt.md` |
| Technical Lead | `persona-technical-lead-*.prompt.md` |
| Developer | `persona-developer-*.prompt.md` |
| DBA | `persona-dba-*.prompt.md` |
| QA Engineer | `persona-qa-engineer-*.prompt.md` |
| DevOps Engineer | `persona-devops-engineer-*.prompt.md` |
| Tech Writer | `persona-tech-writer-*.prompt.md` |

## Maintenance Rules

- Every prompt must have valid YAML frontmatter.
- Prefer explicit `description`, `name`, `argument-hint` (when inputs exist), `agent`, and `tools` fields.
- Avoid excessive tools; use the smallest set needed for the task.
- Tools defined in the prompt replace, rather than extend, the custom agent's tools; declare all required permissions in the prompt itself.
- Prefer portable VS Code aliases (`read`, `search`, `edit`, `execute`, `agent`, `web`, `todo`) over implementation-specific IDs.
- Do not specify capacity or provider in the prompt. The user decides how to run the task.
- When using a custom agent, reference its `name` from `.github/agents/` (for example, `archaeologist`, not the display name in the file body).
- When adding a new prompt, use one of the prefixes above to preserve discoverability and organization.
