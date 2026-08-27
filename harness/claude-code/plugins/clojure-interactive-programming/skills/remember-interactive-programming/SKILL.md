---
name: remember-interactive-programming
description: >-
  Remind the agent to work as an interactive programmer against a live system or REPL, using
  evaluated behavior as the source of truth, explaining hidden evaluations to the human,
  preferring structural editing, and maintaining a todo list. Use when a user wants REPL-driven
  programming guidance, especially for Clojure or Backseat Driver workflows.
---

<!-- Generated from harness/github-copilot/plugins/clojure-interactive-programming/skills/remember-interactive-programming/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Remember interactive programming

Work as an interactive programmer with a micro-prompt mindset: use the live system or REPL as the source of truth, make small evaluated changes, explain hidden tool evaluations succinctly, prefer structural editing, and keep the todo list current. Adapt the reminder with workflow and/or workspace specifics when the user provides them.

## When to invoke

- "Remember to use the REPL while programming."
- "Work interactively against the running system."
- "Use Backseat Driver or a live Clojure REPL for this change."
- "Keep me informed about what you evaluate and maintain todos."

## Interactive programming stance

| Principle | Behavior |
| --- | --- |
| System as source of truth | Validate assumptions by evaluating code in the running system or REPL instead of relying only on static reading. |
| Small feedback loops | Explore, modify, evaluate, and adjust in short cycles. |
| Human-visible narration | The human does not see tool evaluations; summarize large evaluations before or after running them. |
| Structural editing | Prefer structural editing tools when editing languages such as Clojure where syntax trees matter. |
| Todo tending | Keep the todo list current so interactive exploration does not lose the goal. |

## REPL workflow

1. State the immediate question the REPL evaluation will answer.
2. Evaluate the smallest expression or code path that provides evidence.
3. If evaluating a large amount of code, describe succinctly what is being evaluated.
4. Use results from the live system to decide the next edit.
5. Prefer structural editing tools for code changes when available.
6. Re-evaluate the changed behavior and update the todo list.

## Gotchas

- **Do not hide large evaluations**: the human cannot see what the REPL tool evaluates, so summarize intent and outcome.
- **Do not treat files as the only truth**: running state may contain loaded vars, data, routes, or configuration not obvious from source.
- **Do not let exploration sprawl**: every evaluation should connect to a todo or current hypothesis.
- **Do not use text-only edits when structural editing is available and safer**: preserve balanced forms and language structure.

## Output template

```markdown
## Interactive programming checkpoint

**Status:** exploring | changed | blocked
**Current hypothesis:** <what the live evaluation is testing>

| Evaluation or edit | Evidence from the system | Next todo |
| --- | --- | --- |
| `<REPL expression or structural edit summary>` | `<observed result>` | `<next action>` |

**Human-visible summary:** <succinct explanation of any large evaluation>
```

## Quality gate

- [ ] The live system or REPL was treated as the source of truth when available.
- [ ] Large evaluations were described succinctly for the human.
- [ ] Structural editing tools were preferred for structural code changes when available.
- [ ] The todo list was maintained during exploration and implementation.
- [ ] The final response reports what was learned from evaluated behavior, not only what was edited.
