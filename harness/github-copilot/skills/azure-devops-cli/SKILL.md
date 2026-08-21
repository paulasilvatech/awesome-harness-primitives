---
name: azure-devops-cli
description: >-
  Manage Azure DevOps with Azure CLI and the azure-devops extension. Use when the user asks for Azure DevOps CLI commands, az devops automation, projects, repos, pull requests, pipelines, builds, work items, artifacts, service endpoints, permissions, or CI/CD scripting.
---

# Azure DevOps CLI

Use the Azure CLI plus the Azure DevOps extension to automate projects, repos, pipelines, builds, pull requests, work items, artifacts, service endpoints, security, teams, users, wikis, variables, agents, and advanced REST calls.

## When to invoke

- "Use Azure DevOps CLI to create a pull request."
- "List pipeline runs with az pipelines."
- "Create or update an Azure Boards work item."
- "Automate Azure DevOps repos, builds, or artifacts."
- "Fix this az devops command or PAT login."

## Prerequisites and context

**CLI Version:** 2.81.0 (current as of 2025)

```bash
# Install Azure CLI on macOS
brew install azure-cli

# Install Azure CLI on Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Azure DevOps extension
az extension add --name azure-devops
```

Authenticate with a PAT only through standard CLI login; do not print or store the token in scripts.

```bash
az devops login --organization https://dev.azure.com/{org} --token YOUR_PAT_TOKEN
az devops configure --defaults organization=https://dev.azure.com/{org} project={project}
az devops configure --list
```

Replace legacy `https://{org}.visualstudio.com` URLs with `https://dev.azure.com/{org}`.

## Command map

```text
az devops          # Main DevOps commands
├── admin          # Administration (banner)
├── extension      # Extension management
├── project        # Team projects
├── security       # Security operations
│   ├── group      # Security groups
│   └── permission # Security permissions
├── service-endpoint # Service connections
├── team           # Teams
├── user           # Users
├── wiki           # Wikis
├── configure      # Set defaults
├── invoke         # Invoke REST API
├── login          # Authenticate
└── logout         # Clear credentials

az pipelines       # Azure Pipelines
├── agent          # Agents
├── build          # Builds
├── folder         # Pipeline folders
├── pool           # Agent pools
├── queue          # Agent queues
├── release        # Releases
├── runs           # Pipeline runs
├── variable       # Pipeline variables
└── variable-group # Variable groups

az boards          # Azure Boards
├── area           # Area paths
├── iteration      # Iterations
└── work-item      # Work items

az repos           # Azure Repos
├── import         # Git imports
├── policy         # Branch policies
├── pr             # Pull requests
└── ref            # Git references

az artifacts       # Azure Artifacts
└── universal      # Universal Packages
```

## Reference routing

Read the smallest reference that matches the user task.

| File | When to read | Covers |
| --- | --- | --- |
| `references/repos-and-prs.md` | Repos, branches, pull requests, branch policies | Repositories, Import, PRs create/list/vote/reviewers/policies, Git refs, Branch policies |
| `references/pipelines-and-builds.md` | Pipelines, builds, releases, artifacts | Pipelines CRUD, runs, builds, releases, artifacts download/upload |
| `references/boards-and-iterations.md` | Work items, sprints, area paths | Work items, WIQL, create/update/relations, Area paths, Iterations, Team iterations |
| `references/variables-and-agents.md` | Pipeline variables, variable groups, agent pools | Pipeline variables, Variable groups, Pipeline folders, Agent pools/queues |
| `references/org-and-security.md` | Projects, teams, users, permissions, wikis | Projects, Extensions, Teams, Users, Security groups/permissions, Service endpoints, Wikis, Admin |
| `references/advanced-usage.md` | Output formatting, JMESPath, aliases | Output formats, JMESPath queries, Global args, Common params, Git aliases |
| `references/workflows-and-patterns.md` | Automation scripts and repeatable workflows | Common workflows, Best practices, Error handling, Scripting patterns, Real-world examples |
| `references/long-comments-on-windows.md` | Long descriptions or discussions fail on Windows | `cmd.exe` 8191 char cap on `az.cmd`, shell detection, `azps.ps1`, native `--file-path`, `az devops invoke --in-file` |

