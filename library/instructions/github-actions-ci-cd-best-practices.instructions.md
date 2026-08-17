---
applyTo: ".github/workflows/*.yml,.github/workflows/*.yaml"
description: "Enforces GitHub Actions CI/CD conventions for workflow structure, permissions, secrets, OIDC, action pinning, caching, testing, deployments, rollback, and troubleshooting."
---

# GitHub Actions CI/CD Conventions — Secure, Fast, and Reliable Workflows

These instructions apply to GitHub Actions workflow files under `.github/workflows/*.yml` and `.github/workflows/*.yaml`. They are authoritative for workflow structure, job boundaries, action pinning, token permissions, secrets, OIDC, caching, test orchestration, artifacts, deployment gates, rollback, and CI/CD troubleshooting in matched files; repository release policy, environment protection rules, and application-specific build or test instructions win where they are stricter.

## Workflow Structure and Triggers

Write workflows as clear, modular automation with descriptive `name`, precise `on` triggers, explicit `permissions`, and predictable concurrency.

| Concern | Convention |
| --- | --- |
| Workflow files | Use descriptive file names such as `build-and-test.yml` and `deploy-prod.yml`; keep workflow purpose obvious from the file name and workflow `name`. |
| Triggers | Choose the narrowest correct event: `push`, `pull_request`, `workflow_dispatch`, `schedule`, `repository_dispatch`, or `workflow_call`; prefer branch and path filters such as `on: push: branches: [main]` and `on: pull_request` when they reduce unnecessary runs. |
| Reuse | Use reusable workflows with `workflow_call` for repeated build/test/deploy patterns instead of copy-pasting jobs across many workflows. |
| Concurrency | Set `concurrency` for critical workflows, shared environments, and deployments so parallel runs do not race or waste resources. |
| Permissions | Set workflow-level `permissions` to least privilege, usually `contents: read`, then override at job level only where needed. |
| Manual inputs | Use `workflow_dispatch` inputs for controlled manual deployments rather than editing workflow files to change release behavior. |

## Jobs, Steps, and Action Pinning

Jobs represent distinct phases such as `lint`, `build`, `test`, and `deploy`. Steps stay atomic, named, and auditable.

| Concern | Convention |
| --- | --- |
| Runners | Choose `runs-on` deliberately: `ubuntu-latest` for most CI, `windows-latest` or `macos-latest` for platform-specific work, and `self-hosted` only when private network access, special hardware such as `GPUs`, or cost/performance requirements justify the maintenance burden. |
| Dependencies | Use `needs` for job order, `outputs` for inter-job data such as `artifact_path`, and `if` for branch, event, or status conditions such as `if: success()`, `if: failure()`, and `if: always()`. |
| Step shape | Every step has a descriptive `name`; `run` scripts are short, shell-safe, and fail fast; `with` inputs are explicit; `env` never carries hardcoded secrets. |
| Action references | Pin every `uses` action to a full-length commit SHA and add a human-readable version comment, for example `actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4.3.1`; do not use mutable `@v4`, `@main`, `@latest`, or branch references. |
| Marketplace actions | Prefer trusted publishers such as `actions/`; audit third-party actions before use; enable `dependabot` for action updates. |
| Timeout | Set `timeout-minutes` for long-running jobs so hung workflows do not consume runner time indefinitely. |

## Security and Identity

Secure workflows by default. Treat CI/CD as production-grade privileged automation.

