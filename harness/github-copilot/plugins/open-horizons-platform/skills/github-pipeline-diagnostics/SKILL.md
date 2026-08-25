---
name: github-pipeline-diagnostics
description: >-
  Pipeline diagnostics analyzes GitHub Actions CI/CD failures and remediation patterns. Use this skill when diagnosing workflow failures, build errors, deploy failures, failed jobs or steps, logs triage, actions permissions, OIDC failures, dependency cache issues, and CI/CD debugging.
---

# GitHub Pipeline Diagnostics Skill

Use repository, workflow run, job, and log evidence from GitHub Actions to identify CI/CD failure causes, map them to common remediation patterns, and return a concise diagnosis with validation evidence.

## When to invoke

- "Diagnose why this GitHub Actions workflow failed."
- "Triage a failed CI build or deployment job."
- "Analyze failed job logs and recommend remediation steps."
- "Investigate Actions permissions, OIDC, cache, dependency, build, Docker, or deployment failures."

## Criteria

### GitHub Actions API reference

#### Workflow Runs

```bash
# List recent runs (all statuses)
gh run list --repo {owner}/{repo} --limit 10

# Filter by status
gh run list --repo {owner}/{repo} --status failure --limit 5

# View specific run details
gh run view {run_id} --repo {owner}/{repo}

# View failed job logs
gh run view {run_id} --repo {owner}/{repo} --log-failed

# Re-run failed jobs
gh run rerun {run_id} --repo {owner}/{repo} --failed
```

#### REST API endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/repos/{owner}/{repo}/actions/runs` | GET | List workflow runs |
| `/repos/{owner}/{repo}/actions/runs/{id}` | GET | Get specific run |
| `/repos/{owner}/{repo}/actions/runs/{id}/jobs` | GET | Get jobs for a run |
| `/repos/{owner}/{repo}/actions/runs/{id}/logs` | GET | Download run logs |

#### Run status values

| Status | Meaning |
|--------|---------|
| `queued` | Run is waiting to be picked up |
| `in_progress` | Run is currently executing |
| `completed` | Run has finished (check conclusion) |

#### Run conclusion values

| Conclusion | Meaning | Action |
|-----------|---------|--------|
| `success` | All jobs passed | No action needed |
| `failure` | One or more jobs failed | Investigate failed steps |
| `cancelled` | Run was cancelled | Check if manual or timeout |
| `skipped` | Run was skipped (path filter, condition) | Review trigger conditions |
| `timed_out` | Run exceeded time limit | Optimize or increase timeout |

### Common failure patterns

#### 1. Dependency Install Failures
**Symptoms:** `npm ci`, `yarn install`, or `pip install` step fails
**Causes:** Lock file out of sync, registry down, version conflicts
**Remediation:**
1. Check if `package-lock.json` / `yarn.lock` is committed
2. Compare lock file with `package.json` versions
3. Check npm/PyPI registry status
4. Clear caches and re-run

#### 2. Build/Compile Errors
**Symptoms:** `tsc`, `go build`, `dotnet build` step fails
**Causes:** Type errors, missing imports, breaking API changes
**Remediation:**
1. Read the error message from the failed step output
2. Identify the file and line number
3. Suggest specific code fix
4. Recommend running build locally first

#### 3. Test Failures
**Symptoms:** `jest`, `pytest`, `go test` step fails
**Causes:** Flaky tests, environment differences, assertion failures
**Remediation:**
1. Identify which tests failed
2. Use the `test-coverage` skill for detailed test analysis
3. Check if tests pass locally

#### 4. Docker Build Failures
**Symptoms:** `docker build` or `docker push` step fails
**Causes:** Missing base image, COPY source not found, registry auth
**Remediation:**
1. Check Dockerfile COPY paths match repo structure
2. Verify base image exists and tag is valid
3. Check registry credentials in secrets

#### 5. Deployment Failures
**Symptoms:** `kubectl apply`, `helm upgrade`, or `az webapp deploy` fails
**Causes:** Cluster unreachable, image pull error, resource limits
**Remediation:**
1. Check cluster connectivity (credentials, RBAC)
2. Verify image exists in registry
3. Check resource quotas and limits

## Output template

Return exactly this structure:

```markdown
  ## Pipeline Diagnosis

**Status:** PASS | FAIL | BLOCKED
**Summary:** {one_sentence_summary}

  ### Details
**Repository:** {owner}/{repo}
**Workflow:** {workflow_name}
**Run:** #{run_number} ({run_id})
**Branch:** {branch} | **Event:** {event} | **Status:** {conclusion}

  #### Failed Jobs
| Job | Step | Status | Duration |
|-----|------|--------|----------|
| {job_name} | {step_name} | {conclusion} | {duration} |

  #### Root Cause
{analysis}

  #### Remediation Steps
1. {step_1}
2. {step_2}
3. {step_3}

  #### Recommended Handoff
- {handoff_recommendation}

  ### Validation
- Workflow run data fetched: {pass_fail_result_and_evidence}
- Failed job and step identified: {pass_fail_result_and_evidence}
- Remediation mapped to observed evidence: {pass_fail_result_and_evidence}
```

## Limits

- Do not use this skill for test coverage strategy; use `test-coverage` (`skill`) instead when coverage, quality gates, or test signals are the primary concern.
- Do not use this skill for GitHub CLI mechanics; use `github-cli` (`skill`) instead when the user needs general repository or workflow command help.
- Do not use this skill for Kubernetes operations; use `kubectl-cli` instead when the work is direct cluster operation.
- Do not use this skill for Helm chart fixes; use `helm-cli` instead when the work is chart packaging or release management.
- Do not use this skill to re-run or mutate workflow state unless the user explicitly requested that action.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `pipeline` | `agent` | A persistent agent should diagnose GitHub Actions failures across a conversation. |
| `test-coverage` | `skill` | Failed checks are primarily test, coverage, or quality-gate signals. |
| `github-cli` | `skill` | General GitHub CLI repository or workflow mechanics are needed. |
| `deploy-orchestration` | `skill` | A pipeline failure requires full deployment sequencing or platform rollout context. |
| `observability-stack` | `skill` | Runtime monitoring data is needed to correlate deployment failures with service health. |

## Quality gate

- [ ] Fetched real workflow run data before diagnosing.
- [ ] Identified specific failed job and step.
- [ ] Provided root cause analysis tied to run, job, or log evidence.
- [ ] Included actionable remediation steps.
- [ ] Suggested follow-up when appropriate (`test-coverage` for tests, `@open-horizons-terraform` for infra).
- [ ] Used the output template format with status, summary, details, and validation evidence.
