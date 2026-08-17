---
name: skill-creator
description: "Create, audit, repair, and improve GitHub Copilot Agent Skills for VS Code, GitHub Copilot CLI, and GitHub Copilot cloud agent. Use when a user asks to create a skill, generate a SKILL.md, convert a workflow into a reusable skill, audit an existing skill, fix skill loading issues, optimize a skill description, validate frontmatter, or add references/scripts/assets to a skill package."
argument-hint: "skill name or folder, and what the skill should do"
---

# Skill Creator

Use this skill to create and improve portable Agent Skills that load correctly in GitHub Copilot, VS Code, GitHub Copilot CLI, and other skills-compatible agents. The output is a skill folder with a valid `SKILL.md`, optional bundled resources, and a validation pass before delivery.

## When to use

Use this skill when the user wants to:

- Create a new skill.
- Turn a conversation or repeated workflow into a reusable skill.
- Audit, repair, or modernize an existing skill folder.
- Diagnose why a skill does not appear or does not trigger.
- Optimize a skill description for better automatic loading.
- Add references, scripts, assets, test prompts, or review artifacts to a skill.

## Required skill format

Every skill folder follows this shape:

```text
skill-name/
  SKILL.md
  references/   optional, on-demand Markdown references
  scripts/      optional, runnable helpers
  assets/       optional, templates or static resources
```

The directory name must match the `name` field in `SKILL.md`. The `name` uses lowercase letters, numbers, and hyphens only. Avoid slashes, colons, dots, namespaces, spaces, and uppercase letters because invalid names can prevent discovery.

`SKILL.md` starts with YAML frontmatter on line 1:

```markdown
---
name: skill-name
description: What the skill does and when to use it, with concrete trigger phrases.
---

# Skill instructions
```

Required frontmatter keys:

- `name`: must match the folder.
- `description`: must explain both what the skill does and when to use it. Keep it at or below 1024 characters.

Supported optional keys in this repository:

- `argument-hint`
- `license`
- `user-invocable`
- `disable-model-invocation`

Avoid tool-specific fields such as `allowed-tools`. Use experimental fields such as `context` only when the target agent explicitly supports them and the repository policy allows them.

## Workflow

### 1. Clarify intent

Capture the smallest useful version of the skill before writing files. Ask or infer:

- What capability should the skill provide?
- What user requests should trigger it?
- What should the skill produce?
- Does it need references, scripts, assets, or all three?
- Does it need objective tests, human review, or both?
- Is it a project skill under `.github/skills/` or a personal skill under `~/.copilot/skills/`?

If the user asks to convert an existing conversation into a skill, extract the workflow, mistakes, corrections, commands, output formats, and validation steps from that conversation before asking new questions.

### 2. Choose the package shape

Keep `SKILL.md` focused on the core workflow and progressive disclosure. Move long domain knowledge into `references/`. Put repeatable deterministic work into `scripts/`. Put templates or examples into `assets/`.

Good split:

- `SKILL.md`: overview, when to use, workflow, output requirements, validation.
- `references/*.md`: detailed rules, examples, schemas, style guides.
- `scripts/*`: validators, renderers, converters, reproducible helpers.
- `assets/*`: templates, sample input, HTML review pages, icons, fixtures.

Every file referenced from `SKILL.md` must exist.

### 3. Write or update `SKILL.md`

Use clear imperative instructions. Explain why key steps matter instead of relying on rigid all-caps rules. Include:

- What the skill helps accomplish.
- When it should be used.
- Step-by-step workflow.
- Inputs and outputs.
- Validation commands.
- Pointers to bundled references, scripts, and assets.

Write the `description` for discovery. Include trigger phrases and near-synonyms a real user would type. Do not hide trigger guidance only in the body because the description is the primary discovery surface.

### 4. Add tests or review artifacts

For skills with objective output, write 3 to 5 realistic test prompts and expected checks. Store them in `evals/evals.json` if the user wants an evaluation loop. For subjective skills, provide a human review checklist instead of forcing weak quantitative assertions.

Use [references/schemas.md](references/schemas.md) for optional eval JSON shapes.

For trigger-description review, use [assets/eval_review.html](assets/eval_review.html) to review should-trigger and should-not-trigger prompts with the user.

### 5. Validate before delivery

Run the bundled validator on the skill folder:

```bash
python3 .github/skills/skill-creator/scripts/validate_skill.py .github/skills/<skill-name>
```

Also run repository gates when working in this repository:

```bash
/bin/bash .github/scripts/audit-skills.sh
/bin/bash .github/scripts/audit-primitives.sh
```

Fix every error before claiming the skill is ready.

### 6. Improve an existing skill

When updating a skill:

- Preserve the folder name and `name` field unless the user explicitly asks to rename it.
- Read the current skill before editing.
- Work with existing references, scripts, and assets instead of replacing the package blindly.
- Keep unrelated changes out.
- Validate the updated skill folder.

## Validation checklist

Before delivery, confirm:

- `SKILL.md` starts with frontmatter on line 1.
- `name` exists and matches the folder.
- `description` exists, is specific, and is at most 1024 characters.
- No unsupported frontmatter keys are present.
- No sandbox paths or hard platform leaks are present.
- No broken local file references exist.
- Every bundled script compiles or has a documented runtime requirement.
- Documentation is in English.
- User-facing copy writes "GitHub Copilot" in full.
- No em dashes are present.

## Bundled resources

- [references/schemas.md](references/schemas.md): optional JSON schemas for evals, grading, benchmark summaries, trigger eval sets, and feedback.
- [assets/eval_review.html](assets/eval_review.html): self-contained browser UI for reviewing trigger eval queries.
- [eval-viewer/generate_review.py](eval-viewer/generate_review.py): standard-library review viewer for comparing generated outputs and collecting feedback.
- [scripts/validate_skill.py](scripts/validate_skill.py): deterministic validator for Agent Skill package structure and repository conventions.

## Notes for portability

Prefer portable Agent Skills concepts over one-agent-only mechanics. This skill targets GitHub Copilot in VS Code, GitHub Copilot CLI, and GitHub Copilot cloud agent. If a requested workflow depends on a tool that is not available in the current environment, document the dependency and provide a graceful fallback.
