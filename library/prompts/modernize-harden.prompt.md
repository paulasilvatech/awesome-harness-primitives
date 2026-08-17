---
name: 'modernize-harden'
description: 'Harden a modernized module or system with ranked security, testing, observability, and operations findings.'
agent: 'agent'
argument-hint: 'modernized folder or module'
---

# Modernize Harden

Harden `${input:target:modernized folder or module}`.

## First step

Load the `code-modernization` skill (Agent Skill) before reviewing. Use the `Security Auditor`, `Architecture Critic`, and `Modernization Test Engineer` agents where useful.

## Steps

1. Review transformed code for security, behavior drift, error handling, observability, and operational readiness.
2. Check tests for meaningful assertions and legacy behavior coverage.
3. Run available test, build, and static analysis commands.
4. Write `analysis/<system>/HARDENING.md` with ranked findings.

## Output

Output concisely: return only artifact paths, commands run, ranked findings, validation status, and blockers.
