---
description: "Requires routing, canonical paths, freshness evidence, frontmatter, tool-token, mirror, and validation conventions when editing Copilot primitives. Use when authoring or reviewing primitives, templates, or installed mirrors."
applyTo: ".github/copilot-instructions.md,.github/agents/*.agent.md,.github/instructions/*.instructions.md,.github/skills/**/SKILL.md,.github/prompts/*.prompt.md"
---

# Copilot Primitive Authoring Conventions — Harness-Compatible Files

These instructions apply to canonical Copilot primitive files matched by the
`applyTo` globs. They are authoritative for passive authoring invariants,
routing, canonical paths, frontmatter, tool tokens, validation, and
cross-primitive references; `.github/harness/COPILOT-HARNESS.md` wins for local
runtime discovery and schema.

## Authoritative Sources and Precedence

Use these sources together:

1. `.github/harness/COPILOT-HARNESS.md` as the local runtime contract for
   discovery, fields, tool vocabulary, and measured CLI divergence.
2. The matching instruction file for the primitive type.
3. Same-type primitives under `.github/` as examples only when they agree with
   the higher-priority sources.

There is no versioned primitive template library, mirror tree, synchronization
manifest, or root harness specification in this repository. Do not invent one.

## Responsibility Split

This file owns passive conventions that apply while editing primitive files. The
`copilot-primitive-authoring` skill owns ordered authoring steps and delivery
format. The `open-horizons-architect` agent owns ambiguous type choices,
primitive responsibility boundaries, and consultative suite-level architecture
reviews. Agents own persona, judgment
boundary, and authority. Instructions own passive conventions. Skills own
reusable procedures or criteria. Prompts own explicit VS Code actions.

## Routing and Canonical Paths

| Primitive | Canonical repository path | Routing convention |
| --- | --- | --- |
| Agent | `.github/agents/<name>.agent.md` | Use the primitive authoring procedure. |
| Instruction | `.github/instructions/<name>.instructions.md` | Use the primitive authoring procedure. |
| Skill | `.github/skills/<name>/SKILL.md` | Use the Agent Skill authoring procedure. |
| Prompt | `.github/prompts/<name>.prompt.md` | Use the primitive authoring procedure; treat prompts as VS Code-only. |

Treat `.github/` as the canonical source for repository primitives. This repository has no
checked-in primitive mirror or synchronization manifest; do not describe another path as canonical
unless both the source manifest and deterministic synchronization scripts are added. Use a valid
kebab-case primitive name with no path separators, `..`, leading or trailing hyphen, or double hyphen.

No primitive mirror or plugin source manifest is declared in this repository.
Do not create a second primitive copy or a `com.github.copilot/` directory.

## Frontmatter and Runtime Fields

- Use only fields recognized by the target primitive type.
- For instructions, only `applyTo`, `description`, `name`, and `excludeAgent` are recognized.
- Keep instruction `applyTo` present and set to one quoted, comma-separated glob string.
- Make every `description` a discovery surface that states what the primitive does and when to use it.
- For agents, treat `tools` as an allow-list filter, not a grant request. Omit it or use `["*"]` only when unrestricted access is intentional.
- Preserve the cross-surface vocabulary documented by the local harness.
  Official aliases include `read`, `search`, `edit`, `execute`, `agent`, `web`,
  and `todo`; measured local CLI companions include `grep`, `glob`,
  `web_fetch`, and `web_search`.
- For dual-surface agents, pair `search` with `grep` and/or `glob`, and pair
  `web` with `web_fetch` and/or `web_search` when those capabilities are needed.
- Do not use unsupported agent fields such as `agents`, `infer`, `mode`,
  `hidden`, `agent`, or `title`.
- For skills, set `name` to kebab-case and make it exactly match the parent directory. Keep `SKILL.md` under 500 lines, preferably under 200, and move bulk material into bundled resources.
- Treat prompts as VS Code-only files. They are repository primitives for authoring and distribution, but they are not discovered or executed by Copilot CLI.

## Cross-Primitive References

Reference other primitives by installed name and type, not by relative link. Use relative paths only inside the same skill package, such as `references/`, `scripts/`, `assets/`, or `templates/`. Consult references of the same primitive type as the target artifact so agent, instruction, skill, and prompt responsibilities do not bleed into one another.

