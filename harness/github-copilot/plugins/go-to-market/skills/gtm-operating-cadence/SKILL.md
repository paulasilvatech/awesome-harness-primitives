---
name: "gtm-operating-cadence"
description: >-
  Design operating cadence for scaling companies: meeting architecture, weekly metrics, quarterly planning, decision rights, async communication, CEO updates, and role clarity. Use when meetings do not produce decisions, alignment worsens during growth, decisions take too long, or leadership is stuck in meetings all day.
license: "MIT"
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

# Operating cadence

Operating cadence converts growth-stage coordination into meeting rhythms, metric reporting, quarterly planning, decision authority, and async documentation that make decisions faster instead of adding more meetings.

## When to invoke

- "Our meetings don't produce decisions."
- "We're growing but alignment is getting worse."
- "How often should we meet?"
- "Nobody knows what's happening across functions."
- "Decisions take forever and leadership is in meetings all day."

## Meeting architecture

Separate meetings by function, frequency, and decision authority. Every meeting must produce decisions or be cancelled. Status updates are async.

| Level | Cadence | Participants | Purpose | Success criteria | Anti-pattern |
| --- | --- | --- | --- | --- | --- |
| Level 1: Daily Standup | Daily, 15 min | Teams only, 5-10 people max | Yesterday finished, today starting, blockers | Finishes in 15 minutes and surfaces 1-2 blockers | Whole-company standups, status reporting, strategic discussion |
| Level 2: Weekly Functional Reviews | Weekly, 60 min | Function leadership | Metrics, feedback, blockers, one deep-dive, next-week priorities | One or two problems resolved or delegated | Trying to solve every problem in the meeting |
| Level 3: Weekly All-Hands | Weekly, 60 min | Whole company | CEO update, metric dashboard, one strategic deep dive, Q&A | Same dashboard every week and real answers | Defensive tone or inconsistent metrics |
| Level 4: Bi-Weekly Leadership Alignment | Bi-weekly, 90 min | Leadership | North star progress, functional updates, major decisions, next 2 weeks | Cross-functional blockers resolved | Functions report independently with no decisions |
| Level 5: Quarterly Strategic Planning | Quarterly, half-day to full-day | Leadership and functions | Retro, next-quarter priorities, breakouts, synthesis | Clear commitments and conflict resolution | Too much fun activity, no decisions |

Suggested functional review format: metric recap 10 min → wins/blockers 15 min → one deep-dive 30 min → next week priorities 5 min.

```
Company size <30?
├─ Yes → Levels 2-3 only: weekly functional + all-hands
└─ No → Continue...
    │
    30-100 people?
    ├─ Yes → All 5 levels
    └─ No → All 5 + skip-level reviews + function sub-cadences
```

| Company stage | Cadence adjustment |
| --- | --- |
| <30 people | Skip daily standups if everyone sees the work. Skip bi-weekly leadership because the company is the leadership layer. |
| 30-100 people | Add all five levels; monthly review catches what leaders no longer see daily. |
| 100-300 people | Add skip-level reviews because leadership is 2+ layers from execution. |
| 300+ people | Add function-specific sub-cadences. The CEO should be in fewer meetings than at 50, not more. |

## Weekly metric reporting

Monthly reporting catches problems 30 days late. Weekly reporting catches problems in week 2, when the month can still be saved.

```markdown
WEEK OF <DATE>

North Star: <Metric>
This Week: <Value> | Last Week: <Value> | Change: <+/- trend>
Context: <one sentence explaining why this trend matters>

Functional Metrics:
  Product:  7-Day Retention: <value> | Last: <value> | <change>
            Feature Adoption: <value> | Last: <value> | <change>
            Context: <why it moved>

  GTM:      Pipeline: <value> | Last: <value> | <change>
            New POCs: <value> | Last: <value>
            Context: <why it moved>

  Health:   Team Morale: <score>/10
            Context: <why it moved>
```

| Rule | Standard |
| --- | --- |
| Same metrics every week | Consistency enables pattern recognition. Add metrics when necessary; do not churn them quarterly. |
| One context sentence per metric | Explain why it matters versus plan or versus last period. |
| Trend direction for every metric | Mark up, down, or flat and decide whether significant movement is temporary or structural. |
| Traffic lights | GREEN means on track, YELLOW means watch, RED means action needed. |
| RED owner/action/deadline | Every RED item needs owner, specific action, and deadline. If RED two weeks in a row with the same action plan, escalate because the action plan is not working. |
| Metric count | Keep 8-12 total. If a metric does not change behavior when it moves, remove it. Dashboards with 40 metrics are decoration. |

