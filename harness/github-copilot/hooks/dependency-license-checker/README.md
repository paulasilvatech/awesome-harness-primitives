---
name: 'Dependency License Checker'
description: 'Warns or blocks on newly added dependencies with restricted licenses at session end.'
tags: ['compliance', 'licenses', 'sessionEnd']
---

# Dependency License Checker

Scans dependency manifest diffs and checks licenses for newly added packages.

## Events

- `sessionEnd`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/dependency-license-checker.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/dependency-license-checker/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/dependency-license-checker/hooks.json` to `~/.copilot/hooks/dependency-license-checker.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `LICENSE_MODE=warn|block` (default in manifests: `warn`)
- `BLOCKED_LICENSES` comma-separated SPDX identifiers
- `LICENSE_ALLOWLIST` comma-separated package names
- `LICENSE_LOG_DIR` (default: `logs/copilot/license-checker`)
- `SKIP_LICENSE_CHECK=true` disables it

## Safety posture

Repo-level hook is enabled in warn mode. It does not modify files and skips cleanly outside git repositories. Set `LICENSE_MODE=block` only when you want license violations to stop the session with exit 2.
