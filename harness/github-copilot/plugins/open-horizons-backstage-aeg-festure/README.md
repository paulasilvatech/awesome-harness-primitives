# Backstage AI Kit: agents, instructions, hooks, prompts, and tools

Portable AEG integration assets for an existing Backstage portal. Each agent is
a Markdown file with YAML frontmatter (`name`, `description`, `tools`) followed
by the system prompt. Tools are defined by a minimal OpenAPI contract for the
AEG orchestrator. Any chat plugin that supports system prompts plus tool
calling can consume these assets; if your plugin uses a different manifest
format, copy the content 1:1.

## What goes where

| Asset | Destination | Files |
|------|-------------|-------|
| 4 chat agents | Your chat plugin's agent registry | `agents/*.md` |
| Agent tools | Plugin tool configuration through the `/api/proxy/aeg` proxy | `tools/openapi-aeg.yaml` |
| Backstage repository instructions | Root of your Backstage repository | `instructions/CLAUDE.md` and `instructions/copilot-instructions.md` |
| Backstage repository hooks | `.claude/settings.json` in your Backstage repository | `hooks/` |
| Reusable prompts | `.claude/commands/` (Claude Code) and `.github/prompts/` (Copilot) | `prompts/*.md` |
| Generated-project harnesses | Already shipped in the application template skeleton | Do not duplicate them here |

## AEG-native lifecycle and artifacts

This kit is AEG-native. Agents and prompts should refer to the platform
lifecycle and artifacts below.

| Stage | Primary artifacts | What the chat surface should reference |
|------|-------------------|-----------------------------------------|
| N0 | `CONSTITUTION.md` | Run charter, guardrails, and approved scope |
| L1 | `specs/FRD_*.md`, `specs/NFRD_*.md` | Requirement IDs written in EARS notation |
| G1 | Gate package | Human review of scope, assumptions, and requirement risk |
| L2 | `docs/adr/ADR-*.md` | Architecture decisions and rejected alternatives |
| G2 | Gate package | Human review of architecture, ADR coverage, and readiness |
| L3/L4 | `specs/tasks.yaml`, tests, findings | Approved work plan, execution, and loop back-edges |
| G3/G4 | PRs and GitHub environments | Status and deep-links only; approval stays outside chat |
| N5 | `specs/traceability.yaml`, delivery report | Closed requirement-to-resource evidence chain |

Generated applications use engine-specific harnesses under
`backstage/template-aeg-application/skeleton/harness/`, currently including
`claude-code/` and `copilot-cli/`.

## The 4 agents and their boundaries

| Agent | Does | Never does |
|------|------|------------|
| `aeg-concierge` | Refines the need, classifies intent, starts runs, reports status | Decides gates |
| `aeg-gatekeeper` | Presents G1/G2 decision packages and records approve/reject decisions | Self-approves; handles G3/G4 |
| `aeg-analyst` | Answers questions about traceability, metrics, cost, findings, and delivery reports | Mutates run state |
| `aeg-harvester` | Proposes draft stack profiles and golden-path recommendations from completed runs | Publishes without human approval |

## Cross-cutting rules

- The logged-in Backstage identity flows through every tool call
  (`initiated_by`, `decided_by`); the orchestrator enforces roles.
- The chat plugin is a presentation surface, never the source of enforcement.
- Keep prose, comments, messages, and examples in English.
- Do not reintroduce external requirements-tooling terminology into this kit.
