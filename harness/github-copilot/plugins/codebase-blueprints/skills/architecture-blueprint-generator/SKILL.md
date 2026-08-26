---
name: architecture-blueprint-generator
description: >-
  Generate a comprehensive Project_Architecture_Blueprint.md by analyzing a codebase, detecting technology stacks and architectural patterns, documenting components, dependencies, diagrams, implementation patterns, testing, deployment, and governance. Use when asked to create an architecture blueprint, document project architecture, map layers, produce C4/UML/component diagrams, or guide new development consistency.
argument-hint: "PROJECT_TYPE, ARCHITECTURE_PATTERN, DIAGRAM_TYPE, DETAIL_LEVEL, and optional blueprint focus"
---

# Architecture blueprint generator

Take a codebase and optional configuration variables, transform observed files, dependencies, imports, and runtime configuration into a grounded architecture blueprint, and output a `Project_Architecture_Blueprint.md` document that guides consistent maintenance and new development.

## When to invoke

- "Generate a project architecture blueprint."
- "Analyze this codebase and document its architecture."
- "Create C4 diagrams and implementation patterns for this repo."
- "Map layers, dependencies, and extension points."
- "Write a blueprint for adding new features consistently."

## Inputs

Use `$ARGUMENTS` to set or infer these variables. Defaults are auto-detection and implementation-ready detail when the user does not specify values.

| Variable | Allowed values | Meaning |
| --- | --- | --- |
| `PROJECT_TYPE` | `Auto-detect`, `.NET`, `Java`, `React`, `Angular`, `Python`, `Node.js`, `Flutter`, `Other` | Primary technology stack to analyze. |
| `ARCHITECTURE_PATTERN` | `Auto-detect`, `Clean Architecture`, `Microservices`, `Layered`, `MVVM`, `MVC`, `Hexagonal`, `Event-Driven`, `Serverless`, `Monolithic`, `Other` | Primary architecture pattern to confirm against the code. |
| `DIAGRAM_TYPE` | `C4`, `UML`, `Flow`, `Component`, `None` | Diagram notation or textual relationship map. |
| `DETAIL_LEVEL` | `High-level`, `Detailed`, `Comprehensive`, `Implementation-Ready` | Depth of evidence, examples, and guidance. |
| `INCLUDES_CODE_EXAMPLES` | `true` or `false` | Include representative excerpts that show architectural patterns. |
| `INCLUDES_IMPLEMENTATION_PATTERNS` | `true` or `false` | Document concrete service, repository, controller/API, interface, and domain model patterns. |
| `INCLUDES_DECISION_RECORDS` | `true` or `false` | Extract apparent ADR-style decisions from the code and history only when evidence exists. |
| `FOCUS_ON_EXTENSIBILITY` | `true` or `false` | Emphasize extension points, variation points, plugin mechanisms, and safe modification paths. |

Do not invent repository-specific decisions, diagrams, or runtime services. If evidence is absent, mark it as `Not observed` rather than filling theory.

## Procedure

1. Detect stacks from project files, package manifests, lockfiles, imports, namespaces, framework conventions, build configuration, deployment files, and test setup.
2. Detect architecture by folder organization, dependency direction, component boundaries, interface or abstraction usage, communication mechanisms, and runtime composition.
3. Build the blueprint from observed code, not idealized patterns. Every major claim should cite a file path, package, command, class, module, or configuration key.
4. Create diagrams only when `DIAGRAM_TYPE` is not `None`; keep them consistent with observed dependencies and data flow.
5. Document components, layers, data architecture, cross-cutting concerns, service communication, testing, deployment, extension guidance, and governance.
6. When requested, include code examples, implementation patterns, and decision records only if the repository contains enough evidence.
7. Produce `Project_Architecture_Blueprint.md` or paste-ready markdown when the user does not want a file.

## Architecture detection

