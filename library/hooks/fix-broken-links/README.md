---
name: 'Fix Broken Links'
description: 'Checks URLs after editing web/documentation files and can interactively repair broken links.'
tags: ['links', 'postToolUse']
---

# Fix Broken Links

Checks URLs in files changed by an edit-like tool. With a terminal it can offer replacement/removal choices; without a terminal it reports only.

## Events

- `postToolUse`

## Install

- Repository: copy or use the matching manifest at `.github/hooks/fix-broken-links.json`. Copilot CLI discovers repo hooks from `.github/hooks/*.json`; a bare `hooks/fix-broken-links/hooks.json` is only a package example and is not auto-discovered.
- User: copy `hooks/fix-broken-links/hooks.json` to `~/.copilot/hooks/fix-broken-links.json` and keep this repository path layout or adjust script paths.
- Scripts referenced by the manifest must be executable (`chmod +x`).

## Exit-code and output contract

Copilot hook stdin is JSON. `exit 0` allows the action; `exit 2` blocks and surfaces stderr to the model; any other non-zero exit is a non-blocking hook error. If stdout JSON is emitted, only the Copilot response keys documented in `docs/COPILOT-HARNESS-SPEC.md` are meaningful.

## Environment

- `FIX_BROKEN_LINKS_AGENT` is used internally to prevent recursive Copilot invocations.

## Safety posture

This hook can perform network checks and mutate files during interactive repair. The repo-level `.github/hooks/fix-broken-links.json` ships with `disableAllHooks: true`; enable it only when you want automatic link checking/repair. It exits 0 and does not block tool use.
