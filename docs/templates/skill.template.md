<!-- AUTHORING — delete this block after copying.
Target path: skills/<skill-name>/SKILL.md   The directory name IS the skill name.
Spec: docs/COPILOT-HARNESS-SPEC.md §3

Frontmatter
  name         REQUIRED. 1-64 chars, kebab-case ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$, no "--",
               and it MUST equal the parent directory name.
  description  REQUIRED. 1-1024 chars. Must state BOTH what the skill does AND when to use it —
               this string is the only thing loaded at session start, so it is what triggers activation.
               Write "… Use this skill when <trigger>." (validator: SK005 WARNING if WHEN is missing).
  allowed-tools / user-invocable / disable-model-invocation / argument-hint / license / metadata / tags
               Optional. Put author, version, category inside metadata: they are not top-level keys.

Body: non-empty, keep under ~500 lines. The whole body enters context on activation, so every line
must help execute the task — no meta-commentary about the repository or the workshop it came from.
Bundled resources live in scripts/, references/, assets/ inside this skill directory and are the ONLY
relative paths allowed. Use $ARGUMENTS in the body when the skill is user-invocable.
-->
---
name: "<skill-name>"
description: "<What this skill produces or changes.> Use this skill when <trigger phrasing 1>, <trigger phrasing 2>, or <trigger phrasing 3>."
allowed-tools: ["view", "grep", "glob", "edit"]
user-invocable: true
argument-hint: "<argument>"
---

# <Skill Title>

<One paragraph: the transformation this skill performs, its input, and its output. Name the worked
example technology, and state whether the same procedure generalizes to others.>

## When to invoke

- "<A request phrased the way a user would actually type it.>"
- "<A second phrasing that should also match.>"
- "<A phrasing that looks similar but should NOT match — say which skill handles it instead.>"

## Workflow

### 1. <First step>

- <Concrete action.>
- <Decision rule for the ambiguous case.>

### 2. <Second step>

<Explain the judgment involved, then show it as a contrast table when the distinction is subtle.>

| Do this | Not this |
| --- | --- |
| <Good example.> | <The near-miss it replaces.> |

### 3. <Third step>

<The artifact produced and exactly where it is written.>

## Rules

- <Invariant the skill must never break, such as preserving behavior or encoding.>
- <Content constraint, such as English only, no emojis, no sensitive data in examples.>
- <Verification the skill performs before declaring success.>

## Output Template

<Delete this section when the skill does not emit a fixed artifact.>

```markdown
<The exact structure of the generated file, with placeholders.>
```

## Quality Gate

- [ ] <The produced artifact exists and is well-formed.>
- [ ] <Behavior or output is unchanged where it had to be preserved.>
- [ ] <Every command shown in the output was actually run and works.>
- [ ] <Content constraints hold: English, no emojis, no sensitive data.>

## Related Primitives

| Name | Type | Use it for |
| --- | --- | --- |
| `<skill-name>` | skill | <the adjacent skill and the boundary between them> |
| `<instructions-name>` | instructions | <the conventions this skill must respect while editing> |
