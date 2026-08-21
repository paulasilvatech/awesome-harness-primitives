---
name: readme-blueprint-generator
description: >-
  Generate a comprehensive README.md blueprint by analyzing repository documentation, .github/copilot files, copilot-instructions.md, architecture notes, technology stack, workflow, standards, tests, and exemplars. Use when asked to create or refresh a developer-focused README.
---

# README blueprint generator

Analyze repository guidance and project documentation, extract the facts a new developer or user needs, and produce a concise, well-structured `README.md` with high-level architecture, cross-references, Markdown formatting, and no invented project claims.

## When to invoke

- "Generate a README for this repository."
- "Create a README.md from our GitHub Copilot docs."
- "Build a README blueprint from .github/copilot."
- "Refresh the README with architecture, stack, workflow, and tests."
- "Use copilot-instructions.md to document this project."

## Source inventory

Scan the repository for these sources, using available files as evidence and noting gaps rather than inventing content:

| Source | Extract |
| --- | --- |
| `.github/copilot/Architecture` | Project architecture, major components, diagrams, runtime boundaries. |
| `.github/copilot/Code_Exemplars` | Contribution examples, conventions, patterns worth linking. |
| `.github/copilot/Coding_Standards` | Naming, formatting, review, and implementation rules. |
| `.github/copilot/Project_Folder_Structure` | Directory map and ownership of major folders. |
| `.github/copilot/Technology_Stack` | Languages, frameworks, tools, and versions when available. |
| `.github/copilot/Unit_Tests` | Test framework, commands, coverage expectations, fixtures. |
| `.github/copilot/Workflow_Analysis` | Branching, PR flow, release, CI, and development workflow. |
| `.github/copilot-instructions.md` or `.github/copilot-instructions.md` equivalent | Repository-wide instructions and conventions. |
| Existing `README.md`, package manifests, workflow files | Fill missing setup, commands, badges, and license facts only when evidenced. |

## README sections

| Section | Required content | Primary source |
| --- | --- | --- |
| Project name and description | Project name, purpose, and what it does. | Existing README, manifests, architecture docs. |
| Technology stack | Languages, frameworks, services, versions when available. | `Technology_Stack`. |
| Project architecture | High-level architecture and simple diagram if already described. | `Architecture`. |
| Getting started | Prerequisites, installation, setup, configuration, first run. | Stack docs, manifests, existing scripts. |
| Project structure | Brief folder overview. | `Project_Folder_Structure`. |
| Key features | Main functionality and user/developer value. | Architecture and project docs. |
| Development workflow | Branching, PR, CI, release, and local workflow. | `Workflow_Analysis`. |
| Coding standards | Project-specific conventions. | `Coding_Standards`, `copilot-instructions.md`. |
| Testing | Test approach, commands, and tools. | `Unit_Tests`, package scripts, workflows. |
| Contributing | How to contribute and where exemplars live. | `Code_Exemplars`, instructions. |
| License | License name or "Not specified" if no evidence exists. | `LICENSE`, package metadata, existing docs. |

## Generation rules

- Prefer facts from documentation over guesses from code shape.
- Include version information only when a source states it.
- Use badges only when build status, package version, coverage, or license data is available.
- Include links to repository-local documentation files when they exist and are useful.
- Keep the README concise yet informative; optimize for a new developer's first successful setup.
- Use clear headings, subheadings, lists, tables, and fenced code blocks for commands.
- If a source file is missing, omit the unsupported detail or add a short "Not documented yet" note only when the gap matters.

## Gotchas

- **Do not fabricate setup commands**: derive commands from manifests, scripts, or existing docs.
- **Do not overfit to `.github/copilot` names**: some repositories may use equivalent documentation; preserve source evidence.
- **Do not turn README into an architecture spec**: link deeper docs and keep the README navigational.
- **Do not include empty badges or placeholder links**: every badge and link must resolve to real repository content.

## Output template

```markdown
# <Project Name>

<One-paragraph description of what the project does and who it is for.>

## Technology stack

| Area | Technology | Version/source |
| --- | --- | --- |
| <area> | <tool/framework> | <version or source file> |

## Architecture

<High-level architecture summary.>

## Getting started

### Prerequisites
- <requirement>

### Install
```bash
<install command>
```

### Run
```bash
<run command>
```

## Project structure

| Path | Purpose |
| --- | --- |
| `<path>` | <purpose> |

## Key features

- <feature>

## Development workflow

<workflow summary>

## Coding standards

- <standard>

## Testing

```bash
<test command>
```

## Contributing

<contribution guidance and links to exemplars>

## License

<license or "Not specified in repository files.">
```

## Quality gate

- [ ] `.github/copilot` and `copilot-instructions.md` sources were scanned when present.
- [ ] Architecture, technology stack, project structure, workflow, standards, tests, exemplars, and license are either documented or explicitly omitted for lack of evidence.
- [ ] Commands, versions, badges, and links are backed by repository files.
- [ ] The README is concise, developer-focused, and formatted as valid Markdown.
- [ ] No unsupported project claims or placeholder sections remain.
