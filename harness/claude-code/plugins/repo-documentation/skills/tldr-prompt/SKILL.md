---
name: tldr-prompt
description: >-
  Create tldr-style markdown summaries for GitHub Copilot customization files, MCP server
  documentation, Copilot documentation URLs, or focused Copilot usage queries. Use when asked to
  "tldr this prompt", "summarize this agent", "make a tldr for MCP docs", "summarize Copilot
  instructions", or "show examples for this Copilot file".
---

<!-- Generated from harness/github-copilot/plugins/repo-documentation/skills/tldr-prompt/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# tldr prompt

Transform Copilot customization files, MCP server documentation, Copilot documentation URLs, or focused Copilot usage questions into concise tldr-pages style output with concrete invocation examples.

## When to invoke

- "tldr this prompt file."
- "Summarize this Copilot agent with examples."
- "Create a tldr page for these MCP docs."
- "Show the most useful examples for this instructions file."
- "Make a quick reference for inline chat shortcuts."

## Inputs

Use the user's supplied files, selected text, URLs, or query as the source. Require at least one of:

| Input | Accepted form | Handling |
| --- | --- | --- |
| Copilot customization files | `prompt file`, `.agent.md`, `.instructions.md`, `.collections.md` | Read every supplied file, up to five summaries. |
| URL | Copilot docs, MCP server docs, raw GitHub content, or other documentation | Fetch every supplied URL, up to five summaries. |
| Raw query | Topic such as `MCP servers`, `inline chat shortcuts`, or `chat tools` | Resolve to workspace files or authoritative documentation. |
| Help text | `-h`, `--help`, `/?`, `--tldr`, `--man` output | Summarize common commands and examples. |

If no input is present, return the missing-input message in the output template and do not invent a source.

## Source resolution

Classify input as **UNAMBIGUOUS QUERIES** or **AMBIGUOUS QUERIES**. Handle `file/URL`, `files/URLs`, `data/query**`, `fetch/read`, `s/documentation`, `tools/agents`, `view/general`, `instructions/collections`, and `context-specific` cases explicitly. Keep the output example-driven and in `tldr` / `TLDR` style; include a `one-line` description and mention `sub-commands` when the source has them.


| Situation | Resolution rule |
| --- | --- |
| Specific file or URL supplied | Do not search; read or fetch it directly. |
| Workspace file paths supplied without explicit file attachment syntax | Read all supplied files. |
| URLs supplied without explicit fetch syntax | Fetch all supplied URLs. |
| More than five files or URLs | Summarize the first five and list the rest as not processed. |
| Query about prompts, agents, instructions, or collections | Search the workspace first for `prompt file`, `.agent.md`, `.instructions.md`, `.collections.md`; if no relevant files exist, check https://github.com/github/awesome-copilot and fetch raw content from <https://raw.githubusercontent.com/github/awesome-copilot/main/{folder}/{filename}>. |
| Query about MCP servers | Prefer https://modelcontextprotocol.io/ and <https://code.visualstudio.com/docs/agent-customization/mcp-servers>. |
| Query about inline chat or Ctrl+I | Prefer <https://code.visualstudio.com/docs/chat/inline-chat>. |
| Query about chat view or chat tools | Prefer <https://code.visualstudio.com/docs/chat/chat-overview>. |
| General GitHub Copilot query | Prefer https://code.visualstudio.com/docs/agents/overview or <https://docs.github.com/en/copilot/>. |

When resolving through awesome-copilot, fetch <https://raw.githubusercontent.com/github/awesome-copilot/main/README.md> first, then convert relevant repository links such as <https://github.com/github/awesome-copilot/blob/main/instructions/java-junit5-assertions.instructions.md> to raw URLs such as <https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/java-junit5-assertions.instructions.md>. Preserve supplied URLs, including examples like <https://example.com/docs}}>.

## Example density and invocation syntax

Legacy-compatible examples may mention `typescript-mcp-server-generator`, `typescript-mcp-expert`, `tldr-page`, `URL/prompt`, `<name.prompt[.]md>`, `<name.agent.md>`, `/file command-subcommand1`, `/file command-subcommand2`, `command-subcommand1`, and `command-subcommand2` when those names appear in the source. Use `#file`, `#fetch`, or `#tool:fetch` only when documenting the user's supplied invocation, not as required CLI syntax.


