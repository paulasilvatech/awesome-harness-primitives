---
name: skill-creator
description: "Create, audit, repair, and improve GitHub Copilot Agent Skills for VS Code, GitHub Copilot CLI, and GitHub Copilot cloud agent. Use when a user asks to create a skill, generate a SKILL.md, convert a workflow into a reusable skill, audit an existing skill, fix skill loading issues, optimize a skill description, validate frontmatter, or add references/scripts/assets to a skill package."
argument-hint: "skill name or folder, and what the skill should do"
---

# Skill creator

Create or repair a portable GitHub Copilot Agent Skill by shaping a valid skill folder, writing a focused `SKILL.md`, adding only useful bundled resources, and validating the result before delivery.

## When to invoke

- "Create a new GitHub Copilot skill."
- "Generate a SKILL.md for this workflow."
- "Audit this skill folder and fix loading issues."
- "Optimize this skill description so it triggers correctly."
- "Add references, scripts, or assets to this skill package."

## Inputs

Use `$ARGUMENTS` as the requested skill name, existing folder, or capability description. If `$ARGUMENTS` is empty, infer the target from the user's message and current workspace; if that is still ambiguous, inspect likely skill folders before choosing a safe default.

## Required skill package

Every skill folder must contain `SKILL.md` and may contain bundled resources loaded on demand:

```text
skill-name/
  SKILL.md
  references/   optional, on-demand Markdown references
  scripts/      optional, runnable helpers
  assets/       optional, templates or static resources
```

| Element | Rule |
| --- | --- |
| Folder name | Match the `name` field exactly. Use lowercase letters, numbers, and hyphens only. Avoid slashes, colons, dots, namespaces, spaces, and uppercase letters. |
| `SKILL.md` | Start YAML frontmatter on line 1, followed by exactly one H1 and skill instructions. |
| `name` | Required. Match the parent folder. |
| `description` | Required. Explain what the skill does and when to use it. Keep it at or below 1024 characters. |
| Optional keys | Use only `argument-hint`, `compatibility`, `license`, `user-invocable`, `disable-model-invocation`, `allowed-tools`, `metadata`, and `tags`. |
| `compatibility` | Optional, at or below 500 characters. Use only for a real environment requirement, and repeat it in the body because current GitHub Copilot surfaces do not enforce it. |
| Unsupported keys | Do not use top-level `context`, `authors`, `category`, or `version`; move useful annotations under `metadata`. |

Minimum frontmatter shape:

```markdown
---
name: skill-name
description: What the skill does and when to use it, with concrete trigger phrases.
---

# Skill instructions
```

## Procedure

1. Clarify or infer the smallest useful capability without all-caps directives: triggers, output, required resources, validation needs, and whether the package belongs under `.github/skills/` or `~/.copilot/skills/`.
2. Read any existing skill before editing. Preserve the folder name and `name` field unless the user explicitly asks to rename it.
3. Choose the package shape: keep `SKILL.md` focused, move long knowledge to `references/`, deterministic repeatable work to `scripts/`, and static templates or examples to `assets/`.
4. Write or update `SKILL.md` in clear imperative language and step-by-step workflow only when order matters with discovery-focused `description`, workflow, inputs, outputs, validation, and resource pointers.
5. For objective outputs, add 3 to 5 realistic test prompts with near-synonyms and expected checks and expected checks in `evals/evals.json` when the user wants an evaluation loop; for subjective skills, provide a human review checklist.
6. Validate the skill folder and repository gates when working in this repository.

## Resource placement

| Resource | Use for | Notes |
| --- | --- | --- |
| `SKILL.md` | Overview, when to invoke, core workflow, output, quality gate. | Keep focused and portable. |
| `references/*.md` | Detailed rules, schemas, style guides, examples. | Read on demand, not automatically. |
| `scripts/*` | Validators, renderers, converters, reproducible helpers. | Document runtime requirements; scripts must not store credentials. |
| `assets/*` | Templates, sample input, HTML review pages, icons, fixtures. | Use as static resources unless the skill explicitly edits a copy. |
| `evals/evals.json` | Optional objective trigger or output evaluations and trigger-description review data. | Use `references/schemas.md` for skills-compatible shapes. |

## Validation commands

Run the bundled validator on the skill folder:

```bash
python3 .github/skills/skill-creator/scripts/validate_skill.py .github/skills/<skill-name>
```

When working in this repository, also run:

```bash
python3 harness/github-copilot/scripts/validate_primitives.py --strict
python3 harness/github-copilot/scripts/audit_primitive_content.py --check
python3 harness/github-copilot/scripts/audit_primitive_capabilities.py --check
python3 harness/github-copilot/scripts/audit_primitive_redundancy.py --check
python3 harness/github-copilot/scripts/generate_catalog.py --check
```

Fix every error before claiming the skill is ready. If the validator path differs because the skill is installed elsewhere, use the equivalent `scripts/validate_skill.py` in this package.

## Quality checklist

- [ ] `SKILL.md` starts with frontmatter on line 1.
- [ ] `name` exists and matches the folder.
- [ ] `description` is specific, discovery-focused, and at most 1024 characters.
- [ ] No unsupported frontmatter keys remain.
- [ ] No sandbox paths or hard platform leaks remain.
- [ ] No broken local file references remain.
- [ ] Every bundled script compiles or documents its runtime requirement.
- [ ] Documentation is in English and writes "GitHub Copilot" in full.
- [ ] Existing references, scripts, and assets are preserved unless intentionally replaced.

## Progressive disclosure and bundled resources

- `references/schemas.md`: optional JSON schemas for evals, grading, benchmark summaries, trigger eval sets, and feedback.
- `assets/eval_review.html`: self-contained browser UI for reviewing should-trigger and should-not-trigger prompts with the user.
- `eval-viewer/generate_review.py`: standard-library review viewer for comparing generated outputs and collecting feedback.
- `scripts/validate_skill.py`: deterministic validator for Agent Skill package structure and repository conventions.

## Gotchas

- Preserve step-by-step detail when sequence is load-bearing; do not collapse by-step workflow evidence into vague prose.
- **Do not hide trigger guidance only in the body**; `description` is the primary discovery surface.
- **Do not replace a package blindly**; work with existing references, scripts, and assets.
- **Do not use one-agent-only mechanics unless required**; prefer portable Agent Skills concepts for VS Code, GitHub Copilot CLI, and GitHub Copilot cloud agent.
- **Do not assume unavailable tools**; document the dependency and provide a graceful fallback.

## Output template

```markdown
## Skill package result

**Status:** created | updated | repaired | blocked
**Skill:** `<skill-name>`
**Location:** `<path>`

### Package contents
| Path | Purpose | Created/changed |
| --- | --- | --- |
| `SKILL.md` | <purpose> | <created|changed|unchanged> |

### Discovery
- Name: `<name>`
- Description: <why it triggers for the requested use case>

### Validation
- `scripts/validate_skill.py`: <pass|fail|not run and why>
- Repository gates: <pass|fail|not applicable>
```

## Quality gate

- [ ] `$ARGUMENTS` or the user's request was consumed to identify the target skill.
- [ ] The folder name and `name` field match exactly.
- [ ] Required and optional frontmatter keys follow the supported schema.
- [ ] The description states what the skill does and when to use it with concrete triggers.
- [ ] Bundled resources are referenced only when they exist and are useful on demand.
- [ ] Validation commands were run or the blocker is reported with the exact missing prerequisite.
