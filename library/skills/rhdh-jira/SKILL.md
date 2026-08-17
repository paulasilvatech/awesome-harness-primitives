---
name: rhdh-jira
description: "Work with RHDH Jira projects RHIDP, RHDHPLAN, RHDHBUGS, and RHDHSUPP using acli, GraphQL, and REST fallback. Use for Jira keys, creating features, epics, stories, tasks, bugs, assigning owners, refinement, sprint planning, sprint reports, release status, status updates, duplicate checks, sizing, or sprint ceremony prep."
---

# RHDH Jira

Use this skill for Red Hat Developer Hub Jira workflows in RHIDP, RHDHPLAN, RHDHBUGS, and RHDHSUPP.

## Prerequisites

- `acli` on `PATH`.
- Python 3 for helper scripts.
- API token authentication configured for `acli`.
- Optional REST and GraphQL fallback token file, validated by `scripts/setup.py`.

Run setup verification before workflows that need live Jira access:

```bash
python scripts/setup.py
```

Use `python scripts/setup.py --json` when the workflow needs structured checks.

## First Step

Identify the command from the user request. If the first word matches a command below, load that reference and follow it. If the user gives a Jira key or prose request, infer the command and ask only for missing project, issue type, team, or confirmation.

Do not read token file contents into chat. For missing REST or GraphQL setup, state the missing capability and continue with `acli` when possible.

## Commands

| Command | Use when | Reference |
| --- | --- | --- |
| `assign` | Recommend or assign owners using expertise and capacity. | [references/assign.md](references/assign.md) |
| `refine` | Check readiness, duplicates, hierarchy, fields, comments, and sprint fit. | [references/refine.md](references/refine.md) |
| `plan` | Prepare sprint planning with carryover, velocity, capacity, and ready queue. | [references/plan.md](references/plan.md) |
| `sprint-report` | Summarize sprint review, demos, completion, and member breakdown. | [references/sprint-report.md](references/sprint-report.md) |
| `release` | Produce release readiness, feature matrix, dependencies, bugs, and risks. | [references/release.md](references/release.md) |
| `to-feature` | Create an RHDHPLAN Feature from context. | [references/to-feature.md](references/to-feature.md) |
| `to-epic` | Create an RHIDP Epic from context. | [references/to-epic.md](references/to-epic.md) |
| `to-issue` | Create a Story, Task, Bug, Spike, or Sub-task from context. | [references/to-issue.md](references/to-issue.md) |
| `update-jira-status` | Update issue status, comments, transitions, and parent cascade. | [references/update-jira-status.md](references/update-jira-status.md) |

## API Preference

Use this order:

1. `acli` for simple single-issue reads and writes.
2. GraphQL for bulk reads, expertise profiles, capacity, and refinement checks.
3. REST API for custom-field writes or fallback when `acli` cannot mutate the field.

Before REST or GraphQL, run `python scripts/setup.py --json` and confirm the token file is configured. If unavailable, continue with `acli` where possible.

## Projects

| Key | Purpose | Issue types |
| --- | --- | --- |
| RHIDP | Engineering work | Epic, Story, Task, Sub-task, Vulnerability |
| RHDHPLAN | Program planning | Feature, Outcome, Feature Request, Sub-task |
| RHDHBUGS | Product defects | Bug, Sub-task |
| RHDHSUPP | Support-engineering interactions | Bug |

Do not query archived RHDHPAI unless the user explicitly asks for historical analysis.

## Reference Files

| File | Use when |
| --- | --- |
| [references/acli-commands.md](references/acli-commands.md) | Running unfamiliar `acli` commands or handling flag behavior. |
| [references/fields.md](references/fields.md) | Looking up fields, custom field IDs, labels, priorities, and components. |
| [references/workflows.md](references/workflows.md) | Checking transitions and status exit criteria. |
| [references/templates.md](references/templates.md) | Creating issues. |
| [references/jql-patterns.md](references/jql-patterns.md) | Building JQL, finding boards, and sprint queries. |
| [references/auth.md](references/auth.md) | Setting up REST or GraphQL authentication. |
| [references/rest-api-fallback.md](references/rest-api-fallback.md) | Updating custom fields when `acli` cannot. |
| [references/graphql-queries.md](references/graphql-queries.md) | Complex reads and bulk issue queries. |
| [references/duplicates.md](references/duplicates.md) | Duplicate detection. |
| [references/grill.md](references/grill.md) | Challenging incomplete issue requests before creation. |
| [references/sizing.md](references/sizing.md) | T-shirt sizing and story points. |

## Safety and Confirmation

- Confirm before creating, assigning, transitioning, linking, closing, or commenting on Jira issues.
- Use `--yes` only after the user confirms the mutation.
- Do not expose Jira tokens, API keys, or `.jira-token` contents.
- Prefer comments for decision trail instead of bloating descriptions.
- When closing or descoping, add rationale and set resolution appropriately.

## Common Gotchas

- `acli auth status` checks OAuth and can be misleading with API token auth. Use a Jira project list smoke test instead.
- `view` uses positional issue key, while many mutations use `--key`.
- `--fields` is restrictive on search. Use JSON plus `scripts/parse_issues.py --enrich` for custom fields, labels, sprint, story points, and team.
- Team field JQL uses the `Team[Team]` syntax and the team UUID, not the display name.
- Descriptions read through JSON can be Atlassian Document Format. Do not round-trip ADF through plain `--description`.
- `acli` can silently truncate search results. Use `--limit 200`, `--count`, or pagination for bulk work.

## Validation

- Run `python scripts/setup.py` before live Jira workflows.
- For reads involving custom fields, use `scripts/parse_issues.py --enrich`.
- For mutations, present planned changes and wait for user confirmation.
- For sprint or release reports, state data sources, query scope, and any fallback used.