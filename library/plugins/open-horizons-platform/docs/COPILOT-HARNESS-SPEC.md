# GitHub Copilot Harness — Canonical Primitive Specification

Authoritative reference for this repository. Every rule below is verified against **one or both** of:

- **BUNDLE** — the installed GitHub Copilot CLI runtime (`~/.copilot/pkg/<platform>/<version>/prebuilds/<platform>/runtime.node`,
  `app.js`, `definitions/*.agent.yaml`, `builtin-skills/*/SKILL.md`). Rust source paths recovered from the binary
  (`src/runtime/src/hooks/declarative.rs`, `src/runtime/src/extensions/discovery.rs`, `src/runtime/src/config/loader.rs`)
  are the strongest evidence available.
- **DOCS** — `docs.github.com/en/copilot/...` and `code.visualstudio.com/docs/copilot/customization/...`.

When BUNDLE and DOCS disagree, **BUNDLE wins** and the divergence is called out.

CLI version validated against: **1.0.81-0**.

---

## 1. Custom Agents — `*.agent.md`

### 1.1 Discovery

| Scope | Path |
| --- | --- |
| User | `~/.copilot/agents/*.agent.md` (`$COPILOT_HOME` overrides `~/.copilot`) |
| Repository | `.github/agents/*.agent.md` |
| Organization | `agents/*.agent.md` in the org `.github` / `.github-private` repo |
| Plugin | `<plugin-root>/agents/*.agent.md` |

Precedence on filename collision: **User → Repository → Organization → Enterprise**.
Deduplication key is the filename with `.md` / `.agent.md` stripped.

Filename must match `^[A-Za-z0-9._-]+\.agent\.md$`.

### 1.2 Frontmatter

```yaml
---
name: my-agent                     # OPTIONAL — defaults to filename
description: >-                    # REQUIRED — the only truly required field
  What the agent does and when to select it.
tools: ["read", "grep", "glob", "edit"]  # OPTIONAL allow-list — omit or ["*"] = all tools. Not "search"/"web": see §1.3
model: claude-sonnet-4.5           # OPTIONAL — string or prioritized array
target: github-copilot             # OPTIONAL — "vscode" | "github-copilot"
user-invocable: true               # OPTIONAL — default true; false hides from /agent picker
disable-model-invocation: false    # OPTIONAL — default false; true blocks auto-delegation
mcp-servers:                       # OPTIONAL — CLI/cloud only, ignored by VS Code
  my-server:
    type: local                    # "local" | "stdio" | "http" | "sse"
    command: my-cmd
    args: ["--flag"]
    env: { TOKEN: "${{ secrets.TOKEN }}" }
argument-hint: "<path>"            # OPTIONAL — VS Code only, ignored by CLI
handoffs: []                       # OPTIONAL — VS Code only, ignored by CLI
metadata: {}                       # OPTIONAL — annotation passthrough
---
```

**Field status**

| Field | CLI | VS Code | Notes |
| --- | --- | --- | --- |
| `description` | **REQUIRED** | **REQUIRED** | Non-empty string |
| `name` | optional | optional | Defaults to filename |
| `tools` | optional | optional | See §1.3 |
| `model` | optional | optional | String or array of strings |
| `target` | optional | optional | `vscode` \| `github-copilot` |
| `user-invocable` | optional | optional | BUNDLE-confirmed key |
| `disable-model-invocation` | optional | optional | BUNDLE-confirmed key |
| `mcp-servers` | optional | ignored | BUNDLE-confirmed key |
| `argument-hint` | ignored | optional | VS Code only |
| `handoffs` | ignored | optional | VS Code only |
| `infer` | **RETIRED** | **RETIRED** | Replace with the two fields above |
| `mode`, `hidden`, `agents`, `agent`, `title` | **not an agent field** | — | Remove |

Body: Markdown, **max 30 000 characters**.

Unrecognized frontmatter keys and unrecognized tool names are **silently ignored** — they do not raise
errors, which is precisely why they are dangerous: a misspelled tool list degrades silently.

### 1.3 `tools:` vocabulary

`tools:` is an **allow-list filter**, not an additive grant. Omitting it gives the agent the full tool set;
declaring it restricts the agent to the listed tokens. **Unrecognized or unavailable tokens are ignored** by
design so product-specific tools can be listed in a shared agent profile without breaking another surface.
That compatibility behavior is useful, but it also means a wrong or incomplete tool list can remove capability
without an error.