| Security area | Convention |
| --- | --- |
| Secrets | Store sensitive values in GitHub Secrets or environment secrets and reference them through `secrets.<SECRET_NAME>`, `${{ secrets.MY_SECRET }}`, `secrets.MY_API_KEY`, `MY_SECRET`, `MY_API_KEY`, `PROD_API_KEY`, or `SECRET_NAME` only as placeholders; never print or construct secrets dynamically. |
| Environment secrets | Use `environment` protection, required reviewers, branch restrictions, and environment-specific secrets for staging and production; example URLs such as `https://prod.example.com` belong in environment metadata, not in hardcoded deployment commands. |
| OIDC | Prefer OpenID Connect (`OIDC`) for AWS, Azure, GCP, and other cloud providers; use short-lived credentials and cloud trust policies instead of long-lived static credentials. |
| Cloud actions | Pin cloud authentication actions such as `aws-actions/configure-aws-credentials@<SHA> # v4.x.x` to a full SHA. |
| `GITHUB_TOKEN` | Restrict `GITHUB_TOKEN` to `contents: read` by default; add `pull-requests: write`, `checks: write`, `issues: read`, `packages: write`, or `contents: write` only for jobs that need them. |
| SCA and SAST | Add dependency scanning with `dependency-review-action`, Snyk, Trivy, Mend, or equivalent; add SAST with CodeQL, SonarQube, Bandit, ESLint security plugins, or equivalent. |
| Secret scanning | Enable GitHub secret scanning and consider local hooks such as `git-secrets` to prevent credential leaks before commit. |
| Images | For container workflows, use reproducible builds, sign images with Notary or Cosign, and verify signatures before production deployment. |
| Self-hosted runners | Harden self-hosted runners, restrict network access, patch promptly, and organize access with runner groups; never use untrusted PR code on privileged self-hosted infrastructure. |

## Performance, Caching, and Artifacts

Optimize for fast feedback without hiding correctness problems.

| Performance area | Convention |
| --- | --- |
| Caching | Use `actions/cache` pinned to a full SHA for package manager caches and build outputs; key caches with stable hashes such as `hashFiles('**/package-lock.json')` and `hashFiles('**/requirements.txt')`; use `restore-keys` for compatible fallback caches. |
| Cache debugging | Use `actions/cache/restore` with `lookup-only: true` to diagnose `Cache not found`, `Cache miss`, `Cache hit`, and `Cache creation failed` without mutating cache state. |
| Matrix | Use `strategy.matrix` with `include`, `exclude`, and `fail-fast: false` or `fail-fast: true` according to whether complete reports or fast failure matter more. |
| Checkout | Use `actions/checkout` with `fetch-depth: 1` for most jobs; use `fetch-depth: 0` only for release tags, `git blame`, or deep history analysis; set `submodules: false` and `lfs: false` unless required. |
| Large repos | Consider partial clone filters such as `--filter=blob:none` or `--filter=tree:0` only when the repository size justifies the complexity. |
| Artifacts | Use pinned `actions/upload-artifact` and `actions/download-artifact` to move build outputs, test reports, coverage, screenshots, videos, and release packages; set `retention-days` to manage storage and compliance. |
| Shell efficiency | Combine related commands with `&&`, avoid unnecessary `sleep`, remove unneeded files with `rm -rf` in the same logical step, and keep logs useful on `STDOUT` and `STDERR`. |

## Testing and Quality Gates

Run the cheapest useful tests early and make results visible in pull requests.

| Test layer | Convention |
| --- | --- |
| Unit tests | Run unit tests on every `push` and `pull_request`; use project-appropriate tools such as Jest, Vitest, Pytest, Go testing, JUnit, NUnit, XUnit, or RSpec; publish coverage from Istanbul, Coverage.py, JaCoCo, Codecov, Coveralls, or SonarQube when configured. |
| Integration tests | Run integration tests after unit tests; provision databases and services with `services`, Docker Compose, PostgreSQL/MySQL, RabbitMQ/Kafka, Redis, or similar isolated dependencies. |
| E2E tests | Use Cypress, Playwright, or Selenium against a deployed staging environment when possible; capture screenshots and videos on failure and use stable selectors such as `data-testid`. |
| Performance tests | Run JMeter, k6, Locust, Gatling, or Artillery for critical paths on a scheduled or release cadence; define thresholds for response time, throughput, and error rate. |
| Reporting | Publish JUnit XML, HTML, JSON, coverage, screenshots, videos, and scan reports as artifacts and Checks/Annotations; integrate Allure Report, TestRail, or dashboards when they are already part of the project. |
| Flakiness | Fix `Random failures` and `Passes locally, fails in CI` by removing race conditions, using explicit waits, standardizing environments, and isolating test data. |

## Deployment, Rollback, and Operations

Deployment workflows must protect environments, deploy tested artifacts, and support fast recovery.

