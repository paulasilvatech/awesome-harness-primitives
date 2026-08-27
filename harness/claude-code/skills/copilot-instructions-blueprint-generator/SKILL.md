---
name: copilot-instructions-blueprint-generator
description: >-
  Generate technology-agnostic blueprints for comprehensive copilot-instructions.md files that
  make GitHub Copilot follow exact project versions, architecture, code quality, documentation,
  testing, and versioning conventions discovered from the codebase. Use this skill when the user
  asks for configuration variables, wants to create copilot-instructions.md, or needs
  repository-specific GitHub Copilot coding guidance.
---

<!-- Generated from harness/github-copilot/skills/copilot-instructions-blueprint-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Copilot instructions blueprint generator

Generate a blueprint prompt for creating a `.github/copilot/copilot-instructions.md` file that constrains GitHub Copilot to actual repository versions, architecture, coding standards, tests, and patterns rather than assumptions or generic best practices.

## When to invoke

- "Generate configuration variables for copilot instructions."
- "Create a copilot-instructions.md blueprint."
- "Make GitHub Copilot follow this repo's architecture and versions."
- "Analyze the codebase and write Copilot coding guidance."
- "Document project-specific standards for GitHub Copilot."

## Configuration variables

| Variable | Values | Purpose |
| --- | --- | --- |
| `${PROJECT_TYPE}` | `Auto-detect`, `.NET`, `Java`, `JavaScript`, `TypeScript`, `React`, `Angular`, `Python`, `Multiple`, `Other` | Primary technology. |
| `${ARCHITECTURE_STYLE}` | `Layered`, `Microservices`, `Monolithic`, `Domain-Driven`, `Event-Driven`, `Serverless`, `Mixed` | Architectural approach. |
| `${CODE_QUALITY_FOCUS}` | `Maintainability`, `Performance`, `Security`, `Accessibility`, `Testability`, `All` | Quality priorities. |
| `${DOCUMENTATION_LEVEL}` | `Minimal`, `Standard`, `Comprehensive` | Documentation requirements. |
| `${TESTING_REQUIREMENTS}` | `Unit`, `Integration`, `E2E`, `TDD`, `BDD`, `All` | Testing approach. |
| `${VERSIONING}` | `Semantic`, `CalVer`, `Custom` | Versioning approach. |

## Blueprint requirements

The generated prompt must instruct GitHub Copilot to create `.github/copilot/copilot-instructions.md` and include these rules.

| Area | Required instruction |
| --- | --- |
| Version compatibility | Detect exact language, framework, and library versions from project files before generating code; never use APIs beyond detected versions. |
| Context files | Prioritize `.github/copilot/architecture.md`, `tech-stack.md`, `coding-standards.md`, `folder-structure.md`, and `exemplars.md` when they exist. |
| Codebase patterns | Scan similar files for naming, organization, error handling, logging, documentation, and tests when context files are absent. |
| Conflict resolution | Prefer context files first, then newer files or files with higher test coverage when patterns conflict. |
| Architecture | Maintain `${ARCHITECTURE_STYLE}` boundaries and existing communication patterns. |
| Quality | Apply `${CODE_QUALITY_FOCUS}` only through patterns evident in the repository. |
| Assumptions | Explicitly prohibit practices not evidenced by the codebase. |

## Quality focus sections

Include a section only when `${CODE_QUALITY_FOCUS}` equals that focus or `All`.

| Focus | Required guidance |
| --- | --- |
| `Maintainability` | Self-documenting names, established organization, focused functions, and complexity/length matching existing code. |
| `Performance` | Existing memory/resource management, expensive-operation handling, async patterns, and caching. |
| `Security` | Existing input validation, sanitization, parameterized queries, authentication, authorization, and sensitive-data handling. |
| `Accessibility` | Existing ARIA, keyboard navigation, color/contrast, and text alternative patterns. |
| `Testability` | Existing dependency injection, dependency management, mocks, test doubles, and test style. |

## Documentation and testing sections

| Variable condition | Blueprint section |
| --- | --- |
| `${DOCUMENTATION_LEVEL}` = `Minimal` | Match existing comment level, non-obvious behavior documentation, and parameter style. |
| `${DOCUMENTATION_LEVEL}` = `Standard` | Match XML/JSDoc format, parameter/return/exception docs, examples, and class-level documentation. |
| `${DOCUMENTATION_LEVEL}` = `Comprehensive` | Match the most thoroughly documented files, link style, and design-decision detail. |
| `${TESTING_REQUIREMENTS}` includes `Unit` or `All` | Unit test structure, naming, assertions, mocks, and isolation. |
| `${TESTING_REQUIREMENTS}` includes `Integration` or `All` | Integration patterns, test data setup/teardown, component interaction verification. |
| `${TESTING_REQUIREMENTS}` includes `E2E` or `All` | E2E structure, UI testing, and user journey verification. |
| `${TESTING_REQUIREMENTS}` includes `TDD` or `All` | Test-first progression and refactoring patterns visible in the repo. |
| `${TESTING_REQUIREMENTS}` includes `BDD` or `All` | Given-When-Then structure and behavior-focused descriptions. |

## Technology-specific guidance

Include only sections matching `${PROJECT_TYPE}`, `Auto-detect`, or `Multiple`.

