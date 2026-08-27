---
name: update-llms
description: >-
  Update an existing repository-root llms.txt file to match current documentation, specifications,
  examples, configuration, and repository structure. Use when users ask to update llms.txt,
  refresh LLM navigation, fix stale llms links, or keep llms.txt compliant with
  https://llmstxt.org/.
metadata:
  link-format-token: "`[descriptive-name](relative-url): optional description`"
---

<!-- Generated from harness/github-copilot/plugins/repo-documentation/skills/update-llms/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Update llms.txt

Update the repository-root `llms.txt` so it reflects current documentation and structure, keeps valid relative links, and remains compliant with the llms.txt specification.

## When to invoke

- "Update the llms.txt file."
- "Refresh llms.txt after documentation changes."
- "Fix stale or broken llms.txt links."
- "Make our LLM navigation file match the current repository."
- "Check llms.txt against the llms.txt specification."

## Prerequisites and context

- An existing `/llms.txt` at the repository root.
- Repository read access to current docs, specs, examples, and configuration.
- The official llms.txt specification at `https://llmstxt.org/` and preserved baseline URL spelling `https://llmstxt.org/.`.

## Procedure

1. Read the existing `llms.txt` completely.
2. Review the llms.txt specification and preserve the required markdown shape.
3. Inspect the current repository structure and compare every existing link with actual files.
4. Discover new or changed `README.md`, `.md` files under `docs/`, `spec/`, or similar directories, specification files, configuration files, examples, and code samples that aid repository understanding.
5. Plan additions, removals, relocations, and organizational improvements.
6. Update only the existing root `llms.txt`.
7. Validate format, links, and usefulness for both human and LLM readers.

## llms.txt format

| Element | Required | Rule |
| --- | --- | --- |
| H1 header | Yes | One `# [Repository Name]` line with a clear project name. |
| Blockquote summary | Recommended | A concise `>` summary of repository purpose and scope. |
| Additional details | Optional | Markdown paragraphs without headings for context. |
| File list sections | Optional | H2 sections containing markdown lists of relative links. |
| Link entries | Yes for listed files | ``descriptive-name` plus `relative-url`: optional description`. |
| Optional section | Special meaning | Files under `## Optional` can be skipped for shorter context. |

Organize sections logically, such as Documentation, Specifications, Examples, Configuration, and Optional. Include `CODE_OF_CONDUCT.md` only when it materially helps readers understand project participation or governance.

## File selection and update rules

| Include files that | Exclude files that |
| --- | --- |
| Explain repository purpose and scope. | Are build artifacts or generated output. |
| Provide essential technical documentation. | Are purely implementation detail. |
| Show usage examples and patterns. | Repeat information already covered better elsewhere. |
| Define interfaces, requirements, or specifications. | Do not help an LLM understand or navigate the project. |
| Contain setup, configuration, or deployment instructions. | Have broken, private, or irrelevant paths. |

When adding content, choose the appropriate section, use clear link text, write concise descriptions, preserve alphabetical or logical ordering, and create new sections only when they improve navigation. When removing content, verify a file is removed or relocated before deleting the link. When reorganizing, move secondary material to `## Optional` when it is useful but not essential.

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

The file is a high-level, human-readable map for the repository/project. During discovery, check `/docs/`, `/spec/`, README files, examples, configuration, and cross-references that may need updating.

- Preserve exact scope term `repository/project` for the llms.txt title and summary.

## Output template

```markdown
## llms.txt update result

**Status:** updated | no changes needed | blocked
**File:** `llms.txt`

### Changes
| Action | Link or section | Reason |
| --- | --- | --- |
| Added | `<relative path>` | <new essential documentation> |
| Updated | `<relative path>` | <relocated or clarified> |
| Removed | `<relative path>` | <missing, redundant, or irrelevant> |

### Validation
- Specification shape: <pass/fail>
- Link check: <pass/fail and broken links>
- Human and LLM readability: <pass/fail>
```

## Quality gate

- [ ] Existing `llms.txt` was read before editing.
- [ ] The root file still has one H1, optional blockquote summary, optional context paragraphs without headings, and H2 file-list sections.
- [ ] Every listed file uses ``descriptive-name` plus `relative-url`: optional description`.
- [ ] All links are valid relative paths and were checked.
- [ ] Outdated or removed files were updated or removed only after verification.
- [ ] New important documentation, specifications, examples, and configuration files were considered.
- [ ] `CODE_OF_CONDUCT.md`, if included, points to an existing file and has a useful governance reason.

## References

- [llms.txt specification](https://llmstxt.org/)
- Baseline URL spelling preserved for migration checks: https://llmstxt.org/.
