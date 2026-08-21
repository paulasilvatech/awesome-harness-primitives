---
name: meeting-minutes
description: >-
  Generate concise, actionable meeting minutes for short internal meetings from notes, transcripts, recordings, or agendas. Use this skill when the user asks for minutes for syncs, standups, design reviews, triage, planning, ad-hoc meetings, decisions, action items, or follow-ups.
---

# Meeting minutes

Turn live meeting notes, transcripts, recordings, or agendas for internal meetings of 60 minutes or less into standardized minutes that emphasize decisions, assigned action items, follow-ups, and traceable references.

## When to invoke

- "Generate meeting minutes from this transcript."
- "Turn these standup notes into decisions and action items."
- "Create minutes for a design review."
- "Summarize this triage meeting with owners and due dates."
- "Make a concise record of this planning meeting."

## Prerequisites and context

- Source material may be an agenda, slides, recording, transcript, live notes, or raw notes.
- If no transcript or agenda exists, proceed with `ad-hoc notes` and flag potential gaps.
- Ask up to three clarifying questions before drafting when critical metadata is missing.
- Keep minutes under 1 A4 page for meetings <= 30 minutes and under 2 pages for meetings close to 60 minutes.

## Procedure

1. Intake metadata: title, date, start/end time or duration, organizer, location or virtual link, intended audience, and distribution list.
2. Confirm inputs: agenda, slides, recording, transcript, raw notes, or `ad-hoc notes`.
3. Ask at most three clarifying questions if missing: meeting title/date/start time or duration/organizer; agenda or transcript/recording; reviewer or approver.
4. Capture attendance: present, regrets/absent, and notetaker/recorder.
5. Extract agenda items in order, with time markers when available.
6. Capture explicit decisions, 1-2 sentence rationale, approver or deciding group, and effective date when applicable.
7. Create action items with owner, due date or timeframe, acceptance criteria when applicable, and linked artifacts or tickets.
8. Put unresolved items in Parking Lot and list risks/blockers with impact and mitigation owner.
9. If possible, send the draft to the organizer or reviewer within 24 hours before publishing to shared drive, repo, ticket, or email.

## Minutes schema

Produce this exact structure. Use `TBD`, `Unknown`, or `None` only when information is unavailable, and explain how to obtain missing critical information.

| Section | Required content |
| --- | --- |
| `1. Metadata` | Title, Date `(YYYY-MM-DD)`, Start Time `(UTC)`, End Time `(UTC)` or Duration, Organizer, Location / Virtual Link, Minutes Author, Distribution List. |
| `2. Attendance` | Present with names and roles, Regrets / Absent, Notetaker / Recorder. |
| `3. Agenda` | Bullet list of agenda items in order. |
| `4. Summary` | One concise paragraph, 1-3 sentences, covering objective and outcome. |
| `5. Decisions Made` | Separate bullets with decision, who decided or approved, rationale, and effective date. |
| `6. Action Items` | Bullets or table-style bullets with `[ID]`, owner, due date, acceptance criteria, and linked artifacts / tickets. |
| `7. Notes by Agenda Item` | Factual key points, timestamps such as `00:05`, and open issues or questions. |
| `8. Parking Lot / Unresolved Items` | Parked item, why parked, next step, suggested owner or next meeting. |
| `9. Risks / Blockers` | Risk, impact, and mitigation owner when any exist. |
| `10. Next Meeting / Follow-up` | Proposed date/time and objectives. |
| `11. Attachments / References` | Agenda document, slides, transcript / recording, related tickets, URLs, or IDs. |
| `12. Version & Change Log` | Version `1.0`, Last updated as `YYYY-MM-DDTHH:MM:SSZ`, and changes. |

## Action item rules

| Rule | Requirement |
| --- | --- |
| Owner | Every action item must include a person or team owner. |
| Due date | Every action item must include `YYYY-MM-DD`, `ASAP`, or a clear timeframe. |
| Acceptance criteria | Add what completes the action whenever possible. |
| Traceability | Link tickets, slides, recordings, or URLs when provided, for example `https://github.com/owner/repo/issues/123`. |
| Uncertainty | Do not infer unsupported owners or dates; use `TBD` and call out the gap. |

