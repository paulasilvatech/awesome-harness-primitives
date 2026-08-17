---
description: "Design the target architecture for a modernization while preserving required behavior and naming intentional changes."
agent: agent
argument-hint: "legacy system, rules artifact, map artifact, or target stack"
source: "code-modernization-plugin modernize-reimagine, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin/commands/modernize-reimagine.md"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Modernize Reimagine

Design the target architecture for `${input:target:legacy system, rules artifact, map artifact, or target stack}`.

## First step

Load `code-modernization` before designing. Use the `Architecture Critic` agent to challenge the design before finalizing it.

## Steps

1. Read the brief, assessment, rules, and map artifacts when available.
2. Define target APIs, data model, runtime, deployment model, observability, security, and migration phases.
3. Explicitly list what stays behaviorally identical and what changes intentionally.
4. Write `analysis/<system>/DESIGN.md` and diagram artifacts as needed.

## Output

Output concisely: return only artifact paths, design decisions, intentional behavior changes, validation status, and blockers.