---
name: 'copilot-instructions-blueprint-generator'
description: 'Generate a codebase-specific copilot-instructions.md blueprint for consistent Copilot guidance.'
argument-hint: 'PROJECT_TYPE=<Auto-detect|.NET|Java|JavaScript|TypeScript|React|Angular|Python|Multiple|Other> ARCHITECTURE_STYLE=<Layered|Microservices|Monolithic|Domain-Driven|Event-Driven|Serverless|Mixed>'
---

# /copilot-instructions-blueprint-generator

## Objective

Generate a comprehensive, codebase-specific `copilot-instructions.md` blueprint that guides GitHub Copilot to produce code consistent with the repository's detected technology versions, architecture, code patterns, quality priorities, documentation level, testing requirements, and versioning approach.

## When to Invoke

Use this prompt when a repository needs a new or refreshed Copilot instruction blueprint grounded in actual codebase patterns rather than assumptions or external best practices.

## Preconditions

- The target codebase is available for analysis.
- The team can choose or accept defaults for project type, architecture style, code quality focus, documentation level, testing requirements, and versioning approach.
- The `.github/copilot` directory may or may not already exist.
- The final guidance must be based only on patterns actually observed in the codebase.

## Inputs the Team Must Provide

- `PROJECT_TYPE` — `Auto-detect`, `.NET`, `Java`, `JavaScript`, `TypeScript`, `React`, `Angular`, `Python`, `Multiple`, or `Other`.
- `ARCHITECTURE_STYLE` — `Layered`, `Microservices`, `Monolithic`, `Domain-Driven`, `Event-Driven`, `Serverless`, or `Mixed`.
- `CODE_QUALITY_FOCUS` — `Maintainability`, `Performance`, `Security`, `Accessibility`, `Testability`, or `All`.
- `DOCUMENTATION_LEVEL` — `Minimal`, `Standard`, or `Comprehensive`.
- `TESTING_REQUIREMENTS` — `Unit`, `Integration`, `E2E`, `TDD`, `BDD`, or `All`.
- `VERSIONING` — `Semantic`, `CalVer`, or `Custom`.
- Ask the user for anything that is missing, especially when required configuration would change the generated blueprint.

## What I Will Do

- Detect exact language, framework, and library versions from project files and package managers.
- Prioritize `.github/copilot` context files when present: `architecture.md`, `tech-stack.md`, `coding-standards.md`, `folder-structure.md`, and `exemplars.md`.
- Scan similar files when context files do not provide specific guidance.
- Catalog naming conventions, code organization, error handling, logging, documentation, testing, security, accessibility, performance, and configuration patterns.
- Generate a `copilot-instructions.md` blueprint that prioritizes consistency with existing code over external best practices.
- Include technology-specific guidance only when the relevant stack is detected or selected.

## What I Will NOT Do

- Invent standards, versions, libraries, framework features, or architectural boundaries not present in the codebase.
- Suggest language features beyond the detected version.
- Prescribe practices not evident in the code unless the user explicitly asks for a migration or policy change.
- Ignore conflicting patterns; I will prioritize newer files or files with higher test coverage when evidence supports that choice.
- Overwrite an existing instruction file without stating the intended change scope.
- Use relative links between primitives.

## Output Format

Generate the blueprint in this format:

````markdown
# GitHub Copilot Instructions

## Priority Guidelines

When generating code for this repository:

1. **Version Compatibility**: Always detect and respect the exact versions of languages, frameworks, and libraries used in this project
2. **Context Files**: Prioritize patterns and standards defined in the .github/copilot directory
3. **Codebase Patterns**: When context files don't provide specific guidance, scan the codebase for established patterns
4. **Architectural Consistency**: Maintain our [ARCHITECTURE_STYLE] architectural style and established boundaries
5. **Code Quality**: Prioritize [CODE_QUALITY_FOCUS] in all generated code

## Technology Version Detection

Before generating code, scan the codebase to identify:

1. **Language Versions**: Detect the exact versions of programming languages in use
   - Examine project files, configuration files, and package managers
   - Look for language-specific version indicators such as `<LangVersion>` in .NET projects
   - Never use language features beyond the detected version

