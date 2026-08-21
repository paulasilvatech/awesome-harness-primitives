---
name: '{{PROMPT_NAME}}'
description: '{{ACTIONABLE_ONE_SENTENCE_DESCRIPTION}}'
argument-hint: '{{ARGUMENT_HINT}}'
# agent: 'ask'
# tools: ['search/codebase', 'vscode/askQuestions']
---

# /{{PROMPT_NAME}}

## Template Setup

Delete this section after configuring the prompt.

1. Treat this as a **VS Code-only** prompt file. GitHub Copilot CLI does not discover or execute
   `*.prompt.md`; use an agent skill when a workflow must run in CLI or on both surfaces.
2. In this repository, author the source at `harness/github-copilot/prompts/{{PROMPT_NAME}}.prompt.md`. When VS Code
   workspace discovery is required, declare the installed path in `harness/github-copilot/manifests/installed-primitives.json`
   and publish it with `python3 harness/github-copilot/scripts/sync_installed_primitives.py`; never maintain both copies.
3. Replace every `{{UPPER_SNAKE_CASE}}` authoring placeholder. Keep `${input:...}` and `${selection}`
   only when they are intentional VS Code runtime variables, and remove unused inputs, fields, branches,
   sections, and examples.
4. Leave `agent` omitted to use the current VS Code agent. Uncomment it only when the workflow requires
   `ask`, `agent`, `plan`, or a specific custom agent; do not force a custom agent by default.
5. Omit `tools` when inherited tools are sufficient. If tools are required, copy their exact IDs from
   VS Code's **Configure Tools** picker. IDs such as `search/codebase` and `vscode/askQuestions` are
   VS Code-specific and must not be copied into CLI agent or skill frontmatter.
6. Choose the intended destination explicitly. A prompt may return a Chat response, make approved
   workspace edits, or write an exact path, but it must not assume that every invocation writes files.
7. Refer to another primitive by installed name and type, not by a relative link.
8. Check `docs/HARNESS-VALIDATION.md` before making a current-platform claim. Verify a first-party source
   only when the target version changed, sources conflict, the claim is unverified, the user asks for
   current behavior, or the recorded evidence is older than 90 days.

## Section map

Delete this section after configuring the prompt.

Prompts are the most rigid primitive type. All four reference prompts share the
same ten sections in the same order. Do not reorder, rename, or drop them.

| Section | Status | Include when |
| --- | --- | --- |
| `## Objective` | MANDATORY | Always. First section. |
| `## When to Invoke` | MANDATORY | Always. |
| `## Preconditions` | MANDATORY | Always. What must already be true, and stop if it is not. |
| `## Inputs the Team Must Provide` | MANDATORY | Always. Use this exact title. |
| `## What I Will Do` | MANDATORY | Always. |
| `## What I Will NOT Do` | MANDATORY | Always. The behavioral boundary. |
| `## Output Format` | MANDATORY | Always. Embed the literal artifact skeleton in a fenced block. |
| `## Definition of Done` | MANDATORY | Always. Checkboxes only. |
| `## Prompt Body` | MANDATORY | Always. Numbered steps the model executes, `Step 1` through `Step N`. |
| `## Invocation Example` | MANDATORY | Always. Last section unless `## Related Primitives` follows. |
| `## Related Primitives` | CONDITIONAL | Another primitive owns an adjacent responsibility worth naming. |
| `## Template Setup`, `## Section map` | AUTHORING ONLY | Never ship. Delete before delivery. |

Domain-specific headings belong inside the fenced block under
`## Output Format`, never as extra top-level sections between the ten above.

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

## Inputs the Team Must Provide

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
- [ ] Current platform claims have a source and verification date.

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

CONDITIONAL. Include only when another primitive owns an adjacent responsibility worth naming. Otherwise delete.

| Name | Type | Relationship |
| --- | --- | --- |
| `{{RELATED_PRIMITIVE_NAME}}` | `{{RELATED_PRIMITIVE_TYPE}}` | {{RELATED_PRIMITIVE_PURPOSE}} |
