# Sprint Report

Generate a sprint review summary: committed vs completed, per-member breakdown, epic progress, demo checklist with naming conventions, and velocity trend. Run at the end of each sprint before the review/demo meeting.

Uses GraphQL for bulk reads (skip acli). Writes follow the API preference order in SKILL.md.

Authentication setup: see `references/auth.md`. All examples below assume `AUTH`, `CLOUD_ID`, and `GRAPHQL_URL` are set per that file.

## Input

The caller provides:

1. **Team ID** - Jira team UUID. If not provided, ask.
2. **Sprint** - defaults to active sprint. Accept `previous` for last closed sprint, or a sprint name/ID.
3. **Board ID** - optional. If not provided, discover or ask.

## Workflow

### Step 1 - Resolve Sprint

Find the target sprint:

```bash
# Active sprint (default)
acli jira board list-sprints --board BOARD_ID --state active --json

# Previous sprint
acli jira board list-sprints --board BOARD_ID --state closed --json --recent 1
```

Extract: sprint ID, name, start date, end date.

### Step 2 - Fetch All Sprint Issues

Get every issue that was in the sprint:

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-ExperimentalApi: JiraIssueSearch' \
  -d '{
    "query": "query SprintIssues { jira { issueSearchStable(cloudId: \"'"$CLOUD_ID"'\", issueSearchInput: {jql: \"project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS) AND sprint = SPRINT_ID AND \\\"Team[Team]\\\" = TEAM_ID\"}, first: 100) { totalCount edges { node { key summary status { name } issueType { name } priority { name } assignee { name accountId } storyPoints parentIssue { key summary } fields { edges { node { __typename name ... on JiraLabelsField { labels { edges { node { name } } } } ... on JiraSprintField { selectedSprintsConnection { edges { node { name state startDate } } } } } } } } } } } }"
  }'
