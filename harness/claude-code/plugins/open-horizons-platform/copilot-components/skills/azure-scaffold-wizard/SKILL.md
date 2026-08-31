---
name: azure-scaffold-wizard
description: "Scaffold a complete, production-ready Azure project from scratch for any use case, including RAG chatbots, multi-agent systems, API backends, data pipelines, Azure Functions, full-stack web apps, ML training and inference, and event-driven microservices. Use when the user wants to gather requirements through adaptive questioning and generate a full project structure with source files, Bicep infrastructure, azure.yaml for azd, Docker configuration, CI/CD workflows, a README with architecture diagrams, and Responsible AI documentation targeting Azure Container Apps, Microsoft Foundry, Azure Functions, or Azure ML."
---

# Azure Scaffold Wizard — Universal Project Generator

This skill generates a **complete, production-ready Azure project** deployable with `azd up`. It is fully domain-agnostic and applies to any use case. It produces every file needed: requirements documentation, project structure with all source files, README, Azure Bicep infrastructure, `azure.yaml`, Docker configuration, CI/CD workflows, architecture diagrams, observability setup, and Responsible AI documentation.

## When to invoke

- Scaffolding a new Azure application from an empty or new project directory.
- Gathering requirements and generating a complete deployable project.
- Producing application code, Bicep, `azure.yaml`, containers, CI/CD, observability, and documentation together.

---

## Required Workflow

Follow these steps **in order**. Do not skip or reorder steps. Each step's output feeds the next.

---

### Step 1 — Identify Project Type and Gather Requirements

This is the most critical step. **Do not generate any files until this step is complete.**

#### 1A — Project Type Selection

Ask the user: **"What type of Azure project do you want to build?"**

Present these options:

| # | Project Type | Description | When to Choose |
|---|---|---|---|
| 1 | **RAG Chatbot** | Retrieval-Augmented Generation chatbot with vector search | Conversational AI grounded in your own data |
| 2 | **Multi-Agent System** | Multiple AI agents coordinated by an orchestrator | Parallel/sequential AI reasoning pipeline (Foundry compatible) |
| 3 | **API Backend** | REST or GraphQL API service | Backend service with database and Azure deployment |
| 4 | **Data Pipeline** | ETL/ELT data processing pipeline | Batch or streaming data transformation |
| 5 | **Azure Functions** | Serverless event-driven functions | Lightweight event triggers and integrations |
| 6 | **Full-Stack Web App** | Frontend + Backend web application | Complete web application with UI |
| 7 | **ML Training & Inference** | Model training and serving endpoint | Custom ML model lifecycle on Azure ML |
| 8 | **Event-Driven Microservices** | Message-based distributed system | Async decoupled services at scale |

If the user's request does not fit these categories exactly, choose the closest match or combine patterns. For detailed descriptions, read `references/project-types.md`.

#### 1B — Universal Requirements (ask for ALL project types)

| # | Question | Guidance |
|---|---|---|
| U1 | **What business problem does this solve?** | One sentence. Drives README opening and all documentation. |
| U2 | **Who are the end users?** | Drives UI design, access control decisions, RBAC roles. |
| U3 | **What is the project name?** | kebab-case slug for folder names, azure.yaml, and resource naming. |
| U4 | **Programming language?** | Python (default), TypeScript, C#, or multi-language. Drives all source file templates. |
| U5 | **Azure region?** | Default: `eastus2`. Constrain by AI model availability if applicable. |
| U6 | **Authentication required?** | None (default scaffold), Microsoft Entra ID (production). |
| U7 | **What Azure services beyond the defaults?** | e.g., Cosmos DB, Service Bus, Key Vault, Storage, Redis. Drives extra Bicep modules. |
| U8 | **Frontend required?** | Yes/No. If yes: Next.js (default), React SPA, or other. |
| U9 | **What compliance or regulatory requirements?** | e.g., HIPAA, SOC2, GDPR. Drives TRANSPARENCY_FAQ.md and security docs. |
| U10 | **Target deployment platform?** | Azure Container Apps (default), Azure Functions, AKS, App Service. |
| U11 | **Use Azure AI Foundry Agent Service?** | **Yes** (default for AI-capable types): AI processing via Foundry Hosted Agents with structured output, managed deployment, and MAF. **No**: hand-rolled code using Azure OpenAI SDK directly. **When to ask**: Type 1 (RAG) — always ask. Types 3, 4, 5, 6, 8 — ask only after the type-specific "Include AI?" question is answered Yes. **Skip for**: Type 2 (Multi-Agent, always Foundry) and Type 7 (ML Training, uses Azure ML). |

