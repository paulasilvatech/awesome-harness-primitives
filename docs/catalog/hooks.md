# Copilot Primitives Catalog — Hooks

Runs deterministic checks or automation at Copilot lifecycle events.

Part of the [Copilot primitives catalog](../../CATALOG.md). Generated file: do not
hand-edit it. Regenerate with `python3 harness/github-copilot/scripts/generate_catalog.py`.

## Overview

| Field | Value |
| --- | --- |
| Primitive type | Hook |
| Entries | 8 |
| Canonical source | `harness/github-copilot/hooks/` |
| Typical use cases | Guardrails, compliance checks, logging, and opt-in session automation. |

## Entries

| Hook package | Description | Trigger events | Use cases | Source |
| --- | --- | --- | --- | --- |
| Attester Import Check | Checks newly introduced Python and JavaScript package imports against attester.dev before tool use. | preToolUse | Typical use: Checks newly introduced Python and JavaScript package imports against attester.dev before tool use. | [manifest](../../harness/github-copilot/hooks/attester-import-check/hooks.json) · [docs](../../harness/github-copilot/hooks/attester-import-check/README.md) |
| Dependency License Checker | Warns or blocks on newly added dependencies with restricted licenses at session end. | sessionEnd | Typical use: Warns or blocks on newly added dependencies with restricted licenses at session end. | [manifest](../../harness/github-copilot/hooks/dependency-license-checker/hooks.json) · [docs](../../harness/github-copilot/hooks/dependency-license-checker/README.md) |
| Fix Broken Links | Checks URLs after editing web/documentation files and can interactively repair broken links. | postToolUse | Typical use: Checks URLs after editing web/documentation files and can interactively repair broken links. | [manifest](../../harness/github-copilot/hooks/fix-broken-links/hooks.json) · [docs](../../harness/github-copilot/hooks/fix-broken-links/README.md) |
| Governance Audit | Logs session governance events and scans user prompts for high-risk instructions. | sessionStart, sessionEnd, userPromptSubmitted | Typical use: Logs session governance events and scans user prompts for high-risk instructions. | [manifest](../../harness/github-copilot/hooks/governance-audit/hooks.json) · [docs](../../harness/github-copilot/hooks/governance-audit/README.md) |
| Secrets Scanner | Scans changed files for potential secrets at session end. | sessionEnd | Typical use: Scans changed files for potential secrets at session end. | [manifest](../../harness/github-copilot/hooks/secrets-scanner/hooks.json) · [docs](../../harness/github-copilot/hooks/secrets-scanner/README.md) |
| Session Auto Commit | Automatically commits and pushes repository changes at session end when explicitly enabled. | sessionEnd | Typical use: Automatically commits and pushes repository changes at session end when explicitly enabled. | [manifest](../../harness/github-copilot/hooks/session-auto-commit/hooks.json) · [docs](../../harness/github-copilot/hooks/session-auto-commit/README.md) |
| Session Logger | Logs basic Copilot session lifecycle events and prompt submissions. | sessionStart, sessionEnd, userPromptSubmitted | Typical use: Logs basic Copilot session lifecycle events and prompt submissions. | [manifest](../../harness/github-copilot/hooks/session-logger/hooks.json) · [docs](../../harness/github-copilot/hooks/session-logger/README.md) |
| Tool Guardian | Detects dangerous preToolUse commands such as destructive deletes, force pushes, and database drops. | preToolUse | Typical use: Detects dangerous preToolUse commands such as destructive deletes, force pushes, and database drops. | [manifest](../../harness/github-copilot/hooks/tool-guardian/hooks.json) · [docs](../../harness/github-copilot/hooks/tool-guardian/README.md) |
