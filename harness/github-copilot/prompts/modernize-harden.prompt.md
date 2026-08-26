---
name: 'modernize-harden'
description: 'Harden a modernized module or system with ranked security, testing, observability, and operations findings.'
agent: 'modernization'
argument-hint: 'modernized folder or module'
---

# /modernize-harden

## Objective

Harden a modernized folder or module by reviewing transformed code for security, behavior drift, error handling, observability, operational readiness, and meaningful test coverage, then producing ranked findings and validation evidence.

## When to Invoke

Use this prompt after `modernize-transform` has produced modernized code under `modernized/**`, before release, migration rollout, or production readiness review.

## Preconditions

- The target modernized folder or module exists.
- Relevant transformation evidence, rules, map, design, and test artifacts are available when they exist.
- Test, build, and static analysis commands are known or discoverable from the repository.
- Writing to `analysis/<system>/HARDENING.md` is permitted.
- The `code-modernization` skill is available.

## Inputs the Team Must Provide

- `target` — the modernized folder or module to harden.
- The system name used for `analysis/<system>/HARDENING.md`.
- Relevant rules, design, transformation evidence, and available commands.
- Ask the user for anything that is missing; stop if the target module cannot be identified.

## What I Will Do

- Load the `code-modernization` skill before reviewing.
- Use `se-security-reviewer` for focused security findings, `critical-thinking` for material design assumptions, and `legacy-characterization-testing` for behavior-drift coverage.
- Review transformed code for security, behavior drift, error handling, observability, and operational readiness.
- Check tests for meaningful assertions and legacy behavior coverage.
- Run available test, build, and static analysis commands.
- Write `analysis/<system>/HARDENING.md` with ranked findings.

## What I Will NOT Do

- Perform broad redesign or new feature implementation while hardening.
- Modify legacy source or unrelated modernized modules.
- Mark behavior as safe without checking it against rules, design, transformation evidence, or recorded cases.
- Hide security, testing, observability, or operations gaps because they are inconvenient.
- Claim commands passed when they were not run or when output is unavailable.

## Output Format

Write `analysis/<system>/HARDENING.md` with this shape:

```markdown
# Hardening Review — <system>

## Scope
- Target:
- Reviewed artifacts:

## Validation Commands
| Command | Result | Notes |
| --- | --- | --- |

## Ranked Findings
| Rank | Severity | Area | Finding | Evidence | Recommendation | Owner |
| --- | --- | --- | --- | --- | --- | --- |

## Security Review
- 

## Behavior Drift Review
- 

## Testing Review
- Meaningful assertions:
- Legacy behavior coverage:

## Error Handling and Observability
- Error handling:
- Logs:
- Metrics:
- Traces:

## Operational Readiness
- Configuration:
- Deployment:
- Runbooks:
- Rollback:

## Blockers
- 
```

## Definition of Done

- [ ] The `code-modernization` skill was loaded before review started.
- [ ] Security, behavior drift, error handling, observability, and operational readiness were reviewed.
- [ ] Tests were checked for meaningful assertions and legacy behavior coverage.
- [ ] Available test, build, and static analysis commands were run or each blocker is named.
- [ ] `analysis/<system>/HARDENING.md` exists with ranked findings.
- [ ] The response returns only artifact paths, commands run, ranked findings, validation status, and blockers.

## Prompt Body

Follow these steps in order. Treat hardening as evidence review plus targeted recommendations.

**Step 1 — Load the modernization workflow.**
Load the `code-modernization` and `legacy-characterization-testing` skills. Use `se-security-reviewer` for focused security findings and `critical-thinking` for material design assumptions when useful.

**Step 2 — Resolve the hardening scope.**
Read `${input:target:modernized folder or module}` and determine the system name for `analysis/<system>/HARDENING.md`.

**Step 3 — Review transformed code.**
Inspect the modernized code for security, behavior drift, error handling, observability, and operational readiness. Compare behavior-sensitive code against rules, design, and transformation evidence where available.

**Step 4 — Review tests.**
Check tests for meaningful assertions and legacy behavior coverage. Flag superficial tests, missing behavior-pinning cases, and untested edge cases.

**Step 5 — Run validation commands.**
Run available test, build, and static analysis commands. Record the exact command, result, and any blocker.

**Step 6 — Rank findings.**
Write ranked findings with severity, area, evidence, recommendation, and owner. Include security, testing, observability, and operations findings when applicable.

**Step 7 — Write the artifact.**
Write `analysis/<system>/HARDENING.md` with the ranked review and validation command evidence.

**Step 8 — Report concisely.**
Return only artifact paths, commands run, ranked findings, validation status, and blockers.

## Invocation Example

```
/modernize-harden target=modernized folder or module
```
