# GitHub Copilot Instructions — Legacy Modernization Workshop

> These instructions tell Copilot what your team is building, which stack to use,
> which conventions to follow, and what NOT to do. They apply to the team's entire
> repository.

## Approved Tools — These Only

This workshop uses a **fixed toolchain**: VS Code, GitHub Copilot (Ask + Plan + Agent modes), GitHub Spec-Kit, GitHub, Docker / Docker Compose, and Terraform. Other AI assistants, IDEs, web chat UIs, and SDD frameworks are not permitted because mixing tools breaks specification → code → test traceability.

## Project Context

Modernization of the Natural/Adabas **SIFAP** legacy system (Payment Inspection and Administration System) to Java 21 + Next.js 15. Treat historical corpus counts as fixture assumptions until checked against the [system profile](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-modernization-context/references/system-profile.md) and [source layout](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-modernization-context/references/source-layout.md).

The maintained kit uses five evidence-gated stage agents. See the [workshop orchestration skill](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-workshop-orchestration/SKILL.md).

Use the skills in [`.github/skills/`](.github/skills/) for specialized workflows. Copilot selects the relevant skill from its description; do not duplicate specialized workflows in these global instructions.

## Target Stack

- **Backend:** Java 21 + Spring Boot 3.3 + JPA/Hibernate + PostgreSQL 16
- **Frontend:** Next.js 15 (App Router) + TypeScript 5 (strict) + Tailwind CSS + shadcn/ui
- **Containers:** Docker + Docker Compose created by the team in Stage 3/4 when necessary
- **IaC:** Terraform (Azure provider ~> 3.x)
- **CI/CD:** GitHub Actions
- **Testing:** JUnit 5 + Testcontainers (backend); Vitest + Testing Library (frontend)

## Cross-Cutting Implementation Rules

Detailed Java, TypeScript, database, security, infrastructure, and test rules live in [`.github/instructions/`](.github/instructions/) and load automatically for matching paths.

- Use English class names and comments.
- Path REST APIs as `/api/v1/{resource}`.
- Validate inputs at every system boundary.
- Never hardcode secrets, API keys, or credentials.
- Never expose sensitive data (CPF, benefit amounts) in logs — mask it.
- Configure CORS explicitly — no `*` wildcard in production.
- Use Managed Identity for Azure service-to-service authentication.
- Write tests during implementation, not after the fact.

## Spec-Driven Development (Spec-Kit)

- Every requirement uses **EARS notation** (Easy Approach to Requirements Syntax)
- Every requirement has a unique **REQ-ID** in the `REQ-NNN` format
- **Every requirement includes a `source_legacy:` line** pointing to legacy files or `[GREENFIELD] + justification.`
  Use `01-archaeology/legacy-sifap/natural-programs/*.{NSP,NSN,NSS,NSA,NSL,NSC,NSM,jcl}` or `01-archaeology/legacy-sifap/adabas-ddms/*.{NSD,ddm,txt}` for legacy-backed requirements.
  The traceability gate rejects PRs that violate this rule. See the [SIFAP traceability skill](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-requirements-traceability/SKILL.md).
- Tests trace to REQ-IDs through inline comments
- Branch strategy: one prefix per persona/stage, each cut from `develop` (never from `spec/*`) and merged back `develop` → `main`; there is no `stage` branch.
  - `spec/<NNN>-<feature>` — RE + SA, Stage 2
  - `impl/<NNN>-<feature>` — Dev + DBA + QA, Stage 3
  - `infra/<component>` — DevOps, Stage 4
  - `docs/<topic>` — Tech Writer
  - `agent/<issue-NN>` — Copilot Agent
  - Do not collapse `impl/` — or any other prefix — into `spec/`.
  - Full stage guidance: [workshop flow](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-modernization-context/references/workshop-flow.md)
- Before writing EARS requirements in Stage 2, the pair MUST have read their assigned Natural programs (HARD GATE — see the checklist above)

## Strict Rules — Do Not Do This

- ❌ Do not assume a pre-existing application prototype, containerization, or infrastructure tree. Inspect the target and follow the [source layout contract](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-modernization-context/references/source-layout.md).
- ❌ Do not write an EARS requirement without `source_legacy:` — CI will reject the PR
- ❌ Do not add dependencies without justification in an ADR
- ❌ Do not write tests after the fact — write them during implementation
- ❌ Do not expose secrets in commit messages, logs, or PR descriptions
- ❌ Do not merge into `main` without at least one peer review
- ❌ Do not skip evidence-gated stage handoffs; follow the [workshop flow](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-modernization-context/references/workshop-flow.md).
- ❌ Do not create a root `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. The official `.github/copilot-instructions.md` file is the repository-wide source for this kit.
- ❌ Do not add or edit a Copilot primitive outside the [harness contract](../../COPILOT-HARNESS-SPEC.md) and canonical plugin.

## References

- Workshop flow: [workshop-flow.md](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-modernization-context/references/workshop-flow.md)
- SIFAP source layout: [source-layout.md](../../../harness/github-copilot/plugins/mainframe-natural-adabas/skills/sifap-modernization-context/references/source-layout.md)
- Stage agents and capabilities: [canonical plugin README](../../../harness/github-copilot/plugins/mainframe-natural-adabas/README.md)
- Primitive governance: [COPILOT-HARNESS-SPEC.md](../../COPILOT-HARNESS-SPEC.md)
- Runtime evidence: [HARNESS-VALIDATION.md](../../HARNESS-VALIDATION.md)
- Spec-Kit SDD: <https://github.com/github/spec-kit>
