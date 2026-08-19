# Copilot Harness Documentation

This folder documents how Open Horizons authors GitHub Copilot customization primitives.

## What to read first

- [Copilot Harness Specification](COPILOT-HARNESS-SPEC.md): authoritative technical contract for agents, instructions, skills, plugins, hooks, and validation behavior. It is validated against GitHub Copilot CLI 1.0.81-0.
- [Templates](templates/README.md): starting points for new primitives in this repository.
- [References](references/README.md): illustrative examples from another domain. They are not installed Open Horizons primitives.

## Choose the right primitive

| Need | Primitive | Destination |
| --- | --- | --- |
| Persona, role, boundaries, and tool access | Agent | `.github/agents/<name>.agent.md` |
| Passive rules for matching files | Instructions | `.github/instructions/<name>.instructions.md` |
| Reusable procedure or review checklist | Skill | `.github/skills/<name>/SKILL.md` |
| User-selected VS Code workflow | Prompt | `.github/prompts/<name>.prompt.md` |

## Validate changes

Run this command from the repository root after changing installed primitives:

```sh
python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict
```

The validator is wired into `.github/workflows/validate-agents.yml`. It ignores `.github/docs/` templates and references.
