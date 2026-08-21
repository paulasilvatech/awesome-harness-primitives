# GitHub Copilot Agent Skills

This directory contains 30 Open Horizons skills for GitHub Copilot, GitHub Copilot CLI, and cloud agent workflows. Skills use progressive loading: only `name` and `description` are loaded for discovery, and the full `SKILL.md` body plus bundled resources load only after activation.

## Authoritative contract

Skills in this directory follow the package contract in `../docs/templates/skill.template.md` and the empirically validated harness specification in `../docs/COPILOT-HARNESS-SPEC.md` (validated against GitHub Copilot CLI 1.0.81-0).

Required contract points:

1. Frontmatter includes required `name` and `description`. The `name` is kebab-case, 1-64 characters, and exactly matches the parent directory.
2. `description` is 1-1024 characters, starts with positive trigger language, states what the skill does and when to use it, preserves `DO NOT USE FOR:` routing disambiguation, and includes natural trigger phrases.
3. Optional frontmatter is minimal. `argument-hint` is valid for skills, but only belongs on skills that consume and validate `$ARGUMENTS` in an `## Inputs` section. `allowed-tools` is omitted unless the procedure truly needs a restricted pre-approval list.
4. The body uses `## When to invoke`, `## Prerequisites and context`, `## Procedure` when order matters, `## Criteria` only when judgment matters, `## Limits`, `## Troubleshooting` for real failure modes, `## Output template`, and `## Quality gate`.
5. `## Output template` must be precise enough for repeatable results.
6. `## Quality gate` verifies frontmatter, activation language, output conformance, evidence, tool scope, confirmation gates, bundled resources, line count, and no emoji usage.
7. `SKILL.md` stays under 500 lines, preferably under 200; longer material lives in bundled `references/`, `scripts/`, `assets/`, or `templates/` resources.
8. Cross-references to other primitives use installed name and type, not relative Markdown links. Relative paths are used only for files bundled in the same skill or concrete repository paths.
9. Skills never reference `.prompt.md` files; prompts are VS Code-only and are not GitHub Copilot CLI primitives.

## Available skills

| Skill name | Purpose | Common users |
| --- | --- | --- |
| `agentic-architecture-patterns` | Agentic system architecture decisions and reviews | `@deploy`, `@security` |
| `ai-foundry-operations` | Azure AI Foundry operations | `@deploy`, `@azure-portal-deploy` |
| `architecture-doc` | Architecture document validation | `@deploy` |
| `argocd-cli` | ArgoCD operations | `@deploy`, `@sre` |
| `azure-architecture-diagrams` | Azure architecture diagrams | `@deploy` |
| `azure-cli` | Azure CLI operations | `@terraform`, `@security`, `@sre`, `@azure-portal-deploy` |
| `azure-infrastructure` | Azure infrastructure patterns | `@terraform`, `@security`, `@azure-portal-deploy` |
| `azure-managed-redis-cache` | Azure Managed Redis patterns | `@deploy`, `@terraform` |
| `backstage-deployment` | Backstage portal operations | `@backstage-expert`, `@deploy` |
| `backstage-plugin-builder` | Backstage plugin and module planning, scaffolding, validation, and publication preparation | `@backstage-expert`, `@deploy` |
| `codespaces-golden-paths` | Codespaces dev environments | `@backstage-expert`, `@deploy` |
| `database-management` | Database operations | `@terraform`, `@sre`, `@deploy` |
| `deploy-orchestration` | End-to-end deployment orchestration | `@deploy` |
| `foundry-agent-blueprint` | Azure AI Foundry agent blueprint | `@deploy`, `@azure-portal-deploy` |
| `github-cli` | GitHub API operations | `@deploy`, `@github-integration` |
| `helm-cli` | Helm chart operations | `@deploy`, `@backstage-expert`, `@sre` |
| `issue-ops` | IssueOps dispatcher patterns | `@deploy` |
| `kubectl-cli` | Kubernetes CLI operations | `@deploy`, `@backstage-expert`, `@sre` |
| `markdown-writer` | Markdown document writing | `@deploy` |
| `mcp-ecosystem` | Local MCP reference server lookup | `@backstage-expert`, `@deploy` |
| `observability-stack` | Monitoring operations | `@sre`, `@deploy` |
| `open-horizons-workspace-kit` | Safe publication of instructions, prompts, hooks, automation, governance, and optional project runtime copies | Maintainers and platform teams |
| `pipeline-diagnostics` | GitHub Actions CI/CD diagnostics | `@deploy` |
| `prerequisites` | CLI prerequisite validation | `@deploy` |
| `requirements-engineer` | FRD and NFRD requirements engineering | `@deploy` |
| `sdd-spec-engineer` | Spec-driven development artifacts | `@deploy` |
| `story-planning` | INVEST story planning and optional GitHub Issues | `@deploy` |
| `terraform-cli` | Terraform CLI operations | `@terraform`, `@security`, `@deploy` |
| `test-coverage` | Test coverage and quality gates | `@deploy` |
| `validation-scripts` | Repository validation scripts | `@deploy`, `@sre`, `@security` |

## Validation

Run strict validation after changing skills:

```bash
python3 validation-scripts/scripts/validate-agents.py --strict
```

Review `git status --short` and confirm changes are limited to the intended skill packages, bundled resources, and directly related integration files.
