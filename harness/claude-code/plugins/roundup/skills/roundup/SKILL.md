---
name: roundup
description: >-
  Generate personalized status briefings from a configured Roundup profile and available data
  sources such as GitHub, email, Teams, Slack, and Google Workspace. Use when the user asks for a
  roundup, leadership briefing, team update, weekly status, audience-specific update, or draft in
  their communication style.
---

<!-- Generated from harness/github-copilot/plugins/roundup/skills/roundup/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Roundup

Read the user's Roundup configuration, gather activity from configured sources for the requested audience and time window, synthesize themes instead of listing raw activity, and draft a status briefing in the user's established voice.

## When to invoke

- "Generate a leadership roundup for this week."
- "Draft a team update since Monday."
- "Give me a status briefing for the past two weeks."
- "Roundup what shipped and what is blocked."
- "What audiences and sources are configured for roundup?"

## Prerequisites and context

- The config file is `~/.config/roundup/config.md`; read it in full before gathering data.
- If the file is missing, say: "Looks like roundup hasn't been set up yet. Run roundup-setup first -- it takes about 5 minutes and teaches me how you communicate. Just say 'use roundup-setup' to get started."
- Use only data sources available in the environment. Note inaccessible central sources instead of fabricating coverage.

## Procedure

1. Read `~/.config/roundup/config.md` completely.
2. Determine the audience. If one audience is configured, use it. If multiple are configured and the user did not specify one, ask for a choice using the available audience names.
3. Determine the time window. Use the user's window such as "this week", "since Monday", or "last two weeks"; otherwise default to the past 7 days and mention that window.
4. Pull data from every configured source for that audience and time window.
5. Ask before drafting only for Known Gaps that would leave an obvious hole in the briefing.
6. Synthesize across sources into stories, decisions, blockers, outcomes, and risks.
7. Draft in the configured format, tone, length, filters, audience detail level, and distinctive patterns.
8. Offer iteration options: save to Desktop, make shorter, make longer, adjust tone, incorporate edits, or generate for another audience.

## Source gathering

| Source | What to gather | Notes |
| --- | --- | --- |
| GitHub | Opened, merged, reviewed PRs; opened, closed, active issues; notable commits for detailed audiences. | Extract what shipped, what is in progress, blockers, and review/discussion patterns. |
| M365 / WorkIQ | Email threads, meeting decisions, Teams messages, calendar context. | Ask 2-4 targeted questions with `ask_work_iq`, such as decisions in a meeting series or key threads for a project. |
| Slack | Important threads, announcements, decisions in configured channels. | Focus on what surfaced in chat but is not captured elsewhere. |
| Google Workspace | Gmail threads, Calendar meetings, recently updated Drive docs. | Extract decisions, context, activity, escalations, and action items. |
| Known Gaps | User-supplied context when a central source is unavailable. | Ask only when the gap would materially affect the briefing. |

For executive or big-picture audiences, skip granular commits and individual ticket lists unless they explain a theme or risk. For full play-by-play audiences, include individual items when the config expects detail.

## Synthesis rules

- Match the config's format: grouped bullets, narrative paragraphs, headers, subsections, and typical length.
- Match tone: direct, conversational, first-person, action-oriented, or other configured style.
- Include the content categories the user typically includes.
- Apply `Never Include` filters and preserve `Always Include` standing items unless audience length constraints require folding them into existing bullets.
- Respect distinctive patterns such as opening with a one-line summary, ending with a call to action, or separating risks.
- Synthesize; do not paste an activity log. A PR, Teams thread, and issue about the same topic should become one story.
- Do not pad when data is thin.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| Config seems outdated | Generate from reachable sources, name the failures, and suggest re-running roundup-setup. |
| No config file | Give the exact setup message and stop; do not generate from guesses. |
| Audience not in config | Offer to draft using default style or collect audience preferences and append them to the config. |
| User seems unsure | Explain briefly: "Roundup generates status briefings based on the config you set up earlier. Just tell me who it's for and what time period to cover." Then ask for audience. |
| User wants iteration | Revise while staying anchored to the config's voice; do not drift toward generic AI writing. |
| User forgot configuration | Read the config and summarize audiences, sources, and preferences. |

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `ask_user`
- `follow-up`
- `list_pull_requests`
- `re-present`
- `re-run`
- `roundup-leadership-2025-03-24`
- `roundup-leadership-2025-03-24.md`
- `search_pull_requests`
- `sub-sections`
- `team/project`
- `two-week`
- `~/Desktop`

## Output template

```markdown
Here's a draft <audience name> briefing covering <time window>:

<briefing in the user's configured format and tone, not inside a code block>

Options:
- Looks good -- save to Desktop
- Make it shorter
- Make it longer / add more detail
- Adjust the tone
- I'll make some edits
- Generate for a different audience

<optional gap note if an inaccessible configured source was material>
```

## Quality gate

- [ ] `~/.config/roundup/config.md` was read in full or the missing-config setup message was returned.
- [ ] Audience and time window were determined from the request or config.
- [ ] Every configured accessible data source was checked for the window.
- [ ] Material Known Gaps were handled before drafting or noted after drafting.
- [ ] The draft matches the configured format, tone, filters, audience detail level, and distinctive patterns.
- [ ] Related items across sources were synthesized into themes rather than listed separately.
- [ ] Thin data was reported plainly without filler.
