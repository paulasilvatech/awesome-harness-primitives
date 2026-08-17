---
name: conventional-commit
description: >-
  Generate and execute Conventional Commit messages from staged or unstaged Git changes. Use this skill when the user asks to create a commit, write a conventional commit message, commit staged changes, format a commit as feat/fix/docs, or include a breaking-change footer.
---

# Conventional commit

## When to invoke

- "Create a conventional commit for these changes."
- "Write a commit message for my staged files."
- "Commit this as a fix with a scope."
- "Generate a Conventional Commits message with a BREAKING CHANGE footer."
- "Stage these files and commit them."

## Inputs

Use the user's request, staged changes, and unstaged changes as the source of truth. If the user specifies a type, scope, description, issue reference, or breaking-change note, preserve it unless the diff contradicts it.

## Commit workflow

1. Run `git status` to identify staged, unstaged, and untracked files.
2. Run `git diff --cached` when files are already staged; run `git diff` for unstaged changes that the user wants included.
3. Stage only the intended files with `git add <file>` when the user asks to commit unstaged work.
4. Construct the commit message using the Conventional Commits structure in this skill.
5. Execute the commit in the terminal without an additional confirmation prompt when the user asked you to commit:

```bash
git commit -m "type(scope): description"
```

For messages with a body or footer, pass each paragraph with additional `-m` arguments so Git preserves blank lines.

## Commit message structure

```xml
<commit-message>
  <type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert</type>
  <scope>()</scope>
  <description>A short, imperative summary of the change</description>
  <body>(optional: more detailed explanation)</body>
  <footer>(optional: e.g. BREAKING CHANGE: details, or issue references)</footer>
</commit-message>
```

| Field | Required | Rule |
| --- | --- | --- |
| `type` | Yes | Use one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, or `revert`. |
| `scope` | No | Add a short noun in parentheses when it clarifies the affected area. Omit the parentheses when there is no useful scope. |
| `description` | Yes | Use a short imperative phrase such as "add", not "added". |
| `body` | No | Explain why the change was made or add context that does not fit the subject. |
| `footer` | No | Use for breaking changes and issue references. |

## Type selection

| Type | Use when the diff primarily |
| --- | --- |
| `feat` | Adds user-visible functionality. |
| `fix` | Corrects a bug or broken behavior. |
| `docs` | Changes documentation only. |
| `style` | Changes formatting without changing behavior. |
| `refactor` | Restructures code without adding features or fixing bugs. |
| `perf` | Improves performance. |
| `test` | Adds or changes tests. |
| `build` | Changes build system, dependencies, packaging, or generated artifacts. |
| `ci` | Changes CI workflows or automation. |
| `chore` | Performs maintenance that does not fit another type. |
| `revert` | Reverts a previous commit. |

## Examples

| Scenario | Message |
| --- | --- |
| Parser feature | `feat(parser): add ability to parse arrays` |
| UI bug fix | `fix(ui): correct button alignment` |
| Documentation update | `docs: update README with usage instructions` |
| Processing cleanup | `refactor: improve data processing` |
| Dependency maintenance | `chore: update dependencies` |
| Breaking registration change | `feat!: send email on registration` with footer `BREAKING CHANGE: email service required` |

## Gotchas

- **Do not commit unintended files**: compare `git status` with the user's request before staging.
- **Do not bury breaking changes**: use `!` after the type or scope and include a `BREAKING CHANGE:` footer.
- **Do not use past tense**: descriptions should be imperative, for example `add cache`, not `added cache`.
- **Do not force a scope**: `docs: update README` is better than a vague scope such as `docs(repo): update README`.

## Output template

```markdown
### Conventional commit result

**Status:** committed | message only | blocked
**Files reviewed:** <staged count> staged, <unstaged count> unstaged

**Commit message**
Subject: `<type>(<scope>): <description>`
Body: `<body if needed, or "none">`
Footer: `<footer if needed, or "none">`

**Commands run**
- `git status`
- `git diff --cached` or `git diff`
- `git add <file>` if staging was needed
- `git commit -m "<subject>" [-m "<body>"] [-m "<footer>"]` if a commit was requested
```

## Quality gate

- [ ] `git status` was reviewed before staging or committing.
- [ ] The diff used to write the message matches the files being committed.
- [ ] The type is one of the allowed Conventional Commits types.
- [ ] The description is short, imperative, and non-empty.
- [ ] Scope is present only when it adds clarity.
- [ ] Breaking changes use `!` and/or a `BREAKING CHANGE:` footer.
- [ ] Body and footer are included with separate `-m` arguments when needed.
- [ ] The final response reports whether the commit was created or only a message was produced.
