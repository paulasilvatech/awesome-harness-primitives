# Fields, Labels, Links, Components & Priorities

## Custom Fields

| Field | ID | Type | Notes |
|-------|-----|------|-------|
| Team | `customfield_10001` | `atlassian-team` | **NOT JQL-filterable.** Fetch all, filter by `.name` in post-processing. Returns complex object in JSON: `{id, name, title, avatarUrl, isShared, ...}` |
| Size | `customfield_10795` | dropdown | T-shirt sizing: XS, S, M, L, XL. Returns `{value: "M"}` in JSON. |
| Story Points | `customfield_10028` | number | Primary estimation field. |
| DEV Story Points | `customfield_10506` | number | Inconsistently populated. |
| QE Story Points | `customfield_10572` | number | Inconsistently populated. |
| DOC Story Points | `customfield_10510` | number | Inconsistently populated. |
| Epic Link | `customfield_10014` | issue key | Legacy field - prefer `parent` for new hierarchy. |
| Parent Link | `customfield_10018` | issue key | Links Epic → Feature cross-project. |
| Sprint(s) | `customfield_10020` | array | Array of sprint objects with `name`, `state`, `startDate`, `endDate`. Not available via `--fields` - use `--json`. |
| Release Note Type | `customfield_10785` | dropdown | Values: Feature, Enhancement, Developer Preview, Deprecated Functionality, Removed Functionality, Release Note Not Required. |
| Release Note Text | `customfield_10783` | textarea (ADF) | Actual release note content. Should be populated when RN Type is customer-facing. |
| Acceptance Criteria | `customfield_10718` | textarea | **Almost always null.** Check description and comments instead for "Requirements", "Acceptance Criteria", or bullet-style criteria. |
| Feature Status | `customfield_10807` | dropdown | Found on RHDHPLAN Features. Values include `Proposed`. |
| Rank | `customfield_10019` | string | Lexorank ordering. Generally not needed for agent operations. |

### Custom field JQL syntax

Use `cf[ID]` syntax in JQL for custom fields:

```jql
-- Story points empty
cf[10028] is EMPTY

-- Size is set
cf[10795] is not EMPTY

-- Release Note Type missing
cf[10785] is EMPTY
```

## Standard Fields

| Field | JQL Name | Notes |
|-------|----------|-------|
| Fix Version | `fixVersion` | Version targeting. `fixVersion = '1.10.0'` |
| Affects Version | `affectedVersion` | Used in RHDHBUGS for bug version tracking. |
| Components | `component` | JQL-filterable: `component = 'Documentation'`. Not available via `--fields` - use `--json`. |
| Parent | `parent` | Native hierarchy: sub-task → parent, epic → feature. `parent = RHDHPLAN-382` |
| Security Level | `security` | Present on RHIDP/RHDHPLAN (`"Red Hat Employee"`), typically null on RHDHBUGS/RHDHSUPP. **NOT JQL-filterable** - `security is not EMPTY` returns parse error. |

## Labels

All lowercase, hyphen-separated. Labels are global to the Jira instance.

| Label | Usage |
|-------|-------|
| `demo` | Customer-facing Features/Epics requiring a feature demo |
| `needs-info` | Release planning - needs more information |
| `needs-pm` | Release planning - needs product management input |
| `stretch` | Feature is a stretch goal for a release |
| `test-day` | Feature is a Test Day candidate |
| `rhdh-n.n-candidate` | Feature is a candidate for release n.n (e.g., `rhdh-1.10-candidate`) |
| `ci-fail` | Identifies CI failures |
| `must-have` | Documentation team - must-have for release doc plan |
| `nice-to-have` | Documentation team - nice-to-have for release doc plan |
| `rhdh-customer` | Issues from customer interactions (support cases, engagements) |
| `ga-support` | Target support level: GA (generally available) |
| `tp-support` | Target support level: Tech Preview |
| `dp-support` | Target support level: Developer Preview |

## Link Types

Match by **name** in `issuelinks`, not by ID.

| Name | Use | Direction | Notes |
|------|-----|-----------|-------|
| Blocks | Yes - dependency tracking | inward: "is blocked by", outward: "blocks" | |
| Depend | Yes - dependency tracking | inward: "is depended on by", outward: "depends on" | |
| Related | Yes - feature-to-epic mapping | bidirectional | For cross-team deps, only include when target is outside RHDHPLAN/RHIDP |
| Cloners | **IGNORE** | - | Noise from cross-release cloning |
| Issue split | Informational only | - | |
| Duplicate | **IGNORE** | - | |

List all available link types with: `acli jira workitem link type`

## Components (RHIDP)

Heavily used for filtering and routing. Key components:

Key components (run `acli jira workitem search --jql "project = RHIDP AND component = 'X'" --count` for current counts):

Documentation, Security, UI, Lightspeed, Orchestrator, Continuous Improvement, Plugins, Topology

Query by component: `project = RHIDP AND component = 'Documentation'`

Components are not available via `--fields` on search. Use `--json` to get component data.

## Priorities

| Priority | Notes |
|----------|-------|
| Blocker | Highest. Used for critical z-stream fixes. |
| Critical | High urgency. |
| Major | Standard priority for most work. |
| Normal | Used in RHDHSUPP. Not a standard Jira default. |
| Minor | Low priority. |
| Undefined | **Most common in RHIDP** (~300 open issues). Hygiene signal - should be set. |

## Hierarchy Model

Three JQL fields for hierarchy with subtly different behavior:

| JQL Field | What It Returns | When to Use |
|-----------|----------------|-------------|
| `parent = KEY` | Native Jira hierarchy (sub-task → task, epic → feature) | **Preferred.** Use for all new queries. |
| `'Epic Link' = KEY` | Legacy field - stories linked to an epic | Use only for older data that hasn't migrated. |
| `parentEpic = KEY` | Similar to Epic Link but slightly different results | Avoid unless specifically needed. |

Safest approach: always use `parent = KEY`.
