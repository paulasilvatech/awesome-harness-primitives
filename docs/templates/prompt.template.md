<!-- AUTHORING — delete this block after copying.
Target path: .github/prompts/<name>.prompt.md   Invoked in chat as /<name>.

SCOPE WARNING — this type is NOT part of the Copilot CLI harness.
docs/COPILOT-HARNESS-SPEC.md recognizes five primitives: agents, instructions, skills, plugins, hooks.
Prompt files are a VS Code feature. The VS Code documentation states: "Agents running on the Agent Host
don't use prompt files. To use an existing prompt with the Copilot agent, convert it to an agent skill."
  - Authoring for VS Code only  -> use this template.
  - Authoring for the CLI, or for both -> use docs/templates/skill.template.md instead. A user-invocable
    skill is also reachable as /<skill-name>, so nothing is lost.
  - Never reference a .prompt.md file from an agent, instructions file, or skill.

Frontmatter — the six keys VS Code recognizes, all optional:
  description    Short description of the prompt.
  name           Slash-command name; defaults to the filename.
  argument-hint  Hint text shown in the chat input.
  agent          "ask" | "agent" | "plan" | the name of a custom agent.
  model          Defaults to the model selected in the picker.
  tools          VS Code tool names, tool sets, or <server>/* for MCP.

TOOL VOCABULARY WARNING — VS Code tool names are NOT the CLI tokens. "search" is a real VS Code tool but
a silent no-op in the CLI. Never copy a tools: list between a prompt file and an agent file.
-->
---
name: "<prompt-name>"
description: "<What this prompt does in one sentence.>"
argument-hint: "<argument>=<value>"
agent: "<custom-agent-name>"
---

# /<prompt-name>

## Objective

<Two or three sentences: the outcome this run produces and where it sits in the larger sequence.>

## When to Invoke

<The moment in the workflow this prompt belongs to, and what must have happened before it.>

## Preconditions

- <State the workspace must already be in.>
- <Artifact from a previous step that this run consumes.>

## Inputs the User Must Provide

- <Input and its default value.>
- <Confirmation the run depends on.>

## What I Will Do

- <Observable action, phrased as a commitment.>
- <Observable action.>

## What I Will NOT Do

- <Action deferred to a later step, naming the step.>
- <Answer the run must not fabricate; it marks the item unknown instead.>

## Output Format

<Where the artifact is written and its exact skeleton.>

```markdown
# <Artifact Title>
## <Section>
## <Section>
```

## Definition of Done

- [ ] <The artifact exists at the stated path.>
- [ ] <A second person can verify the result independently.>
- [ ] <Every unknown is marked as unknown rather than guessed.>

## Prompt Body

<The instruction text sent to the model. Keep the steps ordered and explicit.>

**Step 1 — <name>.** <What to do and what to output.>

**Step 2 — <name>.** <What to do, including the table or format to emit.>

**Step 3 — <name>.** <The write step and the target path.>

<Close with the hard constraint for this run, such as: do not open any file to read its contents.>

## Invocation Example

```text
/<prompt-name> <argument>=<value>
```

## Related Primitives

| Name | Type | Use it for |
| --- | --- | --- |
| `<agent-name>` | agent | <the agent this prompt runs under> |
| `<skill-name>` | skill | <the CLI-compatible equivalent or the procedure this prompt defers to> |
