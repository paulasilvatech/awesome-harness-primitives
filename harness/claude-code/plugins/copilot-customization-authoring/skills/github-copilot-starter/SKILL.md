---
name: github-copilot-starter
description: >-
  Bootstrap a complete GitHub Copilot customization for a repository, including
  .github/copilot-instructions.md, scoped instruction files, reusable skills, custom agents, and
  optional copilot-setup-steps.yml. Use this skill when the user asks to set up GitHub Copilot for
  a new project, create Copilot instructions/skills/agents, adapt awesome-copilot examples, or
  configure Coding Agent setup steps for a technology stack.
---

<!-- Generated from harness/github-copilot/plugins/copilot-customization-authoring/skills/github-copilot-starter/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GitHub Copilot starter

Create a production-ready `.github/` Copilot customization for a repository by gathering project context, researching `awesome-copilot` examples, generating instructions, skills, agents, and optional Coding Agent setup workflow files, then reporting how to use and customize them.

## When to invoke

- "Set up GitHub Copilot customization for this repo."
- "Create Copilot instructions, skills, and agents for my project."
- "Bootstrap GitHub Copilot for a React, Python, Java, or .NET stack."
- "Add a copilot-setup-steps.yml workflow."
- "Adapt awesome-copilot examples for this repository."

## Inputs

If the user did not provide these details, infer them from repository files first and ask only for missing decisions that change generated files.

| Input | Examples | Why it matters |
| --- | --- | --- |
| Primary language/framework | JavaScript/React, Python/Django, Java/Spring Boot, C#/.NET, Flutter | Chooses language instruction files, agents, runtime setup, and test commands. |
| Project type | web app, API, mobile app, desktop app, library | Shapes agents, skills, documentation, and security/performance guidance. |
| Additional technologies | database, cloud provider, test framework, package manager | Adds focused instructions and setup steps. |
| Development style | strict standards, flexible, domain-specific patterns | Sets tone and enforcement level. |
| GitHub Actions / Coding Agent | yes or no | Determines whether to create `.github/workflows/copilot-setup-steps.yml`. |

## Procedure

1. Inspect the repository for stack signals before asking questions.
2. Research `awesome-copilot` examples with web fetch before generating content:
   - https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md
   - https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md
   - https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md
   - https://github.com/github/awesome-copilot/tree/main/instructions
   - https://github.com/github/awesome-copilot/tree/main/agents
   - https://github.com/github/awesome-copilot/tree/main/skills
3. Prefer exact technology matches; otherwise combine nearby proven examples. Use simple custom guidance only when no relevant source exists.
4. Add attribution comments whenever content is based on or inspired by `awesome-copilot`.
5. Create `.github/copilot-instructions.md`, scoped instruction files, reusable skill folders, and four custom agents.
6. Create `.github/workflows/copilot-setup-steps.yml` only when the project uses GitHub Actions or the user asks for Coding Agent setup.
7. Validate frontmatter, file names, links, and workflow shape.
8. Return setup instructions, usage examples, customization tips, and testing recommendations.

## File set to create

```text
project-root/
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   │   ├── [language].instructions.md
│   │   ├── testing.instructions.md
│   │   ├── documentation.instructions.md
│   │   ├── security.instructions.md
│   │   ├── performance.instructions.md
│   │   └── code-review.instructions.md
│   ├── skills/
│   │   ├── setup-component/
│   │   │   └── SKILL.md
│   │   ├── write-tests/
│   │   │   └── SKILL.md
│   │   ├── code-review/
│   │   │   └── SKILL.md
│   │   ├── refactor-code/
│   │   │   └── SKILL.md
│   │   ├── generate-docs/
│   │   │   └── SKILL.md
│   │   └── debug-issue/
│   │       └── SKILL.md
│   ├── agents/
│   │   ├── software-engineer.agent.md
│   │   ├── architect.agent.md
│   │   ├── reviewer.agent.md
│   │   └── debugger.agent.md
│   └── workflows/
│       └── copilot-setup-steps.yml
```

Skip `.github/workflows/copilot-setup-steps.yml` entirely when GitHub Actions is out of scope.

## Repository instruction content

Create `.github/copilot-instructions.md` as the root guidance GitHub Copilot reads for every repository interaction.

