---
name: "audit-context"
description: "Audit the repository's Copilot context surface (AGENTS.md, CODEMAP.md, instructions, prompts, agents) and return prioritized corrections."
argument-hint: "scope=.github"
agent: "tech-lead"
tools: ["read", "search"]
---
# /audit-context

## Objective

Audit the repository's context-engineering surface — `AGENTS.md`, `CODEMAP.md`,
`.github/instructions/*`, `.github/prompts/*`, `.github/agents/*` — and return a
prioritized, actionable list of corrections. Every finding is a real issue with a
concrete fix, sorted by severity.

## When to Invoke

Periodically, before a stage handoff, or after several primitives change, to catch
drift, missing scopes, and stale references.

## Preconditions

- The repository has a `.github/` context surface to audit
- The index files [`../instructions/README.md`](../instructions/README.md) and the [prompts index](README.md) are the reference for expected files and conventions

## Inputs the Team Must Provide

- The scope to audit, if narrower than the whole `.github/` surface (optional)

Ask the user only if the scope is ambiguous.

## What I Will Do

- List every file in `.github/instructions/`, `.github/prompts/`, and `.github/agents/` with line counts
- Check the `applyTo:` scope in each instructions file and flag `**` or a missing scope
- Read `CODEMAP.md` and flag it stale if untouched for 30+ days or referencing deleted files
- Check each prompt/agent frontmatter for an informative `description`, an `agent` that resolves to a real agent, minimal tools, and no pinned model
- Use grep to find stale folder references and broken relative links
- Summarize findings in a severity-sorted table, delegating the audit procedure to [`../skills/context-audit/SKILL.md`](../skills/context-audit/SKILL.md)

## What I Will NOT Do

- Flag anything that is not a real issue — no false positives
- Edit code or context files — I audit and recommend; the owner applies fixes
- Suggest pinning a model or provider — the user chooses the execution context (see [`../../09-cheat-sheets/model-routing.md`](../../09-cheat-sheets/model-routing.md))
- Rewrite the primitives myself — restructuring work is redirected to the owning persona's prompt

## Output Format

A severity-sorted Markdown table plus a top-3 summary. Example (illustrative):

```markdown
## Context audit — 2026-05-04

| File | Issue | Severity | Correction |
|------|-------|----------|------------|
| .github/instructions/frontend.instructions.md | applyTo: "**" too broad | High | Scope to frontend/**/*.{ts,tsx} |
| .github/prompts/persona-dba-tune.prompt.md | description is "TBD" | Medium | Write an imperative one-line description |
| CODEMAP.md | Not updated in 62 days | Medium | Run /update-codemap |

### Top 3 corrections
1. Narrow the frontend instructions scope.
2. Refresh CODEMAP.md.
3. Fix the DBA prompt description.
```

## Definition of Done

- [ ] No false positives — every flagged item is an actual issue
- [ ] Every High-severity item has a concrete correction, not a vague suggestion
- [ ] `CODEMAP.md` freshness is explicitly reported
- [ ] `applyTo` scopes are checked in every instructions file
- [ ] Findings are sorted by severity with a top-3 summary
- [ ] No suggestion edits application code — only context files

## Prompt Body

You are the `@tech-lead`. The team wants the context surface kept healthy.

**Step 1 — Inventory.**
List every file under `.github/instructions/`, `.github/prompts/`, and
`.github/agents/`, with line counts. Compare against the index files to spot
anything missing or undocumented.

**Step 2 — Check instruction scopes.**
Open each `*.instructions.md` and read its `applyTo:`. Flag any file with
`applyTo: "**"` or a missing scope as High severity — broad scopes leak context
into unrelated work.

**Step 3 — Check CODEMAP freshness.**
Read `CODEMAP.md`. Flag it stale if it has not changed in 30+ days or references
files that no longer exist. Report its freshness explicitly, even when healthy.

**Step 4 — Check frontmatter quality.**
For each prompt and agent, verify the `description` is informative (not "TBD"), the
`agent` resolves to a real file in `.github/agents/`, the tool set is minimal, and
no model or provider is pinned.

**Step 5 — Find stale references and broken links.**
Grep for references to renamed or deleted folders and for relative links whose
target is missing. Record each with its file and line.

**Step 6 — Prioritize.**
Summarize findings in a table sorted by severity (High, Medium, Low), each with a
concrete correction, and end with the top three corrections.

Report only real issues. Do not propose editing application code — this audit
covers context files only.

## Invocation Example

```
/audit-context scope=.github
```
