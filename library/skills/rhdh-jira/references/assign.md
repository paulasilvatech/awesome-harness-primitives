# Assignee Recommendations

Analyze team expertise, sprint capacity, and context proximity to recommend assignees for unassigned issues. Supports single issues, batch JQL queries, or a passed-in list of issue keys.

Uses GraphQL for all reads (bulk operation). Writes follow the API preference order in SKILL.md - REST preferred here since deep mode already has `AUTH` set from GraphQL reads.

Authentication setup: see `references/auth.md`. All examples below assume `AUTH`, `CLOUD_ID`, and `GRAPHQL_URL` are set per that file.

## Input

The caller provides:

1. **Issue keys** - one or more unassigned issue keys (or a JQL query that produces them)
2. **Team ID** - Jira team UUID (e.g., `ec74d716-af36-4b3c-950f-f79213d08f71-4403`). If not provided, infer from the issue's `customfield_10001` field or the parent epic's team. If neither is available, ask the user.

## Mode Selection

> "Unassigned issues found. **Deep** recommendations (team roster + expertise + capacity + context analysis, ~5-10 API calls) or **quick** (match from data already in context)? [deep/quick]"

Default to **deep** if the user doesn't specify.

## Quick Mode

Match from data already in context - no extra API calls.

1. Collect assignees visible in the current context (report data, search results, etc.) and note their components/domains.
2. Match unassigned issues by component and keyword overlap.
3. If no match, state "insufficient data for recommendation - use deep mode."
4. If multiple matches, prefer the person with fewer open issues in context.
5. Include short rationale.

Skip the rest of this file. Format output per the Output section below.

## Deep Mode

Five analysis layers, executed in order.

### Layer 1 - Team Roster

Query the team directly via the Teams GraphQL API. No need to infer roster from issue assignees.

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST -H 'Content-Type: application/json' \
  -d '{
    "query": "query GetTeamRoster { team { teamV2(id: \"TEAM_ID\", siteId: \"'"$CLOUD_ID"'\") { displayName members(first: 50) { nodes { member { name accountId } state role } } } } }"
  }'
```

Replace `TEAM_ID` with the team UUID.

Extract distinct members: `name`, `accountId`. Filter to `state: FULL_MEMBER` only - exclude alumni and invited members.

If the team has more than 50 members, paginate using `after` cursor. In practice, RHDH teams are <15 people.

### Layer 2 - Expertise Profiles

For each team member, query their recent issue history to build a domain profile.

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-ExperimentalApi: JiraIssueSearch' \
  -d '{
    "query": "query ExpertiseProfile { jira { issueSearchStable(cloudId: \"'"$CLOUD_ID"'\", issueSearchInput: {jql: \"project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS) AND assignee = ACCOUNT_ID AND updated >= -90d ORDER BY updated DESC\"}, first: 50) { edges { node { key summary status { name } issueType { name } fields { edges { node { __typename name ... on JiraComponentsField { components { edges { node { name } } } } } } } } } } } }"
  }'
```

Replace `ACCOUNT_ID` with the member's `accountId`.

Build profile per member:

| Metric | How to compute |
|--------|---------------|
| **Components** | Rank by frequency across all 50 issues. Top 3 are primary domains. |
| **Issue types** | Count by type (Story, Task, Epic, Bug). Shows work pattern. |
| **Domain keywords** | Extract 2-3 word patterns from summaries (e.g., "catalog", "dynamic plugins", "RBAC", "CI/CD"). Rank by frequency. |
| **Specialization %** | `(issues in top component / total issues) × 100`. High (>60%) = specialist. Low (<30%) = generalist. |

### Layer 3 - Sprint Capacity