| Deployment area | Convention |
| --- | --- |
| Staging | Use a GitHub `environment` for staging with branch protection, required reviewers where appropriate, and automated smoke tests after deployment. |
| Production | Use production environment protection, required reviewers, release windows where needed, manual approvals, and monitoring during and immediately after deployment. |
| Strategies | Choose rolling, Blue/Green or `blue/green`, canary, Dark Launch/Feature Flags, A/B testing, or progressive delivery according to risk, rollback speed, and infrastructure support; preserve Kubernetes controls such as `maxSurge`, `maxUnavailable`, Service Mesh, Istio, Linkerd, Ingress, and metric-based analysis when used. |
| Rollback | Store versioned artifacts and previous images; implement rollback commands such as `kubectl rollout undo`; create runbooks for manual rollback and incident response. |
| Incident response | Use actionable alerts, communication plans, and blameless PIRs or post-incident reviews to reduce `MTTR`. |
| Observability | Keep deployment logs, application metrics, Prometheus metrics, distributed tracing through OpenTelemetry or Jaeger, and production alerts connected to release health. |
| Emergency releases | Allow expedited hotfix paths only when they retain authentication, authorization, audit, and core test gates. |

## Troubleshooting Patterns

Diagnose workflow failures by matching symptoms to likely workflow keys instead of repeatedly rerunning unchanged jobs.

| Symptom | Check first |
| --- | --- |
| Workflow not triggering or jobs/steps skipping unexpectedly | Verify `on`, `branches`, `tags`, `paths`, `paths-ignore`, `branches-ignore`, `workflow_dispatch` inputs, `if` conditions, `concurrency`, and branch protection. |
| Permissions errors such as `Resource not accessible by integration` or `Permission denied` | Check `permissions`, `GITHUB_TOKEN`, environment secret access, OIDC trust policy, and role/identity permissions. |
| Cache issues | Check cache `key`, `restore-keys`, `path`, `lookup-only`, cache size, and whether the hash changes too often. |
| Long running workflows or timeouts | Profile longest-running jobs, add caching, use matrix parallelism, choose larger or self-hosted runners only with justification, and split workflows by concern. |
| Flaky tests | Remove non-deterministic behavior, isolate data, replace arbitrary `sleep` with explicit waits, use Docker `services`, and record screenshots or videos. |
| Deployment failures | Review `kubectl logs`, application logs, ConfigMaps, Secrets, network policy, post-deployment health checks, and rollback immediately if production degrades. |

## Workflow Keys and Operational Vocabulary

Preserve these workflow keys, contexts, tools, statuses, and examples when refactoring GitHub Actions guidance because they are common anchors in existing workflows: `# v4.3.1`, `${{ }}`, `${{ secrets.MY_SECRET }}`, `${{ toJson(github) }}`, `${{ toJson(job) }}`, `${{ toJson(steps) }}`, `.github/workflows/*.yml`, `github/workflows/*.yml`, `github/workflows/*.yaml`, `actions/setup-node`, `actions/upload-artifact`, `actions/download-artifact`, `setup-node`, `download-artifact`, `upload-artifact`, `actions/cache`, `actions/cache/restore`, `actions/checkout`, `aws-actions`, `aws-actions/configure-aws-credentials`, `artifact_path`, `package_app`, `my-app-build`, `node-version`, `node_modules`, `package-lock`, `run_id`, `refs/heads/develop`, `refs/heads/main`, `release/*`, `build/test`, `job/step`, `jobs/workflows`, `environment-specific`, `path/branch`, `branch-specific`, `language-specific`, `integration/E2E`, `inter-job`, `inter-workflow`, `passed/failed`, `read-only`, `cost-effective`, `cost-prohibitive`, `credential-less`, `long-lived`, `long-running`, `long-term`, `full-length`, `human-readable`, `third-party`, `auto-scaling`, `fine-grained`, `in-memory`, `multi-line`, `non-deterministic`, `non-essential`, `non-production`, `on-premise`, `open-source`, `post-deployment`, `post-incident`, `pre-commit`, `pre-deployment`, `re-building`, `re-fetching`, `resource-intensive`, `role/identity`, `step-by-step`, `tamper-proof`, `high-quality`, `main`, `develop`, `build`, `test`, `deploy`, `lint`, `services`, `service`, `inputs`, `outputs`, `jobs`, `name`, `path`, `secrets`, `tags`, `branches`, `pull_request`, `repository_dispatch`, `schedule`, `submodules`, `maxSurge`, `maxUnavailable`, `LaunchDarkly`, `Split.io`, `Unleash`, `Applitools`, `Percy`, `Launch/Feature`, `Checks/Annotations.`, `Jobs/Steps`, `Maven/Gradle`, `PostgreSQL/MySQL`, `RabbitMQ/Kafka`, `JS/TS`, `HTML`, `JSON`, `README`, `ITSM`, `SAST`, `OIDC`, `STDOUT/STDERR`, and `Passes locally, fails in CI`. Additional preserved troubleshooting and review terms: `always()`, `deploy-staging`, `double-check`, `sign-offs`, `unit/integration`, `up-to-date`, `users/groups`, `well-defined`, `well-tested`, `workflow/job`, `workflows/jobs`, `workflows/jobs.`, `zero-downtime`, `built-in`, `WhiteSource`, `) and branches (e.g., `, `) with `, and `)? Tags (e.g., `.

