---
applyTo: ".github/workflows/*.yml"
description: "Use when editing GitHub Actions workflows for Open Horizons validation, deployment, release, security, and IssueOps automation."
---

# GitHub Actions Conventions — CI, Security, Release, and IssueOps

This file activates when you edit workflows in `.github/workflows/`. It teaches how Open Horizons configures least-privilege permissions, pinned actions, OIDC, path filters, validation gates, and shell-safe workflow steps. It does **not** cover the shell scripts invoked by workflows, which belong to the `shell` instructions, Copilot primitive schemas, which belong to the `agent-files` instructions, issue form routing, which belongs to the `issue-forms` instructions, Terraform module rules, which belong to the `terraform` instructions, or Kubernetes manifest authoring, which belongs to the `kubernetes` instructions.


## Authoritative Sources and Precedence

Follow these sources in order:

1. Repository files matched by `applyTo: ".github/workflows/*.yml"` for existing local patterns.
2. This `github-actions` instruction file for passive conventions, boundaries, and examples.
3. Official upstream documentation only when it is consistent with repository conventions.

When sources conflict, the higher-priority source wins. Do not duplicate or weaken rules owned by another primitive.

## Responsibility Split

This file owns passive conventions for github actions conventions — ci, security, release, and issueops. Use the `github-cli` and `pipeline-diagnostics` skills for ordered procedures, command sequences, setup, validation, or troubleshooting that goes beyond these rules.

> [!IMPORTANT]
> Workflows are a privileged automation surface. Keep default permissions read-only and raise permissions only at the job that needs them.

## Permissions and OIDC

Set top-level `permissions: contents: read` unless every job needs more. Add `id-token: write` only for Azure OIDC login jobs.

```yaml
# Wrong: grants write access to every job.
permissions: write-all
```

```yaml
permissions:
  contents: read

jobs:
  deploy:
    permissions:
      contents: read
      id-token: write
```

## Action Pinning and Setup

Pin third-party actions to a full SHA with a version comment where possible. The repository already uses SHA-pinned checkout and setup-python in `validate-agents.yml`.

```yaml
# Wrong: mutable branch ref can change without review.
- uses: actions/checkout@main
```

```yaml
- uses: actions/checkout@a26af69be951a213d495a4c3e4e4022e16d87065 # v4
```

> [!WARNING]
> Do not pipe untrusted issue, PR, branch, or commit values directly into shell. Assign them to `env` and quote variables inside Bash.

## Shell Steps

Workflow `run` blocks that rely on Bash must declare `shell: bash` and use `set -euo pipefail`, matching repository scripts.

```yaml
# Wrong: event title is expanded directly in shell.
- run: echo "${{ github.event.issue.title }}"
```

```yaml
- shell: bash
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}
  run: |
    set -euo pipefail
    printf '%s
' "$ISSUE_TITLE"
```

## Path Filters and Validation Gates

Keep path filters aligned with files that truly affect each workflow. Primitive changes must run the strict validator, as in `validate-agents.yml`.

```yaml
# Wrong: primitive validator misses instruction changes.
paths:
  - ".github/agents/**"
```

```yaml
paths:
  - ".github/agents/**"
  - ".github/prompts/**"
  - ".github/skills/**/SKILL.md"
  - ".github/instructions/**"
  - ".github/ISSUE_TEMPLATE/**"
```

> [!NOTE]
> Deployment workflows should include dry-run, plan, or validation jobs before apply or release jobs so operators can inspect evidence.

## Concurrency and Environments

Use `concurrency` to prevent competing deployment updates and GitHub environments for staging or production approvals.

```yaml
# Wrong: multiple production deploys can race.
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
```

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false

jobs:
  deploy-prod:
    environment: production
    runs-on: ubuntu-latest
```

## Conventions

| Rule | Rationale |
|---|---|
| Use least-privilege top-level permissions | Most validation jobs only need read access. |
| Add `id-token: write` only to OIDC jobs | OIDC tokens should not be available to unrelated jobs. |
| Pin actions to SHAs with version comments | Builds remain auditable while humans can see the intended version. |
| Pass untrusted context through `env` before Bash | Quoting variables is safer than interpolating expressions into scripts. |
| Run strict Copilot primitive validation on `.github/**` customization changes | Agents, prompts, skills, instructions, and issue forms route automation. |
| Use concurrency for deployments and releases | Parallel writes can corrupt environment state or publish conflicting artifacts. |

## Do / Do Not

| Do | Do not |
|---|---|
| Keep validation jobs small and targeted | Hide critical failures behind broad `continue-on-error`. |
| Use existing repository scripts for deployment and validation | Reimplement complex Bash inline in workflow YAML. |
| Scope write permissions to the job that needs them | Set `write-all` at workflow level. |
| Include explicit Python, Node, or Terraform setup versions | Depend on runner defaults. |

## Checklist Before Opening a PR

- [ ] Workflow permissions are least-privilege and job-scoped.
- [ ] Third-party actions are SHA-pinned or have a documented repository exception.
- [ ] Bash steps use `shell: bash`, `set -euo pipefail`, and quoted env variables.
- [ ] Path filters include all files that affect the workflow.
- [ ] Deployment or release workflows use concurrency and environment protections where appropriate.
- [ ] Existing validators still run for Copilot primitives, Terraform, scripts, and manifests.