| Evidence | What to inspect | Blueprint conclusion |
| --- | --- | --- |
| Project files | `.csproj`, `pom.xml`, `build.gradle`, `package.json`, `pyproject.toml`, `requirements.txt`, `pubspec.yaml` | `PROJECT_TYPE`, frameworks, build and package boundaries. |
| Dependencies and imports | DI containers, ORMs, routers, state libraries, messaging SDKs, test frameworks | Technology-specific architectural patterns. |
| Folder structure | `src/`, `app/`, `domain/`, `application/`, `infrastructure/`, `controllers/`, `features/`, `components/`, `pages/` | Layered, Clean Architecture, MVC, MVVM, Hexagonal, feature-sliced, or monolithic tendencies. |
| Runtime composition | `Program.cs`, application bootstrap, module registration, route registration, providers, middleware | Entry points, dependency injection, service boundaries. |
| Communication | HTTP clients, queues, events, pub/sub, RPC, database calls | Synchronous vs asynchronous service communication. |
| Deployment config | Dockerfiles, compose files, Helm charts, Bicep/Terraform, CI workflows, serverless config | Deployment topology and environment-specific adaptation. |
| Tests | Unit, integration, system, e2e layouts; fixtures; mocks; test data | Testing architecture and boundary strategy. |

## Blueprint content

| Section | Required content |
| --- | --- |
| Architectural overview | Overall approach, guiding principles, boundaries, enforcement mechanisms, hybrid adaptations. |
| Visualization | High-level overview, component interaction, data flow, or textual relationships when `DIAGRAM_TYPE=None`. |
| Core components | Purpose, responsibility, internal structure, key abstractions, exposed and consumed interfaces, evolution patterns. |
| Layers and dependencies | Layer map, dependency rules, abstraction mechanisms, circular dependencies, dependency injection patterns. |
| Data architecture | Domain model, entities or aggregates, repository/data mapper patterns, transformations, caching, validation. |
| Cross-cutting concerns | Authentication and authorization, error handling and resilience, logging and monitoring, validation, configuration, secrets, feature flags. |
| Service communication | Boundaries, protocols, formats, API versioning, service discovery, retry, circuit breaker, fallback, graceful degradation. |
| Technology-specific patterns | `.NET`, `Java`, `React`, `Angular`, `Python`, `Node.js`, `Flutter`, or other observed stack-specific practices. |
| Testing architecture | Unit/integration/system/e2e boundaries, mocking, test doubles, test data, tools. |
| Deployment architecture | Runtime topology, environment configuration, containers, orchestration, cloud services. |
| Extension and evolution | Feature addition sequence, placement rules, adapter or anti-corruption layer patterns, backward compatibility, migration and deprecation. |
| Architecture governance | Automated checks, review practices, documentation lifecycle, blueprint refresh guidance. |
| Blueprint for new development | Starting points, component creation sequence, integration steps, implementation templates, common pitfalls. |

## Technology-specific prompts

| Stack | Look for |
| --- | --- |
| `.NET` | Host and application model, middleware pipeline, `Program.cs`, dependency injection container, ORM, controllers, minimal APIs. |
| `Java` | Spring/CDI bootstrap, AOP, transaction boundaries, ORM configuration, service implementation, module packaging. |
| `React` | Component composition, state management, side effects, routing, data fetching, caching, rendering optimization. |
| `Angular` | Module organization, component hierarchy, services, DI, RxJS/reactive patterns, route guards. |
| `Python` | Module organization, dependency management, OOP vs functional style, framework integration, async patterns. |
| `Node.js` | Package scripts, framework entry points, middleware, controllers/routes, background jobs, dependency injection or composition. |
| `Flutter` | Widget hierarchy, state management, navigation, platform services, data layer, build flavors. |

## Implementation pattern catalog

Include these only when `INCLUDES_IMPLEMENTATION_PATTERNS=true` or `DETAIL_LEVEL` is `Comprehensive` / `Implementation-Ready`.

