---
name: desk-open
description: >-
  Create and open a new workshop desk with a journal and .signals directory. Use when the operator
  wants to start a new workstream, work does not belong to an existing desk, or a topic needs its
  own durable frame, history, priors, and signal trail.
---

<!-- Generated from harness/github-copilot/plugins/the-workshop/skills/desk-open/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Open a desk

Create a workshop desk by making its folder, persistent journal, and structured signal directory so a future independent GitHub Copilot session can sit down, read the trail, and continue the workstream.

## When to invoke

- "Open a new desk for this workstream."
- "This topic needs its own desk and journal."
- "Create a desk for the security scan."
- "Start a separate frame for ops work."

## Desk model

| Element | Path | Purpose |
| --- | --- | --- |
| Desk root | `desks/<desk-name>/` | Stable home for one focused workstream. |
| Journal | `desks/<desk-name>/journal.md` | Persistent memory; read at session start and written at session end. |
| Signals | `desks/<desk-name>/.signals/` | Structured JSON signal output consumed by a dashboard. |

A desk is long-running in state, not runtime. The journal carries history forward; each GitHub Copilot session is independent and becomes associated with a desk only by reading and writing that desk's files.

## Procedure

1. Choose a short, descriptive kebab-case name such as `security-scan`, `api-review`, `ops`, or `cloud-workshop`.
2. Check whether `desks/<desk-name>/journal.md` already exists.
3. If the journal exists, do not overwrite it. Resume the desk by reading the journal, unless the operator explicitly renames or archives the existing desk first.
4. If the desk is new, create `desks/<desk-name>/journal.md` and `desks/<desk-name>/.signals/`.
5. Write the first journal entry with purpose, scope, initial context, and next step.
6. Announce the created paths and the desk focus.

## Journal requirements

The first entry must be useful to a session starting from zero.

| Field | What to record |
| --- | --- |
| Purpose | The desk's specific focus and why it exists. |
| Scope | Repositories, domains, systems, or workstreams covered by this desk. |
| Initial context | Known constraints, assumptions, relevant links inside the repository, or starting state. |
| Next step | The first concrete action the next session should take. |

When migrating older notes, map any `focus/purpose` wording into the Purpose field.

Use this exact starting shape:

```markdown
# <Desk Name> — Journal

## <date> — Desk opened
- **Purpose:** <what this desk focuses on>
- **Scope:** <repos, areas, or work this desk covers>
- **Next step:** <what the first session should do>
```

## Session orientation

1. The operator or TA starts a session and says "sit at the `<desk-name>` desk".
2. The session reads `desks/<desk-name>/journal.md` to load priors.
3. Work happens; the session uses `signal-write` to emit signals and `desk-journal` to persist state at the end.
4. The next session repeats from step 2.

## Principles

- A desk is a peer, not a sub-agent. It has equal standing to disagree with other desks.
- The journal is the memory. Without it, the next session starts blind.
- One desk, one focus. If the scope is too broad, open two desks.
- The desk identity comes from the journal that was read, not from a persistent process.

## Gotchas

- **Never overwrite a live desk**: an existing `journal.md` means the desk already has state.
- **Do not use vague names**: `misc` and `work` make future routing worse; use a topic or system name.
- **Do not create runtime expectations**: opening a desk initializes storage only; it does not launch or keep a process alive.

## Output template

```markdown
## Desk opened

**Status:** created | resumed | blocked
**Desk:** `desks/<desk-name>/`
**Journal:** `desks/<desk-name>/journal.md`
**Signals:** `desks/<desk-name>/.signals/`

### Focus
- Purpose: <desk purpose>
- Scope: <repos, systems, or topics>
- Next step: <first action>

### Notes
- <existing desk handling, archive requirement, or other important detail>
```

## Quality gate

- [ ] The desk name is short, descriptive, and kebab-case.
- [ ] Existing `desks/<desk-name>/journal.md` was checked before writing.
- [ ] A live desk was not overwritten.
- [ ] New desks include both `journal.md` and `.signals/`.
- [ ] The first journal entry records purpose, scope, and next step.
- [ ] The final response states whether the desk was created, resumed, or blocked.
