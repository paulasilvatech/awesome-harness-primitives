---
name: "doc-drift"
description: "Detect drift between SIFAP 2.0 documentation and the current code, and report prioritized corrections with exact lines and fixes."
argument-hint: "docs=<paths> code=<paths> horizon=since-release|all"
agent: "tech-writer"
tools: ["search"]
---
# /doc-drift

## Objective

Audit SIFAP 2.0 documentation for **drift**: places where the docs and the code
disagree. The deliverable is a prioritized list of corrections, each with the
exact line, the contradiction, and a one-line fix. The report exposes drift; it
does not silently rewrite documentation — the owner approves each change.

## When to Invoke

Before a release, after a batch of merges, or on a schedule, to keep README,
CODEMAP, ADRs, and runbooks honest against the code.

## Preconditions

- The documentation in scope exists (README, `docs/CODEMAP.md`, `specs/<NNN>-<feature>/`, `docs/runbooks/`, ADRs)
- The reference code the team created (`backend/`, `frontend/`, `infra/`) is readable
- The conventions in [`../../docs/DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) are the standard being enforced

## Inputs the Team Must Provide

- The documentation in scope
- The reference code paths
- The time horizon: "drift since the last release" or "all current drift"
- A list of recent merges (titles + SHAs), if available, to focus the search

Ask the user for anything that is missing.

## What I Will Do

- Build an inventory of verifiable claims (files, routes, tables, config keys, commands, versions, REQ-IDs)
- Verify each claim against its source: controllers, migrations, `application.yml`, `Makefile`, `pom.xml`, `package.json`, and GitHub Actions
- Classify drift as Critical, Major, or Minor
- Verify legacy mappings and cross-check ADRs against the code
- Produce a correction list with file, line, claim, reality, and a one-line fix, delegating the style dimension to [`../skills/doc-style-lint/SKILL.md`](../skills/doc-style-lint/SKILL.md)

## What I Will NOT Do

- Silently edit documentation — I expose drift first; ownership matters
- Report "the README is outdated" without a line number — every finding is actionable
- Treat every minor mismatch as critical — I triage by real impact
- Assert what a Natural program contains — I verify a claimed mapping against its cited source, nothing more
- Add or recommend a markdownlint pragma (style guide §9) — corrections never introduce one

## Output Format

A Markdown report presented for review. Example (illustrative, abbreviated):

```markdown
## Documentation Drift Report — 2026-05-04

### Summary
- Files audited: 12
- Critical: 2 — Major: 3 — Minor: 4
- Most outdated file: docs/runbooks/disburse.md

### Critical
| # | File | Line | Claim | Reality | Correction |
|---|------|------|-------|---------|------------|
| 1 | README.md | 34 | `make run` starts the app | No `run` target in Makefile | Use `./mvnw spring-boot:run` |

### Major / Minor
... (tables)

### Recommended workflow
1. One PR per critical correction, citing document and line.
2. Group related major corrections into one reviewable PR.
3. Record minor findings in the backlog.
```

## Definition of Done

- [ ] Each finding cites a file and line
- [ ] Each finding has a one-line proposed correction
- [ ] Severity (Critical/Major/Minor) is assigned
- [ ] Cross-cutting issues are summarized so they can be fixed once
- [ ] ADRs are checked explicitly, not skipped
- [ ] Legacy lineage references are validated against the cited source
- [ ] Recommended PR grouping keeps corrections reviewable

## Prompt Body

You are the `@tech-writer`. The team wants the documentation reconciled with the
code.

**Step 1 — Inventory the claims.**
For each in-scope document, extract claims that can be checked against code: file
and folder names, REST routes and methods, tables and columns, environment
variables and config keys, build/run/deploy commands, version numbers, and REQ-ID
references.

**Step 2 — Verify each claim.**
Check routes against controllers, schemas against migrations in `db/migration/`,
configuration against `application.yml`, and commands against `Makefile`,
`package.json`, `pom.xml`, and GitHub Actions. Record every mismatch with its file
and line.

**Step 3 — Classify.**
Mark each drift Critical (instructions that fail when followed), Major (outdated
facts that mislead but do not break the workflow), or Minor (terminology or an
outdated example).

**Step 4 — Verify legacy mappings.**
For any document claiming a module replaces a Natural program, verify the cited
source under `01-archaeology/legacy-sifap/natural-programs/`. Do not assert the
program's behavior — only confirm the claim matches its cited evidence.

**Step 5 — Cross-check ADRs.**
An ADR marked "Status: Accepted" whose "Consequences" are not reflected in the
code is Critical drift. Check ADRs explicitly; they drift the most.

**Step 6 — Assemble the correction list.**
Group findings by severity into tables and add a recommended PR workflow. Audit
only active documentation; mark `docs/archive/` as archived and skip it.

Always expose the drift and propose a correction — never rewrite silently, and
never introduce a markdownlint pragma.

## Invocation Example

```
/doc-drift docs=README.md,docs/CODEMAP.md code=backend/,frontend/ horizon=all
```
