# Open Horizons Agent Guide

This is the detailed routing and engineering guide published by
`open-horizons-workspace-kit`. Repository custom instructions stay concise; this guide
owns role selection, responsibility boundaries, and durable validation expectations.
Inspect `.github/agents/`, `.github/skills/`, `.github/instructions/`, and
`.github/prompts/` for the installed inventory instead of maintaining manual counts.

## Architecture map

```text
L5 Agentic execution   -> Backstage agent services + AEG + repository agents
L4 Intent engineering -> CONSTITUTION.md + .specs/ + golden paths + approval gates
L3 Context engineering-> MCP servers + memory + Agent Skills + CODEMAP.md
L2 Developer portal   -> Backstage + GitOps + policy + observability
L1 Cloud foundation   -> Infrastructure-as-code modules + AKS manifests
```

The repository-agent harness and application agents are separate runtime surfaces.
GitHub Copilot agents inherit the selected AI choice unless an agent has a verified
reason to pin one. Application agents use Microsoft Agent Framework and the Foundry
deployment configuration owned by their service. Never pass AI identifiers between
those surfaces.

## Repository routing

| Request | Primary agent | Authority boundary |
| --- | --- | --- |
| Unclear or cross-domain repository work | `open-horizons-orchestrator` | Reads and routes; does not implement or deploy. |
| Architecture, SDD, or trust-boundary decisions | `open-horizons-architect` | Writes only an explicitly approved design destination. |
| General code, tests, automation, or documentation | `open-horizons-engineer` | Implements the smallest bounded repository change. |
| Backstage portal, catalog, templates, auth, or plugins | `open-horizons-backstage-expert` | Owns portal code, not cloud deployment. |
| Infrastructure-as-code authoring and validation | `IAC_AGENT` | Plans and validates; never applies. |
| Azure prerequisite and readiness evidence | `open-horizons-azure-readiness` | Read-only cloud assessment. |
| Independent security findings | `open-horizons-security-reviewer` | Reviews; does not accept its own findings. |
| Reliability symptom or incident analysis | `open-horizons-sre-investigator` | Read-only investigation and mitigation advice. |
| Approved rollout, rollback, or verification | `open-horizons-deployment-operator` | Executes only an immutable, approved change package. |

Default to brownfield maintenance. Greenfield design requires explicit user intent.
Every writable path has one owner, and broad changes receive independent validation.

## AEG routing

| Request | Primary agent | Boundary |
| --- | --- | --- |
| Start a run or report status | `open-horizons-aeg-concierge` | Never decides gates. |
| Present or record G1/G2 | `open-horizons-aeg-gatekeeper` | Never self-approves or handles G3/G4. |
| Analyze traceability, findings, metrics, or cost | `open-horizons-aeg-analyst` | Read-only and evidence-bound. |
| Propose a reusable stack profile | `open-horizons-aeg-harvester` | Creates a draft only; publication is a reviewed PR. |

Each AEG agent loads `open-horizons-backstage-aeg-feature` before acting. That skill owns
lifecycle vocabulary, tool classification, actor identity rules, and output contracts.
The authenticated `open-horizons-aeg` MCP server derives the actor and enforces roles.
The AI never supplies `initiated_by`, `decided_by`, `proposed_by`, roles, or tenant claims
as request arguments.

G1 and G2 are AEG decisions. G3 pull-request approval remains in GitHub, and G4 production
promotion remains in the deployment environment. Successful checks are evidence, not
approval.

## Primitive responsibilities

- Agents define persona, judgment, authority, and tool limits.
- Skills define reusable procedures and load detailed references on demand.
- Instructions define passive conventions for matching files.
- Prompts define explicit VS Code actions and are not GitHub Copilot CLI commands.
- Hooks provide bounded lifecycle policy; they do not replace backend authorization.
- MCP servers expose typed capabilities and enforce identity and authorization server-side.

Use the narrowest applicable skill. Keep descriptions domain-qualified and trigger-rich.
Never duplicate long domain guidance in an agent when a companion skill owns it.

## Engineering rules

- Use Workload Identity or Managed Identity and keep credentials in approved secret stores.
- Never commit service-principal credentials or literal secrets in `app-config*.yaml`.
- Use explicit container image versions rather than floating tags.
- Give Kubernetes workloads resources, probes, non-root security context, network policy,
  and standard `app.kubernetes.io/*` labels.
- Pin infrastructure provider versions, use reusable modules, and preserve environment,
  project, owner, and cost-center tags.
- Keep authentication, authorization, tool visibility, and approval as separate controls.
- Treat local files and runtime responses as evidence; do not invent status, metrics, cost,
  deployment state, or validation results.

## Working method

1. Start from the concrete file, failing behavior, command, or acceptance criterion.
2. Read the owning abstraction and the narrowest applicable instruction or skill.
3. State one falsifiable local hypothesis and one focused check.
4. Make the smallest authorized change and immediately run the focused check.
5. Escalate cross-domain conflicts to the architect or orchestrator.
6. Stop for approval before deployment, gate decisions, publication, identity changes, or
   other high-impact mutation.
7. Report changed paths, checks actually run, unrun checks, residual risk, and handoff.

## Common validation

```bash
./scripts/validate-prerequisites.sh
./scripts/validate-config.sh --environment dev
./scripts/deploy-full.sh --environment dev --dry-run
python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict
```

Use repository-specific help and narrower tests when available. Never report a dry run as
a deployment or static primitive validation as runtime activation.

## References

- [AGENTS.md](https://agents.md/)
- [GitHub Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-repository-instructions/add-repository-instructions)
- [GitHub Copilot custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Agent Skills specification](https://agentskills.io/)
- [Backstage MCP actions](https://backstage.io/docs/ai/mcp-actions)
