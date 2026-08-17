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

For Agent Skills, route the authoring workflow explicitly to the `skill-creator` skill. For the overall primitive-authoring procedure, rely on the `copilot-primitive-authoring` skill.

## Preconditions

- The workspace contains this repository's authoring templates under `docs/templates/`.
- The relevant reference patterns under `docs/references/` and the rules in `docs/COPILOT-HARNESS-SPEC.md` are available for inspection.
- The user has provided or will provide the primitive type, primitive name, intent, and destination.
- The destination is one of: Chat response, approved workspace edit, or an exact file path.
- Editing is allowed only when the user selected `edit` or an exact file path and VS Code editing tools are available.

If any required precondition or input is missing, ask for the missing information and stop. Do not infer a missing required value and do not create or modify files until the destination is explicit.

## Inputs

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Primitive type | `${input:primitive_type:agent, instructions, skill, or prompt}` | Yes | Accept only `agent`, `instructions`, `skill`, or `prompt`. Ask and stop if absent or ambiguous. |
| Name | `${input:name}` | Yes | Use a kebab-case artifact name. Ask and stop if absent. |
| Intent | `${input:intent}` | Yes | Use as the purpose, activation trigger, and description source. Ask and stop if absent. |
| Destination | `${input:destination:response, approved edit, or exact path}` | Yes | Accept `response`, `edit`, or an exact target path. Ask and stop if absent or ambiguous. |
| Selected context | `${selection}` | No | Treat an empty selection as absent. Use selected text only as additional user-supplied context. |

Default canonical artifact paths by type:

| Type | Canonical source path |
| --- | --- |
| `agent` | `library/agents/<name>.agent.md` |
| `instructions` | `library/instructions/<name>.instructions.md` |
| `skill` | `library/skills/<name>/SKILL.md` |
| `prompt` | `library/prompts/<name>.prompt.md` |

## What I Will Do

- Validate all required inputs before drafting or editing.
- Use the matching template from `docs/templates/` and remove all template setup notes, unused optional branches, and authoring placeholders.
- Follow the `copilot-primitive-authoring` skill for the authoring procedure.
- For `skill`, invoke or hand off to the `skill-creator` skill and ensure the skill name matches `library/skills/<name>/SKILL.md`.
- Apply the current harness rules from `docs/COPILOT-HARNESS-SPEC.md` and reference-primitives style from `docs/references/`.
- Keep references to other primitives by installed name and type, not by relative link.
- Deliver only to the explicit destination selected by the user.

## What I Will NOT Do

- Create or modify a file without an explicit `edit` destination or exact file path.
- Assume that a Chat response should be written to the workspace.
- Leave authoring placeholders, template setup sections, or mutually exclusive template instructions in the final primitive.
- Force a custom agent in prompt frontmatter; omit `agent` unless the user explicitly asks for one.
- Declare prompt `tools` unless exact VS Code tool IDs are required and known.
- Use CLI no-op tool tokens in agents or skills. Tokens such as `search`, `web`, and `todo` do not grant useful CLI capabilities; use `grep`, `glob`, `web_fetch`, and `web_search` instead.
- Claim that prompts are synchronized automatically from `library/prompts/` to `.github/prompts/`.

## Output Format

Use exactly one destination mode:

- **Response:** return the completed primitive content in Chat and do not modify the workspace.
- **Edit:** apply only the user-approved edit scope, then summarize changed paths and validation evidence.
- **Exact path:** write only the exact requested path if writing is part of the request and editing tools are available; otherwise return the content in Chat and state that no file was written.

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
- [ ] The artifact uses the correct canonical source path for its type.
- [ ] The correct template was applied and all authoring placeholders were removed.
- [ ] The result follows `docs/COPILOT-HARNESS-SPEC.md` and the style of `docs/references/`.
- [ ] Skill creation was routed to the `skill-creator` skill.
- [ ] The `copilot-primitive-authoring` skill informed the authoring procedure.
- [ ] Prompt artifacts state that prompts are VS Code-only and live under `library/prompts/` in this repository.
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

1. **Validate inputs.** Confirm that primitive type, name, intent, and destination are present and unambiguous. If any required value is missing, ask for it and stop before drafting or editing.
2. **Choose the target path.** Map the type to exactly one canonical source path:
   - `agent` -> `library/agents/<name>.agent.md`
   - `instructions` -> `library/instructions/<name>.instructions.md`
   - `skill` -> `library/skills/<name>/SKILL.md`
   - `prompt` -> `library/prompts/<name>.prompt.md`
3. **Load the authoring procedure.** Use the `copilot-primitive-authoring` skill to guide the workflow. If the requested type is `skill`, route the work to the `skill-creator` skill and follow its requirements.
4. **Inspect sources.** Use the appropriate template from `docs/templates/`, the harness rules from `docs/COPILOT-HARNESS-SPEC.md`, and the style patterns from the reference prompt files. Do not copy outdated relative primitive links from references; cite related primitives by name and type.
5. **Draft the primitive.** Fill the selected template with the requested intent. Remove template setup notes, unused alternatives, and all authoring placeholders. For prompts, keep valid frontmatter on line 1 with `name` and `description`; include `argument-hint` only when useful; omit `agent` unless explicitly requested; declare `tools` only with exact VS Code tool IDs when necessary.
6. **Apply tool vocabulary rules.** For agents and skills, do not use no-op tokens such as `search`, `web`, or `todo`; use `grep`, `glob`, `web_fetch`, and `web_search` when those capabilities are required.
7. **Deliver conditionally.** If the destination is `response`, return the primitive content in Chat. If the destination is `edit`, apply only the approved edit. If the destination is an exact path, write only that path and only when editing tools are available.
8. **Validate and report.** Check the Definition of Done. Report the artifact path or Chat-only result, the validation evidence, and any unresolved blockers.

## Invocation Example

1. Select any relevant context in the editor so `${selection}` is available, if useful.
2. Run **Chat: Run Prompt** and choose `/create-copilot-primitive`.
3. Enter `prompt` for `${input:primitive_type:agent, instructions, skill, or prompt}`.
4. Enter `review-api-contract` for `${input:name}`.
5. Enter `Review an API contract for consistency with repository conventions` for `${input:intent}`.
6. Enter `library/prompts/review-api-contract.prompt.md` for `${input:destination:response, approved edit, or exact path}`.
7. Confirm that only the selected destination is used.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `copilot-primitive-authoring` | skill | Provides the shared procedure for authoring Copilot primitives in this repository. |
| `skill-creator` | skill | Owns Agent Skill creation, repair, and validation guidance. |
