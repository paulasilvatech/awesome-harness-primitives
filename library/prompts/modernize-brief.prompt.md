---
description: "Capture a modernization brief: scope, drivers, constraints, non-goals, risks, and success criteria."
agent: agent
argument-hint: "legacy system folder or modernization initiative"
source: "code-modernization-plugin modernize-brief, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin/commands/modernize-brief.md"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Modernize Brief

Create a modernization brief for `${input:target:legacy system folder or modernization initiative}`.

## First step

Load `code-modernization` before drafting or editing artifacts. Ask only for missing business context that cannot be inferred from files.

## Steps

1. Identify scope, business driver, stakeholders, constraints, non-goals, and success criteria.
2. Record known risks, compliance requirements, data sensitivity, runtime constraints, and timeline.
3. Write `analysis/brief.md` or `analysis/<system>/BRIEF.md`.
4. Include open questions for business and technical owners.

## Output

Output concisely: return only the artifact path, assumptions, open questions, and validation status.