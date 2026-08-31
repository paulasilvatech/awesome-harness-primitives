---
name: "create-llms"
description: >-
  Create a new repository-root llms.txt file from repository structure and documentation according to the llms.txt specification. Use when users ask to create llms.txt, generate LLM navigation, document repository structure for LLMs, or add an llms.txt compliant with https://llmstxt.org/.
---

# Create llms.txt

Create a new repository-root `llms.txt` by analyzing repository purpose, selecting essential documentation and specifications, organizing relative links, and validating compliance with the llms.txt specification.

## When to invoke

- "Create an llms.txt file for this repository."
- "Generate LLM navigation from the repository structure."
- "Add an llms.txt compliant with the llms.txt specification."
- "Help LLMs understand this project from key docs and specs."
- "Create a concise map of docs, examples, and configuration."

## Prerequisites and context

- No root `/llms.txt` exists, or the user explicitly wants it recreated from scratch.
- Repository structure is available for analysis.
- Use the official llms.txt specification at `https://llmstxt.org/` and preserve baseline URL spelling `https://llmstxt.org/.` for migration checks.

## Procedure

1. Review the llms.txt specification and required markdown structure.
2. Examine the complete repository structure.
3. Read the main `README.md` when present to infer purpose and scope.
4. Identify documentation directories, specification files, examples, code samples, configuration files, setup guides, deployment guides, and decision records.
5. Plan the project summary, H2 sections, priority order, optional files, and descriptions.
6. Create `/llms.txt` in the repository root.
7. Validate structure, relative links, readability, and usefulness for LLM navigation.

## llms.txt format

| Element | Required | Rule |
| --- | --- | --- |
| H1 header | Yes | Single `# [Repository Name]` line. |
| Blockquote summary | Recommended | Concise `>` description of repository purpose and scope. |
| Additional details | Optional | Context paragraphs without headings. |
| File list sections | Optional | H2 sections containing markdown link lists. |
| Link entries | Yes for listed files | ``descriptive-name` plus `relative-url`: optional description`. |
| Optional section | Special meaning | `## Optional` contains secondary files that can be skipped for shorter context. |

Use logical sections such as Documentation, Specifications, Examples, Configuration, and Optional. Include `CODE_OF_CONDUCT.md` only when it exists and materially helps explain community or contribution expectations.

## File selection rules

| Include files that | Exclude files that |
| --- | --- |
| Explain repository purpose and scope. | Are build artifacts or generated content. |
| Provide essential technical documentation. | Are purely implementation details. |
| Show usage examples and patterns. | Duplicate content better described elsewhere. |
| Define interfaces, specifications, requirements, or data contracts. | Do not help humans or LLMs understand the repository. |
| Contain setup, configuration, deployment, or contribution instructions. | Are broken, private, temporary, or irrelevant. |

Write concise, unambiguous descriptions for both human and LLM readers. Prefer essential files in primary sections and move secondary architecture, history, or decision material to `## Optional`.

## Example artifact

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

## Repository coverage vocabulary

The file is a high-level, human-readable entry point for the repository/project. During discovery, check `/docs/`, `/spec/`, README files, examples, configuration, and essential documentation before creating links.

- Preserve exact scope term `repository/project` for the llms.txt title and summary.

## Open Horizons integration

- Scope generated context to Open Horizons platform vocabulary, ownership, and the current Horizon stage.
- Preserve repository source precedence and exclude secrets, runtime state, and unsupported claims.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## llms.txt creation result

**Status:** created | blocked
**File:** `llms.txt`

### Sections created
| Section | Files included | Rationale |
| --- | --- | --- |
| Documentation | <count> | <why these are essential> |
| Specifications | <count> | <requirements or contracts covered> |
| Examples | <count> | <usage patterns covered> |
| Configuration | <count> | <setup/deployment covered> |
| Optional | <count> | <secondary context> |

### Validation
- Specification shape: <pass/fail>
- Link check: <pass/fail and broken links>
- Human and LLM readability: <pass/fail>
```

## Quality gate

- [ ] Repository structure and `README.md` were examined before writing.
- [ ] Root `llms.txt` has exactly one H1 project title.
- [ ] Summary blockquote is concise and accurate when present.
- [ ] File-list sections use H2 headings and markdown list links.
- [ ] Every link uses a valid relative path and a useful description.
- [ ] Essential documentation, specifications, examples, configuration, and setup files were considered.
- [ ] `CODE_OF_CONDUCT.md`, if included, exists and has a governance purpose.
- [ ] Build artifacts, generated output, and irrelevant implementation details are excluded.

## References

- [llms.txt specification](https://llmstxt.org/)
- Baseline URL spelling preserved for migration checks: https://llmstxt.org/.
