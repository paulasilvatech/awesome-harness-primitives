# Slack Notification Reference

Templates and routing for Slack pings when GitHub notifications aren't getting attention.

<rationale>
GitHub notifications have poor signal/noise ratio. Direct Slack pings are more effective for urgent items that need human attention.
</rationale>

## Message Template

```
Hey @{slack_handle}

PR #{number} ({plugin_name} {action}) needs your attention.

Status:
- Checks: {publish_status} Publish, {smoke_status} Smoke
- Reviews: {review_status}
- Stale: {days} days

Priority: {priority_reason}

{pr_url}

Could you take a look when you have a moment?
```

### Field Values

| Field | Source | Example |
|-------|--------|---------|
| `slack_handle` | Handle mapping (see below) | `@dfestal` |
| `number` | PR number | `1234` |
| `plugin_name` | Extract from PR title/branch | `lightspeed` |
| `action` | Label: `workspace-update` or `workspace-addition` | `update` |
| `publish_status` | Check rollup | `Pass` / `Fail` / `Pending` |
| `smoke_status` | Check rollup | `Pass` / `Fail` / `Pending` |
| `review_status` | Review state | `Approved` / `Awaiting review` / `Changes requested` |
| `days` | Days since `updatedAt` | `5` |
| `priority_reason` | From label classification | `Mandatory workspace - blocking next RHDH release` |

---

## Priority Reasons

| Priority | Reason Text |
|----------|-------------|
| Critical | `Mandatory workspace update - blocking RHDH release` |
| Medium | `Mandatory workspace addition - needed for RHDH catalog` |
| Low | `Community plugin - review when available` |

---

## Channel Routing

| Situation | Channel |
|-----------|---------|
| PR has individual assignee | DM to assignee |
| No assignee on critical PR | `#cope-team` |
| Plugin team PR (non-critical) | `#rhdh-plugins` |
| Release blocker | `#rhdh-release` |

---

## Handle Mapping

GitHub usernames don't always match Slack handles. Maintain a mapping:

```yaml
# Store in .rhdh/slack-handles.yaml or environment
handles:
  # github_username: slack_handle
  dfestal: dfestal
  mhild: mhild
  tkral: tkral
  # When handles differ:
  johndoe: john.doe

# Team fallbacks for unassigned PRs
teams:
  redhat-developer/rhdh-plugins: "#rhdh-plugins"
  redhat-developer/cope: "#cope-team"
```

### Lookup Order

1. Check `handles` mapping for exact GitHub username
2. Fall back to GitHub username as Slack handle (often matches)
3. For team reviewers without individual, use `teams` mapping

---

## Example Messages

### Critical - Mandatory Update (Stale)

```
Hey @dfestal

PR #1234 (lightspeed update) needs your attention.

Status:
- Checks: Pass Publish, Pass Smoke
- Reviews: Awaiting your review
- Stale: 5 days

Priority: Mandatory workspace update - blocking RHDH release

https://github.com/redhat-developer/rhdh-plugin-export-overlays/pull/1234

Could you take a look when you have a moment?
```

### Medium - New Plugin Needs Config

```
Hey @contributor

PR #1235 (new-plugin addition) needs some updates.

Status:
- Checks: Fail Smoke (missing config)
- Reviews: Approved, but can't merge

Priority: Add plugin configuration to enable smoke tests
See: https://github.com/.../README.md#smoke-test-config

https://github.com/redhat-developer/rhdh-plugin-export-overlays/pull/1235
```

### Unassigned Critical - Channel Ping

```
#cope-team

Unassigned critical PR needs an owner:

PR #1236 (aws-appsync update) - mandatory workspace, 3 days stale

Checks: Pass Publish, Pending Smoke
No assignee or individual reviewer

https://github.com/redhat-developer/rhdh-plugin-export-overlays/pull/1236

Can someone pick this up?
```

---

## Anti-Spam Guidelines

- **Don't ping more than once per PR** unless status changes significantly
- **Wait 2 business days** after initial ping before follow-up
- **Batch pings** - send multiple in one session rather than throughout the day
- **Track pings** in worklog to avoid duplicates:

  ```bash
  $RHDH log add "Pinged @dfestal on PR #1234" --tag slack --tag pr-1234
  ```
