---
name: cli-mastery
description: >-
  Interactive training for the GitHub Copilot CLI through guided lessons, quizzes, scenario
  challenges, a final exam, and on-demand reference for slash commands, shortcuts, modes, agents,
  skills, MCP, and configuration. Use when the user says "cliexpert", asks to learn the Copilot
  CLI, wants a quiz, scenario, challenge, cheat sheet, or final exam.
license: MIT
metadata:
  version: 1.2.0
---

<!-- Generated from harness/github-copilot/skills/cli-mastery/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Copilot CLI mastery

Teach GitHub Copilot CLI one module at a time, track progress and XP, and load bundled lesson, quiz, scenario, reference, or final-exam material only when the user's trigger requires it. This remains a UTILITY SKILL; INVOKES are limited to the training workflow, and quiz routing covers `quizzes/scenarios.`.

## When to invoke

- "cliexpert"
- "Teach me the GitHub Copilot CLI."
- "Quiz me on slash commands."
- "Give me a Copilot CLI scenario challenge."
- "Show me a CLI cheat sheet or final exam."

## Prerequisites and context

- This is a utility skill for interactive Copilot CLI training, not general coding help or IDE-only features.
- Use `ask_user` with `choices` for all quizzes and scenarios when an interactive user is available.
- Use `sql` to persist progress in the session database.
- Use `view` to read bundled `references/` modules on demand.

## Routing and content

| Trigger | Action |
| --- | --- |
| `cliexpert`, `teach me` | Read the next `references/module-N-*.md` and teach one concept. |
| `quiz me`, `test me` | Read the current module and ask at least 5 questions via `ask_user`. |
| `scenario`, `challenge` | Read `references/scenarios.md` and run one scenario with choices. |
| `reference` | Read the relevant module and summarize directly. |
| `final exam` | Read `references/final-exam.md` and administer the exam. |

Answer specific GitHub Copilot CLI questions directly when the answer does not require loading a full module.

## Progress model

Initialize progress on first interaction:

```sql
CREATE TABLE IF NOT EXISTS mastery_progress (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS mastery_completed (module TEXT PRIMARY KEY, completed_at TEXT DEFAULT (datetime('now')));
INSERT OR IGNORE INTO mastery_progress (key,value) VALUES ('xp','0'),('level','Newcomer'),('module','0');
```

| Event | XP |
| --- | --- |
| Lesson completed | +20 |
| Correct answer | +15 |
| Perfect quiz | +50 |
| Scenario completed | +30 |
| Final exam | up to 200 |

| XP | Level |
| --- | --- |
| 0 | Newcomer |
| 100 | Apprentice |
| 250 | Navigator |
| 400 | Practitioner |
| 550 | Specialist |
| 700 | Expert |
| 850 | Virtuoso |
| 1000 | Architect |
| 1150 | Grandmaster |
| 1500 | Wizard |

Maximum XP from all content is 1600: 8 modules × 145, 8 scenarios × 30, and final exam 200.

## Teaching behavior

- Teach one concept at a time, then offer quiz, review, or next lesson.
- Show XP after each correct answer.
- When the module counter exceeds 8 and the user says `cliexpert`, offer scenarios, final exam, or review any module.
- Keep module progress aligned with completion records in `mastery_completed`.
- Do not use this skill for general coding, non-CLI questions, or IDE-only features.

## Progressive disclosure and bundled resources

- `references/module-1-slash-commands.md`
- `references/module-2-keyboard-shortcuts.md`
- `references/module-3-modes.md`
- `references/module-4-agents.md`
- `references/module-5-skills.md`
- `references/module-6-mcp.md`
- `references/module-7-advanced.md`
- `references/module-8-configuration.md`
- `references/scenarios.md`
- `references/final-exam.md`

Read only the module or exercise file needed for the current trigger.

## Output template

```markdown
## Copilot CLI mastery session

**Status:** lesson | quiz | scenario | reference | final exam | complete
**Module:** `<number and title>`
**Level:** `<level>`
**XP:** `<current>/<next threshold or max>`

### Content
<one concept, quiz question with choices, scenario, or reference answer>

### Next choices
- `<continue lesson>`
- `<quiz me>`
- `<review module>`
- `<scenario/final exam when eligible>`
```

## Quality gate

- [ ] The trigger was routed to the correct reference file or answered directly for a specific CLI question.
- [ ] Progress tables exist before XP or module state is read or written.
- [ ] Quizzes and scenarios use `ask_user` with `choices` when interaction is available.
- [ ] XP changes follow the defined values and the level is recalculated correctly.
- [ ] Only one concept, question, or scenario step is presented at a time.
- [ ] The response offers the next learner action after each lesson or assessment step.
