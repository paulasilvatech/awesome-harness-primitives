# Claude Code Harness Validation Evidence

Date: **2026-08-31**

Local runtime: **Claude Code 2.1.251**

Binary: `/Users/paulasilva/.local/bin/claude`

This document records dated evidence for `docs/CLAUDE-CODE-HARNESS-SPEC.md`. First-party documentation was fetched directly from `code.claude.com`; page availability was treated as documentation evidence, not runtime proof.

## First-party documentation verification

| Area | First-party source | Verified result |
| --- | --- | --- |
| Customization model | https://code.claude.com/docs/en/features-overview | Claude Code distinguishes persistent instructions, path-scoped rules, skills, subagents, hooks, MCP servers, and plugins. |
| Project instructions and rules | https://code.claude.com/docs/en/memory | Project instructions load from `CLAUDE.md` or `.claude/CLAUDE.md`; path-scoped rules live under `.claude/rules/`. Multi-step procedures should move to skills. |
| Subagents | https://code.claude.com/docs/en/sub-agents | Project and user subagents live under `.claude/agents/` and `~/.claude/agents/`; plugin agents live under `<plugin>/agents/`. Plugin agents do not support `hooks`, `mcpServers`, or `permissionMode`. |
| Skills and commands | https://code.claude.com/docs/en/skills | Skills use `<scope>/skills/<name>/SKILL.md`. Custom commands have merged into skills, but `.claude/commands/*.md` remains supported. Skills are recommended when bundled files or automatic discovery are needed. |
| Tools | https://code.claude.com/docs/en/tools-reference | Tool names are exact strings used by permissions, subagent tool lists, and hook matchers. MCP tools use their runtime-provided names. |
| Hooks | https://code.claude.com/docs/en/hooks | Hooks support command, HTTP, MCP tool, prompt, and agent handlers across the documented lifecycle. The current event set includes `PreModelSwitch` and `PostModelSwitch`. |
| Plugins | https://code.claude.com/docs/en/plugins-reference | Plugins are self-contained and can contain skills, agents, hooks, MCP servers, LSP servers, and monitors. Conventional component directories are automatically discovered. |
| Marketplaces | https://code.claude.com/docs/en/plugin-marketplaces | A repository marketplace lives at `.claude-plugin/marketplace.json`; each entry requires a name and source. Local sources must remain self-contained because installed plugins are copied or cached independently. |

## Claude API skill source verification

The volatile model sources referenced by `foundry-claude-api` were fetched directly on 2026-08-31.

| Source | Result |
| --- | --- |
| https://platform.claude.com/docs/en/models/overview.md | Verified the current model lineup, model IDs, context windows, output limits, pricing summary, and retirement guidance used by the skill. |
| https://platform.claude.com/docs/en/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5.md | Verified Fable 5 and Mythos 5 IDs, availability, refusal behavior, fallback guidance, context/output limits, and pricing. |
| https://platform.claude.com/docs/en/about-claude/models/migration-guide.md | Verified the migration index and current model-specific migration guides. |
| https://platform.claude.com/docs/en/about-claude/pricing.md | Verified the canonical pricing page. The prior `/docs/en/pricing.md` path returned 404 and was corrected in the skill's live-source registry. |

## Runtime probes

| Probe | Result |
| --- | --- |
| `claude --version` | Passed; returned `2.1.251 (Claude Code)`. |
| `claude plugin validate --strict .claude-plugin/marketplace.json` | Passed for the generated marketplace. |
| `python3 harness/claude-code/scripts/validate_primitives.py --strict` before remediation | Passed with 0 errors and 0 warnings across 228 subagents, 195 rules, 490 skills, 48 commands, 139 plugins, and 8 hook packages. |
| `python3 harness/claude-code/scripts/convert_from_copilot.py --check` before remediation | Failed with generated drift, `.DS_Store` residue, and copied .NET `obj/` build artifacts. |
| `python3 harness/claude-code/scripts/generate_catalog.py --check` before remediation | Failed because the generated catalog was stale. |
| Installed-copy manifest inspection before remediation | Failed: all declared `CLAUDE.md` and `.claude/` targets were missing, and the `claude-code-harness` rule source did not exist. |

The failed pre-remediation probes establish why the original Claude harness commit was incomplete despite passing structural validation.

## Verified divergences and conversion policy

| Source behavior | Claude Code behavior | Repository policy |
| --- | --- | --- |
| VS Code prompt files are explicit editor actions. | Custom commands are supported but are now part of the skills system. | Convert prompts to `.claude/commands/*.md` to preserve explicit invocation; do not claim VS Code runtime inputs survive. |
| Copilot instruction metadata includes `applyTo` and `description`. | Claude project-rule frontmatter documents `paths`; `CLAUDE.md` provides global instructions. | Convert `applyTo` to `paths` and preserve descriptions as body scope notes. |
| Copilot and VS Code tool identifiers are surface-specific. | Claude Code uses exact built-in or MCP tool names. | Map only known equivalents and report dropped tools. |
| Copilot and Claude hook schemas differ. | Claude Code uses PascalCase lifecycle events and Claude-specific handler fields. | Convert only explicit event mappings; fail on unmapped events. |
| Plugin component paths may be declared in Copilot manifests. | Claude Code auto-discovers conventional plugin directories. | Generate self-contained Claude plugins and omit Copilot component-path metadata. |

## Post-remediation verification

| Probe | Result |
| --- | --- |
| Four required Claude harness gates | Passed on 2026-08-31: conversion drift, strict validation, catalog drift, and installed-copy drift all returned exit code 0. |
| Strict Claude structural validation | Passed with 0 errors and 0 warnings across 228 subagents, 196 rules, 490 skills, 48 commands, 139 plugins, 8 reusable hook packages, and 1 generated project settings file. |
| Native Claude plugin validation | Passed for all 139 generated plugins and `.claude-plugin/marketplace.json` with Claude Code 2.1.251 (140/140). |
| Workspace-kit compatibility tests | Passed 7 Backstage tests and 17 Open Horizons tests after generated publishers were redirected to isolated `copilot-components/` payloads. |
| Catalog compatibility tests | Passed all 4 `generate_catalog.py` tests after restoring the documented single-document builder API. |
| Project hook activation | Verified `.claude/settings.json` aggregates the 4 hooks active on the Copilot side and the installed-copy manifest publishes all matching scripts under `.claude/hooks/`. |
| Full bundled Python test loop | Passed all 626 tests across 61 test files in both harness trees with `PYTHONDONTWRITEBYTECODE=1`. |

## Unverified behavior

- Semantic equivalence of every converted primitive has not been established by executing all workflows.
- External MCP servers, credentials, network services, and product-specific extensions remain environment-dependent.
- VS Code prompt behavior is not runtime evidence for the generated Claude commands.
- The four intrusive hook packages intentionally disabled by the Copilot repository policy remain generated but inactive in Claude Code.
- Marketplace validation proves schema validity, not successful installation and activation of every plugin.

## Completion evidence

The dated pre-remediation failures above document why commit `ec039b98` was incomplete. The post-remediation table records the corrected state after repository-wide generated audits, all required gates, native plugin validation, and the full bundled test suite passed.
