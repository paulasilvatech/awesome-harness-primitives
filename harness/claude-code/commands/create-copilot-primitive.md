---
description: "Create a Copilot primitive from this repository's templates and reference patterns."
argument-hint: >-
  type=<agent|instructions|skill|prompt> name=<kebab-name> intent=<goal>
  destination=<response|edit|path>
---

<!-- Generated from harness/github-copilot/prompts/create-copilot-primitive.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /create-copilot-primitive

## Objective

Create a new Copilot primitive from an explicit request in VS Code. Collect the desired primitive type, name, intent, and destination; apply current repository governance, dated evidence, the matching template, and same-type reference patterns; and deliver the completed artifact only through the selected destination.

Prompts are exclusive to local VS Code chat. GitHub Copilot Agent Host and CLI do not discover or execute `*.prompt.md` files. In this repository, the source for prompts is `harness/github-copilot/prompts/`; declared installed prompts are generated under `.github/prompts/` by `sync_installed_primitives.py`.

## When to Invoke

Invoke this prompt when a maintainer wants to author one new Copilot primitive: an agent, instructions file, skill, or VS Code prompt. Use it as the VS Code entry point for primitive authoring before creating or editing an artifact.

Before loading any skill, route by primitive type. For `skill`, use the `skill-creator` skill. For `agent`, `instructions`, or `prompt`, use the `copilot-primitive-authoring` skill. For an ambiguous type, a choice between types, or consultative architectural review, use the `copilot-primitive-architect` agent.

## Preconditions

- The workspace contains this repository's authoring templates under `docs/templates/`.
- Repository governance, `docs/COPILOT-HARNESS-SPEC.md`, `docs/HARNESS-VALIDATION.md`, and same-type references are available for inspection.
- The user has provided or will provide the primitive type, primitive name, intent, and destination.
- The primitive name is valid kebab-case with no path separators, no `..`, no leading or trailing hyphen, and no double hyphen.
- The destination is one of: Chat response, approved workspace edit to the canonical source path, or the exact canonical source path calculated from the primitive type and name.
- Editing is allowed only when the user selected `edit` or an exact file path and VS Code editing tools are available.

If any required precondition or input is missing, ask for the missing information and stop. Reject invalid names, path separators, `..`, and any destination that does not match the canonical source path. Do not infer a missing required value and do not create or modify files until the destination is explicit and valid.

## Inputs the Team Must Provide

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
| `agent` | `harness/github-copilot/agents/<name>.agent.md` |
| `instructions` | `harness/github-copilot/instructions/<name>.instructions.md` |
| `skill` | `harness/github-copilot/skills/<name>/SKILL.md` |
| `prompt` | `harness/github-copilot/prompts/<name>.prompt.md` |

## What I Will Do

- Validate all required inputs, including the type, name, canonical path, and destination, before drafting or editing.
- Route by type before loading any skill: `skill` uses `skill-creator`; `agent`, `instructions`, and `prompt` use `copilot-primitive-authoring`; ambiguous type choices or consultative architectural review use `copilot-primitive-architect`.
- Use the matching template from `docs/templates/` and remove all template setup notes, unused optional branches, and authoring placeholders. Apply current section maps: instructions use an authority paragraph instead of `## Scope and Stack Context` and close with `## Checklist Before Opening a PR`; agents use `## What This Agent Knows`, `## What This Agent Does NOT Know`, and `## Anti-Patterns This Agent Rejects`; prompts use `## Inputs the Team Must Provide`.
- Apply the current harness rules from `docs/COPILOT-HARNESS-SPEC.md` and reference-primitives style from `docs/references/` for the same primitive type as the target artifact.
- Use dated evidence from `docs/HARNESS-VALIDATION.md`. Verify a known first-party source only when the user requests current behavior, the target version changed, sources conflict, a claim is unverified, or evidence is older than 90 days.
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
- Hand-edit an installed prompt or claim synchronization unless it is declared in `harness/github-copilot/manifests/installed-primitives.json` and the drift check passes.
- Claim that static repository validation proves a prompt executed successfully in VS Code.
- Call platform behavior current or latest without a source and verification date.

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
- [ ] The correct template was applied and all authoring placeholders were removed. Instructions, agents, and prompts use the current section names from `docs/templates/`.
- [ ] The result follows `docs/COPILOT-HARNESS-SPEC.md` and the style of `docs/references/` for the same primitive type as the target artifact.
- [ ] Current platform claims are supported by dated evidence in `docs/HARNESS-VALIDATION.md` or a newly verified first-party source.
- [ ] Skill creation was routed to the `skill-creator` skill, and `copilot-primitive-authoring` was not used to create or audit an Agent Skill.
- [ ] For `agent`, `instructions`, and `prompt`, the `copilot-primitive-authoring` skill informed the authoring procedure.
- [ ] Prompt artifacts state that prompts are local VS Code-only and live under `harness/github-copilot/prompts/` in this repository.
- [ ] Repository validation, installed-copy drift, and **Chat: Run Prompt** runtime testing are reported as distinct checks.
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

