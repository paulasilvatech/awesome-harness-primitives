# GitHub Copilot CLI Harness Runtime Validation

Date: 2026-08-17
CLI: `GitHub Copilot CLI 1.0.81-0`
Binary: `/Users/paulasilva/.local/bin/copilot`

> Note: the requested scratch root was `/tmp/harness-check`, but this execution environment forbids file operations under `/tmp`. I used `/Volumes/T9/harness-check` instead. The live `~/.copilot` tree was not modified; commands used `COPILOT_HOME=/Volumes/T9/harness-check/copilot-home`.

## Mainframe modernization plugin runtime verification

Verification date: 2026-08-26. Target runtime: GitHub Copilot CLI 1.0.81-9. The probe used
new temporary repositories and an isolated `COPILOT_HOME`; the live user configuration was not modified.

| Evidence | Verified result |
| --- | --- |
| Local marketplace registration and `copilot plugin install mainframe-modernization@copilot-primitives` | The plugin installed and enabled successfully as version 0.1.0 from the local repository marketplace. |
| `copilot skill list --json` | Plugin discovery exposed 15 skills, including `sifap-modernization-context`, `sifap-requirements-traceability`, `sifap-workshop-orchestration`, and `sifap-workspace-kit`. |
| Qualified agent invocation | `mainframe-modernization:sifap-archaeologist` resolved and returned the requested `sifap-ok` probe response. |
| Traceability validator tests | Five standard-library tests passed for real legacy evidence, justified greenfield evidence, missing source, placeholder source, and duplicate identifier cases. |
| Workspace publisher tests | Sixteen standard-library tests passed for profiles, preview, idempotence, conflicts, transaction rollback, retired assets, profile switching, archive-based uninstall, modified-file preservation, and state validity. |
| Disposable repository lifecycle | The `full` profile published 36 managed files; a second preview reported all 36 `unchanged`; uninstall archived all 36 managed files. |

This probe verifies plugin installation, skill discovery, one agent activation, deterministic traceability
validation, and the workspace publisher lifecycle. It does not verify Natural compiler behavior, a real
SIFAP corpus, Java/Next.js builds, Azure access, deployment, GitHub mutations, or VS Code prompt execution.
The four prompt files passed static validation, but **Chat: Run Prompt** was not available through this CLI
probe and remains unverified.

The package changed after this probe on the same date: the `sifap-loop` and `adabas-postgresql-migration`
skills were added, `sifap-evolution` was split into `sifap-quality` and `sifap-operations`, and
`sifap-evolve` was replaced by `sifap-verify` and `sifap-operate`. The recorded skill count, agent name,
and the 36-file publisher lifecycle figure describe the pre-change package and were not re-probed. The
standard-library traceability, workspace-publisher, and loop-graph tests were re-run against the current
package and passed.

The package was then renamed from `mainframe-modernization` to `mainframe-natural-adabas` so the COBOL and
DB2 track could ship as the sibling `mainframe-cobol-db2` package. The install command recorded above uses
the retired name and was not re-probed; treat `copilot plugin install mainframe-natural-adabas@copilot-primitives`
as unverified until a new probe is recorded here.

The track-specific `sifap-workspace-kit` was replaced by the shared `modernization-workspace-kit`, whose
asset policy lives in each package's `workspace-kit.json`. The skill name recorded in the probe row above
is therefore retired. The publisher's sixteen standard-library tests were re-run against the refactored
engine and passed, and a full-profile preview produced 47 planned files for the Natural/Adabas package and
20 for the COBOL/DB2 package. Skill discovery through the CLI was not re-probed.

Two loop-free sibling packages were then added: `mainframe-natural-adabas-classic` and
`mainframe-cobol-db2-classic`. Each restores the original four-stage workshop (archaeology, architecture,
build, evolution) without the correction-loop skill or the engineering graph, keeps the split quality and
operations agents inside the evolution stage, and carries its own `workspace-kit.json`. Both packages were
static-validated with the nine repository gates, and a full-profile publisher preview planned 36 files for
the Natural/Adabas classic package and 17 for the COBOL/DB2 classic package. Neither classic package was
probed through GitHub Copilot CLI or VS Code, so plugin installation, agent discovery, and prompt
execution for them remain unverified.

## First-party customization documentation verification

Verification date: 2026-08-21. These checks fetched known first-party pages directly; they did not use
community sources or treat page availability as runtime proof.

| Area | First-party source | Verified guidance |
| --- | --- | --- |
| Repository instructions | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions | `.github/copilot-instructions.md` is repository-wide; `.github/instructions/**/*.instructions.md` is path-specific; both apply when matched. Repository instructions should be concise, general, and include project layout and working validation commands. |
| VS Code instructions | https://code.visualstudio.com/docs/agent-customization/custom-instructions | `.github/copilot-instructions.md` is always-on. File-based instructions use `.instructions.md`; multiple applicable files are combined without a guaranteed order. Start with one concise global file and add focused path-specific rules. |
| Custom agents | https://code.visualstudio.com/docs/agent-customization/custom-agents | Custom agents define task-specific personas, instructions, tool sets, optional subagent allow-lists through `agents`, model fallback arrays, visibility, and model-invocation controls. Workspace agents live under `.github/agents`; VS Code handoffs are guided transitions between agents. An explicit `agents` list requires the `agent` tool when `tools` is restricted. |
| Agent Skills | https://code.visualstudio.com/docs/agent-customization/agent-skills | Skills are portable on-demand packages. `name` must be kebab-case, no more than 64 characters, and match the parent directory; `description` must state what and when and is no more than 1024 characters. |
| GitHub Copilot plugins | https://docs.github.com/en/copilot/concepts/agents/about-plugins and https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference | An installable plugin can contain agents, skills, hooks, MCP server configurations, and LSP server configurations. The documented component fields do not include repository instructions or VS Code prompt files; those assets must still be published to their repository discovery paths when needed. |
| Prompt files | https://code.visualstudio.com/docs/agent-customization/prompt-files | Prompt files are manually invoked local VS Code slash commands. Agent Host does not use them. Supported metadata includes `description`, `name`, `argument-hint`, `agent`, `model`, and `tools`; unavailable tools are ignored. This repository therefore uses stable generic aliases or an intentional tool set instead of retaining historical environment-specific IDs. |
| VS Code agent tools | https://code.visualstudio.com/docs/agents/run/tools | The current tools picker is the authoritative inventory for a profile. Custom agents and prompts can restrict tools; built-in, MCP, extension, and tool-set availability is environment-specific. VS Code limits one request to 128 enabled tools and recommends selecting only relevant tools. |
| VS Code approvals and permissions | https://code.visualstudio.com/docs/agents/run/approvals | Permission levels are session controls, not primitive frontmatter. VS Code documents Default Approvals, Assisted permissions, Bypass Approvals, and Autopilot plus tool, URL, terminal, sandbox, and managed-policy controls. Managed rules can still block operations under Bypass Approvals or Autopilot. |
| Hooks | https://docs.github.com/en/copilot/reference/hooks-reference | Hooks are supported by Copilot CLI and cloud agent. Repository configs live under `.github/hooks/*.json`; cloud agent runs in an ephemeral Linux environment and honors `bash` or `command`, not PowerShell. |
| GitHub custom-agent tools | https://docs.github.com/en/copilot/reference/custom-agents-configuration | GitHub documents `execute`, `read`, `edit`, `search`, `agent`, `web`, and `todo` aliases and ignores unrecognized names. This conflicts with measured Copilot CLI 1.0.81-0 behavior for `search`, `web`, and `todo`, so cross-surface agents continue using the measured CLI-safe spellings; VS Code-only prompts use the current VS Code aliases. |

The pages did not expose a product version in the fetched content. Recheck them when a target product
version changes, local evidence conflicts, a claim is unverified, the user asks for current behavior, or
this evidence is older than 90 days. Do not refresh this date without repeating the fetch and reviewing
the relevant sections.

## Agent Skills compatibility field verification

Verification date: 2026-08-25. Trigger: the repository harness spec listed `compatibility` as an
unrecognized top-level key while imported Azure skill packages used it, so local sources conflicted.

| Source | Fetched | Result |
| --- | --- | --- |
| https://agentskills.io/specification | 2026-08-25 | `compatibility` is an optional standard frontmatter field, maximum 500 characters, for environment requirements such as intended product, required system packages, or network access. The standard field set is `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. |
| https://code.visualstudio.com/docs/agent-customization/agent-skills | 2026-08-25 | The VS Code header reference documents `name`, `description`, `argument-hint`, `user-invocable`, `disable-model-invocation`, and experimental `context`. It does not list `compatibility`. Page footer showed a 2026-08-19 edit date. |

Local divergence and resolution: `compatibility` is valid in the portable standard but is not acted on
by the current VS Code surface, and BUNDLE generation guidance does not mention it. This repository now
accepts the field with the 500-character bound in
`harness/github-copilot/skills/skill-creator/scripts/validate_skill.py` and
`harness/github-copilot/scripts/validate_primitives.py`, and requires any blocking prerequisite to also
appear in the skill body. Covered by `harness/github-copilot/skills/skill-creator/scripts/test_validate_skill.py`.

Not verified: whether GitHub Copilot CLI or the cloud agent surfaces `compatibility` to users. No
runtime probe was run for this field.

## Open Horizons 2.0.0 aggregate plugin runtime verification

Verification date: 2026-08-25. Target runtime: GitHub Copilot CLI 1.0.81-9. The probe used a
new temporary `COPILOT_HOME`; the live user configuration was not modified and no agent or model was
invoked.

| Evidence | Verified result |
| --- | --- |
| Local marketplace registration and `copilot plugin install open-horizons-platform@copilot-primitives` | The package installed successfully from the local marketplace, was enabled as version 2.0.0, and was loaded live from `harness/github-copilot/plugins/open-horizons-platform`. |
| `copilot skill list --json` | Discovery exposed `open-horizons-backstage-aeg-feature`, the product-qualified `open-horizons-backstage-authentication`, and `open-horizons-workspace-kit`. This verifies representative renamed and new skills without relying on a hand-maintained count. |
| `copilot mcp list` | The installed package exposed `microsoft-docs` over HTTP and local `azure`, `terraform`, and `playwright` servers from the portable MCP manifest. The commands behind those local servers were not started by this probe. |
| AEG contract validator | Eight expected operations passed identity-field exclusion, mutation classification, minimum evidence-run, bearer-security, and `worker_engine: inherit` checks. |
| Safety hook tests | Ten direct payload tests passed for read-only AEG access, mutating AEG approval, literal-secret denial with redaction, environment-variable acceptance, protected portal approval, equivalent Windows-path handling, safe infrastructure planning, approval-required infrastructure mutation, and broad recursive filesystem protection. |
| Workspace-kit tests | Seventeen standard-library tests passed for focused AEG publication, dry-run behavior, idempotence, transaction-wide conflict blocking, injected install, uninstall, and partial-uninstall state-commit rollback, retired-path reconciliation, reversible archive behavior, modified-file preservation, profile switching, MCP translation, target-specific workflow exclusion, blocking dry-run exit codes, and handled transaction errors without tracebacks. |

