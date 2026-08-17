---
description: "Use when editing Copilot primitive source files for agents, instructions, skills, and VS Code prompts in this repository."
applyTo: "library/agents/*.agent.md,library/instructions/*.instructions.md,library/skills/**/SKILL.md,library/prompts/*.prompt.md,.github/agents/*.agent.md,.github/instructions/*.instructions.md,.github/skills/**/SKILL.md,.github/prompts/*.prompt.md"
---

# Copilot Primitive Authoring Conventions

## Scope and Stack Context

These instructions apply to Copilot primitive files matched by the `applyTo` globs: agents, instructions, skills, and VS Code prompts under `library/` and installed mirrors under `.github/`. They define passive authoring invariants for this repository. They do not define an ordered creation or review workflow; use the `copilot-primitive-authoring` skill for procedure.

## Authoritative Sources and Precedence

Follow these sources in order:

1. `docs/COPILOT-HARNESS-SPEC.md` for CLI-discovered agents, instructions, skills, plugins, hooks, fields, tool tokens, and validation semantics.
2. `docs/templates/` for this repository's expected primitive shapes and reusable section patterns.
3. `docs/references/` for calibrated examples of concise, scoped, rationale-driven instructions.

When sources conflict, `docs/COPILOT-HARNESS-SPEC.md` wins over instruction-authoring guidance. Do not copy a reference file's domain-specific content into a primitive authoring rule.

## Responsibility Split

This file owns passive conventions that apply while editing primitive files. The `copilot-primitive-authoring` skill owns ordered authoring steps, evidence gathering, validation sequencing, and delivery format. Agents own persona, judgment boundary, and authority. Instructions own passive conventions. Skills own reusable procedures or criteria. Prompts own explicit VS Code actions.

## Core Conventions

| Rule | Rationale |
| --- | --- |
| Treat `library/` as the canonical source for reusable primitives; do not edit `.github/` mirrors or plugin copies directly. | Mirrors can be regenerated or synchronized, so direct edits drift and disappear. |
| Make every `description` a discovery surface that states what the primitive does and when to use it. | Agents and skills are selected from descriptions before full bodies load. |
| Keep instruction `applyTo` present and set to one quoted, comma-separated glob string. | Without `applyTo`, an instruction file is not applied automatically. |
| Reference other primitives by installed name and type, not by relative link. | Runtime installation paths differ; semantic names survive copying and packaging. |
| Use relative paths only inside the same skill package, such as `references/`, `scripts/`, `assets/`, or `templates/`. | Skill resources travel with the skill; cross-primitive links do not. |

## Frontmatter and Runtime Fields

- Use only fields recognized by the target primitive type. For instructions, only `applyTo`, `description`, `name`, and `excludeAgent` are recognized.
- For agents, treat `tools` as an allow-list filter, not a grant request. Omit it or use `["*"]` only when unrestricted access is intentional.
- Do not use CLI no-op tool tokens: `search`, `web`, `todo`, `all`, `terminal`, `run`, `codebase`, `changes`, `fetch`, or `githubRepo`. They are silently ignored.
- Use valid CLI tokens for the intended capability: `read`, `grep`, `glob`, `edit`, `execute`, `web_fetch`, and `web_search`.
- For skills, set `name` to kebab-case and make it exactly match the parent directory. Keep `SKILL.md` under 500 lines, preferably under 200, and move bulk material into bundled resources.
- Treat prompts as VS Code-only files. They are repository primitives for authoring and distribution, but they are not discovered or executed by Copilot CLI.

## Good / Bad Examples

The examples below illustrate tool-token and discovery-surface rules.

**Good**

```yaml
description: "Review Copilot primitive files for harness compatibility. Use when validating agents, instructions, skills, or prompts."
tools: ["read", "grep", "glob", "web_fetch"]
```

Why: the description states what and when, and every tool token maps to a CLI capability.

**Bad**

```yaml
description: "Primitive helper."
tools: ["search", "web", "todo", "terminal"]
```

Why: the description is not actionable for discovery, and the listed tools are no-op tokens in the CLI.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Start from the matching template and remove template-only notes before saving. | Leave `{{UPPER_SNAKE_CASE}}` placeholders or authoring notes in a finished primitive. |
| Keep responsibilities separate between agent, instructions, skill, and prompt files. | Put a workflow in instructions or passive conventions in a skill procedure. |
| Use concise examples that prove the convention. | Add long tutorials or unrelated reference material to the primitive body. |
| Validate canonical library sources and generated catalog drift. | Treat a clean-looking Markdown file as runtime-compatible without validation. |

## Verification Checklist

- [ ] The edited file is the canonical `library/` source unless the task explicitly targets an installed mirror.
- [ ] Frontmatter uses only recognized fields for the primitive type.
- [ ] Descriptions state both what the primitive does and when to use it.
- [ ] Agent tool lists avoid no-op tokens and use valid CLI tokens such as `read`, `grep`, `glob`, `edit`, `execute`, `web_fetch`, and `web_search`.
- [ ] Skill names are kebab-case, match their parent directory, and keep `SKILL.md` below 500 lines, preferably below 200.
- [ ] Instruction files include an auto-applying quoted `applyTo` string.
- [ ] Prompt files are treated as VS Code-only and not as CLI primitives.
- [ ] Cross-primitive references use primitive name and type; relative paths appear only inside a skill package.
- [ ] No `{{UPPER_SNAKE_CASE}}` placeholders, authoring notes, or unrelated edits remain.
- [ ] Validation passes: `python3 library/scripts/validate_primitives.py --strict`.
- [ ] Catalog drift check passes: `python3 library/scripts/generate_catalog.py --check`.
