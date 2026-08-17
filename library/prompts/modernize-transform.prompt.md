---
description: "Transform one legacy module at a time into modernized code with behavior-pinning tests."
agent: agent
argument-hint: "legacy module and target stack"
source: "code-modernization-plugin modernize-transform, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin/commands/modernize-transform.md"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Modernize Transform

Transform `${input:target:legacy module and target stack}`.

## First step

Load `code-modernization` before editing code. Confirm the legacy source remains read-only unless the user explicitly requests otherwise.

## Steps

1. Read the relevant brief, assessment, rules, map, and design artifacts.
2. Select one bounded legacy module or behavior slice.
3. Use the `Modernization Test Engineer` agent to define behavior-pinning tests.
4. Implement the modernized module under `modernized/**`.
5. Run available tests and compare behavior against legacy evidence or recorded cases.

## Output

Output concisely: return only changed files, tests run, behavior equivalence evidence, validation status, and blockers.