# Issue Refinement

Analyze issues for readiness, missing fields, duplicates, stale comments, and relevance. Produces a refinement report with actionable recommendations and optional auto-fixes.

Uses GraphQL for bulk reads (skip acli). Writes follow the API preference order in SKILL.md.

Authentication setup: see `references/auth.md`. All examples below assume `AUTH`, `CLOUD_ID`, and `GRAPHQL_URL` are set per that file.

## Refinement Context

Before generating the report, determine the refinement context. Ask or infer from conversation.

| Context | Goal | Urgency framing |
|---------|------|------------------|
| **Pre-release prep** | Features are ready to start work when the release kicks off | "Ready for a clean start" |
| **Mid-release hygiene** | In-flight features are on track, no blockers | "On track for delivery" |
| **Feature freeze triage** | All features must be complete or descoped | "Must close or descope before freeze" |

The context affects report tone, Slack messages, and which checks matter most. Pre-release prep cares about sizing + child epics + Refinement transition readiness. Freeze triage cares about completion + blockers + descope candidates.

## Input

The caller provides one of:

1. **Issue key(s)** - one or more specific issues to refine
2. **JQL query** - e.g., `"project = RHIDP AND sprint in openSprints() AND status = New"`
3. **`sprint`** - shorthand for "all issues in the current sprint that need refinement"
4. **`backlog`** - shorthand for "unrefined backlog issues for my team"

If `sprint` or `backlog` is used, ask for the team ID (or infer from context).

## Exit Criteria Reference

Load `references/workflows.md` for the full exit criteria tables per issue type and status. That file is the single source of truth for required fields at each workflow stage.

Key definitions used by the checks below:

- **Unrefined** = Story Points empty AND not in a sprint AND status is New or Refinement.
- **Ready for Planning** = Story Points set AND not in a sprint AND status is Backlog or To Do.
- **Planned** = Story Points set AND in an open/future sprint AND status is To Do, In Progress, or Review AND assignee set.
- **DoR** (Definition of Ready) = all exit criteria from entry statuses complete before moving to In Progress.
- **DoD** (Definition of Done) = all exit criteria for all statuses complete before moving to Closed.

## Refinement Checks

Run all applicable checks for each issue. Use GraphQL `issueSearchStable` for bulk reads.

### Check 1 - Missing Fields (Exit Criteria)

For each issue, determine its type and current status. Look up the required fields from the exit criteria tables in `references/workflows.md`. Report any missing fields.

GraphQL query to fetch issue data:

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-ExperimentalApi: JiraIssueSearch' \
  -d '{
    "query": "query RefineCheck { jira { issueSearchStable(cloudId: \"'"$CLOUD_ID"'\", issueSearchInput: {jql: \"JQL_HERE\"}, first: 50) { totalCount edges { node { key summary status { name } issueType { name } priority { name } assignee { name accountId } storyPoints parentIssue { key summary status { name } } fields { edges { node { __typename name ... on JiraComponentsField { components { edges { node { name } } } } ... on JiraSingleSelectField { fieldOption { value } } ... on JiraSprintField { selectedSprintsConnection { edges { node { name state } } } } ... on JiraLabelsField { labels { edges { node { name } } } } ... on JiraRichTextField { richText { adfValue { json } } } } } } } } } } }"
  }'