| Technology | Guidance to generate |
| --- | --- |
| `.NET` | Detect .NET and C# versions, use compatible language features, match LINQ, async/await, dependency injection, collections, and surrounding code patterns. |
| `Java` | Detect Java version, match design patterns, exception handling, collection usage, and dependency injection. |
| `JavaScript` / `TypeScript` | Detect ECMAScript/TypeScript versions, match imports/exports, type definitions, promises or async/await, and error handling. |
| `React` | Detect React version, match component structure, hooks, lifecycle patterns, state management, and prop typing/validation. |
| `Angular` | Detect Angular version, match components, modules, decorators, RxJS patterns, and component communication. |
| `Python` | Detect Python version, match import organization, type hints, error handling, and module organization. |

## Versioning guidance

| `${VERSIONING}` | Required section |
| --- | --- |
| `Semantic` | Follow Semantic Versioning as applied in the codebase, including breaking changes and deprecations. |
| `CalVer` | Follow Calendar Versioning as applied in the codebase and existing significant-change notation. |
| `Custom` | Match exact observed versioning, changelog, and tagging conventions. |

## Generated blueprint

Use this as the generated artifact, preserving variables:

```markdown
Generate a comprehensive `.github/copilot/copilot-instructions.md` file that guides GitHub Copilot to produce code consistent with this repository's standards, architecture, and technology versions. Base every instruction on actual codebase evidence and avoid assumptions.

# GitHub Copilot Instructions

## Priority guidelines

1. Version compatibility: detect exact languages, frameworks, and libraries before generating code.
2. Context files: prioritize `.github/copilot/architecture.md`, `.github/copilot/tech-stack.md`, `.github/copilot/coding-standards.md`, `.github/copilot/folder-structure.md`, and `.github/copilot/exemplars.md` when present.
3. Codebase patterns: when context files are absent, scan similar files for naming, organization, error handling, logging, documentation, and testing.
4. Architectural consistency: maintain `${ARCHITECTURE_STYLE}` boundaries and established dependency direction.
5. Code quality: prioritize `${CODE_QUALITY_FOCUS}` exactly as demonstrated in the repository.

## Technology version detection

- Detect language versions from project files and configuration, such as `<LangVersion>` in .NET projects.
- Detect framework and library versions from `package.json`, `.csproj`, `pom.xml`, `requirements.txt`, `pyproject.toml`, and equivalent package manifests.
- Never suggest features, APIs, or syntax unavailable in the detected versions.

## Codebase scanning instructions

1. Identify files similar to the file being modified or created.
2. Catalog naming, organization, error handling, logging, documentation, and testing patterns.
3. Follow the most consistent patterns found.
4. When patterns conflict, prioritize `.github/copilot` context, then newer files or files with higher test coverage.
5. Never introduce a pattern that is not present in the repository.

## Quality, documentation, testing, technology, and versioning sections

Generate sections controlled by `${CODE_QUALITY_FOCUS}`, `${DOCUMENTATION_LEVEL}`, `${TESTING_REQUIREMENTS}`, `${PROJECT_TYPE}`, and `${VERSIONING}`. Each section must cite or describe repository evidence for the rule it creates.

## General best practices

- Follow naming conventions exactly as they appear in existing code.
- Match code organization from similar files.
- Apply error handling, logging, configuration, and testing consistently with the codebase.
- Prefer consistency with existing code over external best practices.
```

## Gotchas

- **Do not write generic instructions**: a useful `copilot-instructions.md` names exact versions, files, patterns, and boundaries from this repository.
- **Do not prescribe best practices without evidence**: the blueprint must prefer existing conventions over external ideals.
- **Do not over-constrain undocumented areas**: if the repo has no pattern, instruct GitHub Copilot to inspect nearby code and ask for clarification instead of inventing a standard.


## Required wording to preserve

When generating the blueprint, include `Focus on ${PROJECT_TYPE} technologies` when the user supplies a fixed project type. Preserve the terms `language-specific`, `JavaScript/TypeScript`, `import/export`, `self-documenting`, and `best-documented` so the resulting `copilot-instructions.md` captures version-sensitive language features and documentation standards.

## Output template

```markdown
## Copilot instructions blueprint

**Status:** generated | blocked
**Target file:** `.github/copilot/copilot-instructions.md`
**Project type:** `${PROJECT_TYPE}`
**Architecture:** `${ARCHITECTURE_STYLE}`
**Quality focus:** `${CODE_QUALITY_FOCUS}`

### Blueprint prompt
```markdown
<complete prompt to generate copilot-instructions.md>
```

### Variables used
| Variable | Value |
| --- | --- |
| `${DOCUMENTATION_LEVEL}` | `<value>` |
| `${TESTING_REQUIREMENTS}` | `<value>` |
| `${VERSIONING}` | `<value>` |
```

## Quality gate

- [ ] The blueprint preserves `${PROJECT_TYPE}`, `${ARCHITECTURE_STYLE}`, `${CODE_QUALITY_FOCUS}`, `${DOCUMENTATION_LEVEL}`, `${TESTING_REQUIREMENTS}`, and `${VERSIONING}`.
- [ ] The generated prompt requires exact version detection before code generation.
- [ ] The generated prompt prioritizes `.github/copilot` context files when present.
- [ ] Every quality, documentation, testing, technology, and versioning section is conditional on the variables.
- [ ] The prompt forbids assumptions and practices not evidenced in the codebase.
- [ ] The target path remains `.github/copilot/copilot-instructions.md`.