```md
# {Project Name} — Copilot Instructions

## Project Overview
Brief description of what this project does and its primary purpose.

## Tech Stack
List the primary language, frameworks, and key dependencies.

## Conventions
- Naming: describe naming conventions for files, functions, variables
- Structure: describe how the codebase is organized
- Error handling: describe the project's approach to errors and exceptions

## Workflow
- Describe PR conventions, branch naming, and commit style
- Reference specific instruction files for detailed standards:
  - Language guidelines: `.github/instructions/{language}.instructions.md`
  - Testing: `.github/instructions/testing.instructions.md`
  - Security: `.github/instructions/security.instructions.md`
  - Documentation: `.github/instructions/documentation.instructions.md`
  - Performance: `.github/instructions/performance.instructions.md`
  - Code review: `.github/instructions/code-review.instructions.md`
```

## Scoped instruction files

Instruction files must contain standards, not implementation examples. Avoid code snippets, test code, boilerplate, function signatures, imports, dependency lists, and detailed implementation steps.

```md
<!-- Based on/Inspired by: https://github.com/github/awesome-copilot/blob/main/instructions/{filename}.instructions.md -->
---
applyTo: "**/*.{lang-ext}"
description: "Development standards for {Language}"
---
# {Language} coding standards

Apply the repository-wide guidance from `../copilot-instructions.md` to all code.

## General Guidelines
- Follow the project's established conventions and patterns.
- Prefer clear, readable code over clever abstractions.
- Use the language's idiomatic style and recommended practices.
- Keep modules focused and appropriately sized.
```

Good instruction statements include "Use descriptive variable names and follow camelCase", "Prefer composition over inheritance", "Write unit tests for all public methods", "Use TypeScript strict mode for better type safety", and "Follow the repository's established error handling patterns".

Attribution examples to preserve when sources are used:

```md
<!-- Based on: https://github.com/github/awesome-copilot/blob/main/instructions/nodejs-javascript-vitest.instructions.md -->
<!-- Inspired by: https://github.com/github/awesome-copilot/blob/main/instructions/java-junit5-assertions.instructions.md -->
<!-- and: https://github.com/github/awesome-copilot/blob/main/instructions/springboot.instructions.md -->
```

## Skills and agents

Create six skill folders: `setup-component`, `write-tests`, `code-review`, `refactor-code`, `generate-docs`, and `debug-issue`. Each `SKILL.md` needs `name`, `description`, one H1, usage triggers, requirements, output template, and quality gate.

```md
---
name: {skill-name}
description: {Brief description of what this skill does and when to use it}
---

# {Skill Name}

{One sentence describing what this skill does. Always follow the repository's established patterns.}

Ask for {required inputs} if not provided.

## Requirements
- Use the existing design system and repository conventions.
- Follow the project's established patterns and style.
- Adapt to the specific technology choices of this stack.
- Reuse existing validation and documentation patterns.
```

Always create these agents: `software-engineer.agent.md`, `architect.agent.md`, `reviewer.agent.md`, and `debugger.agent.md`. Fetch the most specific matching agent from `awesome-copilot`; if no match exists, use a generic planning/review/debugging template. When using a source agent, add:

```markdown
<!-- Based on/Inspired by: https://github.com/github/awesome-copilot/blob/main/agents/{filename}.agent.md -->
```

Generic agent frontmatter may use VS Code tool IDs only when targeting VS Code agent files:

```md
---
description: Generate an implementation plan for new features or refactoring existing code.
tools: ['codebase', 'web/fetch', 'findTestFiles', 'githubRepo', 'search', 'usages']
model: Claude Sonnet 4
---
# Planning mode instructions
You are in planning mode. Your task is to generate an implementation plan for a new feature or for refactoring existing code.
Don't make any code edits, just generate a plan.
```

## Coding Agent workflow

Create `.github/workflows/copilot-setup-steps.yml` only when GitHub Actions is used. Keep it simple: runtime setup, dependency installation, lint, test, and build only when those are standard for the stack. Avoid complex configuration, multiple environment configurations, external services, custom scripts, databases, advanced tooling, or multiple package managers.

```yaml
name: "Copilot Setup Steps"
on:
  workflow_dispatch:
  push:
    paths:
      - .github/workflows/copilot-setup-steps.yml
  pull_request:
    paths:
      - .github/workflows/copilot-setup-steps.yml
jobs:
  copilot-setup-steps:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout code
        uses: actions/checkout@v5
```