| Pattern area | Evidence to capture |
| --- | --- |
| Interface design | Interface segregation, abstraction level, generic vs specific interfaces, default implementations. |
| Service implementation | Service lifetime, composition, operation templates, error handling inside services. |
| Repository implementation | Query patterns, transaction management, concurrency handling, bulk operations. |
| Controller/API implementation | Request handling, response formatting, parameter validation, API versioning. |
| Domain model | Entities, value objects, domain events, business rule enforcement. |
| Code examples | Concise excerpts for layer separation, component communication, dependency injection, event publication, plugin registration, and extension interfaces. |

## Criteria

- [ ] The blueprint is descriptive, not aspirational: every architectural claim is backed by observed code or explicitly marked as a recommendation.
- [ ] Diagrams match actual components, dependencies, and data flow.
- [ ] Cross-cutting concerns name concrete implementation files, libraries, middleware, interceptors, or configuration keys.
- [ ] Extension guidance tells a future developer where to place new files and which dependencies are allowed.
- [ ] Decision records are included only when the codebase or history supports context, factors, consequences, and alternatives.

## Gotchas

- **Do not force a pattern label**: if the code is hybrid or inconsistent, say so and map the inconsistency.
- **Do not confuse package structure with runtime boundaries**: verify imports, dependency injection, and calls.
- **Do not over-diagram**: if the user selects `None`, produce clear textual component relationships instead.
- **Do not include secrets**: describe secret management approach without pasting values.

## Source compatibility terms

Retain these architecture-blueprint source terms when interpreting older generated prompts: `Document ${PROJECT_TYPE}-specific architectural patterns:`, `class/interface`, `classes/modules`, `off-the-shelf`, and `publishing/subscription`.

## Output template

```markdown
# Project Architecture Blueprint

**Generated:** <date>
**Scope:** <repository or directories>
**PROJECT_TYPE:** <value>
**ARCHITECTURE_PATTERN:** <value>
**DIAGRAM_TYPE:** <value>
**DETAIL_LEVEL:** <value>

## Executive summary
<one-paragraph architecture summary grounded in observed evidence>

## Architecture detection
| Evidence | Finding | Source |
| --- | --- | --- |
| `<file or dependency>` | `<stack or pattern inference>` | `<path>` |

## Architectural overview
<principles, boundaries, and hybrid patterns>

## Architecture visualization
```mermaid
<diagram or "Diagram omitted because DIAGRAM_TYPE=None">
```

## Core architectural components
| Component | Responsibility | Key files | Interfaces consumed/exposed | Extension points |
| --- | --- | --- | --- | --- |

## Layers and dependencies
<dependency rules, violations, and enforcement>

## Data architecture
<domain model, persistence, validation, caching, transformations>

## Cross-cutting concerns
<auth, error handling, resilience, logging, monitoring, validation, configuration>

## Service communication patterns
<protocols, sync/async flows, API versioning, discovery, resilience>

## Technology-specific patterns
<stack-specific observations>

## Testing architecture
<test boundaries, tools, fixtures, test data>

## Deployment architecture
<topology and environment-specific behavior>

## Extension and evolution patterns
<feature addition, modification, integration, migration guidance>

## Architecture governance
<automated checks, review process, documentation maintenance>

## Blueprint for new development
<workflow, placement rules, templates, pitfalls>

## Open questions and recommendations
| Topic | Evidence gap | Recommendation |
| --- | --- | --- |
```

## Quality gate

- [ ] `PROJECT_TYPE`, `ARCHITECTURE_PATTERN`, `DIAGRAM_TYPE`, `DETAIL_LEVEL`, `INCLUDES_CODE_EXAMPLES`, `INCLUDES_IMPLEMENTATION_PATTERNS`, `INCLUDES_DECISION_RECORDS`, and `FOCUS_ON_EXTENSIBILITY` are honored or explicitly defaulted.
- [ ] The output includes concrete source paths, package names, commands, or configuration keys as evidence.
- [ ] No repository-specific fact is invented when evidence is missing.
- [ ] Optional code examples and decision records appear only when requested and supported.
- [ ] The delivered artifact is `Project_Architecture_Blueprint.md` or paste-ready markdown with the same structure.