This section is intentionally surface-aware because `.github/agents/*.agent.md` is read by VS Code Copilot,
GitHub.com, and GitHub Copilot CLI. Treat the two evidence streams below separately:

- **Official documentation:** GitHub's custom agents configuration reference states that its YAML frontmatter
  applies to agent profiles in GitHub.com, the Copilot CLI, and supported IDEs. It documents tool aliases
  `read`, `search`, `edit`, `execute`, `agent`, `web`, and `todo`, says aliases are case-insensitive, and says
  all unrecognized tool names are ignored. Source:
  <https://docs.github.com/en/copilot/reference/custom-agents-configuration>.
- **VS Code documentation:** VS Code documents predefined tool sets such as `read`, `search`, `edit`,
  `execute`, `web`, and `agent`, plus namespaced tool IDs such as `search/codebase`, `search/usages`,
  `search/changes`, `read/problems`, `read/terminalLastCommand`, and `web/fetch`. Sources:
  <https://code.visualstudio.com/docs/agent-customization/custom-agents> and
  <https://code.visualstudio.com/docs/agent-customization/tool-sets>.
- **Local CLI observation:** a local probe against Copilot CLI 1.0.81-0 reported that `search`, `web`, and
  `todo` granted no additional local tools, while `grep`, `glob`, `web_fetch`, and `web_search` did. A probe
  of the local bundle did not locate the official alias table strings, so the discrepancy is unresolved; the
  alias layer may live server-side or in a component not inspected.

Do not read the local observation as a settled claim that `search` or `web` are invalid. The official
cross-surface alias table says they are valid primary aliases; the local bundle measurement says they did not
expand in that one local CLI probe.

#### Official alias vocabulary

The GitHub reference documents this alias vocabulary for custom agents:

