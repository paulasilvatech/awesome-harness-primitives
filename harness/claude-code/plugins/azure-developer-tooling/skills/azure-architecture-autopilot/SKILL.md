---
name: azure-architecture-autopilot
description: >-
  Design new Azure infrastructure or analyze existing Azure resources, generate interactive
  architecture diagrams, refine through conversation, produce Bicep, review, and deploy. Use when
  asked to design, analyze, modify, or deploy Azure architecture, including "Create X on Azure",
  "Set up a RAG architecture", "Analyze my current Azure infrastructure", "Draw a diagram for
  rg-xxx", Foundry slowness, cost reduction, security strengthening, Microsoft Foundry, AI Search,
  OpenAI, Fabric, ADLS Gen2, Databricks, and Azure services.
---

<!-- Generated from harness/github-copilot/plugins/azure-developer-tooling/skills/azure-architecture-autopilot/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure architecture autopilot

Run a phased Azure architecture pipeline that detects whether the user needs a new design or existing-resource analysis, generates an interactive diagram with bundled Azure icons, then moves through Bicep generation, review, what-if, and deployment without skipping required confirmations.

## When to invoke

- "Create X on Azure."
- "Set up a RAG architecture."
- "Analyze my current Azure infrastructure."
- "Draw a diagram for rg-xxx."
- "Foundry is slow; reduce costs and strengthen security."

## Language and communication rules

Detect the language of the user's first message and keep all user-facing output in that language, including ask_user text, progress updates, reports, and Bicep comments. If the user writes in Korean, respond in Korean. If the user writes in English, respond in English. Do not copy examples from this skill verbatim; adapt structure and content to the user's language.

Progress updates use blockquote plus bold labels:

```markdown
> **[Action]** — [Reason]
> **[Complete]** — [Result]
> **[Warning]** — [Details]
> **[Failed]** — [Cause]
```

## Prerequisites and context

- The diagram engine is embedded in `scripts/`; do not install packages for it.
- Fact-check dynamic Azure facts with Microsoft Docs using `web_fetch` and `web_search` directly from the main agent.
- Sub-agents cannot use `web_fetch` or `web_search`; do Microsoft Docs lookups in the main context.
- `az`, `python`, and `bicep` may not be on PATH. Discover each executable once before a phase and cache the path. On Windows, do not use `Get-Command python`; prefer direct filesystem discovery under `$env:LOCALAPPDATA\Programs\Python` to avoid the Windows Store alias.

Azure CLI discovery pattern:

```powershell
$azCmd = $null
if (Get-Command az -ErrorAction SilentlyContinue) { $azCmd = 'az' }
if (-not $azCmd) {
  $azExe = Get-ChildItem -Path "$env:ProgramFiles\Microsoft SDKs\Azure\CLI2\wbin", "$env:LOCALAPPDATA\Programs\Azure CLI\wbin" -Filter "az.cmd" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
  if ($azExe) { $azCmd = $azExe }
}
```

## Path branching

| Path | Trigger | Required phases |
| --- | --- | --- |
| Path A: New Design (New Build) | "create", "set up", "deploy", "build" | Phase 1 `references/phase1-advisor.md` → Phase 2 `references/bicep-generator.md` → Phase 3 `references/bicep-reviewer.md` → Phase 4 `references/phase4-deployer.md` |
| Path B: Existing Analysis + Modification | "analyze", "current resources", "scan", "draw a diagram", "show my infrastructure" | Phase 0 `references/phase0-scanner.md` → modification conversation → Phase 1 → Phase 2~4 |
| Ambiguous | User could mean either | Ask: `What would you like to do?` with choices `Design a new Azure architecture (Recommended)` and `Analyze + modify existing Azure resources`. |

For modification requests after deployment, return to Phase 1, not Phase 0. This is the Delta Confirmation Rule.

## Procedure