| Stack | Simple steps |
| --- | --- |
| Node.js/JavaScript | `actions/setup-node@v4` with `node-version: "20"` and `cache: "npm"`, `npm ci`, `npm run lint`, `npm test`. |
| Python | `actions/setup-python@v4` with `python-version: "3.11"`, `pip install -r requirements.txt`, `flake8 .`, `pytest`. |
| Java | `actions/setup-java@v4` with `java-version: "17"` and `distribution: "temurin"`, `mvn compile`, `mvn test`. |

The job name must be exactly `copilot-setup-steps`, or GitHub Copilot will not pick it up.

## Gotchas

- **Fetch before authoring**: do not invent formats until `awesome-copilot` docs and relevant directories have been checked.
- **Instructions are standards, not snippets**: keep `.instructions.md` files high-level and avoid code examples.
- **Attribution is required**: every adapted `awesome-copilot` instruction, skill, or agent needs a source comment.
- **Do not create workflow complexity**: `copilot-setup-steps.yml` should prepare the agent environment, not reproduce production infrastructure.
- **Use environment-appropriate tools**: VS Code agent `tools:` entries are not CLI skill `allowed-tools` entries.

## Technical index

Preserve these setup paths, file names, and source-prompt constraints when creating a starter package: `.github/instructions/`, `.github/skills/`, `.github/agents/`, `.github/workflows/`, `github/workflows/`, `{primaryLanguage}.instructions.md`, `testing.instructions.md`, `documentation.instructions.md`, `security.instructions.md`, `performance.instructions.md`, `code-review.instructions.md`, `setup-component/SKILL.md`, `write-tests/SKILL.md`, `code-review/SKILL.md`, `refactor-code/SKILL.md`, `generate-docs/SKILL.md`, `debug-issue/SKILL.md`, `Language/Framework**`, `Component/module`, `Language/runtime`, `language-specific`, `technology-specific`, `project-wide`, `repo-native`, `self-contained`, `coding-agent`, `MCP/tool-related`, `tool-related`, `MANDATORY`, `FIRST`, `STEP`, `ALWAYS`, `CRITICAL`, `MUST`, `STRICTLY`, `AVOID`, `CORRECT`, `GUIDELINES`, `KEEP`, `SIMPLE`, `WORKFLOWS`, `INCLUDE`, and `ONLY`.

## Output template

```markdown
## GitHub Copilot starter result

**Status:** created | partially created | blocked
**Project stack:** <detected or provided stack>
**GitHub Actions / Coding Agent:** <yes/no>

### Files created
| Path | Purpose | Source |
| --- | --- | --- |
| `.github/copilot-instructions.md` | repository-wide guidance | <custom or awesome-copilot source> |
| `.github/instructions/<file>.instructions.md` | scoped standards | <source URL or custom> |
| `.github/skills/<skill>/SKILL.md` | reusable workflow | <source URL or custom> |
| `.github/agents/<agent>.agent.md` | specialized custom agent | <source URL or custom> |
| `.github/workflows/copilot-setup-steps.yml` | Coding Agent setup | <included/skipped> |

### Usage
- <how to use the generated instructions, skills, and agents>

### Customization tips
- <what the user should tailor next>

### Validation
- Frontmatter: <pass/fail>
- Attribution comments: <pass/fail>
- Workflow shape: <pass/fail/not applicable>
```

## Quality gate

- [ ] Project information was inferred or requested before generation.
- [ ] `awesome-copilot` instruction, agent, and skill docs were checked before writing content.
- [ ] `.github/copilot-instructions.md` describes project overview, tech stack, conventions, and workflow.
- [ ] Scoped instruction files have YAML frontmatter and contain standards rather than code snippets.
- [ ] Six skill folders and four agent files are created unless the user narrows scope.
- [ ] Adapted content includes attribution comments with absolute `awesome-copilot` URLs.
- [ ] `copilot-setup-steps.yml`, when created, uses job name `copilot-setup-steps`, simple triggers, `contents: read`, and basic stack setup only.
- [ ] Final response includes VS Code setup instructions, usage examples, customization tips, and testing recommendations.

## References

- [awesome-copilot instructions docs](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md)
- [awesome-copilot agents docs](https://github.com/github/awesome-copilot/blob/main/docs/README.agents.md)
- [awesome-copilot skills docs](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md)
- [awesome-copilot instructions directory](https://github.com/github/awesome-copilot/tree/main/instructions)
- [awesome-copilot agents directory](https://github.com/github/awesome-copilot/tree/main/agents)
- [awesome-copilot skills directory](https://github.com/github/awesome-copilot/tree/main/skills)