| Primary alias | Compatible aliases | Documented mapping or scope | Purpose |
| --- | --- | --- | --- |
| `execute` | `shell`, `Bash`, `powershell` | Shell tools: `bash` or `powershell` | Execute a command in the appropriate shell. |
| `read` | `Read`, `NotebookRead` | `view` | Read file contents. |
| `edit` | `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | Edit tools such as `str_replace`, `str_replace_editor` | Allow file edits. |
| `search` | `Grep`, `Glob` | `search` | Search for files or text in files. |
| `agent` | `custom-agent`, `Task` | Custom agent tools | Invoke another custom agent. |
| `web` | `WebSearch`, `WebFetch` | Not currently applicable for cloud agent | Fetch URLs and perform web search. |
| `todo` | `TodoWrite` | Not currently applicable for cloud agent; supported by VS Code | Structured task lists. |

`Grep` and `Glob` are therefore documented compatible aliases of `search`; using `grep` and `glob` for CLI
coverage is not an off-spec workaround.

#### Local CLI 1.0.81-0 observation

Every row below was measured locally against CLI 1.0.81-0 by declaring a single token and dumping the
resulting tool schema. Because this conflicts with the official alias table for `search`, `web`, and `todo`,
treat it as a local observation until the alias-layer implementation is located.

**Always-on floor** (present even when every token is invalid): `skill`, `sql`.

| Token | Net tools granted beyond the floor in local CLI probe |
| --- | --- |
| `*` | everything (22 beyond floor) — equivalent to omitting `tools:` |
| `read` / `view` | `view` |
| `create` | `create` |
| `edit` / `editFiles` | `create`, `edit` (`editFiles` grants only `edit`) |
| `execute` / `bash` / `shell` / `runCommands` | `bash`, `list_bash`, `read_bash`, `stop_bash` |
| `agent` / `task` | `list_agents`, `read_agent`, `task`, `write_agent` |
| `grep` | `grep` |
| `glob` | `glob` |
| `web_fetch` | `web_fetch` |
| `web_search` | `web_search` |
| `session_store_sql` | `session_store_sql` |
| `fetch_copilot_cli_documentation` | `fetch_copilot_cli_documentation` |
| `write_agent`, `read_agent`, `list_agents`, `read_bash`, `stop_bash`, `list_bash` | the same-named tool |

GitHub's own CLI 1.0.81-0 built-in agent definitions also use these direct tokens:
`context_board`, `lsp`, `powershell`, `read_powershell`, `stop_powershell`, in addition to the table above.
They are BUNDLE-confirmed tokens, but their concrete availability depends on the host surface.

#### Portability matrix

| Capability | VS Code / official alias token | Local CLI companion token | Portable single token? |
| --- | --- | --- | --- |
| Read files | `read` | `read` -> `view` | yes |
| Search code | `search` | `grep`, `glob` | **uncertain — list both** |
| Edit files | `edit` | `edit` -> `create` + `edit` | yes |
| Run commands | `execute` | `execute` -> `bash` family | yes |
| Delegate to subagents | `agent` | `agent` -> `task` family | yes |
| Fetch web page | `web` | `web_fetch` | **uncertain — list both** |
| Web search | `web` | `web_search` | **uncertain — list both** |
| Structured task lists | `todo` | CLI floor includes `sql`; local probe found no extra `todo` tool | surface-specific |

#### Surface-specific and namespaced tools

VS Code-valid tool IDs such as `search/codebase`, `search/usages`, `search/changes`, `read/problems`,
`read/terminalLastCommand`, `web/fetch`, and extension-provided `namespace/tool` IDs are legitimate to author.
They may be ignored by CLI unless that CLI surface has a matching MCP or product tool, so pair them with
portable aliases or CLI-native companions when a capability must work everywhere.

MCP / namespaced CLI tools use `server/tool` or `server/*`, matching BUNDLE regex
`^([a-zA-Z0-9_.-]+/(?:\*|[a-zA-Z0-9_.-]+))(?::(.+))?$` — for example `github-mcp-server/search_code`.

The remaining tokens previously seen in examples — `all`, `terminal`, `run`, `codebase`, `changes`, `fetch`,
`githubRepo` — are not in the official GitHub alias table, the cited VS Code predefined tool-set list, or the
local CLI-native token list. Prefer documented aliases instead. If a future VS Code extension, workspace tool
set, or MCP server defines one of these names, it can be used deliberately; otherwise the name will be ignored
by design. Validators should warn on these unknown tokens rather than treating them as hard schema errors.

`sql` and `skill` are also no-ops as `tools:` tokens in the local CLI probe, but harmlessly so: they are already
in the CLI floor.

#### Repository authoring rule

For dual-surface repository agents, author the **union** of VS Code / official aliases and CLI-observed native
companions whenever a capability has unresolved or surface-specific behavior. Use this pattern and remove
capabilities the agent does not need:

```yaml
tools:
  - read      # VS Code and official alias; local CLI alias -> view
  - search    # Official/VS Code search alias; local CLI observation was unresolved
  - edit      # VS Code and official alias; local CLI alias -> create, edit
  - execute   # VS Code and official alias; local CLI alias -> bash family
  - grep      # Official compatible alias of search; local CLI native search tool
  - glob      # Official compatible alias of search; local CLI native search tool
```

Add `web` plus `web_fetch` and/or `web_search` together when a dual-surface agent needs web access.

This union form is correct under both hypotheses:

- If the official alias layer works in the CLI, `search` provides search and `grep`/`glob` are redundant but
  harmless documented compatible aliases.
- If the local observation reflects the active CLI behavior, `grep`/`glob` provide search and `search` is
  harmlessly ignored.
- VS Code consumes `read`, `search`, `edit`, `execute`, `web`, and `agent` as tool sets or aliases.
- Either way the agent keeps the intended capability on every surface, and unrecognized names are ignored by
  explicit design.

> **Danger:** removing `search` can silently break search in VS Code or any surface using the official alias
> layer; removing `grep`/`glob` can silently break search in a CLI surface matching the local observation.
> Removing `web` can silently break VS Code web tools; removing `web_fetch`/`web_search` can silently break CLI
> web tools. Neither surface is required to report an error — capability can just disappear.

Rule `AG017` must therefore be companion-aware, not a flat ban: `search` should warn or fail only when neither
`grep` nor `glob` is present, and `web` only when neither `web_fetch` nor `web_search` is present. Officially
documented tokens such as `todo` and VS Code namespaced tool IDs such as `search/codebase` must not be treated
as junk.

**Recommendation.** For a general-purpose agent, omit `tools:` entirely (or use `['*']`) so it keeps full
capability as each surface adds tools. Declare an explicit list only when you deliberately want to restrict the
agent, and then list both surfaces for unresolved or non-portable capabilities: `search` with `grep`/`glob`, and
`web` with `web_fetch`/`web_search`.

### 1.4 `model:`

No enumerated allowlist is published. BUNDLE uses lowercase hyphenated IDs (`claude-haiku-4.5`).
Legacy VS Code display names (`GPT-4.1`, `Claude Sonnet 4`) are accepted syntactically but are not CLI model IDs.
Prefer omitting `model` so the agent inherits the user's session model, or use a current lowercase ID.

---

## 2. Custom Instructions — `*.instructions.md`

### 2.1 Discovery

`$HOME/.copilot/copilot-instructions.md`, `$HOME/.copilot/instructions/**/*.instructions.md`,
`.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`,
`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and any directory listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`.

### 2.2 Frontmatter

```yaml
---
applyTo: "**/*.ts,**/*.tsx"   # OPTIONAL — comma-separated globs; "**" = every file
description: "…"              # OPTIONAL — shown on hover
name: "TypeScript Standards"  # OPTIONAL — display name, defaults to filename
excludeAgent: code-review     # OPTIONAL — "code-review" | "cloud-agent"
---
```

Only these four keys are recognized. Frontmatter itself is optional, but **omitting `applyTo` means the file is
never auto-applied** — it can only be attached manually. For a repo of reusable instruction modules, `applyTo`
should always be present.

Body must be non-empty. Keep each file focused and roughly ≤ 2 pages; instructions must be general, not task-specific.

---

## 3. Agent Skills — `<name>/SKILL.md`

### 3.1 Discovery

| Priority | Path |
| --- | --- |
| Built-in | `<bundle>/builtin-skills/<name>/SKILL.md` |
| Project | `.github/skills/<name>/SKILL.md`, `.claude/skills/…`, `.agents/skills/…` |
| Personal | `~/.copilot/skills/<name>/SKILL.md`, `~/.agents/skills/…` |
| Plugin | `<plugin-root>/skills/<name>/SKILL.md` |

Project skills override personal skills of the same name.

### 3.2 Frontmatter

BUNDLE ships this requirement text verbatim inside `runtime.node`:

> Every generated skill must validate all of the following:
> `name` — 1-64 characters, kebab-case, must match the parent skill directory name.
> `description` — 1-1024 characters, must state both **what** the skill does and **when** to use it.

```yaml
---
name: my-skill-name              # REQUIRED — 1-64 chars, ^(?:[a-z0-9]|[a-z0-9][a-z0-9-]*[a-z0-9])$, == directory name
description: >-                  # REQUIRED — 1-1024 chars, must state WHAT and WHEN
  What this skill does. Use this skill when <trigger conditions>.
