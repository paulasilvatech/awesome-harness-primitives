---
name: codespaces-golden-paths
description: "Use when configuring GitHub Codespaces devcontainer environments for Open Horizons Golden Path templates; produces devcontainer recommendations, template mapping, validation checks, and README badge guidance. DO NOT USE FOR: Backstage deployment (use backstage-deployment), CI/CD pipeline orchestration (use deploy-orchestration), or creating Backstage templates from scratch (use backstage-deployment). Triggers include \"add Codespaces to a Golden Path\", \"create a devcontainer for this template\", \"validate Codespaces setup\"."
---

# Codespaces Golden Paths

This workflow configures Codespaces-ready developer environments for Open Horizons Golden Path templates. It produces a template-to-devcontainer mapping, a `.devcontainer/devcontainer.json` design, validation checks, and README badge guidance.

> [!NOTE]
> This skill relies on GitHub Codespaces, devcontainers, and repository Golden Path templates under `golden-paths/`. Use `gh` for GitHub checks when needed, and do not modify scaffolded template files until the user confirms the target template.

## When to invoke
- "Add Codespaces support to the API microservice Golden Path."
- "Create a devcontainer for the Foundry agent template."
- "Validate that this Golden Path opens with the right SDKs in Codespaces."
- "Add the Open in GitHub Codespaces badge to a scaffolded README."

## Prerequisites and context
- Target template path exists under `golden-paths/h1-foundation/`, `golden-paths/h2-enhancement/`, or `golden-paths/h3-innovation/`.
- The template has a skeleton directory where `.devcontainer/devcontainer.json` can be added or validated.
- Required runtime stack is known: Python, Node.js, Java, Terraform, AI/ML, or data pipeline.
- User approval is available before creating or updating template files.

## Procedure

### Step 1: Locate the target Golden Path
```bash
find golden-paths -maxdepth 3 -name template.yaml | sort
```

- [ ] Confirm the exact template directory.
- [ ] Identify the scaffold skeleton path.
- [ ] Confirm the language/runtime and expected ports.

### Step 2: Select the devcontainer profile
| Template type | Base image | Common tools |
|---|---|---|
| Python or FastAPI | `mcr.microsoft.com/devcontainers/python:3.11` | Python, Azure CLI, kubectl/Helm, GitHub CLI |
| Node.js or web | `mcr.microsoft.com/devcontainers/javascript-node:20` | Node.js, npm/yarn, Azure CLI, GitHub CLI |
| Terraform | `mcr.microsoft.com/devcontainers/base:ubuntu` | Terraform, Azure CLI, kubectl/Helm, GitHub CLI |
| Java or Spring Boot | `mcr.microsoft.com/devcontainers/java:21` | Java, Maven, Azure CLI, GitHub CLI |
| AI/ML | `mcr.microsoft.com/devcontainers/python:3.11` | Python, Azure AI SDKs, notebooks, GitHub CLI |

### Step 3: Confirm before modifying template artifacts
```text
Codespaces update summary:
- Template path:
- Runtime profile:
- Files to create or update:
- Forwarded ports:
Proceed with updating the Golden Path devcontainer files? (y/n)
```

> [!IMPORTANT]
> Only proceed with creating or updating `.devcontainer`, README, or template files if the user gives an explicit affirmative. On a negative, ambiguous, or missing response, output the recommended configuration and stop.

### Step 4: Create or validate `devcontainer.json`
A minimal Python/FastAPI profile should include the expected image, features, extensions, setup command, and forwarded ports:

```json
{
  "name": "Python Microservice",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [8000]
}
```

### Step 5: Add README badge guidance
```markdown
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/<owner>/<repo>?quickstart=1)
```

### Step 6: Validate the generated workspace
- [ ] JSON is valid.
- [ ] Feature names are current and pinned to intended major versions.
- [ ] `postCreateCommand` matches files that exist in the scaffold.
- [ ] Ports match the application runtime.
- [ ] Required VS Code extensions are relevant and not excessive.

## Risk classification
| Severity | Meaning |
|---|---|
| High | Devcontainer runs untrusted setup, requests broad credentials, or breaks template scaffolding. |
| Medium | Missing SDK, wrong base image, broken post-create command, or incorrect ports. |
| Low | Missing badge, optional extension gaps, or naming inconsistency. |

## Limits

- Do not use this skill for: Backstage deployment (use backstage-deployment), CI/CD pipeline orchestration (use deploy-orchestration), or creating Backstage templates from scratch (use backstage-deployment).
- Keep exclusions and handoffs as by-name references to installed skills or agents, not relative links to other primitives.
- Stop before mutating infrastructure, clusters, repositories, or generated artifacts unless the procedure's confirmation gate is satisfied.

## Troubleshooting
| Situation | Action |
|---|---|
| Template path is missing | List existing `template.yaml` paths and stop. |
| Runtime stack is unclear | Ask one targeted question and provide a default only if safe. |
| `postCreateCommand` references missing files | Remove or adapt the command to existing scaffold files. |
| Codespaces feature is unavailable | Use the official devcontainers feature registry and document the fallback. |

## Output template

Return exactly this structure:
```markdown
# Codespaces Golden Path Report

## Target
- Template path:
- Runtime profile:

## Files
| File | Action |
|---|---|

## Validation
| Check | Result |
|---|---|

## Developer Instructions
- Open in Codespaces:
- Local fallback:
```

## Quality gate
- [ ] Target Golden Path path exists.
- [ ] User confirmation is captured before template file changes.
- [ ] Devcontainer JSON is valid and references existing scaffold files.
- [ ] README badge uses the correct repository placeholder or target URL.
- [ ] Frontmatter contains a valid `name` matching the directory and a `description` with positive activation language.
- [ ] The response follows `## Output template` and includes evidence for checks actually performed.
- [ ] Tool, command, and file usage stays within this skill's procedure and confirmation gates.
- [ ] Referenced repository paths and bundled resources exist before use.
- [ ] This `SKILL.md` remains under 500 lines and contains no emojis.
