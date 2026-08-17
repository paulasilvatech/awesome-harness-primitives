---
name: rhdh
description: "Primary Red Hat Developer Hub (RHDH) skill for plugin development, overlay management, local testing, Jira work, repo navigation, version compatibility, CI debugging, and environment setup. Use for RHDH, Red Hat Developer Hub, Developer Hub, dynamic plugins, overlays, rhdh-local, RHDH Jira, plugin catalog, RHDH repositories, or RHDH CI/CD tasks."
---

# RHDH

Use this as the entry point for Red Hat Developer Hub work. It routes to specialized RHDH skills and provides the shared CLI, repository map, and activity tracking model.

## First Step

1. Resolve the skill directory from this `SKILL.md` file.
2. Set the CLI variable to the local script:

   ```bash
   RHDH="<skill-dir>/scripts/rhdh"
   ```

3. Run `$RHDH` to check the environment unless the user is only asking a conceptual question.
4. If the output reports `needs_setup: true`, run `$RHDH doctor` before repository or plugin operations.

Ask only when required information is missing. If intent is clear, proceed with the matching route.

## Operating Principles

- Track meaningful milestones with `$RHDH log add` and blockers with `$RHDH todo` when work spans sessions.
- Before using GitHub CLI patterns for RHDH repositories, read [references/github-reference.md](references/github-reference.md).
- Before navigating RHDH repositories, read [references/rhdh-repos.md](references/rhdh-repos.md).
- Use `$RHDH config init` or `$RHDH config set <key> <path>` when local repository paths are missing.
- Do not guess repository relationships, versions, PR commands, or publish checks. Verify them through references or CLI output.

## Routing

| User intent | Action |
| --- | --- |
| Onboard, update, fix, triage, analyze PRs, publish, overlay workspace | Load the `overlay` skill. If unavailable, read `../overlay/SKILL.md`. |
| Create backend plugin, frontend plugin, export, OCI packaging, tgz, dynamic plugin wiring, mount points, routes, entity tabs | Load the `create-plugin` skill. If unavailable, read `../create-plugin/SKILL.md`. |
| Enable, disable, test, start, stop, health-check, backup, restore, or troubleshoot local RHDH | Load the `rhdh-local` skill. If unavailable, read `../rhdh-local/SKILL.md`. |
| Jira issue creation, assignment, refinement, sprint planning, release status, RHIDP, RHDHPLAN, RHDHBUGS, RHDHSUPP | Load the `rhdh-jira` skill. If unavailable, read `../rhdh-jira/SKILL.md`. |
| Environment check, repo path setup, activity review | Use the CLI commands below. |

## CLI Commands

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

## Activity Tracking

Use activity tracking when the work spans sessions or external follow-up:

```bash
$RHDH log add "Started onboarding plugin-name" --tag onboard --tag plugin-name
$RHDH todo add "Follow up on PR #123" --tag pr --tag blocked
$RHDH todo note <slug> "Waiting for CI rerun"
$RHDH todo done <slug>
```

Tracking is recommended, not mandatory. Do not let tracking block small one-step tasks.

## References

| File | Use when |
| --- | --- |
| [references/rhdh-repos.md](references/rhdh-repos.md) | Understanding RHDH repositories and where work belongs. |
| [references/github-reference.md](references/github-reference.md) | Running GitHub CLI commands for PRs, CI, labels, comments, and publish triggers. |
| [references/versions.md](references/versions.md) | Checking RHDH and Backstage version compatibility. |
| [references/slack-notification.md](references/slack-notification.md) | Drafting Slack notifications for RHDH work. |

## Validation

- Run `$RHDH doctor` before operations that depend on local repositories, GitHub CLI, container runtime, or rhdh-local.
- For code or script changes in this skill, run Python compile checks for changed scripts.
- For GitHub CLI operations, prefer read-only commands first and confirm before mutating PRs, labels, comments, or assignments.