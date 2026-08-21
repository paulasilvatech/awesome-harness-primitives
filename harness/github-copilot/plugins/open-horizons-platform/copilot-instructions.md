# GitHub Copilot Instructions for Open Horizons

Start with the shared, tool-agnostic repository instructions in @../AGENTS.md.

Do not duplicate project architecture, commands, layout, security, naming, or language standards here. This file only explains Copilot-specific loading and routing.

## Copilot instruction loading

- VS Code Copilot Chat, Copilot CLI, and the Copilot cloud agent load this file for repository-wide guidance.
- Copilot CLI and the cloud agent also load the root `AGENTS.md`; VS Code also supports `AGENTS.md` as always-on agent guidance.
- The `@../AGENTS.md` reference above is relative to this `.github/` file and resolves to the repository root `AGENTS.md`.
- `.github/instructions/*.instructions.md` files are `applyTo`-scoped and hold file-type or tool-specific standards.
- Use [.github/README.md](README.md) for the integration map across agents, skills, instructions, prompts, hooks, MCP, and cloud setup.

## Copilot primitives

Deploy-managed Copilot chat agents live in `agents/` and define personas, judgment boundaries, and scope:

- `@deploy`
- `@terraform`
- `@security`
- `@sre`
- `@open-horizons-backstage-expert`
- `@azure-portal-deploy`
- `@github-integration`
- `@ado-integration`
- `@hybrid-scenarios`

Skills live in `skills/` and package reusable procedures or review criteria. Load skills progressively so their detailed bodies enter context only when relevant.

Prompt shortcuts live in `prompts/`, but they are VS Code-only. Copilot CLI and Agent Host workflows must use skills instead of depending on prompt files.

## Scoped standards

Do not inline language or tool standards in this always-loaded file. Use these scoped files instead:

- Terraform: @instructions/terraform.instructions.md
- Kubernetes: @instructions/kubernetes.instructions.md
- Python: @instructions/python.instructions.md
- Shell: @instructions/shell.instructions.md
- TypeScript: @instructions/typescript.instructions.md
- GitHub Actions: @instructions/github-actions.instructions.md
- Dockerfile: @instructions/dockerfile.instructions.md
- Docker Compose: @instructions/docker-compose.instructions.md
- Issue forms: @instructions/issue-forms.instructions.md
- Agents, prompts, skills, and instruction files: @instructions/agent-files.instructions.md

## Agent file guidance

When generating or reviewing Copilot agents, prompts, skills, or instructions:

- Follow @instructions/agent-files.instructions.md.
- Use the repository contracts in @docs/COPILOT-HARNESS-SPEC.md and @docs/templates/README.md.
- Include only frontmatter fields supported by the target primitive.
- Define clear ALWAYS, ASK FIRST, and NEVER boundaries for agents.
- Reference skills by installed name and type instead of copying skill content or linking to another primitive by relative path.
- Do not copy VS Code prompt `tools` values such as `search/codebase` or `vscode/askQuestions` into agent frontmatter. Agent `tools` lists may deliberately combine VS Code tool sets such as `search` with CLI tokens such as `grep` and `glob`; see @README.md before removing apparent duplicates.

## Model routing

`model-routing.yaml` is a repository-internal convention and documentation aid. Copilot does not read or enforce it. For Copilot agents, use per-agent `model:` frontmatter in `agents/*.agent.md` only when model pinning is required and supported by the current Copilot agent format.
