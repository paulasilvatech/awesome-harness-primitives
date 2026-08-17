---
name: copilot-primitive-authoring
description: "Author GitHub Copilot agents, instructions, and VS Code prompts in this repository. Use when asked to create or update an agent, instructions file, or prompt with a known primitive type, using repository templates, canonical library paths, and type-specific validation."
---

# Copilot Primitive Authoring

Use this skill to author GitHub Copilot agents, instructions, and VS Code prompts in this repository by applying the canonical template, satisfying the harness contract, validating the result, and updating generated catalogs when applicable.

## When to invoke

- "Create a Copilot agent for this repository."
- "Write custom instructions for these files."
- "Create a VS Code prompt from this workflow."
- "Build an agent, instructions, or prompt primitive suite using the repository templates."

## Prerequisites and context

- Canonical source paths are under `library/`: `library/agents/`, `library/instructions/`, `library/prompts/`, and `library/skills/`.
- Source templates live in `docs/templates/`: `agent.template.md`, `instructions.template.md`, `prompt.template.md`, and `skill.template.md`.
- The harness contract is in `docs/COPILOT-HARNESS-SPEC.md`; it is the authority for CLI-discovered agents, instructions, skills, plugins, hooks, and validation.
- Prompts are VS Code-only. GitHub Copilot CLI does not discover or execute `*.prompt.md`.
- For creating, auditing, repairing, or optimizing Agent Skills, invoke the `skill-creator` skill by name instead of reimplementing that workflow.
- For consultative architectural review or primitive type selection, use `copilot-primitive-architect` (agent).

## Procedure

1. **Route by primitive type before any other work.** Decide exactly one path before reading templates, writing files, or validating output:
   - Type `skill`: use `skill-creator` (skill). This skill does not create or audit Agent Skills.
   - Type `agent`, `instructions`, or `prompt`: continue with this skill.
   - Ambiguous type, choosing between types, or consultative architectural review: use `copilot-primitive-architect` (agent).
   - Consult references of the same type as the target artifact.
2. **Classify the target contract.** Confirm the selected type maps to exactly one canonical target:
   - Agent: persona, judgment boundary, operating posture, tool policy, and handoff behavior. Use `library/agents/<name>.agent.md`.
   - Instructions: passive conventions for matching files. Use `library/instructions/<name>.instructions.md`.
   - Prompt: focused VS Code action explicitly run by a user. Use `library/prompts/<name>.prompt.md` and keep VS Code-only runtime inputs such as `${selection}` only when intentional.
3. **Validate the name and destination before creating the file.** The name must match `^[a-z0-9]+(-[a-z0-9]+)*$`: kebab-case only, no path separators, no `..`, no leading or trailing hyphen, and no double hyphen. Derive the destination from the type and name, then refuse any destination that does not exactly match the canonical path:
   - Agent: `library/agents/<name>.agent.md`.
   - Instructions: `library/instructions/<name>.instructions.md`.
   - Prompt: `library/prompts/<name>.prompt.md`.
   - Skill handoff: `library/skills/<name>/SKILL.md`, handled only by `skill-creator`.
4. **Copy the matching template from `docs/templates/`.** Start from the closest template instead of inventing structure:
   - `docs/templates/agent.template.md` for agents.
   - `docs/templates/instructions.template.md` for instructions.
   - `docs/templates/prompt.template.md` for prompts.
   - `docs/templates/skill.template.md` only when the `skill-creator` skill is handling a skill package.
5. **Place the file at the canonical `library/` path.** Do not manually edit mirrors in `.github/`, generated plugin copies, or packaged plugin components. Use synchronization scripts for generated copies.
6. **Fill frontmatter according to the harness spec.**
   - Agents require `description`; omit `name` and `model` unless there is a concrete reason. If restricting tools, use valid CLI tokens only.
   - Instructions may use `applyTo`, `description`, `name`, and `excludeAgent`; use one quoted comma-separated glob string for `applyTo` when auto-application is intended.
   - Prompts follow the VS Code prompt schema and are not CLI primitives. Do not copy prompt-only tool IDs into agent or skill frontmatter.
   - Skills require `name` and `description`; delegate detailed skill format decisions to `skill-creator`.
