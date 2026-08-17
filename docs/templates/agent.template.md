<!-- AUTHORING — delete this block after copying.
Target path: agents/<name>.agent.md   Filename must match ^[A-Za-z0-9._-]+\.agent\.md$
Spec: docs/COPILOT-HARNESS-SPEC.md §1

Frontmatter
  description  REQUIRED. Non-empty, single line, <= 500 chars. Must state WHAT + WHEN to select.
  name         Optional; defaults to the filename.
  tools        Optional ALLOW-LIST. Omitting it grants everything. Unknown tokens are dropped silently.
               Valid: * read view create edit editFiles execute bash shell runCommands agent task
                      grep glob web_fetch web_search todo_write runTests lsp plan  and  <server>/<tool>
               No-op traps: search web codebase terminal all fetch changes githubRepo run
               Always available regardless of this list: skill, sql
  model        Optional. Prefer omitting so the agent inherits the session model.
  user-invocable / disable-model-invocation / mcp-servers  Optional, CLI-honored.
  argument-hint / handoffs  VS Code only; the CLI ignores them (validator reports INFO).

Body: Markdown, max 30 000 characters. Start with a single H1.
Declare mcp-servers if the body tells the agent to call MCP tools.
-->
---
name: "<agent-name>"
description: "<What this agent does in one sentence.> Use when <the situation that should select it>."
tools: ["read", "grep", "glob", "edit"]
---

# <Agent Name>

## Mission

<Two to four sentences: the outcome this agent owns, the audience it serves, and the posture it takes.
State the single job it exists to do, not a list of capabilities.>

## Operating Principles

- **<Principle name>.** <How it changes behavior in practice, phrased as a rule the agent follows.>
- **<Principle name>.** <Prefer principles that resolve ambiguity: what to do when the request is unclear,
  which artifacts may be written, what to confirm with the user first.>
- **<Principle name>.** <Name the files or directories the agent may modify, and those it must not touch.>

## Workflow

<Optional. Include only when the agent follows a repeatable sequence. Otherwise delete this section.>

1. **<Step>.** <What happens and what it produces.>
2. **<Step>.** <Gate or checkpoint before continuing.>
3. **<Step>.** <Final artifact and where it is written.>

## Out of Scope

- <Request this agent must decline.> Redirect to `<primitive-name>` (<type>).
- <Boundary that protects correctness, such as never editing generated or vendored files.>
- <Boundary that protects scope, such as never expanding into an adjacent domain.>

## Definition of Done

- [ ] <Observable artifact exists at a stated path.>
- [ ] <Property a reviewer can verify without rerunning the agent.>
- [ ] <Validation command passes, when one applies.>

## Anti-Patterns

1. **<Tempting but wrong request>.** Rejected because <reason>. Instead: <what the agent does>.
2. **<Shortcut that produces plausible but unverified output>.** The agent states uncertainty rather than
   inventing an answer.

## Related Primitives

| Name | Type | Use it for |
| --- | --- | --- |
| `<skill-name>` | skill | <the sub-task this agent delegates; skills are always invocable> |
| `<instructions-name>` | instructions | <the file globs whose conventions apply to this agent's edits> |
| `<agent-name>` | agent | <the handoff target, when `agent`/`task` is in `tools:`> |
