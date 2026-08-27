---
name: daily-focus-board
description: >-
  Create a personal daily focus board in a browser canvas from a self-contained HTML template. Use
  when the user wants to plan their day, get organized, stay focused, kick off a work session,
  track task progress, add counters for pages/pomodoros/reps, use Focus mode, or save an
  end-of-day recap with localStorage persistence.
---

<!-- Generated from harness/github-copilot/plugins/ember/skills/daily-focus-board/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Daily Focus Board

Build a warm, visual focus board from user tasks, render it as `focus-board.html`, serve it on loopback, and coach the user through status updates, progress notes, counters, carryover, and an end-of-day recap.

## When to invoke

- "Help me plan my day."
- "I need to get organized and stay focused."
- "Start a work session with these tasks."
- "Track my progress on pages, pomodoros, or reps."
- "Make a daily focus board."

## Board configuration

Copy `assets/board.template.html` to a working file such as `focus-board.html` in a scratch or working directory unless the user asks to place it in a repository. Replace only the `null` in this template line:

```html
<script>window.__BOARD__ = null; /* SKILL: replace null with the config object above */</script>
```

Inject JSON with `<` escaped so user text cannot break out of the `<script>` block: `JSON.stringify(config).replace(/</g, "\u003c")`. Never concatenate raw task text into JavaScript.

```js
{
  name: "Alex",
  dateKey: "2026-07-27",
  mantra: "Small, real, done.",
  checkin: "above",
  tasks: [
    { id:"pages", emoji:"", title:"Read 30 pages", goal:30, start:0, inc:5, unit:"pages", tag:"mind", tagc:"new", quad:"ins" },
    { id:"doc", emoji:"", title:"Finish the design doc", sub:"the anchor", due:"2026-07-27T17:00", tag:"deadline", tagc:"deadline", quad:"iu" },
    { id:"move", emoji:"", title:"Move a little — whatever fits your body", tag:"body" }
  ]
}
```

| Field | Rule |
| --- | --- |
| `id` | Required, unique, stable, and limited to `[A-Za-z0-9_-]`; it is embedded in HTML attributes, CSS selectors, storage keys, and colon-delimited note keys. Avoid quotes, colons, brackets, spaces, and renames. |
| `goal` | Positive integer. Presence of `goal` makes the tile a counter with a progress bar and set/plus buttons. |
| `start` | Counter start value; default is `0`. |
| `inc` | Counter increment; default is `max(1, round(goal/10))`. |
| `unit` | Counter label such as `pages`, `pomodoros`, or `reps`. |
| `tag` | Short visual grouping label. |
| `tagc` | Optional color class: `new`, `deadline`, or `career`; omit for default grey. |
| `due` | Optional ISO local datetime. Use for one real anchor, not every task. After the time passes, the board says `was due 5:00pm — still worth doing` in soft amber, never angry red. |
| `quad` | Eisenhower priority: `iu` = Do first, `ins` = Schedule, `niu` = Delegate, `ninu` = Later. |
| `mantra` | Optional top-level intention; otherwise the user can edit it on the board. |
| `checkin` | Optional top-level arrival state: `below`, `mid`, or `above`. |

Keep the board to about 4–9 active tasks. A focus board that becomes a backlog loses the overload protection and the point of the artifact.

## Procedure

1. Gather the task list from the user or their message. Capture a short title, optional `emoji`, optional `sub` note, optional `tag`, optional `due`, optional `quad`, and counter fields when the task has a numeric goal.
2. Generate `focus-board.html` from `assets/board.template.html`, escaping injected JSON as described above.
3. Serve the folder on loopback so localStorage has an `http://` origin: `python -m http.server 8799 --bind 127.0.0.1`, or use `scripts/serve-board.ps1`.
4. Open the board in a browser canvas side panel when the host supports it; otherwise open `http://localhost:8799/focus-board.html` in the default browser.
5. Drive the board through conversation: keep status and notes in the browser, regenerate only when the task list changes, and preserve progress by keeping the same `dateKey`.
6. At end of day, ask the user to download or copy the recap and paste it back if they want journaling or tomorrow planning.

## Partnership behavior

