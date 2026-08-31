---
paths:
  - harness/github-copilot/agents/*.agent.md
  - harness/github-copilot/instructions/*.instructions.md
  - harness/github-copilot/skills/**/SKILL.md
  - harness/github-copilot/prompts/*.prompt.md
  - docs/templates/*.md
  - ".github/copilot-instructions.md"
  - ".github/agents/*.agent.md"
  - ".github/instructions/*.instructions.md"
  - ".github/skills/**/SKILL.md"
  - ".github/prompts/*.prompt.md"
---

<!-- Generated from harness/github-copilot/instructions/copilot-primitive-authoring.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Requires routing, canonical paths, freshness evidence, frontmatter, tool-token, mirror, and validation conventions when editing Copilot primitives. Use when authoring or reviewing primitives, templates, or installed mirrors.

# Copilot Primitive Authoring Conventions — Harness-Compatible Files

These instructions apply to Copilot primitive files, templates, and installed mirrors matched by the `applyTo` globs. They are authoritative for passive authoring invariants, routing, canonical paths, freshness evidence, frontmatter, tool tokens, validation, and cross-primitive references; the repository-wide governance instructions own global precedence and synchronization, while `docs/COPILOT-HARNESS-SPEC.md` wins for runtime discovery and schema.

## Authoritative Sources and Precedence

Use these sources together:

1. `docs/COPILOT-HARNESS-SPEC.md` as the maintained contract for CLI-discovered agents, instructions, skills, plugins, hooks, fields, tool tokens, and validation semantics.
2. `docs/HARNESS-VALIDATION.md` for dated runtime evidence, tested versions, divergences, and unverified claims. When this evidence contradicts the spec, update the spec before dependent guidance.
3. `docs/templates/` for this repository's expected primitive shapes and reusable section patterns.
4. `docs/references/` for calibrated examples of concise, scoped, rationale-driven instructions.

Do not copy a reference file's domain-specific content into a primitive authoring rule.

## Responsibility Split

This file owns passive conventions that apply while editing primitive files. The `copilot-primitive-authoring` skill owns ordered authoring steps, evidence gathering, validation sequencing, and delivery format. The `copilot-primitive-architect` agent owns ambiguous type choices and consultative suite-level architecture reviews. Agents own persona, judgment boundary, and authority. Instructions own passive conventions. Skills own reusable procedures or criteria. Prompts own explicit VS Code actions.

## Routing and Canonical Paths

| Primitive | Canonical library path | Routing convention |
| --- | --- | --- |
| Agent | `harness/github-copilot/agents/<name>.agent.md` | Use the `copilot-primitive-authoring` skill for procedure. |
| Instruction | `harness/github-copilot/instructions/<name>.instructions.md` | Use the `copilot-primitive-authoring` skill for procedure. |
| Skill | `harness/github-copilot/skills/<name>/SKILL.md` | Use the `skill-creator` skill. |
| Prompt | `harness/github-copilot/prompts/<name>.prompt.md` | Use the `copilot-primitive-authoring` skill for procedure; treat prompts as VS Code-only. |

Treat `harness/github-copilot/` as the canonical source for reusable primitives. Do not edit `.github/` mirrors, generated compatibility guidance, or plugin copies directly unless a file has no declared source. Use a valid kebab-case primitive name with no path separators, `..`, leading or trailing hyphen, or double hyphen.

GitHub Copilot plugin packages keep installable components directly under the plugin root:
`agents/`, `skills/`, `hooks/`, `extensions/`, and `mcp.json`. The distributed `plugin.json` uses
direct component path fields and omits the Agent Plugins `$schema`. Repository-only source ownership
lives in `harness/github-copilot/manifests/plugin-sources.json`. Do not create
`com.github.copilot/` directories.

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

Generate declared repository mirrors with `python3 harness/github-copilot/scripts/sync_installed_primitives.py`. Generate plugin-local components with `python3 harness/github-copilot/scripts/sync_plugin_components.py`. Never resolve drift by editing both copies.

## Freshness and Evidence

