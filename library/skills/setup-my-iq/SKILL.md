---
name: "setup-my-iq"
description: >-
  Create, set up, or update the personal context portfolio: structured markdown files describing who
  you are, how you work, your teams, and your tool/ADO configuration. Runs the interview workflow for
  first-time setup and targeted edits for updates. Trigger this skill when the user asks to: set up
  their context, create or update their context portfolio, "create my IQ", "set up my IQ", edit their
  profile, add/remove a stakeholder, update ADO config, change team info, update pillars, or set up
  any plugin configuration. Trigger when another skill fails to find context (missing files or TODO
  markers) and needs context populated. Also trigger when the user mentions a context change in
  passing (e.g., "my manager changed", "we added someone to the team") to offer a context file update.
  Do NOT trigger for read-only questions like "who's on my team?" or "what's my ADO config?". Those
  are answered directly from the context files referenced in the loaded custom instructions; no skill
  is needed.
---
# Setup My IQ: Create and Update Context Portfolio

Create and maintain the personal context portfolio: a set of structured markdown
files that represent who you are, how you work, and what matters to you. The files
can live anywhere on disk (OneDrive folder, a git repo, a local directory, etc.).
What ties them into the agent is a pointer in one of the user's custom instructions
files (`AGENTS.md`, `copilot-instructions.md`, `CLAUDE.md`, or any `*.instructions.md`
that the host loads into the session).

## How This Skill Works

When invoked, determine the current state and take the right action.

### Discovering existing context

Scan the session for references to the files this skill creates. The host has
already merged all relevant custom instructions files into the session:
`AGENTS.md` (workspace or user-scope), `copilot-instructions.md`,
`CLAUDE.md`, any `*.instructions.md` file, and similar host-specific equivalents.
It doesn't matter which file the pointer came from, just look for the filenames:

- `identity.md`
- `role-and-responsibilities.md`
- `team.md`
- `tools-systems-and-config.md`
- `communication-style.md`
- `preferences-and-constraints.md`

For each, find an `@<absolute-path>` (or equivalent path reference) anywhere in
the loaded instruction text. That's the file's location. Don't rely on the label
or variable name next to the path: users may name pointers differently
(`identityProfile`, `me`, `who-i-am`, etc.). Match on the filename at the end
of the path.

For each filename, classify as:

- **NOT REFERENCED** — no path to this filename is loaded in the session.
- **REFERENCED, FILE MISSING** — a path is loaded but the file doesn't exist on disk.
- **PRESENT** — path is loaded and the file exists. Read it to check for placeholders.

If the six filenames are in mixed states, handle them in this priority order:
first create any NOT REFERENCED files via the interview, then fill REFERENCED,
FILE MISSING entries, then fix incomplete fields in PRESENT files. Summarize
the combined state to the user before starting so they know what to expect.

Concrete example. Suppose `identity.md` and `team.md` are PRESENT and
complete, `tools-systems-and-config.md` is PRESENT but has TODO placeholders
in the ADO section, `role-and-responsibilities.md` and `communication-style.md`
are REFERENCED but the files don't exist on disk, and
`preferences-and-constraints.md` is NOT REFERENCED. The skill should tell the
user: "You have identity and team done. Tools-config has gaps. Role and
communication-style are referenced but missing. Preferences isn't set up at
all. I'll interview you for preferences first, then create role and
communication-style, then fill the gaps in tools-config. OK?"

### 1. No context files referenced
None of the expected filenames appear anywhere in the loaded instructions.
Treat this as first-time setup. Run **First-Time Setup** below.

### 2. Some files referenced but missing on disk
The user started setup previously and didn't finish, or paths exist without
files behind them. **Resume where they left off:**
- List which files exist and which are missing.
- Tell the user: "You have {existing files}. Still need: {missing files}. Want to
  pick up where you left off?"
- When choosing the next file to interview for, the priority order from
  *Discovering existing context* still applies. Within a tie, use this
  default sequence: identity -> role -> team -> tools -> communication-style
  -> preferences-and-constraints.

### 3. Files exist but have incomplete fields

Files exist but some contain unfilled placeholder values. **Fill gaps:**

- Scan all referenced files for any of these incomplete-field patterns:
  - `<!-- TODO -->` — explicit placeholder
  - HTML comments of the form `<!-- ... -->` used as stand-in values
    (e.g., `<!-- your name -->`, `<!-- org name -->`, `<!-- manager name -->`)
  - Any table cell or field whose only content is an HTML comment