The probe supports package-level runtime verification for local installation, skill discovery, and MCP
exposure. It does not prove remote AEG authentication or authorization, AEG tool execution, custom-agent
invocation, MCP subprocess startup, or VS Code prompt execution; those remain environment-specific runtime
checks.

## Official architecture icon and diagram guidance verification

Verification date: 2026-08-25. Target: `azure-draw-io-diagram-generator` icon policy and its
`sdd-requirements-engineer` integration. These checks verified first-party documentation; they did not
grant permission beyond each source's stated terms or visually certify any user-supplied asset.

| Area | First-party source | Verified result |
| --- | --- | --- |
| Architecture diagram quality | [Azure Well-Architected Framework diagram guidance](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-diagrams) | Effective diagrams are audience- and question-specific, use standard notation and directional arrows, label entities and non-obvious relationships, remain accurate, include metadata and legends, support accessibility, use progressive disclosure, live under version control, and use current official icons and service names without arbitrary stretching or recoloring. |
| Azure icons | [Azure Architecture Center icons](https://learn.microsoft.com/en-us/azure/architecture/icons/) | Microsoft permits the supplied icons for architecture diagrams, training materials, or documentation. The page requires nearby product names and prohibits cropping, flipping, rotating, distortion, and using Microsoft product icons to represent another product. The page reports an icon update in July 2026. |
| Microsoft product families | [Microsoft Entra](https://learn.microsoft.com/en-us/entra/architecture/architecture-icons), [Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/icons), [Power Platform](https://learn.microsoft.com/en-us/power-platform/guidance/icons), and [Dynamics 365](https://learn.microsoft.com/en-us/dynamics365/get-started/icons) | Each page publishes a product-specific official set and comparable no-modification terms. Entra additionally prohibits marketing use. Dynamics reports removal of deprecated icons in its January 2026 package. The Microsoft 365 icon page now redirects to archived, retired documentation, so it is treated as a fallback rather than a current preferred source. |
| General Microsoft marks | [Microsoft Trademark and Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks) | Microsoft identifies logos, app icons, and product icons as proprietary brand assets and states that many uses require a license. The architecture-icon permission is therefore not generalized to arbitrary corporate-logo or marketing use. |
| GitHub icons and marks | [Primer Octicons](https://github.com/primer/octicons), [GitHub logo guidance](https://brand.github.com/foundations/logo), and [GitHub Copilot brand guidance](https://brand.github.com/brand-identity/copilot) | Octicons are GitHub-built SVG interface icons under the repository's MIT code license, but GitHub logos and product lockups remain governed by brand and trademark rules. Permitted logo use must not imply affiliation or endorsement and must not modify the mark. GitHub states that the former standalone Copilot logo has been deprecated since 2025. |

The general-purpose canonical `azure-draw-io-diagram-generator` now owns service-map rendering, safe
local SVG embedding, recognized first-party source and terms validation, SHA-256 verification,
external-image rejection, accessibility, and visual/brand review gates. The intentionally removed
`azure-architecture-diagrams` package is neither a source nor a dependency for this guidance.
`sdd-requirements-engineer` routes named Microsoft, Azure, and GitHub product diagrams to the general
generator while retaining Mermaid for concise vendor-neutral logical views. Product-specific plugins,
including Open Horizons, may consume the general skill through generated shared copies without becoming
its canonical owner.

## Frontend experience planning source verification

Verification date: 2026-08-25. Target: planning evidence for
`docs/specs/frontend-experience-plugin-plan.md`. No frontend plugin component or
runtime behavior was implemented or probed by this check.

| Area | Official source | Verified result |
| --- | --- | --- |
| WCAG and ARIA | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [ARIA APG](https://www.w3.org/WAI/ARIA/apg/) | The planning fetch initially received HTTP `403`. During implementation on 2026-08-25, both first-party URLs were fetched successfully through the approved repository web-fetch path. WCAG 2.2 remains the normative target, and APG remains pattern guidance for roles, states, properties, and keyboard support; no criterion or conformance claim was changed by this access recheck. |
| Responsive design and data entry | [Responsive design](https://web.dev/learn/design/) and [data entry](https://web.dev/learn/forms/) | The official courses cover layout at macro and micro levels, internationalization, typography, images, theming, accessibility, interaction, input help, autofill, privacy, usability testing, and cross-device testing. |
| Web performance | [Web Vitals](https://web.dev/articles/vitals) | LCP, INP, and CLS are listed as stable Core Web Vitals. The documented good thresholds are `2.5s`, `200ms`, and `0.1` at the 75th percentile, segmented by mobile and desktop. The page reports last update 2024-10-31. |
| Device design systems | [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/), [Material 3](https://m3.material.io/), and [Fluent 2](https://fluent2.microsoft.design/) | Apple HIG exposes principles, foundations, patterns, components, and input guidance; Material 3 exposes M3 Expressive and 2026 updates; Fluent 2 exposes web, iOS, Android, and Windows components. These are design-system sources, not universal normative standards. |
| Search and structured data | [SEO starter guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) and [structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | Google documents people-first content, descriptive titles and snippets, canonical handling, crawlable resources, and no ranking guarantee. JSON-LD is recommended when practical; markup must match visible content, and valid markup creates eligibility rather than guaranteed rich results. Both pages report last update 2025-12-10. |
| Robots and sitemaps | [Robots guidance](https://developers.google.com/search/docs/crawling-indexing/robots/intro) and [sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview) | `robots.txt` manages crawling but is not a confidentiality or reliable deindexing mechanism. A sitemap can improve discovery but does not guarantee crawling or indexing. Both pages report last update 2025-12-10. |
| HTML metadata | [HTML link types](https://html.spec.whatwg.org/multipage/links.html) | The HTML Living Standard defines `canonical`, `icon`, and `manifest`; it reports last update 2026-08-25. Scalable icons may use `sizes="any"`, while declared bitmap sizes must exist in the resource. |
| Social metadata | [Open Graph](https://ogp.me/) | Open Graph identifies `og:title`, `og:type`, `og:image`, and `og:url` as basic required properties and recommends structured image metadata including alternative text. It does not define a universal preview-image dimension. |
| API contracts | [OpenAPI 3.2.0](https://spec.openapis.org/oas/v3.2.0.html), [GraphQL September 2025](https://spec.graphql.org/September2025/), and [AsyncAPI 3.1.0](https://www.asyncapi.com/docs/reference/specification/v3.1.0) | OpenAPI 3.2.0 was published 2025-09-19; GraphQL has a September 2025 release and a separate June 2026 working draft; AsyncAPI reports 3.1.0. The plan therefore detects and preserves the consuming project's declared contract version. |
| Frontend tests | [Playwright](https://playwright.dev/docs/intro), [visual comparisons](https://playwright.dev/docs/test-snapshots), [accessibility testing](https://playwright.dev/docs/accessibility-testing), [Vitest](https://vitest.dev/guide/), [Testing Library](https://testing-library.com/docs/), and [Storybook testing](https://storybook.js.org/docs/writing-tests) | Playwright supports Chromium, Firefox, and WebKit and warns that screenshot rendering depends on the execution environment. Its accessibility guide requires manual testing in addition to automation. Vitest reports Vite 6 and Node 20 minimums; Testing Library prioritizes user-like tests; Storybook documents browser component, interaction, accessibility, and visual tests without treating 100 percent coverage as the goal. |
| Mocking and contract tests | [MSW](https://mswjs.io/docs/) and [Pact](https://docs.pact.io/) | MSW 2.0 documents reusable REST, GraphQL, and WebSocket interception in browser and Node. Pact distinguishes consumer-driven interaction contracts from schema-only provider conformance. |
| Playwright MCP pin | npm registry package `@playwright/mcp` and [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | `npm view` returned version and latest tag `0.0.79`, Microsoft repository provenance, and Apache-2.0. `npx -y @playwright/mcp@0.0.79 --help` ran successfully and exposed `--headless` and `--isolated`. This proves package metadata and command parsing only, not plugin discovery or browser behavior. |
| VS Code workspace MCP companion | [Microsoft Learn MCP server configuration for VS Code](https://learn.microsoft.com/dotnet/ai/quickstarts/build-mcp-server#configure-the-mcp-server) | The first-party example uses `.vscode/mcp.json` with a top-level `servers` object and a `stdio` server containing `command` and `args`. The frontend setup template therefore translates the portable plugin configuration into that shape and merges only `servers.playwright`; it does not copy the plugin `mcp.json` byte-for-byte or replace other workspace servers. |

## Frontend experience installed-plugin runtime verification

Verification date: 2026-08-25. Target runtime: GitHub Copilot CLI 1.0.81-9. The isolated
home was stored under the session artifact directory; the live user `~/.copilot` configuration was
not modified.

| Evidence | Verified result |
| --- | --- |
| `COPILOT_HOME=<session-artifact> copilot plugin marketplace add /Volumes/T9/copilot-primitives` and `copilot plugin install frontend-experience@copilot-primitives` | The local marketplace registered successfully and the `frontend-experience` 0.1.0 plugin installed and enabled. The CLI reported a live local-marketplace mount from `harness/github-copilot/plugins/frontend-experience`. |
| `copilot plugin list` | The isolated marketplace listed `frontend-experience@copilot-primitives` version 0.1.0 as enabled. Other marketplace entries remained disabled. |
| `copilot skill list` | Plugin discovery exposed exactly 19 declared skills: the 16 new frontend skills plus `anti-ui-slop`, `playwright-explore-website`, and `playwright-generate-test`. |
| `copilot mcp list` | The plugin exposed `playwright (local)` from the pinned `@playwright/mcp@0.0.79` configuration. The aggregate experimental `copilot plugins list` command was unavailable in the isolated configuration even though the binary help listed it, so skill and MCP discovery were verified through their stable dedicated commands. |
| Minimal non-interactive invocations of `frontend-product-designer`, `frontend-experience-engineer`, and `frontend-qa-engineer` | All three installed agents resolved by qualified plugin name and returned the requested probe response. |
| Effective tool-boundary probes | `frontend-product-designer` and `frontend-qa-engineer` could not create sentinel files and reported no edit capability. `frontend-experience-engineer` created an explicitly requested HTML fixture with the edit tool. The probe file was inspected and removed. |
| Playwright MCP browser probe through `frontend-qa-engineer` | Against a disposable local page, the agent navigated successfully, captured before/after snapshots, activated a named button, captured a screenshot, read the console, and inspected network requests. The repeated clean run reported one informational console message, zero errors, `GET /` 200, `GET /status.json` 200, and verdict `Ready`. Temporary screenshots were removed from the plugin directory after the probe. |
| `frontend-project-setup` lifecycle | Nine standard-library tests passed: dry-run, apply/idempotency, conflict with no partial writes, explicit force, conditional discoverability publication, MCP named-entry merge, modified-file preservation, traversal/symlink rejection, and interrupted-write rollback. A separate disposable Next.js fixture then completed CLI dry-run, approved apply with VS Code MCP, repeated apply with all eight actions `unchanged`, strict validation of three rendered instructions plus four rendered prompts, pinned MCP JSON inspection, and approved uninstall that removed the owned `.github` and `.vscode` trees cleanly. |
| `frontend-release-quality-gate` unit tests | Six standard-library tests passed: every supported result state, CLI JSON output, missing/duplicate IDs, unsupported results, valid path evidence, and missing/escaping evidence rejection. |
| Representative pilot matrix under the session artifact directory | Synthetic Next.js public content, React/Vite dashboard, Vue/Nuxt form, React Native/Expo chat, and Electron workflow fixtures were inspected. Stack detection and skill routing matched each scenario. The web pilots produced traceable `US`/`AC`/`SC` chains and concrete implementation gaps. Expo QA loaded mobile/desktop, accessibility, conversational, and test-strategy skills and returned `Blocked` for missing implementation plus simulator/device/VoiceOver/TalkBack evidence. Electron QA loaded mobile/desktop, backend-integration, accessibility, and release-gate skills and returned `Blocked` for missing menu, shortcut, file-dialog, IPC validation, offline, packaging, and high-contrast evidence. These results validate routing and gap reporting, not full native or desktop implementation support. |
| Frontend package link audit | `check_links.py --path harness/github-copilot/plugins/frontend-experience` reported eight public URLs OK and one anonymous `404` for the manifest repository URL. Authenticated `gh repo view paulasilvatech/copilot-primitives` confirmed that exact URL and classified the repository as `PRIVATE`; the anonymous result is an access boundary, not a broken manifest target. |
| VS Code companion prompt execution | Strict validation passed for all four rendered prompts and three rendered instructions after transactional publication into a disposable fixture. Representative **Chat: Run Prompt** execution was not available through this CLI runtime and remains open evidence; prompt execution behavior is not counted as verified. |

The representative probe supports repository assurance classification as `runtime-verified` for package
installation, component discovery, agent activation, tool boundaries, and the tested Playwright web flow.
It does not upgrade unexecuted mobile, desktop packaging, native accessibility, framework build, or VS Code
prompt profiles to verified support.

## Harness namespace, capability, and composition verification

Verification date: 2026-08-21. Target runtime: GitHub Copilot CLI 1.0.81-4.

| Evidence | Verified result |
| --- | --- |
| Canonical relocation to `harness/github-copilot/` | The shared source tree moved without a compatibility symlink or duplicate canonical tree. Repository `.github/` paths remain generated runtime surfaces. All active path references use the new namespace; historical evidence in this file remains unchanged. |
| Strict validation with Python 3.13 and no PyYAML | The fallback frontmatter parser successfully parsed every shared agent, skill, and prompt, including nested `mcp-servers`, arrays, and mappings. Strict validation reported 225 agents, 194 instructions, 421 skills, 48 prompts, 99 plugins, and 16 canonical/installed hook configs with zero errors or warnings. |
| `docs/PRIMITIVE-CAPABILITIES.md` | The static audit covered 239 canonical agents and 57 canonical prompts across shared and plugin-owned sources. It found zero fixed model pins, zero read-only agents inheriting all tools, zero legacy prompt tool names, and zero blocking findings. Forty-six environment-specific MCP, extension, or tool-set cases remain explicitly queued for runtime verification. |
| `docs/PRIMITIVE-REDUNDANCY.md` | The audit found zero exact duplicate groups and zero unclassified candidates. `conventional-commit` was consolidated into `git-commit`; Redis and Backstage shared skills now have one shared canonical source and generated Open Horizons package copies. Sixteen high-similarity pairs remain classified as language, framework, lifecycle, source-framework, or specialization variants. |
| Naming audit | Every shared agent, instruction, skill, prompt, plugin, hook, and plugin-owned agent/skill identifier uses lowercase kebab-case. The validator now rejects non-kebab agent, instruction, plugin, and hook identifiers. |
| Fresh isolated marketplace installation | All 99 marketplace entries installed successfully from the local repository into a new isolated `COPILOT_HOME`; `copilot plugin list` reported 99 installed packages. |
| New plugin probes | `agent-governance:agent-governance-reviewer` returned `governance-ok`; `github-actions-maintenance:github-actions-expert` returned `actions-ok`; the Qdrant plugin exposed all eight expected skills with `source: plugin`. |
| Renamed and mixed-source plugin probes | `fabric-agentic-plugin:fabric-admin` returned `fabric-ok`; `open-horizons-platform:deploy` returned `horizons-ok`. Open Horizons exposed shared `azure-managed-redis-cache` and `backstage-plugin-builder` as plugin skills while drift checks confirmed their package copies match the shared canonical sources. |
| Open Horizons safety payloads | A safe `terraform plan` payload produced no stdout. A `terraform apply` payload returned `permissionDecision: ask` with the expected approval reason. |
| VS Code prompt runtime | First-party prompt/tool/approval pages were reverified and static prompt metadata passed. **Chat: Run Prompt** was not run because no VS Code CLI or customization command was available to this client; environment-specific prompt tool sets remain in the capability audit runtime queue. |

## Body tool-token rule and capability authority verification

Verification date: 2026-08-24. Target runtime: repository validators only. No product version was probed,
so the CLI tool-token evidence recorded above is unchanged and its dates were not refreshed.

| Evidence | Verified result |
| --- | --- |
| Frontmatter-only coverage gap | Every body rule in `validate_primitives.py` (`AG018`-`AG021`, `IN010`-`IN013`, `SK013`-`SK016`, `PR006`-`PR008`) is structural and INFO level, so no gate inspected prose for tool tokens. `custom-agent-foundry.agent.md` taught `search`, `fetch`, `githubRepo`, `usages`, and `run_in_terminal` as literal `tools:` values and passed every check. |
| `AG024` (new, WARNING) | Scans the agent body for no-op or legacy tokens presented inside a usable tool list. A first pass produced 31 findings across 7 files; 26 of those were the correct pattern (tokens named in order to reject or historicize them) plus legitimate `microsoft.docs.mcp` MCP references. Adding a negative-context guard and excluding MCP server identifiers reduced the result to the 5 real tokens in `custom-agent-foundry.agent.md`. Fenced blocks are skipped so source samples and MCP `args` arrays containing `run` or `search` stay silent. |
| `AG024` negative test | A scratch agent declaring `tools: ["search"]` with a body list of `['search', 'githubRepo', 'usages']` raised `AG017` as ERROR and three `AG024` WARNINGs, then was removed. |
| Capability authority detection | `authority()` matched only the literal phrases `read-only policy`, `read-only reviewer`, `editing policy`, and `write policy`. Broadening it to imperative wording reclassified `java-mcp-expert.agent.md` from `unspecified` to `read-only`, exposing a read-only agent that inherited every tool. |
| Bounded-write review queue | No rule covered a bounded-write agent that declares no `tools:` allow-list. Forty-three agents are in that state. A tool allow-list cannot express a policy that scopes which files an agent may touch, so these are reported as `capability-review-required` rather than blocked, and each needs a recorded human decision. |
| Stale committed ledger | `docs/PRIMITIVE-CAPABILITIES.json` at `HEAD` recorded `tools: ['read', 'grep', 'glob', 'edit', 'execute', 'web_fetch', 'web_search']` for `plugins/backstage-expert/agents/backstage-expert.agent.md`, but the unmodified source declared `[execute, read, ms-vscode.vscode-websearchforcopilot/websearch, edit, search]`. The committed ledger was hiding a real `search` no-op token. |
| Gate suite after the change | All nine repository gates pass, including `validate_primitives.py --strict` with zero errors and zero warnings. Blocking capability findings went from a falsely reported 0 to 2 real findings, both fixed. |

## Plugin classification verification

Verification date: 2026-08-24. Repository classifiers and generators only; no product runtime was probed,
so no earlier runtime verification date was refreshed or reused as new evidence.

| Evidence | Verified result |
| --- | --- |
| Classification is not deletion | The redundancy audit reports zero exact duplicates and zero confirmed duplicates, and no package carries archive or supersession evidence. No agent, skill, prompt, plugin, or marketplace entry was removed; classification only annotates the generated audit and catalog. |
| Schema constraint | `plugin.json` rejects unsupported top-level keys through rule `PL007`, so maturity metadata cannot live in the distributed manifest. `keywords` was rejected as a carrier because it is a discovery taxonomy. Governance therefore lives in `harness/github-copilot/manifests/plugin-sources.json`, and `normalize_plugin_manifests.py` does not copy it into `plugin.json`. |
| Governance schema | `_plugin_sources.py` accepts only `lifecycle`, `lastRuntimeProbe`, and `evidence`; rejects `incubating` as an override because it is SemVer-derived; requires a `YYYY-MM-DD` probe date; requires evidence for a probe date; and requires evidence for a `deprecated` lifecycle. Twenty unit tests across `test_plugin_sources.py` and `test_plugin_governance.py` pass. |
| Probe freshness | The classifier treats a representative probe as `runtime-verified` for 90 days. A unit test pins the boundary: the same 2026-08-22 probe classifies as `runtime-verified` on 2026-11-20 and `runtime-stale` on 2026-11-21. |
| Evidence selection | Only the 2026-08-22 flat-layout probes were used, because the 2026-08-20 namespaced probes are explicitly superseded by that verification. `backstage-expert` (`flat-agent-ok` plus a hook denial), `awesome-copilot` (direct agents and skills with an exposed MCP server), and `aws-cloud-development` (`flat-aws-ok`) are recorded. |
| Install is not runtime proof | `backlog-swipe-triage` and `accessibility-kanban` installed successfully, but interactive client-extension behavior was not exercised. They are not recorded as probed and remain `runtime-required`, alongside every other package that ships MCP servers, hooks, or extensions without a current probe. |
| Generated distribution | 100 plugins classified: 96 active and 4 incubating (`context-matic`, `fastah-ip-geo-tools`, `signals-dashboard`, `the-workshop`); 0 deprecated; 3 runtime-verified, 27 runtime-required, 70 static-validated, 0 runtime-stale; 24 upstream-mirror and 76 repository provenance. |
| Plugin-owned primitives were never validated | Every `validate_*` method globbed only its flat tree, so plugin-owned components under `plugins/<name>/` never ran their rule sets: 15 agents, 11 prompts, 18 instructions, and 57 skills, or 101 files in total. That is why the `search` token in `backstage-expert.agent.md` survived; only the capability audit covered it. A shared `plugin_owned_files()` helper now feeds all four validators for plugins whose `componentSource` is `plugin`, raising the counts from 225 to 240 agents, 48 to 59 prompts, 194 to 212 instructions, and 420 to 474 skills. Skills listed in `sharedSkills` are excluded because they are copies generated from an already-validated canonical source, which is why 57 files on disk yield 54 validated skills. Every newly covered file passed with zero errors and zero warnings, so the gap was coverage rather than defect. |
| Plugin-owned coverage negative test | A scratch agent placed under `plugins/fabric-agentic-plugin/agents/` with `tools: ["search"]` and a body list of `['codebase', 'usages', 'githubRepo']` raised one `AG017` ERROR and three `AG024` WARNINGs, then was removed. The same file produced no findings before the scope change. |
| Capability review queue closed | All 42 queued agents received an explicit allow-list derived from their stated editing policy and body evidence. `arm-migration.agent.md` and `apify-integration-expert.agent.md` declare `mcp-servers`, so their lists retain `custom-mcp/*` and `apify/*` respectively; omitting those would have removed MCP capability. `caveman-mode.agent.md` states that full tool access is intentional and therefore records `tools: ["*"]`. Frontmatter parsed cleanly for all 240 agents afterwards. |
| Cross-surface web access | `backstage-expert.agent.md` declared only `ms-vscode.vscode-websearchforcopilot/websearch`, a VS Code extension tool that grants nothing in the CLI, while its workflow and Definition of Done both require first-party documentation verification. It now also declares `web_fetch` and `web_search`. |

## Backstage Expert source and capability verification

Verification date: 2026-08-21. Source application: Backstage `1.54.0-next.3`. Exact reviewed
Backstage commit: `eeac444a9aba7c107525d2a726851e907418c181`. Exact reviewed community-plugins
commit: `dc925a35a9064df8a12028244bfa3f172f5d1d95`.

| Area | First-party source | Verified result |
| --- | --- | --- |
| Upstream repository and contributor contract | https://github.com/paulasilvatech/backstage at `eeac444a9aba7c107525d2a726851e907418c181`; root `package.json`, `CONTRIBUTING.md`, and Apache-2.0 files | The checkout identifies `https://github.com/backstage/backstage`, version `1.54.0-next.3`, `yarn@4.8.1`, Node.js `22 || 24`, Apache-2.0, targeted tests with `CI=1 yarn test <path>`, exact root `yarn tsc`, changed-file formatting, `yarn lint --fix`, `yarn build:api-reports`, `yarn start`, and `yarn new`. Root build, release, and changeset-version mutations are not routine contribution checks. |
| Official AI skills | https://backstage.io/docs/ai/skills and https://backstage.io/docs/ai/well-known-skills | The published well-known set contains six skills: `app-frontend-system-migration`, `plugin-new-frontend-system-support`, `plugin-full-frontend-system-migration`, `mui-to-bui-migration`, `plugin-analytics-instrumentation`, and `onboard-to-openapi-server`. The plugin imports exact snapshots under adapter references with SHA-256 provenance. |
| AI catalog model | https://backstage.io/docs/ai/ai-in-the-catalog | `@backstage/plugin-catalog-backend-module-ai-model` provides `AiResource` skill and rule entities plus the `mcp-server` API subtype. Skill or rule content remains at `backstage.io/source-location`; MCP APIs declare transport remotes. |
| Actions Registry and MCP Actions | https://backstage.io/docs/ai/mcp-actions, https://backstage.io/docs/ai/well-known-actions, and the exact source files `docs/backend-system/core-services/actions*.md` | `@backstage/plugin-mcp-actions-backend` exposes registered actions as MCP tools. Action schemas separate secrets, conservative defaults treat unspecified actions as mutating, attributes describe destructive/read-only/idempotent behavior, filters support IDs and attributes, namespaced tools avoid collisions, permissions restrict visibility, and focused servers may expose separate action sets. The documented well-known action list is non-exhaustive. |
| Authentication | https://backstage.io/docs/auth/, https://backstage.io/docs/auth/github/provider, and https://backstage.io/docs/auth/microsoft/provider | Backstage authentication separates sign-in identity from delegated third-party access. GitHub uses `/api/auth/github/handler/frame` and `@backstage/plugin-auth-backend-module-github-provider`; Microsoft Entra ID uses `/api/auth/microsoft/handler/frame` and `@backstage/plugin-auth-backend-module-microsoft-provider`. Resolver mapping, scopes, secrets, and technical integration credentials remain separate concerns. |
| Kubernetes | https://backstage.io/docs/features/kubernetes/, installation, configuration, and permissions pages | The service-owner feature uses `@backstage/plugin-kubernetes` and `@backstage/plugin-kubernetes-backend`. Cluster and service locators, auth providers, catalog annotations, TLS, metrics, custom resources, and `kubernetes.clusters.read`, `kubernetes.resources.read`, and `kubernetes.proxy` permissions require explicit configuration. Catalog entities must not store service-account tokens. |
| Notifications and signals | https://backstage.io/docs/notifications/, `/usage`, and `/processors` | New frontend documentation is the default. Notifications and Signals are part of create-app from 1.42.0, while navigation and optional settings still require app wiring. Backend plugins use `@backstage/plugin-notifications-node`; external services use authenticated REST. Signals provide optional real-time updates, and processors route to channels such as email or Slack. |
| Permissions | https://backstage.io/docs/permissions/overview and exact permission integration sources | Authentication does not authorize actions. Plugins declare basic or resource permissions, enforce them in the backend, and apply conditional filters before returning resources. In-memory `apply` and query `toQuery` rules must be logically equivalent. |
| Search | https://backstage.io/docs/features/search/ and `/getting-started` | Search separates frontend result extensions, backend engines, and collators. Current new-frontend setup uses feature discovery, result/filter blueprints, engine modules, bounded collator schedules, and Catalog or TechDocs collators. |
| External integrations | https://backstage.io/docs/integrations/, GitHub App, Azure locations/discovery pages, and https://github.com/backstage/community-plugins at `dc925a35a9064df8a12028244bfa3f172f5d1d95` | GitHub core modules cover integrations, catalog discovery, org ingestion, events, and scaffolder publication. Azure modules cover Azure DevOps locations, discovery, events, and `publish:azure`; the active community Azure DevOps UI package was `0.33.0`. Active ServiceNow community packages were frontend `1.14.0`, backend `1.13.1`, and scaffolder module `2.16.1`. |
| Framework reference | https://backstage.io/docs/framework/generated-index, https://backstage.io/api/stable, and exact `docs/backend-system/core-services/` sources | The generated index is a navigation surface, not sufficient API detail. Plugin decisions use the target release's stable API reference, core service definitions, frontend blueprints, and exported extension points; alpha APIs require exact-version evidence. |
| Deterministic upstream import | `import_backstage_upstream.py`, 30 focused unit tests, and `PROVENANCE.json` | The importer verified repository identity, exact commit, clean checkout, Apache-2.0 license, allow-listed files, atomic writes, symlink and path-escape rejection, missing and stray-file detection, optional index removal, local NOTICE fallback, and no-write `--check`. The real pinned checkout reported current with nine imported files. |
| Isolated Agent Plugins runtime | Fresh `COPILOT_HOME` under the session artifact directory | The local marketplace registered as `copilot-primitives`; `backstage-expert@copilot-primitives` installed as version `1.0.0` with 26 skills. `copilot skill list --json` reported all 26 with `source: plugin`, and `--agent backstage-expert:backstage-expert` returned `backstage-ok`. |
| Safety hook and workspace kit | Installed plugin package in the isolated `COPILOT_HOME` | A safe targeted test payload emitted no hook output; create-app emitted `permissionDecision: ask`; malformed audit and disabled modes emitted no decision. The installed workspace kit planned 13 files, applied them, reported all 13 unchanged on a second plan, planned and completed clean uninstall, rejected a conflict with exit 2, and wrote no state on conflict. |
| VS Code prompts | Static prompt validation and capability audit | Both plugin prompts passed structural and tool-alias checks. **Chat: Run Prompt** was not available from this CLI client and was not run; static validation is not runtime proof. |

The Firecrawl MCP endpoint rejected the request because its token was invalid. All URLs above were
therefore fetched directly from their known first-party locations, and repository sources were
read from exact commits. This fallback did not send private repository content to third parties.

## Flat GitHub Copilot plugin layout verification

Verification date: 2026-08-22. Target runtime: GitHub Copilot CLI 1.0.81-4.

| Evidence | Verified result |
| --- | --- |
| https://docs.github.com/en/copilot/concepts/agents/about-plugins | GitHub documents plugin components directly at the plugin root: agents in `agents/`, skills in `skills/`, hooks as root `hooks.json` or under `hooks/`, MCP configuration at the root, and manifest component paths. |
| https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating | The current first-party authoring example omits `$schema` and declares `agents`, `skills`, `hooks`, and `mcpServers` directly in `plugin.json`. |
| https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference | Without the Agent Plugins `$schema`, GitHub Copilot CLI supports direct component path fields and defaults agents and skills to `agents/` and `skills/`. |
| https://agent-plugins.org/specification | Portable Agent Plugins 1.0 standardizes only skills and MCP servers. Reverse-domain client extension directories are permitted for client-specific behavior but are not required by the portable core. |
| Isolated flat `backstage-expert` copy | With `$schema` and `com.github.copilot/` removed, the plugin installed 26 skills, resolved `backstage-expert:backstage-expert`, returned `flat-agent-ok`, and its direct `hooks/backstage-safety/hooks.json` blocked a simulated create-app command. |
| Isolated flat `awesome-copilot` copy | Direct `agents/` and `skills/` loaded, and `mcpServers: "mcp.json"` exposed the `awesome-copilot` server with `source: plugin` while preserving the portable `stdio` configuration. |
| Isolated flat `backlog-swipe-triage` copy | The extension-only plugin installed successfully with `extensions/backlog-swipe-triage` declared directly and no namespaced mirror. |
| Repository-wide migration | All 100 manifests use the flat GitHub Copilot contract. Shared-source ownership moved to `harness/github-copilot/manifests/plugin-sources.json`. No `com.github.copilot/` directory remains under the plugin tree. |
| Full isolated marketplace installation | All 100 entries installed successfully into one fresh `COPILOT_HOME`. The installed packages contained zero namespaced directories, 53 direct agent directories, 72 direct skill directories, three direct hook directories, and 24 direct extension directories. Runtime discovery reported 238 plugin skills and eight plugin MCP servers. |
| Representative runtime probes | `aws-cloud-development:aws-principal-architect` returned `flat-aws-ok`; the direct Backstage hook denied an approval-gated create-app command; the extension-only Backlog Swipe package retained its direct extension entry point after install. |

The namespaced Agent Plugins probes recorded on 2026-08-20 below remain valid observations about
schema-declaring packages, but they no longer define this repository's package architecture. The
2026-08-22 flat-layout verification supersedes that design choice for all managed marketplace plugins.

## Historical Open Horizons namespaced-layout verification

Verification date: 2026-08-20. Target runtime: GitHub Copilot CLI 1.0.81-0.

This section records the previously tested schema-declaring layout. It is retained as historical
runtime evidence and is superseded by the flat-layout verification above.

| Evidence | Verified result |
| --- | --- |
| https://github.com/Ohorizons/open-horizons-platform/commit/7858578302fe0f54fdb43e15f84b14fd5d7519c2 | This was the upstream `main` commit inspected while refreshing the packaged workspace customizations. The plugin intentionally adds package metadata, MCP configuration, harness documentation, and runtime portability fixes that do not exist in the upstream `.github/` tree. |
| `copilot plugin --help`, `copilot plugin install --help`, and `copilot mcp --help` | The installed CLI supports marketplace and repository plugin installation. MCP configuration is loaded from user, workspace, and installed-plugin sources; local servers use `type: local`, while remote servers use `type: http` or `type: sse`. |
| Isolated marketplace install with `COPILOT_HOME=<session-artifact>` | `open-horizons-platform@copilot-primitives` installed successfully, reported 30 skills, and exposed `microsoft-docs`, `azure`, `terraform`, and `playwright` as plugin MCP servers. The representative invocation `--agent open-horizons-platform:deploy` returned `ok` after agents were mirrored under `com.github.copilot/agents/`. |
| GitHub Copilot CLI debug log for the schema-declaring plugin | A top-level legacy `agents` field emitted: `agents are read only from "com.github.copilot/agents"` and was ignored. Moving generated copies to that extension directory loaded the namespaced agents. |
| Isolated schema-declaring hook probe | A root `hooks/hooks.json` did not fire. Moving the identical config to `com.github.copilot/hooks/hooks.json` produced one observable `sessionStart` event, proving the GitHub extension hook path for Agent Plugins 1.0. |
| Open Horizons hook payload and workspace-kit tests | The safety hook passed safe, ask, malformed, disabled, and non-execution payload cases. The workspace-kit publisher passed dry-run, apply, idempotent, conflict-with-no-write, and explicit-force cases. |
| Isolated Open Horizons 1.1.0 marketplace install and simulated high-impact command | The install reported 30 skills and four MCP servers. `open-horizons-platform:deploy` attempted only `printf '%s\n' 'terraform apply simulation'`; the installed `preToolUse` hook emitted `permissionDecision: ask`, and the non-interactive runtime denied the command because it could not ask the user. No Terraform command ran. |
| `npm view @azure/mcp version` and `npx -y @azure/mcp@3.0.0-beta.36 server start --help` | `3.0.0-beta.36` was the published `latest` tag and the configured startup command parsed successfully. |
| `npm view @playwright/mcp version` and `npx -y @playwright/mcp@0.0.79 --help` | `0.0.79` was the published `latest` tag and the configured startup command parsed successfully. |
| https://github.com/hashicorp/terraform-mcp-server/releases/tag/v1.2.0 and `docker manifest inspect hashicorp/terraform-mcp-server:1.2.0` | Release `v1.2.0` was latest and the pinned Docker image tag existed. |

The imported Open Horizons manifest had been an unrelated copy of the `noob-mode` manifest, referenced a
missing skill, was absent from the marketplace, and left every packaged agent and skill unreferenced.
The package was corrected to install its own nine agents, 30 skills, one safety hook, and four MCP
servers. Repository-only instructions, prompts, workflows, issue forms, and templates remain in the
package as a workspace kit and are published only through an explicit dry-run/apply workflow.

## Historical marketplace-wide Agent Plugins verification

Verification date: 2026-08-20. Target runtime: GitHub Copilot CLI 1.0.81-4.

This section records the earlier namespaced migration and its then-current counts. It is retained
for traceability and is superseded by the 2026-08-22 flat-layout verification.

| Evidence | Verified result |
| --- | --- |
| https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating | GitHub documents agents, skills, hooks, and MCP server configurations as plugin components and requires reinstalling a local plugin to refresh cached content. |
| https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference | The legacy GitHub manifest supports component path fields. Declaring the canonical `$schema` opts into Agent Plugins 1.0 semantics; the `extensions` field then has client-specific meaning. |
| https://agent-plugins.org/specification | Agent Plugins 1.0 fixes skills at `skills/` and portable MCP configuration at root `mcp.json`; client-specific content belongs under reverse-domain namespaces. |
| https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace | Marketplace entries require name, description, version, and a source relative to the repository. The marketplace file belongs under `.github/plugin/`. |
| https://docs.github.com/en/copilot/reference/hooks-reference | Hooks remain supported in GitHub Copilot CLI and cloud agent. Hook commands must be bounded, deterministic, and explicit about blocking behavior. |
| `azure-cloud-development@copilot-primitives` before migration | The plugin installed four skills, but GitHub Copilot CLI warned that root `agents/` was ignored because `$schema` was present; its namespaced agent was unavailable. |
| `azure-cloud-development@copilot-primitives` after migration | The plugin installed four skills and `azure-cloud-development:azure-principal-architect` returned `ok` after agents were materialized under `com.github.copilot/agents/`. |
| `copilot plugin marketplace browse copilot-primitives` | The current CLI listed all 96 entries. Although the fetched plugin reference advertises `browse NAME [--json]`, CLI 1.0.81-4 rejected `--json`; the audit therefore uses the deterministic marketplace file rather than parsing CLI display text. |
| Awesome Copilot upstream commit `318066d2213b510e89b500ed0d53506c54093ddc` | At the time of this probe, the upstream materializer copied agents and client extensions into `com.github.copilot/`, kept skills in fixed `skills/`, and emitted a strict served manifest. Twenty-four client-extension packages were imported from this commit. |
| npm registry on 2026-08-20 | Imported extensions pin `@github/copilot-sdk` to `1.0.11-preview.2` and Playwright to `1.62.1`; the Power BI reference MCP is pinned to `0.5.0-beta.12`. |
| Extension validation | 212 JavaScript files passed `node --check`. Signals Dashboard passed 19 tests with one Windows-only skip; Java Modernization Studio passed its Node tests; PR Artifact Explorer passed 13 tests. Windows App Storage Inspector syntax passed, while its runtime self-test was not applicable on macOS because the extension intentionally fails outside Windows. |
| `accessibility-kanban@copilot-primitives` | The extension-only package installed successfully from the local marketplace on CLI 1.0.81-4. Interactive canvas behavior was not exercised in the non-interactive probe; client-extension packages remain covered by source/runtime mirror checks, pinned dependencies, JavaScript syntax, and available unit tests. |
| New package runtime probes | `pcf-development` installed one skill and its `power-platform-expert` agent returned `pcf-ok`. `fabric-agentic-plugin` installed one progressive Fabric skill, exposed two MCP servers, and its `FabricAdmin` agent returned `fabric-ok`. |
| Plugin authoring runtime probe | `copilot-plugin-development` installed the `copilot-plugin-authoring` skill, and its namespaced `copilot-primitive-architect` agent returned `plugin-authoring-ok`. |
| Full isolated marketplace installation | All 96 entries installed successfully into one fresh `COPILOT_HOME`; `copilot plugin list` reported all 96 installed packages. Component behavior remains covered by representative agent, skill, MCP, hook, and client-extension probes rather than assuming installation alone proves execution. |

At that verification point, the marketplace contained 96 self-contained entries. Seventy-two packages sourced agents and skills
from the shared library; 24 own plugin-local agents, hooks, or client extensions. All manifests use the
Agent Plugins 1.0 schema, legacy `.mcp.json` files were removed from runtime packages, every package is
listed exactly once, and deterministic audit results are generated in `docs/PLUGIN-AUDIT.md`.

## Power Apps Component Framework verification

Verification date: 2026-08-20.

| Source | Verified result |
| --- | --- |
| https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview | PCF code components support model-driven and canvas apps, package through solutions, and can become premium when they call external services directly from the browser. The page was dated 2026-01-09. |
| https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations | Canvas PCF does not expose every Dataverse-dependent API, custom authentication is unsupported in canvas components, browser web storage is insecure and unreliable, and connectors should be used for authenticated canvas operations. The page was dated 2025-07-01. |
| https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/ | The manifest schema remains the authoritative contract for component properties, resources, feature usage, and external-service declarations. |

## PowerPlatform Dataverse Client for Python verification

Verification date: 2026-08-19. Target: latest published GitHub release `v1.0.0`; repository `main`
declared version `1.0.1` in `pyproject.toml` at verification time. The instruction targets the shared
1.x GA contract rather than unreleased-only behavior.

| Source | Verified result |
| --- | --- |
| https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/client.py | The v0 shortcuts `create`, `get`, `update`, `delete`, and `upload_file` were removed in 1.0 GA. Access raises `AttributeError` with the namespaced replacement and migration command. |
| https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/operations/files.py | The public upload API is `client.files.upload(table, record_id, file_column, path, *, mode=None, mime_type=None, if_none_match=True) -> None`. |
| https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/data/_upload.py | Auto mode selects a single PATCH below 128 MiB and chunked PATCH at 128 MiB or above. Chunk mode uses the server's `x-ms-chunk-size` value or a 4 MiB fallback; no public `chunk_size` parameter exists. SDK 1.0 forwards `mime_type` only to the small path and sends chunk segments as `application/octet-stream`. |
| https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/operations/records.py | A single-dictionary `records.create` returns one GUID string. Multi-record `records.get` returns pages; `page_size` is the page hint and `top` caps the total number returned. |
| https://github.com/microsoft/PowerPlatform-DataverseClient-Python/blob/v1.0.0/src/PowerPlatform/Dataverse/core/errors.py | `HttpError` exposes `is_transient`, `retry_after`, status, correlation, request, and trace fields for bounded retry and diagnostics. |
| https://learn.microsoft.com/en-us/power-apps/developer/data-platform/file-column-data | The page was dated 2026-03-09. File bytes are handled separately from ordinary record create/update. The Dataverse block-message protocol uses blocks of 4 MB or less; it is distinct from the Python SDK's native chunked PATCH implementation. |

This verification found that the earlier `dataverse-python-file-operations` instruction described the
removed beta `client.upload_file(...)` API, invented a public `chunk_size` argument, treated a single
create result as a list, and used `top=5000` as if it were a page-size setting. The canonical instruction
was corrected to the 1.x GA contract.

## Non-interactive surface verified

Working commands/flags:

```bash
which copilot
copilot --version
copilot --help
copilot -p "/env" --allow-all --no-color --log-level debug --log-dir /Volumes/T9/harness-check/logs --no-remote
copilot -C /Volumes/T9/harness-check/ws -p "Reply only: ok" --allow-all --no-color --log-level debug --log-dir /Volumes/T9/harness-check/logs-tools-portable --no-remote --silent --agent portable-tools-test
copilot skill list --json
copilot plugin list
copilot plugin marketplace list
copilot plugin marketplace add /Volumes/T9/harness-check/ws
copilot plugin marketplace browse copilot-primitives
```

Relevant help output:

- `-p, --prompt <text>`: `Execute a prompt in non-interactive mode (exits after completion)`.
- `--allow-all-tools`: `required for non-interactive mode`.
- `--allow-all`: `equivalent to --allow-all-tools --allow-all-paths --allow-all-urls`.
- `--log-dir <directory>`, `--log-level <level>`, `--no-color`, `--deny-tool[=tools...]` are supported.
- Commands present in help: `plugin`, `plugins`, `skill`, `mcp`, `help`. However, `copilot plugins list` returned `The plugins command is not available.` in this install; `copilot plugin list` worked.

## Scratch workspace

Workspace: `/Volumes/T9/harness-check/ws`. It was initialized with `git init`, but project skill discovery also worked in `/Volumes/T9/harness-check/nogit` without a git repository:

```text
[{'name': 'csharp-nunit', 'source': 'project', 'path': '/Volumes/T9/harness-check/nogit/.github/skills/csharp-nunit', 'enabled': True}]
```

Sample contents copied under `.github/`:

- 12 agents: `CSharpExpert`, `Thinking-Beast-Mode`, `Ultimate-Transparent-Thinking-Beast-Mode`, `azure-iac-generator`, `context7`, `github-actions-expert`, `python-mcp-expert`, `plan`, `playwright-tester`, `terraform`, `gem-browser-tester`, `power-bi-performance-expert`.
- 10 instructions: `agent-safety`, `csharp`, `go`, `markdown`, `python-mcp-server`, `security-and-owasp`, `terraform`, `typescript-mcp-server`, `update-docs-on-code-change`, `instructions`.
- 12 skills: `ai-prompt-engineering-safety-review`, `chrome-devtools`, `copilot-cli-quickstart`, `harness-engineering`, `java-junit`, `csharp-nunit`, `playwright-generate-test`, `secret-scanning`, `terraform-azurerm-set-diff-analyzer`, `github-copilot-starter`, `mini-context-graph`, `plantuml-ascii`.
- Hooks: `session-logger`, `governance-audit` plus a separate probe hook.
- Marketplace: `.github/plugin/marketplace.json`.

## Discovery results

| Primitive type | Discovered? | Evidence | Notes |
|---|---:|---|---|
| Agents | Yes | Debug log: `Plugin activation [agents]: fingerprint=b3e2633489af, plugins=0, loaded=12`. Later, after adding five probes: `loaded=17`. Tool schema enum listed sample/probe agents: `"C# Expert"`, `"Thinking Beast Mode"`, `"Ultimate Transparent Thinking Beast Mode"`, `"azure-iac-generator"`, `"Context7-Expert"`, `"gem-browser-tester"`, `"GitHub Actions Expert"`, `"Plan Mode - Strategic Planning & Architecture"`, `"Playwright Tester Mode"`, `"Power BI Performance Expert Mode"`, `"Python MCP Server Expert"`, `"Terraform Agent"`. | CLI warned for VS Code-only metadata: `.github/agents/azure-iac-generator.agent.md: unknown field ignored: argument-hint`; `.github/agents/context7.agent.md: unknown fields ignored: argument-hint, handoffs`. |
| Instructions | Partly, via prompt context | `/env` prompt response: `Several instruction files apply to this repo (C#, Go, Markdown, Python MCP, Terraform, TS/JS MCP, docs-update) — I'll consult relevant ones before editing matching files.` | This proves applicable project instructions reached the model context, but I did not find a non-interactive command that lists every instruction file by path. |
| Skills | Yes | `copilot skill list --json` listed all 12 project skills with `source: "project"`, e.g. `ai-prompt-engineering-safety-review`, `chrome-devtools`, `copilot-cli-quickstart`, `csharp-nunit`, `harness-engineering`, `java-junit`, `mini-context-graph`, `plantuml-ascii`, `playwright-generate-test`, `secret-scanning`, `terraform-azurerm-set-diff-analyzer`. Debug log also said `Plugin activation [skills]: fingerprint=b3e2633489af, plugins=0, loaded=14` before probes. | `loaded=14` includes the 12 project skills plus 2 built-ins. |
| Hooks | Not proven; no execution observed | Hook probe commands completed successfully but no `harness-hook-output/events.log` was created. Log searches did not show `.github/hooks/probe.json`, `sessionStart`, or hook registration lines. | Non-interactive `-p` and an `-i` run with stdin `/exit` both produced no hook side effect. |
| Marketplace/plugins | Yes for marketplace; no installed plugins | `copilot plugin marketplace add /Volumes/T9/harness-check/ws` returned `Marketplace "copilot-primitives" added successfully.` `copilot plugin marketplace list` then showed `copilot-primitives (Local: /Volumes/T9/harness-check/ws)`. `browse` listed plugins such as `acreadiness-cockpit`, `ai-team-orchestration`, `arch`, etc. | `copilot plugin list` reported `No plugins installed`, as expected because this only registered a marketplace. |

## Risk probes

### `.agent.md` vs `.md`

I added both `.github/agents/suffix-agent-test.agent.md` and `.github/agents/plain-md-agent.md`.

Evidence from the task tool schema enum:

```text
"plain-md-agent",
"suffix-agent-test",
```

Result: **this CLI discovered both `.agent.md` and plain `.md` files in `.github/agents/`**. This differs from the repository spec, which says `*.agent.md`.

### `tools:` vocabulary

Superseded by the complete follow-up test in [Tool vocabulary — definitive test](#tool-vocabulary--definitive-test). The earlier two-agent sample was directionally correct that tool lists change the effective schema, but it was incomplete. The definitive test below dumps the full tool schema for omitted, portable, VS Code-only, and bogus `tools:` values.

### `model:` bogus value

Probe:

```yaml
model: definitely-not-a-real-model-xyz
```

Evidence:

```text
Warning: Custom agent "bogus-model-test" specifies model "definitely-not-a-real-model-xyz" which is not available; using "claude-sonnet-5" instead
```

Result: **unknown model warns and falls back**, it does not fail the session.

### Skill `name` vs directory mismatch

Probe directory: `.github/skills/mismatch-dir/SKILL.md`; frontmatter: `name: different-name`.

Evidence from `copilot skill list --json`:

```text
different-name | source=project | path=/Volumes/T9/harness-check/ws/.github/skills/mismatch-dir | enabled=True
```

Result: **the CLI accepted the mismatch and listed the skill by frontmatter name**. It did not reject, rename to directory, or ignore it.

### Hooks repo path and camelCase events

Configured `.github/hooks/probe.json` with camelCase `sessionStart`, `userPromptSubmitted`, and `postResult`; command wrote to `harness-hook-output/events.log`.

Evidence:

```text
EXIT 0
ok
Side effect:
NONE
```

Result: **not verified** *(superseded — root cause found; see "Hooks — resolved" below)*. In this non-interactive harness, `.github/hooks/*.json` did not produce an observable side effect.

### `disableAllHooks`

Superseded — see below.

## Hooks — resolved (CLI 1.0.81-0)

The earlier "hooks never fire" result was **not** a discovery bug. Root cause: **repository hooks require the workspace to be a trusted folder**.

Isolated `COPILOT_HOME`, one identical hook payload placed in three candidate locations at once, each writing a distinct marker:

```
$ export COPILOT_HOME=$B/ch
$ copilot -C $B/ws -p "Reply only: ok" --allow-all --no-color --no-remote
=== HOOK EVENTS FIRED:
FIRED:USER_HOOKS_DIR at 1786990294
FIRED:SETTINGS_JSON at 1786990294
```

`$COPILOT_HOME/hooks/*.json` and the `hooks` key in `$COPILOT_HOME/settings.json` fired; repo `.github/hooks/probe.json` did not. Six further repo-level candidate paths (`.copilot/hooks/`, `.github/copilot/hooks/`, `.copilot/hooks.json`, `hooks.json`, `.github/hooks.json`) also produced nothing — ruling out a wrong path.

`copilot help config` documents the real gate:

```
`trustedFolders`: list of folders where permission to read or execute files has been granted.
`disableAllHooks`: whether to disable all hooks (repo-level and user-level); defaults to `false`.
`hooks`: inline hook definitions, keyed by event name (same schema as .github/hooks/*.json).
```

Re-run with the workspace trusted, changing nothing else:

```
$ printf '{"trustedFolders":["/Volumes/T9/hooktest/ws"],"disableAllHooks":false}\n' > $COPILOT_HOME/config.json
$ copilot -C $B/ws -p "Reply only: ok" --allow-all --no-color --no-remote
=== FIRED:
FIRED:REPO_GITHUB_HOOKS at 1786990380
```

**Repo-level hooks work.** Failure mode is silent — no warning is emitted when hooks are skipped for lack of trust. Interactive users never see this because accepting the trust prompt writes the entry; it only affects CI/container/`-p` runs with a fresh `COPILOT_HOME`.

### `disableAllHooks` is file-scoped inside `.github/hooks/*.json`

Two sibling files in one directory, one self-disabled:

```
a-enabled.json      -> "disableAllHooks": false
b-disabled.json     -> "disableAllHooks": true
=== FIRED:
FIRED:ENABLED_FILE at 1786990425
```

Only the self-disabled file's hooks were suppressed. It does **not** act globally from a hook file, so shipping a hook off-by-default via `disableAllHooks: true` is safe and does not disable its siblings. The global kill switch is the same key in `config.json`/`settings.json`.

### End-to-end on this repository

All four enabled hook configs fired against the real repo (`trustedFolders` seeded, isolated `COPILOT_HOME`), proving relative `bash` paths resolve from the workspace root:

```
=== hook-logs produced:
.../hook-logs/session-logger/prompts.log
.../hook-logs/session-logger/session.log
.../hook-logs/dependency-license-checker/check.log
.../hook-logs/governance-audit/audit.log

{"timestamp": "...", "event": "sessionStart", "cwd": "/Volumes/T9/copilot-primitives"}
{"timestamp":"...","event":"sessionEnd"}
{"timestamp":"...","event":"userPromptSubmitted","level":"INFO"}
```

`sessionStart`, `userPromptSubmitted` and `sessionEnd` are confirmed live, camelCase as specified. `secrets-scanner` produced no log in that run: invoked directly it works and exits 0, but it scans every modified file (536 here) and exceeds its `timeoutSec` on a large working tree — a hook-authoring lesson, not a discovery failure.

### Relative paths resolve from the workspace root, even for user-level hooks

A hook installed in `$COPILOT_HOME/hooks/probe.json` with `"bash": "hooks/probe/run.sh"`, where that script exists **only inside the workspace**:

```
=== FIRED:
FIRED:USER_SCOPE_RELATIVE_RESOLVED_FROM_WORKSPACE at 1786990785
```

So relative commands are resolved against `-C`/cwd, not against the config file's own directory. Practical consequence: a user-scope hook written with a relative path silently does nothing in every repository that lacks that path. Global installs must use absolute paths.

## Defects or runtime/spec divergences found

No concrete defect was found in the sampled repository primitives that prevents agent, instruction, skill, or marketplace loading.

Runtime/spec divergences to investigate:

1. **Agent filename discovery is broader than the spec**: this CLI discovered `.github/agents/plain-md-agent.md` as an agent, not only `*.agent.md`.
2. **Skill directory/name mismatch is accepted by runtime**: `different-name` under `mismatch-dir` was listed and enabled, even though the spec/validator require equality.
3. **Tool vocabulary mapping is not fully reflected by static rules**: `editFiles` produced an `edit` tool schema, while `search` did not expose grep/glob in the initial selected-agent schema.
4. **Repo hooks are silently skipped in untrusted folders**: `.github/hooks/*.json` never runs until the workspace appears in `trustedFolders`, and no warning says so. Resolved and fully characterised in "Hooks — resolved" above.

Warnings observed from sampled existing agents:

```text
.github/agents/azure-iac-generator.agent.md: unknown field ignored: argument-hint
.github/agents/context7.agent.md: unknown fields ignored: argument-hint, handoffs
.github/agents/gem-browser-tester.agent.md: unknown field ignored: argument-hint
```

These fields are intentionally VS Code-oriented according to the spec, so they are informational unless the goal is zero runtime warnings.

## Could not verify

- A true non-interactive `/env` dump listing all primitive categories by path/name. `copilot -p "/env"` sometimes produced a useful environment summary, but another run answered that `/env` is interactive-only.
- Hook `type: "http"` and the `matcher` filter; only `type: "command"` hooks were exercised. Discovery, precedence and `disableAllHooks` are now verified — see "Hooks — resolved".
- Installed plugin activation from the local marketplace. I verified marketplace registration/browse only; installing marketplace plugins was out of scope because sources point to plugin directories not copied into the scratch workspace.

## How to reproduce

```bash
# Use isolated config, not ~/.copilot
export COPILOT_HOME=/Volumes/T9/harness-check/copilot-home

# Build scratch workspace by copying representative files from /Volumes/T9/copilot-primitives
# to /Volumes/T9/harness-check/ws/.github/{agents,instructions,skills,hooks,plugin}
cd /Volumes/T9/harness-check/ws
git init --quiet

# Skills
copilot skill list --json

# Environment/log evidence
mkdir -p /Volumes/T9/harness-check/logs
copilot -C /Volumes/T9/harness-check/ws -p "/env" \
  --allow-all --no-color --log-level debug \
  --log-dir /Volumes/T9/harness-check/logs --no-remote

# Marketplace
copilot plugin marketplace add /Volumes/T9/harness-check/ws
copilot plugin marketplace list
copilot plugin marketplace browse copilot-primitives

# Agent probe
copilot -C /Volumes/T9/harness-check/ws --agent portable-tools-test \
  -p "Reply only with: ok" --allow-all --no-color \
  --log-level debug --log-dir /Volumes/T9/harness-check/logs-tools-portable \
  --no-remote --silent
```


## Frontmatter warning matrix

Follow-up date: 2026-08-17. Workspace: `/Volumes/T9/harness-check/followup-ws`. Command shape:

```bash
COPILOT_HOME=/Volumes/T9/harness-check/copilot-home \
  copilot -C /Volumes/T9/harness-check/followup-ws \
  -p "Reply only: frontmatter-ok" --allow-all --no-color \
  --log-level debug --log-dir /Volumes/T9/harness-check/followup-logs/frontmatter2 \
  --no-remote
```

`stdout` contained only the model response and run footer; `stderr` was empty:

```text
STDOUT first 4000:
frontmatter-ok

STDERR first 4000:
```

The warnings are therefore **debug-log warnings**, not terminal stdout/stderr output in this non-interactive run. They are emitted during agent loading, once per offending agent file per CLI process/session. Running a second CLI invocation emitted the same warning again for the same file:

```text
warn-invoke1: .github/agents/probe-warning-function.agent.md: unknown field ignored: argument-hint
warn-invoke2: .github/agents/probe-warning-function.agent.md: unknown field ignored: argument-hint
```

A warning does **not** prevent the agent from functioning. Invoking an agent with `argument-hint` produced normal responses:

```text
RUN 1 EXIT 0 STDOUT warning-agent-ok-1 STDERR
RUN 2 EXIT 0 STDOUT warning-agent-ok-2 STDERR
```

Matrix from `process-1786986427015-88325.log`:

| key | warns? | exact warning text | verdict |
|---|---:|---|---|
| `name` | No | — | Real CLI field / accepted silently. |
| `description` | No | — | Real CLI field / accepted silently. |
| `tools` | No | — | Real CLI field / accepted silently. See definitive tool test below for semantics. |
| `argument-hint` | Yes | `.github/agents/probe-argument-hint.agent.md: unknown field ignored: argument-hint` | Ignored by this CLI. |
| `user-invocable` | No | — | Real CLI field / accepted silently. |
| `mcp-servers` | No | — | Real CLI field / accepted silently when shaped correctly. A malformed probe without per-server `tools` logged: `custom agent markdown frontmatter is malformed: mcp-servers.probe-server.tools: Required`. |
| `model` | No | — | Real CLI field / accepted silently for a known model. Unknown model behavior is documented earlier: warn and fall back. |
| `disable-model-invocation` | No | — | Real CLI field / accepted silently. |
| `target` | Yes | `.github/agents/probe-target.agent.md: unknown field ignored: target` | Ignored by this CLI, despite being in the static spec. |
| `handoffs` | Yes | `.github/agents/probe-handoffs.agent.md: unknown field ignored: handoffs` | Ignored by this CLI. |
| `license` | Yes | `.github/agents/probe-license.agent.md: unknown field ignored: license` | Ignored by this CLI. |
| `version` | Yes | `.github/agents/probe-version.agent.md: unknown field ignored: version` | Ignored by this CLI. |
| `author` | Yes | `.github/agents/probe-author.agent.md: unknown field ignored: author` | Ignored by this CLI. |
| `capabilities` | Yes | `.github/agents/probe-capabilities.agent.md: unknown field ignored: capabilities` | Ignored by this CLI. |
| `infer_name` | Yes | `.github/agents/probe-infer-name.agent.md: unknown field ignored: infer_name` | Ignored by this CLI. |
| `allowed-tools` | Yes | `.github/agents/probe-allowed-tools.agent.md: unknown field ignored: allowed-tools` | Ignored by this CLI for agents. |
| `permissions` | Yes | `.github/agents/probe-permissions.agent.md: unknown field ignored: permissions` | Ignored by this CLI. |

Complete warning block from the valid matrix run:

```text
.github/agents/probe-allowed-tools.agent.md: unknown field ignored: allowed-tools
.github/agents/probe-argument-hint.agent.md: unknown field ignored: argument-hint
.github/agents/probe-author.agent.md: unknown field ignored: author
.github/agents/probe-capabilities.agent.md: unknown field ignored: capabilities
.github/agents/probe-handoffs.agent.md: unknown field ignored: handoffs
.github/agents/probe-infer-name.agent.md: unknown field ignored: infer_name
.github/agents/probe-license.agent.md: unknown field ignored: license
.github/agents/probe-permissions.agent.md: unknown field ignored: permissions
.github/agents/probe-target.agent.md: unknown field ignored: target
.github/agents/probe-version.agent.md: unknown field ignored: version
.github/agents/probe-warning-function.agent.md: unknown field ignored: argument-hint
Plugin activation [agents]: fingerprint=c610478b25f3, plugins=0, loaded=22
```

## Tool vocabulary — definitive test

Workspace: `/Volumes/T9/harness-check/tool-ws`. Four probe agents were selected with `--agent`, each with `-p "Reply only: ok"`, `--allow-all`, `--log-level debug`, and separate log directories under `/Volumes/T9/harness-check/tool-logs/`. Full `tool_schemas` were parsed from the final debug request for each selected agent.

### Full effective tool schemas

| agent | `tools:` value | warnings? | count | full sorted tool-name list |
|---|---|---:|---:|---|
| `tools-omitted` | omitted | No | 24 | `bash`, `create`, `edit`, `fetch_copilot_cli_documentation`, `github-mcp-server-get_copilot_space`, `github-mcp-server-get_file_contents`, `github-mcp-server-list_copilot_spaces`, `github-mcp-server-search_code`, `github-mcp-server-search_users`, `glob`, `grep`, `list_agents`, `list_bash`, `read_agent`, `read_bash`, `session_store_sql`, `skill`, `sql`, `stop_bash`, `task`, `view`, `web_fetch`, `web_search`, `write_agent` |
| `tools-portable` | `['read','search','edit','execute']` | No | 9 | `bash`, `create`, `edit`, `list_bash`, `read_bash`, `skill`, `sql`, `stop_bash`, `view` |
| `tools-vscode` | `['codebase','editFiles','runCommands','vscodeAPI']` | No | 7 | `bash`, `edit`, `list_bash`, `read_bash`, `skill`, `sql`, `stop_bash` |
| `tools-bogus` | `['totally_made_up_tool_zzz']` | No | 2 | `skill`, `sql` |

Raw parser output:

```text
## tools-bogus
count 2
warnings 0
names
skill
sql

## tools-omitted
count 24
warnings 0
names
bash
create
edit
fetch_copilot_cli_documentation
github-mcp-server-get_copilot_space
github-mcp-server-get_file_contents
github-mcp-server-list_copilot_spaces
github-mcp-server-search_code
github-mcp-server-search_users
glob
grep
list_agents
list_bash
read_agent
read_bash
session_store_sql
skill
sql
stop_bash
task
view
web_fetch
web_search
write_agent

## tools-portable
count 9
warnings 0
names
bash
create
edit
list_bash
read_bash
skill
sql
stop_bash
view

## tools-vscode
count 7
warnings 0
names
bash
edit
list_bash
read_bash
skill
sql
stop_bash
```

### Questions answered

- **Does an unrecognized tool name produce a warning, or is it silently dropped?** Silently dropped. `tools-bogus` emitted no stdout, stderr, or log warning for `totally_made_up_tool_zzz`; its schema shrank to only `skill` and `sql`.
- **Does `tools-vscode` end up with fewer/different effective tools than `tools-portable`?** Yes. `tools-vscode` had 7 tools; `tools-portable` had 9. `tools-portable` had `create` and `view`; `tools-vscode` did not. Neither received `grep`/`glob` from these tested values.
- **Does `tools-bogus` end up empty or crippled compared to `tools-omitted`?** Yes. It had only `skill` and `sql`, versus 24 tools for omitted.
- **Is `tools:` an allow-list filter over the full tool set, or an additive grant?** It is an **allow-list filter**. Omitting `tools` gave the full 24-tool set; specifying lists reduced the schema. Bogus-only reduced it to the baseline always-present `skill` and `sql`, not to the omitted-tools default.

### Practical consequence of a crippled tool list

I asked `tools-bogus` and `tools-omitted` to list the current directory. The bogus agent could not because it had no file/shell tools:

```text
## tools-bogus exit 0
STDOUT:
I don't have a file-listing or shell tool available in this session (only `skill` and `sql` tools are provided, and no skill applies to listing directory contents). I'm unable to list the current directory's files with the tools I have access to.
```

The omitted-tools agent could list files successfully:

```text
## tools-omitted exit 0
STDOUT:
Files in the current directory:

- `alpha.txt`
- `beta.txt`
- `.github/agents/tools-omitted.agent.md`
- `.github/agents/tools-portable.agent.md`
- `.github/agents/tools-bogus.agent.md`
- `.github/agents/tools-vscode.agent.md`
```

### Verdict on the 160-agent tool rewrite

The rewrite away from unsupported/bogus tool names was **justified**. This CLI treats `tools:` as a filter, emits no warning for unrecognized tool names, and can silently cripple an agent. VS Code names were not uniformly ignored to zero in this exact test (`editFiles` mapped to `edit`, `runCommands` exposed shell helpers), but the resulting set was still different and smaller than the portable list and lacked `view`/`create`. Bogus-only is conclusively crippled.

## Tool token vocabulary — net grants
Follow-up C date: 2026-08-17. Workspace: `/Volumes/T9/harness-check/vocab-ws`; isolated config: `COPILOT_HOME=/Volumes/T9/harness-check/copilot-home`. Each probe agent used a single `tools:` token and was invoked with `--agent <probe> -p "Reply only: ok" --allow-all --no-color --log-level debug --no-remote --silent`. Full `tool_schemas` were parsed from the debug log.
All successful token probes returned `ok`, wrote no stderr, and emitted no agent frontmatter warnings for the `tools:` token. Failed transient auth/network runs for four tokens were rerun successfully. Example run output:
```text
tok-read rc=0 out='ok' err=''
tok-search rc=0 out='ok' err=''
tok-write-agent rc 0 out ok err
tok-bogus rc 0 out ok err
```
The always-on floor was measured with `tools: ["totally_made_up_tool_zzz"]` and is subtracted below:

```text
floor ['skill', 'sql']
```
| token | valid? | net tools granted beyond floor | count |
|---|---:|---|---:|
| `read` | Yes | `view` | 1 |
| `search` | No | — | 0 |
| `edit` | Yes | `create`, `edit` | 2 |
| `execute` | Yes | `bash`, `list_bash`, `read_bash`, `stop_bash` | 4 |
| `web` | No | — | 0 |
| `todo` | No | — | 0 |
| `agent` | Yes | `list_agents`, `read_agent`, `task`, `write_agent` | 4 |
| `view` | Yes | `view` | 1 |
| `create` | Yes | `create` | 1 |
| `bash` | Yes | `bash`, `list_bash`, `read_bash`, `stop_bash` | 4 |
| `glob` | Yes | `glob` | 1 |
| `grep` | Yes | `grep` | 1 |
| `web_fetch` | Yes | `web_fetch` | 1 |
| `web_search` | Yes | `web_search` | 1 |
| `task` | Yes | `list_agents`, `read_agent`, `task`, `write_agent` | 4 |
| `sql` | No | — | 0 |
| `skill` | No | — | 0 |
| `write_agent` | Yes | `write_agent` | 1 |
| `read_agent` | Yes | `read_agent` | 1 |
| `list_agents` | Yes | `list_agents` | 1 |
| `read_bash` | Yes | `read_bash` | 1 |
| `stop_bash` | Yes | `stop_bash` | 1 |
| `list_bash` | Yes | `list_bash` | 1 |
| `session_store_sql` | Yes | `session_store_sql` | 1 |
| `fetch_copilot_cli_documentation` | Yes | `fetch_copilot_cli_documentation` | 1 |
| `all` | No | — | 0 |
| `*` | Yes | `bash`, `create`, `edit`, `fetch_copilot_cli_documentation`, `github-mcp-server-get_copilot_space`, `github-mcp-server-get_file_contents`, `github-mcp-server-list_copilot_spaces`, `github-mcp-server-search_code`, `github-mcp-server-search_users`, `glob`, `grep`, `list_agents`, `list_bash`, `read_agent`, `read_bash`, `session_store_sql`, `stop_bash`, `task`, `view`, `web_fetch`, `web_search`, `write_agent` | 22 |
| `shell` | Yes | `bash`, `list_bash`, `read_bash`, `stop_bash` | 4 |
| `terminal` | No | — | 0 |
| `run` | No | — | 0 |
| `runCommands` | Yes | `bash`, `list_bash`, `read_bash`, `stop_bash` | 4 |
| `codebase` | No | — | 0 |
| `editFiles` | Yes | `edit` | 1 |
| `search/codebase` | No | — | 0 |
| `changes` | No | — | 0 |
| `fetch` | No | — | 0 |
| `githubRepo` | No | — | 0 |
| `totally_made_up_tool_zzz` | No | — | 0 |

### Combination checks

| probe | `tools:` value | net tools granted beyond floor | net count | total schema count |
|---|---|---|---:|---:|
| `combo-read-grep-glob` | `['read', 'grep', 'glob']` | `glob`, `grep`, `view` | 3 | 5 |
| `combo-wildcard` | `['*']` | `bash`, `create`, `edit`, `fetch_copilot_cli_documentation`, `github-mcp-server-get_copilot_space`, `github-mcp-server-get_file_contents`, `github-mcp-server-list_copilot_spaces`, `github-mcp-server-search_code`, `github-mcp-server-search_users`, `glob`, `grep`, `list_agents`, `list_bash`, `read_agent`, `read_bash`, `session_store_sql`, `stop_bash`, `task`, `view`, `web_fetch`, `web_search`, `write_agent` | 22 | 24 |
| `combo-empty` | `[]` | — | 0 | 2 |
| `combo-full-candidate` | `['bash', 'create', 'edit', 'fetch_copilot_cli_documentation', 'glob', 'grep', 'task', 'view', 'web_fetch', 'web_search', 'write_agent', 'read_agent', 'list_agents', 'read_bash', 'stop_bash', 'list_bash', 'session_store_sql']` | `bash`, `create`, `edit`, `fetch_copilot_cli_documentation`, `glob`, `grep`, `list_agents`, `list_bash`, `read_agent`, `read_bash`, `session_store_sql`, `stop_bash`, `task`, `view`, `web_fetch`, `web_search`, `write_agent` | 17 | 19 |

Raw evidence excerpt from the parser output:

```text
read count 3 net ['view']
search count 2 net []
grep count 3 net ['grep']
glob count 3 net ['glob']
* count 24 net ['bash', 'create', 'edit', 'fetch_copilot_cli_documentation', 'github-mcp-server-get_copilot_space', 'github-mcp-server-get_file_contents', 'github-mcp-server-list_copilot_spaces', 'github-mcp-server-search_code', 'github-mcp-server-search_users', 'glob', 'grep', 'list_agents', 'list_bash', 'read_agent', 'read_bash', 'session_store_sql', 'stop_bash', 'task', 'view', 'web_fetch', 'web_search', 'write_agent']
totally_made_up_tool_zzz count 2 net []
combo-read-grep-glob count 5 net ['glob', 'grep', 'view']
combo-wildcard count 24 net ['bash', 'create', 'edit', 'fetch_copilot_cli_documentation', 'github-mcp-server-get_copilot_space', 'github-mcp-server-get_file_contents', 'github-mcp-server-list_copilot_spaces', 'github-mcp-server-search_code', 'github-mcp-server-search_users', 'glob', 'grep', 'list_agents', 'list_bash', 'read_agent', 'read_bash', 'session_store_sql', 'stop_bash', 'task', 'view', 'web_fetch', 'web_search', 'write_agent']
combo-empty count 2 net []
```

### Answers

1. **Always-on floor:** `skill`, `sql`. These appear even with a bogus-only `tools:` list and with `tools: []`.
2. **Valid tokens (grant at least one net tool):** `read`, `edit`, `execute`, `agent`, `view`, `create`, `bash`, `glob`, `grep`, `web_fetch`, `web_search`, `task`, `write_agent`, `read_agent`, `list_agents`, `read_bash`, `stop_bash`, `list_bash`, `session_store_sql`, `fetch_copilot_cli_documentation`, `*`, `shell`, `runCommands`, `editFiles`.
3. **No-op tokens / landmines (grant nothing beyond the floor):** `search`, `web`, `todo`, `sql`, `skill`, `all`, `terminal`, `run`, `codebase`, `search/codebase`, `changes`, `fetch`, `githubRepo`, `totally_made_up_tool_zzz`. No warnings were emitted for these no-ops.
4. **Recommended minimal token set for full 24-tool capability:** either omit `tools:` entirely or use `tools: ["*"]`. Both produced the full 24-tool schema. `tools: ["all"]` is a no-op. An explicit list of common concrete tool names tested as `combo-full-candidate` yielded only 19 total tools and did not include the GitHub MCP tools, so it is not equivalent to full capability.
5. **Correct tokens for code search:** use exact concrete tokens `grep` and `glob`. The migrated alias `search` is a no-op in this CLI. The combination `tools: ["read", "grep", "glob"]` granted `view`, `grep`, and `glob`, confirming aliases and concrete names compose.

### Migration implication

The previous 160-file rewrite away from VS Code-only/bogus names was directionally justified because `tools:` is a filter and unrecognized tokens silently cripple agents. However, the specific portable alias `search` is **not sufficient** for Copilot CLI 1.0.81-0: agents that need search must include `grep` and/or `glob` explicitly, or omit `tools:` / use `"*"` for full capability.
