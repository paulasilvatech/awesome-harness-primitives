---
description: "Use when authoring, reviewing, or debugging a GitHub Copilot Agent Skill under .github/skills/ — SKILL.md frontmatter, the name-must-match-directory rule, description tuning for auto-loading, progressive disclosure, and bundled resources."
applyTo: ".github/skills/**/SKILL.md"
---

# Agent Skills — Authoring Guide

This file activates when you create or edit a `SKILL.md` under `.github/skills/`. It teaches how to author a skill that loads reliably and scopes cleanly: the two-key frontmatter schema, the rule that `name` must equal the skill's directory, how the `description` drives automatic loading, progressive disclosure, and how to bundle scripts and references. It teaches you how to structure and package a skill — it does not decide which skills this workshop needs or what a given skill's domain procedure should contain; that lives in each skill's own `SKILL.md` and in [`.github/copilot-instructions.md`](../copilot-instructions.md).

## What a Skill Is

A skill is a self-contained folder holding a `SKILL.md` plus optional bundled resources (scripts, references, templates, assets) that teaches Copilot a specialized, repeatable capability. Skills are not the same primitive as these instruction files:

| Primitive | Purpose | Loads |
|---|---|---|
| Instruction file (`*.instructions.md`) | Standing rules for files that match `applyTo` | Whenever a matching file is in context |
| Skill (`SKILL.md`) | An on-demand workflow or capability | Only when the request matches its `description` |

Skills are portable across VS Code, the Copilot CLI, and the Copilot coding agent, and they load progressively — the body and resources stay out of context until they are needed.

## Where Skills Live

| Location | Scope |
|---|---|
| `.github/skills/<skill-name>/` | This repository — where every workshop skill belongs |
| `~/.copilot/skills/<skill-name>/` | Personal, across all of your repositories |

Each skill owns its own directory and must contain at least a `SKILL.md`. This instruction file governs `.github/skills/**/SKILL.md`.

## Frontmatter — Only Two Keys

`SKILL.md` frontmatter accepts exactly two keys: `name` and `description`.

```yaml
---
name: "draw-io-diagram-generator"
description: "Use when creating, editing, or generating draw.io diagram files (.drawio, .drawio.svg, .drawio.png), flowcharts, architecture diagrams, sequence diagrams, ER diagrams, or UML class diagrams."
---
```

| Field | Required | Constraint |
|---|---|---|
| `name` | Yes | Lowercase letters, numbers, and hyphens only; 64 characters maximum; **must exactly equal the parent directory name** |
| `description` | Yes | States *when to use* the skill; keyword-dense; 1024 characters maximum |

> [!IMPORTANT]
> `name` must be identical to the skill's folder name. `.github/skills/draw-io-diagram-generator/SKILL.md` must declare `name: "draw-io-diagram-generator"`. If they differ — even by one capital letter or an underscore — the skill **silently fails to load**: there is no error and no warning; it is simply never offered to Copilot.

> [!WARNING]
> Only `name` and `description` are part of the schema. Keys such as `license`, `allowed-tools`, `compatibility`, and `metadata` are **not** recognized — they are ignored, and their presence gives a false impression that a constraint is enforced. Do not add them, and do not ship a `LICENSE.txt` on the assumption that a `license:` key wires it up.

## The description Drives Auto-Loading

Copilot reads only `name` and `description` during discovery, then decides whether to pull in the full skill. A vague description means the skill never activates. Include three things:

1. **What** the skill does (its capability).
2. **When** to use it — concrete triggers, file types, or phrasings the user would type.
3. **Keywords** the user is likely to mention.

Good — specific enough to activate reliably:

```yaml
description: "Use when creating, editing, or generating draw.io diagram files (.drawio, .drawio.svg, .drawio.png), flowcharts, sequence diagrams, or ER diagrams."
```

Poor — too vague to ever activate:

```yaml
description: "Diagram helpers"
```

Quote the value. Use single quotes when the description embeds double-quoted trigger phrases, so you do not have to escape them.

## Required Body Shape in This Repository

After the frontmatter, every workshop skill uses one `#` title in sentence case, then these sections in order. This is the standard the whole `.github/skills/` tree is held to:

- `## When to invoke` — three or four realistic, quoted user requests that should trigger the skill.
- One or more procedure sections — the actual decision tables, checklists, or step recipes.
- `## Output template` — a fenced block showing the exact artifact the skill produces.
- `## Quality gate` — a `- [ ]` checklist the work must pass before it is considered done.

