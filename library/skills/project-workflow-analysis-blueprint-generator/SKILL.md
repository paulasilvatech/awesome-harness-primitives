---
name: project-workflow-analysis-blueprint-generator
description: >-
  Generate technology-agnostic project workflow analysis blueprints that document end-to-end application flows, files, classes, entry points, service layers, data access, error handling, async processing, sequence diagrams, testing patterns, and implementation templates. Use this skill when the user asks to list all files/classes in a workflow, document representative workflows, map an API-to-database flow, or create an implementation-ready workflow blueprint.
---

# Project workflow analysis blueprint generator

Generate a reusable analysis prompt that makes GitHub Copilot inspect a codebase and document representative end-to-end workflows as implementation blueprints grounded in actual files, classes, methods, data paths, error handling, and tests.

## When to invoke

- "List all files and classes involved in this workflow."
- "Document the end-to-end API flow for this feature."
- "Generate a workflow blueprint for this project."
- "Map the service, repository, data access, and test patterns."
- "Create implementation templates based on existing workflows."

## Configuration variables

Preserve these variables in the generated blueprint when the user supplies them; otherwise use the defaults and tell the downstream agent to auto-detect.

| Variable | Values | Purpose |
| --- | --- | --- |
| `${PROJECT_TYPE}` | `Auto-detect`, `.NET`, `Java`, `Spring`, `Node.js`, `Python`, `React`, `Angular`, `Microservices`, `Other` | Primary technology stack. |
| `${ENTRY_POINT}` | `API`, `GraphQL`, `Frontend`, `CLI`, `Message Consumer`, `Scheduled Job`, `Custom` | Starting point for the flow. |
| `${PERSISTENCE_TYPE}` | `Auto-detect`, `SQL Database`, `NoSQL Database`, `File System`, `External API`, `Message Queue`, `Cache`, `None` | Data storage or external persistence mechanism. |
| `${ARCHITECTURE_PATTERN}` | `Auto-detect`, `Layered`, `Clean`, `CQRS`, `Microservices`, `MVC`, `MVVM`, `Serverless`, `Event-Driven`, `Other` | Primary architecture pattern. |
| `${WORKFLOW_COUNT}` | `1-5` | Number of representative workflows to document. |
| `${DETAIL_LEVEL}` | `Standard`, `Implementation-Ready` | Depth of implementation detail. |
| `${INCLUDE_SEQUENCE_DIAGRAM}` | `true`, `false` | Whether to generate a sequence diagram. |
| `${INCLUDE_TEST_PATTERNS}` | `true`, `false` | Whether to include testing approach. |

## Detection rules

| Area | Auto-detect evidence |
| --- | --- |
| Technology | `.sln`, `*.csproj`, `pom.xml`, `build.gradle`, `package.json`, `requirements.txt`, `pyproject.toml`, React/Angular config, Dockerfiles, and service manifests. |
| Entry points | API controllers or route definitions, GraphQL resolvers, UI components that initiate requests, CLI commands, message handlers, event subscribers, scheduled jobs. |
| Persistence | `DbContext`, connection configuration, repository implementations, ORM mappings, SQL files, document-store clients, external API clients, queue producers/consumers, cache clients, file-system paths. |
| Architecture | Folder structure, dependency direction, naming conventions, interfaces, use cases/interactors, CQRS handlers, MVC/MVVM components, service boundaries, event-driven adapters. |

## Workflow blueprint content

For each of the `${WORKFLOW_COUNT}` most representative workflows, require these sections.

