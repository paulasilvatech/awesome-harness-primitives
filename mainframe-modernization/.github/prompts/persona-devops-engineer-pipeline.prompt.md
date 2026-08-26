---
name: "pipeline"
description: "Create a hardened GitHub Actions CI/CD pipeline for SIFAP 2.0 with build, test, security, and environment-promotion gates."
argument-hint: "target=backend|frontend|infra component=<name>"
agent: "devops-engineer"
tools: ["read", "search", "edit"]
---
# /pipeline

## Objective

Create or refactor a **GitHub Actions** workflow for SIFAP 2.0 that builds, tests, scans, and promotes artifacts through `develop` → `main` (production) with explicit gates. The workflow matches the house style already in `.github/workflows/ci.yml`: actions pinned by full commit SHA with a trailing `# vN` comment, a least-privilege `permissions:` block, a `concurrency` group, and `timeout-minutes` on every job. The deliverable lives in `.github/workflows/`.

## When to Invoke

When a bounded context reaches Stage 3/4 and needs automated build, test, and deployment, or when an existing workflow must be hardened (OIDC, SHA pinning, signing).

## Preconditions

- The target component exists (`backend/`, `frontend/`, or `infra/`) or is being created in this PR
- GitHub environments (`dev`, `prod`) are configured with required reviewers
- Azure federated credentials (OIDC) and the container registry are available to the repository

## Inputs the Team Must Provide

- The pipeline target: Java backend service, Next.js frontend app, IaC module, or end-to-end orchestration
- The branch model (feature branches cut from `develop`, promoting `develop` → `main`; see `00-GIT-WORKFLOW.md`)
- The GitHub environments and their required reviewers
- The container registry (for example Azure Container Registry) and any compliance needs (SBOM, signed images)

Ask the user for anything that is missing.

## What I Will Do

- Read [`../skills/pipeline-hardening/SKILL.md`](../skills/pipeline-hardening/SKILL.md) and apply its Tier 1–3 controls
- Choose the trigger surface and organize jobs by stage (build, quality, security, package, deploy)
- Authenticate to Azure with OIDC — no long-lived service-principal secret
- Pin every action by SHA with a `# vN` comment and set a least-privilege `permissions:` block, `concurrency` group, and `timeout-minutes`, mirroring `.github/workflows/ci.yml`
- Emit deployment traceability (merge SHA and related `REQ-ID`s)

## What I Will NOT Do

- Invent action SHAs, secret names, or registry hosts — unknown SHAs are resolved from the action's release and secrets are referenced by name, never inlined
- Write application code (`@builder`), author Terraform modules (`/iac-module`), or change requirements (`@requirements-engineer`)
- Store an Azure secret in GitHub when OIDC works, or grant `permissions: write-all`
- Pin an action to a floating tag (`@v3`, `@main`) instead of a SHA
- Deploy to production without an approval gate, or hardcode a secret anywhere in YAML

## Output Format

The primary artifact is the workflow YAML. Example (backend service):

```yaml
name: backend-ci
on:
  pull_request:
    paths: ["backend/**"]
  push:
    branches: [develop, main]
    paths: ["backend/**"]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    name: Build, test, scan
    runs-on: ubuntu-latest
    timeout-minutes: 20
    defaults:
      run:
        shell: bash
        working-directory: backend
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: "21"
          cache: maven
      - name: Build and test
        run: ./mvnw -B verify
      - name: Scan filesystem (fail on Critical/High)
        uses: aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25 # v0.36.0
        with:
          scan-type: fs
          severity: CRITICAL,HIGH
          exit-code: "1"

  deploy-prod:
    name: Deploy to production
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 20
    environment: prod # required reviewers enforce two approvals
    permissions:
      contents: read
      id-token: write # OIDC federated login; no stored Azure secret
    steps:
      - name: Azure login (OIDC)
        uses: azure/login@7184910d9eb2b1c5e48f7073824a90609bb9b6d6 # v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - name: Install cosign and sign the image by digest
        uses: sigstore/cosign-installer@398d4b0eeef1380460a10c8013a76f728fb906ac # v3
```

Accompany the YAML with: required secrets/variables (by name and purpose), branch-protection settings (required checks `build`, `quality`, `security`), and a one-line promotion flow (`PR → build+scan → develop → deploy-dev → main → 2 approvals → deploy-prod`).

## Definition of Done

- [ ] OIDC authentication; no Azure secret is stored in GitHub
- [ ] Every action is pinned to a commit SHA with a `# vN` comment
- [ ] `build`, `quality`, and `security` are required PR checks
- [ ] The top-level `permissions:` is `contents: read`, elevated only where a job needs it
- [ ] A `concurrency` group prevents two deployments to the same environment at once
- [ ] `timeout-minutes` is defined on every job
- [ ] Production deployments require approvals and carry the merge SHA and related `REQ-ID`s

## Prompt Body

You are the `@devops-engineer`. The team needs a workflow that matches the repo's existing CI conventions exactly.

**Step 1 — Load the hardening controls.**
Read [`../skills/pipeline-hardening/SKILL.md`](../skills/pipeline-hardening/SKILL.md) and open `.github/workflows/ci.yml` to copy the house style (SHA pins with `# vN`, `permissions:`, `concurrency`, `timeout-minutes`).

**Step 2 — Choose the trigger surface.**
`pull_request` for build and test, `push` to protected branches for deployment, and `workflow_dispatch` for manual rollback. Avoid `pull_request_target` unless forks genuinely need secrets.

**Step 3 — Organize jobs by stage.**
`build` (compile and unit-test: `./mvnw -B verify` or `pnpm install --frozen-lockfile && pnpm build && pnpm test`), `quality` (lint, type-check, coverage upload), `security` (Trivy, dependency scan, secret scan on the diff), `package` (build image, push by digest, generate an SBOM with syft, sign with cosign), `deploy-dev` (automatic on `develop`), and `deploy-prod` (on `main`, requires approvals).

**Step 4 — Authenticate with OIDC.**
Use `azure/login` with federated credentials and `id-token: write` scoped to the deploy job only. Never store a service-principal secret.

**Step 5 — Pin, cache, and bound every job.**
Pin every action by SHA with a `# vN` comment. Cache Maven by `pom.xml` hash and use the pnpm store cache. Set `timeout-minutes` per job and a workflow-level `concurrency` group.

**Step 6 — Enforce gates and traceability.**
Make `build`, `quality`, and `security` required checks via branch protection. Tag the deployed image with the merge commit SHA and the related `REQ-ID`s from the PR description, and expose them in the deployment description.

The top-level `permissions:` defaults to `contents: read` and is elevated only where needed. OIDC only — no long-lived Azure secret and no hardcoded secret in YAML. Every action is SHA-pinned with a `# vN` comment, and production deploys behind an approval gate.

## Invocation Example

```
/pipeline target=backend component=<service>
```
