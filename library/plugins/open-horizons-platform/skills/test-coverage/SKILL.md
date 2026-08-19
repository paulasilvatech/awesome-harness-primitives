---
name: test-coverage
description: 'Use when analyzing test coverage, GitHub check runs, PR quality gates, failed tests, coverage regressions, merge readiness, and test improvement recommendations. Produces check-run summaries, coverage findings, severity classification, and actionable test remediation. DO NOT USE FOR: pipeline diagnostics (use pipeline-diagnostics), security review (use @security), deployment orchestration (use @deploy). Triggers include "analyze test coverage", "why are PR checks failing", "review quality gate", and "find coverage gaps".'
---

# Test Coverage

Use this skill to analyze tests, coverage, and PR quality gates using real GitHub Checks and PR evidence. It produces a check summary, coverage risk assessment, failed-test analysis, and targeted recommendations.

> [!NOTE]
> This skill depends on the `gh` CLI, authenticated GitHub access, and repository check-run or PR visibility. It does not use an MCP server by default.

## When to invoke

- "Analyze test coverage for this PR."
- "Why are PR checks failing?"
- "Review merge readiness from checks and reviews."
- "Find coverage gaps introduced by this change."
- "Summarize failed tests from GitHub checks."

## Prerequisites and context

- `gh auth status` succeeds.
- Repository owner/name and PR number, branch, or commit SHA are known.
- Check runs exist for the target ref.
- Coverage artifacts or check output are available if coverage percentage is requested.

## Procedure

### Step 1: Fetch check-run evidence

```bash
gh pr checks <pr-number>
gh api repos/<owner>/<repo>/commits/<ref>/check-runs --jq '.check_runs[] | {name, status, conclusion}'
```

### Step 2: Inspect failed or coverage-related checks

```bash
gh api repos/<owner>/<repo>/check-runs/<check-run-id>
gh pr view <pr-number> --json reviews,commits,statusCheckRollup
```

### Step 3: Classify quality risk

| Severity | Meaning |
| --- | --- |
| Critical | Required test or coverage check failed and blocks merge. |
| High | Coverage regression or repeat test failure on protected branch. |
| Medium | Non-required test failure, flaky test, or missing coverage evidence. |
| Low | Skipped, neutral, cancelled, or informational check. |

### Step 4: Diagnose common patterns

| Pattern | Evidence | Recommendation |
| --- | --- | --- |
| Flaky test | Same test alternates pass and fail | Stabilize timing, test data, and external dependencies. |
| Environment mismatch | CI fails but local pass is reported | Align runtime versions and environment variables. |
| Coverage regression | Coverage below threshold | Add tests for changed branches and error paths. |
| Required check failure | Merge blocked by check policy | Fix the failing check rather than bypassing. |

### Step 5: Escalate when failure is not test-specific

- Use `pipeline-diagnostics` for workflow, dependency install, or build-step failures.
- Use `kubectl-cli` or `helm-cli` for deployment checks that fail inside tests.

## Limits

- Do not use this skill for: pipeline diagnostics (use pipeline-diagnostics), security review (use @security), deployment orchestration (use @deploy).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Check data is unavailable | State the limitation and inspect PR status rollup if available. |
| GitHub auth fails | Ask the operator to run `gh auth login`. |
| Failure is a workflow infrastructure issue | Route to `pipeline-diagnostics`. |
| Coverage report is missing | Report that coverage cannot be quantified and list needed artifact or check name. |
| PR number is ambiguous | List open PRs and ask for the target if multiple match. |

## Output template

Return exactly this structure:

```markdown
## Test Coverage and Quality Report

**Repository:** <owner>/<repo>
**Ref or PR:** <ref-or-pr>
**Severity:** <Critical|High|Medium|Low>

### Check Summary
| Check | Status | Conclusion | Required | Notes |
| --- | --- | --- | --- | --- |
| <check> | <status> | <conclusion> | <yes|no|unknown> | <notes> |

### Coverage Findings
- <finding>

### Recommendations
1. <recommendation>
```

## Quality gate

- [ ] Used real check-run, PR, or coverage artifact data.
- [ ] Separated test failures from pipeline infrastructure failures.
- [ ] Classified severity and merge impact.
- [ ] Identified failed check names and conclusions.
- [ ] Recommended concrete tests or coverage improvements.
- [ ] No emojis or pictographs are present in the report.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
