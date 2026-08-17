# JQL Patterns & Board Reference

All queries tested live against `redhat.atlassian.net`.

## Core Queries

```jql
-- My open issues across all RHDH projects
assignee = currentUser() AND project in (RHIDP, RHDHPLAN, RHDHBUGS, RHDHSUPP) AND status not in (Closed)

-- All open issues (cross-project)
project in (RHIDP, RHDHPLAN, RHDHBUGS, RHDHSUPP) AND status not in (Closed)

-- Issues in active sprint
project = RHIDP AND sprint in openSprints()

-- Unassigned in active sprint
project = RHIDP AND sprint in openSprints() AND assignee is EMPTY

-- Issues in future sprints
project = RHIDP AND sprint in futureSprints()

-- Recently updated (last 7 days)
project = RHIDP AND updated >= -7d ORDER BY updated DESC

-- Recently created bugs (last 14 days)
project = RHDHBUGS AND created >= -14d ORDER BY created DESC

-- Issues by fix version
project = RHIDP AND fixVersion = '1.10.0'

-- Issues by component
project = RHIDP AND component = 'Documentation'
```

## Hygiene Queries

```jql
-- Unrefined stories/tasks (no story points, New status)
project = RHIDP AND status = New AND cf[10028] is EMPTY AND issuetype in (Story, Task)

-- Features missing T-shirt size
project = RHDHPLAN AND issuetype = Feature AND cf[10795] is EMPTY AND status not in (Closed)

-- Bugs without fix version
project = RHDHBUGS AND issuetype = Bug AND fixVersion is EMPTY AND status not in (Closed)

-- Open blocker bugs
project = RHDHBUGS AND status not in (Closed) AND priority = Blocker

-- Overdue issues (released version, still open)
project = RHIDP AND fixVersion in releasedVersions() AND status not in (Closed)

-- Open vulnerabilities (CVE tracking)
project = RHIDP AND issuetype = Vulnerability AND status not in (Closed) ORDER BY priority DESC
```

## Hierarchy & Relationship Queries

```jql
-- Children of a Feature (epics under it)
parent = RHDHPLAN-100

-- Children of an Epic (stories/tasks under it)
parent = RHIDP-5000

-- Legacy: Epic Link (older data)
'Epic Link' = RHIDP-5000

-- Legacy: parentEpic (slightly different results than Epic Link)
parentEpic = RHIDP-5000

-- Orphan stories (no parent)
project = RHIDP AND issuetype = Story AND 'Parent Link' is EMPTY AND 'Epic Link' is EMPTY AND status not in (Closed)
```

Use `parent = KEY` for all new queries. `Epic Link` and `parentEpic` are legacy.

> ⚠️ Cross-project `parent = KEY` queries (e.g., finding RHIDP Epics under a RHDHPLAN Feature) work reliably via `acli` but may fail via GraphQL `issueSearchStable` or REST search (410 Gone). Always use `acli jira workitem search --jql "parent = KEY" --limit 200` for hierarchy lookups.

## Release & Planning Queries

```jql
-- Features by candidate label
project = RHDHPLAN AND labels = 'rhdh-1.10-candidate'

-- Features in Release Pending missing release notes
project = RHDHPLAN AND issuetype = Feature AND status = 'Release Pending' AND cf[10785] is EMPTY

-- Epics in Dev Complete (delivery tracking)
project = RHIDP AND issuetype = Epic AND status = 'Dev Complete'

-- Features with stretch label
project = RHDHPLAN AND issuetype = Feature AND labels = stretch AND status not in (Closed)
```

## Queries That DON'T Work

```jql
-- FAILS: issueFunction is a ScriptRunner add-on, not available
issueFunction in hasLinks()

-- FAILS: security field not queryable via JQL
security is not EMPTY

-- FAILS: childIssuesOf function not available
issuekey in childIssuesOf('RHIDP-5000')

-- FAILS: RHDHPAI project is archived
project = RHDHPAI
```

## Team Filtering

The Team field (`customfield_10001`) cannot be used in JQL. Use `scripts/parse_issues.py`:

```bash
acli jira workitem search --jql "project = RHIDP AND sprint in openSprints()" --json \
  | python scripts/parse_issues.py --enrich -f team="RHDH Install" -s key,summary,status,story_points
```

For acli search command syntax, see `references/acli-commands.md`.
For custom field IDs and `cf[]` JQL syntax, see `references/fields.md`.

---

## Boards

### Active Scrum Boards

| Board | ID | Team/Purpose |
|-------|----|-------------|
| RHDH Cope | 11374 | COPE team sprint board |
| RHDH Install | 11462 | Install team |
| RHDH Plugins | 11549 | Plugins team |
| RHDH Frontend Plugins & UI | 11525 | Frontend/UI team |
| RHDH AI Sprint | 10725 | AI team |
| RHDH Documentation Sprint | 10851 | Documentation team |
| RHDH Security | 11497 | Security team |
| RHIDP Sprints | 9736 | General RHIDP sprint board |
| Perf&Scale | 4783 | Performance and scale testing |
| RHIDP QE Sprints | 10444 | QE team |

### Active Kanban Boards

| Board | ID | Purpose |
|-------|----|---------|
| RHDH support bugs (RHDHSUPP) | 4116 | Support bug tracking |
| RHDH support bugs (RHDHBUGS) | 5367 | Bug tracking |
| RHIDP Feature Requests | 9795 | Feature request tracking |
| RHDH Program Features | 10870 | Program feature tracking |
| RHDH Outcomes | 11124 | Outcomes tracking |
| RHDH AI Triage & Refinement | 10695 | AI triage |
| RHIDP | 10154 | General RHIDP kanban |

### BMPTEMP Boards

Boards linked to the `Board Migration Project (BMPTEMP)` are migration artifacts. Most are inactive, but some may still have active sprints. Check with `acli jira board list-sprints --id <ID> --state active` before assuming they're dead.

## Sprints

### Naming Convention

Sprints follow: `{Team Name} {Sprint Number}` (e.g., "RHDH COPE 3291", "RHDH Install 3291"). Sprint numbers are shared across teams for the same sprint cycle.

### Finding Current Sprint

```bash
# List active sprints for a board
acli jira board list-sprints --id 11374 --state active

# List work items in a sprint
acli jira sprint list-workitems --sprint 65456 --board 11374
```

### Saved Filters

Pre-built JQL filters exist in the instance. Search for them:

```bash
acli jira filter search --name "RHDH"
```

These may be more efficient than building JQL from scratch for common queries.
