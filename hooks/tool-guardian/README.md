---
name: 'Tool Guardian'
description: 'Detects dangerous preToolUse commands such as destructive deletes, force pushes, and database drops.'
tags: ['security', 'preToolUse']
---

# Tool Guardian

Scans tool input before execution for dangerous command patterns.

## Events

- `preToolUse`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/tool-guardian.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/tool-guardian/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/tool-guardian/hooks.json` to `~/.copilot/hooks/tool-guardian.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `GUARD_MODE=block|warn` (default in manifests: `block`)
- `TOOL_GUARD_ALLOWLIST` comma-separated literal fragments
- `TOOL_GUARD_LOG_DIR` (default: `.github/logs/copilot/tool-guardian`)
- `SKIP_TOOL_GUARD=true` disables it

## Safety posture

This is a blocking guard when enabled. The repo-level `.github/hooks/tool-guardian.json` ships with `disableAllHooks: true` so clones are not blocked by default. Enable it deliberately, or change `GUARD_MODE=warn` for observation-only use. Blocking uses exit 2 and puts the reason on stderr.
