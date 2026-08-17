---
name: 'modernize-extract-rules'
description: 'Extract cited and testable business rule cards from legacy code, modules, or business processes.'
agent: 'agent'
argument-hint: 'legacy folder, module, or business process'
---

# Modernize Extract Rules

Extract business rules from `${input:target:legacy folder, module, or business process}`.

## First step

Load the `code-modernization` skill (Agent Skill) before extracting rules. Use the `Business Rules Extractor` agent for deep rule mining.

## Steps

1. Locate calculations, validations, eligibility checks, authorizations, policies, and state transitions.
2. Cite each rule with source file evidence.
3. Convert each rule into plain language and Given/When/Then examples with concrete values.
4. Mark confidence and unresolved SME questions.
5. Write `analysis/<system>/RULES.md`.

## Output

Output concisely: return only the artifact path, rule count, low-confidence questions, validation status, and blockers.
