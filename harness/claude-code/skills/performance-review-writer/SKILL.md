---
name: performance-review-writer
description: >-
  Draft self-assessments, peer reviews, 360 reviews, upward feedback, annual reviews, mid-year
  reviews, and performance appraisals in the user's voice. Use when asked to write or improve
  review-cycle feedback using WorkIQ evidence, STAR examples, constructive tone, and markdown
  drafts saved under outputs/<year>/<month>/.
---

<!-- Generated from harness/github-copilot/skills/performance-review-writer/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Performance review writer

Draft honest, evidence-backed performance review text by gathering review context, surfacing contributions from WorkIQ or user notes, applying STAR structure, and saving a markdown draft the user can review manually.

## When to invoke

- "Write my self-assessment for this review cycle."
- "Draft a peer review for a colleague."
- "Help me write upward feedback for my manager."
- "I have my annual or mid-year review due."
- "Write a 360 review or performance appraisal."

## Prerequisites and context

- WorkIQ MCP access is recommended for Microsoft 365, Outlook, Teams, meeting, and communication evidence.
- If WorkIQ is unavailable or sparse, ask the user for `3–5` bullet points and proceed with those.
- Save drafts as markdown under `outputs/<year>/<month>/`, for example `outputs/2025/12/2025-review-self-assessment.md` or `outputs/2025/12/2025-peer-review-alex-chen.md`.
- Never submit a review; only draft text for the user to review and submit manually.

## Procedure

1. Gather at most three initial facts unless already provided: review type, subject, and review period.
2. Use WorkIQ or user-provided bullets to collect evidence for the review period. Summarize and redact evidence; do not reproduce raw excerpts, attendee lists, or sensitive personal details.
3. Draft using the schema for self-assessment, peer review, or upward feedback.
4. Mark thin claims with `[NEEDS DETAIL]` instead of inventing evidence.
5. Iterate on requested edits.
6. Save the final markdown draft to `outputs/<year>/<month>/` with a descriptive filename.

## Review types and evidence

| Type | Subject | Evidence to find | Tone |
| --- | --- | --- | --- |
| Self-assessment | The user | Delivered results, initiatives led, problems solved, repeated projects, praise, feedback, collaboration breadth. | Confident, evidence-backed, growth-oriented, first person. |
| Peer review | A colleague | Interactions between the user and subject, shared projects, help given, friction, observable impact. | Specific, constructive, balanced. |
| Upward feedback | The user's manager | Direction, support, feedback patterns, expectation clarity, recognition, availability, development support. | Diplomatic, honest, forward-looking. |

Use STAR for achievements: Situation, Task, Action, Result. Name projects, dates, outcomes, and people when appropriate; use numbers such as `reduced review time by 30%` only when supported.

## Style rules

| Do | Do not |
| --- | --- |
| Use specific projects, dates, outcomes, and observable behaviors. | Write vague filler such as "goes above and beyond", "team player", or "hard worker". |
| Acknowledge real challenges and what was learned. | Omit struggles entirely or overstate impact. |
| Use first person for self-assessments. | Write passively, such as "it was achieved". |
| Keep most fields to `2–4` sentences. | Over-write; longer is not better. |
| Frame development areas as next-cycle goals. | Attack personality, character, or motives. |
| Mark `[NEEDS DETAIL]` when evidence is weak. | Leave thin sections unmarked. |

## Review-cycle vocabulary

Use impact-focused language for self, peer, and manager feedback. For peer/upward reviews, describe what you/they did with observable evidence. If the review is a mid-year check-in, name it that way. Filename examples include `2025-review-self-assessment.md` and `2025-peer-review-alex-chen.md`.

## Output template

```markdown
## <Review period> <review type> draft — <subject>

**Status:** draft | needs detail | blocked
**Evidence used:** <WorkIQ summary or user-provided bullets, redacted>
**Saved to:** `outputs/<year>/<month>/<filename>.md`

### Draft
<self-assessment, peer review, or upward feedback content>

### Sections needing detail
- <section>: <specific missing evidence or "none">

### Validation
- WorkIQ or user notes reviewed: <yes/no and source type>
- Sensitive raw excerpts omitted: <yes/no>
- Draft saved: <yes/no and path>
```

## Examples

### Self-assessment schema

```markdown
## [Review Period] Self-Assessment — [Your Name]

### Summary
1–2 sentence overview of your year and primary areas of impact.

### Key Achievements
**[Project or Initiative Name]**
- Context: what was the situation or goal?
- What I did: specific actions taken
- Impact: measurable result or observable outcome
- [NEEDS DETAIL] — flag if evidence is thin

### Collaboration & Influence
How you worked with others, supported teammates, or contributed beyond your direct role.

### Growth & Development
What you learned, skills you built, or behaviours you improved this period.

### Areas for Development
1–2 honest areas where you want to grow next cycle. Frame as goals, not failures.

### Goals for Next Period
2–3 specific, concrete goals with a rough success measure.
```

### Peer review schema

```markdown
## Peer Review — [Colleague Name], [Their Role]
## Submitted by: [Your Name] | Period: [Review Period]

### Overall Impression
1–2 sentences on working with this person.

### Strengths (with examples)
**[Strength]**
- Example: specific situation where this showed up
- Impact on you / the team / the project

### Areas for Growth
1–2 specific, constructive observations. Frame as "I think [name] would have even more impact if..." not as criticism.

### Collaboration
How easy it was to work together: responsiveness, reliability, communication.

### Would you work with this person again?
Yes/No and a brief honest reason. Only include if the review form asks.
```

### Upward feedback schema

```markdown
## Feedback for [Manager Name]
## Submitted by: [Your Name] (anonymous if applicable) | Period: [Review Period]

### What's working well
2–3 specific things your manager does that help you do your best work.

### What could be better
Use: "When [X happens], I find it harder to [Y]. It would help if..."

### Support for my development
Specific development support, feedback, or opportunities.

### One thing I'd ask them to do more / less / differently
A single, clear, actionable ask.
```

## Limits

- Do not submit reviews or access systems to submit them.
- Decline requests to create dishonestly negative reviews or personal attacks; offer constructive reframing.
- Do not include sensitive information from unrelated conversations or threads.

## Quality gate

- [ ] Review type, subject, and period are known or explicitly marked missing.
- [ ] Evidence comes from WorkIQ summaries or user-provided bullets, not invented details.
- [ ] Achievement claims use STAR or equivalent context-action-impact structure.
- [ ] Thin areas are marked `[NEEDS DETAIL]`.
- [ ] Peer and upward feedback focus on observable behavior, not personality.
- [ ] No raw private excerpts, attendee lists, or sensitive unrelated details are included.
- [ ] Draft is saved under `outputs/<year>/<month>/` when file writing is requested or possible.
