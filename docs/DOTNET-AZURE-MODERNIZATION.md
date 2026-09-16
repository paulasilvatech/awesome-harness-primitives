# Legacy .NET migration and Azure modernization

A standalone primitive suite for two distinct paths:

1. **Rehost:** retain the legacy ASP.NET/.NET Framework application in a Windows custom container on
   Azure App Service, subject to platform and dependency assessment.
2. **Modernize:** upgrade the runtime and application model, prove Linux portability, then prepare
   Linux App Service or Azure Container Apps (ACA).

The suite does not assume an application is portable, provision Azure resources, install an SDK, or
publish containers merely because it was installed. Its bundled scripts are local, read-only checks.

## Verified platform snapshot

Official documentation was checked on **2026-09-15**:

| Decision | Evidence-based guidance |
| --- | --- |
| New stable-LTS modernization target | [.NET support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core), updated 2026-09-08, lists .NET 10 LTS through 2028-11-14. Recheck patches, SDK and support at execution time. |
| .NET 8/9 or .NET 11 | The same policy lists 8/9 in maintenance through 2026-11-10 and 11 RC1 as a pre-release. Do not confuse highest version with a stable production default. |
| Keep Windows | [App Service custom containers](https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container) documents LTSC-based Windows images; Windows Server 2025 bases are explicitly unsupported. |
| Move to ACA | [ACA container requirements](https://learn.microsoft.com/en-us/azure/container-apps/containers) specify Linux `amd64`; a Windows image cannot be reused as-is. |
| Upgrade tooling | [Upgrade Assistant](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview) is marked deprecated. Discover an available [GitHub Copilot upgrade workflow](https://learn.microsoft.com/en-us/dotnet/core/porting/github-copilot-upgrade/overview) or use reviewed manual changes. |

The detailed source ledger, including a lifecycle-documentation divergence, is in
[validation evidence](HARNESS-VALIDATION.md#net-azure-modernization-suite-evidence).
These checks are documentation evidence, not proof that a real application runs in any target.

## Components and responsibility

| Type | Component | Responsibility |
| --- | --- | --- |
| Agent | [dotnet-modernization-assessor](../harness/github-copilot/agents/dotnet-modernization-assessor.agent.md) | Read-only evidence, target choice, blockers, alternatives and handoff. No shell or writes. |
| Agent | [dotnet-azure-modernizer](../harness/github-copilot/agents/dotnet-azure-modernizer.agent.md) | Bounded implementation and orchestration; cloud/Git mutations require separate authorization. |
| Skill | [dotnet-modernization-assessment](../harness/github-copilot/skills/dotnet-modernization-assessment/SKILL.md) | Inventory interpretation, path assessment and local image/port checks. |
| Skill | [dotnet-windows-appservice](../harness/github-copilot/skills/dotnet-windows-appservice/SKILL.md) | Legacy Windows-container rehosting, build/identity/state/rollout validation. |
| Skill | [dotnet-linux-modernization](../harness/github-copilot/skills/dotnet-linux-modernization/SKILL.md) | Runtime and app-model modernization, Linux portability, App Service versus ACA. |
| Instructions | [dotnet-azure-modernization](../harness/github-copilot/instructions/dotnet-azure-modernization.instructions.md) | Passive project/container compatibility, identity, state and validation invariants. |
| Reused skill | [dotnet-upgrade](../harness/github-copilot/skills/dotnet-upgrade/SKILL.md) | Framework/package upgrade procedure; refreshed together with its existing agent and instructions. |

Optional companions are `legacy-characterization-testing`, `azure-prepare`, `azure-validate`, and
`azure-deploy` (skills). The suite describes the fallback when they or Microsoft upgrade tools are
unavailable. It does not assume an MCP server name, fixed model, or VS Code-only tool ID.

## Install in the application repository

These are **standalone library components**, not a newly registered plugin. They are not automatically
installed into this curator repository's own customizations.

For GitHub Copilot, copy the two new agent files into the target application's `.github/agents/`,
the three complete skill directories plus `dotnet-upgrade` into `.github/skills/`, and the new
instruction file into `.github/instructions/`. Preserve bundled references and scripts.
Compare existing destinations first; do not overwrite user customizations.

For Claude Code, use the generated equivalents from
[the Claude harness](../harness/claude-code/README.md): subagents into `.claude/agents/`, complete skill
directories into `.claude/skills/`, and the generated rule into `.claude/rules/`.
The standalone CLI helpers have the same input/output contract. Do not manually edit the generated
Claude sources.

The pre-existing `dotnet-upgrade` agent and instructions are optional if using the new orchestrator;
its skill is the shared upgrade procedure. Avoid installing unrelated .NET rules blindly, and scope
the installed instruction globs to the application's folders when sharing a monorepo.
See [general installation guidance](USAGE.md) for discovery and runtime boundaries.

## Typical requests

Select `dotnet-modernization-assessor` for a read-only decision:

```text
Assess this ASP.NET Framework application. Compare a Windows-container rehost on App Service
with modernization to the supported .NET LTS and Linux. Do not modify files or deploy.
```

Select `dotnet-azure-modernizer` for authorized preparation:

```text
Use the assessment to prepare only the Windows App Service rehost.
Preserve the framework and application behavior. Do not publish images or create Azure resources.
```

```text
Modernize the selected API to the verified supported .NET LTS, preserve its tested contract,
prove Linux compatibility, and prepare ACA configuration. Stop before deployment.
```

If the user writes in another language, respond in that language while preserving exact primitive
names. No VS Code prompt file is needed to use these agents or skills.

## Local scripts

Use the configured Python 3.10+ executable. From an application repository with the skill installed:

```sh
python3 .github/skills/dotnet-modernization-assessment/scripts/inventory_dotnet.py .
python3 .github/skills/dotnet-modernization-assessment/scripts/validate_container_target.py --image-inspect image-inspect.json --target aca --framework net10.0 --listen-port 8080 --target-port 8080
```

The second command requires inspection JSON collected from the actual selected image. It does not
collect that evidence itself and does not run a container. A synthetic object is suitable for tests,
not a deployment claim.

| Script | Output | Exit semantics |
| --- | --- | --- |
| [inventory_dotnet.py](../harness/github-copilot/skills/dotnet-modernization-assessment/scripts/inventory_dotnet.py) | Literal project inventory, package IDs, Windows/app-model signals and coverage warnings. | `0` complete selected text scan; `1` incomplete; `2` invalid input/error. |
| [validate_container_target.py](../harness/github-copilot/skills/dotnet-modernization-assessment/scripts/validate_container_target.py) | Image/TFM/platform and declared port consistency, with explicit unchecked items. | `0` platform-consistent only; `1` incompatible; `2` invalid evidence/error. |

Neither script emits source snippets, secret configuration values or inspection environment variables.
Neither evaluates MSBuild nor establishes runtime support or behavior.
See [full contracts and limitations](../harness/github-copilot/skills/dotnet-modernization-assessment/references/script-contracts.md).

## Validation and execution limits

The [synthetic tests](../harness/github-copilot/skills/dotnet-modernization-assessment/scripts/test_dotnet_assessment.py)
run with the repository's existing standard-library runner:

```sh
cd harness/github-copilot/skills/dotnet-modernization-assessment/scripts
python3 -m unittest test_dotnet_assessment -v
```

CI already discovers bundled `test_*.py` files, including generated copies; no new test dependency or
runner was introduced. Primitive validators, generated catalogs, plugin copies of reused components,
Claude conversion and installed-copy drift checks remain the repository completion gates.

Actual migration still requires an application, its approved baseline, a compatible Windows runner
for the Windows path, a Linux runner for Linux validation, and explicitly authorized Azure access for
cloud checks. Agent runtime activation, Windows/Linux application builds and Azure deployment have
not been proven merely by generating and structurally validating this suite.
