---
name: copilot-primitive-authoring
description: "Author GitHub Copilot agents, instructions, and VS Code prompts in this repository. Use when asked to create or update an agent, instructions file, or VS Code prompt with a known primitive type, using repository templates, canonical library paths, and type-specific validation."
---

# Copilot primitive authoring

Author GitHub Copilot agents, instructions, and VS Code prompt primitives by routing to the correct primitive contract, starting from repository templates, writing canonical `library/` sources, and validating only with gates that apply to the selected type.

## When to invoke

- "Create a Copilot agent for this repository."
- "Write custom instructions for these files."
- "Create a VS Code prompt from this workflow."
- "Update this agent, instructions, or prompt primitive."
- "Build a primitive suite using the repository templates."

## Prerequisites and context

- Canonical source paths are `library/agents/`, `library/instructions/`, `library/prompts/`, and `library/skills/`.
- Source templates live in `docs/templates/`: `agent.template.md`, `instructions.template.md`, `prompt.template.md`, and `skill.template.md`.
- The harness contract is `docs/COPILOT-HARNESS-SPEC.md`; it is authoritative for CLI-discovered agents, instructions, skills, plugins, hooks, and validation.
- VS Code prompts are VS Code-only. GitHub Copilot CLI does not discover or execute prompt primitives.
- For creating, auditing, repairing, or optimizing Agent Skills, invoke `skill-creator` (skill) instead of reimplementing that workflow.
- For consultative architectural review or primitive type selection, use `copilot-primitive-architect` (agent).

## Primitive routing

| User intent | Primitive type | Canonical destination | This skill action |
| --- | --- | --- | --- |
| Persona, judgment boundary, operating posture, tool policy, handoff behavior | Agent | `library/agents/<name>.agent.md` | Continue. |
| Passive conventions for matching files | Instructions | `library/instructions/<name>.instructions.md` | Continue. |
| Focused VS Code action explicitly run by a user | Prompt | `library/prompts/<name>` prompt markdown file | Continue, but do not claim CLI validation. |
| Specialized reusable workflow with optional bundled resources | Skill | `library/skills/<name>/SKILL.md` | Hand off to `skill-creator` (skill). |
| Ambiguous type or architecture review | Unknown | None | Use `copilot-primitive-architect` (agent). |

## Procedure

1. Route by primitive type before reading templates or writing files.
2. Validate the requested name against `^[a-z0-9]+(-[a-z0-9]+)*$`: kebab-case only, no path separators, no `..`, no leading or trailing hyphen, and no double hyphen.
3. Derive the canonical path from the type and refuse any destination outside the matching `library/` path.
4. Copy the matching template from `docs/templates/` instead of inventing structure.
5. Place the file only at the canonical `library/` source path. Do not manually edit `.github/` mirrors, generated plugin copies, or packaged plugin components.
6. Fill frontmatter according to the harness spec:
   - Agents require `description`; omit `name` and `model` unless there is a concrete reason. If restricting tools, use valid CLI tokens only.
   - Instructions may use `applyTo`, `description`, `name`, and `excludeAgent`; use one quoted comma-separated glob string for `applyTo` when auto-application is intended.
   - Prompts follow the VS Code prompt schema and may keep VS Code runtime inputs such as `${selection}` only when intentional.
   - Skills require `name` and `description`; detailed skill decisions belong to `skill-creator`.
7. Write the body to match the type contract: agents define mission and operating posture; instructions define conventions and verification; prompts define invocation, inputs, behavior, destination handling, and done criteria.
8. Reference related primitives by installed name and type, such as `dependency-review` (skill), never by cross-primitive relative links.
9. Remove template placeholders, authoring notes, unused alternatives, and unsupported frontmatter keys.
10. Validate according to primitive type and update generated catalogs only when the canonical source change causes drift.

## Validation matrix

| Type | Validation |
| --- | --- |
| Agent | `python3 library/scripts/validate_primitives.py --strict` and `python3 library/scripts/generate_catalog.py --check`. |
| Instructions | `python3 library/scripts/validate_primitives.py --strict` and `python3 library/scripts/generate_catalog.py --check`. |
| Skill handoff | `skill-creator` owns skill validation; do not duplicate it here. |
| Prompt | Manually verify YAML frontmatter starts on line 1, `name` and `description` are non-empty, body is non-empty, and no authoring placeholders remain. Test in VS Code with Chat: Run Prompt when discovery is required. |

