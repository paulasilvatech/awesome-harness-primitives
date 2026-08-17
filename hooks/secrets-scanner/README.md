---
name: 'Secrets Scanner'
description: 'Scans changed files for potential secrets at session end.'
tags: ['security', 'secrets', 'sessionEnd']
---

# Secrets Scanner

Scans changed or staged text files for credential-like patterns and logs only redacted matches.

## Events

- `sessionEnd`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/secrets-scanner.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/secrets-scanner/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/secrets-scanner/hooks.json` to `~/.copilot/hooks/secrets-scanner.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `SCAN_MODE=warn|block` (default in manifests: `warn`)
- `SCAN_SCOPE=diff|staged` (default: `diff`)
- `SECRETS_ALLOWLIST` comma-separated literal fragments
- `SECRETS_LOG_DIR` (default: `logs/copilot/secrets`)
- `SKIP_SECRETS_SCAN=true` disables it

## Safety posture

Repo-level hook is enabled in warn mode. It does not modify files, redacts findings in logs, and skips outside git repositories. Set `SCAN_MODE=block` to block with exit 2 when findings are detected.
