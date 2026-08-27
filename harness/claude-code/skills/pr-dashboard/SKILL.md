---
name: pr-dashboard
description: >-
  Open a browser-based GitHub pull request dashboard for a date range and role filter using the
  bundled CLI. Use when the user asks to show my PRs, open PR dashboard, check pull request
  status, see requested reviews, assigned PRs, all involved PRs, or review PR activity for a week,
  month, year, or explicit date range.
---

<!-- Generated from harness/github-copilot/skills/pr-dashboard/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# PR dashboard

Parse a user's pull request dashboard request into a date query and role filter, run the bundled Node.js dashboard CLI through GitHub CLI authentication, and report whether the browser dashboard opened.

## When to invoke

- "Show my PRs."
- "Open PR dashboard for last 2 weeks."
- "Show requested reviews this month."
- "Check assigned pull requests for March 2026."
- "Show all PRs from 2026-01-01 to 2026-03-31."

## Prerequisites and context

- GitHub CLI (`gh`) must be installed and authenticated; if authentication fails, suggest `gh auth login`.
- Node.js must be available to run `pr-dashboard-cli.mjs`.
- The dashboard script is bundled under `pr-dashboard/scripts/`; locate it before execution.

## Request parsing

| User says | `query` | `role` |
| --- | --- | --- |
| `show my PRs` | `last 7 days` | `Authored by me` |
| `show my PRs last 2 weeks` | `last 2 weeks` | `Authored by me` |
| `PR dashboard this month reviews` | `this month` | `Requested reviews` |
| `PR dashboard march 2026 assigned` | `march 2026` | `Assigned to me` |
| `show all PRs last 30 days` | `last 30 days` | `All` |

## Role mapping

| Keywords | Role |
| --- | --- |
| `my PRs`, `authored`, `I wrote` | `Authored by me` |
| `reviews`, `review requested`, `reviewing` | `Requested reviews` |
| `assigned` | `Assigned to me` |
| `all`, `involves me` | `All` |

Default to `last 7 days` and `Authored by me` when the user does not specify a date range or role.

## Supported date ranges

Pass natural language through as-is when it matches one of these forms:

| Form | Examples |
| --- | --- |
| Relative days/weeks | `last 7 days`, `last 2 weeks`, `last 30 days` |
| Calendar period | `this week`, `last week`, `this month`, `last month` |
| Month and year | `march 2026`, `feb 2025` |
| Explicit range | `2026-01-01 - 2026-03-31` |
| Whole year | `2025` |

## Procedure

1. Extract `query` and `role` from the user request using the parsing and role tables.
2. Locate the bundled CLI script without assuming the installation root:

```bash
SKILL_SCRIPT=$(find ~/.copilot -name "pr-dashboard-cli.mjs" -path "*/pr-dashboard/scripts/*" 2>/dev/null | head -1)
node "$SKILL_SCRIPT" "<query>" "<role>"
```

3. If the command exits successfully, tell the user the dashboard is opening in their browser.
4. If it fails, show the error output and recommend `gh auth login` when the error indicates authentication.

## Progressive disclosure and bundled resources

- `scripts/pr-dashboard-cli.mjs`: CLI entry point that queries GitHub and opens the dashboard.
- `scripts/lib`: helper modules used by the CLI.
- `assets/dashboard.html`: browser UI template consumed by the CLI.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `gh` authentication error | GitHub CLI is not logged in or token expired. | Run `gh auth login`, then retry the same query and role. |
| `SKILL_SCRIPT` is empty | Skill is not installed under `~/.copilot` or script path changed. | Locate `pr-dashboard/scripts/pr-dashboard-cli.mjs` in the active skill installation. |
| Browser does not open | Headless environment or OS browser launcher unavailable. | Report the generated output path or command output if the script provides one. |

## Output template

```markdown
### PR dashboard result

**Status:** opened | blocked
**Query:** `<query>` / `<date range>`
**Role:** `<role>` / `Authored by me` | `Requested reviews` | `Assigned to me` | `All`
**Script:** `<path to pr-dashboard-cli.mjs>`

**Command**
`node "$SKILL_SCRIPT" "<query>" "<role>"`

**Validation**
- GitHub CLI authentication: pass | fail | not checked
- Dashboard launch: pass | fail
```

## Quality gate

- [ ] The user request was parsed into a supported date `query` and role.
- [ ] Defaults were applied only when date range or role were missing.
- [ ] `SKILL_SCRIPT` was located under `pr-dashboard/scripts/` before running Node.js.
- [ ] The command used `node "$SKILL_SCRIPT" "<query>" "<role>"`.
- [ ] Authentication failures mention `gh auth login`.
- [ ] The final response states whether the dashboard opened or why it was blocked.
