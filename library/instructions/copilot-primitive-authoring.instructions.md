---
description: "Requires routing, canonical paths, frontmatter, tool-token, mirror, and validation conventions when editing Copilot primitives. Use when authoring or reviewing agents, instructions, skills, prompts, or installed mirrors."
applyTo: "library/agents/*.agent.md,library/instructions/*.instructions.md,library/skills/**/SKILL.md,library/prompts/*.prompt.md,.github/agents/*.agent.md,.github/instructions/*.instructions.md,.github/skills/**/SKILL.md,.github/prompts/*.prompt.md"
---

# Copilot Primitive Authoring Conventions — Harness-Compatible Files

These instructions apply to Copilot primitive files matched by the `applyTo` globs: agents, instructions, skills, VS Code prompts, and installed mirrors under `library/` or `.github/`. They are authoritative for passive authoring invariants, routing, canonical paths, frontmatter, tool tokens, validation, and cross-primitive references in matched files; `docs/COPILOT-HARNESS-SPEC.md` wins for runtime discovery, schema, and validation semantics.

## Authoritative Sources and Precedence

Follow these sources in order:

1. `docs/COPILOT-HARNESS-SPEC.md` for CLI-discovered agents, instructions, skills, plugins, hooks, fields, tool tokens, and validation semantics.
2. `docs/templates/` for this repository's expected primitive shapes and reusable section patterns.
3. `docs/references/` for calibrated examples of concise, scoped, rationale-driven instructions.

When sources conflict, `docs/COPILOT-HARNESS-SPEC.md` wins over instruction-authoring guidance. Do not copy a reference file's domain-specific content into a primitive authoring rule.

## Responsibility Split

This file owns passive conventions that apply while editing primitive files. The `copilot-primitive-authoring` skill owns ordered authoring steps, evidence gathering, validation sequencing, and delivery format. The `copilot-primitive-architect` agent owns ambiguous type choices and consultative suite-level architecture reviews. Agents own persona, judgment boundary, and authority. Instructions own passive conventions. Skills own reusable procedures or criteria. Prompts own explicit VS Code actions.

## Routing and Canonical Paths

| Primitive | Canonical library path | Routing convention |
| --- | --- | --- |
| Agent | `library/agents/<name>.agent.md` | Use the `copilot-primitive-authoring` skill for procedure. |
| Instruction | `library/instructions/<name>.instructions.md` | Use the `copilot-primitive-authoring` skill for procedure. |
| Skill | `library/skills/<name>/SKILL.md` | Use the `skill-creator` skill. |
| Prompt | `library/prompts/<name>.prompt.md` | Use the `copilot-primitive-authoring` skill for procedure; treat prompts as VS Code-only. |

Treat `library/` as the canonical source for reusable primitives. Do not edit `.github/` mirrors or plugin copies directly unless a task explicitly targets an installed mirror. Use a valid kebab-case primitive name with no path separators, `..`, leading or trailing hyphen, or double hyphen.

## Frontmatter and Runtime Fields

- Use only fields recognized by the target primitive type.
- For instructions, only `applyTo`, `description`, `name`, and `excludeAgent` are recognized.
- Keep instruction `applyTo` present and set to one quoted, comma-separated glob string.
- Make every `description` a discovery surface that states what the primitive does and when to use it.
- For agents, treat `tools` as an allow-list filter, not a grant request. Omit it or use `["*"]` only when unrestricted access is intentional.
- Do not use CLI no-op tool tokens: `search`, `web`, `todo`, `all`, `terminal`, `run`, `codebase`, `changes`, `fetch`, or `githubRepo`.
- Use valid CLI tokens for intended capabilities: `read`, `grep`, `glob`, `edit`, `execute`, `web_fetch`, and `web_search`.
- For skills, set `name` to kebab-case and make it exactly match the parent directory. Keep `SKILL.md` under 500 lines, preferably under 200, and move bulk material into bundled resources.
- Treat prompts as VS Code-only files. They are repository primitives for authoring and distribution, but they are not discovered or executed by Copilot CLI.

## Cross-Primitive References and Mirrors

Reference other primitives by installed name and type, not by relative link. Use relative paths only inside the same skill package, such as `references/`, `scripts/`, `assets/`, or `templates/`. Consult references of the same primitive type as the target artifact so agent, instruction, skill, and prompt responsibilities do not bleed into one another.

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

## Conventions

| Rule | Rationale |
| --- | --- |
| Treat `library/` as the canonical source and avoid direct `.github/` mirror edits. | Mirrors can be regenerated or synchronized, so direct edits drift and disappear. |
| Route `skill` work to `skill-creator`, and route `agent`, `instructions`, and `prompt` work to `copilot-primitive-authoring`. | Agent Skills have separate packaging rules, and other primitive types share authoring procedure. |
| Use valid kebab-case names and canonical paths. | Discovery, catalog generation, mirroring, and plugin packaging remain deterministic. |
| Keep descriptions actionable and include when to use the primitive. | Agents and skills are selected from descriptions before full bodies load. |
| Use only recognized frontmatter fields and valid tool tokens. | Unknown fields or no-op tokens silently break runtime behavior. |
| Reference primitives by name and type rather than relative links. | Runtime installation paths differ, but semantic names survive copying and packaging. |
| Validate primitives with repository scripts before delivery. | Markdown shape alone does not prove harness compatibility. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Start from the matching template and remove template-only notes before saving. | Leave uppercase double-brace placeholders or authoring notes in a finished primitive. |
| Keep responsibilities separate between agent, instructions, skill, and prompt files. | Put a workflow in instructions or passive conventions in a skill procedure. |
| Use concise examples that prove the convention. | Add long tutorials or unrelated reference material to the primitive body. |
| Apply validation appropriate to the primitive type. | Treat a clean-looking Markdown file as runtime-compatible without type-specific checks. |
| Use `read`, `grep`, `glob`, `edit`, `execute`, `web_fetch`, and `web_search` where those capabilities are needed. | Use `search`, `web`, `todo`, `all`, `terminal`, `run`, `codebase`, `changes`, `fetch`, or `githubRepo` as CLI tool tokens. |

## Checklist Before Opening a PR

- [ ] The edited file is the canonical `library/` source unless the task explicitly targets an installed mirror.
- [ ] Frontmatter uses only recognized fields for the primitive type.
- [ ] Descriptions state both what the primitive does and when to use it.
- [ ] Agent tool lists avoid no-op tokens and use valid CLI tokens such as `read`, `grep`, `glob`, `edit`, `execute`, `web_fetch`, and `web_search`.
- [ ] Skill names are kebab-case, match their parent directory, and keep `SKILL.md` below 500 lines, preferably below 200.
- [ ] Instruction files include an auto-applying quoted `applyTo` string.
- [ ] Prompt files are treated as VS Code-only and not as CLI primitives.
- [ ] Cross-primitive references use primitive name and type; relative paths appear only inside a skill package.
- [ ] No uppercase double-brace placeholders, authoring notes, or unrelated edits remain.
- [ ] For `agent`, `instructions`, and `skill` primitives, validation passes: `python3 library/scripts/validate_primitives.py --strict`.
- [ ] For `agent`, `instructions`, and `skill` primitives, catalog drift check passes: `python3 library/scripts/generate_catalog.py --check`.
- [ ] For `prompt` primitives, do not claim validation from repository validators. Manually verify valid YAML frontmatter on line 1 with non-empty `name` and `description`, non-empty body, and no authoring placeholders; publish manually in `.github/prompts/` only if VS Code discovery is required; test with Chat: Run Prompt.