- List the gaps: "I found incomplete fields in {files}. Want to fill them in?"
- For each gap, ask the specific question for that field (not the full interview).
- Update the file in place with the user's answer.

### 4. Files are complete, user wants to update
The user asked to change something, or mentioned a context change in passing
(e.g., "my manager changed", "we hired someone new", "I moved to a different
team"). **Targeted update:**
- If the user mentioned the change in passing during another task, offer: "It
  sounds like your {file} may need updating. Want me to fix that now?"
- If the user explicitly asked, proceed directly.
- Read the file from the path resolved in *Discovering existing context*.
- Make the edit and confirm with the user.

### 5. Files are complete, user wants a full refresh
The user wants to redo a file from scratch. Re-run the interview for that
specific file following the same steps as first-time setup.

---

## First-Time Setup

All `assets/...` paths in this skill are relative to this SKILL.md's
directory. Use your file-read tool to load the bundled templates from those
paths. If for some reason a template isn't readable, fall back to the field
structure shown in the example walkthrough at the bottom of this file.

### 1. Choose context directory

Ask: "Where should your context files live? Anywhere persistent works: a synced
cloud folder (OneDrive, Dropbox, iCloud), a local directory, or a git repo. Just
pick a path you can find again later."

- Create the directory if it doesn't exist.
- Store the path for later steps.
- On macOS or Linux, suggest `~/my-iq-context` or `~/OneDrive/my-iq-context` as
  defaults. Substitute `$HOME` for `%USERPROFILE%` in any path the skill
  produces later.

### 2. Begin the interview

Introduce the process:

"I'm going to interview you and produce your personal context portfolio: a set
of markdown files that represent who you are, how you work, and what matters
to you. Any AI skill, agent, or plugin can read these files and immediately
understand what it's working with.

We'll go one file at a time. I'll ask you questions, draft the file, and then
ask you to tell me what I got wrong. You can skip any file you don't want
right now. Ready to start?"

### 3. Pre-fill factual fields from available data sources

**This step is MANDATORY before asking any interview questions.** Do not skip
it, even if you expect it to return nothing.

Before asking the user anything, attempt to gather factual data from whatever
connected sources your environment provides. The user should never have to
type information a connected system already knows.

**What to look for (per file):**

| File | Factual fields to pre-fill |
|------|---------------------------|
| `identity.md` | Name, role/title, organization, team, manager |
| `role-and-responsibilities.md` | Teams supported, cadences (from calendar), reporting line |
| `team.md` | Direct reports, frequent collaborators, org chart data |
| `tools-systems-and-config.md` | ADO org/project/team/area path, repos, tools in use |
| `communication-style.md` | Writing samples from mail/docs (ask permission first) |
| `preferences-and-constraints.md` | No pre-fill (these are subjective boundaries) |

**How to execute:**

1. Check what data sources are available in your environment (work profile,
   directory, calendar, ADO, mail, etc.). Use only sources already authorized.
2. Query them for the relevant factual fields for the file you're about to
   interview for.
3. Present findings as a proposal: "I pulled some information from your work
   profile. Here's what I found -- confirm or correct before we continue."
4. Mark each value as auto-filled so the user knows what came from a system
   vs. what you're asking them to provide.
5. Only after the pre-fill proposal is confirmed (or if no sources are
   available), proceed to ask the remaining questions.

**If no data sources are available:** State that explicitly ("I don't have
access to a work profile or directory in this environment, so I'll ask you
directly") and proceed to the interview questions. Do not silently skip this
step.

See the full rules and constraints in the *Pre-fill from available data
sources before asking* section under Interview Rules.

### 4. Interview for identity.md

Load the template from `assets/templates/identity.md` in this skill bundle for
the file structure.

**First: apply step 3 (pre-fill).** Query available sources for name, role,
org, team, and manager. Present any findings for confirmation. Then proceed
to the questions below for fields not covered by pre-fill.

Open-ended questions to ask (these always need the user):

- If you had to explain what you actually do to someone at a dinner party, what would you say?
- What do people come to you for?

Factual questions to ask only if pre-fill didn't cover them:

- What's your name and current role?
- What organization or company are you with?
- What team are you on?
- Who's your manager?

Once you have enough to draft (don't keep asking past that point), draft the
file. Present it with the reaction pass (see Interview Rules below). Revise,
then write to the context directory.

Transition: "That's identity done. Next is role-and-responsibilities, which
captures what your weeks actually look like. Ready?"
## Extended reference

Additional detailed guidance was moved to [references/extended-guide.md](references/extended-guide.md) to keep this skill within the progressive-disclosure budget.

