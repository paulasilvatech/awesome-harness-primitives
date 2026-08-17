---
applyTo: '**'
description: 'Conventions for concise Copilot process tracking when a workspace-visible progress file is explicitly required.'
---

# Copilot Process Tracking Conventions — Minimal Workspace Log

These instructions apply when a task explicitly requires workspace-visible Copilot process tracking in the repository root. They are authoritative for the shape, restraint, and lifecycle of `./Copilot-Processing.md`; the user's current request, repository editing rules, and any prohibition on creating extra files win when they conflict.

Legacy enforcement vocabulary for this file includes `ABSOLUTE`, `MANDATORY`, `RULES`, `ENFORCEMENT`, `NEVER`, and `STOP`; preserve the restraint those terms signal while expressing the primitive as passive conventions.

## Tracking File Purpose

Use `./Copilot-Processing.md` only when process tracking is required for the interaction or follow-up. The file records the user request, an action plan, granular task items, completion status, and a final summary. Keep it in the workspace root so the user can edit it to reshape the interaction or save it when follow-up may be needed.

## Communication Restraint

- Do not flood the session with repeated status updates.
- Avoid phase announcements, verbose commentary, and progress narration unless the user explicitly asks for them.
- Work silently while updating the tracking file.
- Output only the text the task requires when a process-tracking convention specifies exact user-facing text.
- Do not repeat the word `Phase` in user-facing output unless the active task explicitly requires it.

## Planning and Execution Records

The tracking file should contain:

- User request details.
- A clear action plan.
- Detailed and granular task-specific action items.
- Todo and complete status (`todo/complete`) for each action item.
- Dependencies or prerequisites for each task.
- A final summary after all actions are complete.

Execute action items in logical groupings and groupings/phases where the user requires that vocabulary, then update completion status after each grouping. Do not skip items, combine unrelated actions without marking their status, or leave the tracking file stale.

## Lifecycle and Cleanup

Create `./Copilot-Processing.md` only when needed. When all actions are complete, add the final summary to the file and tell the user exactly: `Added final summary to ./Copilot-Processing.md.` Also remind the user to review the summary, confirm completion, and remove the file when done so it is not added to the repository.

## Good / Bad Examples

The examples below illustrate concise tracking without noisy chat output.

**Good:**

```markdown
# Copilot Processing

## Request
Rebuild assigned instruction primitives.

## Action Plan
- [x] Read contracts and references.
- [x] Rewrite assigned files.
- [ ] Run validation.
```

Why: The file records request context, plan, and status in one workspace-visible place without flooding the chat.

**Bad:**

```markdown
# Phase 1
I am starting now.

# Phase 2
I am still working.
```

Why: The log uses noisy phase headers and status chatter instead of actionable tasks and completion state.

## Conventions

| Rule | Rationale |
|---|---|
| Use `./Copilot-Processing.md` only when the task requires workspace-visible process tracking | Extra files create repository noise when tracking is unnecessary |
| Capture request details, action plan, granular tasks, dependencies, status, and final summary | Follow-up work remains understandable and resumable |
| Work silently and avoid repeated status updates | Chat context stays focused on task outcomes |
| Execute and mark action items in logical groupings | The tracking file reflects real progress |
| End with `Added final summary to ./Copilot-Processing.md.` when the tracking process is complete | The user receives the expected completion signal |
| Remind the user to remove the tracking file when done | Temporary process files do not accidentally enter source control |

## Do / Do Not

| Do | Do not |
|---|---|
| Keep process details in `./Copilot-Processing.md` when requested | Scatter progress narration through chat |
| Use granular checklist items with clear dependencies | Use vague status notes that cannot be acted on |
| Update completion state after work is actually done | Mark items complete before verification |
| Add a final summary after all actions complete | Leave the tracking file without closure |
| Tell the user to review and remove the file when done | Let a temporary tracking file be committed accidentally |

## Checklist Before Opening a PR

- [ ] `./Copilot-Processing.md` exists only if process tracking was explicitly required.
- [ ] The tracking file includes user request details, an action plan, granular tasks, dependencies, status, and final summary.
- [ ] Chat output avoids repeated status updates, phase announcements, and verbose commentary.
- [ ] Action items are marked complete only after execution.
- [ ] The final user message includes `Added final summary to ./Copilot-Processing.md.` when this tracking convention applies.
- [ ] The user is reminded to review and remove the tracking file when done.