#### 1C — Type-Specific Requirements

Based on the project type selected in 1A, read the corresponding reference file and ask the type-specific questions defined there:

| Project Type | Reference File | What It Adds |
|---|---|---|
| RAG Chatbot | `references/rag-chatbot.md` | Vector store, embedding model, chunking strategy, data sources, conversation memory |
| Multi-Agent System | `references/multi-agent.md` | Agent names/roles, orchestration topology, MCP tools, Foundry model choice |
| API Backend | `references/api-backend.md` | Endpoints, database, API style (REST/GraphQL), rate limiting |
| Data Pipeline | `references/data-pipeline.md` | Data sources/sinks, scheduling, batch vs. stream, transformations |
| Azure Functions | `references/function-app.md` | Triggers, bindings, Durable Functions, runtime stack |
| Full-Stack Web App | `references/full-stack-app.md` | Frontend framework, SSR/SPA, state management, API integration |
| ML Training & Inference | `references/ml-training.md` | ML framework, compute targets, model registry, managed endpoints |
| Event-Driven Microservices | `references/event-driven.md` | Message broker, event schemas, KEDA scaling rules |

The selected reference file contains:
- Type-specific qualifying questions
- The project folder structure for that type
- Source file templates and generation instructions
- Required Bicep modules list
- Type-specific quality checklist

#### 1C-bis — Load Foundry Agent Patterns (Conditional)

If U11 = Yes (or if the project type is Multi-Agent), also read `references/foundry-agent-patterns.md`. This file provides the shared Foundry agent scaffolding patterns (agent.yaml, MAF main.py, schemas.py, skills, two-mode dispatcher, registration script) used by the type-specific reference file's "Foundry Mode" section. **Exception**: Multi-Agent projects use their own complete patterns in `references/multi-agent.md` — do not load `foundry-agent-patterns.md` for Multi-Agent.

#### 1D — Document the Requirements

Create `docs/requirements.md` with a structured summary of ALL answers organized by section: Universal (U1–U11) and Type-Specific.

---

### Step 2 — Generate Project Structure

Based on the requirements from Step 1, generate the folder layout.

Every project, regardless of type, includes these **common root files and directories**:

```
<project-slug>/
├── azure.yaml                          # azd project descriptor + hooks
├── docker-compose.yml                  # Local dev: all containers without Azure
├── docker-compose.override.yml         # Local overrides (ports, volumes, hot-reload)
├── .env.example                        # All env vars documented with descriptions
├── README.md
├── TRANSPARENCY_FAQ.md                 # Responsible AI FAQ
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
├── SUPPORT.md
├── LICENSE                             # MIT
│
├── .github/
│   └── workflows/
│       ├── ci.yml                      # PR validation: lint, type-check, test, Bicep build
│       └── deploy.yml                  # Push to main: build, push, deploy
│
├── infra/
│   ├── main.bicep                      # Subscription-scoped entry point
│   ├── main.parameters.json            # azd parameter bindings
│   ├── abbreviations.json              # Azure resource name prefix map
│   └── modules/                        # (varies by project type + U7 choices)
│
├── scripts/
│   ├── preprovision.sh                 # Region + model validation (posix)
│   ├── preprovision.ps1                # Region + model validation (windows)
│   ├── postprovision.sh                # Build, push, register (posix)
│   └── postprovision.ps1               # Build, push, register (windows)
│
├── docs/
│   ├── requirements.md                 # Output of Step 1
│   ├── architecture.md                 # Narrative architecture description
│   ├── DeploymentGuide.md              # Step-by-step azd up walkthrough
│   ├── production-migration.md         # Scaffold → production gaps
│   ├── troubleshooting.md              # Common errors + fixes
│   └── images/
│       └── readme/
│           ├── solution-architecture.svg
│           └── pipeline-flow.svg       # (if applicable)
│
└── <type-specific directories from reference file>
```

Read the type-specific reference file (loaded in Step 1C) for the additional directories and files specific to the selected project type.

---

### Step 3 — Generate Type-Specific Source Files

Follow the **generation instructions** in the type-specific reference file loaded in Step 1C. This step produces the core application code.