| Section | Required detail |
| --- | --- |
| Workflow overview | Name, business purpose, trigger action/event, and all files/classes involved in the complete workflow. |
| Entry point implementation | Controller/route/resolver/component/handler/job class and method; complete signature; attributes or annotations; request DTO/model; validation; authentication/authorization. |
| Service layer implementation | Service classes, dependencies, interfaces, method signatures, return types, key business logic, dependency injection registration. |
| Data mapping patterns | DTO-to-domain mapping, mapper configuration or manual methods, validation during mapping, domain events. |
| Data access implementation | Repository interfaces and implementations, query methods, entity/model definitions, transaction handling, ORM or SQL details. |
| Response construction | Response DTO/model, domain-to-response mapping, status-code selection, error response structure. |
| Error handling patterns | Exception types, try/catch locations, global exception handlers, logging, retry policies, circuit breakers, compensating actions. |
| Asynchronous processing | Background jobs, event publication, queue send/receive, callbacks, webhooks, monitoring of async operations. |
| Naming conventions | Controller, service, repository, DTO, CRUD method, variable, and file organization patterns. |
| Implementation templates | Starter templates for a new endpoint, service method, repository method, domain model, and error handling path. |

Conditional sections:

| Condition | Add this detail |
| --- | --- |
| `${ARCHITECTURE_PATTERN}` is `CQRS` or `Auto-detect` | Complete command/query handler implementations. |
| `${ARCHITECTURE_PATTERN}` is `Clean` or `Auto-detect` | Use case/interactor implementations. |
| `${PERSISTENCE_TYPE}` is `SQL Database` or `Auto-detect` | ORM configuration, annotations, Fluent API usage, actual SQL queries or ORM statements. |
| `${PERSISTENCE_TYPE}` is `NoSQL Database` or `Auto-detect` | Document structures and query/update operations. |
| `${INCLUDE_TEST_PATTERNS}` is `true` | Unit tests for each layer, mocks, fixtures, integration tests, test data generation, API/controller tests. |
| `${INCLUDE_SEQUENCE_DIAGRAM}` is `true` | Sequence diagram with components, method calls, parameter types, return values, conditionals, and error paths. |

## Technology-specific patterns

| Technology | Blueprint must extract |
| --- | --- |
| `.NET` | Controller attributes, filters, dependency injection, `Startup.cs` or `Program.cs`, Entity Framework `DbContext`, EF Core or Dapper repository, AutoMapper profiles, middleware, extension methods, Options pattern, `ILogger`, authentication/authorization filters or policies. |
| `Java` / `Spring` | Controller annotations, dependency injection, service transaction boundaries, repository interfaces and implementations, JPA entities and relationships, DTOs, bean configuration, component scanning, exception handlers, custom validators. |
| `React` | Component props and state, `useState`, `useEffect`, custom hooks, API service implementation, Context or Redux state management, form handling, route configuration. |
| `Microservices` | Service boundaries, API contracts, messaging, retries, idempotency, compensation, observability, and cross-service data ownership. |

## Generated blueprint

Use this prompt body as the generated artifact, filling variables with user values or defaults:

