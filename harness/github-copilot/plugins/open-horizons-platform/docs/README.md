# GitHub Copilot Harness Documentation

This folder documents how Open Horizons authors GitHub Copilot customization primitives.

## What to read first

- [Copilot Harness Specification](COPILOT-HARNESS-SPEC.md): authoritative technical contract for agents, instructions, skills, plugins, hooks, and validation behavior. It is validated against GitHub Copilot CLI 1.0.81-0.
- [Templates](templates/README.md): starting points for new primitives in this repository.

## Choose the right primitive

| Need | Primitive | Package source | Published workspace path |
| --- | --- | --- | --- |
| Persona, role, boundaries, and tool access | Agent | `agents/<name>.agent.md` | `.github/agents/<name>.agent.md` when used without the plugin |
| Passive rules for matching files | Instructions | `instructions/<name>.instructions.md` | `.github/instructions/<name>.instructions.md` |
| Reusable procedure or review checklist | Skill | `skills/<name>/SKILL.md` | `.github/skills/<name>/SKILL.md` when used without the plugin |
| User-selected VS Code workflow | Prompt | `prompts/<name>.prompt.md` | `.github/prompts/<name>.prompt.md` |
| Bounded lifecycle automation | Hook | `hooks/<name>/hooks.json` | `.github/hooks/<name>.json` plus referenced scripts |

## Validate changes

Run this command from the `open-horizons-platform` plugin root:

```sh
python3 skills/validation-scripts/scripts/validate-agents.py --strict
```

After publishing the workspace kit, use `python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict`. The validator is wired into `.github/workflows/validate-agents.yml` and ignores documentation templates.
