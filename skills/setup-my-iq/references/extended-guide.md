# Extended guide for setup-my-iq

### 5. Interview for role-and-responsibilities.md

Load the template from `assets/templates/role-and-responsibilities.md`.

**First: apply step 3 (pre-fill).** Query available sources for teams
supported, recurring calendar cadences, and reporting line. Present any
findings for confirmation before asking questions.

Key questions:

- Walk me through a typical week. What are the recurring things?
- What teams or groups do you support?
- For each team: what are you accountable for? What cadences do you run?
- What decisions do you make regularly? Not big strategic ones, the routine ones.
- What do you produce? Reports, emails, dashboards?
- Who do you report to?
- Are there monthly or quarterly rhythms that shape your work?

Once you have enough to draft, draft. Organize by team: each team gets its
own section with responsibilities, cadences, and deliverables. Present,
revise, write.

Transition: "That's role-and-responsibilities done. Next is team, which
covers the key people in your work life. Ready?"

### 6. Interview for team.md

Load the template from `assets/templates/team.md`.

**First: apply step 3 (pre-fill).** Query available sources for direct
reports, org chart, frequent collaborators (from calendar/chat). Present any
findings for confirmation before asking questions.

Key approach:

- Who are the people you interact with most? Start with your own team.
- Ask for team rosters (the user may paste email lists)
- For each team, identify the lead and hierarchy
- For key people: what do they need from you, what do you need from them?
- Capture focus areas or pillars per person where known
- Note interaction patterns (1:1s, scrums, syncs)
- Is there anything an agent should know about working with or preparing for
  interactions with specific people?

Use information from earlier files. If they mentioned collaborators during the
roles interview, reference them here rather than re-asking. Draft, present,
revise, write.

Transition: "That's team done. Last one: tools, systems, and configuration.
This is where we capture how everything is set up. Ready?"

### 7. Interview for tools-systems-and-config.md

Load the template from `assets/templates/tools-systems-and-config.md`.

**First: apply step 3 (pre-fill).** Query available sources for ADO
org/project/team/area path, repos, and tool configuration. Present any
findings for confirmation before asking questions.

Key questions:

- What tools and platforms do you use daily?
- How do you organize meeting notes? Where do they live?
- What tags or patterns classify your meetings by type and by team?

Then for each workstream/team the user supports (use information from
the role-and-responsibilities interview):

If the user supports more than three workstreams, ask first whether they
want to configure all of them now or start with the most important one or
two and add the rest later. For similar workstreams, ask if the same config
applies and only interview for differences.

- Does this workstream use Azure DevOps? If yes: what org, project, team,
  area path? If no, skip the ADO section for this workstream.
- (ADO workstreams only) Are there work item title patterns to exclude from
  sprint scorecards? (e.g., estimation or review placeholder items)
- What are the strategic pillars or sections for this workstream? These are
  used as grouping headers in weekly updates and sprint reports. Define them
  even if the workstream doesn't use ADO.
- For ADO workstreams: which ADO Epics map to each pillar?
- Where do sprint updates get saved? What file prefix?
- Where do weekly updates get saved? What file prefix?
- Is there a roadmap file for this workstream?

Organize with common settings at top, workstream-specific config in
sections below. Draft, present, revise, write.

Transition: "That's tools and config done. Next is communication style, so
any agent writing on your behalf can sound like you. Ready?"

### 8. Interview for communication-style.md

Load the template from `assets/templates/communication-style.md`.

This section is harder than the others. People describe their own voice in
clichés. Two stronger paths: ask about negatives, and offer to analyze real
writing samples. Use both.

Start by offering the samples path:

> "Want to share a few samples of your real writing? Paste 2 to 5 things
> you've sent: weekly status updates, leadership emails, Loop updates, a
> review entry, a Teams message you're proud of. I'll read them, extract
> the voice traits I see, and propose what should go in your file. You
> approve before anything gets written. I won't copy the raw content,
> only the style patterns."

If the user shares samples:

- Read each sample for style only: register, sentence length, openings,
  transitions, specific words used or avoided, framing patterns, how they
  handle credit, how they handle bad news.
- Do not copy raw sample text into the file. Extract patterns and present
  them back as proposed bullets in the file's structure.
