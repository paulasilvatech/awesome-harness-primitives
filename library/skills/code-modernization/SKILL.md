---
name: code-modernization
description: "Guide legacy code modernization with a disciplined GitHub Copilot workflow: brief, assess, map, extract business rules, reimagine architecture, transform modules, and harden with tests and security review. Use for COBOL, JCL, legacy Java, .NET, C++, classic ASP, monolith modernization, behavior-preserving rewrite, business-rule extraction, modernization assessment, or legacy-to-modern transformation."
source: "code-modernization-plugin, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Code Modernization

Use this skill to guide behavior-preserving modernization of legacy systems. The workflow is intentionally staged so the team understands the system before transforming it.

## Workflow

1. **Brief**: define what is being modernized, why now, constraints, non-goals, and success criteria.
2. **Assess**: inventory languages, modules, integrations, build, test coverage, complexity, and risk.
3. **Extract rules**: turn hidden procedural logic into business rule cards with source evidence.
4. **Map**: map legacy modules to target domains, packages, services, and migration sequence.
5. **Reimagine**: design the target API, data model, runtime, and operational model.
6. **Transform**: rewrite module by module under `modernized/**`, with tests that pin legacy behavior.
7. **Harden**: review security, tests, error handling, observability, and deployment readiness.

## GitHub Copilot Primitives

| Need | Primitive |
| --- | --- |
| Deep legacy discovery | `Legacy Analyst` agent |
| Business rule extraction | `Business Rules Extractor` agent |
| Target design review | `Architecture Critic` agent |
| Security hardening | `Security Auditor` agent |
| Characterization tests | `Modernization Test Engineer` agent |
| Repeatable workflow entry points | `/modernize-*` prompts |
| Folder safety rules | `code-modernization.instructions.md` |

## Folder Contract

- `legacy/**`: source evidence and legacy behavior. Read-only by default.
- `analysis/**`: briefs, assessments, maps, rule catalogs, designs, and reports.
- `modernized/**`: transformed or replacement implementation and tests.

## Rules

- Do not transform code before assessment and business-rule extraction.
- Cite source files for findings. If line numbers are unavailable, cite the file and explain why.
- Distinguish observed behavior from inferred intent.
- Prefer multiple focused artifacts over one oversized report.
- Use characterization tests to preserve legacy behavior before intentional behavior changes.
- Do not invent complexity, cost, runtime, or risk metrics. Use measured values or state assumptions.

## Validation

- Run available inventory tools such as `scc`, `cloc`, or language-specific analyzers when present.
- Run available test suites before and after transformation.
- For transformed modules, provide evidence that tests compare or pin legacy behavior.
- For hardening, report findings by severity with concrete remediation.