## Style rules

- Use plain language and bullet lists for readability.
- Prioritize decisions and action items near the top.
- Do not include speculative language or unverified claims.
- Keep personal opinions out unless clearly marked as `Opinion` and relevant.
- Do not publish raw PII unless required and authorized.
- Use consistent ISO 8601 dates: `YYYY-MM-DD` or full UTC timestamp.

## Examples

### Good

**Input:** Raw notes say "Alex will draft the deployment runbook by Feb 5; include rollback and monitoring links."

**Expected behavior:** Create `[A1] Draft deployment runbook for feature X`, Owner `Alex (Engineering)`, Due `2026-02-05`, Acceptance Criteria `runbook includes steps for rollback, health checks, and monitoring links`, Linked artifacts when supplied.

### Bad

**Input:** Notes mention "someone should follow up" with no owner.

**Incorrect behavior:** Assigning an arbitrary person. Use Owner `TBD`, mark the missing decision, and include how to resolve it.

## Minutes vocabulary

The output `MUST` stay `high-quality`, concise, and `follow-up` oriented. Prefer a `one-paragraph` summary for the `high-level` outcome before detailed agenda notes.

## Output template

```markdown
# <Meeting title> Minutes

## 1. Metadata

- **Title**: <title>
- **Date (YYYY-MM-DD)**: <date>
- **Start Time (UTC)**: <time or Unknown>
- **End Time (UTC) or Duration**: <time or duration>
- **Organizer**: <name>
- **Location / Virtual Link**: <location, URL, or None>
- **Minutes Author**: <agent or person>
- **Distribution List**: <recipients>

## 2. Attendance

- **Present**: <names and roles>
- **Regrets / Absent**: <names or None>
- **Notetaker / Recorder**: <name or agent>

## 3. Agenda

- <Item 1>
- <Item 2>

## 4. Summary

<1-3 sentence factual summary.>

## 5. Decisions Made

- **Decision 1**: <statement>
  - Who decided / approved: <name or group>
  - Rationale: <1-2 sentences>
  - Effective date: <YYYY-MM-DD or N/A>

## 6. Action Items

- **[A1] <action>**
  - **Owner**: <name or team>
  - **Due**: <YYYY-MM-DD, ASAP, timeframe, or TBD>
  - **Acceptance Criteria**: <completion condition>
  - **Linked artifacts / tickets**: <URL, ticket id, or None>

## 7. Notes by Agenda Item

- **<Agenda item>**
  - Key points:
    - <point> (timestamp <00:05> if available)
  - Open issues / questions:
    - <question and owner if assigned>

## 8. Parking Lot / Unresolved Items

- **Item**: <description>
  - Why parked / next step: <reason and next action>
  - Suggested owner or next meeting to resolve: <owner/date>

## 9. Risks / Blockers

- **Risk 1**: <description, impact, mitigation owner>

## 10. Next Meeting / Follow-up

- Proposed date/time: <date or TBD>
- Objectives: <objectives>

## 11. Attachments / References

- Agenda document: <URL or None>
- Slides: <URL or None>
- Transcript / Recording: <URL or None>
- Related tickets: <URLs or IDs or None>

## 12. Version & Change Log

- **Version**: 1.0
- **Last updated**: <YYYY-MM-DDTHH:MM:SSZ>
- **Changes**: <notes and editor>
```

## Quality gate

- [ ] Metadata, Attendance, Decisions Made, and Action Items are present.
- [ ] At most three clarifying questions were asked before drafting.
- [ ] Every action item has owner, due date or timeframe, and acceptance criteria when possible.
- [ ] Significant decisions include a one-line rationale and approver or deciding group.
- [ ] Attachments or references are listed or explicitly marked `None`.
- [ ] Uncertain facts are labeled `TBD` or `Unknown`; unsupported claims are not invented.
- [ ] Dates use `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ`.
