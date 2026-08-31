# Claude Code Catalog - Hooks

Reusable deterministic lifecycle automation packages.

Part of the [Claude Code catalog](../claude-code.md). Generated file: do not
hand-edit it. Regenerate with
`python3 harness/claude-code/scripts/generate_catalog.py`.

## Overview

| Field | Value |
| --- | --- |
| Entries | 8 |
| Generated source | `harness/claude-code/` |

## Entries

| Name | Events | Source |
| --- | --- | --- |
| `attester-import-check` | `PreToolUse` | [source](../../../harness/claude-code/hooks/attester-import-check) |
| `dependency-license-checker` | `SessionEnd` | [source](../../../harness/claude-code/hooks/dependency-license-checker) |
| `fix-broken-links` | `PostToolUse` | [source](../../../harness/claude-code/hooks/fix-broken-links) |
| `governance-audit` | `SessionEnd, SessionStart, UserPromptSubmit` | [source](../../../harness/claude-code/hooks/governance-audit) |
| `secrets-scanner` | `SessionEnd` | [source](../../../harness/claude-code/hooks/secrets-scanner) |
| `session-auto-commit` | `SessionEnd` | [source](../../../harness/claude-code/hooks/session-auto-commit) |
| `session-logger` | `SessionEnd, SessionStart, UserPromptSubmit` | [source](../../../harness/claude-code/hooks/session-logger) |
| `tool-guardian` | `PreToolUse` | [source](../../../harness/claude-code/hooks/tool-guardian) |