**Step 1 — Validate inputs.** Confirm that primitive type, name, intent, and destination are present and unambiguous. The name must match valid kebab-case with lowercase letters and digits separated by single hyphens, and it must not contain path separators, `..`, a leading hyphen, a trailing hyphen, or a double hyphen. If any required value is missing or invalid, ask for it and stop before drafting or editing.

**Step 2 — Choose and verify the target path.** Map the type and validated name to exactly one canonical source path:
- `agent` -> `harness/github-copilot/agents/<name>.agent.md`
- `instructions` -> `harness/github-copilot/instructions/<name>.instructions.md`
- `skill` -> `harness/github-copilot/skills/<name>/SKILL.md`
- `prompt` -> `harness/github-copilot/prompts/<name>.prompt.md`
If the destination is an exact path, it must exactly match the canonical source path. If it does not match, reject it and stop. For `edit`, write only the canonical source path.

**Step 3 — Route before loading skills.** For `skill`, use the `skill-creator` skill. For `agent`, `instructions`, or `prompt`, use the `copilot-primitive-authoring` skill. For an ambiguous type, a choice between types, or consultative architectural review, use the `copilot-primitive-architect` agent and stop the creation workflow until the type is explicit.

**Step 4 — Inspect sources and freshness.** Use repository governance, the appropriate template from `docs/templates/`, harness rules from `docs/COPILOT-HARNESS-SPEC.md`, dated evidence from `docs/HARNESS-VALIDATION.md`, and same-type references. Verify a known first-party URL only when the user asks for current behavior, the target version changed, sources conflict, a claim is unverified, or evidence is older than 90 days. Do not copy outdated relative primitive links from references; cite related primitives by name and type.

**Step 5 — Draft the primitive.** Fill the selected template with the requested intent. Remove template setup notes, unused alternatives, and all authoring placeholders. For prompts, keep valid frontmatter on line 1 with `name` and `description`; include `argument-hint` only when useful; omit `agent` unless explicitly requested; declare `tools` only with exact VS Code tool IDs when necessary; use the ten mandatory prompt sections in order, including `## Inputs the Team Must Provide`.

**Step 6 — Apply tool vocabulary rules.** For agents and skills, do not use no-op tokens such as `search`, `web`, or `todo`; use `grep`, `glob`, `web_fetch`, and `web_search` when those capabilities are required.

**Step 7 — Deliver conditionally.** If the destination is `response`, return the primitive content in Chat. If the destination is `edit`, apply only the approved edit. If the destination is an exact path, write only that path and only when editing tools are available.

**Step 8 — Validate and report.** Check the Definition of Done. Run `python3 harness/github-copilot/scripts/validate_primitives.py --strict`, `python3 harness/github-copilot/scripts/audit_primitive_content.py --check`, `python3 harness/github-copilot/scripts/audit_primitive_capabilities.py --check`, `python3 harness/github-copilot/scripts/audit_primitive_redundancy.py --check`, `python3 harness/github-copilot/scripts/generate_catalog.py --check`, `python3 harness/github-copilot/scripts/sync_plugin_components.py --check`, and `python3 harness/github-copilot/scripts/sync_installed_primitives.py --check`. For a prompt, also test **Chat: Run Prompt** in a representative scenario; static validation checks metadata and structure but does not execute the prompt. Report the artifact path or Chat-only result, freshness evidence when used, validation evidence, and unresolved blockers.

## Invocation Example

1. Select any relevant context in the editor so `${selection}` is available, if useful.
2. Run **Chat: Run Prompt** and choose `/create-copilot-primitive`.
3. Enter `prompt` for `${input:primitive_type:agent, instructions, skill, or prompt}`.
4. Enter `review-api-contract` for `${input:name}`.
5. Enter `Review an API contract for consistency with repository conventions` for `${input:intent}`.
6. Enter `harness/github-copilot/prompts/review-api-contract.prompt.md` for `${input:destination:response, approved edit, or exact path}`.
7. Confirm that the exact path matches the canonical source path for type `prompt` and name `review-api-contract`.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `copilot-primitive-authoring` | skill | Provides the shared procedure for authoring Copilot primitives in this repository. |
| `skill-creator` | skill | Owns Agent Skill creation, repair, and validation guidance. |
