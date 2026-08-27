---
name: remember
description: >-
  Transform lessons learned into domain-organized memory instructions for global or workspace
  scope. Use this skill when the user says /remember, asks to save a workflow lesson, records
  repeated mistakes, documents shortcuts or commands, discovers effective workflows, or wants
  durable VS Code memory instructions.
---

<!-- Generated from harness/github-copilot/plugins/copilot-customization-authoring/skills/remember/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Memory keeper

Turn a user-provided lesson into succinct, reusable, domain-organized memory instructions stored in the correct global or workspace instruction file.

## When to invoke

- "/remember >shell-scripting use POSIX syntax in shared scripts"
- "Remember this workflow lesson globally."
- "Save this project-specific testing convention."
- "We keep forgetting this command; store it."
- "Add this reusable problem-solving pattern to memory."

## Inputs

Use `$ARGUMENTS` as the `/remember` command body. Parse it with this syntax:

```text
/remember [>domain-name [scope]] lesson content
```

| Part | Required | Meaning |
| --- | --- | --- |
| `>domain-name` | No | Explicit memory domain, for example `>clojure` or `>git-workflow`. |
| `scope` | No | `global`, `user`, `workspace`, or `ws`; default is `global`. |
| `lesson content` | Yes | The lesson to turn into reusable instructions. |

Examples:

```text
/remember >shell-scripting now we've forgotten about using fish syntax too many times
/remember >clojure prefer passing maps over parameter lists
/remember avoid over-escaping
/remember >clojure workspace prefer threading macros for readability
/remember >testing ws use setup/teardown functions
```

## Scope and storage

| Scope | Aliases | Destination |
| --- | --- | --- |
| Global | `global`, `user` | `<global-prompts>`: `vscode-userdata:/User/prompts/` |
| Workspace | `workspace`, `ws` | `<workspace-instructions>`: `<workspace-root>/.github/instructions/` |

Default to global scope. Throughout this skill, `<global-prompts>` and `<workspace-instructions>` mean these directories.

## Memory file structure

| Part | Rule |
| --- | --- |
| Description frontmatter | Keep descriptions general and focused on the domain responsibility. |
| ApplyTo frontmatter | Use a few broad glob patterns relevant to the domain; target directories for general domains and file extensions for language-specific domains. |
| Main headline | Use `# <Domain Name> Memory`. |
| Tag line | Add a succinct tagline describing the domain's value. |
| Learnings | Give each distinct lesson its own level 2 headline. |

## Procedure

1. Parse domain, scope, and lesson content from `$ARGUMENTS`.
2. Find existing memory and instruction files to understand domain structure:
   - Global: `<global-prompts>/memory.instructions.md`, `<global-prompts>/*-memory.instructions.md`, and `<global-prompts>/*.instructions.md`.
   - Workspace: `<workspace-instructions>/memory.instructions.md`, `<workspace-instructions>/*-memory.instructions.md`, and `<workspace-instructions>/*.instructions.md`.
3. Analyze the lesson and recent chat context for the reusable pattern.
4. Categorize the learning as a gotcha/common mistake, enhancement to an existing section, new best practice, or process improvement.
5. Determine target domain and path:
   - Explicit domain: use it unless it appears to be a typo, then request human input.
   - Universal global learning: `<global-prompts>/memory.instructions.md`.
   - Universal workspace learning: `<workspace-instructions>/memory.instructions.md`.
   - Domain-specific global learning: `<global-prompts>/{domain}-memory.instructions.md`.
   - Domain-specific workspace learning: `<workspace-instructions>/{domain}-memory.instructions.md`.
6. Read the target domain file and nearby memory files before editing to avoid redundancy.
7. Update an existing section or create a new domain memory file following the required structure.
8. Write succinct, clear, actionable instructions that generalize beyond the specific incident.
9. Report the updated path and the new or revised lesson headline.

Use a todo list to track progress and keep the user informed when the host supports todo tracking.

## Writing guidelines

| Guideline | Apply it by |
| --- | --- |
| Generalize beyond specifics | Extract a reusable pattern instead of preserving task-only details. |
| Be concrete | Include commands or code examples when they make the lesson actionable. |
| Prefer positive phrasing | State what to do rather than only what to avoid. |
| Keep it succinct | Write scannable instructions, not a transcript. |
| Remove redundancy | Merge with existing guidance when the domain file already covers the point. |
| Capture durable value | Store coding style, workflow, critical paths, tool usage, and reusable problem-solving approaches. |

## Update triggers

Common scenarios that warrant memory updates include repeatedly forgetting the same shortcuts or commands, discovering effective workflows, learning domain-specific best practices, finding reusable problem-solving approaches, making coding style decisions with rationale, and identifying cross-project patterns that work well.

## Gotchas

- **Scope changes persistence:** global memory applies to all VS Code projects, while workspace memory applies only to the current repository.
- **Domain typos create clutter:** when an explicit `>domain-name` looks accidental, request clarification instead of creating a near-duplicate domain.
- **Specific incidents should become general rules:** future assistants need reusable guidance, not a narrative of the current task.

## Legacy syntax compatibility

Also accept the compact syntax `/remember [>domain [scope]] lesson clue`, where `[scope]` is optional. Preserve examples such as `/remember >clojure prefer passing maps over parameter lists`, `/remember avoid over-escaping`, and `/remember >testing ws use setup/teardown functions` when teaching usage. The knowledge base should remain self-organizing, domain-driven, and useful for hard-won lessons without becoming task-specific. When documenting old paths, recognize `vscode-userdata:/User/prompts/*-memory.instructions.md` and `User/prompts/*-memory.instructions.md` as global memory file patterns. The memory-file-structure anchor in older docs maps to the Memory file structure section here.

## Output template

```markdown
## Memory update result

**Status:** updated | needs clarification | blocked
**Scope:** global | workspace
**Domain:** `<domain>`
**Path:** `<memory file path>`

### Lesson stored
## <Lesson headline>
<succinct actionable instruction that generalizes the user's lesson>

### Validation
- Existing memories checked for redundancy: pass | fail
- Target file structure valid: pass | fail
- `applyTo` frontmatter reviewed: pass | fail
```

## Quality gate

- [ ] `$ARGUMENTS` was parsed for domain, scope, and lesson content.
- [ ] Existing memory files were discovered before choosing the target path.
- [ ] The target scope is correct: global/user or workspace/ws.
- [ ] The stored lesson is reusable, concise, and actionable.
- [ ] Existing memory was updated instead of duplicated when a matching lesson existed.
- [ ] New memory files follow the required frontmatter, H1, tagline, and level 2 learning structure.
- [ ] The final report names the updated path and lesson headline.