user-invocable: true             # OPTIONAL — BUNDLE-confirmed
disable-model-invocation: false  # OPTIONAL — BUNDLE-confirmed
allowed-tools: ["view", "grep"]  # OPTIONAL — pre-approved tools
argument-hint: "<arg>"           # OPTIONAL — BUNDLE-confirmed; body may use $ARGUMENTS
license: MIT                     # OPTIONAL
metadata: { author: "…" }        # OPTIONAL — string→string map
tags: ["ci", "deploy"]           # OPTIONAL — add only when useful and non-redundant
---
```

Not recognized: `compatibility`, `authors`, `context`, `category`, `version` at top level
(use `metadata:` for those). Unknown keys are ignored rather than rejected.

### 3.3 Progressive disclosure

1. **Discovery** (~100 tokens) — only `name` + `description` are loaded for every skill at session start.
2. **Activation** (< ~5 000 tokens) — the full `SKILL.md` body is injected when the skill triggers.
3. **Resources** — files under `scripts/`, `references/`, `assets/` load on demand via relative paths.

Keep `SKILL.md` under ~500 lines; move bulk content into bundled resources.

---

## 4. Plugins — `plugin.json`

### 4.1 Manifest discovery order (BUNDLE `extensions/discovery.rs`)

`.plugin/plugin.json` → `plugin.json` → `.github/plugin/plugin.json` → `.claude-plugin/plugin.json`

A manifest at the plugin root is valid.

### 4.2 Legacy and Agent Plugins 1.0 manifests

Without the canonical `$schema`, GitHub Copilot CLI accepts the legacy manifest fields `agents`, `skills`,
`commands`, `hooks`, `mcpServers`, `lspServers`, `outputStyles`, `postInstallMessage`, and related path
configuration. Legacy component path defaults are `agents/` and `skills/`.

Declaring the Agent Plugins 1.0 schema switches to its strict manifest contract:

```jsonc
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "…",
  "author": { "name": "…", "email": "…", "url": "…" },
  "license": "MIT",
  "repository": "https://github.com/owner/repo",
  "homepage": "https://…",
  "keywords": ["…"],
  "extensions": {
    "com.github.copilot": {}
  }
}
```

The canonical schema allows only `$schema`, `name`, `version`, `description`, `author`, `homepage`,
`repository`, `license`, `keywords`, and `extensions`. Agent Plugins 1.0 discovers skills from immediate
children of `skills/` and MCP servers from root `mcp.json`; those locations are fixed and are not declared
in `plugin.json`. GitHub Copilot's Agent Plugins 1.0 extension discovers agents from the top-level
`com.github.copilot/agents/` directory and hooks from `com.github.copilot/hooks/hooks.json`. A repository
may keep canonical sources in `agents/` and `hooks/`, but it must generate and validate the
extension-directory copies used at runtime.

Agent Plugins 1.0 `mcp.json` requires
`"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"` and `mcpServers`. Portable server
types are `stdio`, `streamable-http`, and `sse`; legacy `local` and `http` values and client-only `tools`
filters are not valid in this file.

Runtime verification against GitHub Copilot CLI 1.0.81-0 on 2026-08-19 confirmed that a schema-declaring
plugin's top-level `agents` field is ignored with a warning and agents under
`com.github.copilot/agents/` are loaded. See the repository's dated harness validation evidence.

Runtime verification on 2026-08-20 confirmed that `hooks/hooks.json` at the schema-declaring plugin root
did not fire, while the identical configuration under `com.github.copilot/hooks/hooks.json` fired on
`sessionStart`.

### 4.3 Marketplace — `marketplace.json`

Discovery (BUNDLE): `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, `.claude-plugin/marketplace.json`.

