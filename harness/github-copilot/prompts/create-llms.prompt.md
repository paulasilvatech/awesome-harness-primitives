---
name: 'create-llms'
description: 'Create an llms.txt file from the repository structure that follows the llms.txt specification.'
agent: 'agent'
tools: ['read', 'search', 'edit', 'web']
argument-hint: 'target=llms.txt'
---

# /create-llms

## Objective

Create a root `llms.txt` file from the repository structure that complies with the official llms.txt specification at https://llmstxt.org/ and gives LLMs a concise, accurate, human-readable entry point for understanding the repository's purpose, documentation, specifications, examples, and configuration.

## When to Invoke

Use this prompt when a repository does not yet have `llms.txt`, or when the team explicitly wants to regenerate the LLM navigation file from scratch.

## Preconditions

- The repository root is available for inspection.
- A new root `/llms.txt` file may be created or overwritten with approval.
- The official specification at https://llmstxt.org/ can be reviewed or is already known.
- Important documentation, specifications, examples, and configuration files are present or their absence can be reported.

## Inputs the Team Must Provide

- `target` — normally `llms.txt` at repository root.
- Repository or project name if it is not clear from `README.md` or repository metadata.
- Any file categories the team requires, such as Documentation, Specifications, Examples, Configuration, or Optional.
- Ask the user for anything that is missing when it affects the project purpose, scope, or permission to create the file.

## What I Will Do

- Review https://llmstxt.org/ before creating the file.
- Inspect the complete repository structure, read `README.md` when present, and identify the primary purpose and scope.
- Catalog important directories, README files, documentation files, `.md` files in `/docs/`, `/spec/`, specification files, configuration files, examples, and code samples.
- Prioritize files for LLM understanding and group them into logical H2 sections.
- Create `llms.txt` at the repository root with valid Markdown links and concise descriptions.

## What I Will NOT Do

- Include generated content, build artifacts, redundant files, or files that do not help an LLM understand the project.
- Invent a project purpose, file description, or specification link when repository evidence is insufficient.
- Use absolute paths in file links; llms.txt links must be repository-relative URLs.
- Skip link validation before reporting success.
- Create unrelated documentation or modify files other than `/llms.txt` unless explicitly requested.

## Output Format

Create `llms.txt` with this shape:

```txt
# [Repository Name]

> [Concise description of the repository's purpose and scope]

[Optional additional context paragraphs without headings]

## Documentation

- [Main README](README.md): Primary project documentation and getting started guide
- [Contributing Guide](CONTRIBUTING.md): Guidelines for contributing to the project
- [Code of Conduct](CODE_OF_CONDUCT.md): Community guidelines and expectations

## Specifications

- [Technical Specification](spec/technical-spec.md): Detailed technical requirements and constraints
- [API Specification](spec/api-spec.md): Interface definitions and data contracts

## Examples

- [Basic Example](examples/basic-usage.md): Simple usage demonstration
- [Advanced Example](examples/advanced-usage.md): Complex implementation patterns

## Configuration

- [Setup Guide](docs/setup.md): Installation and configuration instructions
- [Deployment Guide](docs/deployment.md): Production deployment guidelines

## Optional

- [Architecture Documentation](docs/architecture.md): Detailed system architecture
- [Design Decisions](docs/decisions.md): Historical design decision records
```

Report completion with:

```markdown
## llms.txt Creation Result

### Created File
- `llms.txt`

### Sections
- Documentation
- Specifications
- Examples
- Configuration
- Optional

### Validation
- Specification checked: https://llmstxt.org/
- Link validation: passed
- Human and machine readability: passed
```

## Definition of Done

- [ ] `llms.txt` exists at the repository root.
- [ ] The file follows https://llmstxt.org/ with one H1 `repository/project` name, an optional blockquote summary, optional additional context paragraphs without headings, and H2 file-list sections.
- [ ] The project name and summary accurately reflect repository evidence.
- [ ] Essential files are grouped logically and prioritized for LLM understanding.
- [ ] Every link follows `[descriptive-name](relative-url): optional description` and resolves from the repository root.
- [ ] Optional secondary content appears under `Optional` when it can be skipped for shorter context.
- [ ] The file serves both human and machine readers effectively.

## Prompt Body

Follow these steps in order.

**Step 1 — Review the specification.** Read the official llms.txt specification at https://llmstxt.org/. Confirm the required H1 header, recommended blockquote summary, optional additional details without headings, and H2 sections containing Markdown lists of links.

**Step 2 — Analyze the repository.** Examine the complete repository structure. Read the main `README.md` if present. Identify the primary purpose, scope, important directories, documentation directories, specification files, examples, and configuration files.

**Step 3 — Discover content.** Find README files, documentation files, `.md` files in `/docs/`, `/spec/`, and similar locations, technical specifications, API specifications, setup guides, deployment guides, example files, code samples, and relevant configuration files.

**Step 4 — Plan the content.** Write a concise purpose statement for the blockquote. Build a priority-ordered list of essential files and secondary files. Group files into logical categories such as Documentation, Specifications, Examples, Configuration, and Optional.

**Step 5 — Apply selection criteria.** Include files that explain purpose and scope, provide technical documentation, show usage patterns, define interfaces and specifications, or contain setup and configuration instructions. Exclude purely implementation details, redundant files, build artifacts, generated content, and files irrelevant to understanding the project.

**Step 6 — Create the file.** Write `llms.txt` at the repository root. Use clear link names, valid relative URLs, concise descriptions, consistent formatting, and a logical flow from general to specific.

**Step 7 — Validate.** Verify compliance with https://llmstxt.org/, check that all links are valid and accessible, confirm that the file is human-readable and machine-readable, and ensure it enables LLMs to quickly understand the repository.

**Step 8 — Report.** Summarize the created file, sections, important inclusions, intentional exclusions, and validation evidence.

## Invocation Example

```
/create-llms target=llms.txt
```
