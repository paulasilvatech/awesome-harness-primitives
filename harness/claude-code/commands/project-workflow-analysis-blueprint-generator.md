---
description: >-
  Generate an implementation-ready blueprint that documents end-to-end application workflows
  across the detected project architecture.
argument-hint: >-
  PROJECT_TYPE=<Auto-detect|.NET|Java|Spring|Node.js|Python|React|Angular|Microservices|Other>
  WORKFLOW_COUNT=<1-5>
---

<!-- Generated from harness/github-copilot/prompts/project-workflow-analysis-blueprint-generator.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /project-workflow-analysis-blueprint-generator

## Objective

Analyze the codebase and document representative end-to-end application workflows as implementation-ready blueprints that future developers and Copilot can use to add similar features consistently across the detected architecture.

## When to Invoke

Use this prompt when a team needs concrete workflow documentation that traces from entry point through service, mapping, data access, response, error handling, async behavior, tests, diagrams, conventions, and reusable implementation templates.

## Preconditions

- The target project is available for codebase analysis.
- At least one representative workflow exists in the codebase.
- The team can choose or accept auto-detection for project type, entry point, persistence, architecture pattern, workflow count, detail level, sequence diagrams, and test patterns.
- Generated guidance must reflect actual implementation patterns from the repository.

## Inputs the Team Must Provide

- `PROJECT_TYPE` — `Auto-detect`, `.NET`, `Java`, `Spring`, `Node.js`, `Python`, `React`, `Angular`, `Microservices`, or `Other`.
- `ENTRY_POINT` — `API`, `GraphQL`, `Frontend`, `CLI`, `Message Consumer`, `Scheduled Job`, or `Custom`.
- `PERSISTENCE_TYPE` — `Auto-detect`, `SQL Database`, `NoSQL Database`, `File System`, `External API`, `Message Queue`, `Cache`, or `None`.
- `ARCHITECTURE_PATTERN` — `Auto-detect`, `Layered`, `Clean`, `CQRS`, `Microservices`, `MVC`, `MVVM`, `Serverless`, `Event-Driven`, or `Other`.
- `WORKFLOW_COUNT` — `1-5` representative workflows to document.
- `DETAIL_LEVEL` — `Standard` or `Implementation-Ready`.
- `INCLUDE_SEQUENCE_DIAGRAM` — `true` or `false`.
- `INCLUDE_TEST_PATTERNS` — `true` or `false`.
- Ask the user for anything that is missing, especially when auto-detection cannot identify representative workflows.

## What I Will Do

- Detect technologies, entry points, persistence mechanisms, and architecture patterns from the repository.
- Select the most representative workflows and list all files and classes involved.
- Document entry point, service layer, data mapping, data access, response construction, error handling, asynchronous processing, tests, sequence diagrams, naming conventions, and implementation templates.
- Include technology-specific patterns for .NET, Spring, React, and other detected stacks.
- Identify common pitfalls, performance considerations, extension mechanisms, and configuration-driven feature patterns.
- Conclude with the most important consistency patterns for new feature implementation.

## What I Will NOT Do

- Invent workflow steps, classes, persistence behavior, tests, or sequence calls that do not exist.
- Replace source code or refactor the project.
- Document more than `WORKFLOW_COUNT` workflows.
- Treat optional testing or sequence diagram sections as mandatory when their configuration is `false`.
- Generalize external best practices over repository-specific implementation patterns.
- Ignore error handling, async processing, or naming conventions when they are present.

## Output Format

Return the blueprint in this format:

````markdown
# Project Workflow Blueprint

## Configuration
| Variable | Value |
| --- | --- |
| PROJECT_TYPE | Auto-detect/.NET/Java/Spring/Node.js/Python/React/Angular/Microservices/Other |
| ENTRY_POINT | API/GraphQL/Frontend/CLI/Message Consumer/Scheduled Job/Custom |
| PERSISTENCE_TYPE | Auto-detect/SQL Database/NoSQL Database/File System/External API/Message Queue/Cache/None |
| ARCHITECTURE_PATTERN | Auto-detect/Layered/Clean/CQRS/Microservices/MVC/MVVM/Serverless/Event-Driven/Other |
| WORKFLOW_COUNT | 1-5 |
| DETAIL_LEVEL | Standard/Implementation-Ready |
| INCLUDE_SEQUENCE_DIAGRAM | true/false |
| INCLUDE_TEST_PATTERNS | true/false |