Examples of what each type generates:
- **RAG Chatbot**: ingestion pipeline, vector store client, retrieval chain, chat API, prompt templates
- **Multi-Agent System**: agent containers with agent.yaml, schemas, skills, orchestrator backend, two-mode dispatcher
- **API Backend**: routers, models, services, middleware, database migrations
- **Data Pipeline**: pipeline definitions, transformers, connectors, scheduling config
- **Azure Functions**: function triggers, bindings, orchestrations, shared utilities
- **Full-Stack Web App**: frontend components, API client, backend endpoints, shared types
- **ML Training**: training scripts, model definitions, inference endpoints, evaluation
- **Event-Driven**: message handlers, event schemas, saga orchestrators, dead-letter processors

Generate ALL source files with complete, functional code — not placeholders or stubs.

**When U11 = Yes (Foundry mode):** The Foundry agent patterns from `references/foundry-agent-patterns.md` produce additional files: an `agents/` directory with agent.yaml, main.py, schemas.py, skills/, plus a dispatcher (`hosted_agents.py`) and registration script (`register_agents.py`). The type-specific reference file specifies exactly which parts of the existing code the Foundry agent **replaces** vs which parts it **augments**.

---

### Step 4 — Generate Azure Infrastructure and Deployment

#### 4A — Bicep Infrastructure

Read `references/bicep-patterns.md` for universal Bicep patterns.

Generate `infra/main.bicep` (subscription-scoped) and all required modules.

**Base modules for ALL project types:**
- `monitoring.bicep` — App Insights + Log Analytics workspace
- `container-registry.bicep` — ACR (if containerized, which is most types)
- `container-apps-env.bicep` — Managed Environment (if U10 = ACA)
- `container-app.bicep` — Reusable per-app module
- `role-assignments.bicep` — RBAC for all managed identities

**Add type-specific modules** as listed in the loaded reference file (e.g., `ai-foundry.bicep` for RAG/Multi-Agent, `ai-search.bicep` for RAG, `function-app.bicep` for Functions).

**Add optional service modules** based on U7 answers: `cosmos.bicep`, `storage.bicep`, `keyvault.bicep`, `servicebus.bicep`, etc.

#### 4B — azure.yaml and Hook Scripts

Read `references/azure-yaml-patterns.md`.

Generate:
- `azure.yaml` with preprovision and postprovision hooks
- `scripts/preprovision.sh` + `scripts/preprovision.ps1` — validate region, model availability, exit non-zero on failure
- `scripts/postprovision.sh` + `scripts/postprovision.ps1` — ACR login, image build with timestamp tag, registration

#### 4C — Docker Configuration

Read `references/docker-patterns.md`.

Generate:
- `Dockerfile` for each service (multi-stage, non-root user, health checks)
- `docker-compose.yml` for local development
- `docker-compose.override.yml` for local overrides
- `.dockerignore` per service

#### 4D — Observability Setup

Read `references/observability-patterns.md` for OpenTelemetry + Azure Monitor patterns.

Configure observability in all backend/API entry points:
- Azure Application Insights integration via OpenTelemetry
- Structured JSON logging
- Custom trace attributes for domain-specific telemetry
- FastAPI/Express lifespan integration

---

### Step 5 — Generate Documentation and Architecture

#### 5A — README.md

Read `references/readme-template.md` for the section template and conventions.

Generate a complete README with all required sections populated from requirements — no placeholder text.

#### 5B — Architecture Diagrams

Read `references/architecture-diagrams.md` for SVG generation prompts and conventions.

Generate:
- `docs/images/readme/solution-architecture.svg` — Azure resource topology diagram
- `docs/images/readme/pipeline-flow.svg` — Data/agent flow diagram (if applicable)

SVG requirements: `viewBox` + `preserveAspectRatio`, `system-ui` fonts, no external imports, under 50KB.

#### 5C — Responsible AI Documents

Read `references/responsible-ai.md` for the TRANSPARENCY_FAQ.md template.

Generate `TRANSPARENCY_FAQ.md` addressing all 6 required questions, populated with project-specific content from Step 1.

#### 5D — CI/CD Workflows

Read `references/cicd-patterns.md`.

Generate `.github/workflows/ci.yml` and `.github/workflows/deploy.yml` with language-appropriate steps.

#### 5E — Supporting Documents

