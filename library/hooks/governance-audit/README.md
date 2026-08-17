---
name: 'Governance Audit'
description: 'Logs session governance events and scans user prompts for high-risk instructions.'
tags: ['governance', 'sessionStart', 'sessionEnd', 'userPromptSubmitted']
---

# Governance Audit

Logs session start/end metadata and scans submitted prompts for threat signals without logging full prompt text.

## Events

- `sessionStart`
- `sessionEnd`
- `userPromptSubmitted`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/governance-audit.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/governance-audit/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/governance-audit/hooks.json` to `~/.copilot/hooks/governance-audit.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `GOVERNANCE_LEVEL=open|standard|strict|locked` (default: `standard`)
- `BLOCK_ON_THREAT=true|false` (default in manifests: `false`)
- `SKIP_GOVERNANCE_AUDIT=true` disables it

## Safety posture

Repo-level hook is enabled in standard warn/log mode. It writes governance logs under `logs/copilot/governance` and redacts credential evidence. In strict/locked mode or with `BLOCK_ON_THREAT=true`, threat matches block with exit 2.