## Initial Detection Phase
- Technologies detected: [languages, frameworks, versions when visible]
- Entry points detected: [controllers, routes, resolvers, UI components, handlers, jobs]
- Persistence detected: [database, ORM, repositories, APIs, queues, cache]
- Architecture detected: [pattern and evidence]

## Workflow 1 — [Name]

### 1. Workflow Overview
- Description: [brief description]
- Business purpose: [purpose]
- Triggering action or event: [trigger]
- Files/classes involved: [complete workflow list]

### 2. Entry Point Implementation
[Controller/resolver/component/message handler/CLI/scheduled job details]

### 3. Service Layer Implementation
[Service classes, dependencies, method signatures, business logic, interfaces, dependency injection]

### 4. Data Mapping Patterns
[DTO/domain/entity mapping, validation, domain events]

### 5. Data Access Implementation
[Repositories, queries, entities, transaction handling]

### 6. Response Construction
[Response models, mapping, status codes, error response structure]

### 7. Error Handling Patterns
[Exceptions, try/catch, global handlers, logging, retries, circuit breakers, compensating actions]

### 8. Asynchronous Processing Patterns
[Background jobs, events, queues, callbacks, webhooks, tracking, monitoring]

### 9. Testing Approach
[Only when INCLUDE_TEST_PATTERNS=true]

### 10. Sequence Diagram
[Only when INCLUDE_SEQUENCE_DIAGRAM=true]

### 11. Naming Conventions
[Controller, service, repository, DTO, method, variable, and file organization patterns]

### 12. Implementation Templates
[New endpoint, service method, repository method, domain model, and error handling templates]

## Technology-Specific Implementation Patterns
[.NET/Spring/React or detected stack-specific implementation patterns]

## Implementation Guidelines
1. Step-by-step implementation process
2. Common pitfalls to avoid
3. Extension mechanisms

## Conclusion
[Most important patterns to follow when implementing new features]
````

## Definition of Done

- [ ] `WORKFLOW_COUNT` representative workflows are documented, limited to `1-5`.
- [ ] Each workflow includes overview, entry point, service layer, data mapping, data access, response construction, error handling, async patterns, naming conventions, and templates.
- [ ] Optional testing and sequence diagram content is included only when configured.
- [ ] Technology-specific patterns are grounded in detected repository evidence.
- [ ] Files/classes involved in each workflow are listed.
- [ ] Implementation guidance includes order of work, pitfalls, and extension mechanisms.
- [ ] Unknowns are labeled rather than invented.

## Prompt Body

Follow these steps in order.

**Step 1 — Configure analysis variables.**
Use `${PROJECT_TYPE="Auto-detect|.NET|Java|Spring|Node.js|Python|React|Angular|Microservices|Other"}`, `${ENTRY_POINT="API|GraphQL|Frontend|CLI|Message Consumer|Scheduled Job|Custom"}`, `${PERSISTENCE_TYPE="Auto-detect|SQL Database|NoSQL Database|File System|External API|Message Queue|Cache|None"}`, `${ARCHITECTURE_PATTERN="Auto-detect|Layered|Clean|CQRS|Microservices|MVC|MVVM|Serverless|Event-Driven|Other"}`, `${WORKFLOW_COUNT=1-5}`, `${DETAIL_LEVEL="Standard|Implementation-Ready"}`, `${INCLUDE_SEQUENCE_DIAGRAM=true|false}`, and `${INCLUDE_TEST_PATTERNS=true|false}`.

**Step 2 — Run the initial detection phase.**
If `PROJECT_TYPE` is `Auto-detect`, examine codebase structure for .NET solutions/projects, Spring configurations, Node.js/Express files, primary languages, frameworks, folder structure, and key components. Otherwise focus on the selected technology. If `ENTRY_POINT` is `Auto-detect`, look for API controllers or route definitions, GraphQL resolvers, UI components that initiate network requests, message handlers or event subscribers, and scheduled job definitions. If `PERSISTENCE_TYPE` is `Auto-detect`, examine database context/connection configurations, repository implementations, ORM mappings, external API clients, and file system interactions.

**Step 3 — Select representative workflows.**
Choose the `${WORKFLOW_COUNT}` most representative end-to-end workflows. For each workflow, provide a name, brief description, business purpose, triggering action or event, and all files/classes involved in the complete workflow.