```markdown
Analyze the codebase and document `${WORKFLOW_COUNT}` representative end-to-end workflows that can serve as implementation templates for similar features.

## Initial detection

- Project type: `${PROJECT_TYPE}`. If `Auto-detect`, inspect project files and configuration to identify languages, frameworks, and primary architecture.
- Entry point: `${ENTRY_POINT}`. If `Auto-detect`, find API controllers/routes, GraphQL resolvers, frontend event sources, CLI commands, message consumers, or scheduled jobs.
- Persistence: `${PERSISTENCE_TYPE}`. If `Auto-detect`, inspect database contexts, repositories, ORM mappings, external API clients, queues, caches, and file-system usage.
- Architecture: `${ARCHITECTURE_PATTERN}`. If `Auto-detect`, infer from folder structure, dependency direction, handlers, services, controllers, ViewModels, and event adapters.

## Per-workflow documentation

For each workflow:
1. Name the workflow, business purpose, trigger, and all files/classes involved.
2. Document the entry point with full signature, attributes/annotations, request DTO/model, validation, and authentication/authorization.
3. Document service classes, dependencies, interfaces, method signatures, return types, and key business logic.
4. Document DTO/domain mapping, mapper configuration or manual methods, validation, and domain events.
5. Document repositories, entities/models, transaction handling, SQL/ORM/document/queue/API operations, and persistence boundaries.
6. Document response models, status-code selection, and error response generation.
7. Document exception types, try/catch patterns, global handlers, logging, retries, circuit breakers, and compensating actions.
8. Document async jobs, events, queues, callbacks, webhooks, and monitoring.
9. If `${INCLUDE_TEST_PATTERNS}` is `true`, document unit, integration, API/controller, fixture, mocking, and test-data patterns.
10. If `${INCLUDE_SEQUENCE_DIAGRAM}` is `true`, generate a detailed sequence diagram with method calls, parameter types, return values, conditional flows, and errors.
11. Document naming conventions for controllers, services, repositories, DTOs, CRUD methods, variables, and file layout.
12. Provide implementation templates for a new endpoint, service method, repository method, domain model, and error handling path.

## Technology extraction

- For `.NET`, include controllers, filters, DI in `Startup.cs` or `Program.cs`, Entity Framework `DbContext`, EF Core or Dapper, AutoMapper, middleware, extension methods, Options, `ILogger`, and auth policies.
- For `Spring`, include annotations, transaction boundaries, repositories, JPA entities, DTOs, beans, component scanning, exception handlers, and validators.
- For `React`, include props/state, hooks, API clients, Context/Redux, forms, and routes.

## Implementation guidance

Conclude with step-by-step guidance for adding similar features, including where to start, the implementation order such as model → repository → service → controller, extension points, configuration-driven behavior, performance considerations, and common pitfalls.
```

## Gotchas

- **Do not invent patterns**: the blueprint must instruct GitHub Copilot to use only files and conventions actually found in the codebase.
- **Do not stop at a class list**: require signatures, dependencies, data movement, errors, and tests.
- **Representative means reusable**: choose workflows that teach future feature implementation, not one-off wiring.
- **Sequence diagrams must include errors**: happy-path-only diagrams miss rollback, retries, and compensating actions.


## Naming and evidence vocabulary

Require the downstream workflow document to capture concrete names and examples such as `EntityNameController`, `EntityNameService`, `IEntityNameRepository`, `EntityNameRequest`, and `EntityNameResponse`. For `Java/Spring` and `Node.js/Express`, inspect `solutions/projects`, `context/connection` configuration, `query/mutation` schema entries, `Authentication/authorization` annotations, `domain/entity` mapping, `cross-cutting` concerns, and `error-prone` extension points.

## Output template

```markdown
## Project workflow blueprint

**Status:** generated | blocked
**Project type:** `${PROJECT_TYPE}`
**Entry point:** `${ENTRY_POINT}`
**Persistence:** `${PERSISTENCE_TYPE}`
**Architecture:** `${ARCHITECTURE_PATTERN}`
**Workflow count:** `${WORKFLOW_COUNT}`

### Blueprint prompt
```markdown
<complete prompt for GitHub Copilot to analyze and document workflows>
```

### Variables used
| Variable | Value |
| --- | --- |
| `${DETAIL_LEVEL}` | `<value>` |
| `${INCLUDE_SEQUENCE_DIAGRAM}` | `<true|false>` |
| `${INCLUDE_TEST_PATTERNS}` | `<true|false>` |
```

## Quality gate

- [ ] The generated blueprint preserves all configured `${PROJECT_TYPE}`, `${ENTRY_POINT}`, `${PERSISTENCE_TYPE}`, `${ARCHITECTURE_PATTERN}`, `${WORKFLOW_COUNT}`, `${DETAIL_LEVEL}`, `${INCLUDE_SEQUENCE_DIAGRAM}`, and `${INCLUDE_TEST_PATTERNS}` values.
- [ ] The blueprint requires actual codebase evidence before documenting patterns.
- [ ] Each workflow asks for all files/classes, entry point, service layer, mapping, data access, response, error handling, async behavior, naming, and templates.
- [ ] Optional sequence diagram and testing sections appear only when their variables require them.
- [ ] Technology-specific guidance is conditional and does not mandate a stack that was not detected.
