# Reference: GitHub CLI for Overlay Repository

Working with PRs and repository content using `gh` CLI.

**Repo shorthand:** `REPO="redhat-developer/rhdh-plugin-export-overlays"`

---

## Essential Patterns

### Always use `--json` + `--jq` for scripting

More stable than parsing text output:

```bash
# Stable - JSON output
gh pr list --json number,title --jq '.[] | "\(.number): \(.title)"'

# Fragile - text parsing
gh pr list | awk '{print $1, $2}'
```

### Always include `--limit` for large result sets

```bash
# Good - bounded result
gh pr list --repo $REPO --state open --limit 100

# Risky - unbounded (could be thousands)
gh pr list --repo $REPO --state all
```

### Avoid `!=` in jq expressions

Bash interprets `!` as history expansion:

```bash
# BROKEN - bash expands != as history reference
gh pr view 1 --jq '.reviews | map(select(.state != "COMMENTED"))'

# WORKS - use "not" pattern instead
gh pr view 1 --jq '.reviews | map(select(.state == "COMMENTED" | not))'
```

---

## PR Listing

### All Open PRs

```bash
gh pr list --repo $REPO --state open --limit 100 \
  --json number,title,labels,assignees,updatedAt,author
```

### Filter by Label

```bash
# Single label
gh pr list --repo $REPO --label mandatory-workspace

# Multiple labels (AND)
gh pr list --repo $REPO --label mandatory-workspace --label workspace-update

# Search for label (OR) - use search syntax
gh pr list --repo $REPO --search "label:mandatory-workspace label:workspace-update"
```

### Filter by Author

```bash
gh pr list --repo $REPO --author github-actions[bot]
```

---

## PR Details

### Full Context

```bash
gh pr view <number> --repo $REPO \
  --json number,title,state,author,labels,assignees,reviewRequests,reviews,statusCheckRollup,files,updatedAt,createdAt,mergeable,body
```

### Just Labels

```bash
gh pr view <number> --repo $REPO --json labels --jq '.labels[].name'
```

### Just Assignees

```bash
gh pr view <number> --repo $REPO --json assignees --jq '.assignees[].login'
```

### Check Status

```bash
gh pr view <number> --repo $REPO --json statusCheckRollup \
  --jq '.statusCheckRollup[] | "\(.name): \(.status) \(.conclusion)"'
```

### Specific Check (e.g., publish)

```bash
gh pr view <number> --repo $REPO --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.name | contains("publish"))'
```

### Files Changed

```bash
gh pr view <number> --repo $REPO --json files --jq '.files[].path'
```

### Extract Workspace Name

```bash
gh pr view <number> --repo $REPO --json files \
  --jq '.files[].path | select(startswith("workspaces/")) | split("/")[1]' | sort -u
```

---

## PR Actions

### Comment

```bash
gh pr comment <number> --repo $REPO --body "/publish"
```

### Add/Remove Label

```bash
gh pr edit <number> --repo $REPO --add-label "needs-review"
gh pr edit <number> --repo $REPO --remove-label "needs-review"
```

### Add Assignee / Request Review

```bash
gh pr edit <number> --repo $REPO --add-assignee username
gh pr edit <number> --repo $REPO --add-reviewer username
```

---

## Repository Content

### Get File Content

```bash
gh api repos/$REPO/contents/<path> --jq '.content' | base64 -d
```

### Get CODEOWNERS

```bash
gh api repos/$REPO/contents/CODEOWNERS --jq '.content' | base64 -d
```

### Get versions.json

```bash
gh api repos/$REPO/contents/versions.json --jq '.content' | base64 -d | jq '.'
```

### Get File from PR Branch

```bash
# First get the branch name
BRANCH=$(gh pr view <number> --repo $REPO --json headRefName --jq '.headRefName')

# Then get file from that branch
gh api repos/$REPO/contents/<path>?ref=$BRANCH --jq '.content' | base64 -d
```

---

## CI & Workflow Runs

### PR Status Can Be Stale

`gh pr checks` and `statusCheckRollup` can be stale. Always verify with run list:

