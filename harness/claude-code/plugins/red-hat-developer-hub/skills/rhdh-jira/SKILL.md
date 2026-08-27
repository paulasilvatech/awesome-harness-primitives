---
name: rhdh-jira
description: >-
  Use this skill when the user works with RHDH Jira projects RHIDP, RHDHPLAN, RHDHBUGS, or
  RHDHSUPP using acli, GraphQL, and REST fallback. Trigger for Jira keys, creating features,
  epics, stories, tasks, bugs, assigning owners, refinement, sprint planning, sprint reports,
  release status, status updates, duplicate checks, sizing, or sprint ceremony prep.
---

<!-- Generated from harness/github-copilot/plugins/red-hat-developer-hub/skills/rhdh-jira/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# RHDH Jira

Execute Red Hat Developer Hub Jira workflows for RHIDP, RHDHPLAN, RHDHBUGS, and RHDHSUPP by routing the user's request to the correct command reference, preferring `acli` for simple work, and using GraphQL or REST only when the workflow requires bulk reads or custom-field writes.

## When to invoke

- "Refine RHIDP-123 and check whether it is ready for sprint planning."
- "Create a RHDHPLAN feature from this context."
- "Assign owners for these RHDH Jira issues."
- "Prepare the RHDH sprint report and release status."
- "Update Jira status, comments, transitions, and parent cascade."

## Prerequisites and context

- `acli` must be on `PATH` and authenticated with API token auth.
- Python 3 is required for helper scripts.
- REST and GraphQL fallback require token setup validated by `scripts/setup.py`.
- Run `python scripts/setup.py` before live Jira workflows; use `python scripts/setup.py --json` when structured capability checks are needed.
- Do not read token file contents into chat. If REST or GraphQL setup is missing, state the missing capability and continue with `acli` when possible.

## Procedure

1. Identify the command from the first word of the user's request, a Jira key, or the requested outcome.
2. Load the relevant command reference before running Jira operations.
3. Ask only for missing project, issue type, team, or mutation confirmation.
4. Prefer read-only discovery before mutation, including duplicate checks for creation workflows.
5. Present planned mutations and wait for user confirmation before creating, assigning, transitioning, linking, closing, or commenting.
6. Use `--yes` only after the user confirms the exact mutation.
7. Report data sources, query scope, and any fallback path used.

## Command routing

| Command | Use when | Reference |
| --- | --- | --- |
| `assign` | Recommend or assign owners using expertise and capacity. | `references/assign.md` |
| `refine` | Check readiness, duplicates, hierarchy, fields, comments, and sprint fit. | `references/refine.md` |
| `plan` | Prepare sprint planning with carryover, velocity, capacity, and ready queue. | `references/plan.md` |
| `sprint-report` | Summarize sprint review, demos, completion, and member breakdown. | `references/sprint-report.md` |
| `release` | Produce release readiness, feature matrix, dependencies, bugs, and risks. | `references/release.md` |
| `to-feature` | Create an RHDHPLAN Feature from context. | `references/to-feature.md` |
| `to-epic` | Create an RHIDP Epic from context. | `references/to-epic.md` |
| `to-issue` | Create a Story, Task, Bug, Spike, or Sub-task from context. | `references/to-issue.md` |
| `update-jira-status` | Update issue status, comments, transitions, and parent cascade. | `references/update-jira-status.md` |

## API preference and projects

Use APIs in this order:

1. `acli` for simple single-issue reads and writes.
2. GraphQL for bulk reads, expertise profiles, capacity, and refinement checks.
3. REST API for custom-field writes or fallback when `acli` cannot mutate the field.

Before REST or GraphQL, run `python scripts/setup.py --json` and confirm the token file is configured.

| Key | Purpose | Issue types |
| --- | --- | --- |
| RHIDP | Engineering work | Epic, Story, Task, Sub-task, Vulnerability |
| RHDHPLAN | Program planning | Feature, Outcome, Feature Request, Sub-task |
| RHDHBUGS | Product defects | Bug, Sub-task |
| RHDHSUPP | Support-engineering interactions | Bug |

Do not query archived RHDHPAI unless the user explicitly asks for historical analysis.

## Progressive disclosure and bundled resources

| Resource | Use when |
| --- | --- |
| `references/acli-commands.md` | Running unfamiliar `acli` commands or handling flag behavior. |
| `references/fields.md` | Looking up fields, custom field IDs, labels, priorities, and components. |
| `references/workflows.md` | Checking transitions and status exit criteria. |
| `references/templates.md` | Creating issues. |
| `references/jql-patterns.md` | Building JQL, finding boards, and sprint queries. |
| `references/auth.md` | Setting up REST or GraphQL authentication. |
| `references/rest-api-fallback.md` | Updating custom fields when `acli` cannot. |
| `references/graphql-queries.md` | Complex reads and bulk issue queries. |
| `references/duplicates.md` | Duplicate detection. |
| `references/grill.md` | Challenging incomplete issue requests before creation. |
| `references/sizing.md` | T-shirt sizing and story points. |
| `references/support.md` | Support-engineering workflow details. |
| `scripts/setup.py` | Verify live Jira, REST, and GraphQL capability. |
| `scripts/parse_issues.py` | Enrich JSON search results with custom fields, labels, sprint, story points, and team. |
| `scripts/command-metadata.json` | Command metadata for routing and help. |
| `assets/examples/` | Example artifacts. |
| `assets/templates/` | Templates consumed by creation workflows. |

## Safety and gotchas

- **Confirm before mutation**: creation, assignment, transition, linking, closing, and commenting require explicit user confirmation.
- **Do not expose secrets**: never paste Jira tokens, API keys, or `.jira-token` contents.
- **`acli auth status` can mislead**: use a Jira project list smoke test for API token auth.
- **Issue key flags vary**: `view` uses a positional issue key, while many mutations use `--key`.
- **`--fields` is restrictive on search**: use JSON plus `scripts/parse_issues.py --enrich` for custom fields, labels, sprint, story points, and team.
- **Team JQL is not display-name based**: use `Team[Team]` syntax and the team UUID.
- **Descriptions can be ADF**: do not round-trip Atlassian Document Format through plain `--description`.
- **Search results can truncate silently**: use `--limit 200`, `--count`, or pagination for bulk work.
- **Prefer comments for decision trail**: do not bloat issue descriptions with every decision update.

## Output template

```markdown
## RHDH Jira result

**Status:** complete | needs confirmation | blocked
**Command:** assign | refine | plan | sprint-report | release | to-feature | to-epic | to-issue | update-jira-status
**Projects/issues:** <RHIDP/RHDHPLAN/RHDHBUGS/RHDHSUPP keys>
**Data sources:** acli | GraphQL | REST | fallback

### Findings or planned changes
- <finding, recommendation, or mutation>

### Validation
- `python scripts/setup.py`: pass | fail | not run
- Custom-field enrichment: pass | fail | not needed
- User confirmed mutation: yes | no | not applicable
```

## Quality gate

- [ ] The request is routed to the correct command reference.
- [ ] `python scripts/setup.py` or `python scripts/setup.py --json` was run before live Jira access requiring configured capabilities.
- [ ] GraphQL and REST are used only when their setup is validated or `acli` cannot satisfy the workflow.
- [ ] Mutations are presented and confirmed before execution; `--yes` is used only after confirmation.
- [ ] Tokens, API keys, and `.jira-token` contents are never exposed.
- [ ] Sprint or release reports state data sources, query scope, and fallback used.
- [ ] The output follows `## Output template` exactly.
