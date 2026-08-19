---
name: pipeline-diagnostics
description: 'Use when diagnosing GitHub Actions CI/CD failures, failed workflow runs, build errors, deploy job failures, skipped workflows, queue delays, and failed job logs. Produces workflow evidence, failed step identification, root-cause analysis, and remediation steps. DO NOT USE FOR: test analysis (use test-coverage), Kubernetes operations (use kubectl-cli), Helm charts (use helm-cli). Triggers include "diagnose this workflow failure", "why did CI fail", "inspect failed GitHub Actions logs", and "debug the deploy pipeline".'
---

# Pipeline Diagnostics

Use this skill to analyze GitHub Actions workflow runs from real `gh` output and repository workflow files under `.github/workflows/`. It produces a concise diagnosis with failed job, failed step, likely root cause, and the next remediation owner.

> [!NOTE]
> This skill depends on the `gh` CLI, authenticated GitHub access, and workflow visibility for the target repository. It does not use an MCP server by default.

## When to invoke

- "Diagnose this failed GitHub Actions run."
- "Why did the deploy pipeline fail?"
- "Inspect the failed job logs for this workflow."
- "Explain why the workflow was skipped."
- "Find the root cause of this CI error."

## Prerequisites and context

- `gh auth status` succeeds.
- The repository owner/name, workflow name, run ID, branch, or PR number is known.
- `.github/workflows/` exists in the repository.
- The user wants CI/CD diagnosis rather than test coverage analysis or Kubernetes troubleshooting.

## Procedure

### Step 1: Identify the run

```bash
gh run list --limit 10
gh run list --status failure --limit 5
```

If the user provides a PR, inspect checks first.

```bash
gh pr checks <pr-number>
```

### Step 2: Fetch failed job evidence

```bash
gh run view <run-id>
gh run view <run-id> --log-failed
```

Collect workflow name, run number, branch, event, failed job, failed step, and the first actionable error line.

### Step 3: Classify failure severity

| Severity | Meaning |
| --- | --- |
| Critical | Required check blocks merge or deployment, security scan failed, or release workflow failed. |
| High | Main CI failed on a protected branch or repeat failure affects multiple PRs. |
| Medium | PR-only failure with clear remediation and no production impact. |
| Low | Skipped, cancelled, neutral, or documentation-only check issue. |

### Step 4: Diagnose by pattern

| Pattern | Evidence | Next action |
| --- | --- | --- |
| Dependency install | Fails in `npm ci`, `pip install`, or package restore | Check lock file and registry errors. |
| Build or compile | Type, import, or compiler error | Identify file and line, then fix or hand off to code owner. |
| Test failure | Test runner reports failed tests | Use `test-coverage` for detailed test analysis. |
| Docker failure | `docker build` or push error | Check Dockerfile paths, image tags, and registry auth. |
| Deployment failure | `kubectl`, `helm`, or Azure step failed | Route to `kubectl-cli`, `helm-cli`, or `azure-cli`. |

### Step 5: Recommend rerun only when appropriate

Rerun failed jobs only when evidence indicates flake, transient infrastructure, or external service failure.

```text
Pipeline action: rerun failed jobs
Workflow run: <run-id>
Repository: <owner>/<repo>
Proceed with rerunning failed jobs? (y/n)
```

> [!IMPORTANT]
> Only rerun GitHub Actions jobs after an explicit affirmative response. On a negative, ambiguous, or missing response, do not trigger a rerun; output the diagnosis and stop.

```bash
gh run rerun <run-id> --failed
```

## Limits

- Do not use this skill for: test analysis (use test-coverage), Kubernetes operations (use kubectl-cli), Helm charts (use helm-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Run ID is missing | List recent runs and ask the user to identify the target if ambiguous. |
| GitHub auth fails | Ask the operator to run `gh auth login`; do not infer logs. |
| Logs are unavailable | Use run summary, job status, and workflow file evidence; state the limitation. |
| Failure is a test assertion | Stop CI diagnosis and use `test-coverage` for test-specific analysis. |
| Failure is a live cluster error | Summarize the pipeline evidence and route to `kubectl-cli` or `helm-cli`. |

## Output template

Return exactly this structure:

```markdown
## Pipeline Diagnosis

**Workflow:** <workflow>
**Run:** <run-id>
**Branch:** <branch>
**Event:** <event>
**Severity:** <Critical|High|Medium|Low>

### Failed Job and Step
| Job | Step | Conclusion | Evidence |
| --- | --- | --- | --- |
| <job> | <step> | <conclusion> | <log excerpt> |

### Root Cause
<analysis>

### Remediation
1. <step>

### Handoff
- <skill or owner>
```

## Quality gate

- [ ] Used real `gh` run or PR check data.
- [ ] Identified workflow, run, failed job, and failed step.
- [ ] Included one actionable log excerpt or stated why logs were unavailable.
- [ ] Classified severity.
- [ ] Recommended rerun only when justified by evidence.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
