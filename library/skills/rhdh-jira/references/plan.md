# Sprint Planning Prep

Generate a sprint planning package: carryover report, velocity trend, per-member capacity, ready-for-planning queue, and sprint fill suggestions. Run before each bi-weekly sprint planning call.

Uses GraphQL for bulk reads (skip acli). Writes follow the API preference order in SKILL.md.

Authentication setup: see `references/auth.md`. All examples below assume `AUTH`, `CLOUD_ID`, and `GRAPHQL_URL` are set per that file.

## Input

The caller provides:

1. **Team ID** - Jira team UUID. If not provided, ask the user.
2. **Board ID** - optional. If not provided, discover from `references/jql-patterns.md` board table or ask.
3. **Sprint** - optional. Defaults to "plan the next sprint" (uses active sprint for carryover, next sprint as target).

## Workflow

### Step 1 - Resolve Sprint Context

Find the team's board and identify sprints. Use acli for sprint lookup (simple, single call):

```bash
acli jira board list-sprints --board BOARD_ID --state active --json
acli jira board list-sprints --board BOARD_ID --state closed --json --recent 3
acli jira board list-sprints --board BOARD_ID --state future --json --recent 1
```

Identify:

- **Active sprint** (ending soon) - source for carryover
- **Next sprint** (future) - target for planning
- **Last 3 closed sprints** - source for velocity

### Step 2 - Carryover Report

Issues in the active sprint that are NOT Closed or Release Pending. These carry into the next sprint.

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-ExperimentalApi: JiraIssueSearch' \
  -d '{
    "query": "query Carryover { jira { issueSearchStable(cloudId: \"'"$CLOUD_ID"'\", issueSearchInput: {jql: \"project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS) AND sprint = SPRINT_ID AND status not in (Closed, \\\"Release Pending\\\") AND \\\"Team[Team]\\\" = TEAM_ID\"}, first: 50) { totalCount edges { node { key summary status { name } assignee { name } storyPoints issueType { name } } } } } }"
  }'
```

**Validation:** Flag any Epics in the sprint - only Bug, Task, or Story should be in sprints. "⚠ RHIDP-1234 is an Epic - Epics should be broken down into Stories/Tasks, not added to sprints."

Sum carryover SP. If carryover > avg velocity, flag: "Carryover ({N} SP) exceeds avg velocity ({M} SP) - sprint is overcommitted before adding new work."

### Step 3 - Velocity Calculation

For each of the last 3 closed sprints, count completed SP:

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-ExperimentalApi: JiraIssueSearch' \
  -d '{
    "query": "query Velocity { jira { issueSearchStable(cloudId: \"'"$CLOUD_ID"'\", issueSearchInput: {jql: \"project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS) AND sprint = SPRINT_ID AND status in (Closed, \\\"Release Pending\\\") AND \\\"Team[Team]\\\" = TEAM_ID\"}, first: 100) { totalCount edges { node { storyPoints } } } } }"
  }'
```

Compute: SP per sprint, 3-sprint average, trend (↑ accelerating / → stable / ↓ decelerating).

### Step 4 - Per-Member Capacity

Reuse the capacity query from `references/assign.md` Layer 3. For each team member (roster from `assign.md` Layer 1):

- Open issues in active sprint (carryover per person)
- SP committed in active sprint
- Issues in next sprint (already planned)
- Overloaded flag (≥10 open issues or ≥21 SP)

### Step 5 - Ready-for-Planning Queue

Backlog issues that are refined and ready to pull into the sprint:

```bash
jql: "project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS)
  AND \"Team[Team]\" = TEAM_ID
  AND status in (Backlog, \"To Do\")
  AND sprint not in (openSprints(), futureSprints())
  AND (cf[10028] is not EMPTY OR issuetype = Bug)
  AND issuetype in (Bug, Task, Story)
  ORDER BY priority ASC, created ASC"
```

Rank by priority, then by parent epic priority. Include: key, summary, priority, SP, parent epic key, assignee (if set).

### Step 6 - Available Capacity

```
available_SP = avg_velocity - carryover_SP
```

If negative, warn: "No room for new work - carryover alone exceeds velocity."

### Step 7 - Sprint Fill Suggestions

Automatically generate issue-to-person recommendations from the ready queue. Uses expertise matching from `references/assign.md` Layer 2 (if not already fetched, run it now).

For each ready-for-planning issue, score against each team member using the same formula from `assign.md` (expertise × 3 + proximity × 2 - capacity × 1). Suggest assignments up to `available_SP`.