1. Detect language and determine Path A, Path B, or ambiguous path.
2. Discover tool paths once for the phase: `az`, `python`, `bicep`, and diagram module path.
3. While waiting for user input, preload the next-step information in parallel: reference files, Microsoft Docs, Python path discovery, diagram module path verification, `az account show/list`, or `az group list` depending on the question.
4. For Path B, run Phase 0 scan and diagram before asking what to modify.
5. Run Phase 1 interactive design or modification confirmation and generate `01_arch_diagram_draft.html` with the embedded diagram engine.
6. Do not proceed to Bicep generation until the diagram has been generated and shown to the user. Spec collection alone does not complete Phase 1.
7. Run Phase 2 Bicep generation, Phase 3 code review plus compilation verification, and Phase 4 validate → what-if → deploy.
8. Always inform the user when transitioning phases and never skip the what-if between Phase 3 and Phase 4.

## Service coverage and sources

Optimized services include Microsoft Foundry, Azure OpenAI, AI Search, ADLS Gen2, Key Vault, Microsoft Fabric, Azure Data Factory, VNet/Private Endpoint, and AML/AI Hub. Other Azure services are supported by consulting Microsoft Docs; do not send anxiety-inducing messages such as "out of scope" or "best-effort".

| Information type | Handling | Examples |
| --- | --- | --- |
| Stable | Use reference files first | `isHnsEnabled: true`, Private Endpoint triple set, PE/security/naming patterns. |
| Dynamic | Always fetch Microsoft Docs | API version, model availability, SKU, and region. |

## Progressive disclosure and bundled resources

- `references/phase0-scanner.md`: existing resource scan, relationship inference, and diagram.
- `references/phase1-advisor.md`: interactive architecture design, diagram generation, and fact checking.
- `references/bicep-generator.md`: Bicep code generation rules.
- `references/bicep-reviewer.md`: code review checklist and compilation verification.
- `references/phase4-deployer.md`: validate → what-if → deploy.
- `references/service-gotchas.md`: required properties and PE mappings.
- `references/azure-dynamic-sources.md`: Microsoft Docs URL registry.
- `references/azure-common-patterns.md`: PE, security, and naming patterns.
- `references/ai-data.md`: AI/Data service guide.
- `assets/06-architecture-diagram.png`: example generated architecture diagram.
- `assets/07-azure-portal-resources.png`: example Azure portal resource view.
- `assets/08-deployment-succeeded.png`: example successful deployment result.

## Gotchas

- **Do not skip diagram confirmation**: Phase 1 is incomplete until `01_arch_diagram_draft.html` is generated and shown.
- **Do not rediscover tools repeatedly**: discover once per phase and cache paths.
- **Do not use `Get-Command python` on Windows**: it may hit the Windows Store alias.
- **Do not delegate Microsoft Docs fact-checking to sub-agents**: they cannot use `web_fetch` or `web_search`.
- **Do not skip what-if**: Phase 4 must run validate and what-if before deploy.

<!-- Baseline technical terms preserved for loss check: `GHCP`, `HTML`, `Model/SKU`, `auto-generate`, `choices`, `explore/task/general-purpose`, `follow-up`, `general-purpose`, `highest-priority`, `pip install`, `PowerShell` / `powershell`, `re-discover`, `task` -->

## Output template

```markdown
### Azure architecture autopilot result

**Status:** designed | analyzed | deployed | needs input | blocked
**Path:** New Design | Existing Analysis + Modification
**Current phase:** Phase 0 | Phase 1 | Phase 2 | Phase 3 | Phase 4
**Diagram:** `01_arch_diagram_draft.html`

| Phase | Artifact | Validation | Notes |
| --- | --- | --- | --- |
| Phase 0 | <scan/diagram or n/a> | <result> | <notes> |
| Phase 1 | <diagram/spec> | shown to user | <notes> |
| Phase 2 | <Bicep files> | generated | <notes> |
| Phase 3 | <review/compile> | pass/fail | <notes> |
| Phase 4 | <what-if/deploy> | pass/fail | <notes> |

**Next step:** <action or user decision needed>
```

## Quality gate

- [ ] User-facing output language matches the user's first message.
- [ ] Path A, Path B, or ambiguous branch was selected from the user's request.
- [ ] Tool paths were discovered once and reused for the phase.
- [ ] Dynamic Azure facts were checked against Microsoft Docs.
- [ ] `01_arch_diagram_draft.html` was generated and shown before Bicep generation.
- [ ] Each phase read and followed its corresponding `references/*.md` file.
- [ ] Phase 4 includes validate and what-if before deploy.
- [ ] Referenced bundled files exist and were loaded only when needed.