7. **Write the body to match the type contract.** Agents define mission, activation, operating principles, procedure, limits, output, and done criteria. Instructions define scope, precedence, conventions, examples, and verification. Prompts define VS Code invocation, preconditions, runtime inputs, destination behavior, prompt body, and definition of done.
8. **Reference related primitives by installed name and type.** Write references such as "Use `dependency-review` (skill)". Do not use relative links between separate primitives because installation paths differ.
9. **Remove every template placeholder and authoring note.** Search the changed primitive or skill folder for double-brace template markers; no upper-snake-case template placeholders may remain.
10. **Validate according to primitive type.** Run only gates that actually cover the selected type, and never claim prompt validation from repository validators:
   - For `agent`, `instructions`, or `skill`, run:
   ```sh
   python3 library/scripts/validate_primitives.py --strict
   python3 library/scripts/generate_catalog.py --check
   ```
   - For `prompt`, no repository validator exists. Manually verify valid YAML frontmatter starts on line 1, `name` and `description` are non-empty, the body is non-empty, and no authoring placeholders remain. Publish manually to `.github/prompts/` only when VS Code discovery is required, and test with **Chat: Run Prompt** in a representative scenario.
11. **Update generated catalog or synchronized copies when applicable.** If `generate_catalog.py --check` or another synchronization check reports drift caused by the canonical source change, run the corresponding non-check command, then rerun the check command.
12. **Self-check only the artifact you produced.** Confirm the created or updated artifact satisfies this workflow and the selected type contract. Route broader consultative review to `copilot-primitive-architect` (agent).
13. **Report the result with evidence.** Include created paths, classification rationale, validation commands, command outcomes, and any follow-up that remains.

## Output template

Return exactly this structure:

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

## Limits

- Do not use this skill to create, repair, or audit Agent Skills directly. Use `skill-creator` (skill) for that work.
- Do not use this skill for consultative primitive reviews or type-selection decisions. Use `copilot-primitive-architect` (agent) for that work.
- Do not manually edit `.github/` mirrors, plugin-generated copies, or packaged plugin components. Edit canonical `library/` sources and use the repository synchronization scripts.
- Do not treat prompts as CLI primitives. Prompts are VS Code-only and require VS Code runtime and publication handling.
- Do not add no-op CLI tool tokens such as `search`, `web`, or `todo`; they do not grant capability in GitHub Copilot CLI.
- Do not leave placeholders, authoring notes, unused optional sections, or unsupported frontmatter keys in final primitives.

## Gotchas

- **Tool names are surface-specific:** VS Code prompt tool IDs such as `search/codebase` must not be copied into CLI agent `tools` or skill `allowed-tools`.
- **No-op CLI tokens are misleading:** `search`, `web`, and `todo` look useful but grant nothing in CLI. Use valid tokens from the harness spec or omit the allow-list when unrestricted access is intended.
- **Instructions are passive:** If the requested artifact has ordered setup, migration, generation, or review steps, use a skill or prompt instead of instructions.
- **Catalog drift is expected after new primitives:** Run the generator when the check command reports drift caused by your canonical source change.

## Repository resources

Read these repository sources as needed for the current primitive type:

- `docs/templates/README.md` for template selection and cross-type rules.
- `docs/templates/agent.template.md` for agent structure.
- `docs/templates/instructions.template.md` for instructions structure.
- `docs/templates/prompt.template.md` for VS Code prompt structure.
- `docs/templates/skill.template.md` plus `skill-creator` (skill) for skill packages.
- `docs/COPILOT-HARNESS-SPEC.md` for authoritative runtime and validation rules.
- `docs/references/` for examples of finished primitives.

## Quality gate

- [ ] Routing by primitive type happened before any authoring work.
- [ ] The primitive type is explicitly classified and matches the user's requested outcome.
- [ ] The requested name is valid kebab-case and the destination exactly matches the canonical path for that type.
- [ ] The file starts from the matching `docs/templates/` template or the handoff to `skill-creator` is explicit.
- [ ] The final frontmatter satisfies the harness spec for that primitive type.
- [ ] Canonical paths under `library/` are used, and generated mirrors are not edited manually.
- [ ] Related primitives are referenced by name and type, not by cross-primitive relative links.
- [ ] Prompts are documented as VS Code-only when selected.
- [ ] No double-brace template placeholders, authoring notes, unused alternatives, or unsupported keys remain.
- [ ] The validation path matched the primitive type, and prompts were not declared validated by repository validators.