| Source count | Examples per source | Rule |
| --- | --- | --- |
| One file or URL | 5-8 examples | Cover the most common use cases by frequency. |
| 2-3 files or URLs | 3-5 examples each | Keep each summary complete but compact. |
| 4-5 files or URLs | 2-3 examples each | Use only essential examples. |
| 6+ files or URLs | First five only, 2-3 examples each | List remaining files or URLs without summarizing. |
| Inline chat context | 3-5 essential examples | Reduce verbosity for Ctrl+I style use. |

Use the correct invocation style:

| File type | Example syntax |
| --- | --- |
| Prompt | `/prompt-name {{parameters}}` |
| Agent | `@agent-name {{request}}` |
| Instructions | State when the instructions apply; do not imply direct invocation. |
| Collections | List included files and how the collection changes context. |
| MCP documentation | Show setup, server configuration, and tool usage examples. |

Use `{{placeholder}}` for every user-provided value: `{{filename}}`, `{{url}}`, `{{topic}}`, `{{parameter}}`.

## Procedure

1. Validate that at least one file, selection, URL, help output, or query is present.
2. Identify the source type: `prompt file`, `.agent.md`, `.instructions.md`, `.collections.md`, MCP server documentation, inline chat, chat tools, or general Copilot docs.
3. Read or fetch content. For ambiguous queries, apply the source resolution table.
4. Extract the source purpose, key parameters, subcommands or modes, and high-frequency use cases.
5. Generate one tldr block per processed source using the output template.
6. Adapt verbosity to context: inline chat is concise; chat view can include fuller examples.

## Gotchas

- **IMPORTANT / NOTE labels become prose**: summarize admonitions without copying noisy formatting unless the distinction changes behavior.
- **DOES / UNAMBIGUOUS markers are source terminology**: preserve such terms only when they affect examples or modes.
- **Folder words are evidence**: `agents`, `collections`, `instructions`, and `prompts` can identify source type and should not be collapsed away.


- **Do not create a tldr page file**: render markdown directly in chat.
- **Do not fabricate examples**: examples must reflect the source's actual capabilities.
- **Do not skip the More information line**: point to the local filename or source URL.
- **Do not over-process bulk input**: summarize the first five sources and list the rest.
- **Do not use direct-invocation syntax for instructions**: instructions apply by context, not by command.

## Output template

```markdown
# <command-or-source-name>

> <short, snappy description.>
> <one to two sentences summarizing the source.>
> More information: <name.prompt[.]md | name.agent.md | name.instructions.md | name.collections.md | URL>

- <common use case>:

`<correct invocation using {{placeholder}} values>`

- <common use case>:

`<correct invocation using {{placeholder}} values>`
```

Missing input response:

```text
Error: Missing required input.

You MUST provide one of the following:
1. A Copilot file: /tldr-prompt #file:{{name.prompt[.]md | name.agent.md | name.instructions.md | name.collections.md}}
2. A URL: /tldr-prompt #fetch {{https://example.com/docs}}
3. A search query: /tldr-prompt "{{topic}}" (e.g., "MCP servers", "inline chat", "chat tools")

Please retry with one of these inputs.
```

## Quality gate

- [ ] At least one valid source was read or fetched, or the missing-input response was returned.
- [ ] Each summary has a title, description, More information line, and examples.
- [ ] Invocation examples match the source type: `/` for prompts, `@` for agents, contextual wording for instructions and collections.
- [ ] Every user-supplied value uses `{{placeholder}}` syntax.
- [ ] Single-source output includes 5-8 examples; multi-source output follows the density table.
- [ ] The output is rendered directly in chat and no new tldr file is created.
- [ ] Resolved documentation uses the authoritative URLs listed in this skill when no specific source is supplied.

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [VS Code MCP servers](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
- [VS Code agents overview](https://code.visualstudio.com/docs/agents/overview)
- [VS Code chat overview](https://code.visualstudio.com/docs/chat/chat-overview)
- [VS Code inline chat](https://code.visualstudio.com/docs/chat/inline-chat)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot/)
- [Awesome Copilot](https://github.com/github/awesome-copilot)
- [Awesome Copilot raw file pattern](https://raw.githubusercontent.com/github/awesome-copilot/main/{folder}/{filename})
- [Awesome Copilot README raw](https://raw.githubusercontent.com/github/awesome-copilot/main/README.md)
