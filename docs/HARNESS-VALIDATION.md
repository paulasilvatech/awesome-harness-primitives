# GitHub Copilot CLI Harness Runtime Validation

Date: 2026-08-17
CLI: `GitHub Copilot CLI 1.0.81-0`
Binary: `/Users/paulasilva/.local/bin/copilot`

> Note: the requested scratch root was `/tmp/harness-check`, but this execution environment forbids file operations under `/tmp`. I used `/Volumes/T9/harness-check` instead. The live `~/.copilot` tree was not modified; commands used `COPILOT_HOME=/Volumes/T9/harness-check/copilot-home`.

## First-party customization documentation verification

Verification date: 2026-08-19. These checks fetched known first-party pages directly; they did not use
community sources or treat page availability as runtime proof.

| Area | First-party source | Verified guidance |
| --- | --- | --- |
| Repository instructions | https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions | `.github/copilot-instructions.md` is repository-wide; `.github/instructions/**/*.instructions.md` is path-specific; both apply when matched. Repository instructions should be concise, general, and include project layout and working validation commands. |
| VS Code instructions | https://code.visualstudio.com/docs/agent-customization/custom-instructions | `.github/copilot-instructions.md` is always-on. File-based instructions use `.instructions.md`; multiple applicable files are combined without a guaranteed order. Start with one concise global file and add focused path-specific rules. |
| Custom agents | https://code.visualstudio.com/docs/agent-customization/custom-agents | Custom agents define task-specific personas, instructions, and tool sets. Workspace agents live under `.github/agents`; VS Code handoffs are guided transitions between agents. |
| Agent Skills | https://code.visualstudio.com/docs/agent-customization/agent-skills | Skills are portable on-demand packages. `name` must be kebab-case, no more than 64 characters, and match the parent directory; `description` must state what and when and is no more than 1024 characters. |
| GitHub Copilot plugins | https://docs.github.com/en/copilot/concepts/agents/about-plugins and https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference | An installable plugin can contain agents, skills, hooks, MCP server configurations, and LSP server configurations. The documented component fields do not include repository instructions or VS Code prompt files; those assets must still be published to their repository discovery paths when needed. |
| Prompt files | https://code.visualstudio.com/docs/agent-customization/prompt-files | Prompt files are manually invoked local VS Code slash commands. Agent Host does not use them. Supported metadata includes `description`, `name`, `argument-hint`, `agent`, `model`, and `tools`; unavailable tools are ignored. |
| Hooks | https://docs.github.com/en/copilot/reference/hooks-reference | Hooks are supported by Copilot CLI and cloud agent. Repository configs live under `.github/hooks/*.json`; cloud agent runs in an ephemeral Linux environment and honors `bash` or `command`, not PowerShell. |

The pages did not expose a product version in the fetched content. Recheck them when a target product
version changes, local evidence conflicts, a claim is unverified, the user asks for current behavior, or
this evidence is older than 90 days. Do not refresh this date without repeating the fetch and reviewing
the relevant sections.

## Open Horizons plugin integration verification

Verification date: 2026-08-20. Target runtime: GitHub Copilot CLI 1.0.81-0.

| Evidence | Verified result |
| --- | --- |
| https://github.com/Ohorizons/open-horizons-platform/commit/7858578302fe0f54fdb43e15f84b14fd5d7519c2 | This was the upstream `main` commit inspected while refreshing the packaged workspace customizations. The plugin intentionally adds package metadata, MCP configuration, harness documentation, and runtime portability fixes that do not exist in the upstream `.github/` tree. |
| `copilot plugin --help`, `copilot plugin install --help`, and `copilot mcp --help` | The installed CLI supports marketplace and repository plugin installation. MCP configuration is loaded from user, workspace, and installed-plugin sources; local servers use `type: local`, while remote servers use `type: http` or `type: sse`. |
| Isolated marketplace install with `COPILOT_HOME=<session-artifact>` | `open-horizons-platform@copilot-primitives` installed successfully, reported 30 skills, and exposed `microsoft-docs`, `azure`, `terraform`, and `playwright` as plugin MCP servers. The representative invocation `--agent open-horizons-platform:deploy` returned `ok` after agents were mirrored under `com.github.copilot/agents/`. |
| GitHub Copilot CLI debug log for the schema-declaring plugin | A top-level legacy `agents` field emitted: `agents are read only from "com.github.copilot/agents"` and was ignored. Moving generated copies to that extension directory loaded the namespaced agents. |
| Isolated schema-declaring hook probe | A root `hooks/hooks.json` did not fire. Moving the identical config to `com.github.copilot/hooks/hooks.json` produced one observable `sessionStart` event, proving the GitHub extension hook path for Agent Plugins 1.0. |
| Open Horizons hook payload and workspace-kit tests | The safety hook passed safe, ask, malformed, disabled, and non-execution payload cases. The workspace-kit publisher passed dry-run, apply, idempotent, conflict-with-no-write, and explicit-force cases. |
| `npm view @azure/mcp version` and `npx -y @azure/mcp@3.0.0-beta.36 server start --help` | `3.0.0-beta.36` was the published `latest` tag and the configured startup command parsed successfully. |
| `npm view @playwright/mcp version` and `npx -y @playwright/mcp@0.0.79 --help` | `0.0.79` was the published `latest` tag and the configured startup command parsed successfully. |
| https://github.com/hashicorp/terraform-mcp-server/releases/tag/v1.2.0 and `docker manifest inspect hashicorp/terraform-mcp-server:1.2.0` | Release `v1.2.0` was latest and the pinned Docker image tag existed. |

The imported Open Horizons manifest had been an unrelated copy of the `noob-mode` manifest, referenced a
missing skill, was absent from the marketplace, and left every packaged agent and skill unreferenced.
The package was corrected to install its own nine agents, 30 skills, one safety hook, and four MCP
servers. Repository-only instructions, prompts, workflows, issue forms, and templates remain in the
package as a workspace kit and are published only through an explicit dry-run/apply workflow.

Other imported marketplace manifests may still combine the Agent Plugins schema URL with legacy GitHub
top-level component fields. The repository validator currently grandfathers those packages unless they
declare `extensions.com.paulasilvatech.copilot-primitives.componentSource: plugin`; migrating every legacy
package to closed Agent Plugins 1.0 layout is separate work.

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
