---
description: "Use when creating or reviewing GitHub Actions, CI/CD workflows, YAML pipeline gates, build checks, and deployment automation."
applyTo: ".github/workflows/**,.github/actions/**,**/action.yml,**/action.yaml"
---

# CI/CD Conventions — GitHub Actions Gates

This file activates when you edit workflows under `.github/workflows/`, composite actions under `.github/actions/`, or any `action.yml`/`action.yaml`. It teaches how to structure the pipeline, pin actions, scope permissions, and keep the gates honest. The two live workflows — [`ci.yml`](../workflows/ci.yml) and [`spec-quality.yml`](../workflows/spec-quality.yml) — are the reference; read them before changing a gate.

## The Live Gates

| Workflow · Job | What it enforces | Blocking? |
|---|---|---|
| `ci.yml` · `detect-changes` | `dorny/paths-filter` sets `backend`/`frontend`/`infra` outputs so downstream jobs run only on relevant changes | n/a |
| `ci.yml` · `natural-format` | Fails when Natural source uses comma decimal format declarations such as `(P9,2)` instead of the Natural CE period form `(P9.2)` | Yes |
| `ci.yml` · `backend` | JDK 21 (temurin) + `./mvnw -B verify`; uploads the Jacoco report | Yes |
| `ci.yml` · `frontend` | pnpm 9 + Node 20; `pnpm lint`, `pnpm typecheck`, `pnpm test --run --coverage` | Yes |
| `ci.yml` · `infra` | `terraform fmt -check -recursive`, then `init -backend=false` + `validate` per module | Yes |
| `spec-quality.yml` · `markdown-lint` | `markdownlint-cli2` over `**/*.md` | Yes |
| `spec-quality.yml` · `spec-traceability` | Reports REQ-IDs in `specs/` not yet referenced by a test (emits `::warning::`) | No |
| `spec-quality.yml` · `legacy-traceability` | Every REQ-ID in `specs/` must carry a valid `source_legacy:` line | Yes |

> [!IMPORTANT]
> `legacy-traceability` fails the build; `spec-traceability` only warns. See [`requirements.instructions.md`](requirements.instructions.md) for the exact `source_legacy:` format the gate accepts.

## Pin Every Action by Commit SHA

Reference actions by full 40-character commit SHA, with the human-readable tag in a trailing comment. Tags are mutable; SHAs are not.

```yaml
# Correct — immutable reference
- uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
# Wrong — a tag can be moved to malicious code
- uses: actions/checkout@v6
```

## Least-Privilege Permissions

Declare `permissions` at the top of every workflow with the narrowest scope, then widen per job only where needed.

```yaml
permissions:
  contents: read # default for the whole workflow

jobs:
  detect-changes:
    permissions:
      contents: read
      pull-requests: read # only this job needs it
```

## Path-Filtered, Conditional Jobs

Gate heavy jobs behind `detect-changes` so a docs-only PR does not run Maven or Terraform.

```yaml
backend:
  needs: detect-changes
  if: needs.detect-changes.outputs.backend == 'true'
```

## Concurrency and Timeouts

Every workflow cancels superseded runs, and every job sets a `timeout-minutes` so a hung step cannot burn the runner.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Deployment with OIDC (Forward-Looking)

No deploy job exists yet. When you add one, authenticate to Azure with OIDC federation — never a stored client secret — and request `id-token: write` only on that job.

```yaml
permissions:
  id-token: write # request the short-lived OIDC token
  contents: read
steps:
  - uses: azure/login@<full-sha> # pin it
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
      subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

Deployed workloads authenticate service-to-service with Managed Identity (see [`infrastructure.instructions.md`](infrastructure.instructions.md)); hardening checklists live in the [`pipeline-hardening`](../skills/pipeline-hardening/SKILL.md) skill.

## Conventions

| Rule | Rationale |
|---|---|
| Pin actions by full commit SHA | Prevents supply-chain tag hijacking |
| `permissions:` block on every workflow, `contents: read` default | Least privilege by construction |
| `concurrency` + `cancel-in-progress` | No wasted or racing runs on the same ref |
| `timeout-minutes` on every job | A stuck step fails fast |
| OIDC federation, never a stored cloud secret | No long-lived credentials in the repo |

## Do / Do Not

| Do | Do not |
|---|---|
| Reference `@<sha> # vN` | Reference `@v4`, `@main`, or a branch |
| Grant `id-token: write` per deploy job | Grant `write-all` at workflow level |
| Read the workflow before editing a gate | Guess what a gate checks |
| Let `detect-changes` skip irrelevant jobs | Run every job on every PR |

## Checklist Before Opening a PR

- [ ] Every `uses:` is pinned to a full commit SHA with a version comment
- [ ] The workflow declares a top-level `permissions:` block scoped to least privilege
- [ ] Each job sets `timeout-minutes`, and the workflow sets `concurrency`
- [ ] New gates are described accurately in the relevant instruction file
- [ ] Any cloud step uses OIDC, not a stored secret, and requests `id-token: write` narrowly
- [ ] `markdownlint-cli2` and the existing CI jobs pass locally where reproducible
