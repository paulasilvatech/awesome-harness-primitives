---
description: "Scaffold a new GitHub Copilot agent skill folder that follows the repository's authoring conventions."
agent: agent
argument-hint: "skill name and what it should do"
---

# New Skill

Scaffold a new skill under `.github/skills/` following [../instructions/skills-authoring.instructions.md](../instructions/skills-authoring.instructions.md). If the `skill-creator` skill is available, load it for the authoring workflow and description optimization.

## First step, always

If the `skill-creator` skill is available, load it before drafting or editing the skill. If it is not available, follow [../instructions/skills-authoring.instructions.md](../instructions/skills-authoring.instructions.md) directly.

## Inputs

Ask for any that are missing:

- **Skill name** (lowercase, hyphenated; becomes the folder name).
- **Purpose**: what it does and the concrete triggers (keywords, phrasings) that should activate it.
- Whether it needs **references** (on-demand Markdown), **assets** (templates), or **scripts** (runnable helpers).

## Steps

1. Create `.github/skills/<name>/SKILL.md` with frontmatter on line 1:

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
