---
description: "Harden a modernized module or system with security review, test audit, error handling, observability, and operational readiness findings."
agent: agent
argument-hint: "modernized folder or module"
source: "code-modernization-plugin modernize-harden, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin/commands/modernize-harden.md"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Modernize Harden

Harden `${input:target:modernized folder or module}`.

## First step

Load `code-modernization` before reviewing. Use the `Security Auditor`, `Architecture Critic`, and `Modernization Test Engineer` agents where useful.

## Steps

1. Review transformed code for security, behavior drift, error handling, observability, and operational readiness.
2. Check tests for meaningful assertions and legacy behavior coverage.
3. Run available test, build, and static analysis commands.
4. Write `analysis/<system>/HARDENING.md` with ranked findings.

## Output

Output concisely: return only artifact paths, commands run, ranked findings, validation status, and blockers.