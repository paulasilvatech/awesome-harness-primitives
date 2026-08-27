---
name: code-exemplars-blueprint-generator
description: >-
  Generate a configurable prompt blueprint for scanning a codebase and producing an exemplars.md
  catalog of high-quality, real code examples. Use this skill when the user asks for code
  exemplars, exemplar blueprint prompts, coding standard examples, repository pattern catalogs, or
  configuration variables for exemplar generation.
---

<!-- Generated from harness/github-copilot/plugins/codebase-blueprints/skills/code-exemplars-blueprint-generator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Code exemplars blueprint generator

Turn the user's exemplar-generation settings into a complete prompt that instructs GitHub Copilot to scan real repository files, choose representative code patterns, and create an actionable `exemplars.md` document.

## When to invoke

- "Generate a prompt to find code exemplars in this repo."
- "Create an exemplars.md blueprint for our coding standards."
- "Give me configuration variables for scanning examples."
- "Find representative .NET, Java, React, Angular, Python, or TypeScript patterns."
- "Build a prompt that catalogs high-quality code examples."

## Inputs

Use `$ARGUMENTS` as optional configuration text. Accept explicit values for `PROJECT_TYPE`, `SCAN_DEPTH`, `INCLUDE_CODE_SNIPPETS`, `CATEGORIZATION`, `MAX_EXAMPLES_PER_CATEGORY`, and `INCLUDE_COMMENTS`; otherwise use the defaults in the configuration table.

## Configuration variables

| Variable | Allowed values | Default | Controls |
| --- | --- | --- | --- |
| `PROJECT_TYPE` | `Auto-detect`, `.NET`, `Java`, `JavaScript`, `TypeScript`, `React`, `Angular`, `Python`, `Other` | `Auto-detect` | Which languages and frameworks the generated prompt emphasizes. |
| `SCAN_DEPTH` | `Basic`, `Standard`, `Comprehensive` | `Standard` | How much project-wide convention and architecture analysis to request. |
| `INCLUDE_CODE_SNIPPETS` | `true`, `false` | `true` | Whether `exemplars.md` includes short snippets as well as file paths. |
| `CATEGORIZATION` | `Pattern Type`, `Architecture Layer`, `File Type` | `Pattern Type` | How examples are grouped. |
| `MAX_EXAMPLES_PER_CATEGORY` | Positive integer | `3` | Maximum exemplars in each category. |
| `INCLUDE_COMMENTS` | `true`, `false` | `true` | Whether each exemplar explains key implementation details and principles. |

Render these settings in the generated prompt as literal configuration assignments when useful:

```text
${PROJECT_TYPE="Auto-detect|.NET|Java|JavaScript|TypeScript|React|Angular|Python|Other"}
${SCAN_DEPTH="Basic|Standard|Comprehensive"}
${INCLUDE_CODE_SNIPPETS=true|false}
${CATEGORIZATION="Pattern Type|Architecture Layer|File Type"}
${MAX_EXAMPLES_PER_CATEGORY=3}
${INCLUDE_COMMENTS=true|false}
```

## Exemplar selection criteria

Only include actual files that exist in the codebase. Never invent hypothetical examples.

| Criterion | What to look for | Reject when |
| --- | --- | --- |
| Readability | Clear naming, small units, visible intent | Clever but opaque implementation. |
| Documentation | Helpful comments, docstrings, or README-backed usage | Comments repeat syntax without explaining why. |
| Error handling | Explicit validation, typed errors, recoverable failure paths | Exceptions swallowed or converted to vague messages. |
| Architecture fit | Separation of concerns, dependency direction, conventional boundaries | Feature code bypasses layers or central conventions. |
| Tests | Representative unit, integration, or component tests | Tests only assert imports or snapshots with no behavior. |
| Maintainability | Low duplication, simple control flow, standard patterns | Code smell is present even if the file is common. |

## Category catalog

