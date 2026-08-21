---
name: 'update-llms'
description: 'Update the root llms.txt file to reflect current repository documentation, specifications, and structure.'
agent: 'agent'
tools: ['read', 'search', 'edit', 'web']
argument-hint: 'target=llms.txt'
---

# /update-llms

## Objective

Update the existing root `llms.txt` file so it accurately reflects current repository documentation, specifications, examples, configuration, and structure while remaining compliant with the official llms.txt specification at https://llmstxt.org/ and useful to both LLMs and humans.

## When to Invoke

Use this prompt after documentation, specifications, examples, configuration, or repository structure changes, or when existing `llms.txt` links, descriptions, or sections may be outdated.

## Preconditions

- A root `/llms.txt` file already exists.
- Repository files can be inspected to verify links and current structure.
- The official specification at https://llmstxt.org/ can be reviewed or is already known.
- Editing the root `llms.txt` file is allowed.

## Inputs the Team Must Provide

- `target` — normally `llms.txt` at repository root.
- Any known documentation, specification, or structure changes that prompted the update.
- The intended repository/project name and summary if the current values are wrong.
- Ask the user for anything that is missing when it affects the project purpose or file-selection criteria.

## What I Will Do

- Read the current `llms.txt` and compare its references with the actual repository.
- Review https://llmstxt.org/ and preserve the required H1, optional blockquote summary, additional context paragraphs, and H2 file-list sections.
- Discover new README files, Markdown docs in `/docs/`, `/spec/`, and equivalent locations, specification files, configuration files, examples, and code samples.
- Add, remove, rename, or reorganize links to keep the file accurate and concise.
- Validate all relative links and keep descriptions clear, unambiguous, and useful for LLM navigation.

## What I Will NOT Do

- Create a new `llms.txt` from scratch when the task is to update an existing one unless the existing file is absent and the user approves creation.
- Include build artifacts, generated content, redundant files, or implementation-only files that do not help understand the project.
- Leave broken links, stale moved-file paths, or empty sections.
- Violate the llms.txt markdown structure by adding unsupported heading levels for file-list organization.
- Overwrite repository purpose or summary with guesses when the evidence is unclear.

## Output Format

Apply the update to `llms.txt` and report using this structure:

```markdown
## llms.txt Update Result

### Updated File
- `llms.txt`

### Format
- H1 project name: present
- Blockquote summary: present
- Additional details: [present/absent]
- H2 file-list sections: [count]

### Changes Made
| Change | Reason |
| --- | --- |
| Added `[Main README](README.md)` | Essential project entry point |
| Removed `[Old Guide](docs/old.md)` | File no longer exists |

### Validation
- Specification checked: https://llmstxt.org/
- Link validation: passed
- Human and machine readability: passed
```

The updated `llms.txt` must retain this specification shape:

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

## Definition of Done

- [ ] `llms.txt` accurately reflects current repository structure and content.
- [ ] The file follows https://llmstxt.org/ with one H1, an optional blockquote summary, optional additional details without headings, and H2 file-list sections.
- [ ] Every file link follows `[descriptive-name](relative-url): optional description`.
- [ ] Key files are logically organized under sections such as Documentation, Specifications, Examples, Configuration, and Optional.
- [ ] Removed, relocated, broken, redundant, generated, or irrelevant references are corrected or removed.
- [ ] Language is concise, clear, unambiguous, human-readable, and LLM-readable.
- [ ] All links are valid relative paths from the repository root.

## Prompt Body

Follow these steps in order.

**Step 1 — Review the current file and specification.** Read the existing `llms.txt` file thoroughly. Review https://llmstxt.org/ and confirm continued compliance with the exact format: H1 header, optional blockquote summary, zero or more additional details without headings, and zero or more H2 sections containing Markdown lists of links.

**Step 2 — Analyze repository structure.** Examine the current repository structure completely. Compare current directories and files with what the existing `llms.txt` documents. Identify new directories, moved files, removed files, renamed files, and documentation that should be included.

**Step 3 — Discover content changes.** Identify README files, `.md` files in `/docs/`, `/spec/`, and similar documentation folders, specification files, configuration files, examples, code samples, and any changed documentation structure. Include files that explain purpose, scope, technical documentation, usage patterns, interfaces, specifications, setup, and configuration.

**Step 4 — Create an update plan.** List additions, removals, link updates, summary updates, and organizational improvements needed to maintain accuracy. Use logical ordering within sections and create new H2 sections only when they improve LLM navigation.

**Step 5 — Apply file-selection criteria.** Include files that explain the repository's purpose and scope, provide essential technical documentation, show usage examples and patterns, define interfaces and specifications, or contain configuration and setup instructions. Exclude purely implementation details, redundant files, build artifacts, generated content, and files irrelevant to understanding the project.

**Step 6 — Update `llms.txt`.** Preserve or correct the H1 project name, summary blockquote, optional context paragraphs, H2 file-list sections, Markdown link format, clear descriptions, and the special `Optional` section for secondary files that can be skipped for shorter context.

**Step 7 — Validate links and readability.** Check every relative link. Confirm no broken or invalid links remain, formatting is consistent, descriptions are specific, and the result serves as an effective LLM navigation tool.

**Step 8 — Report the change.** Summarize additions, removals, updates, and validation. State any files intentionally excluded and why.

## Invocation Example

```
/update-llms target=llms.txt
```
