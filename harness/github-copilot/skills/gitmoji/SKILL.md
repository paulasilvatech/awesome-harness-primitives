---
name: "gitmoji"
description: >-
  Generate commit messages that follow the gitmoji convention (https://gitmoji.dev) by choosing the single best emoji or shortcode for a diff, staged change, or plain-language change description. Use when asked to write a gitmoji commit, add an emoji to a commit message, choose a gitmoji, gitmoji this change, or follow a gitmoji-style commit history. Generates the message only and does not run git commands.
license: "MIT"
---

# Gitmoji

Generate a copyable commit message in the https://gitmoji.dev/ convention: infer the dominant change intent, select exactly one gitmoji, match unicode versus shortcode style, and write an imperative subject plus optional body.

## When to invoke

- "Write a gitmoji commit for these changes."
- "Gitmoji this diff."
- "Which gitmoji should I use?"
- "Add an emoji to my commit message."
- "This project uses gitmoji-style commits."

## Message format

```text
<intention> [scope?][:?] <message>
```

| Field | Rule |
| --- | --- |
| `intention` | Exactly one gitmoji expressing the goal of the commit. |
| `scope` | Optional codebase area in parentheses; use only if the existing history uses scopes or it clarifies the change. |
| `message` | Brief imperative phrase, lowercase start, no trailing period. |
| body | Optional; include only when the why is not obvious from the subject or when documenting a breaking change. |

Examples:

```text
✨ add multi-tenant support to the billing service
🐛 (auth) prevent token refresh loop on expired sessions
♻️ (api): extract pagination logic into shared helper
```

## Emoji selection

Consult `references/gitmoji-reference.md` before final selection because the full official list has 75 gitmojis and a more specific choice may exist.

| Emoji | Shortcode | Use when |
| --- | --- | --- |
| ✨ | `:sparkles:` | Introduce features. |
| 🐛 | `:bug:` | Fix a bug. |
| 🚑️ | `:ambulance:` | Critical production hotfix. |
| 📝 | `:memo:` | Add or update documentation. |
| ♻️ | `:recycle:` | Refactor without behavior change. |
| ✅ | `:white_check_mark:` | Add, update, or pass tests. |
| ⚡️ | `:zap:` | Improve performance. |
| 🎨 | `:art:` | Improve structure or formatting of code. |
| 🔥 | `:fire:` | Remove code or files. |
| 🔒️ | `:lock:` | Fix security or privacy issues. |
| ⬆️ | `:arrow_up:` | Upgrade dependencies. |
| 🔧 | `:wrench:` | Add or update configuration files. |
| 💄 | `:lipstick:` | Add or update UI/style files. |
| 💥 | `:boom:` | Introduce breaking changes. |
| 🚨 | `:rotating_light:` | Fix compiler or linter warnings. |
| 🌐 | `:globe_with_meridians:` | Internationalization or localization. |

## Procedure

1. Work from the provided diff, staged files, modified paths, or plain description.
2. If the repository style is unknown and history is available, inspect `git log --oneline -10` to choose unicode versus shortcode and scope style.
3. Identify the dominant intent. If the change mixes unrelated feature, fix, refactor, test, and docs work, choose the dominant intent and suggest splitting commits.
4. Prefer specific emojis over generic ones: typo ✏️ instead of 🐛, file move 🚚 instead of ♻️, trivial fix 🩹 instead of 🐛, security 🔒️ over bug.
5. Write a subject under 72 characters including the emoji when possible.
6. Add a body only for rationale, breaking changes, or context that does not fit the subject.
7. Output the message in a code block and one short explanation. Do not execute `git commit`.

## Style decisions

| Situation | Rule |
| --- | --- |
| Unicode history | Default to unicode, e.g. `✨ add dark mode`. |
| Shortcode history | Match shortcode, e.g. `:sparkles: add dark mode`. |
| Tests | Use ✅ for passing tests; use 🧪 only for intentionally failing tests such as a TDD red step. |
| Hotfix | Use 🚑️ only for urgent production fixes; ordinary bugs are 🐛. |
| Formatting | Use 🎨 for code structure/formatting; use 💄 for visual UI/style files. |
| Breaking change | Use 💥 and document the break in the body. |
| Revert | Use ⏪️ with a subject referencing the reverted commit. |
| Merge | Use 🔀 `merge branch '<name>' into <target>`. |
| Initial commit | Use 🎉 `begin project`. |
| Work in progress | Use 🚧 and say what remains. |
| No obvious match | Re-scan `references/gitmoji-reference.md`, then fall back to ✨, 🐛, or ♻️. |

## Limits

- Do not run `git commit` or any other mutating git command.
- If the project follows plain Conventional Commits from https://www.conventionalcommits.org/ without emojis, use the `git-commit` skill instead.
- If the convention is ambiguous, ask for recent history or inspect `git log --oneline -10` when allowed.

## Progressive disclosure and bundled resources

- `references/gitmoji-reference.md`: complete official gitmoji list; read it before choosing a final emoji.

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `adding/updating`
- `commit-message-storyteller`
- `feat:`
- `fix:`
- `non-critical`
- `re-triggered`
- `staged/modified`
- `well-formed`

Shortcode style may be preferred on GitHub or GitLab when repository history uses codes such as `:sparkles:`.

## Output template

```markdown
## Gitmoji commit message

```text
<emoji or shortcode> (<optional-scope>) <imperative subject>

<optional body>
```

**Why:** <one sentence explaining why this gitmoji matches the dominant intent>
**Style matched:** unicode | shortcode | unknown
```

## Quality gate

- [ ] Exactly one gitmoji or shortcode starts the subject.
- [ ] The selected emoji matches the dominant intent and was checked against `references/gitmoji-reference.md`.
- [ ] Unicode versus shortcode style matches existing history when evidence is available.
- [ ] Subject is imperative, concise, lowercase after the emoji unless a proper noun requires capitalization, and has no trailing period.
- [ ] Mixed unrelated changes are called out as candidates for separate commits.
- [ ] No git command that mutates history is executed.

## References

- [gitmoji](https://gitmoji.dev)
- [gitmoji with trailing slash](https://gitmoji.dev/)
- [Conventional Commits](https://www.conventionalcommits.org/)
