---
name: 'Attester Import Check'
description: 'Checks newly introduced Python and JavaScript package imports against attester.dev before tool use.'
tags: ['security', 'supply-chain', 'preToolUse']
---

# Attester Import Check

Checks package imports in proposed tool input before a write/edit tool runs.

## Events

- `preToolUse`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/attester-import-check.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/attester-import-check/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/attester-import-check/hooks.json` to `~/.copilot/hooks/attester-import-check.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `ATTESTER_MODE=block|warn` (default in manifests: `block`)
- `ATTESTER_BASE_URL` (default: `https://attester.dev`)
- `ATTESTER_IMPORT_CHECK_NO_CACHE=1` disables cache

## Safety posture

This is a blocking supply-chain guard when enabled. The repo-level `.github/hooks/attester-import-check.json` ships with `disableAllHooks: true` so clones are not blocked by default; enable it deliberately after accepting the attester.dev network dependency.