```jsonc
{
  "name": "my-marketplace",   // REQUIRED — kebab-case (letters, numbers, hyphens, dots)
  "description": "…",         // recommended — BUNDLE warns "No marketplace description provided"
  "owner": {                  // REQUIRED — owner.name REQUIRED, owner.email optional
    "name": "…", "email": "…"
  },
  "plugins": [                // REQUIRED — BUNDLE errors "Marketplace has no plugins defined" when empty
    { "name": "my-plugin", "source": "<plugin-source>", "description": "…", "version": "1.0.0" }
  ],
  "metadata": { "pluginRoot": "<plugin-root>" }
}
```

Install with `copilot plugin marketplace add <owner>/<repo>` then `/plugin install <name>`.

---

## 5. Hooks — `hooks.json`

### 5.1 Discovery and precedence

| Order | Source | Path |
| --- | --- | --- |
| 1 | Policy (admin) | `/etc/github-copilot/policy.d/*.json`, `C:\ProgramData\GitHub\Copilot\policy.d\*.json` |
| 2 | Repository | `.github/hooks/*.json` (any `*.json` filename) |
| 3 | User | `~/.copilot/hooks/*.json` |
| 4 | Repo settings | `hooks` key in `.github/copilot/settings.json` |
| 5 | User settings | `hooks` key in `~/.copilot/settings.json` |
| 6 | Legacy plugin | `<plugin-root>/hooks.json` or `<plugin-root>/hooks/hooks.json` |
| 7 | Agent Plugins 1.0 GitHub extension | `<plugin-root>/com.github.copilot/hooks/hooks.json` |

All matching sources are **merged** — every hook registered for an event runs. Policy hooks cannot be
disabled by `disableAllHooks`.

#### 5.1.1 Repository hooks require a trusted folder (MEASURED, CLI 1.0.81-0)

`.github/hooks/*.json` is **silently ignored** unless the workspace path is listed in `trustedFolders`
(`~/.copilot/config.json`). This is a security boundary: untrusted checkouts cannot execute code on
session start. User-level hooks (`~/.copilot/hooks/`, `settings.json`) fire regardless of trust.

The entry is written automatically the first time a user accepts the trust prompt in an interactive
session, so this is invisible in normal use. It only bites in **CI, containers, and `-p` automation**
using a fresh `COPILOT_HOME` — there, seed it explicitly:

