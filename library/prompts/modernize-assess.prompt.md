---
name: 'modernize-assess'
description: 'Assess a legacy system or modernization portfolio with inventory, complexity, dependencies, risks, and modernization recommendations.'
agent: 'agent'
argument-hint: 'system folder, or --portfolio parent folder'
---

# Modernize Assess

Assess `${input:target:system folder, or --portfolio parent folder}`.

## First step

Load the `code-modernization` skill (Agent Skill) before scanning or writing artifacts. Use the `Legacy Analyst`, `Security Auditor`, and `Modernization Test Engineer` agents where useful.

## Steps

1. If target starts with `--portfolio`, assess each immediate system folder and write `analysis/portfolio.html`.
2. Otherwise assess a single system and write `analysis/<system>/ASSESSMENT.md`.
3. Inventory languages, build system, dependencies, tests, data stores, integrations, and runtime entry points.
4. Run available non-destructive inventory tools such as `scc`, `cloc`, or language-specific analyzers.
5. Identify technical debt, security risk, documentation gaps, and modernization pattern.
6. Create an architecture diagram artifact when helpful, for example `analysis/<system>/ARCHITECTURE.mmd`.

## Output

Output concisely: return only artifact paths, commands run, major findings, validation status, and blockers.
