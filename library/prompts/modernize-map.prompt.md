---
description: "Map legacy modules to target architecture boundaries, data flows, and migration sequence."
agent: agent
argument-hint: "legacy system folder and target architecture"
source: "code-modernization-plugin modernize-map, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin/commands/modernize-map.md"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Modernize Map

Map `${input:target:legacy system folder and target architecture}`.

## First step

Load `code-modernization` before mapping. Use the `Legacy Analyst` agent for source structure and the `Architecture Critic` agent to review the mapping.

## Steps

1. Identify legacy modules, data stores, integrations, and business domains.
2. Map each legacy area to target packages, services, modules, or retained components.
3. Define sequencing, strangler boundaries, data migration checkpoints, and rollback considerations.
4. Write `analysis/<system>/MAP.md` and a diagram artifact such as `analysis/<system>/MAP.mmd`.

## Output

Output concisely: return only artifact paths, key mapping decisions, validation status, and blockers.