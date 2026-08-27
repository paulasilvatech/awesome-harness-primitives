---
name: create-readme
description: >-
  Create or improve a concise, appealing, project-specific README.md with a clear overview, setup,
  usage, and practical examples. Use this skill when the user asks to generate, refresh, polish,
  rewrite, or make a repository README more useful for GitHub readers.
---

<!-- Generated from harness/github-copilot/skills/create-readme/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create README

Review the repository, infer the project purpose and usage from real files, and produce a concise, comprehensive, and well-structured GitHub Flavored Markdown README.md that is attractive, accurate, and free of boilerplate sections owned by separate files.

## When to invoke

- "Create a README for this repository."
- "Refresh or polish the README.md."
- "Make this project README more appealing and useful."
- "Generate setup and usage instructions from the codebase."

## README content model

| Section | Include when | Content rule |
| --- | --- | --- |
| Header | Always | Project name, one-line value proposition, and logo/icon if one exists in the repository. |
| Overview | Always | Explain what the project does, who it is for, and why it exists. |
| Features | When meaningful capabilities exist | Use short bullets grounded in repository behavior, not generic claims. |
| Architecture or stack | When the stack affects setup or use | Mention frameworks, services, CLI tools, and major directories discovered in the project. |
| Getting started | Always for runnable projects | Provide prerequisites, install, configure, and run commands from package files or docs. |
| Usage | When the project exposes an app, CLI, API, library, or workflow | Show the shortest successful example and expected result. |
| Configuration | When environment variables or config files exist | List required variables without inventing secret values. |
| Testing | When tests exist | Include the existing test command only. |
| Troubleshooting | When common setup issues are evident | Keep concise and actionable. |

Do not include sections like `LICENSE`, `CONTRIBUTING`, `CHANGELOG`, etc. There are dedicated files for those sections.

## Procedure

1. Review the entire project and workspace enough to identify its purpose, entry points, package managers, setup commands, and existing docs.
2. Prefer facts from files such as `package.json`, `pyproject.toml`, `README.md`, `Dockerfile`, `compose.yaml`, `.env.example`, workflow files, and source entry points.
3. If a logo or icon exists, use it in the README header with a relative path that is valid from `README.md`.
4. Write concise GitHub Flavored Markdown. Use tables, fenced code blocks, and GitHub admonition syntax where appropriate.
5. Keep the README project-specific; remove placeholders, marketing fluff, and unsupported claims.

## Style rules

- Use a confident senior open-source maintainer voice: clear, helpful, and direct.
- Keep the readme concise and to the point.
- Do not overuse emojis; this repository rebuild forbids emojis in skill text, and generated README content should use them only if the project style clearly requires them.
- Use GFM (GitHub Flavored Markdown) for formatting, and GitHub admonition syntax when a warning or note is genuinely useful.
- Make commands copy-pasteable and avoid chaining commands that hide failing steps.

## Inspiration sources

Use these README files for structure, tone, and content patterns without copying project-specific claims:

| Source | Useful pattern |
| --- | --- |
| `https://raw.githubusercontent.com/Azure-Samples/serverless-chat-langchainjs/refs/heads/main/README.md` | Clear cloud sample overview and deployment-oriented setup. |
| `https://raw.githubusercontent.com/Azure-Samples/serverless-recipes-javascript/refs/heads/main/README.md` | Practical sample structure and concise usage flow. |
| `https://raw.githubusercontent.com/sinedied/run-on-output/refs/heads/main/README.md` | Compact tool positioning and example-first usage. |
| `https://raw.githubusercontent.com/sinedied/smoke/refs/heads/main/README.md` | Short, appealing project introduction and focused commands. |
| `https://github.com/orgs/community/discussions/16925` | GitHub admonition syntax reference. |

## Gotchas

- **Do not invent commands**: if setup or test commands are absent, say what was found instead of fabricating `npm install` or `pytest`.
- **Do not duplicate governance files**: link or mention dedicated files only when useful; do not add full `LICENSE`, `CONTRIBUTING`, or `CHANGELOG` sections.
- **Do not write a generic README**: every feature, command, and path must come from the repository or be clearly framed as a user-supplied assumption.

## Output template

````markdown
# <Project name>

<One-sentence value proposition.>

[Optional logo/icon]

## Overview

<What it does, who it helps, and the main workflow.>

## Features

- <specific capability>
- <specific capability>

## Getting started

### Prerequisites

- <tool/version or service>

### Install

```bash
<install command>
```

### Run

```bash
<run command>
```

## Usage

```bash
<minimal example>
```

## Configuration

| Name | Required | Purpose |
| --- | --- | --- |
| `<env-or-setting>` | yes/no | <purpose> |

## Testing

```bash
<test command>
```
````

## Quality gate

- [ ] The README is based on actual repository files, not generic assumptions.
- [ ] Setup, run, usage, and test commands are copied from existing project configuration or clearly omitted when absent.
- [ ] No full `LICENSE`, `CONTRIBUTING`, or `CHANGELOG` sections were added.
- [ ] Any logo or icon path exists and is valid from `README.md`.
- [ ] GitHub Flavored Markdown renders cleanly, with fenced code blocks closed.
- [ ] The README remains concise and project-specific.

## References

- [Azure Samples serverless chat README](https://raw.githubusercontent.com/Azure-Samples/serverless-chat-langchainjs/refs/heads/main/README.md)
- [Azure Samples serverless recipes README](https://raw.githubusercontent.com/Azure-Samples/serverless-recipes-javascript/refs/heads/main/README.md)
- [run-on-output README](https://raw.githubusercontent.com/sinedied/run-on-output/refs/heads/main/README.md)
- [smoke README](https://raw.githubusercontent.com/sinedied/smoke/refs/heads/main/README.md)
- [GitHub admonition syntax discussion](https://github.com/orgs/community/discussions/16925)