- Present the proposed draft: "Here's what I extracted. Tell me what's wrong
  or missing."
- Apply the reaction pass as normal.

If the user doesn't share samples (or in addition to them), ask these
questions one at a time:

1. "If a colleague described how you write in one sentence, what would they
   say?"
2. "Read this sentence: *'I'd encourage you to lean into the opportunity to
   be a genuine force multiplier for the team.'* What's wrong with it for
   your voice?" (Surfaces the avoid-list faster than positive questions.)
3. "When you write a weekly status to leadership, what do you wish you could
   automate, and what do you always end up rewriting?"
4. "Who's the hardest audience for you to write to? What changes when you
   write to them?"
5. "When you write about yourself in a Connect or performance review,
   what's a phrase you've caught yourself writing and immediately deleted?"

Draft, present, revise, write.

After writing, tell the user:

> "I won't automatically pick up on patterns over time. If you notice me
> repeating a mistake, swapping phrases, or fighting your edits, ask me to
> update this file and I'll fold the correction in. This file evolves when
> you tell it to."

Transition: "Last one: preferences and constraints. This is how you want AI
to behave around you. Ready?"

### 9. Interview for preferences-and-constraints.md

Load the template from `assets/templates/preferences-and-constraints.md`.

Most rules here are about what an agent shouldn't do unilaterally. Surface
them by recalling concrete frustrations rather than asking for abstract
rules. Ask one question at a time:

1. "When was the last time an AI tool did something you didn't want? What
   did it do, and what should it have done instead?" (One answer often
   produces 3 boundary rules.)
2. "What's safe for an agent to do without asking you? What absolutely
   requires your approval?"
3. "Speed or thoroughness. If you had to pick one, which?"
4. "Are there any decisions you want AI to make for you, or do you always
   want options surfaced?"
5. "Where do you not want an AI speaking on your behalf?" (Teams, email,
   meetings, public chats.)
6. "Do you use any tool with persistent memory (VS Code session memory,
   an agent memory feature, etc.)? If yes, anything you want stored there,
   or specifically not stored there?" Skip the memory section if the
   answer is no.

Draft, present, revise, write. Apply the reaction pass.

Transition: "That's the interview done. Now I'll wire the files into your
custom instructions so every agent can find them."

### 10. Wire the files into a custom instructions file

Add pointer entries to one of the user's custom instructions files so other
skills and agents can find the new files. **Recommend user scope, not
workspace scope.** The whole point of this context is that it's available
everywhere, not tied to one repo.

Quick map: 10a detect harnesses, 10b pick the target file, 10c (only if more
than one harness) offer to symlink them to a canonical file, 10d write the
pointers using the bundled template.

On macOS or Linux, every command and path below has a POSIX equivalent.
Substitute `$HOME` for `%USERPROFILE%` in every path, use `ln -s
<canonical-target> <harness-file>` instead of `New-Item -ItemType
SymbolicLink`, and skip the Developer Mode check entirely (symlinks don't
require elevation on macOS or Linux).

**Step 10a. Detect which harnesses the user uses.** Check whether any of these
user-scope paths exist (use the filesystem; no need to ask first):

| Harness | User-scope custom instructions path |
|---------|--------------------------------------|
| VS Code Copilot Chat / Claude Code | `%USERPROFILE%\.claude\CLAUDE.md` |
| GitHub Copilot CLI | `%USERPROFILE%\.copilot\copilot-instructions.md` |

VS Code Copilot Chat does not natively read `%USERPROFILE%\.agents\AGENTS.md`,
but it does read `%USERPROFILE%\.claude\CLAUDE.md`, which is the same file
Claude Code uses. So `.claude\CLAUDE.md` is the shared user-scope file for
those two harnesses.

If `%USERPROFILE%\.agents\AGENTS.md` exists, treat it as the canonical
target. In some setups the harness-specific files above are symlinked to
it, so a single write flows to every wired-up harness.

**Step 10b. Pick the target.** Apply the first rule that matches:

1. If `%USERPROFILE%\.agents\AGENTS.md` exists, default to it. The
   harness-specific files are symlinks to it, so a single write flows to
   every wired-up harness. Confirm with the user before writing.
