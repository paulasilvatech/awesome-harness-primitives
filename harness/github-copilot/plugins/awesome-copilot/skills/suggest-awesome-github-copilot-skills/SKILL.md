---
name: "suggest-awesome-github-copilot-skills"
description: >-
  Suggest relevant GitHub Copilot Agent Skills from the awesome-copilot repository by comparing remote skills with local repository skills, detecting missing or outdated skills, bundled assets, duplicates, and repository-fit gaps. Use when the user asks which awesome-copilot skills to install, update, compare, or recommend for the current repository.
---

# Suggest awesome GitHub Copilot skills

Analyze repository context and the GitHub awesome-copilot skill catalog, then recommend missing or outdated self-contained Agent Skills without installing or updating anything unless the user explicitly asks.

## When to invoke

- "Suggest awesome-copilot skills for this repo."
- "Which GitHub Copilot skills should we install?"
- "Compare our skills with awesome-copilot."
- "Find outdated local skills from awesome-copilot."
- "Recommend Agent Skills for this project."

## Prerequisites and context

- Remote catalog: https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md.
- Remote skill folders live under https://github.com/github/awesome-copilot/tree/main/skills.
- Use `web_fetch` for README and raw `SKILL.md` files. Use `execute/bash` with `curl` only when a bundled asset cannot be retrieved completely through `web_fetch`.
- Scan local skills from `.github/skills/` first; if that folder does not exist, report that no local project skills were found.
- Do not install, update, replace, or delete skills until the user asks for a specific install or update.
- Legacy references to `#fetch`, `#runInTerminal`, `#todos`, `fetch`, and `githubRepo` mean the current CLI equivalents are `web_fetch`, `execute/bash`, session tracking, and raw GitHub URLs.

## Procedure

1. Fetch the available skill list and descriptions from https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md.
2. List all folders in `.github/skills/`.
3. For each local folder, read `SKILL.md` front matter and extract `name` and `description`.
4. List bundled assets in each local skill folder.
5. For each local skill that appears in awesome-copilot, fetch the remote raw file at `https://raw.githubusercontent.com/github/awesome-copilot/main/skills/{skill-name}/SKILL.md`.
6. Compare entire local and remote `SKILL.md` content, including front matter and body.
7. Identify exact matches, outdated skills, front matter changes, instruction changes, and bundled asset changes.
8. Review chat history, repository files, languages, frameworks, cloud providers, infrastructure, testing, CI/CD, deployment, and specialized workflow needs.
9. Compare available remote skills with local skills to avoid duplicates and find coverage gaps.
10. Present a structured table with suggestions, descriptions, bundled assets, install status, similar local skills, rationale, and links.
11. AWAIT user request before installation or update: DO NOT INSTALL OR UPDATE UNLESS DIRECTED to proceed.
12. Download/Update assets only after direction: download the full remote skill folder into `.github/skills/`, preserve folder structure, include `SKILL.md` and bundled assets, and do not adjust content.

## Context analysis criteria

| Area | Inspect for |
| --- | --- |
| Repository patterns | Programming languages such as `.cs`, `.js`, `.py`, `.ts`; frameworks such as ASP.NET, React, Azure, and Next.js; project types such as web apps, APIs, libraries, tools, and infrastructure. |
| Development workflow | Testing, CI/CD, deployment, package managers, and validation commands. |
| Infrastructure and cloud | Azure, AWS, GCP, Terraform, Bicep, Kubernetes, and workflow automation. |
| Chat history context | Recent discussions, pain points, feature requests, code review patterns, and specialized task needs. |
| Local skills | Existing capabilities, duplicate coverage, similar names, descriptions, and bundled assets. |

## Version comparison rules

| Status | Definition |
| --- | --- |
| Already installed and up-to-date | Local `SKILL.md` exactly matches the remote awesome-copilot `SKILL.md`. |
| Installed but outdated | Local skill exists and remote content differs. |
| Not installed in repo | Remote skill is relevant and no matching local skill exists. |

For outdated skills, document front matter changes, instruction updates, and bundled asset changes. Calculate similarity qualitatively enough to explain whether an update is recommended.

Example remote raw URL pattern:

```text
https://raw.githubusercontent.com/github/awesome-copilot/main/skills/{skill-name}/SKILL.md
```

Example skill links to preserve in output:

- https://github.com/github/awesome-copilot/tree/main/skills/gh-attach
- https://github.com/github/awesome-copilot/tree/main/skills/aspire
- https://github.com/github/awesome-copilot/tree/main/skills/terraform-azurerm-set-diff-analyzer

## Skill structure checks

Each Agent Skill is a folder containing `SKILL.md` with YAML front matter and optional bundled assets. Folder names are lowercase with hyphens, for example `azure-deployment-preflight`. The `name` field must match the folder name. awesome-copilot front matter commonly uses:

```markdown
---
name: 'skill-name'
description: 'Brief description of what this skill provides and when to use it'
---
```

## Limits

- Do not provide commentary beyond the table and analysis requested.
- Do not install or update unless directed.
- Do not adjust remote skill contents during install or update.
- Do not suggest duplicates already covered by equal or stronger local skills.
- Do not rely on relative links between primitives; use remote GitHub URLs for awesome-copilot links.

## Output template

```markdown
## Awesome Copilot skill suggestions

| Awesome-Copilot Skill | Description | Bundled Assets | Already Installed | Similar Local Skill | Suggestion Rationale |
| --- | --- | --- | --- | --- | --- |
| [gh-attach](https://github.com/github/awesome-copilot/tree/main/skills/gh-attach) | GitHub CLI skill for managing repositories and workflows | None | No | None | Would enhance GitHub workflow automation capabilities |
| [aspire](https://github.com/github/awesome-copilot/tree/main/skills/aspire) | Aspire skill for distributed application development | 9 reference files | Yes | aspire | Already covered by existing Aspire skill |
| [terraform-azurerm-set-diff-analyzer](https://github.com/github/awesome-copilot/tree/main/skills/terraform-azurerm-set-diff-analyzer) | Analyze Terraform AzureRM provider changes | Reference files | Outdated | terraform-azurerm-set-diff-analyzer | Instructions updated with new validation patterns; update recommended |

### Analysis
- Local skills scanned: <count or folder missing>
- Remote skills considered: <count>
- Recommended installs: <count>
- Recommended updates: <count>
```

## Quality gate

- [ ] The awesome-copilot README skills catalog was fetched from https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md.
- [ ] Local `.github/skills/` folders and front matter were scanned or reported absent.
- [ ] Remote raw `SKILL.md` files were fetched for local skills that appear in the catalog.
- [ ] Each recommendation explains relevance to repository context and avoids duplicates.
- [ ] Outdated skills include specific differences or update rationale.
- [ ] No install, update, delete, or content adjustment occurred without a user request.
- [ ] The output uses the table format exactly and includes remote skill links.

## References

- [awesome-copilot skills README](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md)
- [awesome-copilot skills folder](https://github.com/github/awesome-copilot/tree/main/skills)
- [gh-attach skill](https://github.com/github/awesome-copilot/tree/main/skills/gh-attach)
- [aspire skill](https://github.com/github/awesome-copilot/tree/main/skills/aspire)
- [terraform-azurerm-set-diff-analyzer skill](https://github.com/github/awesome-copilot/tree/main/skills/terraform-azurerm-set-diff-analyzer)