2. **Framework Versions**: Identify the exact versions of all frameworks
   - Check `package.json`, `.csproj`, `pom.xml`, `requirements.txt`, and equivalent files
   - Respect version constraints when generating code
   - Never suggest features not available in the detected framework versions

3. **Library Versions**: Note the exact versions of key libraries and dependencies
   - Generate code compatible with these specific versions
   - Never use APIs or features not available in the detected versions

## Context Files

Prioritize the following files in .github/copilot directory if they exist:

- **architecture.md**: System architecture guidelines
- **tech-stack.md**: Technology versions and framework details
- **coding-standards.md**: Code style and formatting standards
- **folder-structure.md**: Project organization guidelines
- **exemplars.md**: Exemplary code patterns to follow

## Codebase Scanning Instructions

1. Identify similar files to the one being modified or created
2. Analyze naming conventions, code organization, error handling, logging approaches, documentation style, and testing patterns
3. Follow the most consistent patterns found in the codebase
4. When conflicting patterns exist, prioritize patterns in newer files or files with higher test coverage
5. Never introduce patterns not found in the existing codebase

## Code Quality Standards

### Maintainability
- Write self-documenting code with clear naming
- Follow naming and organization conventions evident in the codebase
- Keep functions focused on single responsibilities
- Limit function complexity and length to match existing patterns

### Performance
- Follow existing patterns for memory and resource management
- Match existing patterns for computationally expensive operations
- Follow established asynchronous, caching, and optimization patterns

### Security
- Follow existing input validation and sanitization techniques
- Use parameterized queries matching existing patterns
- Follow established authentication and authorization patterns
- Handle sensitive data according to existing patterns

### Accessibility
- Follow existing accessibility patterns, ARIA attribute usage, keyboard navigation, color, contrast, and text alternative patterns

### Testability
- Follow established patterns for testable code, dependency injection, dependency management, mocking, test doubles, and test style

## Documentation Requirements

[Minimal|Standard|Comprehensive documentation guidance based on observed code]

## Testing Approach

[Unit|Integration|E2E|TDD|BDD guidance based on existing test structure]

## Technology-Specific Guidelines

[.NET|Java|JavaScript/TypeScript|React|Angular|Python guidance only when detected or selected]

## Version Control Guidelines

[Semantic|CalVer|Custom versioning guidance based on the codebase]

## General Best Practices

- Follow naming conventions exactly as they appear in existing code
- Match code organization patterns from similar files
- Apply error handling consistent with existing patterns
- Follow the same approach to testing as seen in the codebase
- Match logging patterns from existing code
- Use the same approach to configuration as seen in the codebase

## Project-Specific Guidance

- Scan the codebase thoroughly before generating any code
- Respect existing architectural boundaries without exception
- Match the style and patterns of surrounding code
- When in doubt, prioritize consistency with existing code over external best practices
````

## Definition of Done

- [ ] Exact language, framework, and library versions are documented from real project evidence.
- [ ] `.github/copilot` context files are prioritized when present.
- [ ] Guidance is based on actual code patterns and avoids assumptions.
- [ ] Architecture style, boundaries, naming, error handling, logging, documentation, testing, and configuration patterns are covered.
- [ ] Technology-specific sections match detected or selected technologies.
- [ ] Documentation, testing, code quality, and versioning guidance reflect the selected configuration variables.
- [ ] The final `copilot-instructions.md` blueprint is comprehensive yet concise enough for Copilot to use.

## Prompt Body

Follow these steps in order.

**Step 1 — Configure the generation variables.**
Use `${PROJECT_TYPE="Auto-detect|.NET|Java|JavaScript|TypeScript|React|Angular|Python|Multiple|Other"}`, `${ARCHITECTURE_STYLE="Layered|Microservices|Monolithic|Domain-Driven|Event-Driven|Serverless|Mixed"}`, `${CODE_QUALITY_FOCUS="Maintainability|Performance|Security|Accessibility|Testability|All"}`, `${DOCUMENTATION_LEVEL="Minimal|Standard|Comprehensive"}`, `${TESTING_REQUIREMENTS="Unit|Integration|E2E|TDD|BDD|All"}`, and `${VERSIONING="Semantic|CalVer|Custom"}`. Treat these as configuration variables for the generated prompt.

