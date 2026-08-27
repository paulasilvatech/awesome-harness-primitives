# GitHub Copilot Instructions for Open Horizons

Open Horizons is an open-source Agentic DevOps product on Azure AKS and Backstage. It
serves Developer IDP and Agent IDP personas through one portal.

## Authority and context budget

- Keep this file short because `.github/copilot-instructions.md` enters every request.
- Use `AGENTS.md` as the detailed guide for routing, skills, hooks, and ownership.
- Do not maintain primitive counts in prose; inspect installed directories and the
  generated repository catalog.

## Copilot primitive loading

GitHub Copilot CLI reads repository primitives from `.github/` plus `AGENTS.md`.
Canonical runtime locations include `.github/agents/`, `.github/skills/`,
`.github/instructions/`, `.github/mcp.json`, `.github/copilot/settings.json`, and
`.github/copilot-instructions.md`. Hook descriptors use `.github/hooks/*.json`.

- `~/.copilot/` is user-level configuration. Repo-local `.copilot/` is documentation only.
- `.github/prompts/*.prompt.md` files are explicit VS Code actions, not CLI commands.
- `.github/mcp.json` is read by GitHub Copilot CLI; `.vscode/mcp.json` is VS Code-only.
- Keep GitHub Copilot AI identifiers and Microsoft Foundry deployment identifiers on
  their owning runtime surfaces.

Official references: [CLI configuration](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference),
[custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration), and
[hooks](https://docs.github.com/en/copilot/reference/hooks-reference).

## Architecture map

```text
L5 Agentic Execution  -> Backstage agent services + AEG + repository agents
L4 Intent Engineering -> CONSTITUTION.md + .specs/ + scripts/golden-paths/
L3 Context Engineering-> MCP servers + memory + .github/skills/ + CODEMAP.md
L2 Developer Portal   -> Backstage + deploy/ + policies/ + observability
L1 Cloud Foundation   -> infrastructure modules + backstage/k8s/
```

Horizon stages are H1 Foundation, H2 Enhancement, and H3 Innovation.

## Durable engineering rules

- Use explicit deployment image versions and reject floating tags.
- Use Workload Identity or Managed Identity; never commit service-principal secrets.
- Store secrets in Azure Key Vault or another approved secret store.
- Kubernetes manifests set resources, non-root security context, probes, network policy,
  and standard `app.kubernetes.io/*` labels.
- Infrastructure code pins provider versions, uses reusable modules, and preserves
  `environment`, `project`, `owner`, and `cost-center` tags.
- Python uses Python 3.11+, FastAPI, Pydantic, structlog, and PEP 8.
- Shell scripts use strict mode, usage text, input validation, and meaningful names.

## Operational routing

- Default repository work to brownfield maintenance.
- Use `open-horizons-orchestrator` for cross-domain routing and
  `open-horizons-engineer` for general implementation, tests, and documentation.
- Use `open-horizons-aeg-*` agents with `open-horizons-backstage-aeg-feature` for AEG
  runs, G1/G2 decisions, analysis, and harvesting.
- The authenticated AEG server derives actor identity and enforces roles. The AI does
  not send actor, role, or tenant claims as request arguments.
- Application agents (`orchestrator`, `pipeline`, `sentinel`, `compass`, `guardian`,
  `lighthouse`, `forge`) use Microsoft Agent Framework and Microsoft Foundry Hosted
  Agents, not repository harness AI identifiers.
- Every routed issue template emits an `agent:` label that resolves to an installed
  repository agent; `config.yml` is chooser configuration and is not routed.

## Common commands

```bash
./scripts/deploy-full.sh --environment dev --dry-run
./scripts/deploy-full.sh --environment dev
./scripts/validate-prerequisites.sh
./scripts/validate-config.sh --environment dev
./scripts/validate-deployment.sh --environment dev
```
