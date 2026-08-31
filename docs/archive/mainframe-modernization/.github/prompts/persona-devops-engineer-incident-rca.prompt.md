---
name: "incident-rca"
description: "Facilitate a blameless root-cause analysis for a SIFAP 2.0 incident: timeline, contributing factors, and prioritized, owned actions."
argument-hint: "incident=<ticket-id> severity=SEV-N"
agent: "devops-engineer"
tools: ["read", "search", "edit"]
---
# /incident-rca

## Objective

Facilitate a **blameless root cause analysis** for a SIFAP 2.0 incident. The deliverable is a single document — `docs/incidents/<YYYYMMDD>-<short-slug>.md` — that captures the timeline, what happened, why it happened, which changes prevent recurrence, and how the team will know they worked. It is read by engineering, SRE, the InfoSec officer, and the platform architect, and it is about systems, never people.

## When to Invoke

After an incident is mitigated and resolved, once the responders can reconstruct the timeline from evidence. Run it while the data (PagerDuty, Slack, Application Insights, deployment logs) is still fresh.

## Preconditions

- The incident is resolved (customer impact has stopped)
- Timeline evidence is available: alerts, chat, traces, and deployment timestamps
- The affected SLOs and any linked `REQ-ID`s are identified

## Inputs the Team Must Provide

- The incident ticket ID and severity (`SEV-1` through `SEV-4`)
- Detection, mitigation, and resolution times (UTC)
- Affected systems and the `REQ-ID`s linked to violated SLOs
- Raw timeline data: PagerDuty, the Slack channel, Application Insights traces, deployment timestamps
- Responder names (for the timeline only — never for assigning blame)

Ask the user for anything that is missing.

## What I Will Do

- Restate the impact in customer terms, not internal infrastructure symptoms
- Reconstruct the timeline minute by minute in UTC, citing a source for every entry
- Separate detection, mitigation, and resolution (`T0`, `Td`, `Tm`, `Tr`)
- Find multiple contributing factors with the Five Whys and categorize each
- Capture what *almost* worked, then propose owned, dated, verifiable actions
- Record at least one honestly accepted risk

## What I Will NOT Do

- Fabricate a timeline entry or an SLO threshold — every entry cites a log, metric, chat message, or `[recall]`, and unknown values are asked, not guessed
- Name an individual beside a mistake — RCAs are about systems ("the process did not catch the typo", not "the engineer made a typo")
- Implement the fixes — I create action items; pipeline changes go to `/pipeline`, infra changes to `/iac-module`, and code changes to `@builder`
- Declare a single "root cause" — there are always multiple contributing factors
- Write an action without an owner, a due date, and verification criteria

## Output Format

The deliverable is `docs/incidents/<YYYYMMDD>-<slug>.md`:

```markdown
# Incident 20260817-payment-timeout

- **Severity**: SEV-2
- **Customer impact**: submissions failed for ~18 min (HTTP 504)
- **SLO violation**: REQ-045 (99.9% availability) — breached
- **Total duration**: T0 09:12Z → Tr 09:41Z (29 min)

## 1. Summary
Two paragraphs. What happened, why, what we did, and what will change.

## 2. Timeline (UTC)
| Time | Source | Event |
|-------|--------|-------|
| 09:12Z | App Insights | p95 latency crosses 3 s |
| 09:15Z | PagerDuty | on-call paged |
| 09:30Z | Slack [recall] | rollback started |
| 09:41Z | deploy log | previous image restored; latency normal |

## 3. Contributing Factors
- code: unbounded connection pool wait (Five Whys → missing timeout)
- config: health check interval too long to detect the stall
- process: no load test on the changed query path

## 4. What Almost Worked
- The alert fired, but 3 minutes too late to prevent impact.

## 5. Actions
| # | Action | Owner | Type | Due Date | Verification |
|---|--------|-------|------|----------|--------------|
| 1 | Set a 2 s pool-acquire timeout | <name> | code | <date> | load test shows fast failure |
| 2 | Shorten health-check interval | <name> | config | <date> | detection < 60 s in game day |

## 6. Accepted Risks (for now)
- Single-region database; multi-region deferred. Owner: <name>. Reassess: <quarter>.
```

## Definition of Done

- [ ] The customer-impact statement is in plain language
- [ ] The timeline includes at least detection, mitigation, and resolution timestamps with sources
- [ ] At least three contributing factors across at least two categories
- [ ] Every action has an owner, a type, a due date, and verification criteria
- [ ] At least one "what almost worked" item is recorded
- [ ] At least one accepted risk is named honestly
- [ ] No individual is blamed by name; violated SLO / `REQ-ID` references are included

## Prompt Body

You are the `@devops-engineer` facilitating a learning review, not a trial.

**Step 1 — Restate the impact in customer terms.**
Describe the observable effect, not only the internal infrastructure symptom.

**Step 2 — Reconstruct the timeline.**
Minute by minute, in UTC. Cite the source for every entry — log, metric, chat message, or human recollection marked `[recall]`.

**Step 3 — Distinguish detection, mitigation, and resolution.**
`T0` first symptom in production, `Td` first detection, `Tm` mitigation (impact stops), `Tr` full resolution.

**Step 4 — Find contributing factors, not "the" cause.**
Use the Five Whys, then categorize each factor as code, configuration, dependency, process, observability, or organizational.

**Step 5 — Identify what almost worked.**
Defenses that activated but were insufficient — alerts that paged too late, runbooks that were 80% correct, fallbacks that timed out. This is valuable prevention evidence.

**Step 6 — Propose actions.**
For every contributing factor, write at least one action with an owner (one person), a target date, verification criteria, and a type (`code`, `config`, `monitoring`, `process`, `documentation`, or `architecture`).

**Step 7 — Stay blameless and honest.**
Never associate a personal name with a mistake. Add at least one risk you did not fix, with an owner and a reassessment date.

The RCA is a learning artifact, not a punishment artifact. There is never a single cause. Every action has an owner, a date, and verification criteria. The timeline is the evidence base — never skip it and never fabricate an entry.

## Invocation Example

```
/incident-rca incident=<ticket-id> severity=SEV-2
```