```bash
# Get the branch name first
BRANCH=$(gh pr view <number> --repo $REPO --json headRefName --jq '.headRefName')

# Check latest run (not PR status)
gh run list --repo $REPO --branch $BRANCH --limit 3 --json databaseId,conclusion,status
```

### Get Failed Logs

```bash
# Get run ID from branch
gh run list --repo $REPO --branch <branch> --limit 3 --json databaseId,conclusion,status

# View failed logs only
gh run view <run-id> --repo $REPO --log-failed

# Filter for errors (large logs)
gh run view <run-id> --repo $REPO --log-failed 2>&1 | grep -A 5 "Error\|FAIL" | head -50
```

### Common Overlay Repo Failures

| Error Pattern | Likely Cause | Fix |
|--------------|--------------|-----|
| `source.json: backstage version mismatch` | `repo-backstage-version` doesn't match upstream | Update to actual upstream version |
| `CODEOWNERS: no entry for workspace` | Missing CODEOWNERS entry | Add entry for new workspace |
| `plugins-list.yaml: invalid format` | YAML syntax error | Validate YAML structure |
| `smoke test failed` | Plugin doesn't load | Check backstage.json overrides |

---

## Overlay Repo Specifics

### `/publish` Comment Trigger

The overlay repo uses a workflow triggered by `/publish` comment:

```bash
# Trigger publish
gh pr comment <number> --repo $REPO --body "/publish"

# Check if already triggered
gh pr view <number> --repo $REPO --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.name | contains("publish"))'
```

**Guards before triggering:**

1. PR is open (not closed/merged)
2. No `do-not-merge` label
3. Publish check not already successful

### Bot PRs Need Manual `/publish`

Bot PRs (e.g., `github-actions[bot]`) can't auto-trigger workflows due to GitHub security restrictions.

```bash
# Find bot PRs needing publish
gh pr list --repo $REPO --author "github-actions[bot]" --json number,title,statusCheckRollup \
  --jq '.[] | select(.statusCheckRollup | map(.name) | index("publish") == null)'
```

---

## Batch Operations

### Get Multiple PRs

```bash
# Get numbers first
NUMBERS=$(gh pr list --repo $REPO --label mandatory-workspace --json number --jq '.[].number')

# Then iterate
for num in $NUMBERS; do
  gh pr view $num --repo $REPO --json title,assignees
done
```

### Trigger Publish on Multiple PRs

```bash
for num in 1234 1235 1236; do
  gh pr comment $num --repo $REPO --body "/publish"
  sleep 2  # Rate limiting
done
```

### Check Rate Limit

```bash
gh api rate_limit --jq '.rate | "Remaining: \(.remaining)/\(.limit)"'
```

---

## jq Patterns

### Filter by Conclusion

```bash
gh pr view <number> --repo $REPO --json statusCheckRollup \
  --jq '[.statusCheckRollup[] | select(.conclusion == "success")] | length'
```

### Check if Label Exists

```bash
gh pr view <number> --repo $REPO --json labels \
  --jq '.labels | map(.name) | index("do-not-merge") != null'
```

### Days Since Update

```bash
gh pr view <number> --repo $REPO --json updatedAt \
  --jq '((now - (.updatedAt | fromdateiso8601)) / 86400 | floor)'
```

---

## Action Confirmation Tiers

### Auto-execute (no confirmation needed)

- Post `/publish` comment
- Add labels
- Request review
- Post informational comments

### Require confirmation

- `merge` - irreversible
- `approve` - official approval
- `close` - closes PR/issue
- Remove labels (could affect automation)

---

## Review Decision Guide

### Approve if

- All CI checks pass
- No security issues
- Follows existing patterns
- CODEOWNERS entry present (for additions)

### Request Changes if

- Missing CODEOWNERS for new workspace
- Compatibility bypass detected (manual source.json edit)
- CI failures unresolved
- Missing required fields in config

### Close & Refine if

- Plugin fundamentally incompatible
- Duplicate of existing workspace
- Owner unresponsive (>30 days stale after pings)
