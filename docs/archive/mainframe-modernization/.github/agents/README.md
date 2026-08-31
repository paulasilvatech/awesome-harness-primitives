# Agents Index

This directory contains the GitHub Copilot custom agents for the workshop — **17** in total, each in its own `<name>.agent.md`.

> [!NOTE]
> Copilot discovers `*.agent.md` files in `.github/agents/`. Invoke an agent by its `name` with `@<name>` (for example `@archaeologist`). The `name` also binds prompts: a `*.prompt.md` file selects its agent through the `agent:` frontmatter key, so an agent's id is a contract, not a label.

The kit uses **two agent layers** — this is the core mental model, so the agents are grouped by layer rather than listed flat:

- **Stage agents (4)** — one per workshop stage, used sequentially across the day.
- **Persona agents (10)** — one per team role, used by the pair that owns that role.

Three further **specialist agents** sit outside both layers; they add depth for specific work and are listed last.

## Stage agents

Four sequential agents, one per workshop stage. They chain through the `handoffs:` frontmatter key — `archaeologist -> architect -> builder` each hand off to the next; the terminal Stage 4 agent (`evolution`) has none.

| Stage | Agent | Invoke | Bound prompts | Description |
| --- | --- | --- | --- | --- |
| Stage 1 | [`archaeologist`](archaeologist.agent.md) | `@archaeologist` | 5 | Stage 1 agent — reads legacy Natural/Adabas code, extracts business rules, maps dependencies, and records open questions |
| Stage 2 | [`architect`](architect.agent.md) | `@architect` | 4 | Stage 2 agent — defines bounded contexts, writes EARS specifications, generates ADRs, and designs a Modular Monolith architecture |
| Stage 3 | [`builder`](builder.agent.md) | `@builder` | 5 | Stage 3 agent — translates Natural to Java, generates JPA from FDTs, writes equivalence tests, and builds REST + Next.js |
| Stage 4 | [`evolution`](evolution.agent.md) | `@evolution` | 4 | Stage 4 agent — writes GitHub issues for Copilot Agent, reviews AI-generated PRs, and configures CI/CD and IaC |

## Persona agents

Ten agents, one per team role. The Developer persona is served by the [`implementer`](implementer.agent.md) agent, so its prompts are named `persona-developer-*` but bind to `agent: "implementer"`.

| Agent | Invoke | Bound prompts | Description |
| --- | --- | --- | --- |
| [`product-owner`](product-owner.agent.md) | `@product-owner` | 3 | Product Owner assistant for writing specifications, refining the backlog, and validating acceptance with EARS notation and the SDD workflow |
| [`requirements-engineer`](requirements-engineer.agent.md) | `@requirements-engineer` | 4 | Requirements engineering assistant for EARS notation, specification validation, and legacy-traceable requirements in the SDD workflow |
| [`enterprise-architect`](enterprise-architect.agent.md) | `@enterprise-architect` | 3 | Enterprise architecture assistant for the Spec-Kit constitution, ADRs, external integration mapping, and cross-cutting design |
| [`software-architect`](software-architect.agent.md) | `@software-architect` | 3 | Software architecture assistant for CODEMAP, bounded contexts, module topology, and API contracts |
| [`tech-lead`](tech-lead.agent.md) | `@tech-lead` | 3 | Technical leadership assistant for CODEMAP and context curation, Copilot usage guidance, and code-review standards |
| [`implementer`](implementer.agent.md) | `@implementer` | 6 | Implementation assistant for Java 21 and Next.js 15 — TDD, bug fixing, and refactoring with REQ-ID traceability |
| [`dba`](dba.agent.md) | `@dba` | 4 | Database assistant for PostgreSQL migrations, query optimization, indexing strategy, and SQL-injection auditing |
| [`qa-engineer`](qa-engineer.agent.md) | `@qa-engineer` | 5 | Quality assurance assistant for test generation from specs, coverage-gap analysis, and CI quality gates |
| [`devops-engineer`](devops-engineer.agent.md) | `@devops-engineer` | 5 | DevOps assistant for GitHub Actions pipelines, Terraform IaC, container builds, observability, and incident analysis |
| [`tech-writer`](tech-writer.agent.md) | `@tech-writer` | 5 | Technical writing assistant for API docs, runbooks, ADRs, CODEMAP, and Diátaxis-style content with drift detection |

## Specialist agents

Three depth specialists that fit neither the Stage nor the persona layer. Each owns **no** prompts; invoke them directly with `@<name>`.

| Agent | Invoke | Bound prompts | Description |
| --- | --- | --- | --- |
| [`se-ux-ui-designer`](se-ux-ui-designer.agent.md) | `@se-ux-ui-designer` | 0 | UX/UI research specialist for the SIFAP modern UI — Jobs-to-be-Done, user journeys, and accessibility specs that feed the frontend build. Use for research and design intent; use @expert-react-frontend-engineer or @implementer to write the actual Next.js code. |
| [`expert-react-frontend-engineer`](expert-react-frontend-engineer.agent.md) | `@expert-react-frontend-engineer` | 0 | Frontend depth specialist for the SIFAP UI — React 19 + Next.js 15 App Router, Server/Client boundaries, Server Actions, optimistic UI, accessibility, and performance. Use for frontend-heavy work; use @implementer for a single traceable tasks.md item or any backend change. |
| [`java-mcp-expert`](java-mcp-expert.agent.md) | `@java-mcp-expert` | 0 | Greenfield specialist for building Model Context Protocol (MCP) servers in Java with the official MCP Java SDK, Project Reactor, and Spring Boot 3.3. Use when a team extends the toolchain with a custom MCP server; the SIFAP legacy-to-Java modernization itself belongs to @archaeologist, @architect, and @builder. |

## Prompt ownership

The 59 prompts in [`../prompts/`](../prompts/) bind to an agent through their `agent:` key:

- All **59** bind to one of the **14** named agents above (Stage + persona) — no prompt is left on the generic built-in `agent: "agent"`. The per-agent counts are in the tables' **Bound prompts** columns.
- The three specialist agents (`se-ux-ui-designer`, `expert-react-frontend-engineer`, `java-mcp-expert`) own **0** prompts and are invoked directly.

Regenerate the counts with `grep -h '^agent:' ../prompts/*.prompt.md | sort | uniq -c`.

## Maintenance Rule

- Renaming an agent silently breaks **every** prompt bound to it via `agent:`; rename the agent and all its prompt bindings together, then re-run the validator.
- `description` is the only frontmatter key the gate strictly requires; `handoffs` is for Stage agents only and only when a next stage exists.
- The required body sections (`Mission`, `Lead Personas`, `Operating Principles`, `What This Agent Knows`, `What This Agent Does NOT Know`, `Available Prompts`, a `Definition of Done` heading, `Anti-Patterns This Agent Rejects`, `Spec-Kit Integration`) and the full schema are defined in [`../PRIMITIVE-STANDARD.md`](../PRIMITIVE-STANDARD.md) and enforced by [`../scripts/validate-copilot-primitives.py`](../scripts/validate-copilot-primitives.py).
- When you add an agent, add its row to the correct layer above and, if a prompt should invoke it, set that prompt's `agent:` to this `name`.
