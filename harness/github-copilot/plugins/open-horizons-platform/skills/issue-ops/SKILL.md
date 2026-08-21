---
name: issue-ops
description: 'Use when dispatching GitHub Issue slash commands through the IssueOps workflow, validating dispatcher mappings, or explaining /validate and /check-agents automation. Produces a command safety review, dispatcher execution plan, and GitHub issue comment output. DO NOT USE FOR: manual script execution (use validation-scripts), Backstage deployment (use open-horizons-backstage-deployment), full platform deployment (use deploy-orchestration). Triggers include "run /validate from an issue", "dispatch this slash command", "check the IssueOps mapping", and "why did /check-agents fail".'
---

# Issue Ops

Use this skill to operate the repository's IssueOps dispatcher, which maps slash commands in GitHub issue comments to approved automation through `.github/workflows/issue-ops.yml` and the bundled `dispatcher.py`. It produces a command review, a safe dispatch decision, and the expected issue comment result.

> [!NOTE]
> This skill depends on GitHub Actions, the `gh` CLI for inspection, repository write permissions for issue comments, and the bundled `dispatcher.py`. Resolve bundled paths relative to this `SKILL.md`; do not assume the skill was copied to `.github/skills/`.

## When to invoke

- "Run /validate on this deployment issue."
- "Explain why the IssueOps slash command failed."
- "Check whether /check-agents is safe to dispatch."
- "Validate the IssueOps workflow before we use it."
- "Show the output that the dispatcher will post back to the issue."

## Prerequisites and context

- `.github/workflows/issue-ops.yml` exists and listens for issue comments that start with `/`.
- Bundled `dispatcher.py` exists and contains the active `COMMAND_MAP`.
- The mapped script in `COMMAND_MAP` exists before dispatch; if it does not exist, the dispatcher must fail safely.
- `gh auth status` succeeds when inspecting issues or workflow runs.
- The target issue and repository are known.

## Procedure

### Step 1: Identify the requested command

1. Read only the first slash-command line from the issue body or comment.
2. Confirm it is one of the dispatcher-supported commands in bundled `dispatcher.py`.
3. Reject commands with shell chaining, command substitution, redirection, or unapproved flags.

```bash
ISSUE_OPS_SKILL="<directory containing this SKILL.md>"
ISSUE_BODY="/check-agents" python3 "$ISSUE_OPS_SKILL/dispatcher.py"
```

Run the dispatcher only through the workflow or with controlled `ISSUE_BODY` in a safe local check.

### Step 2: Verify workflow and script anchors

```bash
test -f .github/workflows/issue-ops.yml
test -f "$ISSUE_OPS_SKILL/dispatcher.py"
test -f "$ISSUE_OPS_SKILL/../validation-scripts/scripts/validate-deployment.sh"
test -f "$ISSUE_OPS_SKILL/../validation-scripts/scripts/validate-agents.py"
```

### Step 3: Classify command risk

| Risk | Meaning |
| --- | --- |
| High | Command can create, update, or comment on GitHub artifacts, or can trigger deployment validation against live infrastructure. |
| Medium | Command reads live workflow, cluster, or deployment state and posts summarized output. |
| Low | Local parser inspection or dry-run analysis with no GitHub or infrastructure side effects. |

### Step 4: User confirmation gate

```text
IssueOps command: <slash command>
Repository: <owner>/<repo>
Issue: #<number>
Mapped dispatcher: <issue-ops skill directory>/dispatcher.py
Risk: <High|Medium|Low>
Proceed with dispatching and posting the result to GitHub? (y/n)
```

> [!IMPORTANT]
> Only dispatch IssueOps commands or post GitHub comments after an explicit affirmative response. On a negative, ambiguous, or missing response, do not dispatch; output the planned command and stop.

### Step 5: Dispatch through GitHub Actions

Use the workflow path as the authoritative execution surface. Inspect workflow runs and logs with `gh`.

```bash
gh run list --workflow issue-ops.yml --limit 10
gh run view <run-id> --log-failed
```

### Step 6: Verify result comment and failures

1. Confirm the workflow posted a result comment to the issue.
2. If the dispatcher reports `Script not found`, treat the command as safely rejected.
3. If validation failed, hand off remediation to `validation-scripts`, `kubectl-cli`, or `pipeline-diagnostics` based on the failing command output.

## Limits

- Do not use this skill for: manual script execution (use validation-scripts), Backstage deployment (use open-horizons-backstage-deployment), full platform deployment (use deploy-orchestration).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Unknown slash command | Return the supported commands from `COMMAND_MAP`; do not execute anything. |
| Mapped script is missing | Report the missing path from dispatcher output and stop. |
| Arguments contain unsafe shell syntax | Reject the command and ask for plain flags or values. |
| GitHub authentication fails | Ask the operator to run `gh auth login` or configure workflow permissions. |
| Workflow run fails | Use `gh run view <run-id> --log-failed` and summarize the failing step. |

## Output template

Return exactly this structure:

```markdown
## IssueOps Dispatch Report

**Repository:** <owner>/<repo>
**Issue:** #<number>
**Command:** `<slash command>`
**Risk:** <High|Medium|Low>

### Dispatcher Mapping
- Dispatcher: `<issue-ops skill directory>/dispatcher.py`
- Workflow: `.github/workflows/issue-ops.yml`
- Mapped script exists: <yes|no>

### Execution Result
- Workflow run: <id or not run>
- Status: <success|failure|blocked>
- Posted comment: <yes|no>

### Findings
- <finding>
```

## Quality gate

- [ ] Confirmed the command is in bundled `dispatcher.py`.
- [ ] Verified mapped script existence before dispatch or documented safe rejection.
- [ ] Rejected unsafe shell syntax in arguments.
- [ ] Received explicit approval before dispatching or posting comments.
- [ ] Reviewed workflow logs for failed dispatches.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