Avoid vanity metrics that look good but do not predict outcomes: total downloads without adoption context, CEO headlines without supporting metrics, or pipeline without deal-health detail.

## Quarterly planning

Without quarterly planning, each function optimizes locally: Sales chases deals outside ICP, Product builds for one customer, and Marketing runs campaigns that do not connect to pipeline.

| Week | Work | Output |
| --- | --- | --- |
| Week 1: Retrospective + Data Gathering | Leadership prepares previous quarter results vs plan. Each function writes a 1-page retrospective: what worked, what did not, what we would do differently. Finance prepares revenue actuals, spend actuals, and forecast. Collect market data, competitive moves, customer feedback themes, and win/loss analysis. | Shared pre-read and facts. |
| Week 2: Priority Setting | Leadership half-day: review retrospectives as pre-read, agree on 3-5 company-level priorities, assign owner, success metric, and resource requirements, identify what you are not doing, resolve dependencies. | One-page priority set. |
| Week 3: OKR Cascade + Resource Allocation | Functions translate priorities into team OKRs. Leadership reviews alignment. Headcount, budget, and tools are finalized. Plan is shared company-wide. | Final plan and function commitments. |

Use the north star as the tiebreaker: "Does this help us hit the goal?" Prioritize what does and defer nice-to-have work. For every priority added, name one thing you are stopping. If you cannot name what you are not doing, you have too many priorities.

```markdown
Q2 2026 Roadmap
North Star: <what we are optimizing for>

Pillar 1: Product (<percent> team effort)
  Initiative: <name>
    Problem: <what we are solving>
    Success: <specific metric>
    Owner: <name>
    Timeline: <when>

Pillar 2: GTM (<percent> team effort)
  Initiative: <name>
    Problem: <what we are solving>
    Success: <specific metric>
    Owner: <name>
    Timeline: <when>

Pillar 3: People (<percent> effort)
  Initiative: <name>
    Problem: <what we are solving>
    Success: <specific metric>
    Owner: <name>
    Timeline: <when>

Pillar 4: Tech Debt (<percent> effort)
  Initiative: <name>
    Problem: <what we are solving>
    Success: <specific metric>
    Owner: <name>
    Timeline: <when>
```

## Decision velocity and authority

The fix for slow decisions is not more meetings; it is clear decision rights. Scaling companies often treat reversible, low-stakes choices like irreversible, high-stakes choices.

| Decision | Who decides | Timeline | Escalation |
| --- | --- | --- | --- |
| Company strategy | CEO | 1 week | Board if strategic |
| Feature priority | Product lead | 1 week | CEO if >3 engineering weeks |
| Customer support issue | CSM | Immediately | CS lead if escalated |
| Marketing campaign | Marketing lead | 2 weeks | CMO if >$10K budget |
| Hiring | Function leader | 2 weeks | CEO if role not approved |
| New partnership | CEO | 2 weeks | Board if strategic |
| Vendor selection | Function leader | 1 week | CEO if >$50K/year |

| Decision type | Examples | Decision mode | Timeline |
| --- | --- | --- | --- |
| Type 1: irreversible, high-stakes | Pricing model, market entry, major partnership | CEO or leadership decides after debate in one meeting | 1-2 weeks max |
| Type 2: reversible, low-stakes | Campaign creative, feature prioritization, single hire | Function owner decides, informs, iterates | Same day or next day |

Make decisions with 70% information, not 100%. Consensus culture often masquerades as collaboration: "Let's get everyone aligned" can mean nobody wants to decide. Name the decider, let them decide, and move on.

```
Does the meeting produce decisions?
├─ No → Can it be async?
│   ├─ Yes → Make it async and cancel the meeting
│   └─ No → Redesign with decision agenda
└─ Yes → Are the right people in the room?
    ├─ No → Fix attendee list; fewer is better
    └─ Yes → Keep it
```

## Async-first communication and CEO updates

Default to async and escalate to sync only when real-time collaboration is necessary.

| Use async for | Use sync for |
| --- | --- |
| Decision documents, major proposals with 48-72 hours for comments, progress updates, process changes, SOPs, and decisions already made | Real-time brainstorming, major disagreement, complex whiteboard topics, team building, and relationship work |

