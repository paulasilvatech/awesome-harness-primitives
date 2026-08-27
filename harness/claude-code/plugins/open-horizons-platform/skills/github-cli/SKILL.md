---
name: github-cli
description: >-
  GitHub CLI operations use gh commands and GitHub API workflows for repositories, issues, pull
  requests, Actions, packages, repository discovery, GitHub App setup, and pull request
  automation. Use this skill when working with gh repo, gh pr, gh issue, gh workflow, gh run, gh
  api, Actions checks, or package operations.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/github-cli/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GitHub CLI

Use this skill to turn GitHub platform requests into ordered `gh` command workflows, preserve repository and enterprise identity context, and return pull request, issue, workflow, repository, API, or package evidence with URLs for created resources.

## When to invoke

- "Manage a pull request with GitHub CLI."
- "Create, list, or close GitHub issues."
- "Run or inspect a GitHub Actions workflow."
- "Clone, view, or create a GitHub repository."
- "Use gh api or GitHub App setup for repository automation."

## Prerequisites and context

- GitHub CLI installed and authenticated.
- Appropriate repository permissions.
- For GitHub Enterprise Managed Users, user accounts are governed by the enterprise IdP. Use GitHub App or token credentials for Backstage technical integration even when Backstage sign-in uses Microsoft Entra ID.

## Procedure

1. Confirm GitHub CLI authentication and the target repository before repository, issue, pull request, workflow, or API operations.
2. Choose the command group that matches the requested GitHub object.
3. Use `--json` for scripting and URLs for human follow-up where available.
4. Capture operation results and links for any created or modified resource.
5. Return the result using the output template.

### Authentication

```bash
# Check auth status
gh auth status

# Login
gh auth login
```

### Repository operations

```bash
# Clone repository
gh repo clone <owner/repo>

# View repository
gh repo view

# Create repository
gh repo create <name> --public --description "Description"
```

### Pull request operations

```bash
# Create PR
gh pr create --title "Title" --body "Description"

# List PRs
gh pr list

# View PR
gh pr view <number>

# Merge PR
gh pr merge <number> --merge
```

### Workflow operations

```bash
# List workflows
gh workflow list

# Run workflow
gh workflow run <workflow-name>

# View workflow run
gh run view <run-id>

# Watch workflow run
gh run watch <run-id>
```

### Issue operations

```bash
# Create issue
gh issue create --title "Title" --body "Description"

# List issues
gh issue list

# Close issue
gh issue close <number>
```

### Best practices

1. Use gh api for advanced operations.
2. Set default repository with gh repo set-default.
3. Use --json flag for scripting.
4. Authenticate with tokens for CI/CD.

## Output template

Return exactly this structure:

```markdown
**Status:** PASS | FAIL | BLOCKED
**Summary:** One sentence describing the repository, pull request, issue, workflow, API, or package outcome.

### Details
1. Command executed: `<gh command>`
2. Repository context: `<owner/repo or default repository>`
3. Operation result: `<created, updated, listed, viewed, merged, triggered, watched, or failed>`
4. Resource URLs: `<PR, issue, run, repository, package, or none>`
5. Next steps: `<review, watch run, merge, close issue, or none>`

### Validation
- Authentication check: `<gh auth status evidence or reason not checked>`
- Command result: `<exit code or observed gh output>`
```

## Limits

- Do not use this skill for Azure DevOps integration.
- Use `open-horizons-engineer` (`agent`) instead when the task is implementing GitHub platform integration, GitHub Apps, org discovery, GHAS, Actions CI/CD, or Packages configuration.
- Do not use this skill for Terraform execution.
- Use `terraform-cli` (`skill`) instead when the task is Terraform init, plan, apply, validate, fmt, state, import, module development, provider locks, or tfvars.
- Do not use this skill for Kubernetes commands.
- Use `kubectl-cli` (`skill`) instead when the task is direct Kubernetes resource inspection, logs, events, or manifest application.
- Do not use this skill for pipeline failure analysis.
- Use `pipeline-diagnostics` (`skill`) instead when the task is diagnosing GitHub Actions job or step failures.

## Progressive disclosure and bundled resources

- `scripts/setup-github-app.sh`: use when the GitHub task requires GitHub App setup automation.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `open-horizons-deployment-operator` | `agent` | Coordinating approved GitHub operations as part of platform deployment. |
| `open-horizons-engineer` | `agent` | Configuring GitHub Apps, organization discovery, GHAS, Actions, or Packages. |
| `pipeline-diagnostics` | `skill` | Diagnosing workflow run failures and CI/CD errors. |
| `validation-scripts` | `skill` | Running repository validation scripts after GitHub operations. |
| `prerequisites` | `skill` | Checking whether `gh` and related tooling are installed and authenticated. |

## Quality gate

- [ ] `name` is `github-cli` and matches the parent directory.
- [ ] The target repository context is clear before running repository-scoped commands.
- [ ] The response includes URLs for created pull requests, issues, workflow runs, or repositories when available.
- [ ] `gh auth status` is checked or the reason for skipping it is stated.
- [ ] `--json` usage is reported when command output is intended for scripting.
- [ ] The bundled script path listed above exists before referring to it.
