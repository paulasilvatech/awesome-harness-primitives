---
applyTo: "**/*.prompt.md"
description: "Enforces VS Code Copilot prompt file conventions for frontmatter, naming, inputs, tools, workflow, output, validation, and maintenance. Use when authoring reusable Copilot Chat prompt files."
---

# Copilot Prompt File Conventions — VS Code Reusable Prompts

These instructions apply to VS Code Copilot prompt files matched by the `applyTo` glob. They are authoritative for prompt frontmatter, file naming, placement, body structure, input variables, tool declarations, guardrails, output definitions, examples, quality checks, and maintenance; organization-specific prompt metadata and workspace standards win where they define stricter prompt-file requirements.

## Scope and Principles

Write prompt files for maintainers and contributors authoring reusable prompts for Copilot Chat. Optimize for predictable behaviour, clear expectations, minimal permissions, and portability across repositories. Follow VS Code prompt file documentation and organization-specific conventions when they apply.

## Frontmatter Requirements

Every high-quality prompt file should include YAML frontmatter with one field per line and consistent quoting, with single quotes preferred for readability and version control clarity.

| Field | Required/Recommended | Description |
| --- | --- | --- |
| `description` | Recommended | A short description of the prompt as a single sentence with an actionable outcome. |
| `name` | Optional | The name shown after typing `/` in chat; defaults to filename when omitted. |
| `agent` | Recommended | The agent to use: `ask`, `edit`, `agent`, or a custom agent name; defaults to the current agent. |
| `model` | Optional | The language model to use; defaults to the currently selected model. |
| `tools` | Optional | List of tool/tool set names available for this prompt. |
| `argument-hint` | Optional | Hint text shown in chat input to guide user interaction. |

If `tools` are specified and the current agent is `ask` or `edit`, the default agent becomes `agent`. Preserve additional metadata such as `language`, `tags`, or `visibility` when the organization requires it.

## File Naming and Placement

Use kebab-case filenames ending with `.prompt.md` and store them under `.github/prompts/` unless the workspace standard specifies another directory. Choose a short filename that communicates the action, such as `generate-readme.prompt.md`, not `prompt1.prompt.md`.

## Body Structure and Inputs

Start with one `#` heading that matches the prompt intent so it surfaces well in Quick Pick search. Organize content with predictable sections such as `Mission` or `Primary Directive`, `Scope & Preconditions`, `Inputs`, `Workflow` (step-by-step), `Output Expectations`, and `Quality Assurance`. Adjust headings to fit the domain, but preserve the logical flow: why → context → inputs → actions → outputs → validation.

Use `${input:variableName[:placeholder]}` for required values and explain when the user must provide them. Mention contextual variables such as `${selection}`, `${file}`, and `${workspaceFolder}` only when essential, and describe how Copilot should interpret them. Define how to proceed when mandatory context is missing, for example: request the file path and stop if it remains undefined.

## Tools, Permissions, and Guardrails

Limit `tools` to the smallest set that enables the task. List tools in preferred execution order when sequence matters. If a prompt inherits tools from a chat mode, mention that relationship and state any critical tool behaviours or side effects. Warn about destructive operations such as file creation, edits, or terminal commands and include guard rails or confirmation steps in the workflow.

## Tone, Output, Examples, and Maintenance

Write direct, imperative sentences targeted at Copilot, such as Analyze, Generate, or Summarize. Keep sentences short and unambiguous, following Google Developer Documentation translation best practices to support localization. Avoid idioms, humor, and culturally specific references.

Specify the format, structure, and location of expected results, such as `Create docs/adr/adr-XXXX.md using the template below`. Include success criteria and failure triggers so Copilot knows when to halt or retry. Provide validation steps, manual checks, automated commands, or acceptance criteria that reviewers can run.

Embed Good/Bad examples or scaffolds such as Markdown templates and JSON stubs when they help the prompt produce consistent output. Keep reference tables inline when they are necessary and self-contained. Link to authoritative documentation instead of duplicating lengthy guidance. Version-control prompts with the code they affect, review them periodically, and extract broadly useful guidance into instruction files or shared prompt packs when appropriate.

## Good / Bad Examples

The examples below illustrate discovery-ready frontmatter and concrete input handling.

**Good**

```yaml
---
name: 'generate-readme'
description: 'Generate a concise README for the selected project. Use when repository documentation is missing or stale.'
agent: 'agent'
tools: ['codebase', 'editFiles', 'search']
argument-hint: '${input:projectPath:Path to the project}'
---
```

Why: the prompt has a clear command name, actionable description, explicit agent, least-privilege tools, and an input placeholder.

**Bad**

```yaml
---
description: 'Do stuff.'
tools: ['all']
---
```

Why: the discovery surface is vague and the tool declaration is not least-privilege.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use YAML frontmatter with `description`, optional `name`, recommended `agent`, optional `model`, optional `tools`, and optional `argument-hint`. | VS Code can discover and run prompts predictably. |
| Use kebab-case filenames under `.github/prompts/` unless the workspace standard differs. | Prompt files are easy to find and invoke. |
| Structure bodies around mission, scope, inputs, workflow, output, and quality assurance. | Copilot receives enough context to act consistently. |
| Define `${input:variableName[:placeholder]}`, `${selection}`, `${file}`, and `${workspaceFolder}` usage precisely. | Missing or ambiguous context does not lead to unsafe guesses. |
| Keep tools least-privilege and document destructive side effects. | Prompt execution avoids unnecessary permissions and unintended edits. |
| Specify output location, format, success criteria, failure triggers, and validation. | Reviewers can verify whether the prompt did the requested work. |
| Maintain prompts with their owning code and update links, tools, and model requirements over time. | Prompt behavior stays aligned with the repository. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Write direct imperative instructions such as Analyze, Generate, and Summarize. | Use idioms, humor, or culturally specific references. |
| Include Good/Bad examples, templates, or JSON stubs when they improve consistency. | Duplicate long authoritative documentation inside the prompt. |
| Tell Copilot to halt, retry, or request missing context when required inputs are absent. | Let the prompt invent mandatory paths, selections, or workspace facts. |
| Test prompts in VS Code with `Chat: Run Prompt`. | Assume Markdown validity means the prompt executes correctly. |
| Keep security, compliance, and privacy references current. | Leave stale tool lists, model requirements, or linked documents. |

## Checklist Before Opening a PR

- [ ] Frontmatter fields are complete, accurate, consistently quoted, and least-privilege.
- [ ] The filename is kebab-case, action-oriented, and placed under `.github/prompts/` or the workspace standard directory.
- [ ] Inputs include placeholders, default behaviours, and fallbacks for missing context.
- [ ] Workflow covers preparation, execution, and post-processing without gaps.
- [ ] Output expectations include formatting, storage details, success criteria, and failure triggers.
- [ ] Validation steps are actionable through commands, diff checks, review prompts, or acceptance criteria.
- [ ] Security, compliance, and privacy policies referenced by the prompt are current.
- [ ] Prompt executes successfully in VS Code with `Chat: Run Prompt` using representative scenarios.

## References

- Prompt Files Documentation: https://code.visualstudio.com/docs/copilot/customization/prompt-files#_prompt-file-format
- Awesome Copilot Prompt Files: https://github.com/github/awesome-copilot
- Tool Configuration: https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode#_agent-mode-tools