Document every decision: what was decided, why, who decided, when it takes effect, and who needs to know. Store decisions in a searchable wiki, shared drive, docs, or emails instead of Slack alone. Slack is ephemeral, noisy, and hard to search 6 months later.

The CEO weekly update is the highest-leverage communication tool at scale. Send it Sunday night or Monday morning, every week, in the same format:

1. Week focus: one paragraph on the priority.
2. North Star Progress: 1-2 bullets on metric trend and why it matters.
3. Wins This Week: 3-5 bullets on what shipped, customer/partner wins, and big-picture implication.
4. Blockers Getting Resolved: 1-2 bullets on what is being unblocked and who needs to know.
5. Ask: optional single bullet for referrals, feedback, or customer introductions.

Avoid updates that are too long, too detailed, only good news, or inconsistent. If the update skips a week, the team notices.

## Role clarity and ownership

Role clarity beats titles. Every initiative needs exactly one owner, supporting teammates, a metric, and impact-based success criteria. Eliminate initiatives without clear ownership within 48 hours.

| Test | Pass | Fail |
| --- | --- | --- |
| Single owner | One named person owns the outcome. | "The team" owns it, so nobody owns it. |
| KPI linkage | Success is measured by moving KPIs. | Success is completing tasks. |
| ROI clarity | Burn rate and resources connect to outcome. | Spend increases without visible return. |

## Terminology and preserved cadence signals

Use these exact operating terms when they fit the situation: five-level architecture, decision-making velocity, cross-functional blockers, skip-levels, follow-ups, Wins/blockers, CEO/leadership decisions, customer/product decisions, Customer/partner wins, customer-voice, wins/customer-voice, Up/down/flat trends, 7.2/10 morale scores, nice-to-have and to-have tradeoffs, and under-communicating in persistent docs.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `enterprise-account-planning` | skill | The operating issue is deal cadence, stakeholder management, MEDDICC, or account planning. |
| `0-to-1-launch` | skill | The task is launch-specific execution cadence. |
| `board-and-investor-communication` | skill | The task is board meeting structure or investor updates. |

## Output template

```markdown
## Operating cadence design - <company/team>

**Status:** designed | needs decision | blocked
**Scale:** <people count / stage>
**Primary failure mode:** <slow decisions / bad alignment / metric drift / meeting overload>

### Cadence architecture
| Level | Keep / add / remove | Participants | Decision owner | Notes |
| --- | --- | --- | --- | --- |
| Daily Standup | <choice> | <participants> | <owner> | <notes> |
| Weekly Functional Review | <choice> | <participants> | <owner> | <notes> |
| Weekly All-Hands | <choice> | <participants> | <owner> | <notes> |
| Bi-Weekly Leadership Alignment | <choice> | <participants> | <owner> | <notes> |
| Quarterly Strategic Planning | <choice> | <participants> | <owner> | <notes> |

### Weekly dashboard
| Metric | This week | Last week | Trend | Color | Owner | Action/deadline |
| --- | --- | --- | --- | --- | --- | --- |
| <metric> | <value> | <value> | <up/down/flat> | GREEN / YELLOW / RED | <name> | <action> |

### Decision rights
| Decision | Decider | Type 1/Type 2 | Timeline | Escalation |
| --- | --- | --- | --- | --- |
| <decision> | <person/role> | <type> | <timeline> | <path> |

### Quarterly priorities
- North star: <metric>
- Priorities: <3-5 priorities with owners and success metrics>
- Not doing: <explicit stopped/deferred work>

### Communication plan
- CEO weekly update: <day/time and sections>
- Async decision documentation: <where decisions live>
- Sync-only topics: <allowed reasons>
```

## Quality gate

- [ ] Each meeting has a decision purpose, owner, participants, and cancellation or async alternative when it is only status.
- [ ] Weekly dashboard has 8-12 behavior-changing metrics, trend direction, context, traffic-light status, and owner/action/deadline for every RED item.
- [ ] RED metrics repeated for two weeks are escalated.
- [ ] Quarterly plan has 3-5 priorities, owners, success metrics, resource allocation, and a "not doing" list.
- [ ] Decision rights name one decider and classify Type 1 versus Type 2 decisions.
- [ ] CEO weekly update and async decision documentation are specified in searchable, persistent formats.
- [ ] Output follows the `## Output template` exactly.

## References

- [technical-product-gtm source](https://github.com/beingsmit/technical-product-gtm)
- [Smit Patel](https://linkedin.com/in/smitkpatel)
