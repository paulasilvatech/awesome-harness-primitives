---
name: memory-merger
description: >-
  Merge mature lessons from a domain memory instruction file into the matching long-lived
  instruction file while preserving applyTo coverage and removing merged memory sections. Use when
  the user invokes /memory-merger, asks to merge domain memories, consolidate instruction
  memories, or move workspace/user memory into instructions.
---

<!-- Generated from harness/github-copilot/plugins/copilot-customization-authoring/skills/memory-merger/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Memory merger

Consolidate a domain-specific memory file into its durable instruction file by parsing the requested domain and scope, proposing candidate memories, merging approved content without knowledge loss, and cleaning up the memory source.

## When to invoke

- "/memory-merger >prompt-engineering"
- "/memory-merger >clojure workspace"
- "Merge my git-workflow memories into instructions."
- "Consolidate the workspace memory file for this domain."
- "Move mature lessons from the memory instructions into the main instructions."

## Inputs

Use `$ARGUMENTS` as `/memory-merger >domain-name [scope]`.

| Argument | Required | Accepted values | Meaning |
| --- | --- | --- | --- |
| `>domain-name` | Yes | Any domain slug such as `>clojure`, `>git-workflow`, `>prompt-engineering` | Selects `{domain}-memory.instructions.md` and `{domain}.instructions.md`. |
| `[scope]` | No | `global`, `user`, `workspace`, `ws` | Selects where to read and write instruction files. Defaults to `global`. |

Reject input that lacks `>domain-name`. Normalize the domain by removing the leading `>` only when constructing paths.

## Scope mapping

| Scope input | Canonical scope | Memory file | Instruction file |
| --- | --- | --- | --- |
| omitted | `global` | `<global-prompts>/{domain}-memory.instructions.md` | `<global-prompts>/{domain}.instructions.md` |
| `global` | `global` | `<global-prompts>/{domain}-memory.instructions.md` | `<global-prompts>/{domain}.instructions.md` |
| `user` | `global` | `<global-prompts>/{domain}-memory.instructions.md` | `<global-prompts>/{domain}.instructions.md` |
| `workspace` | `workspace` | `<workspace-instructions>/{domain}-memory.instructions.md` | `<workspace-instructions>/{domain}.instructions.md` |
| `ws` | `workspace` | `<workspace-instructions>/{domain}-memory.instructions.md` | `<workspace-instructions>/{domain}.instructions.md` |

`<global-prompts>` means `vscode-userdata:/User/prompts/`. `<workspace-instructions>` means `<workspace-root>/.github/instructions/`.

## Procedure

1. Parse `>domain-name` and `[scope]`; default scope to `global`.
2. Resolve the memory and instruction paths from the scope mapping.
3. Read the memory file; it must exist. Read the instruction file if present.
4. If the memory file is missing, glob the chosen directory for nearby `{domain}` matches. If exactly one likely match exists, use it; if multiple plausible matches exist, ask the user to choose.
5. Inventory every memory section: headline, details, examples, file patterns, and likely destination in the instruction file.
6. Present the proposal and stop for approval before editing.
7. After approval, define the quality bar, draft the merged instruction content, evaluate it, and iterate until it reaches the quality bar.
8. Create or update the instruction file. If creating it, include valid instruction frontmatter.
9. Merge `applyTo` patterns from both memory and instruction files when both exist, preserving comprehensive coverage without duplicates.
10. Remove only the merged sections from the memory file; leave skipped or unapproved memories intact.

## Proposal format

Show every candidate before changing files:

```markdown
## Proposed Memories for Merger

### Memory: <headline>
**Content:** <key points, examples, and constraints>
**Location:** <target section in {domain}.instructions.md>
**Disposition:** merge | skip candidate | needs clarification
```

Then say exactly: `Please review these memories. Approve all with 'go' or specify which to skip.` Stop and wait.

## Merge quality bar

| Criterion | 10/10 requirement |
| --- | --- |
| Zero knowledge loss | Every detail, example, nuance, command, path, pattern, and exception from approved memories survives. |
| Minimal redundancy | Overlapping guidance is consolidated once without deleting meaning. |
| Maximum scannability | Headings, lists, parallel structure, and selective bold text make the result easy to scan. |
| Frontmatter integrity | `applyTo` patterns from both files are merged and deduplicated. |
| Safe cleanup | The memory file loses only sections that were actually merged and approved. |

## Gotchas

- **Do not edit before approval**: the proposal step is an intentional checkpoint; stop after presenting candidate memories.
- **Do not treat missing instruction files as blockers**: create `{domain}.instructions.md` with proper frontmatter when only `{domain}-memory.instructions.md` exists.
- **Do not delete skipped memory sections**: memory cleanup applies only to approved and merged content.
- **Do not collapse `global` and `workspace` paths**: they have different lifetimes and storage locations.

Compatibility literals preserved from legacy invocations: `/memory-merger >prompt-engineering`, `/memory-merger >clojure workspace`, `/memory-merger >git-workflow ws`, `clojure-memory`, `STOP`, `STOPS`, ` (default), `, ` where scope is `, `, or `.

## Output template

```markdown
## Memory merger result

**Status:** proposed | merged | blocked
**Domain:** `<domain>`
**Scope:** `global | workspace`

### Files
- Memory: `<resolved {domain}-memory.instructions.md path>`
- Instructions: `<resolved {domain}.instructions.md path>`

### Proposed or merged memories
| Memory | Location | Disposition |
| --- | --- | --- |
| `<headline>` | `<target section>` | `merged | skipped | pending approval` |

### Validation
- Knowledge loss check: `<pass/fail and evidence>`
- Redundancy check: `<pass/fail and evidence>`
- `applyTo` merge: `<not needed/pass/fail>`
```

## Quality gate

- [ ] `$ARGUMENTS` was parsed as `/memory-merger >domain-name [scope]`.
- [ ] Scope aliases `global`, `user`, `workspace`, and `ws` resolved to the correct paths.
- [ ] The memory file was read, or a typo recovery glob was performed before blocking.
- [ ] Every memory section was proposed before any file edit.
- [ ] User approval was received before updating files.
- [ ] Approved memories were merged with zero knowledge loss and minimal redundancy.
- [ ] `applyTo` patterns were merged without duplicates when both files had frontmatter.
- [ ] Only merged sections were removed from `{domain}-memory.instructions.md`.