```

For each issue, check:

| Issue Type | Field | How to verify |
|------------|-------|---------------|
| All | Assignee | `assignee` is not null |
| All | Priority | `priority.name` is not "Undefined" |
| All | Component | At least one component in `JiraComponentsField` |
| Feature/Epic | Team | Cannot be read via GraphQL - use REST fallback: `GET /rest/api/3/issue/{key}?fields=customfield_10001` |
| Feature/Epic | Size | `JiraSingleSelectField` named "Size" has a value |
| Story/Task/Bug | Story Points | `storyPoints` is not null |
| Epic | Description | `JiraRichTextField` named "Description" is not empty |
| Feature (Refinement+) | Candidate label | Labels include `rhdh-X.Y-candidate` pattern |
| Feature (Backlog+) | Child Epics | Query `parent = {key}` to verify at least one Epic child exists |
| Epic (To Do+) | Child Stories/Tasks | Query `parent = {key}` to verify children exist |

### Check 2 - Duplicate Detection

Run the audit check from `references/duplicates.md` for each issue. Flag likely and possibly related duplicates in the report.

### Check 3 - Parent/Hierarchy Integrity

Verify the issue's position in the hierarchy:

| Issue Type | Check | Action if missing |
|------------|-------|-------------------|
| Epic | Has a parent Feature in RHDHPLAN | "Epic has no parent Feature. Link to an existing Feature or create one." |
| Story/Task | Has a parent Epic | "Story/Task has no parent Epic. Link to an existing Epic or create one." |
| Feature | Has at least one child Epic (if status ≥ Backlog) | "Feature in Backlog+ has no child Epics. Create delivery Epics." |
| Epic | Has at least one child Story/Task (if status ≥ To Do) | "Epic in To Do+ has no children. Break down into Stories/Tasks." |

Query parent:

```graphql
parentIssue { key summary status { name } issueType { name } }
```

Query children:

```bash
jql: "parent = {key} AND status != Closed"
```

### Check 4 - Unaddressed Comments

Fetch recent comments on each issue and check for unanswered questions or action items.

```bash
curl -s -u "$AUTH" \
  "https://redhat.atlassian.net/rest/api/3/issue/ISSUE_KEY/comment?orderBy=-created&maxResults=5" \
  -H "Accept: application/json"
```

Flag if:

- The most recent comment is a **question** (contains `?`) and was not posted by the current assignee - "Unaddressed question from {author}, {N} days ago."
- The most recent comment mentions **action items** (contains "TODO", "action item", "follow up", "next step") - "Unaddressed action item from {author}."
- The last comment is older than 14 days on an In Progress issue - "Stale - no activity for {N} days."

### Check 5 - Relevance and Staleness

Flag issues that may no longer be relevant:

| Condition | Flag |
|-----------|------|
| Status is New or Refinement AND `updated` > 90 days ago | "Stale in {status} for {N} days. Still relevant?" |
| Status is In Progress AND `updated` > 30 days ago | "In Progress but no updates for {N} days. Blocked?" |
| Fix Version is set to a released version AND status != Closed | "Fix version {version} is released but issue is still open." |
| Linked upstream issue is closed but this issue is still open | "Upstream {link} is closed. Can this be closed too?" |

For upstream checks, look at issue links with `outwardIssue` or `inwardIssue` containing GitHub URLs in comments or external links.

### Check 6 - Sprint Readiness (when input is `sprint`)

For issues in the current sprint, verify they meet the "Planned" criteria:

- Story Points set
- Assignee set
- Status is To Do, In Progress, or Review
- Component set

Flag any sprint issue missing these as "not sprint-ready."

## Output

### Data Contract

```json
{
  "issues_checked": 15,
  "issues_with_findings": 8,
  "findings": [
    {
      "key": "RHIDP-1234",
      "summary": "Issue summary",
      "status": "New",
      "type": "Epic",
      "checks": [
        {
          "check": "missing_fields",
          "severity": "error",
          "details": "Missing: Component, Size",
          "auto_fixable": false
        },
        {
          "check": "no_parent",
          "severity": "warning",
          "details": "Epic has no parent Feature in RHDHPLAN",
          "auto_fixable": false
        },
        {
          "check": "duplicate",
          "severity": "info",
          "details": "Possibly related to RHIDP-1100 (72% summary overlap)",
          "auto_fixable": false
        }
      ]
    }
  ],
  "summary": {
    "missing_fields": 5,
    "duplicates": 2,
    "hierarchy_gaps": 3,
    "unaddressed_comments": 1,
    "stale_issues": 2,
    "sprint_not_ready": 4
  },
  "auto_fixable": [
    {"key": "RHIDP-5678", "action": "set_priority", "value": "Major", "reason": "Parent epic is Major, child inherits"}
  ]
}
```

### Markdown Template

```markdown
## Refinement Report

Checked: {issues_checked} issues | Findings: {issues_with_findings} issues