Include only categories relevant to the detected or requested stack.

| Stack | Candidate categories |
| --- | --- |
| `.NET` | Domain Models, Repository Implementations, Service Layer Components, Controller Patterns, Dependency Injection Usage, Middleware Components, Unit Test Patterns. |
| Frontend (`JavaScript`, `TypeScript`, `React`, `Angular`) | Component Structure, State Management, API Integration, Form Handling, Routing Implementation, UI Components, Unit Test Examples. |
| `Java` | Entity Classes, Service Implementations, Repository Patterns, Controller/Resource Classes, Configuration Classes, Unit Tests. |
| `Python` | Class Definitions, API Routes/Views, Data Models, Service Functions, Utility Modules, Test Cases. |
| Architecture layer grouping | Presentation Layer, Business Logic Layer, Data Access Layer, Cross-Cutting Concerns such as logging, error handling, authentication/authorization, and validation. |

When `SCAN_DEPTH` is `Comprehensive`, ask the downstream scan to add Consistency Patterns, Architecture Observations, Implementation Conventions, and Anti-patterns to Avoid.

## Generated prompt requirements

The generated prompt must instruct GitHub Copilot to:

1. Detect primary languages and frameworks from file extensions and configuration files when `PROJECT_TYPE` is `Auto-detect`; otherwise focus on the requested stack.
2. Identify high-quality implementation, documentation, test, and structure examples.
3. Prioritize files that demonstrate standards the team should copy.
4. Verify every referenced path exists.
5. Document file path, description, pattern/component type, optional key implementation comments, and optional short snippets.
6. Create `exemplars.md` with an introduction, table of contents, organized sections based on `CATEGORIZATION`, no more than `MAX_EXAMPLES_PER_CATEGORY` examples per category, and maintenance recommendations.

## Prompt fragments to preserve

The generated prompt may include exact conditional language such as `Focus on ${PROJECT_TYPE} code files` when `PROJECT_TYPE` is not `Auto-detect`. Preserve stack category labels including `Controllers/API`, `Routes/Views**`, `models/DTOs`, and `Authentication/authorization` when the target repository uses those layers. Prefer the phrase `well-structured` for exemplar quality because the downstream artifact should distinguish representative files from merely functional files.

## Output template

```markdown
## Code exemplars blueprint

**Status:** ready
**Configuration:** `PROJECT_TYPE=<value>`, `SCAN_DEPTH=<value>`, `INCLUDE_CODE_SNIPPETS=<true/false>`, `CATEGORIZATION=<value>`, `MAX_EXAMPLES_PER_CATEGORY=<n>`, `INCLUDE_COMMENTS=<true/false>`

### Generated prompt
```text
Scan this codebase and generate an exemplars.md file that identifies high-quality, representative code examples. The exemplars should demonstrate our coding standards and patterns to help maintain consistency.

Configuration:
- PROJECT_TYPE: <value>
- SCAN_DEPTH: <value>
- INCLUDE_CODE_SNIPPETS: <true/false>
- CATEGORIZATION: <value>
- MAX_EXAMPLES_PER_CATEGORY: <n>
- INCLUDE_COMMENTS: <true/false>

<complete scan instructions, stack categories, documentation format, and verification rules>
```

### Expected artifact
`exemplars.md` containing real repository file references, organized categories, and actionable guidance for developers implementing new features consistently.
```

## Quality gate

- [ ] All six configuration variables are present and resolved to allowed values.
- [ ] The generated prompt requires real existing file paths and bans hypothetical examples.
- [ ] Stack-specific categories match `PROJECT_TYPE` or auto-detection.
- [ ] `SCAN_DEPTH=Comprehensive` includes consistency patterns, architecture observations, implementation conventions, and anti-patterns.
- [ ] The output artifact is literally named `exemplars.md`.
- [ ] The prompt caps each category at `MAX_EXAMPLES_PER_CATEGORY`.
