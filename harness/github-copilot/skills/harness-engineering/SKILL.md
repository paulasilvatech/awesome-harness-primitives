---
name: "harness-engineering"
description: >-
  Adopt or review repository-level harness engineering for GitHub Copilot and coding agents. Use when users want durable agent instructions, guardrails, regression checks, drift checks, failure memory, or adoption reports that prevent repeated AI coding-agent mistakes in a target repository.
---

# Harness engineering

Turn repeated coding-agent mistakes into durable repository artifacts by combining instructions, constraints, feedback, memory, evaluation, and governance into a small, evidence-backed harness.

## When to invoke

- "Make this repository more reliable for GitHub Copilot."
- "Add durable agent instructions and guardrails."
- "Prevent this coding-agent mistake from happening again."
- "Add drift checks for our project rules."
- "Review or refresh our existing agent harness."

## Harness model

```text
Harness = Instructions + Constraints + Feedback + Memory + Evaluation + Governance
```

| Principle | Apply it |
| --- | --- |
| Source of truth | Treat the target repository as authoritative for stack, package manager, CI, docs, naming, and architecture. |
| Inspect before editing | Read existing guidance before adding new guidance. |
| Smallest useful harness | Update existing files before creating duplicates. |
| Enforce when practical | Turn high-value rules into tests, linters, type checks, CI, pre-commit hooks, or drift scripts. |
| Manual where safer | Use review points when automation would be brittle or misleading. |
| Failure memory | Record high-risk failures and name the check or review point that prevents recurrence. |
| No template dumping | Adapt every artifact to evidence in the target repository. |

## Discovery evidence

Read these files and folders when they exist, then summarize the stack, entry points, commands, conventions, failures, and unenforced rules:

- `README.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.github/instructions/`
- `.github/workflows/`
- `CONTRIBUTING.md`
- `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, or `build.gradle`
- `docs/`
- `scripts/`
- existing tests and CI checks

## Adoption workflow

1. Choose the harness surface that fits the target repository.
2. Write target-specific agent instructions.
3. Add enforceable checks for high-value rules.
4. Record failure memory for high-risk or recurring failures.
5. Add drift checks for guidance that can silently become stale.
6. Report the adoption with evidence, assumptions, and follow-up.

| Need | Preferred artifact |
| --- | --- |
| Always-on agent behavior | `AGENTS.md` or `.github/copilot-instructions.md` |
| File-scoped guidance | `.github/instructions/*.instructions.md` |
| Recurring project checks | `scripts/check_*.py`, shell scripts, or package scripts |
| CI enforcement | Existing workflow files or a small new workflow |
| Known failures | `docs/failures/*.md` |
| Architecture or process decisions | `docs/decisions/*.md` |
| Adoption evidence | `docs/harness/adoption-report.md` or similar |

Agent instructions must cover project purpose, ownership boundaries, setup, test, lint, build, verification commands, package manager rules, dependency rules, safe editing rules, generated file rules, forbidden paths, testing expectations, PR or commit conventions, and how to record new failures or decisions. Avoid broad personality guidance and rules that cannot be checked or reviewed.

## Enforceable checks and failure memory

Good checks are narrow, fast, named clearly, documented with the rule they protect, and runnable locally or in CI.

```text
Rule: Do not edit generated API clients.
Check: script scans diffs for generated paths and fails with a clear message.

Rule: Every failure memory note names a regression check.
Check: script validates docs/failures/*.md for a "Detection" section.

Rule: Profile docs and templates must stay aligned.
Check: test compares profile README files to expected template files.
```

Create `docs/failures/<slug>.md` for user-visible, high-risk, or recurring failures unless an existing note already covers the root cause:

```markdown
# Short Failure Title

## Summary
What failed, who saw it, and why it matters.

## Root Cause
The technical or process cause. Avoid blame.

## Prevention
Instruction, test, drift check, CI gate, fixture, or manual review point that prevents or detects recurrence.

## Evidence
Links to issue, PR, test, log, command output, or file paths.
```

If automation is unsafe, record the manual review point and why automation would mislead.

## Drift checks and review criteria

Use drift checks when guidance can silently become stale: docs mention removed commands, profile snippets diverge from generated examples, failure notes omit regression checks, decision records are missing for structural changes, or CI references stale scripts or package commands. Prefer the repository's existing language; if there is no convention, Python with only the standard library is a portable default.

When reviewing harness changes, take an opposing perspective and report findings first, ordered by severity, with file and line references when available. Look for generic copied rules, duplicate or conflicting instruction files, broad checks with false positives, unenforced high-risk rules, missing failure memory, generated docs not refreshed, CI gates that skip relevant checks, and harness defaults overwriting target conventions. Do not modify files during review unless explicitly asked.

## Limits

- Do not use this skill for ordinary feature implementation unless the user asks to improve the repository's agent operating environment.
- Do not copy generic templates without repository evidence.
- Do not create duplicate harness surfaces when an equivalent location already exists.

## Optional external reference use

The prompt-first harness workflow at `https://github.com/baskduf/harness-starter-kit` is optional reference material only when the user asks for it or the target repository already uses it. Do not let that reference override repository evidence.

## Output template

```markdown
## Harness engineering report

**Status:** adopted | reviewed | blocked
**Repository inspected:** <path or repository>

### Evidence reviewed
- <file or folder>: <fact learned>

### Harness changes or findings
| Area | Artifact | Rule or finding | Enforcement |
| --- | --- | --- | --- |
| Instructions | `<path>` | <target-specific rule> | <check, CI, or manual review point> |

### Validation
- `<command or review>`: <pass, fail, or not run with reason>

### Follow-up
- <assumption, skipped failure memory reason, or next check>
```

## Quality gate

- [ ] The target repository was inspected before edits or review conclusions.
- [ ] New or changed guidance is specific to repository evidence.
- [ ] High-value rules have checks, CI gates, or documented manual review points.
- [ ] Failure memory was created when required, or the report explains why it was skipped.
- [ ] Generated docs or indexes were refreshed when affected.
- [ ] The final report names every command run and its result.
- [ ] Review output lists findings by severity and does not edit files unless requested.

## References

- [Harness starter kit](https://github.com/baskduf/harness-starter-kit)