```

### Step 3 - Partition Issues

Split into categories:

| Category | Condition |
|----------|-----------|
| **Completed** | Status is Closed or Release Pending |
| **Carried over** | Status is anything else (In Progress, To Do, Review, etc.) |
| **Added mid-sprint** | Issue's sprint start date is after the sprint's start date (scope creep) |

### Step 4 - Committed vs Completed

| Metric | Computation |
|--------|-------------|
| Committed SP | Sum SP of all sprint issues (completed + carried) |
| Completed SP | Sum SP of completed issues only |
| Completion rate | `completed_sp / committed_sp × 100` |
| Scope creep | Count and SP of mid-sprint additions |

Flag if completion rate < 70%: "⚠ Below 70% completion - review sprint commitments."
Note if > 100%: "Team completed more than committed - pulled in extra work."

### Step 5 - Per-Member Breakdown

Group issues by assignee. For each team member:

- Issues closed (count)
- SP completed
- Issues carried over (count)
- SP carried over

Highlight: top contributor (most SP completed), anyone with 0 completions (may be blocked, on PTO, or doing non-Jira work - don't assume negatively).

### Step 6 - Epic Progress

Group completed work by parent Epic (`parentIssue`). For each Epic with at least one completed child:

1. Count total children (query: `parent = {epic_key}` - include ALL statuses for the denominator)
2. Count closed children (filter to `status in (Closed, "Release Pending")`)
3. Compute: "X/Y stories closed this sprint ({before}% → {after}% complete)"

### Step 7 - Demo Checklist

Find issues with `demo` label. For each:

1. Check if the parent Feature (in RHDHPLAN) has a Feature Demo link set
2. Generate the expected naming conventions:
   - **Demo file:** `${SPRINT_NUMBER} ${JIRA_Project}-${JIRA_NUMBER} ${DEMO_TITLE}`
   - **Slide:** `${SPRINT_NUMBER} ${Team name} Review`
3. Suggest demo venue:
   - **Sprint Review** - customer-facing features
   - **Team Forum** - team-related demos
   - **Architecture Call** - deep technical topics

Flag missing demo links: "❌ Demo required but no Feature Demo link set on parent Feature."

### Step 8 - Velocity Trend

Fetch last 3 closed sprints. For each, sum SP of Closed/Release Pending issues (same query pattern as plan.md Step 3 - duplicated here to avoid transitive loading):

```bash
acli jira board list-sprints --board BOARD_ID --state closed --json --recent 3
```

Then for each closed sprint:

```bash
jql: "project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS)
  AND sprint = SPRINT_ID
  AND status in (Closed, \"Release Pending\")
  AND \"Team[Team]\" = TEAM_ID"
```

Compute this sprint's velocity vs 3-sprint average. Show trend (↑ accelerating / → stable / ↓ decelerating).

### Step 9 - Save Report

Offer to save the report as a markdown file:

> "Save report as markdown? [y/N]"

If yes, save to `sprint-report-{team}-{sprint}-{YYYY-MM-DD}.md` in the current working directory. Accept a custom path if the user provides one.

## Output

### Data Contract

```json
{
  "team": "RHDH Cope",
  "sprint": "Sprint 47",
  "period": "May 7–20, 2026",
  "committed": {"count": 14, "sp": 21},
  "completed": {"count": 11, "sp": 18},
  "carried_over": {"count": 3, "sp": 5},
  "scope_creep": {"count": 2, "sp": 4},
  "completion_rate": 86,
  "per_member": [
    {"name": "Allison Hill", "closed": 4, "sp_done": 8, "carried": 1, "sp_carry": 3}
  ],
  "epic_progress": [
    {"key": "RHIDP-100", "summary": "Dynamic plugins v2", "closed_this_sprint": 3, "total": 8, "pct_before": 37, "pct_after": 75}
  ],
  "demos": [
    {"key": "RHIDP-1234", "summary": "...", "demo_link_set": true, "file_name": "3247 RHIDP-1234 Demo title", "venue": "Sprint Review"}
  ],
  "velocity": {
    "this_sprint": 18,
    "average": 18,
    "trend": "stable"
  }
}
```

### Markdown Template

```markdown
## Sprint Report - {team} {sprint}

Period: {start} – {end}

### Summary
| Metric | Value |
|--------|-------|
| Committed | {committed_sp} SP ({committed_count} items) |
| Completed | {completed_sp} SP ({completed_count} items) |
| Carried over | {carried_sp} SP ({carried_count} items) |
| Added mid-sprint | {scope_count} items ({scope_sp} SP) |
| Completion rate | {rate}% {icon} |

### Per-Member
| Member | Closed | SP Done | Carried | SP Carry |
|--------|--------|---------|---------|----------|

### Epic Progress
| Epic | Summary | This Sprint | Overall |
|------|---------|-------------|---------|

### Demo Items
| # | Issue | Summary | Demo Link | File Name | Venue |
|---|-------|---------|-----------|-----------|-------|

**Slide name:** `{sprint_number} {team} Review`

### Velocity Trend
| Sprint | SP | vs Avg |
|--------|----|--------|
{sprint}: {sp} SP | 3-sprint avg: {avg} SP | Trend: {trend}
```

## Error Handling

| Error | Action |
|-------|--------|
| No active/closed sprint found | "No sprint found for this board. Check board ID." |
| Sprint has 0 issues | "Empty sprint. Was work tracked elsewhere?" |
| Parent Epic query fails | Skip epic progress for that issue. Note "parent unavailable." |
| Demo label but no parent Feature | Note "Demo item has no parent Feature - cannot check demo link." |
| File save fails | Warn. Report was already displayed in terminal. |

## Caveats

1. **Scope creep detection is approximate.** It checks if the issue's sprint assignment date is after the sprint start. Issues moved between sprints may show false positives.
2. **Per-member breakdown only shows Jira-tracked work.** Code reviews, documentation, support, and meetings don't appear. Note this in the report.
3. **Demo venue routing is a suggestion.** Based on the issue type and labels, not a hard rule.
4. **Release Pending counts as completed.** Per team convention, Release Pending items remain in sprint and are counted as "done" for velocity.