```markdown
## When to invoke

- "Draw a sequence diagram for the payment flow."
- "Turn this ER sketch into a .drawio file."

## Generating the diagram

Decision tables, recipes, and style rules go here.

## Output template

The exact artifact the skill produces.

## Quality gate

- [ ] Verifiable criterion
```

Add `## Gotchas`, `## Troubleshooting`, or `## References` sections when they carry real signal, but the four above are mandatory.

## Progressive Disclosure

Skills load in three levels, so install cost stays low:

| Level | What loads | When |
|---|---|---|
| Discovery | `name` and `description` only | Always |
| Instructions | The full `SKILL.md` body | When the request matches the description |
| Resources | Scripts, references, templates | Only when the body links to them and Copilot follows the link |

Keep the `SKILL.md` body focused. Past roughly 200 lines, move deep material into `references/` and link to it, so Copilot pulls detail on demand instead of paying for it upfront. Treat about 500 lines as a hard ceiling.

## Bundling Resources

| Folder | Holds | Read into context? |
|---|---|---|
| `scripts/` | Executable automation (`.py`, `.sh`, `.ts`) | Only when run |
| `references/` | Documentation Copilot reads to decide | Yes, when linked |
| `templates/` | Scaffolds Copilot modifies and builds on | Yes, when linked |
| `assets/` | Static files emitted unchanged in output | No |

The `templates/` versus `assets/` split is about intent: if Copilot edits the file, it is a template; if the file is emitted as-is, it is an asset. Reference bundled files with paths relative to the skill directory, for example `[the validator](./scripts/validate-drawio.py)`.

Prefer a script over regenerated inline code when the same logic would be rewritten on each run, when deterministic behavior matters (file edits, API calls), or when the operation deserves its own tests. Scripts should expose `--help`, fail with clear messages, store no secrets, and use relative paths.

## Writing High-Impact Skills

- **Teach only what Copilot would otherwise get wrong.** Skip language syntax and first-page documentation; spend the budget on internal conventions, non-obvious defaults, version-specific quirks, and domain workflows.
- **Guard the shared description budget.** Every installed skill's description competes for the same discovery window. Keep descriptions short and keyword-dense.
- **Gotchas are the highest-signal content.** A proactive "never do X because Y" prevents a whole class of mistakes; add one every time Copilot produces a wrong result.
- **Prefer flexible guidance to rigid steps** for open-ended work. Reserve numbered steps for procedures where sequence truly matters (build, deploy, setup).

Rigid steps bind Copilot to one file layout and rot quickly:

```text
1. Open src/api/handlers.ts
2. Find processOrder
3. Add a try-catch around lines 45-60
```

Flexible guidance adapts to the real code:

```text
When hardening error handling in API handlers:
- Wrap every database call in the project's error-handling utility
- Log failures with enough context to debug in production
```

## Conventions

| Rule | Rationale |
|---|---|
| Frontmatter carries only `name` and `description` | Any other key is ignored and hides a false assumption |
| `name` equals the skill's directory name exactly | A mismatch makes the skill silently fail to load |
| `description` says *when* to use the skill, in 1024 keyword-dense characters or fewer | It is the only text discovery sees; vague text never activates |
| Body follows `## When to invoke` then a procedure then `## Output template` then `## Quality gate` | Matches the standard every workshop skill is held to |
| Deep detail moves to `references/` past roughly 200 lines | Keeps the discovery and instruction levels cheap |
| Scripts expose `--help`, handle errors, and store no secrets | Bundled automation must be safe and self-describing |

## Do / Do Not

| Do | Do not |
|---|---|
| Name the folder and `name` identically | Rename one without the other |
| Write a trigger-rich `description` | Ship a vague description such as "helpers" |
| Keep only `name` and `description` in frontmatter | Add `license`, `allowed-tools`, `compatibility`, or `metadata` |
| Link bundled files with relative paths | Hardcode absolute or machine-specific paths |
| Split large skills into `references/` | Let one `SKILL.md` grow past roughly 500 lines |
| Put the four required sections in every skill | Drop `## When to invoke`, `## Output template`, or `## Quality gate` |

## Checklist Before Opening a PR

- [ ] `SKILL.md` frontmatter contains only `name` and `description`, both quoted
- [ ] `name` is lowercase and hyphenated, 64 characters or fewer, and identical to the parent directory name
- [ ] `description` states what the skill does and when to use it, and stays within 1024 characters
- [ ] The body has `## When to invoke`, at least one procedure section, `## Output template`, and `## Quality gate`
- [ ] Content teaches non-obvious knowledge, not language syntax or first-page docs
- [ ] Any bundled scripts, references, templates, or assets are linked with relative paths
- [ ] The body stays focused, with deep detail in `references/`, and no emoji or inline lint pragma was introduced
