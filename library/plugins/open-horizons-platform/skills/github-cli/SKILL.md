---
name: github-cli
description: "Use when running focused GitHub CLI operations for Open Horizons repositories, pull requests, issues, workflows, releases, GitHub Apps, and API calls; produces commands, URLs, status, and next steps. DO NOT USE FOR: Azure DevOps integration (use ado-integration), Terraform operations (use terraform-cli), or Kubernetes operations (use kubectl-cli). Triggers include \"create a GitHub issue\", \"check a workflow run\", \"open a pull request\"."
---

# GitHub CLI

This workflow performs focused GitHub operations through `gh`, including repository inspection, PRs, issues, workflows, and GitHub App setup. It produces a command log, created artifact URLs, and recommended next steps while requiring confirmation before changing repository state.

> [!NOTE]
> This skill shells out to the GitHub CLI (`gh`) and may use bundled `scripts/setup-github-app.sh` for GitHub App setup. Resolve bundled paths relative to this `SKILL.md`, authenticate with the intended account or GitHub App token, and verify repository context before mutating operations.

## When to invoke
- "Create a GitHub issue for this finding."
- "Open a pull request with these changes."
- "Check the latest workflow run and summarize failures."
- "Configure a GitHub App for Backstage technical integration."
- "List releases or tags for this repository."

## Prerequisites and context
- `gh auth status` succeeds for the intended host and account.
- Repository context is set with `gh repo view` or `gh repo set-default`.
- Required repository permissions are available.
- For Enterprise Managed Users, user sign-in may use Entra while GitHub App or token credentials remain required for technical portal integration.
- Explicit approval is available before creating issues, PRs, repos, comments, workflow dispatches, merges, or app changes.

## Procedure

### Step 1: Verify auth and repository context
```bash
gh auth status
gh repo view
gh repo set-default <owner>/<repo>
```

- [ ] Host, owner, repository, and account are correct.
- [ ] Token scopes or app permissions match the operation.
- [ ] No secrets are printed.

### Step 2: Use read operations first
```bash
gh pr list --limit 20
gh issue list --limit 20
gh workflow list
gh run list --limit 10
gh release list --limit 20
```

For structured output:

```bash
gh pr view <number> --json title,state,author,url
```

### Step 3: Confirm before creating GitHub artifacts or mutating state
```text
GitHub operation summary:
- Repository:
- Operation: issue | PR | workflow dispatch | merge | repo create | app setup | comment
- Title or target:
- Files or resources affected:
Proceed with this GitHub mutation? (y/n)
```

> [!IMPORTANT]
> Only proceed with creating issues, PRs, comments, repositories, workflow runs, merges, or GitHub App changes if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the proposed command and stop.

### Step 4: Execute approved operations
```bash
gh issue create --title "<title>" --body "<body>"
gh pr create --title "<title>" --body "<body>"
gh workflow run <workflow-name>
gh run view <run-id>
gh run watch <run-id>
```

For GitHub App setup when explicitly requested:

```bash
scripts/setup-github-app.sh --target backstage --org <github-org>
```

### Step 5: Verify and report URLs
```bash
gh issue view <number> --web
gh pr view <number> --json url,state,statusCheckRollup
gh run view <run-id> --json url,conclusion,status
```

- [ ] Created artifact URL is captured.
- [ ] PR checks or workflow status are summarized.
- [ ] Follow-up owners and labels are documented when applicable.

## Risk classification
| Severity | Meaning |
|---|---|
| Critical | Wrong repository, secret exposed, unapproved merge, or destructive repo operation. |
| High | Workflow dispatch affects production, PR targets wrong base, or GitHub App permissions are too broad. |
| Medium | Missing labels, incomplete issue body, failed checks, or insufficient token scopes. |
| Low | Formatting, metadata, or notification gaps. |

## Limits

- Do not use this skill for: Azure DevOps integration (use ado-integration), Terraform operations (use terraform-cli), or Kubernetes operations (use kubectl-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Not authenticated | Run `gh auth login` or configure an approved token, then verify `gh auth status`. |
| Wrong repository | Stop, set the intended repository, and rerun read-only commands first. |
| Permission denied | Report missing permission or scope; do not request broader access than needed. |
| Workflow run fails | Capture run URL, failing job, and logs summary; route pipeline diagnosis if needed. |

## Output template

Return exactly this structure:
```markdown
# GitHub CLI Operation Report

## Context
- Host:
- Repository:
- Actor:

## Commands
| Command | Result |
|---|---|

## Artifacts
| Type | URL | Status |
|---|---|---|

## Next Steps
- 
```

## Quality gate
- [ ] Auth and repository context are verified before mutation.
- [ ] User confirmation is captured before creating or changing GitHub artifacts.
- [ ] URLs and statuses are reported for created or inspected artifacts.
- [ ] Secrets and tokens are never printed.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