## Procedure

1. Identify the target organization, project, resource type, and command group.
2. Configure defaults with `az devops configure --defaults` when repeated commands share organization and project.
3. Read the relevant reference file for exact command syntax.
4. Use `--output json` or `--query` for scripts; avoid parsing human table output.
5. For commands that create or mutate resources, preview inputs and use explicit names, IDs, and project context.
6. For unsupported CLI gaps, use `az devops invoke` with the documented REST route.
7. Report the command run, output summary, and any IDs or URLs created.

## Command selection patterns

| Goal | Command family | Notes |
| --- | --- | --- |
| Create/list projects | `az devops project` | Use org defaults or pass organization explicitly. |
| Create PRs and policies | `az repos pr`, `az repos policy` | Prefer branch names and repository IDs from CLI output. |
| Queue or inspect builds | `az pipelines build`, `az pipelines runs` | Use JSON output for automation. |
| Manage releases | `az pipelines release` | Confirm project and definition before mutation. |
| Work with boards | `az boards work-item`, `az boards area`, `az boards iteration` | Use WIQL for complex queries. |
| Manage artifacts | `az artifacts universal` | Confirm feed, package, version, and path. |
| Manage service connections | `az devops service-endpoint` | Treat credentials as secrets; do not echo them. |
| Security and permissions | `az devops security group`, `az devops security permission` | Use descriptors and namespace IDs carefully. |

## Gotchas

- **Do not expose `YOUR_PAT_TOKEN`**: pass tokens through secure input or environment-controlled login, never commit them.
- **Configure defaults carefully**: stale defaults can mutate the wrong organization or project.
- **Prefer `https://dev.azure.com/{org}`**: legacy `https://{org}.visualstudio.com` URLs should be replaced.
- **Windows long comments fail through `az.cmd`**: read `references/long-comments-on-windows.md` before sending long `--discussion`, `--description`, or `--content` values.
- **JMESPath is not shell-neutral**: quote `--query` expressions differently for Bash, PowerShell, and cmd.exe when needed.

## Progressive disclosure and bundled resources

This skill is a router over reference files. Read only the reference matching the task so command details stay precise without loading every Azure DevOps domain.

- `references/repos-and-prs.md`
- `references/pipelines-and-builds.md`
- `references/boards-and-iterations.md`
- `references/variables-and-agents.md`
- `references/org-and-security.md`
- `references/advanced-usage.md`
- `references/workflows-and-patterns.md`
- `references/long-comments-on-windows.md`

## CLI shorthand

Defaults avoid repeating `--org/--project`. Boards references include `WIQL/create/update/relations` patterns.

## Output template

```markdown
## Azure DevOps CLI result

**Status:** complete | blocked | failed
**Organization:** `https://dev.azure.com/{org}`
**Project:** `<project>`
**Command group:** `az <group>`

### Commands
- `<command run or recommended>`

### Results
| Resource | ID/Name | URL/State |
| --- | --- | --- |
| <resource> | <id or name> | <url or state> |

### Validation
- Authentication/config checked: pass | fail
- Reference file used: `<references/file.md>`
- Output captured as JSON or explicit IDs: pass | fail
```

## Quality gate

- [ ] Azure CLI and `azure-devops` extension prerequisites are satisfied or installation commands are provided.
- [ ] Organization uses `https://dev.azure.com/{org}` and the project context is explicit.
- [ ] `YOUR_PAT_TOKEN` or any real PAT is never printed, committed, or embedded in scripts.
- [ ] The relevant bundled reference file was used for exact syntax.
- [ ] Mutating commands identify the target resource by explicit project, repository, pipeline, work item, or descriptor.
- [ ] Scripted output uses JSON, IDs, or `--query` instead of fragile table parsing.
- [ ] Windows long-comment workarounds are used when command length may exceed the `cmd.exe` limit.

## References

- [Azure CLI Linux install](https://aka.ms/InstallAzureCLIDeb)
