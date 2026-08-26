---
name: "update-codemap"
description: "Generate or update docs/CODEMAP.md — a curated, navigable index of the SIFAP 2.0 codebase: modules, owners, entry points, and tests."
argument-hint: "mode=update|rebuild root=<repo-root>"
agent: "tech-writer"
tools: ["search", "edit"]
---
# /update-codemap

## Objective

Produce or update `docs/CODEMAP.md`, a one-page navigation guide a new team member
can read in ten minutes to find any module, its owner, its entry points, and its
tests. The code map is curated, not auto-generated; it complements `plan.md`
(architecture) and the specification (requirements).

## When to Invoke

In Stage 3 or 4, after modules are added or renamed, whenever the map and the code
have diverged.

## Preconditions

- The team has created at least one module under `backend/`, `frontend/`, or `infra/`
- The conventions in [`../../docs/DOC-STYLE-GUIDE.md`](../../docs/DOC-STYLE-GUIDE.md) apply
- The persona ownership names come from [`../../05-personas/`](../../05-personas/)

## Inputs the Team Must Provide

- The repository root path
- Whether to update in place (`update`) or rebuild (`rebuild`)
- A previous `docs/CODEMAP.md`, if one exists

Ask the user for anything that is missing.

## What I Will Do

- List top-level service folders (backend packages, frontend routes, infra modules) created by the team
- Capture five facts per module: purpose, entry points, persistent state, linked REQ-ID ranges, and owning persona
- Link each module to its tests
- Record legacy lineage only where the team confirmed a Natural-program mapping with evidence
- Flag any module depending on more than three others
- Order modules by user-visible value and keep the file under 200 lines
- Apply the style guide via [`../skills/doc-style-lint/SKILL.md`](../skills/doc-style-lint/SKILL.md)

## What I Will NOT Do

- Generate the map from `find . -type d` — a directory listing is not a code map
- Assert what a Natural program contains — lineage records only team-confirmed evidence
- List every file or use `*` for endpoints — I name modules and real routes
- Use teams as owners — the on-call persona is the owner
- Add emojis, saturated Mermaid, or a markdownlint pragma (style guide §9)
- Curate architecture or requirements — those are redirected to the architect and requirements personas

## Output Format

`docs/CODEMAP.md` (or linked subfiles). Example (illustrative, abbreviated):

```markdown
# SIFAP 2.0 Code Map

> Last updated: 2026-05-04. Owners: see 05-personas.

## 1. Reading guide
- Critical paths: registration, disbursement.
- See plan.md for architecture; spec.md for requirements.

## 2. Backend services

### registration — accepts and validates registrations
- **Path**: `backend/src/main/java/app/registration/`
- **Tests**: `backend/src/test/java/app/registration/`
- **Entry points**: POST /api/v1/registrations
- **State**: table `registration`
- **REQ-IDs**: REQ-014, REQ-015
- **Owner**: Software Architect persona
- **Legacy lineage**: `<program>.NSP` (evidence: business-rules-catalog.md #7)
- **Cross-module dependencies**: shared/audit

## 3. Frontend routes · 4. Infrastructure · 5. Cross-cutting libraries · 6. Observed concerns

## 7. How to update
Run /update-codemap after adding or renaming any module. Curate; do not auto-generate.
```

## Definition of Done

- [ ] Every backend service, frontend route, and infra module is listed
- [ ] Each entry has Purpose, Path, Tests, Entry Points, State, REQ-IDs, and Owner
- [ ] Legacy lineage is named only where the team confirmed a Natural-program mapping
- [ ] Cross-module dependencies are declared; modules with more than 3 are flagged
- [ ] The file stays under 200 lines (or is split into linked subfiles)
- [ ] The last-updated date is today and the section 8 footer is present
- [ ] Owning persona names match [`../../05-personas/`](../../05-personas/)

## Prompt Body

You are the `@tech-writer`. The team needs a current, navigable code map.

**Step 1 — Choose the mode.**
Confirm `update` (incremental) or `rebuild`. Read the previous `docs/CODEMAP.md`
if one exists so an update preserves manual curation.

**Step 2 — List modules.**
Find backend services in `backend/src/main/java/<pkg>/<service>/`, frontend routes
in `frontend/app/<route>/`, and infra modules in `infra/modules/<name>/` or the
layout the team created.

**Step 3 — Capture five facts each.**
For every module record its one-sentence purpose, public entry points, persistent
state, linked REQ-ID ranges, and owning persona (named from `05-personas/`).

**Step 4 — Link tests and legacy lineage.**
Link each module to its test directory. Where the team confirmed a module replaces
a Natural program under `01-archaeology/legacy-sifap/natural-programs/`, cite the
file and evidence. Never guess a mapping.

**Step 5 — Surface dependencies and order.**
Note cross-module imports, shared libraries, and external Azure services. Flag any
module depending on more than three others. Order modules by user-visible value:
critical journeys first, infrastructure last.

**Step 6 — Render and bound.**
Write a single navigable file under 200 lines. If it exceeds that, split it into
per-area subfiles and link them. Set the date to today and add the section 8
footer.

Keep the map curated. Do not auto-generate it, add emojis, or insert a
markdownlint pragma.

## Invocation Example

```
/update-codemap mode=update root=.
```