If `generate_catalog.py --check` reports drift caused by your canonical source change, run the corresponding generator, then rerun the check.

## Limits

- Do not use this skill to create, repair, or audit Agent Skills directly. Use `skill-creator` (skill).
- Do not use this skill for consultative primitive reviews or type-selection decisions. Use `copilot-primitive-architect` (agent).
- Do not manually edit `.github/` mirrors, plugin-generated copies, packaged plugin components, or `library/plugins/`.
- Do not treat prompts as CLI primitives.
- Do not add no-op CLI tool tokens such as `search`, `web`, or `todo`; they do not grant capability in GitHub Copilot CLI.
- Do not leave placeholders, authoring notes, unused optional sections, or unsupported frontmatter keys in final primitives.

## Gotchas

- **Tool names are surface-specific:** VS Code prompt tool IDs such as `search/codebase` must not be copied into CLI agent `tools` or skill `allowed-tools`.
- **No-op CLI tokens are misleading:** `search`, `web`, and `todo` look useful but grant nothing in CLI. Use valid tokens from the harness spec or omit the allow-list when unrestricted access is intended.
- **Instructions are passive:** If the requested artifact has ordered setup, migration, generation, or review steps, use a skill or prompt instead of instructions.
- **Catalog drift is expected after new primitives:** Run the generator when the check command reports drift caused by your canonical source change.

## Repository resources

Read these repository sources as needed for the current primitive type:

| Resource | Use when |
| --- | --- |
| `docs/templates/README.md` | Selecting templates and checking cross-type rules. |
| `docs/templates/agent.template.md` | Authoring an agent. |
| `docs/templates/instructions.template.md` | Authoring instructions. |
| `docs/templates/prompt.template.md` | Authoring a VS Code prompt. |
| `docs/templates/skill.template.md` | Understanding skill package expectations before handing off to `skill-creator`. |
| `docs/COPILOT-HARNESS-SPEC.md` | Checking runtime and validation rules. |
| `docs/references/` | Comparing against finished primitive examples. |

## Compatibility vocabulary

Use the exact primitive labels `agent`, `instructions`, `prompt`, and `skill` when reporting classification. Legacy repository docs may mention `.github/prompts/`, `github/prompts/`, `library/prompts/<name>` prompt file, and legacy prompt file suffixes; treat those as VS Code prompt publication patterns, not GitHub Copilot CLI runtime primitives. Preserve `prompt-only`, `non-check`, and `upper-snake-case` terminology when explaining validation or cleanup.

## Output template

```markdown
## Primitive authoring result

**Status:** Done | Blocked | Needs follow-up
**Primitive type:** Agent | Instructions | Prompt | Skill handoff | Mixed suite
**Paths:** <created canonical library paths>

### Summary
<one or two sentences describing what changed>

### Validation
- `python3 library/scripts/validate_primitives.py --strict`: <pass, fail, or not run with reason>
- `python3 library/scripts/generate_catalog.py --check`: <pass, fail, or not run with reason>
- Prompt manual validation and Chat: Run Prompt test: <pass, fail, or not applicable with reason>

### Follow-up
<catalog updates, synchronization, open questions, or `None`>
```

## Quality gate

- [ ] Routing by primitive type happened before authoring work.
- [ ] The primitive type is explicitly classified and matches the user's requested outcome.
- [ ] The requested name is valid kebab-case and the destination exactly matches the canonical path for that type.
- [ ] The file starts from the matching `docs/templates/` template or the handoff to `skill-creator` is explicit.
- [ ] Final frontmatter satisfies the harness spec for that primitive type.
- [ ] Canonical paths under `library/` are used, and generated mirrors are not edited manually.
- [ ] Related primitives are referenced by name and type, not by cross-primitive relative links.
- [ ] Prompts are documented as VS Code-only when selected.
- [ ] No double-brace template placeholders, authoring notes, unused alternatives, or unsupported keys remain.
- [ ] Validation matched the primitive type, and prompt primitives were not declared validated by repository validators.
