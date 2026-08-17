---
name: "create-copilot-primitive"
description: "Create a Copilot primitive from this repository's templates and reference patterns."
argument-hint: "type=<agent|instructions|skill|prompt> name=<kebab-name> intent=<goal> destination=<response|edit|path>"
---
# /create-copilot-primitive

## Objective

Create a new Copilot primitive from an explicit request in VS Code. Collect the desired primitive type, name, intent, and destination; apply the matching repository template; adapt the result to the patterns in the reference primitives; and deliver the completed artifact only through the selected destination.

Prompts are exclusive to VS Code. GitHub Copilot CLI does not discover or execute `*.prompt.md` files. In this repository, the source for prompts is `library/prompts/`; publish or copy a prompt manually to `.github/prompts/` only when VS Code workspace discovery requires it. Do not claim or assume automatic prompt synchronization.

## When to Invoke

Invoke this prompt when a maintainer wants to author one new Copilot primitive: an agent, instructions file, skill, or VS Code prompt. Use it as the VS Code entry point for primitive authoring before creating or editing an artifact.

Before loading any skill, route by primitive type. For `skill`, use the `skill-creator` skill. For `agent`, `instructions`, or `prompt`, use the `copilot-primitive-authoring` skill. For an ambiguous type, a choice between types, or consultative architectural review, use the `copilot-primitive-architect` agent.

## Preconditions

- The workspace contains this repository's authoring templates under `docs/templates/`.
- The relevant reference patterns under `docs/references/` and the rules in `docs/COPILOT-HARNESS-SPEC.md` are available for inspection.
- The user has provided or will provide the primitive type, primitive name, intent, and destination.
- The primitive name is valid kebab-case with no path separators, no `..`, no leading or trailing hyphen, and no double hyphen.
- The destination is one of: Chat response, approved workspace edit to the canonical source path, or the exact canonical source path calculated from the primitive type and name.
- Editing is allowed only when the user selected `edit` or an exact file path and VS Code editing tools are available.

If any required precondition or input is missing, ask for the missing information and stop. Reject invalid names, path separators, `..`, and any destination that does not match the canonical source path. Do not infer a missing required value and do not create or modify files until the destination is explicit and valid.

## Inputs

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Primitive type | `${input:primitive_type:agent, instructions, skill, or prompt}` | Yes | Accept only `agent`, `instructions`, `skill`, or `prompt`. Ask and stop if absent or ambiguous. |
| Name | `${input:name}` | Yes | Accept only a valid kebab-case artifact name: lowercase letters and digits separated by single hyphens, with no path separators, no `..`, no leading or trailing hyphen, and no double hyphen. Reject and stop if absent or invalid. |
| Intent | `${input:intent}` | Yes | Use as the purpose, activation trigger, and description source. Ask and stop if absent. |
| Destination | `${input:destination:response, approved edit, or exact path}` | Yes | Accept `response`, `edit`, or the exact canonical source path calculated from the type and name. Reject and stop if absent, ambiguous, or any other path. |
| Selected context | `${selection}` | No | Treat an empty selection as absent. Use selected text only as additional user-supplied context. |

Canonical artifact paths by type, after validating `<name>`:

| Type | Canonical source path |
| --- | --- |
| `agent` | `library/agents/<name>.agent.md` |
| `instructions` | `library/instructions/<name>.instructions.md` |
| `skill` | `library/skills/<name>/SKILL.md` |
| `prompt` | `library/prompts/<name>.prompt.md` |

## What I Will Do

- Validate all required inputs, including the type, name, canonical path, and destination, before drafting or editing.
- Route by type before loading any skill: `skill` uses `skill-creator`; `agent`, `instructions`, and `prompt` use `copilot-primitive-authoring`; ambiguous type choices or consultative architectural review use `copilot-primitive-architect`.
- Use the matching template from `docs/templates/` and remove all template setup notes, unused optional branches, and authoring placeholders.
- Apply the current harness rules from `docs/COPILOT-HARNESS-SPEC.md` and reference-primitives style from `docs/references/` for the same primitive type as the target artifact.
- Keep references to other primitives by installed name and type, not by relative link.
- Deliver only to the explicit destination selected by the user, and write only the canonical source path for the validated type and name.

## What I Will NOT Do

- Create or modify a file without an explicit `edit` destination or exact canonical file path.
- Assume that a Chat response should be written to the workspace.
- Write to a destination that differs from the canonical source path calculated from the primitive type and name.
- Leave authoring placeholders, template setup sections, or mutually exclusive template instructions in the final primitive.
- Force a custom agent in prompt frontmatter; omit `agent` unless the user explicitly asks for one.
- Declare prompt `tools` unless exact VS Code tool IDs are required and known.
- Use the `copilot-primitive-authoring` skill to create or audit Agent Skills.
- Use CLI no-op tool tokens in agents or skills. Tokens such as `search`, `web`, and `todo` do not grant useful CLI capabilities; use `grep`, `glob`, `web_fetch`, and `web_search` instead.
- Claim that prompts are synchronized automatically from `library/prompts/` to `.github/prompts/`.
- Claim that prompt artifacts were validated by `validate_primitives.py`; repository validators do not cover prompts.

## Output Format

Use exactly one destination mode:

- **Response:** return the completed primitive content in Chat and do not modify the workspace.
- **Edit:** apply only the user-approved edit scope at the canonical source path, then summarize changed paths and validation evidence.
- **Exact path:** write only the exact requested path when it matches the canonical source path, writing is part of the request, and editing tools are available; otherwise return the content in Chat and state that no file was written.

