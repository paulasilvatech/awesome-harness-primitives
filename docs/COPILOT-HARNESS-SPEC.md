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

**Runtime observed:** CLI 1.0.81-0 discovered both `*.agent.md` and plain `*.md` files in
`.github/agents/` — see [HARNESS-VALIDATION.md](HARNESS-VALIDATION.md#agentmd-vs-md).

**Policy recommended:** this repository accepts only `^[A-Za-z0-9._-]+\.agent\.md$` for portability,
clarity, and validator consistency. Treat plain `.md` agent discovery as runtime tolerance, not as an
authoring target.

### 1.2 Frontmatter

```yaml
---
name: my-agent                     # OPTIONAL — defaults to filename
description: >-                    # REQUIRED — the only truly required field
  What the agent does and when to select it.
tools: ["read", "grep", "glob", "edit"]  # OPTIONAL allow-list — omit or ["*"] = all tools. Not "search"/"web": see §1.3
model: claude-sonnet-4.5           # OPTIONAL — string or prioritized array
target: github-copilot             # OPTIONAL — VS Code/static metadata; CLI warns and ignores it
user-invocable: true               # OPTIONAL — default true; false hides from /agent picker
disable-model-invocation: false    # OPTIONAL — default false; true blocks auto-delegation
mcp-servers:                       # OPTIONAL — CLI/cloud only, ignored by VS Code; each server requires tools
  my-server:
    type: local                    # "local" | "stdio" | "http" | "sse"
    command: my-cmd
    args: ["--flag"]
    env: { TOKEN: "${{ secrets.TOKEN }}" }
    tools: ["*"]
argument-hint: "<path>"            # OPTIONAL — VS Code only; CLI warns and ignores it
handoffs: []                       # OPTIONAL — VS Code only; CLI warns and ignores it
agents: ["reviewer"]               # OPTIONAL — VS Code subagent allow-list; requires the agent tool
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
| `target` | ignored (debug warning) | optional | Accepted but not a recognized CLI runtime field; see warning matrix |
| `user-invocable` | optional | optional | BUNDLE-confirmed key |
| `disable-model-invocation` | optional | optional | BUNDLE-confirmed key |
| `mcp-servers` | optional | ignored | BUNDLE-confirmed key; every server entry requires `tools` |
| `argument-hint` | ignored (debug warning) | optional | VS Code only |
| `handoffs` | ignored (debug warning) | optional | VS Code only |
| `agents` | unverified in tested CLI | optional | VS Code subagent allow-list; include `agent` in an explicit `tools` allow-list |
| `infer` | **RETIRED** | **RETIRED** | Replace with the two fields above |
| `mode`, `hidden`, `agent`, `title` | **not an agent field** | — | Remove |

Body: Markdown, **max 30 000 characters**.

**Runtime observed:** recognized CLI fields are accepted with no warning. Unknown frontmatter keys are
accepted but ignored with debug-log warnings, not terminal output; for example `target` logs
`unknown field ignored: target`. A malformed `mcp-servers` entry without per-server `tools` logs
`custom agent markdown frontmatter is malformed: mcp-servers.probe-server.tools: Required`. See
[HARNESS-VALIDATION.md](HARNESS-VALIDATION.md#frontmatter-warning-matrix).

Unrecognized tool names are different: they are **silently ignored** with no warning, so a misspelled
tool list can still degrade capability silently.

### 1.3 `tools:` vocabulary

`tools:` is an **allow-list filter**, not an additive grant. Omitting it gives the agent the full tool set;
declaring it restricts the agent to the listed tokens. **Unrecognized tokens are silently dropped with no
warning**, so a typo or a VS Code-only name quietly removes capability instead of failing loudly.

Every row below was measured against CLI 1.0.81-0 by declaring a single token and dumping the resulting
tool schema — see [HARNESS-VALIDATION.md](HARNESS-VALIDATION.md).

**Always-on floor** (present even when every token is invalid): `skill`, `sql`.

| Token | Net tools granted beyond the floor |
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

> **No-op tokens in the tested Copilot CLI — these grant nothing and are enforced as errors by rule
> `AG017` for cross-surface agents:**
> `search`, `web`, `todo`, `all`, `terminal`, `run`, `codebase`, `changes`, `fetch`, `githubRepo`, `search/codebase`.
>
> `search` is the dangerous one: it reads as "let this agent search code" but grants **no** search capability.
> Use `grep` and `glob` explicitly. Likewise use `web_fetch` and `web_search` instead of `web`.
> `todo` is unnecessary because the `sql` tool that backs task lists is always in the floor.
>
> First-party VS Code and GitHub cloud-agent documentation reverified on 2026-08-21 documents `search`,
> `web`, and `todo` aliases. A deliberately `target: vscode` agent may use those aliases, but a
> cross-surface agent must retain the measured CLI-safe spellings until a newer CLI runtime probe changes
> this evidence.
>
> `sql` and `skill` are also no-ops as tokens, but harmlessly so — they are already in the floor.
>
> Rule `AG024` extends this to prose: an agent body that presents these tokens inside a usable tool
> list is flagged, because agents that document tool lists propagate them into the agents they
> generate. Naming a token in order to reject, hedge, or historicize it is the correct pattern and is
> not flagged, and fenced blocks are skipped so source samples and MCP server configuration whose
> arrays legitimately contain `run` or `search` stay silent.

MCP / namespaced tools use `server/tool` or `server/*`, matching BUNDLE regex
`^([a-zA-Z0-9_.-]+/(?:\*|[a-zA-Z0-9_.-]+))(?::(.+))?$` — for example `github-mcp-server/search_code`.

**Recommendation.** For a general-purpose agent, omit `tools:` entirely (or use `["*"]`) so it keeps full
capability as the CLI adds tools. Declare an explicit list only when you deliberately want to restrict the
agent, and then always spell out `grep`/`glob`/`web_fetch`/`web_search` rather than the alias-looking no-ops.

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

**Runtime observed:** CLI 1.0.81-0 accepted a project skill whose frontmatter `name` differed from its
directory and listed it by frontmatter name — see
[HARNESS-VALIDATION.md](HARNESS-VALIDATION.md#skill-name-vs-directory-mismatch).

**Policy recommended:** this repository still requires `name == directory` because that is the bundled
generation guidance and validator policy.

```yaml
---
name: my-skill-name              # REQUIRED — 1-64 chars, ^(?:[a-z0-9]|[a-z0-9][a-z0-9-]*[a-z0-9])$, == directory name
description: >-                  # REQUIRED — 1-1024 chars, must state WHAT and WHEN
  What this skill does. Use this skill when <trigger conditions>.
user-invocable: true             # OPTIONAL — BUNDLE-confirmed
disable-model-invocation: false  # OPTIONAL — BUNDLE-confirmed
allowed-tools: ["view", "grep"]  # OPTIONAL — pre-approved tools
argument-hint: "<arg>"           # OPTIONAL — BUNDLE-confirmed; body may use $ARGUMENTS
compatibility: "Requires az CLI" # OPTIONAL — Agent Skills standard, 1-500 chars
license: MIT                     # OPTIONAL
metadata: { author: "…" }        # OPTIONAL — string→string map
tags: ["ci", "deploy"]           # OPTIONAL — add only when useful and non-redundant
---
```

`compatibility` is defined by the Agent Skills standard (max 500 characters) and verified on
2026-08-25 against the [Agent Skills specification](https://agentskills.io/specification). The
current VS Code Agent Skills reference does not list it, and BUNDLE does not act on it, so treat it
as portable documentation only and repeat any blocking prerequisite in the skill body — see
[HARNESS-VALIDATION.md](HARNESS-VALIDATION.md#agent-skills-compatibility-field-verification).

Not recognized: `authors`, `context`, `category`, `version` at top level
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

### 4.2 Flat GitHub Copilot plugin manifests

This repository packages GitHub Copilot plugins with the direct layout documented by GitHub. The
distributed manifest omits `$schema` and points to components located directly under the plugin root:

```jsonc
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "…",
  "author": { "name": "…", "email": "…", "url": "…" },
  "license": "MIT",
  "repository": "https://github.com/owner/repo",
  "homepage": "https://…",
  "keywords": ["…"],
  "agents": "agents/",
  "skills": "skills/",
  "hooks": "hooks/safety/hooks.json",
  "extensions": ["extensions/my-extension"],
  "mcpServers": "mcp.json"
}
```

Supported component fields include `agents`, `skills`, `commands`, `hooks`, `extensions`,
`mcpServers`, and `lspServers`. GitHub documents `agents/` and `skills/` as default paths. This
repository uses explicit direct paths and prohibits a committed `com.github.copilot/` directory.

Shared canonical agents and skills are materialized into the package's direct directories by
`sync_plugin_components.py`. Plugin-owned content remains canonical in the same direct directories.
Repository-only ownership, shared-source references, imported extension provenance, and mixed
`sharedSkills` configuration live in `harness/github-copilot/manifests/plugin-sources.json`; this
metadata is not distributed in `plugin.json`.

Root `mcp.json` retains the portable Agent Plugins MCP schema:
`"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"` and `mcpServers`. Portable server
types are `stdio`, `streamable-http`, and `sse`; legacy `local` and `http` values and client-only `tools`
filters are not valid in this file. The flat manifest declares it through
`"mcpServers": "mcp.json"`. Runtime verification on 2026-08-22 confirmed that direct agents, skills,
hooks, extensions, and this MCP configuration install without a namespaced mirror; see
`docs/HARNESS-VALIDATION.md`.

The portable Agent Plugins 1.0 specification itself standardizes only skills and MCP servers. It permits
reverse-domain client extension directories, but this repository intentionally targets GitHub Copilot's
documented flat package contract for GitHub-specific agents, hooks, and extensions.

### 4.3 Plugin classification

`plugin.json` carries no maturity, tier, status, or category field: unsupported top-level keys fail rule
`PL007`, and `keywords` is a discovery taxonomy that must not double as governance. Classification
therefore lives in the canonical `harness/github-copilot/manifests/plugin-sources.json` under an optional
`governance` object and is projected into `docs/PLUGIN-AUDIT.md` and `docs/CATALOG.md` by the shared
classifier `harness/github-copilot/scripts/_plugin_governance.py`.

`governance` accepts only `lifecycle`, `lastRuntimeProbe`, and `evidence`. A probe date requires evidence,
and a `deprecated` lifecycle requires evidence. Because it is repository governance rather than
distribution metadata, `normalize_plugin_manifests.py` never copies it into `plugin.json`.

| Axis | Values | Derivation |
| --- | --- | --- |
| Lifecycle | `active`, `incubating`, `deprecated` | `incubating` is derived from a `0.x` manifest version. `deprecated` is an explicit, evidence-backed override. `active` is the default. |
| Assurance | `runtime-verified`, `runtime-stale`, `runtime-required`, `static-validated` | A dated representative probe within 90 days is `runtime-verified` and becomes `runtime-stale` afterwards. Packages shipping MCP servers, hooks, or client extensions are `runtime-required` until probed, because static checks never exercise those surfaces. |
| Provenance | `repository`, `upstream-mirror` | `upstream-mirror` requires both `upstreamRepository` and a pinned `upstreamCommit`. |

Classification is descriptive and is never authority to remove, hide, or block a package. A deprecated or
unprobed package remains installable. Installing a marketplace entry is not evidence of runtime behavior:
`runtime-verified` requires a representative activation, such as an agent invocation, a hook decision, or
an MCP server exposure, recorded with a date in `docs/HARNESS-VALIDATION.md`.

### 4.4 Marketplace — `marketplace.json`

Discovery (BUNDLE): `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, `.claude-plugin/marketplace.json`.

```jsonc
{
  "name": "my-marketplace",   // REQUIRED — kebab-case (letters, numbers, hyphens, dots)
  "description": "…",         // recommended — BUNDLE warns "No marketplace description provided"
  "owner": {                  // REQUIRED — owner.name REQUIRED, owner.email optional
    "name": "…", "email": "…"
  },
  "plugins": [                // REQUIRED — BUNDLE errors "Marketplace has no plugins defined" when empty
    { "name": "my-plugin", "source": "./harness/github-copilot/plugins/my-plugin", "description": "…", "version": "1.0.0" }
  ],
  "metadata": { "pluginRoot": "./harness/github-copilot/plugins" }
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
| 6 | Plugin | Path declared by `hooks`, conventionally `<plugin-root>/hooks.json` or a file under `<plugin-root>/hooks/` |

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
folder is trusted; after trusting, it fires. No warning is emitted either way — see
[HARNESS-VALIDATION.md](HARNESS-VALIDATION.md).

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

Run `python3 harness/github-copilot/scripts/validate_primitives.py` to check every rule above plus this repository's
mandatory body contracts. The validator also checks `harness/github-copilot/prompts/*.prompt.md` against the local VS
Code prompt policy: metadata and section structure are validated statically, but prompt execution still
requires **Chat: Run Prompt** in VS Code.

Use `--strict` to fail on warnings, `--json` for machine-readable output, and
`--kind <agents|instructions|skills|prompts|plugins|hooks>` for a focused check.

Frontmatter rules cover what an agent declares; `AG024` additionally scans the agent body for no-op or
legacy tool tokens taught as usable tool lists. Agent rules apply to the flat `agents/` tree and to
plugin-owned agents under `plugins/<name>/agents/`; library copies are skipped because they are generated
from a canonical source that is already validated. The capability audit classifies each agent's stated
authority against its declared tools: a read-only agent that inherits every tool is blocking, while a
bounded-write agent that inherits every tool enters a review queue, because a policy that scopes which
files an agent may touch cannot be expressed as a tool allow-list. Declaring `tools: ["*"]` is the explicit
way to record that full inheritance is deliberate.

Generated distribution surfaces have separate drift gates:

```sh
python3 harness/github-copilot/scripts/normalize_plugin_manifests.py --check
python3 harness/github-copilot/scripts/audit_plugins.py --check
python3 harness/github-copilot/scripts/audit_primitive_content.py --check
python3 harness/github-copilot/scripts/audit_primitive_capabilities.py --check
python3 harness/github-copilot/scripts/audit_primitive_redundancy.py --check
python3 harness/github-copilot/scripts/generate_catalog.py --check
python3 harness/github-copilot/scripts/sync_plugin_components.py --check
python3 harness/github-copilot/scripts/sync_installed_primitives.py --check
```