Generate:
- `docs/architecture.md` — narrative description of the architecture
- `docs/DeploymentGuide.md` — step-by-step `azd up` walkthrough
- `docs/production-migration.md` — gaps between scaffold and production (auth, storage, scaling, security)
- `docs/troubleshooting.md` — common errors and fixes
- `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`

#### 5F — Production Security Documentation

Read `references/security-patterns.md` for authentication, RBAC, Key Vault, and network isolation patterns.

Use these patterns to populate `docs/production-migration.md` with specific guidance for:
- Microsoft Entra ID integration (app registration, token validation)
- Role-based access control aligned with end users (U2)
- Azure Key Vault secret management
- VNet injection and private endpoints
- Input validation and sanitization

---

### Step 6 — Quality Checklist

Run through this checklist before delivering. Every item must pass.

#### Universal Checks (all project types)

**Requirements & Documentation:**
- [ ] `docs/requirements.md` exists with all U1–U11 + type-specific answers
- [ ] `TRANSPARENCY_FAQ.md` covers all 6 required questions
- [ ] README includes all required sections with no placeholder text
- [ ] `docs/production-migration.md` documents all production gaps

**Infrastructure:**
- [ ] `main.bicep` is subscription-scoped (`targetScope = 'subscription'`)
- [ ] All secrets use `@secure()` — no plain-text secret outputs
- [ ] `main.parameters.json` binds all params to `${AZURE_*}` azd env vars
- [ ] Role assignments grant appropriate roles to all managed identities

**azure.yaml & Deployment:**
- [ ] `IMAGE_TAG` is always a timestamp (`YYYYMMDDHHmmss`), never `latest`
- [ ] Preprovision hook validates region and exits non-zero on failure
- [ ] Postprovision hook validates images before registration
- [ ] Hooks have both `windows` (pwsh) and `posix` (sh) variants

**Docker:**
- [ ] All Dockerfiles use non-root user
- [ ] `docker-compose.yml` enables full local development without Azure
- [ ] `.env.example` documents ALL required environment variables

**CI/CD:**
- [ ] `ci.yml` has lint + type-check + test + Bicep validation steps
- [ ] `deploy.yml` builds, pushes, and deploys on main branch

**Architecture Diagrams:**
- [ ] All SVGs use `viewBox` + `preserveAspectRatio="xMidYMid meet"`
- [ ] No external font imports (use `system-ui`)
- [ ] SVGs render correctly in a browser

**Observability:**
- [ ] App Insights connection string configured in all containers
- [ ] OTel trace setup in backend/API entry point

#### Type-Specific Checks

Run the quality checklist defined in the loaded type-specific reference file from Step 1C.

#### Foundry Agent Checks (if U11 = Yes)

Run these in addition to Universal and Type-Specific checks:

- [ ] `agent.yaml` has meaningful `description:` (2-3 sentences, not a placeholder)
- [ ] `main.py` uses `default_options={"response_format": Schema}` for structured output
- [ ] `schemas.py` has `confidence_score`, `confidence_level`, `summary`, and `errors` fields
- [ ] `skill.md` defines role, input contract, step-by-step instructions, and output requirements
- [ ] `register_agents.py` passes `description=agent_def["description"]` to `create_version()`
- [ ] `hosted_agents.py` correctly switches between Foundry mode and direct HTTP mode
- [ ] `docker-compose.yml` does NOT set `AZURE_AI_PROJECT_ENDPOINT` on the backend (enables local mode)
- [ ] `ai-foundry.bicep` module is included in `infra/main.bicep`
- [ ] RBAC includes both `Cognitive Services OpenAI User` and `Azure AI User` roles
- [ ] Postprovision hook calls `register_agents.py`

## Output template

```markdown
## Azure scaffold result

- Project: `<name and project type>`
- Location: `<folder>`
- Azure target: `<compute and dependent services>`
- Generated surfaces: `<application, infrastructure, CI/CD, documentation>`
- Validation: `<commands and results>`
- Deployment command: `azd up`
```

## Quality gate

- [ ] Universal and type-specific requirements are resolved.
- [ ] Generated source, infrastructure, deployment, and documentation surfaces are complete.
- [ ] Secrets are externalized and managed identities are used where supported.
- [ ] Images use explicit tags and generated workloads use secure defaults.
- [ ] Bicep, application checks, container configuration, and links validate.