```jsonc
// $COPILOT_HOME/config.json
{ "trustedFolders": ["/abs/path/to/repo"], "disableAllHooks": false }
```

Measured: identical hook file fires from `~/.copilot/hooks/` but not from `.github/hooks/` until the
folder is trusted; after trusting, it fires. No warning is emitted either way.

#### 5.1.2 `disableAllHooks` scope (MEASURED)

The key means two different things depending on where it appears:

| Location | Scope |
| --- | --- |
| `~/.copilot/config.json`, `settings.json` | **Global** — kills all repo- and user-level hooks |
| Inside a `.github/hooks/<file>.json` | **File-scoped** — disables only that file's hooks |

The file-scoped form is the supported way to ship a hook **off by default**: a sibling file with
`disableAllHooks: false` still fires normally in the same session.

#### 5.1.3 Path resolution (MEASURED)

Relative `bash` / `command` / `cwd` paths resolve against the **workspace root** (`-C` / cwd) — for
user-level hooks as well as repository ones, not against the directory holding the hook config. A
user-scope hook therefore only works in repositories that happen to contain that relative path; use an
absolute path for anything installed under `~/.copilot/hooks/`.

Hook commands that scan the working tree must also respect `timeoutSec`: the shipped `secrets-scanner`
exits 0 standalone but is killed mid-run on a large diff (536 modified files) under its configured
timeout, silently producing no log.

### 5.2 Structure

```jsonc
{
  "version": 1,               // REQUIRED
  "disableAllHooks": false,   // OPTIONAL
  "hooks": {
    "preToolUse": [
      {
        "type": "command",    // "command" | "http"
        "bash": "./script.sh",       // unix command
        "powershell": "./script.ps1",// windows command
        "command": "./script",        // cross-platform fallback
        "cwd": ".",
        "env": { "MODE": "block" },
        "timeoutSec": 30,
        "matcher": "^(bash|shell)$"  // optional tool-name filter
      }
    ]
  }
}
```

### 5.3 Valid event names (BUNDLE-confirmed, camelCase)

`sessionStart`, `sessionEnd`, `userPromptSubmitted`, `userPromptTransformed`, `preToolUse`, `postToolUse`,
`postToolUseFailure`, `preMcpToolCall`, `permissionRequest`, `preCompact`, `errorOccurred`, `agentStop`,
`subagentStart`, `subagentStop`, `notification`, `postResult`.

PascalCase aliases exist for VS Code compatibility. Note the asymmetries:
`agentStop` ↔ `Stop`, `userPromptSubmitted` ↔ `UserPromptSubmit`.
**Prefer camelCase** — it is the native Copilot CLI form.

### 5.4 I/O contract

- **stdin** — JSON payload. BUNDLE-confirmed fields include `hook_event_name`, `transcriptPath`/`transcript_path`,
  `agentName`, `agent_display_name`, `sessionId`, `toolCalls`, `toolInput`/`tool_input`, `toolResult`/`tool_result`,
  `initialPrompt`/`initial_prompt`, `prompt`, `transformedPrompt`, `custom_instructions`, `last_assistant_message`,
  `stopReason`/`stop_reason`, `errorContext`/`error_context`, `recoverable`, `timestamp`, `notification_type`.
- **exit 0** — success; stdout JSON (if any) is applied.
- **exit 2** — block (`hook exited with code 2`); stderr is surfaced to the model.
- **other non-zero** — non-blocking error, logged.
- **stdout JSON** — BUNDLE-confirmed response keys: `permissionDecision` (`allow`/`deny`/`ask`),
  `permissionDecisionReason`, `behavior`, `modifiedArgs`, `updatedInput`, `modifiedResult`, `modifiedPrompt`,
  `modifiedTransformedPrompt`, `additionalContext`, `suppressOutput`, `handled`, `handledBy`, `responseContent`,
  `interrupt`, `hookSpecificOutput`, `decision`, `reason`, `continue`.

Hook scripts must be executable (`chmod +x`).

---

## 6. Validation

For Open Horizons repository primitives, run `python3 .github/skills/validation-scripts/scripts/validate-agents.py --strict`.
This repository does not include catalog-generation, plugin-sync, or JSON-output primitive validation scripts; do not document or run those commands here.
