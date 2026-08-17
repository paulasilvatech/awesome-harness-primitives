---
description: "Extract business rules from legacy code into cited, testable rule cards."
agent: agent
argument-hint: "legacy folder, module, or business process"
source: "code-modernization-plugin modernize-extract-rules, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin/commands/modernize-extract-rules.md"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Modernize Extract Rules

Extract business rules from `${input:target:legacy folder, module, or business process}`.

## First step

Load `code-modernization` before extracting rules. Use the `Business Rules Extractor` agent for deep rule mining.

## Steps

1. Locate calculations, validations, eligibility checks, authorizations, policies, and state transitions.
2. Cite each rule with source file evidence.
3. Convert each rule into plain language and Given/When/Then examples with concrete values.
4. Mark confidence and unresolved SME questions.
5. Write `analysis/<system>/RULES.md`.

## Output

Output concisely: return only the artifact path, rule count, low-confidence questions, validation status, and blockers.