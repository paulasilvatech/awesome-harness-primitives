---
name: desk-journal
description: >-
  Read, write, or append persistent desk journal entries that survive session boundaries and
  capture what was done, current state, next step, dead ends, artifacts, and desk closure
  handoffs. Use when the user asks to resume from a journal, write an end-of-session entry, add a
  mid-session checkpoint, or record a desk wind-down.
---

<!-- Generated from harness/github-copilot/plugins/the-workshop/skills/desk-journal/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Desk journal

Maintain `desks/<desk-name>/journal.md` as a concise persistent trail; read the latest entry to resume work or append a new entry that tells the next session what happened, where things stand, and what to do next.

## When to invoke

- "Read the desk journal before we continue."
- "Write an end-of-session journal entry."
- "Add a mid-session checkpoint to the journal."
- "Wind down this desk with a final summary."
- "Record what was done, current state, and next step."

## Prerequisites and context

- The journal path is `desks/<desk-name>/journal.md`; infer `<desk-name>` from the active desk, user request, or repository convention.
- The journal is persistent memory, not a full diary. Keep entries short enough for future sessions to scan.
- If the desk path cannot be inferred, report the missing desk name rather than writing to an arbitrary location.

## Journal entry types

| Situation | Entry type | Required fields |
| --- | --- | --- |
| Start of session | Read, not write by default | Most recent `Current state` and `Next step`; earlier history only as needed. |
| Mid-session checkpoint | Progress entry | `Worked on`, `Current state`, `Next step`; include decisions or significant progress. |
| End of session | Handoff entry | `Worked on`, `Current state`, `Next step`; include blockers and dead ends. |
| Desk wind-down | Desk closed entry | `Summary`, `Artifacts`, `Handoff`. |

## Writing rules

- Append to `desks/<desk-name>/journal.md`; do not rewrite history unless the user explicitly asks to correct an entry.
- Write for someone who knows nothing about the current session.
- Be specific: name repositories, artifacts, commands, decisions, failures, and next files to inspect when useful.
- Include what did not work so the next session does not repeat dead ends.
- Keep normal entries to 3-5 lines; put larger context on the bench as a separate artifact.
- Always include a next step for session entries.

## Entry templates

### Session or checkpoint entry

```markdown
## <date> — <short summary>
- **Worked on:** <what was done this session>
- **Current state:** <where things stand right now>
- **Next step:** <what the next session should pick up>
```

### End-of-desk entry

```markdown
## <date> — Desk closed
- **Summary:** <what this desk accomplished overall>
- **Artifacts:** <what's on the bench from this desk>
- **Handoff:** <anything another desk or the operator needs to know>
```

## Reading rules

| Need | Read |
| --- | --- |
| Resume work | The most recent entry first; use `Next step` as the starting point. |
| Understand decisions | Earlier entries around decision dates. |
| Close a desk | Recent entries plus bench artifacts so the final `Summary`, `Artifacts`, and `Handoff` are accurate. |
| Resolve conflicting state | Prefer newer entries unless they explicitly say they are uncertain. |

## Resume discipline

Entries must prevent the next session from having to `re-derive` the current state. Include enough concrete evidence, artifact names, and blockers to make that possible.
## Principles

- The journal is a cairn: every entry is a stone left so the next traveler finds the way.
- Honesty beats completeness; "I got stuck on X and don't know why" is more useful than silence.
- The journal is for the next session, not the current one.
- A vague entry such as "Worked on security scanning" is weak; a useful entry says which repos were scanned, what was found, what was triaged, and what remains.

## Output template

```markdown
## Desk journal result

**Status:** read | appended | blocked
**Journal:** `desks/<desk-name>/journal.md`
**Entry type:** start-of-session | mid-session checkpoint | end-of-session | desk closed

### Entry or latest state
```markdown
## <date> — <short summary or Desk closed>
- **Worked on:** <what was done this session>
- **Current state:** <where things stand right now>
- **Next step:** <what the next session should pick up>
```

### Notes
- <dead end, artifact, handoff, or none>
```

## Quality gate

- [ ] The journal path is `desks/<desk-name>/journal.md` and the desk name is not guessed when unavailable.
- [ ] Start-of-session work reads the most recent entry before summarizing context.
- [ ] Appended session entries include `Worked on`, `Current state`, and `Next step`.
- [ ] Desk closure entries include `Summary`, `Artifacts`, and `Handoff`.
- [ ] Entries are concise but specific enough for a future session to resume without re-deriving state.
- [ ] Dead ends, blockers, or uncertainty are recorded honestly when relevant.
