---
name: setup-my-iq
description: >-
  Create, resume, repair, or update a personal context portfolio of markdown files for identity,
  role, team, tools and ADO config, communication style, preferences, and constraints. Use when
  users ask to set up my IQ, create my IQ, update context files, edit
  profile/team/stakeholder/ADO/pillar information, or when another skill finds missing context
  files or TODO placeholders.
---

<!-- Generated from harness/github-copilot/skills/setup-my-iq/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Setup My IQ

Create and maintain a personal context portfolio by discovering existing file pointers, interviewing only for missing or stale information, pre-filling facts from authorized sources, and writing structured markdown files.

## When to invoke

- "Set up my IQ or create my context portfolio."
- "Update my profile, team, stakeholders, pillars, or ADO config."
- "My manager changed; update my context."
- "Another skill says my context files are missing or have TODO markers."
- "Resume my context setup."

## Prerequisites and context

The portfolio can live in any persistent directory, including OneDrive, Dropbox, iCloud, a local directory, or a git repo. It is connected to agents by an absolute path pointer in a loaded custom instruction file such as `AGENTS.md`, `copilot-instructions.md`, `CLAUDE.md`, or any `*.instructions.md` file loaded by the host.

Expected filenames:

- `identity.md`
- `role-and-responsibilities.md`
- `team.md`
- `tools-systems-and-config.md`
- `communication-style.md`
- `preferences-and-constraints.md`

Use bundled templates from `assets/templates/` for first-time setup. If a template is unreadable, use the structure in `references/extended-guide.md`.

## Discovery and state classification

Scan the loaded instruction text for paths ending in the six expected filenames. Match the filename at the end of an `@<absolute-path>` or equivalent path reference; do not depend on pointer labels such as `identityProfile`, `me`, or `who-i-am`.

| State | Meaning | Action |
| --- | --- | --- |
| `NOT REFERENCED` | No loaded path points to the filename. | Create it through first-time setup. |
| `REFERENCED, FILE MISSING` | A path is loaded but no file exists on disk. | Resume setup for that file at the referenced path. |
| `PRESENT` | Path exists and file exists. | Read it and inspect for placeholders or requested updates. |

If states are mixed, process in this priority order: create `NOT REFERENCED`, fill `REFERENCED, FILE MISSING`, then repair incomplete `PRESENT` files. Within a tie, use `identity.md`, `role-and-responsibilities.md`, `team.md`, `tools-systems-and-config.md`, `communication-style.md`, then `preferences-and-constraints.md`.

Example status summary: "You have identity and team done. Tools-config has gaps. Role and communication-style are referenced but missing. Preferences isn't set up at all. I'll interview you for preferences first, then create role and communication-style, then fill the gaps in tools-config."

## Procedure

1. Discover all six filenames from loaded instruction pointers and classify each state.
2. If no files are referenced, ask where the context files should live; suggest `~/my-iq-context` or `~/OneDrive/my-iq-context` on macOS or Linux and substitute `$HOME` for `%USERPROFILE%` in generated paths.
3. Create the directory if needed.
4. Before asking interview questions for a file, attempt factual pre-fill from authorized data sources such as work profile, directory, calendar, ADO, mail, or docs.
5. Present pre-fill findings as auto-filled proposals and ask the user to confirm or correct them. If no sources are available, say so explicitly and continue.
6. Ask only the questions needed for the current missing, incomplete, or updated fields.
7. Draft the file from the bundled template, show it for a reaction pass, revise, and write it.
8. Move to the next file or targeted update until the requested setup or repair is complete.

## Pre-fill targets and interview rules