- Use repository manifests, the harness spec, and dated validation evidence before external research.
- Verify first-party documentation when the user asks for current or latest behavior, a relevant target version changed, local sources conflict, a claim is marked unverified, or affected platform evidence is older than 90 days.
- Prefer a known official URL and use search only to locate a moved first-party page.
- Record the source URL, target product or version, verification date, result, and divergence in `docs/HARNESS-VALIDATION.md`; then update the spec and dependent guidance.
- Do not refresh a date without repeating the check, and do not describe an undated assumption as current platform behavior.

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
| Treat `harness/github-copilot/` as the canonical source and avoid direct `.github/` mirror edits. | Mirrors can be regenerated or synchronized, so direct edits drift and disappear. |
| Route `skill` work to `skill-creator`, and route `agent`, `instructions`, and `prompt` work to `copilot-primitive-authoring`. | Agent Skills have separate packaging rules, and other primitive types share authoring procedure. |
| Use valid kebab-case names and canonical paths. | Discovery, catalog generation, mirroring, and plugin packaging remain deterministic. |
| Keep descriptions actionable and include when to use the primitive. | Agents and skills are selected from descriptions before full bodies load. |
| Use only recognized frontmatter fields and valid tool tokens. | Unknown fields or no-op tokens silently break runtime behavior. |
| Reference primitives by name and type rather than relative links. | Runtime installation paths differ, but semantic names survive copying and packaging. |
| Keep volatile platform facts in dated validation evidence and stable rules in primitives. | Current behavior can be refreshed once without duplicating dates and version claims. |
| Synchronize declared installed and plugin copies with repository scripts. | Canonical content cannot drift across distribution surfaces. |
| Validate primitives with repository scripts before delivery. | Markdown shape alone does not prove harness compatibility. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Start from the matching template and remove template-only notes before saving. | Leave uppercase double-brace placeholders or authoring notes in a finished primitive. |
| Keep responsibilities separate between agent, instructions, skill, and prompt files. | Put a workflow in instructions or passive conventions in a skill procedure. |
| Use concise examples that prove the convention. | Add long tutorials or unrelated reference material to the primitive body. |
| Apply validation appropriate to the primitive type. | Treat a clean-looking Markdown file as runtime-compatible without type-specific checks. |
| Verify current claims conditionally against first-party sources. | Force network research for stable local edits or refresh dates without evidence. |
| Use `read`, `grep`, `glob`, `edit`, `execute`, `web_fetch`, and `web_search` where those capabilities are needed. | Use `search`, `web`, `todo`, `all`, `terminal`, `run`, `codebase`, `changes`, `fetch`, or `githubRepo` as CLI tool tokens. |

## Checklist Before Opening a PR

- [ ] The edited file is the canonical `harness/github-copilot/` source unless the task explicitly targets an installed mirror.
- [ ] Frontmatter uses only recognized fields for the primitive type.
- [ ] Descriptions state both what the primitive does and when to use it.
- [ ] Agent tool lists avoid no-op tokens and use valid CLI tokens such as `read`, `grep`, `glob`, `edit`, `execute`, `web_fetch`, and `web_search`.
- [ ] Skill names are kebab-case, match their parent directory, and keep `SKILL.md` below 500 lines, preferably below 200.
- [ ] Instruction files include an auto-applying quoted `applyTo` string.
- [ ] Prompt files are treated as VS Code-only and not as CLI primitives.
- [ ] Cross-primitive references use primitive name and type; relative paths appear only inside a skill package.
- [ ] No uppercase double-brace placeholders, authoring notes, or unrelated edits remain.
- [ ] Current or latest claims are supported by dated first-party or runtime evidence.
- [ ] All primitive types pass `python3 harness/github-copilot/scripts/validate_primitives.py --strict`.
- [ ] Plugin normalization, marketplace audit, catalog, plugin component, and declared installed-copy drift checks pass.
- [ ] Prompt validation is reported accurately: repository validation covers local structure and metadata, while **Chat: Run Prompt** is still required to prove VS Code runtime behavior.
