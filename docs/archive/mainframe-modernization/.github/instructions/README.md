# Instructions Index

This directory contains the GitHub Copilot file-specific instructions for the workshop.

> Important: Copilot discovers `*.instructions.md` files in `.github/instructions/` and its subdirectories. This workshop keeps them directly in this directory so the index and scopes are easy to review.

## Instruction Files

| File | Description | `applyTo` scope |
| --- | --- | --- |
| `agent-skills.instructions.md` | Use when authoring, reviewing, or debugging GitHub Copilot Agent Skills — SKILL.md frontmatter, the name-equals-directory rule, description tuning, and progressive disclosure. | `.github/skills/**/SKILL.md` |
| `backend.instructions.md` | Use when implementing backend APIs, services, controllers, request validation, error handling, and business service boundaries. | `backend/src/main/java/**,backend/src/test/java/**` |
| `cicd.instructions.md` | Use when creating or reviewing GitHub Actions, CI/CD workflows, YAML pipeline gates, build checks, and deployment automation. | `.github/workflows/**,.github/actions/**,**/action.yml,**/action.yaml` |
| `database.instructions.md` | Use when writing database repositories, migrations, schema changes, SQL queries, indexes, and rollback-safe data changes. | `backend/src/main/java/**/infrastructure/**,backend/src/main/resources/db/migration/**` |
| `draw-io.instructions.md` | Use when creating, editing, or reviewing draw.io diagrams and mxGraph XML in .drawio, .drawio.svg, or .drawio.png files. | `**/*.drawio,**/*.drawio.svg,**/*.drawio.png` |
| `frontend-spec.instructions.md` | Use when implementing or reviewing Next.js 15 App Router, TypeScript, Tailwind CSS, shadcn/ui, and server components under frontend/. | `frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**,frontend/**/*.ts,frontend/**/*.tsx` |
| `frontend.instructions.md` | Use when building frontend UI components, pages, client interactions, component state, accessibility, and user-facing flows. | `frontend/app/**,frontend/components/**,frontend/src/app/**,frontend/src/components/**` |
| `infrastructure.instructions.md` | Use when creating or reviewing infrastructure as code, Terraform, Bicep, Azure resource definitions, and environment configuration. | `infra/**,**/*.tf,**/*.bicep,compose*.yml,compose*.yaml,docker-compose*.yml,docker-compose*.yaml` |
| `java-junit5-assertions.instructions.md` | Use when writing or reviewing JUnit 5 (Jupiter) assertions in backend Java tests — expected-value ordering, lazy messages, assertAll, assertThrows/assertThrowsExactly, timeouts, and assertInstanceOf. | `**/*Test.java,**/*IT.java,**/*Steps.java,**/*StepDefs.java` |
| `modular-monolith.instructions.md` | Use when designing or reviewing Modular Monolith architecture, package-by-feature boundaries, JPA mapping, and Strangler Fig migration. | `backend/src/main/java/**,backend/pom.xml,backend/build.gradle*` |
| `natural-adabas.instructions.md` | Use when reading Natural/Adabas legacy code, language patterns, FDT structure, naming conventions, and batch flows. | `01-archaeology/legacy-sifap/**,**/*.NSP,**/*.nsp,**/*.NSN,**/*.nsn,**/*.NSS,**/*.nss,**/*.NSA,**/*.nsa,**/*.NSL,**/*.nsl,**/*.NSC,**/*.nsc,**/*.NSM,**/*.nsm,**/*.NSD,**/*.nsd,**/*.NAT,**/*.nat,**/*.CPY,**/*.cpy,**/*.DDM,**/*.ddm,**/*.jcl,**/*.JCL` |
| `requirements.instructions.md` | Use when writing or reviewing requirements, EARS specifications, acceptance criteria, traceability, and docs-backed requirements. | `docs/**/*.md,specs/**/*.md,02-modern-spec/**/*.md` |
| `security.instructions.md` | Use when implementing or reviewing authentication, authorization, crypto, secure configuration, secrets handling, and security-sensitive code. | `backend/src/main/java/**/auth/**,backend/src/main/java/**/security/**,backend/src/main/java/**/config/**,backend/src/main/resources/**,frontend/**/auth/**,frontend/**/middleware.ts` |
| `terraform.instructions.md` | Use for generic Terraform hygiene (file layout, variables, outputs, formatting, validation, testing, state); kit Azure rules live in infrastructure.instructions.md. | `**/*.tf` |
| `tests.instructions.md` | Use when creating or reviewing automated tests, test strategy, specs, coverage gaps, regression tests, and quality gates. | `**/*.test.*,**/*.spec.*,**/tests/**` |

## Maintenance Rule

- Every file MUST maintain valid YAML frontmatter with exactly the needed `description` and `applyTo` fields.
- `applyTo` is a single quoted string; multiple globs are comma-separated with no spaces after commas.
- Avoid `applyTo: "**"`; prefer specific globs that match the files the instruction truly governs.
- Keep the house pattern consistent: intro paragraph -> topical sections -> `## Conventions` -> `## Do / Do Not` -> `## Checklist Before Opening a PR`.
- When creating a new area, add a new flat `*.instructions.md` file in this directory and update this index.
