---
name: github-issue-ops
description: >-
  Dispatches authorized GitHub issue-comment commands to read-only repository
  validation. Use when implementing or validating /check-agents, /help, issue
  comment authorization, command parsing, or IssueOps workflow behavior.
---

# GitHub Issue Ops Dispatcher

Dispatch a deliberately small, read-only command set from GitHub issue comments.
The workflow has no cloud identity, secrets, cluster context, or mutation path
other than posting its result to the originating issue.

## When to invoke

- Add or validate an IssueOps command.
- Review IssueOps authorization, parsing, status propagation, or workflow routing.
- Diagnose `/check-agents` or `/help` behavior in issue comments.

## Procedure

### Authorization boundary

The workflow handles only newly created `issue_comment` events. A job starts only
when all of these conditions are true:

1. The comment belongs to an issue, not a pull request.
2. The comment begins with `/`.
3. GitHub reports the comment author association as `OWNER`, `MEMBER`, or
   `COLLABORATOR`.

Unauthorized comments do not start a job. The job has only `contents: read` and
`issues: write`; it has no OIDC token permission, Azure login, Azure secrets, or
cloud mutation capability.

### Supported commands

| Command | Behavior |
| --- | --- |
| `/check-agents` | Runs `validate-agents.py --strict` with Python 3.11 after installing exactly `PyYAML==6.0.3`. |
| `/help` | Returns the supported commands and authorization boundary without running a subprocess. |

Commands take no arguments and must begin the first line. `/onboard` and
`/validate` return a failed, explanatory result: onboarding requires an approved
deployment workflow, and deployment validation requires an authenticated cluster
context. Other commands also fail with help.

### Dispatch behavior

1. Read the comment from `ISSUE_COMMENT`.
2. Parse the first line with `shlex.split` and validate the command name.
3. Reject arguments, unsupported commands, malformed quoting, and oversized input.
4. For `/check-agents`, execute a fixed argument list with `shell=False` semantics,
   a repository-root working directory, and a five-minute timeout.
5. Post the Markdown result, then make the workflow job return the dispatcher's
   exit status.

## Output template

```markdown
## IssueOps command result

**Command:** </check-agents | /help | unsupported command>
**Status:** <PASS | FAIL>
**Exit code:** <process exit code>

<summary and safely rendered command output>
```

## Limits

- This control plane performs no onboarding, deployment, cluster validation, or
  cloud authentication.
- Pull-request comments, issue bodies, issue-opened events, unauthorized actors,
  leading whitespace before `/`, and commands after the first line do not run.
- Use `validation-scripts` (`skill`) for direct validation and
  `deploy-orchestration` (`skill`) for approved platform changes.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `validation-scripts` | `skill` | Running repository validators directly. |
| `deploy-orchestration` | `skill` | Coordinating approved deployment actions. |
| `github-cli` | `skill` | Performing general GitHub issue operations. |

## Quality gate

- [ ] The event and job guard exclude issue bodies and pull-request comments.
- [ ] Only owners, members, and collaborators can start the job.
- [ ] Permissions remain `contents: read` and `issues: write` with no OIDC.
- [ ] Every action is SHA-pinned and PyYAML is exactly version-pinned.
- [ ] Only `/check-agents` and `/help` can succeed.
- [ ] Parsing tests cover supported, unsupported, malformed, and injected input.
- [ ] Dispatcher and workflow preserve a nonzero command status after commenting.
