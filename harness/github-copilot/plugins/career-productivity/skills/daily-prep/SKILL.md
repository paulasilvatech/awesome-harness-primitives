---
name: daily-prep
description: >-
  Prepare a structured HTML day-prep file for tomorrow or a requested date by pulling Outlook calendar details through WorkIQ, classifying meetings, detecting conflicts and day-fit issues, cross-referencing workspace tasks, finding learning and deep-work slots, and producing productivity recommendations. Use this skill when the user says "prepare me for tomorrow", "prep me for Friday", asks what a date looks like, or requests weekly planning.
---

# Daily prep

Generate a self-contained HTML prep file for a target workday with meeting context, task-linked prep bullets, conflict detection, learning and deep-work slots, and productivity recommendations.

## When to invoke

- "Prepare me for tomorrow."
- "Prep me for Friday."
- "What does March 25 look like?"
- "Run daily prep for next Monday, focused on customer meetings."
- "Plan my week using daily prep."

## Prerequisites and context

- WorkIQ MCP access to Outlook or Microsoft 365 calendar is required for meeting details.
- Workspace task files, customer folders, meeting notes, or plans improve prep bullets.
- Output path is `outputs/YYYY/MM/YYYY-MM-DD-prep.html`.

## Procedure

1. Determine the target date. Use the user's date if supplied; otherwise use tomorrow. If tomorrow is Saturday or Sunday, use Monday.
2. Pull calendar details from WorkIQ and cross-references workspace context: subject, start, end, organizer, attendees with email addresses, location, online status, and accepted or declined response. Follow up for optional, tentative, and recurring flags if missing.
3. Classify meetings, apply zone markers, and evaluate against the ideal day structure.
4. Detect overlaps, customer overload, deep-work disruption, non-ideal placement, early intrusion, and lunch conflicts.
5. Search workspace task files and recent customer/project context related to meeting subjects, customer names, and attendees.
6. Generate chronological prep for each meeting with time, subject, organizer, attendees, and 3–5 actionable prep bullets or clarification questions.
7. Find learning slots, morning focus gaps, and deep-work blocks; compute totals against targets.
8. Generate productivity recommendations and write or update `outputs/YYYY/MM/YYYY-MM-DD-prep.html` as self-contained dark-theme HTML with embedded CSS, color-coded timeline, and responsive layout.
9. If the file already exists, read it first and update rather than overwriting manual notes.

WorkIQ calendar prompt:

```text
What meetings do I have on {target date}? For each meeting, include: subject, start time, end time, organizer, all attendees with their email addresses, location, whether it's online, and whether I've accepted or declined.
```

follow-up prompt when needed:

```text
For the meetings on {target date}, which ones are marked as optional or tentative? Which ones are recurring?
```

## Meeting classification

| Label | Criteria |
| --- | --- |
| `[Customer · HIGH]` | External attendees from customer/partner domains, or subject matches a known customer name. |
| `[Internal]` | Only internal company domain attendees. |
| `[Community]` | CoP, community, guild, or learning sessions. |
| `[Upskilling]` | Training, workshop, certification, or learning. |
| `[Optional · skip]` | Tentative, low importance, or known recurring optional events such as Office Hours or Open Q&A. |
| `[Personal]` | Private events or non-work. |

## Day structure and scoring

| Zone | Time | Purpose | Rules |
| --- | --- | --- | --- |
| Morning Focus | Before 09:00 | Admin, learning, personal work | Protect from others' meetings. Flag external events. |
| Customer Zone | 09:00–12:00 | Customer or external meetings | Max 2 customer meetings. Prefer mornings for external calls. |
| Lunch | 12:00–13:00 | Break | Protected. Flag any overlap. |
| Deep Work | 13:00–15:30 | Deliverables, focused coding/writing | Minimize meetings. Flag non-essential meetings as disruption. |
| Protected (strict) | 15:30–16:00 | End-of-day wind-down | Flag all meetings regardless of organizer. |
| Protected (flex) | 16:00+ | End of day | Flag others' meetings only. Self-organized OK. |

