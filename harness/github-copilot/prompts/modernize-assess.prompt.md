---
name: 'modernize-assess'
description: 'Assess a legacy system or modernization portfolio with inventory, complexity, dependencies, risks, and modernization recommendations.'
agent: 'modernization'
argument-hint: 'system folder, or --portfolio parent folder'
---

# /modernize-assess

## Objective

Assess a legacy system or modernization portfolio by producing an evidence-based inventory of languages, build systems, dependencies, tests, data stores, integrations, runtime entry points, technical debt, security risk, documentation gaps, modernization pattern, and recommended next steps.

## When to Invoke

Use this prompt after `modernize-brief` exists or enough initiative context is available, and before `modernize-extract-rules`, `modernize-map`, `modernize-reimagine`, `modernize-transform`, and `modernize-harden` rely on system inventory and risk evidence.

## Preconditions

- The target is either one system folder or `--portfolio` followed by a parent folder.
- The workspace contains the legacy source, build files, tests, configuration, or deployment artifacts to inspect.
- Non-destructive inventory commands are allowed when available.
- Writing to `analysis/<system>/ASSESSMENT.md`, `analysis/portfolio.html`, and optional diagram artifacts is permitted.
- The `code-modernization` skill is available.

## Inputs the Team Must Provide

- `target` — a system folder, or `--portfolio parent folder` for portfolio assessment.
- Any existing brief, known business priorities, or modernization constraints.
- Permission boundaries for running non-destructive tools such as `scc`, `cloc`, or language-specific analyzers.
- Ask the user for anything that is missing; stop if the target folder or portfolio root is undefined.

## What I Will Do

- Load the `code-modernization` skill before scanning or writing artifacts.
- Load a product-specific context skill when available, use `natural-adabas-analysis` for Natural/Adabas sources, and use `se-security-reviewer` for a focused security pass when risk warrants it.
- Assess each immediate system folder when the target starts with `--portfolio` and write `analysis/portfolio.html`.
- Assess a single system otherwise and write `analysis/<system>/ASSESSMENT.md`.
- Inventory languages, build system, dependencies, tests, data stores, integrations, and runtime entry points.
- Run available non-destructive inventory tools such as `scc`, `cloc`, or language-specific analyzers.
- Identify technical debt, security risk, documentation gaps, and a modernization pattern.
- Create an architecture diagram artifact when helpful, for example `analysis/<system>/ARCHITECTURE.mmd`.

## What I Will NOT Do

- Modify legacy source code, dependency manifests, runtime configuration, or production data.
- Run destructive commands, migrations, deployments, or commands that require credentials unless explicitly approved.
- Extract detailed rule cards; `modernize-extract-rules` owns `analysis/<system>/RULES.md`.
- Decide the target architecture; `modernize-map` and `modernize-reimagine` own mapping and design.
- Treat tool output as complete when generated files, vendored code, or hidden entry points may need manual review.

## Output Format

Write the applicable artifact shape:

```markdown
# Modernization Assessment — <system>

## Executive Summary
- Modernization pattern:
- Major findings:
- Blockers:

## Inventory
| Area | Evidence | Notes |
| --- | --- | --- |
| Languages |  |  |
| Build system |  |  |
| Dependencies |  |  |
| Tests |  |  |
| Data stores |  |  |
| Integrations |  |  |
| Runtime entry points |  |  |

## Complexity and Risk
| Finding | Category | Severity | Evidence | Recommendation |
| --- | --- | --- | --- | --- |

## Security and Compliance Notes
- 

## Documentation Gaps
- 

## Modernization Recommendations
- 

## Commands Run
| Command | Result | Notes |
| --- | --- | --- |

## Diagram Artifacts
- `analysis/<system>/ARCHITECTURE.mmd`

## Next Handoff
- Use `modernize-extract-rules` for rule mining.
- Use `modernize-map` for architecture boundary mapping.

For portfolio mode, write `analysis/portfolio.html` with one section per immediate system folder and a cross-system risk summary.
```

## Definition of Done

- [ ] The `code-modernization` skill was loaded before assessment work started.
- [ ] `analysis/portfolio.html` exists for `--portfolio`, or `analysis/<system>/ASSESSMENT.md` exists for a single system.
- [ ] Languages, build system, dependencies, tests, data stores, integrations, and runtime entry points are inventoried.
- [ ] Available non-destructive tools such as `scc`, `cloc`, or language-specific analyzers were run, or each unavailable tool is named.
- [ ] Technical debt, security risk, documentation gaps, and modernization pattern are identified with evidence.
- [ ] `analysis/<system>/ARCHITECTURE.mmd` is created when an architecture diagram artifact is helpful.
- [ ] The response returns only artifact paths, commands run, major findings, validation status, and blockers.

## Prompt Body

Follow these steps in order. Keep the assessment evidence-based and non-destructive.

**Step 1 — Load the modernization workflow.**
Load the `code-modernization` skill and any product-specific context skill. Use `natural-adabas-analysis` for Natural/Adabas sources and `se-security-reviewer` for a focused security pass when risk warrants it.

**Step 2 — Resolve assessment mode.**
Read `${input:target:system folder, or --portfolio parent folder}`. If it starts with `--portfolio`, enumerate each immediate system folder under the parent folder. Otherwise assess the single system folder.

**Step 3 — Inventory the system.**
Identify languages, build system, dependencies, tests, data stores, integrations, and runtime entry points from files, manifests, scripts, documentation, and configuration.

**Step 4 — Run non-destructive tooling.**
Run available inventory tools such as `scc`, `cloc`, or language-specific analyzers. Record every command and result. If a tool is unavailable, record that rather than installing new tooling by default.

**Step 5 — Analyze modernization risks.**
Identify technical debt, security risk, documentation gaps, test gaps, dependency risk, runtime risk, and a modernization pattern suitable for the system.

**Step 6 — Create artifacts.**
Write `analysis/portfolio.html` for portfolio mode. Otherwise write `analysis/<system>/ASSESSMENT.md`. Create `analysis/<system>/ARCHITECTURE.mmd` when a diagram clarifies dependencies, runtime entry points, integrations, or data stores.

**Step 7 — Prepare handoffs.**
Point rule mining to `modernize-extract-rules`, boundary mapping to `modernize-map`, design work to `modernize-reimagine`, implementation to `modernize-transform`, and readiness review to `modernize-harden`.

**Step 8 — Report concisely.**
Return only artifact paths, commands run, major findings, validation status, and blockers.

## Invocation Example

```
/modernize-assess target=--portfolio legacy-systems
```