**Step 4 — Document entry point implementation.**
For API entry points, document the API controller class and method, complete method signature, `attributes/annotations`, full request DTO/model class definition, validation attributes, custom validators, authentication and authorization attributes, and checks. For GraphQL entry points, document the resolver class and method, complete schema definition for the `query/mutation`, input type definitions, and resolver method implementation with parameter handling. For Frontend entry points, document the component that initiates the API call, event handler, API client service method, and state management code. For Message Consumer entry points, document the message handler class and method, subscription configuration, complete message model definition, deserialization, and validation logic.

**Step 5 — Document service layer implementation.**
Document each service class, dependencies, complete method signatures with parameters and return types, actual method implementations with key business logic, interface definitions where applicable, and dependency injection registration patterns. For `CQRS` or `Auto-detect`, include complete command/query handler implementations when present. For `Clean` or `Auto-detect`, show use case/interactor implementations when present.

**Step 6 — Document data mapping and data access.**
Document DTO to domain model mapping code, object mapper configurations or manual mapping methods, validation logic during mapping, and domain events created during mapping. Document repository interfaces and implementations, complete method signatures, actual query implementations, entity/model class definitions with all properties, and transaction handling patterns. For `SQL Database` or `Auto-detect`, include ORM configurations, annotations, Fluent API usage, actual SQL queries, or ORM statements. For `NoSQL Database` or `Auto-detect`, show document structure definitions and document query/update operations.

**Step 7 — Document response and error handling.**
Document response DTO/model definitions, mapping from domain/entity models to response models, status code selection logic, and error response structure. Document exception types, try/catch patterns at each layer, global exception handler configurations, error logging implementations, retry policies, circuit breaker patterns, and compensating actions for failure scenarios.

**Step 8 — Document asynchronous processing.**
Document background job scheduling code, event publication implementations, message queue sending patterns, callback or webhook implementations, and how async operations are tracked and monitored.

**Step 9 — Add optional testing approach.**
When `INCLUDE_TEST_PATTERNS` is true, document unit test implementations for each layer, mocking patterns, test fixture setup, integration test implementations, test data generation approaches, and API/controller test implementations.

**Step 10 — Add optional sequence diagram.**
When `INCLUDE_SEQUENCE_DIAGRAM` is true, generate a detailed sequence diagram showing all components, method calls with parameter types, return values between components, conditional flows, and error paths.

**Step 11 — Document naming conventions.**
Capture controller naming such as `EntityNameController`, service naming such as `EntityNameService`, repository naming such as `IEntityNameRepository`, DTO naming such as `EntityNameRequest` and `EntityNameResponse`, CRUD method naming patterns, variable naming conventions, and file organization patterns.

**Step 12 — Provide implementation templates and technology-specific patterns.**
Provide reusable templates for creating a new API endpoint, implementing a new service method, adding a new repository method, creating new domain model classes, and implementing proper error handling. For .NET, include complete controller classes with attributes, filters, dependency injection, service registration in `Startup.cs` or `Program.cs`, Entity Framework `DbContext` configuration, repository implementation with EF Core or Dapper, AutoMapper profiles, middleware, extension methods, Options pattern, `ILogger`, and authentication/authorization filters or policies. For Spring, include controller annotations, dependency injection, service transaction boundaries, repositories, JPA entities with relationships, DTOs, Bean configuration, component scanning, exception handlers, and custom validators. For React, include component structure with props and state, hooks such as `useState`, `useEffect`, custom hooks, API service implementation, state management with Context or Redux, form handling, and route configuration.

**Step 13 — Write implementation guidelines and conclusion.**
Explain where to start when adding a similar feature, order of implementation such as model → repository → service → controller, how to integrate cross-cutting concerns, error-prone areas, performance considerations, common bugs, extension points, adding behavior without modifying existing code, and configuration-driven feature patterns. Conclude with the most important patterns to follow to maintain consistency with the codebase.

## Invocation Example

```
/project-workflow-analysis-blueprint-generator PROJECT_TYPE=Auto-detect ENTRY_POINT=API PERSISTENCE_TYPE=Auto-detect ARCHITECTURE_PATTERN=Auto-detect WORKFLOW_COUNT=3 DETAIL_LEVEL=Implementation-Ready INCLUDE_SEQUENCE_DIAGRAM=true INCLUDE_TEST_PATTERNS=true
```