**Step 2 — Identify exact technology versions.**
If `PROJECT_TYPE` is `Auto-detect`, detect all programming languages, frameworks, and libraries by scanning file extensions and configuration files. Otherwise focus on the selected technology. Extract precise version information from project files such as `package.json`, `.csproj`, `pom.xml`, and `requirements.txt`. Document version constraints and compatibility requirements.

When a specific project type is selected, apply the rule: `Focus on ${PROJECT_TYPE} technologies`.

**Step 3 — Understand architecture.**
Analyze folder structure and module organization. Identify layer boundaries, component relationships, and communication patterns. Maintain the selected or detected architectural style and established boundaries.

**Step 4 — Prioritize context files.**
Read `.github/copilot/architecture.md`, `.github/copilot/tech-stack.md`, `.github/copilot/coding-standards.md`, `.github/copilot/folder-structure.md`, and `.github/copilot/exemplars.md` when they exist. Use these files before inferred codebase patterns.

**Step 5 — Document code patterns.**
Identify similar files to those Copilot is likely to modify. Catalog naming conventions, code organization, error handling, logging approaches, documentation style, test patterns, and coverage. When context files do not provide guidance, follow the most consistent codebase patterns. When conflicts exist, prioritize newer files or files with higher test coverage.

**Step 6 — Capture quality standards.**
For `Maintainability`, include self-documenting code, clear naming, established patterns, focused functions, and matching complexity and length. For `Performance`, include memory and resource management, expensive operations, async operations, caching, and optimization patterns. For `Security`, include input validation, sanitization, parameterized queries, authentication, authorization, and sensitive data handling. For `Accessibility`, include accessibility patterns, ARIA attributes, keyboard navigation, color, contrast, and text alternatives. For `Testability`, include testable code, dependency injection, dependencies, mocking, test doubles, and testing style.

**Step 7 — Capture documentation requirements.**
For `Minimal`, match existing comments, documentation patterns, non-obvious behavior documentation, and parameter description format. For `Standard`, match XML/JSDoc style, parameter, return, exception, usage example, and class-level documentation style. For `Comprehensive`, match the most detailed documentation patterns, best-documented code, linking patterns, and explanation depth for design decisions.

**Step 8 — Capture testing approach.**
For `Unit`, match test structure, class and method naming, assertion patterns, mocking approach, and isolation. For `Integration`, match test patterns, data setup and teardown, component interaction testing, and system behavior verification. For `E2E`, match E2E test structure, UI testing, and user journey verification. For `TDD`, match test case progression and refactoring patterns after tests pass. For `BDD`, match Given-When-Then structure, behavior descriptions, and business focus.

**Step 9 — Add technology-specific guidelines.**
For `.NET`, detect the .NET version, C# version, LINQ usage, async/await patterns, dependency injection, collection types, and patterns. For Java, detect Java version, design patterns, exception handling, collection types, and dependency injection. For JavaScript/TypeScript, detect ECMAScript or TypeScript version, module import/export patterns, type definitions, promises, async/await, and error handling. For React, detect React version, component structure, hooks, lifecycle, state management, and prop typing. For Angular, detect Angular version, component and module patterns, decorator usage, RxJS, and component communication. For Python, detect Python version, import organization, type hints, error handling, and module organization.

**Step 10 — Add version control guidance.**
For `Semantic`, follow Semantic Versioning patterns, breaking change documentation, and deprecation notices as applied in the codebase. For `CalVer`, follow Calendar Versioning patterns, documenting changes, and highlighting significant changes. For `Custom`, match exact versioning, changelog, and tagging conventions observed in the project.

**Step 11 — Generate implementation notes.**
Place the final `copilot-instructions.md` in the `.github/copilot` directory. Reference only patterns and standards that exist in the codebase. Include explicit version compatibility requirements. Avoid prescribing practices not evident in the code. Provide concrete examples from the codebase. Keep the result comprehensive yet concise. Explicitly instruct Copilot to prioritize consistency with existing code over external best practices or newer language features.

## Invocation Example

```
/copilot-instructions-blueprint-generator PROJECT_TYPE=Auto-detect ARCHITECTURE_STYLE=Mixed CODE_QUALITY_FOCUS=All DOCUMENTATION_LEVEL=Standard TESTING_REQUIREMENTS=All VERSIONING=Semantic
```
