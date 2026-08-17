<!-- AUTHORING NOTES — remove this entire block before using the prompt.

Scope and placement
- Prompt files are a VS Code feature. They are not a primitive discovered or executed by GitHub Copilot CLI.
- In this repository, author the canonical source at `library/prompts/{{PROMPT_NAME}}.prompt.md`.
  Repository synchronization publishes it to `.github/prompts/` for VS Code discovery; do not author the
  synchronized copy directly.
- For a workflow that must run in GitHub Copilot CLI, or in both CLI and VS Code, create an agent skill instead.

Placeholders and runtime variables
- Replace every visible `{{UPPER_SNAKE_CASE}}` authoring placeholder.
- Keep VS Code runtime variables such as `${input:topic}` and `${selection}`. They are resolved when the prompt
  runs and are not authoring placeholders.
- Delete optional fields, inputs, branches, sections, and examples that the finished prompt does not need.

Frontmatter
- Keep `name`, `description`, and `argument-hint` concise and aligned with the prompt body.
- `agent` is optional. Omit it to use the current agent. Add `agent: 'ask'`, `agent: 'agent'`, `agent: 'plan'`,
  or a custom-agent name only when the workflow requires that behavior. Do not force a custom agent.
- `tools` is optional. Omit it when inherited tools are sufficient. If used, copy exact IDs from the VS Code
  Configure Tools picker. For example, `search/codebase` and `vscode/askQuestions` are VS Code tool IDs.
  Tool IDs are environment-dependent, and VS Code tool names must not be copied into CLI agent frontmatter.
- Uncomment the optional frontmatter examples below only after adapting them to the target VS Code environment.

Structure
- The sections before Prompt Body define the contract: trigger, inputs, scope, output, and acceptance criteria.
- Prompt Body contains the reusable operational instructions. Do not restate the contract there without an
  execution reason.
- Make the destination explicit: a chat response, approved workspace edits, or an exact file path. Never assume
  that every prompt writes a file.
- Refer to another component by name and type, such as "the `{{RELATED_NAME}}` skill". Do not use relative links
  between primitives.
-->
---
name: '{{PROMPT_NAME}}'
description: '{{ACTIONABLE_ONE_SENTENCE_DESCRIPTION}}'
argument-hint: '{{ARGUMENT_HINT}}'
# agent: 'ask'
# tools: ['search/codebase', 'vscode/askQuestions']
---

# /{{PROMPT_NAME}}

## Objective

{{OBJECTIVE}}

Deliver the result to `${input:destination:response, edit, or file path}`. Do not create or modify a file unless
the selected destination, prompt purpose, and available VS Code tools explicitly allow it.

## When to Invoke

{{INVOCATION_TRIGGER_AND_WORKFLOW_POSITION}}

## Preconditions

- {{REQUIRED_WORKSPACE_OR_TASK_STATE}}
- {{REQUIRED_CONTEXT_OR_ARTIFACT}}
- {{REQUIRED_PERMISSION_OR_SAFETY_CONDITION}}

If a required precondition is not met, identify it and stop before making changes.

## Inputs

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Topic or task | `${input:topic}` | Yes | Use as the primary scope; ask for it and stop if it remains undefined. |
| Selected context | `${selection}` | No | Treat an empty selection as absent; do not infer content that was not provided or inspected. |
| Destination | `${input:destination:response, edit, or file path}` | Yes | Accept `response`, `edit`, or an exact file path; clarify ambiguous destinations before writing. |
| {{ADDITIONAL_INPUT_NAME}} | {{ADDITIONAL_INPUT_SOURCE}} | {{YES_OR_NO}} | {{ADDITIONAL_INPUT_HANDLING}} |

## What I Will Do

- {{OBSERVABLE_COMMITMENT_ONE}}
- {{OBSERVABLE_COMMITMENT_TWO}}
- Validate the result against the Definition of Done and report the evidence.
- Deliver only to the selected destination.

## What I Will NOT Do

- {{OUT_OF_SCOPE_ACTION}}
- Invent missing facts, evidence, file contents, tool results, or validation outcomes.
- Modify files outside the explicitly approved edit scope or destination.
- Claim that content was written, edited, or verified when the required tool was unavailable or not run.

## Output Format

Use exactly one destination mode:

- **Response:** return `{{RESPONSE_FORMAT}}` in Chat and do not modify the workspace.
- **Edit:** apply only `{{APPROVED_EDIT_SCOPE}}`, then summarize changed paths and validation results.
- **File path:** create or update only the exact requested path when writing is part of the prompt's purpose and
  editing tools are available. Otherwise, return the proposed content in Chat and state that no file was written.

Use this result skeleton, adapting only the content under each heading:

```markdown
## Result
{{RESULT_CONTENT}}

## Evidence
{{EVIDENCE_OR_TRACEABILITY}}

## Validation
{{VALIDATION_RESULT}}
```

## Definition of Done

- [ ] {{PRIMARY_VERIFIABLE_SUCCESS_CRITERION}}
- [ ] {{SECONDARY_VERIFIABLE_SUCCESS_CRITERION}}
- [ ] The result uses the requested destination and no unapproved file was changed.
- [ ] Claims are supported by provided or inspected evidence; unknowns are labeled explicitly.
- [ ] Required checks were run, or each check that could not run is named with the reason.

## Prompt Body

Complete `{{TASK_TYPE}}` for the following runtime context:

- **Topic:** `${input:topic}`
- **Destination:** `${input:destination:response, edit, or file path}`
- **Selected context:**

  ```text
  ${selection}
  ```

Follow these steps in order:

1. **Validate the request.** Confirm that the topic, destination, and required preconditions are unambiguous.
   If information is missing, use `vscode/askQuestions` only when that tool is configured and available;
   otherwise ask for the missing information in Chat and stop before changing anything.
2. **Gather only the necessary evidence.** Use the selected context and any permitted VS Code tools. Distinguish
   inspected facts from assumptions, and do not expand beyond `{{SCOPE_BOUNDARY}}`.
3. **Perform the task.** {{CORE_OPERATIONAL_INSTRUCTIONS}}
4. **Verify the result.** Check `{{TASK_SPECIFIC_VALIDATION}}` and evaluate every Definition of Done item. Do not
   report a check as passed unless its evidence is available.
5. **Deliver conditionally.**
   - For `response`, return the requested format in Chat without workspace edits.
   - For `edit`, modify only the approved scope, then report changed paths and validation.
   - For an exact file path, write only when file output is intended and an editing tool is available. Otherwise,
     return the content in Chat, identify the intended path, and state that it was not written.

{{FINAL_HARD_CONSTRAINT}}

## Invocation Example

1. Select the relevant context in the editor so `${selection}` is populated.
2. Run **Chat: Run Prompt** and choose `/{{PROMPT_NAME}}`.
3. Enter `Review the selected implementation and return prioritized, evidence-based findings` for `topic`.
4. Enter `response` for `destination`.
5. Verify that the result appears in Chat and that no workspace file changed.

## Related Primitives

Delete this section when the prompt stands alone.

| Name | Type | Relationship |
| --- | --- | --- |
| `{{RELATED_PRIMITIVE_NAME}}` | `{{RELATED_PRIMITIVE_TYPE}}` | {{RELATED_PRIMITIVE_PURPOSE}} |