## Good / Bad Examples

The examples below illustrate immutable action pinning, least-privilege permissions, and explicit artifact passing.

**Good:**

```yaml
permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact_path: ${{ steps.package_app.outputs.path }}
    steps:
      - name: Checkout code
        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4.3.1
      - name: Package application
        id: package_app
        run: |
          zip -r dist.zip dist
          echo "path=dist.zip" >> "$GITHUB_OUTPUT"
```

Why: The workflow pins the action to an immutable SHA, grants only read access by default, uses a named output, and writes through `GITHUB_OUTPUT`.

**Bad:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@main
      - run: echo "$PROD_API_KEY" && ./deploy-script.sh
```

Why: The action reference is mutable, the secret is printed, permissions are implicit, and deployment lacks environment protection.

## Conventions

| Rule | Rationale |
|---|---|
| Use precise triggers, names, and concurrency groups | Workflows run when intended and do not race shared resources |
| Set least-privilege `permissions` and pin all `uses` actions to full SHAs | Compromised tokens or mutable action tags cannot silently expand the blast radius |
| Prefer OIDC and environment secrets over long-lived static credentials | Cloud deployments use short-lived, auditable credentials |
| Cache dependencies with stable keys and publish artifacts with retention policies | CI stays fast while outputs remain reproducible and inspectable |
| Run unit, integration, E2E, security, and performance gates at appropriate points | Failures surface before deployment and with enough context to debug |
| Protect staging and production with environments, approvals, health checks, and rollback | Releases are controlled and recoverable |
| Troubleshoot by checking workflow keys, permissions, cache keys, and logs | Diagnosis is faster than repeated blind reruns |

## Do / Do Not

| Do | Do not |
|---|---|
| Pin actions to full commit SHAs with version comments | Use mutable action tags or branches such as `@v4`, `@main`, or `@latest` |
| Start with `contents: read` and grant write scopes only per job | Leave `GITHUB_TOKEN` with broad implicit permissions |
| Use OIDC for cloud authentication where possible | Store long-lived cloud access keys as repository secrets |
| Use `hashFiles` and `restore-keys` for dependency caches | Make cache keys so dynamic that every run misses |
| Upload test reports, coverage, screenshots, and release packages as artifacts | Rebuild or re-fetch outputs in every downstream job |
| Deploy through protected environments with rollback commands ready | Deploy directly to production without approvals or recovery paths |
| Capture logs and metrics for deployment health | Treat a successful deploy command as proof the application works |

## Checklist Before Opening a PR

- [ ] Workflow `name`, file name, and `on` triggers match the workflow purpose.
- [ ] `permissions` are least privilege at workflow and job scope.
- [ ] Every `uses` reference is pinned to a full commit SHA with a version comment.
- [ ] Secrets are accessed only through GitHub secrets or environment secrets and are not printed.
- [ ] OIDC is used for cloud authentication where the provider supports it.
- [ ] Caching, matrix jobs, checkout depth, artifacts, and retention are configured deliberately.
- [ ] Unit, integration, E2E, security, performance, and reporting gates match project risk.
- [ ] Staging and production deployments use protected environments, health checks, and rollback.
- [ ] Troubleshooting guidance preserves trigger, permission, cache, flaky-test, and deployment-failure diagnostics.

## References

- Example protected environment URL placeholder: https://prod.example.com