### ❌ Missing Fields ({count})

| # | Issue | Type | Status | Missing |
|---|-------|------|--------|---------|
| 1 | [RHIDP-1234](url) | Epic | New | Component, Size |

### 🔄 Possible Duplicates ({count})

| # | Issue | Possibly duplicates | Overlap |
|---|-------|--------------------|---------|
| 1 | [RHIDP-1234](url) | [RHIDP-1100](url) | 72% |

### 🔗 Hierarchy Gaps ({count})

| # | Issue | Type | Gap |
|---|-------|------|-----|
| 1 | [RHIDP-1234](url) | Epic | No parent Feature |

### 💬 Unaddressed Comments ({count})

| # | Issue | Last comment | By | Days ago |
|---|-------|--------------|----|----------|
| 1 | [RHIDP-5678](url) | "Can we use the new API?" | Allison Hill | 7 |

### ⏰ Stale Issues ({count})

| # | Issue | Status | Last updated | Flag |
|---|-------|--------|-------------|------|
| 1 | [RHIDP-9012](url) | New | 95 days ago | Still relevant? |

### 🏃 Sprint Not Ready ({count})

| # | Issue | Missing for sprint |
|---|-------|--------------------|
| 1 | [RHIDP-3456](url) | Story Points, Assignee |

### Summary

| Check | Count |
|-------|-------|
| Missing fields | {n} |
| Possible duplicates | {n} |
| Hierarchy gaps | {n} |
| Unaddressed comments | {n} |
| Stale issues | {n} |
| Sprint not ready | {n} |
```

## Remediation

After presenting the report:

Use the standard confirmation flow from SKILL.md (`y/N/edit`). **y** applies auto-fixable changes and prompts for non-auto-fixable. **N** is report only.

### Auto-fixable actions

These are non-controversial changes applied without individual prompts:

- Setting Priority to parent's priority when child has "Undefined"
- Adding missing Component when parent Epic has exactly one component

### Always requires user input

- Setting Size (T-shirt) - needs estimation
- Setting Story Points - needs estimation
- Linking to parent Feature/Epic - needs selection from candidates
- Marking as duplicate - destructive, needs confirmation
- Closing stale issues - needs relevance confirmation. When closing, **always** add a comment documenting the rationale (e.g., "Closing as stale - no activity for 90 days, no longer on the roadmap") and set the resolution field (e.g., `Won't Do`, `Duplicate`, `Done`). This preserves the decision trail for future reference.
- Marking as duplicate - same rule: add a comment linking to the original issue and set resolution to `Duplicate`

For writes, follow the API preference order from SKILL.md. Since refinement uses GraphQL reads (AUTH is already set), prefer REST for writes.

## Error Handling

| Error | Action |
|-------|--------|
| `issueSearchStable` returns errors | See SKILL.md Error Handling. |
| Comment fetch fails (REST 403) | Skip Check 4 for that issue. Note "comments not accessible." |
| GraphQL rate limit (429) | Wait 5 seconds, retry once. If still fails, report partial results. |
| JQL returns 0 results | "No issues match the query. Check the JQL or team/sprint filters." |
| Issue type not recognized | Skip exit criteria check. Note "unknown issue type - skipped field validation." |

## Caveats

1. **Duplicate detection is keyword-based.** It catches obvious duplicates but misses semantically similar issues with different wording. When in doubt, flag as "possibly related" not "duplicate."
2. **Comment analysis is heuristic.** Question detection (looking for `?`) has false positives (rhetorical questions, URLs with query params). Use as a signal, not a verdict.
3. **Team field requires REST fallback.** GraphQL cannot reliably read team values from issues. When checking the Team field, make a REST call per issue: `GET /rest/api/3/issue/{key}?fields=customfield_10001`.
4. **Exit criteria may evolve.** The field requirements are maintained in `references/workflows.md`. If the process changes, update that file.
5. **Triage is automated separately.** The RHDH Triage Maintainer role is handled by an AI CronJob (`jira_triager_agent.py`) that sets Component, Team, and Priority on new issues. This refinement check complements triage - it validates deeper readiness, not initial routing.