For each team member, query their current sprint load.

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-ExperimentalApi: JiraIssueSearch' \
  -d '{
    "query": "query SprintCapacity { jira { issueSearchStable(cloudId: \"'"$CLOUD_ID"'\", issueSearchInput: {jql: \"project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS) AND assignee = ACCOUNT_ID AND sprint in (openSprints(), futureSprints()) AND status != Closed\"}, first: 50) { totalCount edges { node { key summary status { name } storyPoints fields { edges { node { __typename name ... on JiraSprintField { selectedSprintsConnection { edges { node { name state } } } } } } } } } } } }"
  }'
```

Compute per member:

| Metric | How to compute |
|--------|---------------|
| **Open issues (current sprint)** | Count issues where sprint state = `active` |
| **Total SP committed** | Sum `storyPoints` across active sprint issues |
| **Next sprint load** | Count issues where sprint state = `future` |
| **Overloaded flag** | Set if open issues ≥ 10 or SP committed ≥ 21 |

### Layer 4 - Soft Signals

Derive from Layers 2 and 3 data. No additional API calls.

| Signal | Condition | Output |
|--------|-----------|--------|
| **Growth opportunity** | For Major or lower priority issues: member has ≤ 2 issues in the matching component/domain | "Growth opportunity for {name} - {N} prior issues in this area." |
| **Bus factor** | One member owns >60% of a component's issues across the team | "Consider spreading {component} knowledge - {name} owns {pct}%." |
| **Concentration warning** | Same member recommended for 4+ issues in this batch | "{name} recommended for {N} issues - consider distributing." |
| **Critical goes to experts** | Blocker/Critical priority issues | Always recommend the top domain contributor. Do not suggest growth opportunities for Blocker/Critical. |

### Layer 5 - Context Proximity

Compare each unassigned issue against each member's *current* open work (already fetched in Layer 3).

For each `(unassigned issue, team member)` pair:

1. **Component overlap** - does the unassigned issue share a component with any of the member's open issues? Score: +3 per shared component.
2. **Keyword overlap** - extract 2-3 word tokens from the unassigned issue summary. Compare against the member's open issue summaries. Score: +1 per shared keyword (case-insensitive, ignoring stop words).
3. **Parent overlap** - does the unassigned issue share a parent epic with any of the member's open issues? Score: +5 (strongest signal - same deliverable).

Higher proximity score = lower context-switching cost.

## Scoring

For each `(unassigned issue, team member)` pair, compute a composite score:

```
score = (expertise_match × 3) + (proximity_score × 2) - (capacity_penalty × 1)
```

Where:

| Factor | Computation |
|--------|-------------|
| `expertise_match` | Number of matching components + domain keywords between the issue and the member's profile (Layer 2) |
| `proximity_score` | Context proximity score from Layer 5 |
| `capacity_penalty` | `open_issues_current_sprint × 1`. If overloaded flag is set, add +10 penalty. |

**Rank members by score (descending).** Recommend the top scorer. Include the runner-up if scores are within 20%.

**Override rules:**

- Blocker/Critical: always recommend the highest `expertise_match` regardless of capacity (note the load concern in rationale).
- Overloaded members (≥10 open sprint issues): exclude unless they are the only expert for a Blocker/Critical.

## Output

### Data Contract

Callers (refinement, release, or other workflows) consume this structure:

```json
{
  "team": "RHDH Cope",
  "team_id": "ec74d716-af36-4b3c-950f-f79213d08f71-4403",
  "mode": "deep",
  "roster_size": 9,
  "recommendations": [
    {
      "key": "RHIDP-1234",
      "summary": "Issue summary text",
      "priority": "Major",
      "proposed_assignee": "Allison Hill",
      "proposed_account_id": "712020:9974d75b-...",
      "score": 14,
      "rationale": "Top expertise in plugins (12/50 issues). Capacity: 5 issues / 13 SP. Currently working on RHIDP-1200 (related component).",
      "runner_up": "Noah Rhodes (score: 12)",
      "signals": ["context_proximity: RHIDP-1200 shares 'plugins' component"]
    }
  ],
  "warnings": [
    "Bus factor: Allison Hill owns 70% of 'plugins' issues. Consider spreading.",
    "Daniel Wagner overloaded (12 open sprint issues) - excluded from non-critical."
  ]
}
```

### Markdown Template

```markdown
## Assignee Recommendations ({team})

