---
name: commit-message-storyteller
description: >-
  Analyze git diffs, staged changes, or plain change descriptions and generate narrative
  Conventional Commits messages that explain why the change matters. Use when asked to "write a
  commit message", "generate a commit", "describe my changes", "what should I commit this as",
  "commit this", "summarize my diff", or "help me commit".
---

<!-- Generated from harness/github-copilot/plugins/git-github-workflow/skills/commit-message-storyteller/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Commit message storyteller

Transforms git diffs, staged files, modified file lists, or plain descriptions into copyable Conventional Commits messages with a clear subject, an optional story-driven body, and issue or breaking-change footers.

## When to invoke

- "Write a commit message for this diff."
- "What should I commit this as?"
- "Summarize my staged changes as a Conventional Commit."
- "Help me commit with a message that explains why."
- "Generate multiple commit messages if this diff should be split."

## Prerequisites and context

Have at least one source of change context:

- `git diff` for unstaged working tree changes.
- `git diff --staged` or `git diff --cached` for staged files.
- A plain-language description of what changed and why.
- A list of modified files, functions, symbols, or issue numbers.

Use https://www.conventionalcommits.org/ as the specification source. Read `references/conventional-commits-guide.md` when examples or scope guidance are needed.

## Procedure

1. Gather the change context: what changed, why it changed, and who or what triggered it.
2. Infer or confirm whether the diff is one logical change or several unrelated changes.
3. Select the Conventional Commits type from the table below.
4. Write the subject in imperative mood, with an optional scope only when it clarifies the affected area.
5. Add a body only when it tells the story: the previous problem, the reason for the change, or the impact.
6. Add footers for issues and breaking changes.
7. Return copyable messages and a one-line explanation of the story told.

## Commit type selection

| Type | Use when the change primarily |
| --- | --- |
| `feat` | Adds a new feature or capability. |
| `fix` | Corrects a bug or incorrect behavior. |
| `refactor` | Restructures code without changing behavior. |
| `perf` | Improves performance. |
| `docs` | Changes documentation only. |
| `style` | Changes formatting, whitespace, or semicolons with no logic change. |
| `test` | Adds or updates tests. |
| `chore` | Changes build process, dependencies, generated files, or routine config. |
| `ci` | Changes CI/CD pipelines or automation. |
| `revert` | Reverts a previous commit. |

## Message construction

```text
<type>(<optional scope>): <short imperative summary>

<body — the story: why this change was made, what problem it solves>

<footer — issue refs, breaking change notices>
```

| Part | Rule |
| --- | --- |
| Subject | Keep it under 72 characters, lowercase after the colon, no final period. |
| Verb | Use imperative mood: `add`, `fix`, `remove`; not `added`, `fixes`, or `removed`. |
| Body | Explain the why, because the diff already shows the what. Keep lines under 100 characters. |
| Footer | Use `Closes #123`, `Fixes #456`, `Refs #789`, and `BREAKING CHANGE: <description>` when applicable. |

## Split heuristics

| Situation | Action |
| --- | --- |
| Different files with unrelated purposes | Suggest multiple commits. |
| Same file but distinct concerns, such as bug fix plus refactor | Suggest splitting unless the refactor enables the fix. |
| Everything is tightly coupled | Produce one message. |
| User says `keep it short` | Omit the body and produce a strong subject line. |
| No issue number exists | Omit the footer entirely. |

## Gotchas

- **Do not write update-only subjects**: replace `update file.js` with the specific intent and impact.
- **Do not invent why**: infer from the diff when possible; otherwise mark the reason as missing or keep the body neutral.
- **Do not bury breaking changes**: add `BREAKING CHANGE:` even when the subject already uses `!`.
- **Do not ask when context is enough**: only ask whether one diff is one logical change or multiple when the split is genuinely ambiguous.

## Progressive disclosure and bundled resources

- `references/conventional-commits-guide.md`: detailed examples, type choices, and scope guidelines.

## Commit context vocabulary

Preserve issue and audience context when present: `Who/what` triggered the change, whether it affects `open-source` maintainers, and runtime details such as `mid-request` failures.

## Output template

````markdown
### Commit message storyteller result

**Status:** message ready | split recommended | blocked
**Source reviewed:** `git diff` | `git diff --staged` | `git diff --cached` | description | file list

**Commit message**
```text
<type>(<scope>): <imperative summary>

<body explaining why, omitted when not needed>

<footer such as Closes #123 or BREAKING CHANGE: details>
```

**Story told:** <one sentence explaining the problem, decision, and impact>

**Split guidance:** <one commit is fine | suggested commit boundaries>
````

## Quality gate

- [ ] The message follows Conventional Commits type and subject rules.
- [ ] The subject is imperative, non-empty, lowercased after the colon, and under 72 characters.
- [ ] The body explains why, not just what files changed.
- [ ] Breaking changes use a `BREAKING CHANGE:` footer.
- [ ] Issue references use `Closes #123`, `Fixes #456`, or `Refs #789` only when known.
- [ ] Logically unrelated changes are split or explicitly called out.
- [ ] `references/conventional-commits-guide.md` is used when detailed examples are needed.
