---
name: create-agentsmd
description: >-
  Create a high-quality AGENTS.md file for a repository by inspecting project structure,
  workflows, commands, tests, and conventions. Use this skill when the user asks to create,
  update, or improve AGENTS.md, add coding-agent instructions, document repo setup for agents, or
  follow the agents.md format.
---

<!-- Generated from harness/github-copilot/plugins/repo-documentation/skills/create-agentsmd/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create AGENTS.md

Create a complete root `AGENTS.md` that gives coding agents accurate setup, workflow, testing, style, and repository-context instructions without cluttering the human-facing README.

## When to invoke

- "Create an AGENTS.md for this repository."
- "Generate coding agent instructions for my project."
- "Update our AGENTS.md using the current repo structure."
- "Make this repo follow https://agents.md/."
- "Document setup and test commands for agents."

## Prerequisites and context

- The target file is `AGENTS.md` at the repository root unless a monorepo subproject needs a closer nested `AGENTS.md`.
- Follow the open AGENTS.md format at `https://agents.md/.`.
- Use standard Markdown. There are no required fields; include sections only when they help agents work safely and correctly.

## AGENTS.md purpose

| Principle | Rule |
| --- | --- |
| Agent-focused | Include detailed technical instructions automated tools need. |
| Complements `README.md` | Do not duplicate human marketing or onboarding prose. |
| Predictable location | Put root guidance at `AGENTS.md`; use nested files for monorepos when scope differs. |
| Flexible Markdown | Adapt section names to the project instead of forcing irrelevant headings. |
| Ecosystem compatibility | Write portable guidance that works across GitHub Copilot, Cursor, Aider, Gemini CLI, and other coding agents. |

## Procedure

1. Analyze the project structure: languages, frameworks, package managers, build tools, tests, and architecture shape.
2. Inspect source-of-truth files: `package.json`, `.csproj`, `pom.xml`, Gradle files, `Makefile`, CI workflows, existing docs, lint configs, test config, Dockerfiles, and deployment manifests.
3. Extract exact commands for install, development, build, lint, test, coverage, and deployment. Prefer commands already used in CI.
4. Identify code style: naming, file organization, import/export patterns, formatting, linting, and language/framework conventions.
5. Draft `AGENTS.md` with actionable bullets and command snippets.
6. Validate commands when practical; mark unverified commands explicitly instead of inventing success.
7. For monorepos, document package navigation and precedence: the closest `AGENTS.md` governs a given path.

## Recommended content

| Section | Include |
| --- | --- |
| Project Overview | Brief purpose, architecture overview, key technologies and frameworks. |
| Setup Commands | Installation, environment setup, dependency management, database setup. |
| Development Workflow | Dev server, watch/hot reload, package manager specifics. |
| Testing Instructions | Unit, integration, e2e, coverage, file locations, naming conventions, focused test commands. |
| Code Style | Language conventions, linting, formatting, file organization, naming, imports and exports. |
| Build and Deployment | Build outputs, environment configurations, deployment commands, CI/CD requirements. |
| Security Considerations | Secrets management, auth patterns, permissions, security tests. |
| Monorepo Instructions | Package navigation, selective builds/tests, cross-package dependencies. |
| Pull Request Guidelines | Title format, required checks, review process, commit conventions. |
| Debugging and Troubleshooting | Common issues, logging, debug configuration, performance notes. |

## Command discovery targets

| Ecosystem | Files to inspect | Commands to look for |
| --- | --- | --- |
| Node/TypeScript | `package.json`, lockfiles, `turbo.json`, `vite.config.*`, `tsconfig.json` | `npm`, `pnpm`, `yarn`, `pnpm turbo run test --filter <project_name>`, `pnpm vitest run -t "<test name>"` |
| .NET | `*.sln`, `*.csproj`, `Directory.Build.props`, `.config/dotnet-tools.json` | `dotnet restore`, `dotnet build`, `dotnet test` |
| Java | `pom.xml`, `build.gradle`, `settings.gradle` | `mvn test`, `mvn verify`, `gradle test`, `./gradlew build` |
| Python | `pyproject.toml`, `requirements*.txt`, `tox.ini`, `noxfile.py` | `python -m pytest`, `ruff check`, `mypy`, environment setup commands |
| CI/CD | `.github/workflows/*`, pipeline YAML | Required checks and exact CI command names. |

