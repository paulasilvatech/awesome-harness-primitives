# Prompt files — VS Code only

> **These are not Copilot CLI primitives.** Agents running on the Agent Host — which includes the
> Copilot CLI — do not read prompt files. Nothing in this directory loads in a CLI session, and the
> repository validator does not check it.
>
> Source: [Use prompt files in VS Code](https://code.visualstudio.com/docs/agent-customization/prompt-files)
> — *"Agents running on the Agent Host don't use prompt files. To use an existing prompt with the
> Copilot agent, convert it to an agent skill."*

They are kept here because they still work in VS Code chat, where they are invoked manually as slash
commands.

## Install

Copy into the workspace location VS Code discovers:

```sh
mkdir -p .github/prompts
cp library/prompts/new-skill.prompt.md .github/prompts/
```

Then invoke it in chat with `/new-skill`.

## Frontmatter

All keys are optional. Only these are recognised:

| Field | Description |
| --- | --- |
| `description` | Short description of the prompt. |
| `name` | Name used after typing `/` in chat; defaults to the file name. |
| `argument-hint` | Hint text shown in the chat input field. |
| `agent` | `ask`, `agent`, `plan`, or a custom agent name. Defaults to `agent` when `tools` is set. |
| `model` | Language model to run the prompt with. |
| `tools` | Tool or tool-set names available to the prompt. Unavailable tools are ignored. |

The files here also carry provenance keys (`source`, `source_url`, `license`, `imported_date`,
`last_sync`). VS Code ignores unknown frontmatter keys, so they are harmless.

> **Never copy a `tools:` list between a prompt file and a CLI agent file.** The two vocabularies only
> look alike: tokens such as `search` and `codebase` are real tools in VS Code but grant nothing in the
> CLI. See [docs/COPILOT-HARNESS-SPEC.md](../../docs/COPILOT-HARNESS-SPEC.md) §1.3.

## Targeting the CLI instead

Convert the prompt to an [agent skill](../skills/). A skill marked `user-invocable` is still callable as
`/name`, so nothing is lost in the conversion and it works in both VS Code and the CLI.
[docs/templates/skill.template.md](../../docs/templates/skill.template.md) is the starting point;
VS Code's Agent Customizations editor also offers an experimental one-time migration.
