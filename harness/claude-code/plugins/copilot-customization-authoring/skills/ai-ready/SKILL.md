---
name: ai-ready
description: >-
  Help users install and use John Papa's ai-ready skill as the up-to-date source for making
  repositories AI-ready with AGENTS.md, copilot-instructions.md, CI workflows, issue templates,
  and stack-specific guidance. Use when the user asks to make a repo ai-ready, set up AI config,
  prepare for AI contributions, or install ai-ready.
---

<!-- Generated from harness/github-copilot/plugins/copilot-customization-authoring/skills/ai-ready/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AI ready

Guide the user to install the latest external `ai-ready` skill, transform their request into safe installation and review steps, and hand off execution to the installed source-of-truth skill; USE THIS SKILL for the ai-ready wrapper handoff.

## When to invoke

- "Make this repo ai-ready."
- "Set up AI config for this repository."
- "Prepare this repo for AI contributions."
- "Install the ai-ready skill."
- "Add AGENTS.md and copilot-instructions.md guidance."

## Source-of-truth model

This local skill is a wrapper. The full `ai-ready` skill by John Papa is large, changes frequently, and remains authoritative at `https://github.com/johnpapa/ai-ready`. John Papa's GitHub profile is `https://github.com/johnpapa`.

| Artifact the external skill may create | Purpose |
| --- | --- |
| `AGENTS.md` | Repository-level agent instructions and workflow expectations. |
| `copilot-instructions.md` | GitHub Copilot custom instructions for the stack and conventions. |
| CI workflows | Automated checks that future AI contributions should respect. |
| Issue templates | Structured requests for features, bugs, chores, and AI-ready work intake. |
| Stack-specific guidance | Conventions mined from project files and PR review patterns. |

## Procedure

1. Tell the user to add or update the external skill from inside Copilot CLI:

   ```text
   /skills add johnpapa/ai-ready
   ```

   Re-running the command updates the skill in the user's personal skills directory.

2. Remind the user to review the installed skill before loading it:

   ```bash
   head -20 ~/.copilot/skills/ai-ready/SKILL.md
   ```

3. After the user confirms review and installation, tell them to reload skills:

   ```text
   /skills reload
   ```

4. Tell the user to invoke the installed skill with:

   ```text
   make this repo ai-ready
   ```

5. Do not run `/skills add johnpapa/ai-ready`, `/skills reload`, or repository-modifying AI-ready actions on the user's behalf. The user must run the installation and decide when to load the external skill.

## Limits

- Do not replicate the full external `ai-ready` instructions here; use this wrapper to keep discovery current while the upstream skill evolves.
- Do not create or edit `AGENTS.md`, `copilot-instructions.md`, CI workflows, or issue templates from this wrapper alone.
- Do not claim the installed skill has been reviewed unless the user confirms it.

## Output template

````markdown
## ai-ready handoff

**Status:** installation instructions provided | awaiting user install | ready to invoke external skill
**Source of truth:** `johnpapa/ai-ready`

### Commands for the user
```text
/skills add johnpapa/ai-ready
/skills reload
make this repo ai-ready
```

### Review command
```bash
head -20 ~/.copilot/skills/ai-ready/SKILL.md
```

### Notes
- Re-run `/skills add johnpapa/ai-ready` to update the skill.
- The user must run installation and review commands themselves.
````

## Quality gate

- [ ] The user is told that `https://github.com/johnpapa/ai-ready` is the source of truth.
- [ ] The `/skills add johnpapa/ai-ready` command is shown exactly.
- [ ] The review command `head -20 ~/.copilot/skills/ai-ready/SKILL.md` is shown exactly.
- [ ] The `/skills reload` and `make this repo ai-ready` follow-up commands are shown.
- [ ] The skill does not run installation or repository-modifying commands on the user's behalf.
- [ ] The response makes clear that re-running the add command updates to the latest version.

## References

- [John Papa](https://github.com/johnpapa)
- [johnpapa/ai-ready](https://github.com/johnpapa/ai-ready)
