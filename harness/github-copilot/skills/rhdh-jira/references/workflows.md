# Jira Workflows & Exit Criteria

Exit criteria are **operational requirements** - fields that must be set before transitioning an issue to the next status. Transitioning without meeting these criteria results in broken issue state.

## Feature Workflow (RHDHPLAN)

```
New → Refinement → Backlog → In Progress → Release Pending → Closed
```

| Status | Required Fields Before Entry |
|--------|----------------------------|
| New | Assignee, Priority, Team |
| Refinement | Architect, QA Contact, Doc Contact, Link to Feature Request and/or Design Doc, Size (T-shirt) |
| Backlog | Candidate Version label (`rhdh-n.n-candidate`), Delivery Epics (Eng, QE, Doc) defined. Optional: `stretch` label for stretch goals. |
| In Progress | Fix Version set. At least one child Epic is In Progress, Dev Complete, Release Pending, or Closed. |
| Release Pending | Link to Feature Demo(s). ALL child Epics in Release Pending or Closed. |
| Closed | Target Version publicly available. |

### Definition of Ready (DoR)

Completion of all exit criteria from New, Refinement, and Backlog before moving to In Progress.

### Definition of Done (DoD)

Completion of all exit criteria for all statuses before moving to Closed.

---

## Epic Workflow (RHIDP)

```
New → Planning → To Do → In Progress → Dev Complete → Release Pending → Closed
```

| Status | Required Fields Before Entry |
|--------|----------------------------|
| New | Assignee, Team, Priority, Component |
| Planning | Description (including Acceptance Criteria), Size (T-shirt). Epic is refined; owner is defining stories/tasks. |
| To Do | All expected Stories/Tasks defined within the Epic. |
| In Progress | Stories are in progress. Fix Version updated. |
| Dev Complete | All linked stories, spikes, and tasks in Closed. Automation (E2E) may still be in progress. |
| Release Pending | Release Notes fields updated (Release Notes Text + Release Notes Type). All work (stories, spikes, automation) done. |
| Closed | Release (GA) has happened. |

---

## Story/Task Workflow (RHIDP)

```
New → Refinement → To Do → In Progress → Review → Closed
```

| Status | Required Fields Before Entry |
|--------|----------------------------|
| New | Description, Acceptance Criteria |
| Refinement | Acceptance Criteria, Story Points, Team, Priority, Assignee |
| To Do | Assignee set |
| In Progress | Work has started |
| Review | PR is up for review, has dev docs, and has been tested. Move to Closed once PR is merged. |
| Closed | PR merged and verified |

---

## Bug Workflow (RHDHBUGS)

```
New → Refinement → Backlog → In Progress → Review → Release Pending → Closed
```

| Status | Required Fields Before Entry |
|--------|----------------------------|
| New | Description, Acceptance Criteria, Story Points |
| Refinement | Acceptance Criteria, Story Points, Team, Priority |
| Backlog | Assignee |
| In Progress | Work has started |
| Review | PR up for review and tested |
| Release Pending | Release Notes fields updated (Release Notes Text + Release Notes Type). Work to be verified. |
| Closed | PR merged and verified |

---

## Feature Request Workflow (RHDHPLAN)

```
Backlog → Under Review → Accepted | Deferred | Rejected
```

Create as `type = Feature Request` in RHDHPLAN. Kanban-style - no sprints.

| Status | Meaning |
|--------|---------|
| Backlog | New request. Customer cases can be linked to show demand. |
| Under Review | ENG/PM reviewing. Researching and following up. |
| Accepted | Feature created and linked back to request. Will be prioritized into a future release. |
| Deferred | Not being added to roadmap right now. Comment describes why. May be re-evaluated. |
| Rejected | Won't be added to roadmap. Comment describes why. |

---

## RHDHSUPP Bug Workflow

```
New → In Progress → Review → Release Pending → Closed
```

Simplified workflow. Statuses Refinement, Backlog, and To Do exist in the workflow definition but are not used in practice.

| Status | Required Fields Before Entry |
|--------|----------------------------|
| New | Description, linked to customer case |
| In Progress | Engineering investigating |
| Review | Fix identified, PR in review |
| Release Pending | Fix ready, awaiting release |
| Closed | Resolved. Story Points set to capture effort spent. |

---

## Automation Rules

These automations run in the RHDH Jira instance:

| Rule | Trigger | Action |
|------|---------|--------|
| Keep Fix Version in Sync | Epic fix version updated | Reflect to all child issues |
| Move Epic to In Progress | Child issue moves to In Progress | Move parent Epic to In Progress |
| Inherit Fix Version | Fix-version-less epic added to a feature with fix version | Epic inherits the fix version |
| Move Feature to In Progress | Child epic moves to In Progress | Move parent Feature to In Progress |

Be aware of these when setting fix versions or transitioning issues - changes may cascade automatically.