## Template for the generated file

```markdown
# AGENTS.md

## Project Overview

<Brief description of the project, its purpose, and key technologies.>

## Setup Commands

- Install dependencies: `<package manager> install`
- Start development server: `<command>`
- Build for production: `<command>`

## Development Workflow

- <Development server startup instructions>
- <Hot reload/watch mode information>
- <Environment variable setup>

## Testing Instructions

- Run all tests: `<command>`
- Run unit tests: `<command>`
- Run integration tests: `<command>`
- Test coverage: `<command>`
- <Specific testing patterns or requirements>

## Code Style

- <Language and framework conventions>
- <Linting rules and commands>
- <Formatting requirements>
- <File organization patterns>

## Build and Deployment

- <Build process details>
- <Output directories>
- <Environment-specific builds>
- <Deployment commands>

## Pull Request Guidelines

- Title format: <component> Brief description
- Required checks: `<lint command>`, `<test command>`
- <Review requirements>

## Additional Notes

- <Project-specific context>
- <Common gotchas or troubleshooting tips>
- <Performance considerations>
```

## Examples

### Good

- `Use pnpm dlx turbo run where <project_name> to jump to a package instead of scanning with ls.`
- `Run pnpm install --filter <project_name> to add the package to your workspace so Vite, ESLint, and TypeScript can see it.`
- `Run pnpm turbo run test --filter <project_name> for every check defined for that package.`
- `After moving files or changing imports, run pnpm lint --filter <project_name>.`

### Bad

- `Run the tests.` without naming the command.
- `Follow our usual style.` without linking it to files or examples.
- Copying the full README instead of agent-specific instructions.
- Stating commands that are not present in project files and were not verified.

## Gotchas

- **Closest file wins in monorepos**: root `AGENTS.md` should explain global rules; nested files should contain package-specific overrides.
- **Do not over-document human context**: agents need commands, conventions, and boundaries more than product narrative.
- **Do not invent workflows**: if CI is the only source of truth, derive commands from `.github/workflows` and label anything unverified.

## AGENTS.md terminology

Preserve project guidance terms that agents search for: `Import/export`, `Watch/hot-reload`, `[command]`, `[lint command]`, `[package manager] install`, `[test command]`, `building/testing`, `hot-reload`, `human-focused`, `packages/projects`, `pnpm dlx turbo run where <project_name>`, `pnpm install --filter <project_name>`, `pnpm lint`, `pnpm lint --filter <project_name>`, `pnpm test`, `project-specific`, `react-ts`, and `top-level`.

## Output template

```markdown
## AGENTS.md result

**Status:** created | updated | blocked
**Path:** `AGENTS.md`
**Scope:** root | monorepo package `<path>`

### Sources inspected
- `<file>`: <facts used>

### Sections included
- Project Overview
- Setup Commands
- Development Workflow
- Testing Instructions
- Code Style
- Build and Deployment
- Pull Request Guidelines
- Additional Notes

### Validation
- `<command>`: pass | fail | not run (<reason>)
```

## Quality gate

- [ ] `AGENTS.md` is at the repository root or the correct monorepo subproject root.
- [ ] Setup, build, test, lint, and deployment commands come from repository sources or are marked unverified.
- [ ] The file includes agent-focused technical guidance, not duplicated README prose.
- [ ] Monorepo precedence and package-specific commands are documented when applicable.
- [ ] Markdown is clear, portable, and uses exact commands in backticks.
- [ ] The final response lists the sources inspected and any commands not validated.

## References

- [AGENTS.md](https://agents.md/.)
