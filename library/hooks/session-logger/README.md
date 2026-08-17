---
name: 'Session Logger'
description: 'Logs basic Copilot session lifecycle events and prompt submissions.'
tags: ['logging', 'sessionStart', 'sessionEnd', 'userPromptSubmitted']
---

# Session Logger

Logs session start/end and prompt-submitted event metadata. It does not write prompt content or tool payloads to logs.

## Events

- `sessionStart`
- `sessionEnd`
- `userPromptSubmitted`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/session-logger.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/session-logger/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/session-logger/hooks.json` to `~/.copilot/hooks/session-logger.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `LOG_LEVEL` for prompt event log level (default in manifest: `INFO`)
- `SKIP_LOGGING=true` disables it

## Safety posture

Repo-level hook is enabled. It writes minimal local logs under `logs/copilot` and exits 0; it never blocks.
