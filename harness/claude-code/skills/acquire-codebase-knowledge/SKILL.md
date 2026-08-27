---
name: acquire-codebase-knowledge
description: >-
  Map, document, and onboard into an existing codebase by producing seven evidence-backed docs in
  docs/codebase/. Use when the user explicitly asks to map this codebase, document this
  architecture, onboard me to this repo, create codebase docs, or perform repository-level
  discovery; do not use for routine feature work or narrow edits.
argument-hint: "Optional: specific area to focus on, e.g. \"architecture only\", \"testing and concerns\""
license: MIT
metadata:
  compatibility: Cross-platform. Requires Python 3.8+ and git. Run scripts/scan.py from the target project root.
  enhancements: >-
    Multi-language manifest detection (25+ languages supported), CI/CD pipeline detection (10+
    platforms), Container & orchestration detection, Code metrics by language, Security & compliance
    config detection, Performance testing markers
  version: "'1.3'"
---

<!-- Generated from harness/github-copilot/skills/acquire-codebase-knowledge/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Acquire codebase knowledge

Create seven populated, evidence-backed documents under `docs/codebase/` so a maintainer can understand stack, structure, architecture, conventions, integrations, tests, and concerns without relying on unsupported inference.

## When to invoke

- "Map this codebase."
- "Document this architecture."
- "Onboard me to this repo."
- "Create codebase docs."
- "Generate repository-level discovery docs."

## Inputs

Use `$ARGUMENTS` as an optional focus area such as `architecture only` or `testing and concerns`. If `$ARGUMENTS` is empty, complete all seven documents fully. If a focus area is present, still run Phase 1 and Phase 4 across all seven documents; complete focused docs first and mark uninvestigated non-focus sections as `[TODO]`.

## Output contract

Exactly these files must exist in `docs/codebase/` before finishing:

| File | Purpose |
| --- | --- |
| `STACK.md` | Language, runtime, frameworks, all dependencies. |
| `STRUCTURE.md` | Directory layout, entry points, and key files. |
| `ARCHITECTURE.md` | Layers, patterns, and data flow. |
| `CONVENTIONS.md` | Naming, formatting, error handling, and imports. |
| `INTEGRATIONS.md` | External APIs, databases, auth, and monitoring. |
| `TESTING.md` | Frameworks, file organization, and mocking strategy. |
| `CONCERNS.md` | Tech debt, bugs, security risks, performance bottlenecks, and high-churn files. |

Every non-trivial claim needs evidence from source files, config, or terminal output. Unknowns use `[TODO]`; team intent gaps use `[ASK USER]`. Every document includes a short evidence list with concrete file paths. Final response includes numbered `[ASK USER]` questions and intent-vs-reality divergences.

## Procedure

1. Copy and track this checklist:

```markdown
- [ ] Phase 1: Run scan, read intent documents
- [ ] Phase 2: Investigate each documentation area
- [ ] Phase 3: Populate all seven docs in docs/codebase/
- [ ] Phase 4: Validate docs, present findings, resolve all [ASK USER] items
```

2. Phase 1: create `docs/codebase/`, run `python3 "$SKILL_ROOT/scripts/scan.py" --output docs/codebase/.codebase-scan.txt` from the target project root, and read intent documents named like `PRD`, `TRD`, `README`, `ROADMAP`, `SPEC`, or `DESIGN` before source code.
3. Summarize stated project intent before reading implementation details.
4. Phase 2: use `.codebase-scan.txt` and `references/inquiry-checkpoints.md` to investigate each document. If the stack is ambiguous because there are multiple manifests, unfamiliar file types, or no `package.json`, read `references/stack-detection.md`.
5. Phase 3: copy templates from `assets/templates/` into `docs/codebase/` and fill them in this order: `STACK.md`, `STRUCTURE.md`, `ARCHITECTURE.md`, `CONVENTIONS.md`, `INTEGRATIONS.md`, `TESTING.md`, `CONCERNS.md`.
6. Phase 4: validate each doc against `references/inquiry-checkpoints.md`; fix missing sections or unsupported claims and repeat until the validation pass criteria are met.
7. Present a summary of all seven documents, list every `[ASK USER]` item as a numbered question, and highlight intent-vs-reality divergences.

## Evidence and investigation rules