No primitive mirrors are currently declared. If distribution is added later,
define one source manifest, deterministic generation, and a CI drift check
before creating a second copy.

## Freshness and Evidence

- Use the local harness contract before external research.
- Verify first-party documentation when the user asks for current or latest
  behavior, a relevant target version changed, local sources conflict, or the
  local contract marks a claim unresolved.
- Prefer a known official URL and use search only to locate a moved first-party page.
- Update `.github/harness/COPILOT-HARNESS.md` only when new evidence changes the
  local runtime contract. Do not describe an unverified assumption as current
  platform behavior.

## Good / Bad Examples

The examples below illustrate tool-token and discovery-surface rules.

**Good**

```yaml
description: "Review Copilot primitive files for harness compatibility. Use when validating agents, instructions, skills, or prompts."
tools: ["read", "search", "grep", "glob", "web", "web_fetch"]
```

Why: the description states what and when, and the tool list preserves both the
official aliases and measured local CLI companions.

**Bad**

```yaml
description: "Primitive helper."
tools: ["terminal", "run", "codebase"]
```

Why: the description is not actionable for discovery, and the listed tools are
not in either the documented alias set or measured local CLI set.

## Conventions

| Rule | Rationale |
| --- | --- |
| Treat `.github/` as the canonical repository source. | It is the only installed and versioned primitive surface in this repository. |
| Route `skill` work to `skill-creator`, and route `agent`, `instructions`, and `prompt` work to `copilot-primitive-authoring`. | Agent Skills have separate packaging rules, and other primitive types share authoring procedure. |
| Use valid kebab-case names and canonical paths. | Discovery and inventory generation remain deterministic. |
| Keep descriptions actionable and include when to use the primitive. | Agents and skills are selected from descriptions before full bodies load. |
| Use only recognized frontmatter fields and surface-aware tool tokens. | Unknown fields or missing companion tokens can silently break runtime behavior. |
| Reference primitives by name and type rather than relative links. | Runtime installation paths differ, but semantic names survive copying and packaging. |
| Keep volatile platform facts in the local harness contract and stable rules in primitives. | Runtime behavior has one repository evidence source. |
| Add mirrors only with a source manifest, deterministic generation, and drift validation. | Distribution copies must not become competing sources. |
| Validate primitives with repository scripts before delivery. | Markdown shape alone does not prove harness compatibility. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Preserve the established same-type structure and remove authoring residue. | Leave uppercase double-brace placeholders or authoring notes in a finished primitive. |
| Keep responsibilities separate between agent, instructions, skill, and prompt files. | Put a workflow in instructions or passive conventions in a skill procedure. |
| Use concise examples that prove the convention. | Add long tutorials or unrelated reference material to the primitive body. |
| Apply validation appropriate to the primitive type. | Treat a clean-looking Markdown file as runtime-compatible without type-specific checks. |
| Verify current claims conditionally against first-party sources. | Force network research for stable local edits or make current claims without evidence. |
| Preserve official aliases and measured local CLI companions where capabilities diverge. | Treat `search`, `web`, or `todo` as universally invalid, or assume they provide local CLI companions without evidence. |

## Checklist Before Opening a PR

- [ ] The edited file is the canonical `.github/` repository primitive.
- [ ] Frontmatter uses only recognized fields for the primitive type.
- [ ] Descriptions state both what the primitive does and when to use it.
- [ ] Agent tool lists preserve required official aliases and measured local CLI companions.
- [ ] Skill names are kebab-case, match their parent directory, and keep `SKILL.md` below 500 lines, preferably below 200.
- [ ] Instruction files include an auto-applying quoted `applyTo` string.
- [ ] Prompt files are treated as VS Code-only and not as CLI primitives.
- [ ] Cross-primitive references use primitive name and type; relative paths appear only inside a skill package.
- [ ] No uppercase double-brace placeholders, authoring notes, or unrelated edits remain.
- [ ] Current or latest claims are supported by dated first-party or runtime evidence.
- [ ] `python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict` passes.
- [ ] `python3 .github/skills/verify-skills.py` passes.
- [ ] `python3 scripts/update-copilot-inventory.py --check` passes.
- [ ] Prompt validation is reported accurately: repository validation covers local structure and metadata, while **Chat: Run Prompt** is still required to prove VS Code runtime behavior.
