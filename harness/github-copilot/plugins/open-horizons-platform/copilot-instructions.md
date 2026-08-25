# GitHub Copilot Instructions for Open Horizons

Open Horizons is an open-source Agentic DevOps Platform on Azure AKS and Backstage. It serves Developer IDP and Agent IDP personas through one portal.

## Authority and token budget

- Keep this file short: `.github/copilot-instructions.md` is injected into every Copilot request.
- Use `AGENTS.md` as the authoritative long-form inventory for agents, prompts, instructions, skills, hooks, and path references.
- Do not duplicate primitive counts here; use the generated current inventory in `AGENTS.md`.

## Copilot primitive loading

Copilot CLI reads repository primitives from `.github/` natively, plus `AGENTS.md`. Canonical paths include `.github/agents/`, `.github/skills/`, `.github/instructions/`, `.github/mcp.json`, `.github/copilot/settings.json`, and `.github/copilot-instructions.md`; hook descriptors are discovered from `.github/hooks/*.json` only when present.

- `~/.copilot/` is user-level config. A repo-local `.copilot/` directory is not a recognized Copilot CLI primitive path; `.copilot/README.md` is documentation only.
- `.github/prompts/*.prompt.md` files are explicit VS Code actions. Copilot CLI does not discover or execute them as slash commands.
- `.github/mcp.json` is read by Copilot CLI; `.vscode/mcp.json` is read by VS Code only.
- `.github/model-routing.yaml` is a validated runtime contract with two isolated surfaces: GitHub Copilot models for repository harness agents and Microsoft Foundry deployments for the seven MAF application agents. Never pass model identifiers across surfaces.

Official references: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference, https://docs.github.com/en/copilot/reference/custom-agents-configuration, and https://docs.github.com/en/copilot/reference/hooks-reference.

## Architecture map

```text
L5 Agentic Execution  -> backstage/server/agent-api-maf/ (application) + .github/agents/ (engineering harness)
L4 Intent Engineering  -> CONSTITUTION.md + .specs/ + scripts/golden-paths/ + .github/model-routing.yaml
L3 Context Engineering -> mcp-servers/ + backstage/server/agent-api/memory/ + .github/skills/ + CODEMAP.md
L2 Platform Engineering-> backstage/ + deploy/ + policies/ + grafana/ + prometheus/
L1 Cloud/Infrastructure-> terraform/modules/ + backstage/k8s/
```

Horizon stages: H1 Foundation, H2 Enhancement, H3 Innovation.

## Durable engineering rules

- Never use `:latest` in deployment manifests; use explicit version tags.
- Use Workload Identity or Managed Identity; never commit service principal secrets.
- Store secrets in Azure Key Vault, not source code.
- Kubernetes manifests must set resource requests/limits, non-root security contexts, probes, network policies, and standard `app.kubernetes.io/*` labels.
- Terraform uses snake_case, provider versions, reusable modules, and tags: `environment`, `project`, `owner`, `cost-center`.
- Python uses Python 3.11+, FastAPI, Pydantic, structlog, and PEP 8.
- Shell scripts use bash strict mode, usage text, input validation, and meaningful variable names.

## Operational notes

- GitHub Copilot harness work defaults to brownfield maintenance. Use `open-horizons-orchestrator` for cross-domain routing and `open-horizons-engineer` for general bug fixes, features, improvements, modernization, tests, and documentation.
- The seven application agents (`orchestrator`, `pipeline`, `sentinel`, `compass`, `guardian`, `lighthouse`, `forge`) use Microsoft Agent Framework and Microsoft Foundry Hosted Agents, not GitHub Copilot models.
- Ignored local add-ons are excluded from the generated repository inventory.
- Context quality and intent drift scripts are `scripts/audit-context-quality.sh` and `scripts/measure-intent-drift.sh`.
- All 26 issue forms under `.github/ISSUE_TEMPLATE/` emit an `agent:` label that resolves to a repository agent; `config.yml` is the issue-template chooser configuration and is not routed.

## Common commands

```bash
./scripts/deploy-full.sh --environment dev --dry-run
./scripts/deploy-full.sh --environment dev
./scripts/validate-prerequisites.sh
./scripts/validate-config.sh --environment dev
./scripts/validate-deployment.sh --environment dev
```