**Framing:** "These are suggestions - team members self-select during planning."

### Step 8 - Critical Customer Bugs

Separately surface any critical/blocker bugs with `rhdh-customer` label:

```bash
jql: "project in (RHIDP, RHDHBUGS) AND priority in (Blocker, Critical) AND labels = rhdh-customer AND \"Team[Team]\" = TEAM_ID AND status != Closed"
```

Note: "Critical customer bugs are exempt from capacity constraints - work immediately regardless of sprint load."

### Step 9 - Continuous Improvement Items

Surface open issues with `Component: Continuous Improvement` (retro action items):

```bash
jql: "project = RHIDP AND component = 'Continuous Improvement' AND \"Team[Team]\" = TEAM_ID AND status != Closed ORDER BY priority ASC"
```

Note: "Retro action items to consider for this sprint."

## Output

### Data Contract

```json
{
  "team": "RHDH Cope",
  "active_sprint": "Sprint 47",
  "target_sprint": "Sprint 48",
  "carryover": {
    "count": 5,
    "sp": 13,
    "items": [{"key": "...", "summary": "...", "assignee": "...", "status": "...", "sp": 5}],
    "epic_violations": ["RHIDP-1234"]
  },
  "velocity": {
    "sprints": [{"name": "Sprint 46", "sp": 21}, {"name": "Sprint 45", "sp": 18}],
    "average": 18,
    "trend": "accelerating"
  },
  "capacity": [
    {"name": "Allison Hill", "carryover_items": 2, "carryover_sp": 8, "open": 5, "sp_load": 13, "overloaded": false}
  ],
  "available_sp": 5,
  "ready_queue": [
    {"key": "...", "summary": "...", "priority": "Critical", "sp": 3, "parent_epic": "RHIDP-100"}
  ],
  "fill_suggestions": [
    {"key": "RHIDP-5678", "proposed_assignee": "Noah Rhodes", "score": 12, "rationale": "..."}
  ],
  "critical_customer_bugs": [],
  "ci_items": []
}
```

### Markdown Template

```markdown
## Sprint Planning - {team}

{active_sprint} → Planning {target_sprint}

### Carryover ({count} items, {sp} SP)
| # | Issue | Summary | Assignee | Status | SP | Days |
|---|-------|---------|----------|--------|----|------|

⚠ Carryover ({sp} SP) vs avg velocity ({avg} SP): {assessment}

### Velocity (last 3 sprints)
| Sprint | Completed SP | Trend |
|--------|-------------|-------|
Avg: {avg} SP | Trend: {trend}

### Capacity
| Member | Carryover | Open | SP Load | Status |
|--------|-----------|------|---------|--------|

### Available Capacity
Avg velocity: {avg} SP − Carryover: {carry_sp} SP = **{available} SP available**

### Ready for Planning ({count} items, {total_sp} SP in queue)
| # | Issue | P | Summary | SP | Parent Epic |
|---|-------|---|---------|----|----||

### Sprint Fill Suggestions
| # | Issue | Summary | Suggested Assignee | Score | Rationale |
|---|-------|---------|-------------------|-------|-----------|

*Suggestions are recommendations - team members self-select during planning.*

### 🚨 Critical Customer Bugs (exempt from capacity)
| Issue | Summary | Priority | Assignee |

### 🔧 Retro Action Items (Continuous Improvement)
| Issue | Summary | Status |
```

## Error Handling

| Error | Action |
|-------|--------|
| Board ID not found | Ask user. List available boards via `acli jira board list`. |
| No active sprint | "No active sprint found. Is the team between sprints?" |
| No closed sprints (new team) | Skip velocity. Note: "No historical data - velocity unavailable." |
| `issueSearchStable` fails | Fall back to REST `/rest/api/3/search`. |
| Carryover query returns 0 | "Clean sprint - no carryover. Full velocity available." |

## Caveats

1. **Velocity is SP-based.** Teams with inconsistent SP estimation will see noisy trends. Fall back to issue count if SP coverage < 50%.
2. **Sprint fill suggestions reuse assign.md scoring.** If expertise profiles aren't cached, this step adds ~5-10 API calls.
3. **Bug SP exemption.** The doc says "every item needs story points or needs to be time-boxed." Bugs in the ready queue without SP are still shown but flagged.
4. **Release Pending items stay in sprint.** Per team convention, Release Pending items remain in the sprint and count toward capacity.
