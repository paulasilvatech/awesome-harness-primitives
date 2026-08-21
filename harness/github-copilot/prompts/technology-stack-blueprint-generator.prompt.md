---
name: 'technology-stack-blueprint-generator'
description: 'Generate a technology stack blueprint that documents detected languages, frameworks, dependencies, and implementation patterns.'
argument-hint: 'project_type=<Auto-detect|.NET|Java|JavaScript|React.js|React Native|Angular|Python|Other> depth=<Basic|Standard|Comprehensive|Implementation-Ready>'
---

# /technology-stack-blueprint-generator

## Objective

Generate a technology stack blueprint that documents detected languages, frameworks, dependencies, tooling, configuration, conventions, usage patterns, and implementation-ready templates for a repository so future code generation follows the existing stack instead of inventing new patterns.

## When to Invoke

Use this prompt before adding substantial new code, onboarding to an unfamiliar repository, planning modernization work, or standardizing code generation across multiple technology areas.

## Preconditions

- The repository or target project area is available for inspection.
- Project files, configuration files, build scripts, pipeline definitions, and dependency manifests can be read.
- The team has selected the desired analysis depth and output format.
- If diagrams, licenses, or implementation-ready examples are requested, the repository contains enough evidence to produce them without guessing.

## Inputs the Team Must Provide

- `PROJECT_TYPE` — `Auto-detect`, `.NET`, `Java`, `JavaScript`, `React.js`, `React Native`, `Angular`, `Python`, or `Other`.
- `DEPTH_LEVEL` — `Basic`, `Standard`, `Comprehensive`, or `Implementation-Ready`.
- `INCLUDE_VERSIONS` — `true` or `false`.
- `INCLUDE_LICENSES` — `true` or `false`.
- `INCLUDE_DIAGRAMS` — `true` or `false`.
- `INCLUDE_USAGE_PATTERNS` — `true` or `false`.
- `INCLUDE_CONVENTIONS` — `true` or `false`.
- `OUTPUT_FORMAT` — `Markdown`, `JSON`, `YAML`, or `HTML`.
- `CATEGORIZATION` — `Technology Type`, `Layer`, or `Purpose`.
- Ask the user for anything that is missing, especially scope, depth, or destination.

## What I Will Do

- Scan the codebase for file extensions, project files, configuration files, dependency manifests, build scripts, and pipeline definitions.
- Detect programming languages, framework versions, package managers, build tooling, test frameworks, and deployment infrastructure.
- Analyze `.NET`, `Java`, `JavaScript`, `React.js`, and `Python` stacks when detected or explicitly requested.
- Document implementation patterns for configuration, authentication, authorization, validation, logging, dependency injection, data access, APIs, services, UI components, and testing.
- Extract representative usage examples only from inspected code.
- Produce a blueprint categorized by technology type, layer, or purpose in the requested format.

## What I Will NOT Do

- Invent dependencies, versions, licenses, conventions, diagrams, or implementation patterns not supported by repository evidence.
- Replace the repository's stack, package manager, build system, or framework choices unless the user asks for recommendations.
- Treat `Auto-detect` as permission to scan outside the workspace.
- Present speculative technology-decision context as fact; label uncertain rationale explicitly.
- Save output to a file unless the destination is explicit and editing tools are available.

## Output Format

Return or write the blueprint using the selected `OUTPUT_FORMAT`. For `Markdown`, use this concrete skeleton:

```markdown
# Technology Stack Blueprint

## Analysis Configuration
| Setting | Value |
| --- | --- |
| Project type | Auto-detect |
| Depth level | Implementation-Ready |
| Include versions | true |
| Include licenses | false |
| Include diagrams | true |
| Include usage patterns | true |
| Include conventions | true |
| Categorization | Technology Type |

## Technology Identification
| Technology | Evidence | Version | Purpose | License |
| --- | --- | --- | --- | --- |
| Java | `pom.xml` | `21` | Backend runtime | Unknown |

## Core Technologies
### .NET Stack Analysis
### Java Stack Analysis
### JavaScript Stack Analysis
### React Analysis
### Python Analysis

## Implementation Patterns & Conventions
### Naming Conventions
### Code Organization
### Common Patterns

## Usage Examples
### API Implementation Examples
### Data Access Examples
### Service Layer Examples
### UI Component Examples

## Technology Stack Map
### Core Framework Usage
### Integration Points
### Development Tooling
### Infrastructure

## Technology-Specific Implementation Details
### .NET Implementation Details
### React Implementation Details

## Blueprint for New Code Implementation
### File/Class Templates
### Code Snippets
### Implementation Checklist
### Integration Points
### Testing Requirements
### Documentation Requirements

## Technology Relationship Diagrams
### Stack Diagram
### Dependency Flow
### Component Relationships
### Data Flow

## Technology Decision Context
### Apparent Choices
### Legacy or Deprecated Technologies
### Constraints and Boundaries
### Upgrade Paths and Compatibility Considerations
```

Save file output as `Technology_Stack_Blueprint.md`, `Technology_Stack_Blueprint.json`, `Technology_Stack_Blueprint.yaml`, or `Technology_Stack_Blueprint.html` according to `OUTPUT_FORMAT` only when file output is requested.

## Definition of Done