Mode: **{mode}** | Roster: {roster_size} members | Issues analyzed: {count}

| # | Issue | P | Summary | Recommended | Score | Rationale |
|---|-------|---|---------|-------------|-------|-----------|
| 1 | [RHIDP-1234](url) | Major | Summary | Allison Hill | 14 | plugins (12/50), 5 issues/13 SP, proximity: RHIDP-1200 |

**Signals:**
- Bus factor: Allison Hill owns 70% of 'plugins'. Consider Angie Henderson (3/50, 5 issues/8 SP).
- Growth opportunity for Cristian Santos in 'catalog' - 2 prior issues.

**Warnings:**
- Daniel Wagner excluded (12 open sprint issues, overloaded).
```

## Assignment

After the user reviews recommendations:

Use the standard confirmation flow from SKILL.md (`y/N/edit`).

Follow the API preference order from SKILL.md. In deep mode (GraphQL reads already set up `AUTH`), prefer REST. In quick mode (no prior API calls), prefer acli.

### REST API assignment

```bash
curl -s -X PUT \
  -u "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"assignee": {"accountId": "ACCOUNT_ID"}}}' \
  "https://redhat.atlassian.net/rest/api/3/issue/RHIDP-1234"
```

| HTTP Status | Action |
|-------------|--------|
| 204 | Assigned. Report success. |
| 400 | User cannot be assigned (permissions). Report and skip. |
| 403 | No edit permission. Report and skip. |
| 429 | Wait 5 seconds, retry once. |

### acli assignment

```bash
acli jira workitem assign --key RHIDP-1234 --assignee "ACCOUNT_ID" --yes
```

`--assignee` accepts an account ID or email address. `--yes` is mandatory to avoid interactive prompts.

For bulk assignment from a file:

```bash
# Create a file with key,accountId pairs
acli jira workitem assign --from-file assignments.txt --yes
```

If acli fails, fall back to REST API.

After all assignments, summarize:

```markdown
## Assignment Results
- ✅ RHIDP-1234 → Allison Hill
- ✅ RHIDP-5678 → Noah Rhodes
- ❌ RHIDP-9012 → Angie Henderson (403: no edit permission)
```

## Error Handling

| Error | Action |
|-------|--------|
| Team ID not found / `teamV2` returns null | "Team not found. Verify the team UUID." |
| `issueSearchStable` returns errors | See SKILL.md Error Handling. |
| Member has 0 issues in 90 days | Include in roster but mark as "no recent activity - cannot build expertise profile." |
| GraphQL rate limit (429) | Wait 5 seconds, retry once. If still fails, skip that member and note "partial profile." |
| All members overloaded | Warn: "All team members have ≥10 open sprint issues. Recommending least-loaded member with caveat." |
| Unassigned issue has no components | Score on keyword and parent overlap only. Note: "No components set - recommendation based on summary keywords only." |

## Caveats

1. **Expertise profiles are backward-looking.** 90-day window may miss someone who recently joined the team or changed focus areas.
2. **Story points are inconsistently set.** Capacity scoring falls back to issue count when SP data is sparse.
3. **`issueSearchStable` is beta.** Requires `X-ExperimentalApi: JiraIssueSearch` header. If it breaks, fall back to REST `/rest/api/3/search` with the same JQL.
4. **Team field values cannot be read via GraphQL on issues.** Use `team.teamV2` for roster (works). For filtering issues by team, use JQL `"Team[Team]" = {teamId}` in the search query.
5. **Context proximity is only as good as issue metadata.** Issues without components or with vague summaries produce weak proximity scores.