When reporting completion, use this structure:

```markdown
## Result
<created primitive type, name, and destination>

## Artifact
<path or "Chat response only">

## Validation
<checks performed and any checks that could not run>
```

## Definition of Done

- [ ] The primitive type, name, intent, and destination were explicit before any edit.
- [ ] The name is valid kebab-case with no path separators, no `..`, no leading or trailing hyphen, and no double hyphen.
- [ ] The artifact uses the correct canonical source path for its type, and any exact path destination matches that path.
- [ ] The correct type-based route was chosen before loading any skill.
- [ ] The correct template was applied and all authoring placeholders were removed.
- [ ] The result follows `docs/COPILOT-HARNESS-SPEC.md` and the style of `docs/references/` for the same primitive type as the target artifact.
- [ ] Skill creation was routed to the `skill-creator` skill, and `copilot-primitive-authoring` was not used to create or audit an Agent Skill.
- [ ] For `agent`, `instructions`, and `prompt`, the `copilot-primitive-authoring` skill informed the authoring procedure.
- [ ] Prompt artifacts state that prompts are VS Code-only and live under `library/prompts/` in this repository.
- [ ] Prompt validation, when applicable, was manual and did not rely on `validate_primitives.py`.
- [ ] No unapproved file was created or modified.

## Prompt Body

You are creating a new Copilot primitive in VS Code.

Runtime context:

- **Primitive type:** `${input:primitive_type:agent, instructions, skill, or prompt}`
- **Name:** `${input:name}`
- **Intent:** `${input:intent}`
- **Destination:** `${input:destination:response, approved edit, or exact path}`
- **Selected context:**

  ```text
  ${selection}
  ```

Follow these steps in order:

1. **Validate inputs.** Confirm that primitive type, name, intent, and destination are present and unambiguous. The name must match valid kebab-case with lowercase letters and digits separated by single hyphens, and it must not contain path separators, `..`, a leading hyphen, a trailing hyphen, or a double hyphen. If any required value is missing or invalid, ask for it and stop before drafting or editing.
2. **Choose and verify the target path.** Map the type and validated name to exactly one canonical source path:
   - `agent` -> `library/agents/<name>.agent.md`
   - `instructions` -> `library/instructions/<name>.instructions.md`
   - `skill` -> `library/skills/<name>/SKILL.md`
   - `prompt` -> `library/prompts/<name>.prompt.md`
   If the destination is an exact path, it must exactly match the canonical source path. If it does not match, reject it and stop. For `edit`, write only the canonical source path.
3. **Route before loading skills.** For `skill`, use the `skill-creator` skill. For `agent`, `instructions`, or `prompt`, use the `copilot-primitive-authoring` skill. For an ambiguous type, a choice between types, or consultative architectural review, use the `copilot-primitive-architect` agent and stop the creation workflow until the type is explicit.
4. **Inspect sources.** Use the appropriate template from `docs/templates/`, the harness rules from `docs/COPILOT-HARNESS-SPEC.md`, and style patterns from reference files of the same primitive type as the target artifact. Do not copy outdated relative primitive links from references; cite related primitives by name and type.
5. **Draft the primitive.** Fill the selected template with the requested intent. Remove template setup notes, unused alternatives, and all authoring placeholders. For prompts, keep valid frontmatter on line 1 with `name` and `description`; include `argument-hint` only when useful; omit `agent` unless explicitly requested; declare `tools` only with exact VS Code tool IDs when necessary.
6. **Apply tool vocabulary rules.** For agents and skills, do not use no-op tokens such as `search`, `web`, or `todo`; use `grep`, `glob`, `web_fetch`, and `web_search` when those capabilities are required.
7. **Deliver conditionally.** If the destination is `response`, return the primitive content in Chat. If the destination is `edit`, apply only the approved edit. If the destination is an exact path, write only that path and only when editing tools are available.
8. **Validate and report.** Check the Definition of Done. For `agent`, `instructions`, or `skill`, run `python3 library/scripts/validate_primitives.py --strict` and `python3 library/scripts/generate_catalog.py --check`. For `prompt`, do not use repository validators as evidence; manually verify valid YAML frontmatter starts on line 1 with non-empty `name` and `description`, a non-empty body, and no authoring placeholders; publish manually to `.github/prompts/` only if VS Code discovery requires it; test with **Chat: Run Prompt** in a representative scenario. Report the artifact path or Chat-only result, the validation evidence, and any unresolved blockers.

## Invocation Example

1. Select any relevant context in the editor so `${selection}` is available, if useful.
2. Run **Chat: Run Prompt** and choose `/create-copilot-primitive`.
3. Enter `prompt` for `${input:primitive_type:agent, instructions, skill, or prompt}`.
4. Enter `review-api-contract` for `${input:name}`.
5. Enter `Review an API contract for consistency with repository conventions` for `${input:intent}`.
6. Enter `library/prompts/review-api-contract.prompt.md` for `${input:destination:response, approved edit, or exact path}`.
7. Confirm that the exact path matches the canonical source path for type `prompt` and name `review-api-contract`.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `copilot-primitive-authoring` | skill | Provides the shared procedure for authoring Copilot primitives in this repository. |
| `skill-creator` | skill | Owns Agent Skill creation, repair, and validation guidance. |
