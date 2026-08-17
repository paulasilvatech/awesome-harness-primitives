# GitHub Copilot CLI Harness Runtime Validation

Date: 2026-08-17
CLI: `GitHub Copilot CLI 1.0.81-0`
Binary: `/Users/paulasilva/.local/bin/copilot`

> Note: the requested scratch root was `/tmp/harness-check`, but this execution environment forbids file operations under `/tmp`. I used `/Volumes/T9/harness-check` instead. The live `~/.copilot` tree was not modified; commands used `COPILOT_HOME=/Volumes/T9/harness-check/copilot-home`.

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

Result: **not verified**. In this non-interactive harness, `.github/hooks/*.json` did not produce an observable side effect. I cannot honestly claim repo-level hook discovery or camelCase acceptance from these runs.

### `disableAllHooks`

Not verified. Because hooks did not execute at all in the observable non-interactive runs, there was no meaningful baseline against which to prove suppression.

## Defects or runtime/spec divergences found

No concrete defect was found in the sampled repository primitives that prevents agent, instruction, skill, or marketplace loading.

Runtime/spec divergences to investigate:

1. **Agent filename discovery is broader than the spec**: this CLI discovered `.github/agents/plain-md-agent.md` as an agent, not only `*.agent.md`.
2. **Skill directory/name mismatch is accepted by runtime**: `different-name` under `mismatch-dir` was listed and enabled, even though the spec/validator require equality.
3. **Tool vocabulary mapping is not fully reflected by static rules**: `editFiles` produced an `edit` tool schema, while `search` did not expose grep/glob in the initial selected-agent schema.
4. **Hooks could not be empirically proven in this harness**: `.github/hooks/*.json` did not trigger side effects in `-p` or the tested `-i` invocation.

Warnings observed from sampled existing agents:

```text
.github/agents/azure-iac-generator.agent.md: unknown field ignored: argument-hint
.github/agents/context7.agent.md: unknown fields ignored: argument-hint, handoffs
.github/agents/gem-browser-tester.agent.md: unknown field ignored: argument-hint
```

These fields are intentionally VS Code-oriented according to the spec, so they are informational unless the goal is zero runtime warnings.

## Could not verify

- A true non-interactive `/env` dump listing all primitive categories by path/name. `copilot -p "/env"` sometimes produced a useful environment summary, but another run answered that `/env` is interactive-only.
- Hook discovery/execution and `disableAllHooks`, for reasons above.
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