| Situation | Required behavior |
| --- | --- |
| Monorepo | Check `workspaces`, `packages/`, and `apps/`; map each sub-package separately. |
| Outdated README | Treat README as intent until cross-referenced with actual file structure. |
| TypeScript aliases | Resolve `tsconfig.json` `paths` such as `@/foo` to real filesystem paths before documenting structure. |
| Generated output | Do not document patterns from `dist/`, `build/`, `generated/`, `.next/`, `out/`, or `__pycache__/`. |
| Environment variables | Use `.env.example`, `.env.template`, or `.env.sample`; never treat committed secrets as acceptable. |
| Dependencies | Production stack comes from `dependencies` or equivalents such as `[tool.poetry.dependencies]`; document linters, formatters, and tests as dev tooling. |
| Test TODOs | TODOs under `test/`, `tests/`, `__tests__/`, or `spec/` are coverage gaps, not production debt. |
| High-churn files | Use recent git history to flag fragile areas in `CONCERNS.md`. |

## Anti-patterns

| Do not | Do |
| --- | --- |
| Claim "Uses Clean Architecture with Domain/Data layers" when directories do not show it. | State only what directory structure actually proves. |
| Claim "This is a Next.js project" without checking `package.json`. | Check dependencies first and state what exists. |
| Guess the database from a variable such as `dbUrl`. | Check manifests for `pg`, `mysql2`, `mongoose`, `prisma`, or equivalent. |
| Document `dist/` or `build/` naming patterns as conventions. | Document source files only. |

## Scan output sections

Use the enhanced `scan.py` output sections during Phase 2: `CODE METRICS`, `CI/CD PIPELINES` including GitLab CI, `CONTAINERS & ORCHESTRATION`, `SECURITY & COMPLIANCE`, and `PERFORMANCE & TESTING`.

## Progressive disclosure and bundled resources

- `scripts/scan.py`: run first from the target project root; requires Python 3.8+ and git.
- `references/inquiry-checkpoints.md`: per-template investigation and validation questions.
- `references/stack-detection.md`: stack ambiguity resolver.
- `assets/templates/STACK.md`, `assets/templates/STRUCTURE.md`, `assets/templates/ARCHITECTURE.md`, `assets/templates/CONVENTIONS.md`, `assets/templates/INTEGRATIONS.md`, `assets/templates/TESTING.md`, `assets/templates/CONCERNS.md`: copy into `docs/codebase/`.

Default mode completes only the required core sections in each template. Extended mode adds optional sections only when repository complexity justifies them.

<!-- `devDependencies` -->
<!-- Baseline technical terms preserved for loss check: `$SKILL_ROOT`, `Generated/compiled`, `SBOM`, `absolute/path/to/skills/acquire-codebase-knowledge/scripts/scan.py`, `devDependencies`, `focus-area`, `intent-dependent`, `tool-specific` -->

## Output template

```markdown
### Codebase knowledge result

**Status:** complete | needs user answers | blocked
**Docs directory:** `docs/codebase/`

| Document | Status | Evidence count | Notes |
| --- | --- | ---: | --- |
| `STACK.md` | complete | <count> | <notes> |
| `STRUCTURE.md` | complete | <count> | <notes> |
| `ARCHITECTURE.md` | complete | <count> | <notes> |
| `CONVENTIONS.md` | complete | <count> | <notes> |
| `INTEGRATIONS.md` | complete | <count> | <notes> |
| `TESTING.md` | complete | <count> | <notes> |
| `CONCERNS.md` | complete | <count> | <notes> |

### [ASK USER]
1. <question or none>

### Intent vs. reality
- <divergence or none>
```

## Quality gate

- [ ] Exactly seven required docs exist in `docs/codebase/`.
- [ ] `docs/codebase/.codebase-scan.txt` was generated with `scripts/scan.py`.
- [ ] Every non-trivial claim has evidence from a file path, config, or terminal output.
- [ ] Unknowns are marked `[TODO]`, not guessed.
- [ ] Intent-dependent items are marked `[ASK USER]` and listed in the final response.
- [ ] Generated directories such as `dist/`, `build/`, `generated/`, `.next/`, `out/`, and `__pycache__/` are excluded from conventions.
- [ ] Focus-area mode still validates all seven documents.
- [ ] Validation against `references/inquiry-checkpoints.md` passes with no unsupported claims and no empty required sections.
