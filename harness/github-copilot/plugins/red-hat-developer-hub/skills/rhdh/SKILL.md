---
name: rhdh
description: >-
  Route and support Red Hat Developer Hub (RHDH) work across plugin development, overlay management, local testing, Jira, repository navigation, version compatibility, CI debugging, and environment setup. Use this skill when the user asks about RHDH, Developer Hub, dynamic plugins, overlays, rhdh-local, RHDH Jira, plugin catalogs, repositories, or CI/CD tasks.
---

# RHDH

Use this entry point for Red Hat Developer Hub work: initialize the bundled CLI, check environment readiness, route to specialized RHDH skills or references, and track durable activity when work spans sessions.

## When to invoke

- "Help with Red Hat Developer Hub."
- "Work on an RHDH dynamic plugin."
- "Triage this RHDH overlay or CI failure."
- "Set up rhdh-local or test a plugin catalog."
- "Create or update an RHDH Jira issue."

## Prerequisites and context

- Resolve the skill directory from this `SKILL.md` file before running bundled commands.
- Set the CLI variable to the local script:

```bash
RHDH="<skill-dir>/scripts/rhdh"
```

- Run `$RHDH` to check the environment unless the user asks only a conceptual question.
- If output reports `needs_setup: true`, run `$RHDH doctor` before repository or plugin operations.
- Use `$RHDH config init` or `$RHDH config set <key> <path>` when local repository paths are missing.

## Routing

| User intent | Route |
| --- | --- |
| Onboard, update, fix, triage, analyze PRs, publish, or manage overlay workspace | Load the `overlay` skill if available. |
| Create backend plugin, frontend plugin, export, OCI packaging, `tgz`, dynamic plugin wiring, mount points, routes, or entity tabs | Load the `create-plugin` skill if available. |
| Enable, disable, test, start, stop, health-check, backup, restore, or troubleshoot local RHDH | Load the `rhdh-local` skill if available. |
| Jira issue creation, assignment, refinement, sprint planning, release status, `RHIDP`, `RHDHPLAN`, `RHDHBUGS`, or `RHDHSUPP` | Load the `rhdh-jira` skill if available. |
| Environment check, repo path setup, activity review, or repository navigation | Use the bundled CLI and references in this skill. |

Do not use relative links to other primitives; refer to specialized skills by name and type.

## CLI commands

```bash
$RHDH                         # Environment status and next steps
$RHDH doctor                  # Full environment check
$RHDH config init             # Auto-detect repo paths
$RHDH config show             # Show configured paths
$RHDH config set overlay /path
$RHDH config set local /path
$RHDH config set rhdh /path
$RHDH workspace list
$RHDH workspace status <name>
$RHDH log show --limit 10
$RHDH todo list
```

## Operating principles

- Ask only when required information is missing; if intent is clear, proceed with the matching route.
- Track meaningful milestones with `$RHDH log add` and blockers with `$RHDH todo` when work spans sessions.
- Before using GitHub CLI patterns for RHDH repositories, read `references/github-reference.md`.
- Before navigating RHDH repositories, read `references/rhdh-repos.md`.
- Do not guess repository relationships, versions, PR commands, or publish checks; verify through references or CLI output.
- Prefer read-only GitHub CLI commands first and confirm before mutating PRs, labels, comments, or assignments.

## Activity tracking

Use activity tracking for multi-session work or external follow-up:

```bash
$RHDH log add "Started onboarding plugin-name" --tag onboard --tag plugin-name
$RHDH todo add "Follow up on PR #123" --tag pr --tag blocked
$RHDH todo note <slug> "Waiting for CI rerun"
$RHDH todo done <slug>
```

Tracking is recommended, not mandatory. Do not let tracking block small one-step tasks.

## Progressive disclosure and bundled resources

| Resource | Use when |
| --- | --- |
| `scripts/rhdh` | Running environment checks, config, workspace status, logs, and todos. |
| `rhdh/` | Python CLI implementation behind `scripts/rhdh`; inspect only when changing or debugging this skill. |
| `references/rhdh-repos.md` | Understanding RHDH repositories and where work belongs. |
| `references/github-reference.md` | Running GitHub CLI commands for PRs, CI, labels, comments, and publish triggers. |
| `references/versions.md` | Checking RHDH and Backstage version compatibility. |
| `references/slack-notification.md` | Drafting Slack notifications for RHDH work. |

## Gotchas

- **Do not bypass `$RHDH doctor` when setup is incomplete**: repository paths, GitHub CLI, container runtime, and rhdh-local assumptions may be wrong.
- **Do not guess RHDH repository relationships**: read `references/rhdh-repos.md` before navigation.
- **Do not mutate GitHub state as the first command**: inspect first, then confirm mutating PR, label, comment, or assignment operations.
- **Do not let tracking become ceremony**: log milestones and blockers only when they help continuity.

## Output template

```markdown
## RHDH routing result

**Status:** routed | completed | blocked
**Intent:** <overlay | plugin | local | Jira | repo navigation | environment>
**CLI:** `$RHDH`

### Environment
- `$RHDH`: pass | fail | skipped, <reason>
- `$RHDH doctor`: pass | fail | not needed
- `needs_setup`: true | false | unknown

### Route
| Area | Primitive or resource | Reason |
| --- | --- | --- |
| <area> | `<skill or reference>` | <why selected> |

### Activity tracking
- Log entry: <created or not needed>
- Todo: <created, updated, closed, or not needed>

### Next action
<concrete next step>
```

## Quality gate

- [ ] `RHDH="<skill-dir>/scripts/rhdh"` is established before CLI commands.
- [ ] `$RHDH` was run or skipped only for a conceptual question.
- [ ] `$RHDH doctor` was run when `needs_setup: true` or local dependencies matter.
- [ ] The route matches the user's intent and avoids relative links to other primitives.
- [ ] Required references were read before GitHub CLI patterns or repository navigation.
- [ ] Activity tracking is used for multi-session work and skipped for small one-step tasks.
- [ ] Mutating GitHub operations are preceded by read-only inspection and confirmation.