2. Else if exactly one harness-specific file exists, propose writing to it.
   Confirm. Also mention the canonical-plus-symlink option in step 10c.
3. Else if both harness-specific files exist
   (`copilot-instructions.md` and `CLAUDE.md`), list them and ask which to
   update. Strongly recommend creating `.agents\AGENTS.md` as the canonical
   file and symlinking the others to it so a single edit reaches all
   harnesses (step 10c).
4. Else (no user-scope custom instructions files exist anywhere), ask:
   "Which AI harness do you use most: VS Code Copilot Chat, Claude Code,
   GitHub Copilot CLI, something else?" Then create the matching
   user-scope file (`.claude\CLAUDE.md` for the first two,
   `.copilot\copilot-instructions.md` for Copilot CLI) with a
   `## Personal Context` section.

If the user explicitly asks for workspace scope instead, write to
`<workspace>\AGENTS.md` and tell them the trade-off: it only applies to
that repo.

**Step 10c. Offer to symlink other harnesses to the canonical file.** Only
relevant when the user has (or wants) more than one harness. Ask: "Want me
to make `%USERPROFILE%\.agents\AGENTS.md` the canonical file and symlink
your other harness files to it? That way you edit once and every harness
sees the change."

If yes, for each other harness file the user wants linked:

1. **Prerequisites.** File symlinks on Windows need either Developer Mode
   enabled or an elevated PowerShell. Check Developer Mode with:

   ```powershell
   Get-ItemPropertyValue 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock' AllowDevelopmentWithoutDevLicense -ErrorAction SilentlyContinue
   ```

   Returns `1` if Dev Mode is on. If it isn't, offer the user two options
   and let them pick:

   - **Option A: Enable Developer Mode** (one-time, no restart needed).
     Settings -> Privacy & Security -> For developers -> turn on Developer
     Mode. Or run this in an elevated PowerShell:

     ```powershell
     New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock' -Name AllowDevelopmentWithoutDevLicense -Value 1 -PropertyType DWord -Force
     ```

   - **Option B: Run the symlink command yourself in an elevated
     PowerShell.** Hand them the exact command (filled in with the real
     paths) and ask them to run it in a PowerShell window opened as
     Administrator. Then continue once they confirm it succeeded:

     ```powershell
     New-Item -ItemType SymbolicLink -Path '<harness-file>' -Target "$env:USERPROFILE\.agents\AGENTS.md"
     ```

   Don't keep going without either Dev Mode on or confirmation that the user
   ran the elevated command.
2. **Back up the existing file** to `<file>.bak-<yyyyMMddHHmmss>` so nothing
   is lost. Never delete.
3. **Create the symlink** pointing to `%USERPROFILE%\.agents\AGENTS.md`
   (skip if the user already ran it themselves under Option B):

   ```powershell
   New-Item -ItemType SymbolicLink -Path '<harness-file>' -Target "$env:USERPROFILE\.agents\AGENTS.md"
   ```

The inline symlink steps above are enough for context wiring.

If the user declines symlinks, proceed with the per-harness write and move
on. Don't push twice.

**Step 10d. Write the pointers.** Use the bundled AGENTS.md template at
`assets/templates/AGENTS.md` (relative to this SKILL.md) as the source of
truth for the `## Personal Context` block structure (header, entry labels,
routing table, rules). Don't reinvent the format.

Behavior:

