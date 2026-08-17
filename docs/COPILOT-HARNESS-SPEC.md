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
tools: ["read", "edit", "search"]  # OPTIONAL — omit or ["*"] = all tools; [] = no tools
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

The CLI resolves **portable aliases** (case-insensitive):

| Alias | Compatible spellings | Meaning |
| --- | --- | --- |
| `execute` | `shell`, `bash`, `powershell` | Run shell commands |
| `read` | `view`, `Read`, `NotebookRead` | Read files |
| `edit` | `write`, `create`, `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | Modify files |
| `search` | `grep`, `glob`, `Grep`, `Glob` | Search files and content |
| `agent` | `task`, `custom-agent`, `Task` | Invoke subagents |
| `web` | `web_fetch`, `web_search`, `WebSearch`, `WebFetch` | Network access |
| `todo` | `TodoWrite`, `update_todo` | Task lists |

Native CLI tool names observed in BUNDLE `definitions/*.agent.yaml`:
`grep`, `glob`, `view`, `bash`, `read_bash`, `stop_bash`, `powershell`, `read_powershell`, `stop_powershell`, `lsp`.

MCP / namespaced tools use `server/tool` or `server/*`, matching BUNDLE regex
`^([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)(?::(.+))?$` — for example `github-mcp-server/search_code`.

**VS Code-only tool names are ignored by the CLI**: `codebase`, `editFiles`, `vscodeAPI`, `openSimpleBrowser`,
`findTestFiles`, `githubRepo`, `terminalLastCommand`, `terminalSelection`, `testFailure`, `problems`, `usages`,
`changes`, `runCommands`, `runTasks`, `runTests`, `searchResults`, `extensions`, `new`, `fetch`, and their
`namespace/name` variants such as `search/codebase` or `edit/editFiles`.

> **Consequence:** an agent whose `tools:` list contains *only* VS Code names has an empty effective tool set
> in the CLI. Always include portable aliases so the agent works in both harnesses.

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
name: my-skill-name              # REQUIRED — 1-64 chars, ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$, == directory name
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

### 4.2 Manifest

```jsonc
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-plugin",          // REQUIRED — kebab-case; letters, numbers, hyphens, dots
  "version": "1.0.0",           // semver recommended
  "description": "…",           // ≤ 1024 chars
  "author": { "name": "…", "email": "…", "url": "…" },
  "license": "MIT",
  "repository": "https://github.com/owner/repo",
  "homepage": "https://…",
  "keywords": ["…"],
  "extensions": {               // Agent Plugins 1.0 client namespaces
    "com.github.copilot": { "agents": ["./agents/x.agent.md"], "skills": ["./skills/y/"] }
  }
}
```

BUNDLE-confirmed manifest keys: `$schema`, `name`, `version`, `description`, `author`, `email`, `repository`,
`license`, `homepage`, `keywords`, `extensions`, `paths`, `exclusive`, `skills`, `agents`, `commands`,
`mcpServers`, `lspServers`, `outputStyles`, `hooks`, `postInstallMessage`, `strict`.

BUNDLE error strings enforce: `Plugin name must be kebab-case (letters, numbers, hyphens, and dots)`.

Component path defaults when omitted: `agents/`, `skills/`. `${PLUGIN_DATA}` is expanded in plugin scripts.

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
    { "name": "my-plugin", "source": "./plugins/my-plugin", "description": "…", "version": "1.0.0" }
  ],
  "metadata": { "pluginRoot": "./plugins" }
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
| 6 | Plugin | `<plugin-root>/hooks.json` or `<plugin-root>/hooks/hooks.json` |

All matching sources are **merged** — every hook registered for an event runs. Policy hooks cannot be
disabled by `disableAllHooks`.

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

Run `python3 scripts/validate_primitives.py` to check every rule above.
Use `--strict` to fail on warnings and `--json` for machine-readable output.
