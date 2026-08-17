---
name: 'Session Auto Commit'
description: 'Automatically commits and pushes repository changes at session end when explicitly enabled.'
tags: ['git', 'sessionEnd']
---

# Session Auto Commit

Stages, commits, and attempts to push outstanding changes when a session ends.

## Events

- `sessionEnd`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/session-auto-commit.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/session-auto-commit/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/session-auto-commit/hooks.json` to `~/.copilot/hooks/session-auto-commit.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `SKIP_AUTO_COMMIT=true` disables it

## Safety posture

This hook mutates repository history and may push to a remote. The repo-level `.github/hooks/session-auto-commit.json` ships with `disableAllHooks: true`; enable it only in repositories where automatic commits and pushes are desired. It exits 0 on skips/failures so it does not block the session.