| File | Factual pre-fill | Open questions |
| --- | --- | --- |
| `identity.md` | Name, role/title, organization, team, manager. | What do you actually do? What do people come to you for? |
| `role-and-responsibilities.md` | Teams supported, cadences from calendar, reporting line. | What does a typical week look like? What decisions or deliverables are yours? |
| `team.md` | Direct reports, frequent collaborators, org chart data. | How should collaborators be grouped? Who are key stakeholders? |
| `tools-systems-and-config.md` | ADO org/project/team/area path, repos, tools in use. | Which systems matter most? What configuration should agents know? |
| `communication-style.md` | Writing samples from mail or docs, only after permission. | What tone should agents use for you? What should they avoid? |
| `preferences-and-constraints.md` | No pre-fill because boundaries are subjective. | What constraints, defaults, or preferences should agents respect? |

Incomplete-field patterns are `<!-- TODO -->`, any HTML comment used as a stand-in value such as `<!-- your name -->`, and any table cell or field whose only content is an HTML comment.

## Update modes

| Situation | Behavior |
| --- | --- |
| Some files are referenced but missing | List existing and missing files; offer to pick up where the user left off. |
| Files exist with placeholders | List the exact gaps and ask targeted questions for those fields only. |
| Files are complete and user mentions a change in passing | Offer to update the relevant file, for example team or manager information. |
| Files are complete and user explicitly asks for a change | Read the resolved file, edit it in place, and confirm. |
| User asks for a full refresh | Re-run the interview for that specific file. |
| Read-only question such as "who's on my team?" | Answer from context files directly; do not use this skill. |

## Progressive disclosure and bundled resources

- `assets/templates/identity.md`: identity portfolio template.
- `assets/templates/role-and-responsibilities.md`: role and cadence template.
- `assets/templates/team.md`: team and stakeholder template.
- `assets/templates/tools-systems-and-config.md`: tools, systems, ADO, and repository configuration template.
- `assets/templates/communication-style.md`: communication style template.
- `assets/templates/preferences-and-constraints.md`: preferences and constraints template.
- `references/extended-guide.md`: full interview details, reaction pass guidance, and fallback structures.

## Gotchas

- **Pre-fill is mandatory**: attempt authorized factual data lookup before asking any interview questions, even if the result is empty.
- **Filename matching beats variable names**: users may name pointers arbitrarily; match on `identity.md` and the other filenames.
- **Do not silently skip missing sources**: state when work profile, directory, calendar, ADO, or mail access is unavailable.
- **Do not ask the full interview for a placeholder repair**: ask only for the missing field.

## Setup vocabulary

The SKILL package uses `assets/...` paths loaded with the agent's file-read capability. Host instructions may be workspace, user-scope, or host-specific; still match filenames. Treat pre-fill as MANDATORY, including `mail/docs` checks where authorized. Preserve tool/ADO configuration and add/remove stakeholder requests. Do not invoke for read-only questions. Incomplete-field patterns include `<!-- ... -->`, `<!-- org name -->`, and `<!-- manager name -->`. Keep progressive-disclosure by reading bundled references only when needed.

- Preserve exact setup term `incomplete-field` for placeholder repairs.

## Output template

```markdown
## Setup My IQ result

**Status:** created | updated | resumed | needs input | blocked
**Context directory:** `<absolute path or unresolved>`

### Portfolio state
| File | State | Action taken |
| --- | --- | --- |
| `identity.md` | <NOT REFERENCED / REFERENCED, FILE MISSING / PRESENT> | <created, updated, skipped, or needs input> |

### Questions asked
- <targeted question or "none">

### Files written
- `<absolute path>`

### Validation
- Pre-fill attempted: <yes/no and source type>
- Placeholders remaining: <count or unknown>
```

## Quality gate

- [ ] All six expected filenames were searched in loaded instruction pointers.
- [ ] Each file was classified as `NOT REFERENCED`, `REFERENCED, FILE MISSING`, or `PRESENT`.
- [ ] Authorized pre-fill was attempted before interview questions, or unavailable sources were explicitly reported.
- [ ] Templates from `assets/templates/` or fallback structures from `references/extended-guide.md` were used.
- [ ] Existing files were updated in place instead of duplicating context.
- [ ] Placeholder-only fields were detected and repaired with targeted questions.
- [ ] The final report lists files written and any remaining blockers.
