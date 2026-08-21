---
name: "suggest-awesome-github-copilot-instructions"
description: >-
  Suggest relevant GitHub Copilot instruction files from the awesome-copilot repository by comparing repository context, chat needs, local .github/instructions files, and remote versions. Use this skill when the user asks what Copilot instructions to add, whether local instructions are outdated, or how to install/update awesome-copilot instructions without duplicates.
---

# Suggest awesome GitHub Copilot instructions

Compare the current repository's language, framework, workflow, and existing `.github/instructions/` coverage against the GitHub awesome-copilot instruction catalog, then return a table of relevant missing or outdated instruction files and wait for an explicit install or update request before changing files.

## When to invoke

- "Suggest Copilot instructions for this repo."
- "Which awesome-copilot instructions should we add?"
- "Check whether our `.github/instructions` files are outdated."
- "Compare local instructions with awesome-copilot."
- "Install or update selected GitHub Copilot instructions."

## Prerequisites and context

- Read local instruction files from `.github/instructions/` and repository-wide instructions from `.github/copilot-instructions.md` when present.
- Fetch the catalog from <https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md>.
- Fetch remote instruction versions with raw URLs: `https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/{filename}`.
- When updating a requested instruction, replace the entire local file with the remote version and do not adjust content. Legacy source language may say use `#fetch`, `#runInTerminal`, `#todos`, or `githubRepo`; in the CLI, map those to available fetch, execute, tracking, and repository mechanisms rather than copying unsupported tool names into frontmatter.

## Procedure

1. Fetch available instructions from the awesome-copilot README.instructions catalog.
2. Discover local `*.instructions.md` files in `.github/instructions/` and, when relevant, community `instructions/` files.
3. Read YAML front matter from local files to extract `description` and `applyTo` patterns.
4. For each local file that corresponds to an awesome-copilot file, fetch the raw remote version using `https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/{filename}`.
5. Compare entire file content, including front matter and body, to classify up-to-date, outdated, missing, or similar-but-not-identical coverage.
6. Analyze repository context: languages, frameworks, project type, testing, CI/CD, deployment, recent chat needs, and development workflow requirements.
7. Match relevant remote instructions against gaps and avoid duplicates.
8. Present only the structured suggestion table and analysis.
9. AWAIT the user's explicit request before installing or updating specific instructions; DO NOT INSTALL OR UPDATE UNLESS DIRECTED TO DO SO.
10. If the user requests installation or update, download the selected remote files into `.github/instructions/` and preserve remote content byte-for-byte.

## Local inventory rules

| Source | What to collect |
| --- | --- |
| `.github/instructions/NAME.instructions.md` | File name, `description`, `applyTo`, body hash or exact content, and covered technologies. |
| `.github/copilot-instructions.md` | Repository-wide conventions that may make a remote instruction redundant. |
| `instructions/NAME.instructions.md` | Community/distribution instructions already present. |
| Repository files | Language extensions `.cs`, `.js`, `.py`, `.ts`; framework indicators such as ASP.NET, React, Azure, Next.js; test and CI files. |
| Chat history context | Recent pain points, technology-specific questions, coding standards, and workflow requests. |

## Version comparison rules

| Classification | Condition | Recommendation |
| --- | --- | --- |
| Already installed and up-to-date | Local and remote content are exact matches. | Do not suggest installation. |
| Installed but outdated | Same file exists locally but content differs. | Show key differences and recommend update when useful. |
| Not installed in repo | Remote file is relevant and no equivalent local coverage exists. | Suggest install with rationale. |
| Similar local instruction | Different local file covers the same technology or practice. | Explain overlap and avoid duplicate install unless remote adds distinct value. |

Document specific differences for outdated files:

- Front matter changes: `description`, `applyTo` patterns.
- Content updates: guidelines, examples, best practices.
- Similarity and whether the update would add value.

## Relevance criteria

