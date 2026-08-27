---
name: git-commit
description: >-
  Execute git commit with conventional commit message analysis, intelligent staging, and message
  generation. Use when user asks to commit changes, create a git commit, or mentions "/commit".
  Supports: (1) Auto-detecting type and scope from changes, (2) Generating conventional commit
  messages from diff, (3) Interactive commit with optional type/scope/description overrides, (4)
  Intelligent file staging for logical grouping
allowed-tools: Bash
license: MIT
---

<!-- Generated from harness/github-copilot/skills/git-commit/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Git commit with Conventional Commits

Create one logical Git commit by inspecting `git status --porcelain`, choosing the correct staged or working-tree diff, staging only intended files, and writing a Conventional Commits message that matches the actual change.

## When to invoke

- "Commit these changes."
- "Create a git commit for my staged files."
- "Use /commit for this diff."
- "Generate a conventional commit message and commit it."
- "Stage this logical change and commit it."

## Commit workflow

1. Run `git status --porcelain` before touching the index.
2. If files are already staged, inspect `git diff --staged`; otherwise inspect `git diff` for the working tree the user wants included.
3. Decide whether the requested change is one logical commit. If unrelated changes are present, stage specific paths only: `git add path/to/file1 path/to/file2`.
4. For mixed hunks in the same file, use `git add -p` instead of staging the whole file.
5. Preserve a user-supplied type, scope, description, issue reference, or breaking-change note unless the inspected diff contradicts it; explain any necessary correction.
6. Generate the subject from the diff: type, optional scope, and imperative description under 72 characters.
7. Execute `git commit -m "<type>[scope]: <description>"` when the user asked to commit. For a body or footer, pass separate `-m` arguments rather than embedding command substitutions.
8. If hooks fail, fix the hook findings and create a new commit attempt. Do not amend unless the user explicitly asks.

## Conventional Commit format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Element | Rule | Example |
| --- | --- | --- |
| `type` | Choose the primary intent of the diff. | `feat`, `fix`, `docs` |
| `scope` | Add a short module, package, app, or feature area only when it clarifies ownership. | `api`, `auth`, `docs` |
| `description` | Present tense, imperative mood, no trailing period, preferably <72 chars. | `add token refresh guard` |
| `body` | Explain why, migration notes, or context that does not fit the subject. | `This keeps old clients working during rollout.` |
| `footer` | Use for issue references and breaking changes. | `Closes #123`, `Refs #456`, `BREAKING CHANGE: extends key behavior changed` |

## Commit types

| Type | Use when the diff primarily changes |
| --- | --- |
| `feat` | User-visible capability or supported behavior. |
| `fix` | Bug fix, regression, broken behavior, or incorrect output. |
| `docs` | Documentation only. |
| `style` | Formatting/style only, with no logic change. |
| `refactor` | Internal restructuring with no feature or fix. |
| `perf` | Performance improvement. |
| `test` | Test additions or corrections. |
| `build` | Build system, packaging, dependency, or generated artifact behavior. |
| `ci` | CI, workflow, release automation, or config changes. |
| `chore` | Maintenance/misc work that does not fit another type. |
| `revert` | Reverts an earlier commit. |

## Staging rules

| Situation | Command | Constraint |
| --- | --- | --- |
| Exact files requested | `git add path/to/file1 path/to/file2` | Stage only named files. |
| Test files by pattern | `git add *.test.*` | Confirm the pattern does not catch unrelated files. |
| Component directory | `git add src/components/*` | Use only when all files belong to the same logical change. |
| Partial file | `git add -p` | Prefer hunk staging to unrelated whole-file commits. |
| Already staged | `git diff --staged` | Do not replace the index unless the user asks. |

## Git safety protocol

- Never commit secrets: `.env`, `credentials.json`, private keys, tokens, or generated secret dumps.
- Never update git config as part of committing.
- Never run destructive commands such as `--force` pushes or hard resets without an explicit request.
- Never skip hooks with `--no-verify` unless the user explicitly asks.
- Never force push to `main` or `master`.
- Reference issues with `Closes #123` only when the diff actually completes the issue; use `Refs #456` for partial work.
- Preserve legacy decision labels when useful: `type/scope`, `body/footer`, `area/module`, `feature/fix`, `system/dependencies`, `CI/config`, and `Add/update` tests all map to the Conventional Commits choices above.
- NEVER force push to `main/master`; keep this uppercase warning visible because it is the core Git safety rule.

## Breaking changes

Use either an exclamation mark in the subject or a `BREAKING CHANGE:` footer; use both when the risk is high or external users must notice it.

```text
feat!: remove deprecated endpoint

feat: allow config to extend other configs

BREAKING CHANGE: `extends` key behavior changed
```

## Gotchas

- **Do not stage by habit**: `git add .` can silently include secrets or another user's work.
- **Do not use past tense**: write `fix auth redirect`, not `fixed auth redirect`.
- **Do not force a vague scope**: omit the scope rather than writing `chore(repo)` when the type already carries the meaning.
- **Do not amend after hook failure by default**: the original instruction requires a new commit attempt unless the user asks for amend.

## Output template

```markdown
## Git commit result

**Status:** committed | message only | blocked
**Files reviewed:** <staged count> staged, <unstaged count> unstaged, <untracked count> untracked
**Diff used:** `git diff --staged` | `git diff`

**Commit message**
Subject: `<type>[optional scope]: <description>`
Body: `<body or none>`
Footer: `<footer(s) or none>`

**Commands run**
- `git status --porcelain`
- `git diff --staged` or `git diff`
- `git add <paths>` / `git add -p` if staging was needed
- `git commit -m "<subject>" [-m "<body>"] [-m "<footer>"]`

**Safety checks**
- Secrets check: pass | blocked with evidence
- Hook result: pass | fail with evidence
```

## Quality gate

- [ ] `git status --porcelain` was reviewed before staging or committing.
- [ ] The diff inspected is the diff being committed: `git diff --staged` for staged files or `git diff` for intended unstaged files.
- [ ] The commit contains one logical change and no unintended files.
- [ ] No secrets such as `.env`, `credentials.json`, private keys, or tokens are staged.
- [ ] The type is one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, or `revert`.
- [ ] The description is imperative, present tense, non-empty, and under 72 characters where practical.
- [ ] Breaking changes use `!` or a `BREAKING CHANGE:` footer.
- [ ] Hooks were not skipped unless the user explicitly requested `--no-verify`.