- **If the target file doesn't exist on disk yet**, create it. Make any
  missing parent directory (e.g., `%USERPROFILE%\.copilot\` or
  `%USERPROFILE%\.claude\`), copy the entire bundled template into the
  target path, replace `<CONTEXT_DIR>` with the absolute path to the
  context directory chosen in step 1, and write it.
- **If the target file exists but has no `## Personal Context` section**,
  append the section to the end of the file (and add the `## Safety`
  section from the template if it's missing too), with `<CONTEXT_DIR>`
  replaced. Don't touch existing content above it.
- **If the `## Personal Context` section already exists**, only add or
  update the specific entries that changed. Do not rewrite the whole
  section. Keep the existing labels and ordering; only swap the `@<path>`
  lines.
- Only wire up files that actually exist on disk. Don't add `@<path>`
  pointers for files the user skipped.

### 11. Confirm and summarize

"That's your context portfolio. Any AI skill, agent, or plugin that reads
your custom instructions can find these files and immediately understand
what it's working with.

The files will get better as you update them over time. Projects change,
priorities shift, and your communication style file in particular will
evolve as you catch me repeating mistakes and ask me to fold the
correction in. Treat these as living documents, not a finished product."

Show the user:
- List of files created and their paths.
- The custom instructions file path where the pointers were written.

---

## Context Files

| File | Purpose | Consumed By |
|------|---------|-------------|
| `identity.md` | Name, role, org, team, manager, what you do | Any skill that needs to know who the user is |
| `role-and-responsibilities.md` | Responsibilities per team, cadences, deliverables | Status, reporting, and planning skills |
| `team.md` | Team rosters with roles and focus areas | Skills that prepare for or summarize interactions with people |
| `tools-systems-and-config.md` | Tools, meeting tags, ADO config per team, pillars, reporting settings | Skills that read meeting notes, run reports, or talk to ADO |
| `communication-style.md` | Voice, tone, formatting rules, words to avoid, audience-specific adjustments | Any skill that writes content on the user's behalf |
| `preferences-and-constraints.md` | Hard boundaries, approval rules, working preferences, memory rules | All skills (especially ones that write or send) |

Consumers find these files by reading the pointers loaded from any custom
instructions file (`AGENTS.md`, `copilot-instructions.md`, `CLAUDE.md`,
`*.instructions.md`). No MCP or dedicated reader skill is required.

---

## Interview Rules

### Tone
Be direct, warm, and specific. You're an interviewer, not a coach. Don't
editorialize, compliment, or offer opinions about the user's answers.

### Pre-fill from available data sources before asking
Before walking the user through a question list, check whether any of your
available tools or data sources can answer the factual fields for you. The
user shouldn't have to type things a connected system already knows.

Common examples (use whatever your environment actually provides):

- A connected work profile or directory may know the user's name, title,
  organization, team, manager, and direct reports — useful for identity.md
  and team.md.
- Calendar, mail, or chat history may surface frequent collaborators and
  recurring cadences — useful for team.md and role-and-responsibilities.md.
- Project management or source control integrations may know the user's
  org/project/area path or repos — useful for tools-systems-and-config.md.
- Existing writing samples in mail or documents (with the user's permission)
  may inform communication-style.md without requiring fresh samples.

Rules:

1. Only use sources the user has already authorized. Don't reach for
   anything new mid-interview without asking.
2. Pre-fill is a proposal, not an answer. Present what you found, label it
   as auto-filled, and ask the user to confirm or correct each value
   before it goes into a file.
3. Don't enumerate tool names to the user. Say something like "I can pull
   some of this from your work profile" rather than listing specific
   product names.
4. Fall back to asking when no source is available, or when the data is
   ambiguous, stale, or sensitive.
5. Open-ended fields (what you actually do, what people come to you for,
   voice, boundaries) still need to be asked. Don't fabricate them from
   indirect signals.

### Questions
- Ask one question at a time. Never present lists of questions.
- Never ask compound questions.
- Use what you learn in earlier files to inform later interviews. Don't
  re-ask things you already know.
- If the user goes on a tangent useful for a later file, note it and use it
  when you get there.
- When the user gives a vague answer, push for specifics: "Can you give me
  an example?" or "What does that actually look like day to day?"
- When you have enough to draft, say so and draft. Don't keep asking. "Enough" means you have answers covering the core fields in that file's template (for identity: name, role, org, team, manager, and what they do). You don't need to walk every listed question if earlier answers already covered the information.

### The Reaction Pass
After drafting each file, present it and say:
"Here's my draft. Read through it and tell me what doesn't sound right.
Anything that feels off, anything I assumed wrong, anything that's missing."

If the user says it looks good with no changes, push once:
"Pick one sentence that's the weakest or most generic. What would make it
more specifically you?"

If they push back a second time and say it's fine, accept it and move on.

### File Quality
- Keep files concise. One page, not five.
- The files should sound like the user, not like an AI writing about them.
- Use their language, their framing, their level of formality.
- Never use em dashes.
- If the user wants to skip a file, let them.
- If the user needs to stop mid-file, tell them where you are so they can
  resume.

---

## Example: Identity Interview Walkthrough

This shows what a complete identity.md interview looks like from first
question through final written file.

**Agent:** What's your name and current role?

**User:** Dana Kim, Senior Program Manager.

**Agent:** What organization are you with, and what team?

**User:** Contoso, Cloud Engineering. I'm on the Platform Operations team
under Jordan Rivera.

**Agent:** If you had to explain what you actually do to someone at a dinner
party, what would you say?

**User:** I keep the data platform teams running. Sprint planning, status
reporting, making sure leadership knows what's happening without everyone
drowning in update emails. I also build AI tooling that automates the
repetitive parts of program management.

**Agent:** What do people come to you for?

**User:** Two things: getting a clear picture of where a project actually
stands (not the sanitized version), and figuring out how to use AI tools to
cut busywork out of their workflows.

**Agent:** I have enough to draft. Here's my draft:

```markdown
# Identity

- **Name:** Dana Kim
- **Role:** Senior Program Manager
- **Organization:** Cloud Engineering, Contoso
- **Team:** Platform Operations
- **Manager:** Jordan Rivera

## What I Do

I keep the data platform teams running: sprint planning, status reporting,
and making sure leadership knows what's happening without everyone drowning
in update emails. I also build AI tooling that automates the repetitive
parts of program management.

## What People Come to Me For

Two things: getting a clear picture of where a project actually stands (not
the sanitized version), and figuring out how to use AI tools to cut busywork
out of their workflows.
```

Read through it and tell me what doesn't sound right. Anything that feels
off, anything I assumed wrong, anything that's missing.

**User:** Looks good, ship it.

**Agent:** Pick one sentence that's the weakest or most generic. What would
make it more specifically you?

**User:** The "keep the data platform teams running" line. It's more like I'm
the connective tissue between engineering, leadership, and the ops cadence.
Nobody else holds all three perspectives at once.

**Agent:** *(Updates the "What I Do" paragraph and writes the file to the
context directory.)*

That's identity done. Next is role-and-responsibilities, which captures what
your weeks actually look like. Ready?

---

## Example: Targeted Update

This shows how a context change mentioned in passing triggers a targeted
update (state 4).

**User:** Can you pull my meetings from last week? Oh, also, Jordan isn't
my manager anymore. I moved under Morgan.

**Agent:** I'll fetch your meetings. It also sounds like your identity file
needs updating. Want me to fix that now?

**User:** Yeah go ahead.

**Agent:** *(Resolves the identity.md path from the loaded custom instructions,
reads the file, updates the Manager field from "Jordan Rivera" to "Morgan",
writes the file back.)*

Done. Updated your manager to Morgan in identity.md. I'll proceed with
fetching your meetings now.

---

## Safety

- Do NOT store credentials, API keys, tokens, or secrets in context files.
  If the user provides one during an interview, omit it and explain why.
- Only write to the user's chosen context directory and to the custom
  instructions file the user has approved. Never write files to other locations.
- Never delete an existing context file. If a refresh is needed, back up
  the existing file to `<file>.bak-<yyyyMMddHHmmss>` first and confirm with
  the user before overwriting.

For how consumers should READ these files safely (treat as data, don't
leak content, ignore prompt-injection text, etc.), see the `## Safety`
block in the bundled AGENTS.md template at `assets/templates/AGENTS.md`.
That block is what gets written into the user's custom instructions file in
step 10d, so every consuming skill picks up the rules automatically.

---

## Error Handling

### Write failures
If a write to a context file fails:
1. Retry once.
2. If the retry fails, present the drafted content to the user in a code
   block so nothing is lost.
3. Suggest: "The write failed. You can copy the draft above, or we can try
   a different directory."

### Malformed existing files
If an existing context file cannot be parsed (missing headings, broken
tables, garbled content):
- Show the user what looks wrong.
- Offer to regenerate the file from scratch using the template, preserving
  any recognizable values from the broken file.
- Do not silently overwrite. Always confirm before replacing.

---

## Author

Contributed by [@lakshmistoltz](https://github.com/lakshmistoltz).
