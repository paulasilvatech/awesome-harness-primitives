---
applyTo: "**/*.prompt.md"
description: "Applies current VS Code prompt conventions for canonical sources, metadata, runtime inputs, tools, destination safety, body structure, and testing. Use when creating or updating a prompt."
---

# VS Code Prompt Conventions - Explicit User-Invoked Actions

These instructions apply to `*.prompt.md` files matched by `**/*.prompt.md`.
They are authoritative for this repository's prompt metadata, source path, body
contract, runtime inputs, destination handling, and tests; current VS Code
prompt documentation wins for runtime fields.

## Runtime and Source Boundary

Prompt files are manually invoked actions for local VS Code chat. GitHub Copilot
CLI does not discover or execute them; convert a workflow that must run in the
CLI into an Agent Skill.

Author the canonical source at `.github/prompts/<name>.prompt.md`. This
repository has no prompt mirror or synchronization manifest; do not create or
maintain a second copy.

## Metadata and Inputs

The VS Code schema supports `description`, `name`, `argument-hint`, `agent`, `model`, and `tools`. This repository requires non-empty `name` and `description` for every canonical prompt.

- Keep the filename and `name` kebab-case and aligned.
- Keep `description` concise and action-oriented.
- Add `argument-hint` only when it helps users supply meaningful input.
- Omit `agent` to inherit the current agent unless the workflow requires `ask`, `agent`, `plan`, or a named custom agent.
- Omit `model` unless a verified fixed model is required.
- Omit `tools` when inherited tools are sufficient. When a stable built-in capability is required, prefer the current aliases `read`, `search`, `edit`, `execute`, `web`, `agent`, or `todo`; use an MCP/extension tool or tool set only when the prompt truly depends on it. Unavailable tools are ignored.
- Define `${input:name}` values and contextual variables such as `${selection}`, `${file}`, or `${workspaceFolder}` only when the body consumes them and defines missing-input behavior.

## Body Contract

Follow the established same-type structure. Keep these ten sections once and in
order:

1. `## Objective`
2. `## When to Invoke`
3. `## Preconditions`
4. `## Inputs the Team Must Provide`
5. `## What I Will Do`
6. `## What I Will NOT Do`
7. `## Output Format`
8. `## Definition of Done`
9. `## Prompt Body`
10. `## Invocation Example`

Add `## Related Primitives` only when a named adjacent primitive matters. Put domain headings inside the fenced output skeleton rather than adding extra top-level contract sections.

## Destination and Safety

Choose exactly one destination mode per invocation: Chat response, approved workspace edit, or an exact file path. Validate the destination before editing. Do not infer permission to write from the fact that a prompt can use editing tools.

Ask for missing required inputs and stop before side effects. Distinguish inspected evidence from assumptions, validate the completed result, and never claim a file was written or a command passed when the required tool was unavailable.

Prompt frontmatter controls tool availability, not approval. Default Approvals, Assisted permissions,
Bypass Approvals, Autopilot, URL approval, terminal approval, sandboxing, and managed organizational rules
remain VS Code session or policy controls. Do not add a `permissions` field.

Repository files may be linked when they are intentional runtime context. References to another primitive use its installed name and type rather than a cross-primitive relative link.

## Freshness and Testing

Verify first-party VS Code documentation when prompt schema, tool IDs,
variables, or model behavior is material and the user requests current
behavior, sources conflict, or the target version changed.

Run repository validation and installed-mirror checks. Then use **Chat: Run Prompt** with representative inputs, verify the selected destination, and confirm no unapproved file changed. If VS Code runtime testing is unavailable, report it as not run.

## Conventions

| Rule | Rationale |
| --- | --- |
| Treat prompts as VS Code-only explicit actions. | Agent Host and Copilot CLI users are routed to a portable Skill instead. |
| Keep canonical sources under `.github/prompts/`. | The repository has one versioned prompt source. |
| Require clear inputs, preconditions, limits, output, and done criteria. | Manual invocation remains predictable and safe. |
| Use exact target-environment tool IDs only when needed. | Unknown tools are ignored and do not provide capability. |
| Test destination behavior in VS Code. | Static Markdown validation cannot prove runtime side effects. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use the ten-section local template. | Ship authoring notes or improvise a competing section structure. |
| Inherit the current agent and model by default. | Pin a surface, agent, or model without a workflow requirement. |
| Validate inputs and destination before edits or commands. | Treat every prompt invocation as permission to modify the workspace. |
| Keep prompt tool IDs separate from CLI agent tokens. | Copy `search/codebase` or VS Code tool IDs into CLI metadata. |
| Report runtime tests and limitations honestly. | Claim repository validators execute prompts. |

## Checklist Before Opening a PR

- [ ] Filename, `name`, and description are valid and aligned.
- [ ] Optional fields and runtime variables are present only when consumed.
- [ ] The ten mandatory sections appear once and in order.
- [ ] Preconditions define stop behavior for missing context.
- [ ] The destination is explicit and write scope is bounded.
- [ ] Tool IDs are exact for the tested VS Code environment and least privilege.
- [ ] Current platform claims have dated first-party evidence.
- [ ] The three repository-owned primitive gates pass.
- [ ] **Chat: Run Prompt** passed with representative input, or the unrun test is reported.

## References

- VS Code prompt files: https://code.visualstudio.com/docs/agent-customization/prompt-files