- [ ] The selected configuration values are recorded and applied consistently.
- [ ] Every listed technology is backed by inspected evidence such as `package.json`, `.csproj`, `pom.xml`, Gradle files, source files, build scripts, or pipeline definitions.
- [ ] Versions and licenses are included only when requested and available from manifests or configuration.
- [ ] Usage patterns and conventions are included only when requested and backed by representative code examples.
- [ ] The output is categorized by `Technology Type`, `Layer`, or `Purpose` as requested.
- [ ] Implementation-ready output includes templates, snippets, integration points, tests, and documentation requirements.
- [ ] Unknowns, assumptions, and unsupported diagram requests are labeled clearly.

## Prompt Body

Follow these steps in order.

**Step 1 — Configure the analysis.** Confirm `PROJECT_TYPE`, `DEPTH_LEVEL`, `INCLUDE_VERSIONS`, `INCLUDE_LICENSES`, `INCLUDE_DIAGRAMS`, `INCLUDE_USAGE_PATTERNS`, `INCLUDE_CONVENTIONS`, `OUTPUT_FORMAT`, and `CATEGORIZATION`. If `PROJECT_TYPE` is `Auto-detect`, inspect the repository broadly enough to identify all stacks in scope; otherwise focus on the requested technology.

**Step 2 — Identify technologies.** Scan file extensions, content, project files, configuration files, dependency manifests, build scripts, and pipeline definitions. Extract dependencies from `package.json`, `.csproj`, `pom.xml`, Maven files, Gradle files, Python dependency files, and equivalent manifests. Include precise versions when `INCLUDE_VERSIONS=true`. Document dependency license information when `INCLUDE_LICENSES=true` and the information is available.

**Step 3 — Analyze each detected core stack.** For `.NET`, document target frameworks, language versions, NuGet package references, project structure, `appsettings.json`, `IOptions`, Identity, `JWT`, REST, GraphQL, minimal APIs, EF Core, Dapper, dependency injection, and middleware pipeline components. For `Java`, document JDK version, Maven/Gradle dependencies, package structure, Spring Boot configuration, annotation patterns, dependency injection, JPA, JDBC, Spring MVC, and JAX-RS. For `JavaScript`, document ECMAScript version, transpiler settings, npm dependencies, ESM, CommonJS, webpack, Vite, TypeScript configuration, testing frameworks, and test patterns. For `React.js`, document React version, hooks versus class components, Context, Redux, Zustand, Material-UI, Chakra, routing, forms, API integration, and component tests. For `Python`, document Python version, language features, dependencies, virtual environment setup, Django, Flask, FastAPI, ORM usage, structure, and API design.

**Step 4 — Document conventions when requested.** If `INCLUDE_CONVENTIONS=true`, capture naming conventions for classes, types, methods, functions, variables, files, interfaces, and abstract classes. Describe file structure, folder hierarchy, component and module boundaries, responsibility separation, error handling, logging, configuration access, authentication, authorization, validation, and testing patterns.

**Step 5 — Extract usage patterns when requested.** If `INCLUDE_USAGE_PATTERNS=true`, include inspected examples for `controller/endpoint` implementation, controllers, endpoints, request DTOs, response formatting, validation, error handling, repositories, entities, models, queries, transaction handling, service classes, business logic, cross-cutting concerns, dependency injection, UI component structure, state management, event handling, and API integration.

**Step 6 — Build the technology map.** For `Comprehensive` or `Implementation-Ready`, document core framework usage, framework-specific configuration, customization points, integration points, authentication flow, frontend/backend data flow, third-party services, IDE settings, code analysis tools, linters, formatters, build and deployment pipelines, testing frameworks, deployment environment, containers, cloud services, monitoring, and logging infrastructure.

**Step 7 — Add implementation details.** For `.NET`, describe service registration lifetimes (`Scoped`, `Singleton`, `Transient`), configuration binding, base controllers, action results, route attributes, filters, ORM configuration, entity configuration, relationships, query optimization, endpoint organization, parameter binding, response types, language features, idioms, and version-dependent features. For `React.js`, describe function versus class components, props interfaces, component composition, custom hooks, `useState`, `useEffect` cleanup, Context, local versus global state, store configuration, selectors, CSS modules, `styled-components`, theme implementation, and responsive design.

**Step 8 — Produce implementation-ready guidance when requested.** If `DEPTH_LEVEL=Implementation-Ready`, provide file/class templates, ready-to-use code snippets, an end-to-end implementation checklist, integration points, testing requirements, and documentation requirements for new features.

**Step 9 — Add diagrams and decision context.** If `INCLUDE_DIAGRAMS=true`, include a stack diagram, dependency flow, component relationships, and data flow using Markdown-safe diagram syntax. Always document apparent technology-choice reasons, legacy or deprecated technologies marked for replacement, constraints, boundaries, upgrade paths, and compatibility considerations. Label inferred rationale as inferred.

**Step 10 — Deliver and validate.** Format the result as `Markdown`, `JSON`, `YAML`, or `HTML`. If file output is requested, save as `Technology_Stack_Blueprint.<extension>` where the extension is `md`, `json`, `yaml`, or `html`. Verify that the blueprint contains no unsupported claims and that every major fact has evidence.

## Invocation Example

```
/technology-stack-blueprint-generator project_type=Auto-detect depth=Implementation-Ready include_versions=true include_licenses=false include_diagrams=true include_usage_patterns=true include_conventions=true output_format=Markdown categorization="Technology Type"
```
