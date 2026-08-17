---
name: 'new-skill'
description: 'Scaffold a new GitHub Copilot Agent Skill using the skill-creator skill workflow.'
agent: 'agent'
argument-hint: 'skill name and what it should do'
---

# New Skill

Scaffold a new skill under `library/skills/` by using `skill-creator` (type: skill) for the authoring workflow, validation expectations, and description optimization.

## First Step

Route the request to `skill-creator` (type: skill) before drafting or editing the skill. If that skill is unavailable in VS Code, stop and report that the required authoring primitive is missing.

## Inputs

Ask for any that are missing:

- **Skill name** (lowercase, hyphenated; becomes the folder name).
- **Purpose**: what it does and the concrete triggers (keywords, phrasings) that should activate it.
- Whether it needs **references** (on-demand Markdown), **assets** (templates), or **scripts** (runnable helpers).

## Steps

1. Create `library/skills/<name>/SKILL.md` with frontmatter on line 1:

   ```markdown
   ---
   name: <name>
   description: "<what it does> Use when <triggers and keywords>."
   ---

   # <Title>

   One-paragraph overview.

   ## When to use

   ## Workflow

   ## References
   ```

2. The folder name must equal `name`. Keep `description` within 1024 characters and rich with triggers.
3. Add `references/`, `assets/`, or `scripts/` only if needed, and reference each from `SKILL.md` (no dangling links).
4. Keep `SKILL.md` focused; push depth into `references/` (progressive disclosure).
5. Make any script self-contained (prefer standard library) and runnable in this environment.

## Rules

- Portable only: no sandbox home paths or `/mnt/...` paths, no hard platform-product dependency.
- English; "GitHub Copilot" not bare "Copilot"; no em dashes; never fabricate metrics.

## Done when

- The skill appears in the available-skills list (frontmatter parses).
- The folder name matches `name`, every referenced file exists, and any script runs.

## Output

Output concisely: return only the skill path, validation status, and any critical findings or blockers. Do not narrate the process steps.
