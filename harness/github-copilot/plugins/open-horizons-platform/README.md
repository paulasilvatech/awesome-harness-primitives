# Open Horizons GitHub Copilot Plugin

This directory is the installable GitHub Copilot package for the Open Horizons
Agentic DevOps product. It combines focused agents, portable Agent Skills, safety
hooks, MCP integrations, and an optional repository workspace publisher.

## Package surfaces

| Path | Runtime responsibility |
| --- | --- |
| `plugin.json` | Package identity and direct component paths. |
| `agents/` | Engineering, operations, review, and AEG personas. |
| `skills/` | Reusable procedures and on-demand domain knowledge. |
| `hooks/open-horizons-safety/` | Approval and secret-safety policy for supported hook hosts. |
| `mcp.json` | Microsoft Learn, Azure, infrastructure, and Playwright MCP configuration. |
| `instructions/` | Passive repository conventions published by the workspace kit. |
| `prompts/` | Optional VS Code actions published by the workspace kit. |
| `workflows/` and `ISSUE_TEMPLATE/` | Optional GitHub automation published by the workspace kit. |

Plugin installation directly activates only components declared in
[`plugin.json`](plugin.json). Instructions, prompts, workflows, issue templates, and
`AGENTS.md` require explicit publication with `open-horizons-workspace-kit`.

## AEG feature

The AEG feature is a named family so its purpose remains visible during discovery:

- Agents: `open-horizons-aeg-concierge`, `open-horizons-aeg-gatekeeper`,
  `open-horizons-aeg-analyst`, and `open-horizons-aeg-harvester`.
- Skill: `open-horizons-backstage-aeg-feature`.
- VS Code actions: `open-horizons-aeg-start`, `open-horizons-aeg-modernize`,
  `open-horizons-aeg-status`, `open-horizons-aeg-approve`, and
  `open-horizons-aeg-harvest`.
- Passive rules: `open-horizons-backstage-aeg` instructions.

The package does not invent an AEG URL or credential scheme. An adopter configures an
authenticated MCP server named `open-horizons-aeg` that implements the contract bundled
with the AEG feature skill. Until that server is available, AEG agents report `blocked`
instead of substituting direct HTTP calls or fabricated state.

The server derives actor identity from the authenticated principal. G1 and G2 decisions
remain AEG operations; G3 pull-request approval and G4 production promotion remain in
their owning GitHub and deployment systems.

## Naming policy

| Prefix | Use |
| --- | --- |
| `open-horizons-aeg-*` | AEG roles and explicit AEG actions. |
| `open-horizons-*` | Product-specific engineering and operations. |
| `backstage-*` | Reusable Backstage capabilities. |
| `azure-*` | Azure-specific architecture and operations. |
| `foundry-*` | Microsoft Foundry application-agent capabilities. |
| `github-*` | GitHub APIs, automation, and Copilot customization. |
| `python-*` | Reusable Python engineering procedures. |

Names use kebab-case. A skill folder exactly matches its `name`, and descriptions state
both what the capability does and when it should activate. New generic names are rejected
when a domain-qualified name makes discovery clearer.

## Installation

Register this repository marketplace and install the package named in `plugin.json`:

```bash
copilot plugin marketplace add paulasilvatech/copilot-primitives
copilot plugin install open-horizons-platform@copilot-primitives
```

Verify package discovery with the installed GitHub Copilot CLI:

```bash
copilot plugin list
copilot skill list --json
copilot mcp list
```

MCP prerequisites are explicit: Azure and Playwright use Node.js and `npx`, the
infrastructure integration uses Docker, and Microsoft Learn requires outbound HTTPS. The
package embeds no service credentials.

## Workspace publication

Preview a focused AEG publication:

```bash
python3 <installed-package>/skills/open-horizons-workspace-kit/scripts/install_workspace_kit.py \
  --target <repository> \
  --profile aeg
```

Profiles are `aeg`, `core`, `automation`, and `full`. Add `--apply` only after reviewing
the complete plan. Conflicts block the transaction. Uninstall archives unchanged managed
files beneath `.github/.open-horizons-workspace-kit-backup/` and preserves modified files.

VS Code prompt files are optional actions, not GitHub Copilot CLI commands. Workflows that
must be portable across GitHub Copilot hosts live in Agent Skills.

## Validation

From the `copilot-primitives` repository root:

```bash
python3 harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-aeg-feature/scripts/validate_aeg_contract.py
python3 harness/github-copilot/plugins/open-horizons-platform/hooks/open-horizons-safety/test_guard.py
python3 harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-workspace-kit/scripts/test_install_workspace_kit.py
python3 harness/github-copilot/scripts/validate_primitives.py --strict
python3 harness/github-copilot/scripts/audit_plugins.py --check
python3 harness/github-copilot/scripts/generate_catalog.py --check
```

Static validation does not prove a remote AEG deployment or VS Code prompt execution.
Record those runtime checks separately when the required environment is available.

## References

- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [GitHub Copilot custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [GitHub Copilot hooks](https://docs.github.com/en/copilot/reference/hooks-reference)
- [Agent Skills specification](https://agentskills.io/)
- [Backstage MCP actions](https://backstage.io/docs/ai/mcp-actions)