| Criterion | Evidence |
| --- | --- |
| Language match | Repository contains matching file extensions or package manifests. |
| Framework match | Indicators such as ASP.NET, React, Azure, Next.js, or related dependencies. |
| Project type | Web app, API, library, tool, data project, infrastructure repository, or documentation repository. |
| Development workflow | Testing, CI/CD, deployment, security, accessibility, or review needs. |
| Existing coverage | Local instruction files already cover or partially cover the topic. |
| User intent | Recent or current user asks for standards, process, or instruction recommendations. |

## Output table requirements

Include links to both awesome-copilot instructions and similar local instructions when available. Example rows:

| Awesome-Copilot Instruction | Description | Already Installed | Similar Local Instruction | Suggestion Rationale |
| --- | --- | --- | --- | --- |
| [blazor.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/blazor.instructions.md) | Blazor development guidelines | Yes | `blazor.instructions.md` | Already covered by existing Blazor instructions. |
| [pcf-react-platform-libraries.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/pcf-react-platform-libraries.instructions.md) | ReactJS development standards | No | None | Would enhance React development with established patterns. |
| [java-junit5-assertions.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/java-junit5-assertions.instructions.md) | Java development best practices | Outdated | `java-junit5-assertions.instructions.md` | `applyTo` pattern differs: remote uses `'**/*.java'` vs local `'*.java'`; update recommended. |

## Installation and update rules

- Do not install or update unless the user explicitly requests specific files.
- Download/Update assets only after approval: download new instructions to `.github/instructions/`.
- Update outdated instructions by replacing the entire local file with the latest remote version.
- Do not adjust content of downloaded files.
- Preserve file location in `.github/instructions/`.
- Avoid suggesting duplicates when existing instructions already cover the project-specific need or an existing copilot-instruction already applies. Use `curl` only when the normal fetch path truncates content.

## Gotchas

- **Do not rely on labels alone**: a local instruction can cover a remote topic under a different file name.
- **Do not edit remote content after download**: requested updates must be byte-for-byte from awesome-copilot.
- **Do not over-recommend**: only suggest instructions that align with repository technology and workflow.
- **Do not provide extra narrative beyond the table and analysis** when the user asked for process-style output.

## Output template

```markdown
## Awesome Copilot instruction suggestions

| Awesome-Copilot Instruction | Description | Already Installed | Similar Local Instruction | Suggestion Rationale |
| --- | --- | --- | --- | --- |
| `<file>.instructions.md` | <description> | Yes | Outdated | No | `<local file or None>` | <why this is relevant, duplicate, or update-worthy; include the awesome-copilot blob URL in text if needed> |

### Outdated instruction differences
| Local file | Remote file | Key differences | Recommendation |
| --- | --- | --- | --- |
| `.github/instructions/<file>.instructions.md` | `https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/{filename}` | <description/applyTo/content differences> | update | keep |

### Awaiting user action
No files were installed or updated. Say which instruction files to install or update.
```

## Quality gate

- [ ] The awesome-copilot catalog at <https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md> was checked.
- [ ] Local `.github/instructions/` files were inventoried, including `description` and `applyTo`.
- [ ] Remote raw versions were fetched for comparable local files using `https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/{filename}`.
- [ ] Suggestions are grounded in repository language, framework, project type, workflow, and chat context.
- [ ] Existing local coverage and similar local instructions were considered to avoid duplicates.
- [ ] Outdated instructions list specific front matter or content differences.
- [ ] No installation or update occurred unless explicitly requested by the user.

## References

- [Awesome Copilot instructions catalog](https://github.com/github/awesome-copilot/blob/main/docs/README.instructions.md)
- [Blazor instruction example](https://github.com/github/awesome-copilot/blob/main/instructions/blazor.instructions.md)
- [PCF React platform libraries instruction example](https://github.com/github/awesome-copilot/blob/main/instructions/pcf-react-platform-libraries.instructions.md)
- [Java JUnit 5 assertions instruction example](https://github.com/github/awesome-copilot/blob/main/instructions/java-junit5-assertions.instructions.md)
- [Raw instruction URL pattern](https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/{filename})