Targets: learning hours **1.5h/day**. Deep work **2.5h** in 13:00–15:30, and customer meetings **max 2**, preferably 09:00–12:00.

Day Fit Score is 0–100%: morning focus clear +20%, ≤2 customer meetings in 09:00–12:00 +20%, lunch protected +15%, deep work intact +20%, nothing after 15:30 or only self-organized after 16:00 +15%, and ≥1h learning slots found +10%. Show categories as `≥80%`, `50–79%`, and `<50%`.

## Zone markers and day-fit issues

| Condition | Marker or issue | Action |
| --- | --- | --- |
| Starts ≥ 15:30 and < 16:00 | ` After-hours` | Recommend decline. |
| Starts ≥ 16:00 and non-self-organized | ` After-hours` | Recommend decline. |
| Starts ≥ 16:00 and self-organized | none | OK. |
| Before 09:00 and non-self-organized | ` Early` | Recommend decline; intrudes on learning window. |
| Before 09:00 and self-organized | none | OK. |
| Overlaps 12:00–13:00 | ` Lunch conflict` | Note in Calendar Notes. |
| More than 2 `[Customer · HIGH]` meetings | Customer overload | Recommend rescheduling 3rd+ customer meeting. |
| Non-essential meeting in 13:00–15:30 | Deep work disruption | Consider moving to morning. |
| Customer meeting outside 09:00–12:00 | Non-ideal placement | Note outside preferred morning zone. |

Self-organized means the user is the meeting organizer according to WorkIQ.

## Productivity recommendations

Use `auto-decline` only for rules that explicitly qualify; when no prep context exists, record what to `ask/clarify`.

| Section | Include |
| --- | --- |
| Day Fit Score | Score, category, and reasons. |
| Day Shape | Total meeting hours, focus time, learning hours, deep-work hours, heavy/moderate/light assessment. |
| Decline Candidates | Auto-decline candidates: meetings 15:30–16:00, others' meetings ≥16:00, others' meetings <09:00, 3rd+ customer meeting, optional meetings during deep work; include reclaim minutes. |
| Conflict Resolution | Specific recommendation for each overlap, prioritizing customer over internal/optional. |
| Learning Slots | Gaps ≥30 minutes, suggested activity, total versus 1.5h target. |
| Deep Work Blocks | Free gaps in 13:00–15:30, suggested task, total versus 2.5h available. |
| Energy Management | Flag >3h back-to-back customer meetings without a break. |
| Top 3 Priorities | Three highest-impact meeting or task outcomes. |

## Output template

```markdown
## Daily prep result

**Status:** complete | needs calendar access | blocked
**Target date:** `<YYYY-MM-DD>`
**Output file:** `outputs/YYYY/MM/YYYY-MM-DD-prep.html`

### Day shape
- Meeting hours: <hours>
- Learning slots: <found> / 1.5h target
- Deep work: <found> / 2.5h available
- Day Fit Score: <score and category>

### Calendar notes
| Time | Meeting | Label | Marker | Prep summary |
| --- | --- | --- | --- | --- |

### Recommendations
- Decline candidates: <count and reclaim minutes>
- Conflicts: <count and resolution summary>
- Top 3 priorities: <ordered list>

### Validation
- WorkIQ calendar pull: <pass|fail>
- Workspace context checked: <paths or none found>
- HTML file: <created|updated>
```

## Quality gate

- [ ] Target date and `outputs/YYYY/MM/YYYY-MM-DD-prep.html` path are computed correctly.
- [ ] WorkIQ calendar data includes organizer, attendees, response status, optional/tentative, and recurrence where available.
- [ ] Every meeting has a classification label and applicable zone marker.
- [ ] Conflicts and day-fit issues are reported separately.
- [ ] Workspace context was checked for customer names, attendees, tasks, summaries, and plans.
- [ ] Learning and deep-work slots include durations and totals against targets.
- [ ] Existing prep HTML was read before updating.
