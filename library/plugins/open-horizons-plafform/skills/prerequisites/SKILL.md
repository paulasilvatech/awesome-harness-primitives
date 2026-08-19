---
name: prerequisites
description: 'Use when validating local or CI prerequisites for Open Horizons deployments: CLI presence, versions, authentication, Azure/GitHub access, Docker, Node.js, and optional ArgoCD or kubelogin readiness. Produces a prerequisite checklist, missing-tool report, and installation guidance. DO NOT USE FOR: deployment orchestration (use deploy-orchestration), Terraform operations (use terraform-cli), Kubernetes operations (use kubectl-cli). Triggers include "validate prerequisites", "check my CLI tools", "am I ready to deploy", and "install missing tools".'
---

# Prerequisites

Use this skill to validate the operator workstation or CI runner before Open Horizons deployment. It produces a tool and authentication report using the repository scripts `scripts/validate-prerequisites.sh`, `.github/skills/prerequisites/scripts/validate-prerequisites.sh`, and `.github/skills/prerequisites/scripts/validate-cli-prerequisites.sh`.

> [!NOTE]
> This skill depends on shell access, Bash 4 or newer for the skill-local scripts, and installed or installable CLIs such as `az`, `terraform`, `kubectl`, `helm`, `gh`, `jq`, `yq`, `git`, and `curl`. It does not use an MCP server.

## When to invoke

- "Validate prerequisites before deployment."
- "Check whether this machine has the required CLIs."
- "Am I authenticated to Azure and GitHub?"
- "Show what tools are missing for Open Horizons."
- "Prepare a runner for platform validation."

## Prerequisites and context

- Shell execution is allowed.
- The repository root is the working directory.
- For authentication checks, the operator expects `az account show` and `gh auth status` to be meaningful.
- Installing missing tools requires explicit user approval and package-manager access.

## Procedure

### Step 1: Run the repository prerequisite validator

```bash
./scripts/validate-prerequisites.sh
```

### Step 2: Run skill-local validators when deeper CLI detail is needed

```bash
.github/skills/prerequisites/scripts/validate-prerequisites.sh
.github/skills/prerequisites/scripts/validate-cli-prerequisites.sh
```

### Step 3: Inspect required tool categories

| Category | Tools |
| --- | --- |
| Cloud and IaC | `az`, `terraform` |
| Kubernetes | `kubectl`, `helm`, `kubelogin`, `argocd` |
| GitHub | `gh`, `git` |
| Utilities | `jq`, `yq`, `curl` |
| Local runtime | `docker`, `node`, `npx` |

### Step 4: Classify readiness

| Severity | Meaning |
| --- | --- |
| Critical | Required tool missing or Azure/GitHub auth unavailable for requested deployment. |
| High | Required version is too old or cluster auth helper is missing. |
| Medium | Optional but recommended tool is missing. |
| Low | Cosmetic warning or version could not be parsed but tool runs. |

### Step 5: User confirmation gate for installation

```text
Missing tools: <tools>
Install command or package manager: <command>
Scope: local workstation or CI runner
Proceed with installing missing prerequisites? (y/n)
```

> [!IMPORTANT]
> Only install tools or modify the local environment after an explicit affirmative response. On a negative, ambiguous, or missing response, do not install anything; output the missing-tool report and stop.

### Step 6: Re-run validation after approved installation

```bash
./scripts/validate-prerequisites.sh
```

## Limits

- Do not use this skill for: deployment orchestration (use deploy-orchestration), Terraform operations (use terraform-cli), Kubernetes operations (use kubectl-cli).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Bash version is too old | Report that Bash 4 or newer is required for skill-local scripts. |
| `az` is not authenticated | Ask the operator to run `az login` and select the correct subscription. |
| `gh` is not authenticated | Ask the operator to run `gh auth login`. |
| Package manager is unavailable | Provide manual install links or commands without executing them. |
| Script exits non-zero | Preserve the failed section and list exact missing tools. |

## Output template

Return exactly this structure:

```markdown
## Prerequisites Report

**Environment:** <local|CI>
**Overall readiness:** <Ready|Blocked|Partial>

### Tool Status
| Tool | Status | Version | Required action |
| --- | --- | --- | --- |
| <tool> | <present|missing|auth-needed> | <version> | <action> |

### Findings
- <finding>

### Next Steps
1. <step>
```

## Quality gate

- [ ] Ran `./scripts/validate-prerequisites.sh` or explained why it could not run.
- [ ] Verified the skill-local script paths exist before referencing them.
- [ ] Reported missing tools and authentication gaps separately.
- [ ] Did not install anything without explicit approval.
- [ ] Re-ran validation after any approved installation.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
