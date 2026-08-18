---
name: github-actions-efficiency
description: >-
  Audit GitHub Actions workflow efficiency and recommend fixes that reduce CI runtime, runner minutes, and wasted workflow runs. Use when the user asks about caching, concurrency, path filters, matrix reduction, job optimization, workflow cost, or CI baseline design.
---

# GitHub Actions efficiency

Inspect workflow YAML and recent run evidence, identify the highest CI-minute waste, protect required validation through guardrails, and return up to three ranked fixes with validation and impact.

## When to invoke

- "Reduce GitHub Actions runtime and cost."
- "Audit our workflows for wasted CI minutes."
- "Add caching and concurrency to these workflows."
- "Narrow path filters or matrix jobs safely."
- "Create an efficient GitHub Actions baseline."

## Prerequisites and context

- Use `.github/workflows/` when workflows exist.
- If no workflows exist, read `references/actions.md` and define a baseline before proceeding.
- If shell or `gh` CLI access is unavailable, ask for `.github/workflows/` contents and `gh run list --limit 10` output. If only partial files are provided, state: `Static-only analysis (not confirmed with live runs).`

## Procedure

1. Measure workflow structure and recent run evidence:

```bash
rg -n "on:|concurrency:|paths:|paths-ignore:|strategy:|matrix:|cache:" .github/workflows
gh run list --limit 10
run_id=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
gh run view "$run_id" --log-failed
```

2. Look for missing dependency caches, missing `concurrency` cancellation, over-broad triggers, duplicate workflow coverage, and expensive jobs that run on every change regardless of scope.
3. Apply all guardrails before recommending changes.
4. Rank supported fixes by estimated daily CI minutes saved: per-run savings multiplied by runs per day.
5. Select all supported candidates, up to a maximum of three.
6. Validate path-gating and concurrency cancellation with a live test push on a non-protected branch when `gh` access and repo policy allow it.

## Waste candidates

| Candidate | Evidence | Safe fix pattern |
| --- | --- | --- |
| Dependency caching | Repeated install steps and no lockfile-based cache. | Add cache keys derived from lockfiles; avoid caching generated build output unless safe. |
| `concurrency` cancellation | Multiple runs queue on the same branch or PR. | Add group by workflow and ref/PR, then `cancel-in-progress: true` where safe. |
| Duplicate workflow coverage | Multiple workflows run equivalent tests on the same event. | Remove overlap before merging jobs; keep release and required checks intact. |
| Trigger narrowing | Docs-only or unrelated changes run full CI. | Add `paths` or `paths-ignore` at workflow or job level with required validation preserved. |
| Matrix reduction | Matrix legs lack documented version/platform commitment. | Keep documented legs; reduce low-risk event types or run full matrix on scheduled/release events. |
| Critical-path parallelism | Independent jobs run serially. | Split jobs only when setup overhead does not erase wall-clock gains. |

## Guardrails

- Do not hide required validation such as release, schema, migration, or shared-library checks.
- Do not reduce parallelism unless the user prioritizes cost over latency and the new critical path stays within 1.25× the original.
- Preserve only documented matrix legs; remove unsupported legs only with evidence.
- Formatter or bot write-back jobs should use opt-in triggers rather than automatic write-back on every run.
- Split repo-editable YAML recommendations from org-level or GitHub-account settings.
- Treat unexpected live behavior as a real bug even when YAML appears correct.

## Progressive disclosure and bundled resources

- `references/actions.md`: audits, job gating, matrix reduction, live validation, and workflow-specific fixes.
- `references/reporting.md`: before/after efficiency report format and calculations.
- `references/patterns.md`: full YAML examples when inline commands are not enough.
- `references/review-rubric.md`: use when reviewing completed efficiency work.

## Output template

```markdown
## GitHub Actions efficiency result

**Status:** proven live | static-only | blocked
**Scope:** `.github/workflows/<workflow>.yml`

### Waste sources
| Rank | Source | Evidence | Estimated daily CI minutes wasted |
| --- | --- | --- | --- |
| 1 | <driver> | <workflow line, run log, or assumption> | <minutes> |

### Proposed fixes
| Rank | Fix | Evidence | Estimated daily CI minutes saved | Risk |
| --- | --- | --- | --- | --- |
| 1 | <top fix> | <why supported> | <minutes> | <remaining risk> |

### Validation
- Workflow syntax/static review: pass | fail
- Live test push: pass | fail | not run, <reason>
- Path gating: verified | unverified, <reason>
- Concurrency cancellation: verified | unverified, <reason>

### Impact
- PR wall-clock time: <expected or measured>
- Total runner time: <expected or measured>
```

## Quality gate

- [ ] `.github/workflows/` was inspected or its absence was handled with `references/actions.md`.
- [ ] `rg`, `gh run list --limit 10`, and `gh run view "$run_id" --log-failed` were run or the static-only limitation is stated.
- [ ] Every proposed fix has evidence, passes all guardrails, and preserves required validation.
- [ ] No more than three fixes are recommended, ranked by estimated daily CI minutes saved.
- [ ] Validation separates live proof from local/static review and remaining risk.
- [ ] Impact separates PR wall-clock time from total runner time.