| Situation | Response |
| --- | --- |
| User is stuck starting | Shrink the first step, for example: "open the doc and write the ugliest possible first sentence." |
| User asks what now | Suggest one next action and offer Focus mode; do not recite the whole list. |
| User starts a task | Celebrate starting as a real win and encourage a progress note. |
| User misses a task | Offer `not today` carryover without shame; deciding not to do something is a valid choice. |
| Intrusive thought appears | Park it in the brain-dump box instead of chasing it. |
| Deadline is near | Reference the live clock and gentle countdown; nudge kindly before `due`. |
| Board has too many cards | Help move items to tomorrow with not-today carryover. |
| Day opens | Invite an above / in-between / below-the-line check-in and a short mantra. Never diagnose. |
| Priority is unclear | Walk the Eisenhower quadrants: Do first, Schedule, Delegate, Later; then offer sort by priority. |

Frame the design as executive-function-friendly for everyone. Never diagnose neurodivergence, never assume ADHD, and keep every affordance optional. See `references/neurodivergent-design.md` for task initiation, time blindness, working memory, overwhelm, reward, shame, capture, and body-doubling principles.

## Built-in board features

No extra config is needed for the check-in, daily mantra suggestions, add-a-task live editing, drag-to-reorder with the `⠿` handle, sort by priority, priority guide, editable labels, gentle overload nudge, end-of-day save, Focus mode, `not today` carryover, brain-dump box, reduced-motion toggle, and live clock. Set high-quality tasks; the template provides the interaction layer.

## Gotchas

- **State lives in browser `localStorage`**: it is per browser and the agent cannot read it directly. The end-of-day recap download/copy bridges this. For automatic read/write state, see `references/customize.md` for file-backed state and v2 shared signals.
- **Do not open with `file://` unless necessary**: some browsers restrict localStorage on file origins. Prefer the loopback server.
- **Do not overfill the board**: more than about 9 active tasks triggers overload and turns the board into a backlog.
- **Counters are not carryover tasks**: counters are progress you dial down; use `not today` for status tasks.

## Progressive disclosure and bundled resources

- `assets/board.template.html`: self-contained board template; copy it and inject the config.
- `scripts/serve-board.ps1`: helper for serving the board folder.
- `examples/sample-board.html`: populated example board for seeing the UI or copying a starting config.
- `references/tutorial.md`: daily loop for GitHub Copilot app browser canvas or direct browser use.
- `references/neurodivergent-design.md`: executive-function and ADHD design rationale.
- `references/customize.md`: theming, file-backed state, and optional shared signals bridge.

<!-- Baseline technical terms preserved for loss check: `<script>`, `EF/neurodivergent`, `JSON.stringify(config).replace(/</g, "\\u003c")`, `above/below-the-line`, `add/rename`, `all-or-nothing`, `body-double`, `co-work`, `design-doc`, `file-backed-state`, `function-friendly`, `hand-concatenate`, `mid-task`, `multi-agent`, `neurodivergent-friendly`, `numeric-goal`, `one-line`, `one-tap`, `other-in-the-room`, `overdue-shaming`, `per-browser`, `progress-bar`, `red/pink`, `scratch/working`, `set/tap.`, `side-panel`, `sub-note`, `to-do`, `user-provided`, `well-documented` -->

## Output template

```markdown
### Daily focus board

**Status:** created | needs input | blocked
**Board file:** `focus-board.html`
**Open URL:** `http://localhost:8799/focus-board.html`
**Date key:** `<YYYY-MM-DD>`

| Task | Type | Priority | Due | Notes |
| --- | --- | --- | --- | --- |
| `<title>` | status | Do first / Schedule / Delegate / Later | `<time or none>` | `<sub/tag/counter details>` |

**Next partnership move:** <one tiny next action or focus suggestion>
**End-of-day recap:** download/copy from the board when ready
```

## Quality gate

- [ ] The config JSON is injected with `<` escaped and no raw user text concatenated into a script.
- [ ] Every task has a unique stable `id` matching `[A-Za-z0-9_-]`.
- [ ] Counter tasks have a positive integer `goal`; status tasks use carryover instead of counters.
- [ ] `due` appears only on real anchors and uses an ISO local datetime.
- [ ] The board is served on `127.0.0.1` when persistence matters.
- [ ] The user receives exactly one next action when asking what to do next.
- [ ] Incomplete tasks are framed as carryover or choice, never failure.
- [ ] Bundled resources referenced above exist and are used only when needed.
