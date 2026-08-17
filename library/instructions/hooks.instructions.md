---
applyTo: ".github/hooks/**,hooks/**"
description: "Enforces portable hook conventions for discovery, trust, configuration, scripts, events, payloads, blocking, examples, security, packaging, and cross-surface behavior."
---

# Hook Authoring Conventions — Safe Lifecycle Automation

This file applies to repository and reusable hook configurations and scripts under `.github/hooks/**` and `hooks/**`. It is authoritative for safe, fast, deterministic hook design, discovery, trust behavior, path resolution, config fields, script contracts, payload parsing, exit codes, blocking semantics, event usage, examples, portability, packaging, and anti-patterns; the official GitHub Copilot hooks reference wins for current payload schemas and host support, while repository security policy wins where it is stricter.

Hooks are **small, deterministic commands or scripts** that run at specific lifecycle events. An awesome hook does one clear job, runs quickly, and makes its side effects explicit.

## Folder Structure

A GitHub Copilot hook lives in `.github/hooks/` inside your repository:

```text
.github/
└── hooks/
    ├── block-dangerous-commands.json   ← hook config (which event, which script, options)
    └── scripts/
        ├── block-dangerous-commands.sh  ← Bash implementation
        └── block-dangerous-commands.ps1 ← PowerShell implementation (optional if Bash-only)
```

You can have multiple `.json` files — each one registers hooks for one or more events. The host loads all of them.

## Discovery, Trust, and Path Resolution

- Repository hooks in `.github/hooks/*.json` run only when the workspace is trusted. In non-interactive CLI or CI runs with a fresh `COPILOT_HOME`, seed `$COPILOT_HOME/config.json` with `{"trustedFolders":["/abs/path/to/repo"],"disableAllHooks":false}`; otherwise repository hooks are silently skipped.
- User-level hooks and hooks in user settings are not gated by repository trust.
- `disableAllHooks` in `config.json` or settings is a global kill switch for repo- and user-level hooks. The same key inside one `.github/hooks/<file>.json` is file-scoped and disables only that file's hooks; sibling hook files still run.
- Relative `bash`, `command`, and `cwd` paths resolve from the workspace root (`-C` / current working directory), not from the hook config file's directory. Use absolute paths for user-level hooks that must work across repositories.

## The Config File

Each `.json` file maps events to an array of hook entries.

- **Command hooks** (`type: "command"`): run a local script. The host passes event JSON on stdin, your script responds through exit code and stdout.
- **HTTP hooks** (`type: "http"`): call an HTTP endpoint with the event payload when supported by the host. Treat network hooks as higher risk: bound them with timeouts, avoid sending private code or prompts to third parties, and document what leaves the machine.

### Config example

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "matcher": "bash",
        "type": "command",
        "bash": "./.github/hooks/scripts/block-dangerous-commands.sh",
        "powershell": "./.github/hooks/scripts/block-dangerous-commands.ps1",
        "cwd": ".",
        "timeoutSec": 5,
        "env": {
          "BLOCK_MODE": "deny"
        }
      }
    ]
  }
}
```

### Config fields

| Field | Required | What it does |
| ---- | ---- | ---- |
| `type` | yes | `"command"` for scripts or `"http"` for HTTP hooks |
| `matcher` | no | Optional host-level filter by tool name. The field is documented by the spec, but the current repository validation did not verify matcher behavior in CLI 1.0.81-0; keep in-script filtering as the reliable fallback. |
| `bash` | one or both | Command line invoked on Unix / Bash-capable hosts |
| `powershell` | one or both | Command line invoked on Windows / PowerShell-capable hosts |
| `cwd` | no | Working directory, relative to repo root |
| `timeoutSec` | no | Max seconds before the host kills the process (default 30) |
| `env` | no | Extra process environment variables passed to the script |
| `url`, `headers`, `allowedEnvVars` | HTTP only | Endpoint and request controls for HTTP hooks |

### Matchers: documented, not yet validated here

Without a verified matcher, every `preToolUse` hook may fire on **every** tool call. Keep defensive boilerplate like:

```bash
tool_name="$(printf '%s' "$payload" | jq -r '.toolName // .tool_name // .toolInput.name // .tool_input.name // ""')"
[[ "$tool_name" != "bash" ]] && exit 0
```

If a future validated host applies `matcher`, it can skip irrelevant process spawns. Until then, treat `matcher` as an optimization only, not a correctness or security boundary.

If your hooks must work on multiple Copilot surfaces or versions, keep the in-script filtering as a fallback even when using matchers.

### `env` — static configuration for your script

`env` is a **standard host field**. The keys inside it are **author-defined variables** — you choose the names and values.

They arrive as **process environment variables**, not inside the stdin JSON payload. Use them for static configuration that should not be hardcoded:

| Pattern | Example |
| ---- | ---- |
| Mode flag | `"BLOCK_MODE": "deny"` — same script logs in one repo, blocks in another |
| Threshold | `"MAX_CHANGED_FILES": "20"` |
| Path | `"AUDIT_LOG_PATH": ".github/logs/hooks.log"` |
| Feature toggle | `"ENABLE_NOTIFICATIONS": "false"` |

### `bash` and `powershell` — when to provide one or both

The host picks whichever entry matches the current environment. It does not run both, and does not fall back from one to the other.

| Situation | Provide |
| ---- | ---- |
| Private hook, one known platform | Only that platform's entry |
| Published hook claiming cross-platform support | Both entries |
| Single cross-platform runtime (Python, Node, pwsh) | Expose the same script through both entries |
| Bash-only dependency | `bash` only |
| Windows-only dependency | `powershell` only |

Cross-platform example using Python through both entries:

```json
{
  "type": "command",
  "bash": "python3 ./.github/hooks/scripts/check.py",
  "powershell": "python .\\.github\\hooks\\scripts\\check.py"
}
```

## The Script Contract

Every hook script follows the same basic contract: read JSON from stdin, do work, and respond through exit code, stdout, and stderr.

**Important**: payloads vary by event and surface. CLI payloads observed in the bundle include aliases such as `hook_event_name`, `transcriptPath`/`transcript_path`, `agentName`, `agent_display_name`, `sessionId`, `toolCalls`, `toolInput`/`tool_input`, `toolResult`/`tool_result`, `initialPrompt`/`initial_prompt`, `prompt`, `transformedPrompt`, `custom_instructions`, `last_assistant_message`, `stopReason`/`stop_reason`, `errorContext`/`error_context`, `recoverable`, `timestamp`, and `notification_type`. Tool arguments may appear as `toolArgs`/`tool_args` JSON strings or as `toolInput`/`tool_input` objects; validate and parse the fields you actually use.

### Reading stdin and responding — Bash and PowerShell

**Bash**:

```bash
#!/usr/bin/env bash
set -euo pipefail
command -v jq >/dev/null 2>&1 || { echo "jq is required by this hook" >&2; exit 2; }
payload="$(cat)"
tool_name="$(printf '%s' "$payload" | jq -r '.toolName // .tool_name // .toolInput.name // .tool_input.name // ""')"
command="$(printf '%s' "$payload" | jq -r '(.toolArgs // .tool_args // .toolInput // .tool_input // "{}") | if type == "string" then (fromjson? // {}) else . end | .command // ""')"
```

**PowerShell**:

```powershell
Set-StrictMode -Version Latest
$payload = [Console]::In.ReadToEnd() | ConvertFrom-Json
$toolArgs = if ($payload.toolArgs) { $payload.toolArgs | ConvertFrom-Json } elseif ($payload.toolInput) { $payload.toolInput } else { @{} }
$command = $toolArgs.command
```

To deny in `preToolUse` (PowerShell):

```powershell
@{ permissionDecision = 'deny'; permissionDecisionReason = 'Blocked by policy' } |
    ConvertTo-Json -Compress
exit 0
```

### What the script receives

| Input | What it carries |
| ---- | ---- |
| `stdin` | One JSON payload describing the current event |
| process environment | Normal env vars plus any you defined under `env` in the config |
| working directory | `cwd` from the config, or the host default |

### How the script responds

| Channel | Purpose |
| ---- | ---- |
| exit `0` | Script succeeded — host continues unless stdout carried a structured deny |
| exit `2` | Blocks the triggering action; stderr is surfaced to the model |
| other non-zero exit | Non-blocking hook error, logged by the host |
| `stdout` | Structured machine-readable output — only for events that document a stdout schema (like `preToolUse`) |
| `stderr` | Human-readable diagnostics for logs |

### Exit codes and deny: the full picture

The deny mechanism **depends on the event**:

| Event type | How to allow | How to deny / block |
| ---- | ---- | ---- |
| `preToolUse` | exit `0`, empty or `{"permissionDecision":"allow"}` on stdout | **Preferred**: exit `0` + `{"permissionDecision":"deny","permissionDecisionReason":"..."}` on stdout — gives the host a reason to show. **Also works**: exit `2` blocks the tool call, but without a structured reason. |
| `userPromptSubmitted` | exit `0` | exit `2` blocks the prompt (stdout is ignored for this event) |
| `agentStop` | exit `0` | exit `2` blocks the action |
| Other events (`sessionStart`, `sessionEnd`, `postToolUse`, `errorOccurred`) | exit `0` | exit `2` is the only blocking code; other non-zero codes are non-blocking errors |

**Rule of thumb**: if the event has a structured stdout schema (like `preToolUse`), use it — it gives a clean reason. Use exit `2` when the hook must fail closed before it can produce structured output. Do not rely on exit `1` or other non-zero codes to block.

### Example 1: Commit gate — block commits until lint, types, and tests pass

**Why this pattern matters**: the deny reason includes the actual errors, so the agent sees what's broken and fixes it before trying again. This creates a self-correcting feedback loop — the most powerful thing hooks can do.

**Event**: `preToolUse` — fires before the agent runs `git commit`

**Config** — `.github/hooks/commit-gate.json`:

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "./.github/hooks/scripts/commit-gate.sh",
        "cwd": ".",
        "timeoutSec": 120
      }
    ]
  }
}
```

**Script** — `.github/hooks/scripts/commit-gate.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

command -v jq >/dev/null 2>&1 || { echo "jq is required to evaluate commit policy" >&2; exit 2; }
payload="$(cat)"
tool_name="$(printf '%s' "$payload" | jq -r '.toolName // .tool_name // .toolInput.name // .tool_input.name // ""')"

# Only gate bash commands that are git commits
if [[ "$tool_name" != "bash" ]]; then exit 0; fi
command="$(printf '%s' "$payload" | jq -r '(.toolArgs // .tool_args // .toolInput // .tool_input // "{}") | if type == "string" then (fromjson? // {}) else . end | .command // ""')"
if ! printf '%s' "$command" | grep -q "git commit"; then exit 0; fi

CWD="$(printf '%s' "$payload" | jq -r '.cwd // "."')"
ERRORS=""

# 1. TypeScript type check
if [[ -f "$CWD/tsconfig.json" ]]; then
  TSC_OUT=$(cd "$CWD" && npx tsc --noEmit 2>&1) || ERRORS="${ERRORS}
=== TypeScript Errors ===
$(echo "$TSC_OUT" | head -30)"
fi

# 2. Lint
if [[ -f "$CWD/package.json" ]]; then
  HAS_LINT=$(jq -r '.scripts.lint // empty' "$CWD/package.json" 2>/dev/null)
  if [[ -n "$HAS_LINT" ]]; then
    LINT_OUT=$(cd "$CWD" && npm run lint --silent 2>&1) || ERRORS="${ERRORS}
=== Lint Errors ===
$(echo "$LINT_OUT" | tail -30)"
  fi

  # 3. Tests
  HAS_TEST=$(jq -r '.scripts.test // empty' "$CWD/package.json" 2>/dev/null)
  if [[ -n "$HAS_TEST" ]]; then
    TEST_OUT=$(cd "$CWD" && CI=true npm test -- --watchAll=false 2>&1) || ERRORS="${ERRORS}
=== Test Failures ===
$(echo "$TEST_OUT" | tail -30)"
  fi
fi

if [[ -n "$ERRORS" ]]; then
  jq -nc --arg reason "Cannot commit — fix these issues first:
$ERRORS" \
    '{permissionDecision:"deny",permissionDecisionReason:$reason}'
fi
exit 0
```

**What happens at runtime:**

| Scenario | stdout | exit | Host action |
| ---- | ---- | ---- | ---- |
| All checks pass | empty | `0` | Commit proceeds |
| Lint fails | `{"permissionDecision":"deny","permissionDecisionReason":"Cannot commit — fix these issues first:\n=== Lint Errors ===\n..."}` | `0` | Blocks commit; agent sees the errors and fixes them |
| jq missing | empty | `2` | Blocks fail-closed because the policy cannot be evaluated |

### Example 2: Auto-format after file edits

**Why this pattern matters**: the agent writes code, and your formatter runs immediately after — no manual step needed. The agent's next read of that file sees the formatted version.

**Event**: `postToolUse` — fires after `edit` or `create` tool calls

**Config** — `.github/hooks/format-on-save.json`:

```json
{
  "version": 1,
  "hooks": {
    "postToolUse": [
      {
        "type": "command",
        "bash": "./.github/hooks/scripts/format-on-save.sh",
        "cwd": ".",
        "timeoutSec": 15
      }
    ]
  }
}
```

**Script** — `.github/hooks/scripts/format-on-save.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

command -v jq >/dev/null 2>&1 || { echo "jq is required by format-on-save hook" >&2; exit 1; }
payload="$(cat)"
tool_name="$(printf '%s' "$payload" | jq -r '.toolName // .tool_name // .toolInput.name // .tool_input.name // ""')"
result_type="$(printf '%s' "$payload" | jq -r '.toolResult.resultType // .tool_result.resultType // .tool_result.result_type // ""')"

# Only format after successful file writes
case "$tool_name" in
  edit|create) ;;
  *) exit 0 ;;
esac
[[ "$result_type" != "success" ]] && exit 0

file_path="$(printf '%s' "$payload" | jq -r '(.toolArgs // .tool_args // .toolInput // .tool_input // "{}") | if type == "string" then (fromjson? // {}) else . end | .path // ""')"
[[ -z "$file_path" || ! -f "$file_path" ]] && exit 0

# Run the project's formatter — adapt to your stack
if command -v npx >/dev/null 2>&1 && [[ -f "package.json" ]]; then
  npx prettier --write "$file_path" 2>/dev/null || true
elif command -v dotnet >/dev/null 2>&1 && [[ "$file_path" == *.cs ]]; then
  dotnet format --include "$file_path" 2>/dev/null || true
fi
exit 0
```

**What happens at runtime:**

| Scenario | What the hook does | exit |
| ---- | ---- | ---- |
| Agent edits `src/app.ts` successfully | Runs `prettier --write src/app.ts` | `0` |
| Agent runs `bash ls` | Skips (not a file-writing tool) | `0` |
| Prettier not installed | Silently skips formatting | `0` |

### Example 3: Block dangerous commands with structured deny

**Why this pattern matters**: the simplest guardrail — prevent destructive shell commands before they execute, with a clear reason the agent can read.

**Event**: `preToolUse` — fires before any tool call

**Config** — `.github/hooks/block-dangerous.json`:

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "./.github/hooks/scripts/block-dangerous.sh",
        "cwd": ".",
        "timeoutSec": 5,
        "env": {
          "BLOCK_MODE": "deny"
        }
      }
    ]
  }
}
```

**Script** — `.github/hooks/scripts/block-dangerous.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

command -v jq >/dev/null 2>&1 || { echo "jq is required to evaluate command policy" >&2; exit 2; }
payload="$(cat)"
block_mode="${BLOCK_MODE:-log}"
tool_name="$(printf '%s' "$payload" | jq -r '.toolName // .tool_name // .toolInput.name // .tool_input.name // ""')"

[[ "$tool_name" != "bash" ]] && exit 0

command="$(printf '%s' "$payload" | jq -r '(.toolArgs // .tool_args // .toolInput // .tool_input // "{}") | if type == "string" then (fromjson? // {}) else . end | .command // ""')"

if printf '%s' "$command" | grep -qE 'rm -rf /|git reset --hard|git clean -fd|git push.*--force'; then
  # Truncate command to avoid leaking secrets in deny reason or logs
  short_cmd="$(printf '%.80s' "$command")"
  if [[ "$block_mode" == "deny" ]]; then
    jq -cn --arg reason "Destructive command blocked: ${short_cmd}..." \
      '{permissionDecision:"deny",permissionDecisionReason:$reason}'
  else
    echo "Would block: ${short_cmd}..." >&2
  fi
fi
exit 0
```

**What happens at runtime:**

| Scenario | BLOCK_MODE | stdout | exit | Host action |
| ---- | ---- | ---- | ---- | ---- |
| Safe command | any | empty | `0` | Proceeds |
| `git push --force` | `deny` | `{"permissionDecision":"deny",...}` | `0` | Blocks with reason |
| `git push --force` | `log` | empty | `0` | Proceeds (log only) |

## Event Types

The full hooks reference is authoritative. **Always check it for the latest payload shapes** before writing a hook:

- Hooks configuration reference
- About hooks

| Event | stdout | Typical use |
| ---- | ---- | ---- |
| `sessionStart` | **parsed** — `additionalContext` in stdout is injected into the session | Setup, validation, context injection, logging |
| `sessionEnd` | ignored | Cleanup, summaries |
| `userPromptSubmitted` | ignored | Auditing, prompt blocking |
| `preToolUse` | **parsed** — `permissionDecision`, `modifiedArgs`/`updatedInput`, `additionalContext` | Guardrails, deny/block, argument modification |
| `postToolUse` | ignored | Logging, formatting |
| `postToolUseFailure` | — | Recovery after a failed tool run |
| `preMcpToolCall` | — | MCP-specific guardrails |
| `userPromptTransformed` | — | Prompt transformation audit |
| `agentStop` | — | Final validation |
| `subagentStart` | — | Subagent audit |
| `subagentStop` | — | Subagent output validation |
| `errorOccurred` | ignored | Diagnostics, alerts |
| `preCompact` | — | Pre-compaction work |
| `permissionRequest` | — | Approval workflow |
| `notification` | — | Notification handling |
| `postResult` | — | Final result handling |

The spec documents additional camelCase events that older samples may omit. Prefer camelCase names: `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `userPromptTransformed`, `preToolUse`, `postToolUse`, `postToolUseFailure`, `preMcpToolCall`, `permissionRequest`, `preCompact`, `errorOccurred`, `agentStop`, `subagentStart`, `subagentStop`, `notification`, and `postResult`.

### Payload schemas for common events

These are the payload shapes from the hooks reference. Always verify against the official hooks configuration reference for the latest fields.

**`sessionStart`**

```json
{
  "timestamp": 1704614400000,
  "cwd": "/path/to/project",
  "source": "new",
  "initialPrompt": "Create a new feature"
}
```

`source` is `"new"`, `"resume"`, or `"startup"`. `initialPrompt` is the user's first prompt if provided.

**`sessionStart` stdout output** — the host parses stdout for:

```json
{
  "additionalContext": "Current branch: main. Deploy target: staging."
}
```

`additionalContext` is injected directly into the session conversation, letting hooks provide environment-specific context dynamically.

**`sessionEnd`**

```json
{
  "timestamp": 1704618000000,
  "cwd": "/path/to/project",
  "reason": "complete"
}
```

`reason` is `"complete"`, `"error"`, `"abort"`, `"timeout"`, or `"user_exit"`.

**`userPromptSubmitted`**

```json
{
  "timestamp": 1704614500000,
  "cwd": "/path/to/project",
  "prompt": "Fix the authentication bug"
}
```

The field is `prompt` — the exact text the user submitted.

**`preToolUse`**

```json
{
  "timestamp": 1704614600000,
  "cwd": "/path/to/project",
  "toolName": "bash",
  "toolArgs": "{\"command\":\"rm -rf dist\",\"description\":\"Clean build directory\"}",
  "toolInput": {
    "command": "rm -rf dist",
    "description": "Clean build directory"
  }
}
```

Observed payloads may use `toolName` plus `toolArgs` as a JSON string, or `toolInput`/`tool_input` as an object. Parse defensively and support aliases where practical.

**`preToolUse` stdout output** — the host parses stdout for:

| Field | What it does |
| ---- | ---- |
| `permissionDecision` | `"deny"` blocks the tool call. `"allow"` and `"ask"` also accepted; only `"deny"` is currently processed. |
| `permissionDecisionReason` | Human-readable reason shown to the user |
| `modifiedArgs` or `updatedInput` | Replacement tool arguments — used instead of the originals |
| `additionalContext` | Text injected into the agent's context for this turn |

**`postToolUse`**

```json
{
  "timestamp": 1704614700000,
  "cwd": "/path/to/project",
  "toolName": "bash",
  "toolArgs": "{\"command\":\"npm test\"}",
  "toolInput": {
    "command": "npm test"
  },
  "toolResult": {
    "resultType": "success",
    "textResultForLlm": "All tests passed (15/15)"
  }
}
```

`resultType` is `"success"`, `"failure"`, or `"denied"`.

**`errorOccurred`**

```json
{
  "timestamp": 1704614800000,
  "cwd": "/path/to/project",
  "error": {
    "message": "Network timeout",
    "name": "TimeoutError",
    "stack": "TimeoutError: Network timeout\n    at ..."
  }
}
```

**`agentStop`**

```json
{
  "timestamp": 1704618000000,
  "cwd": "/path/to/project"
}
```

Minimal payload — use it to trigger end-of-session actions like running `git diff --stat` or final validation.

## When Hooks Are the Wrong Tool

| Avoid hooks for | Better fit |
| ---- | ---- |
| Open-ended reasoning or style guidance | Instructions, prompts, or agents |
| Long multi-step workflows with memory, retries, or branching | Agents, scripts, or workflow engines |
| Background daemons, watchers, debounce loops, or async jobs | Dedicated automation, services, or CI |
| Heavy repository-wide validation | CI, scheduled jobs, or dedicated automation |

## Universal Design Rules

| Rule | Why it matters |
| ---- | ---- |
| One hook, one responsibility | Small hooks are easier to trust and debug |
| Default to **observe first** | Blocking or mutation should be an explicit choice |
| Keep hooks synchronous, bounded, and non-interactive | Hooks run in the critical path |
| Make hooks deterministic and idempotent | Re-runs should not create drift |
| Do not mutate branch, index, or worktree state by default | Git-destructive behavior is high risk |
| Treat prompts, tool arguments, and tool output as untrusted and sensitive | Input may be hostile or private |
| Redact secrets, credentials, tokens, and private content from logs | Logs often outlive the hook run |

## Script Authoring Rules

- Validate the JSON fields you actually use
- Quote shell variables and never build commands from raw input
- Keep stdout clean unless the host requires structured output
- Use strict modes: Bash `set -euo pipefail`, PowerShell `Set-StrictMode -Version Latest`
- Check dependencies early and fail clearly if they are missing
- Avoid prompts, hidden installs, or environment mutation during execution
- Test scripts by piping representative JSON payloads into them manually

## Choose the Smallest Viable Implementation

1. **PowerShell 7**, **Node.js**, or **Python** for broadly portable hooks
2. **Bash** where Bash is an explicit requirement or safe assumption
3. **An existing project CLI** when the repository already depends on it

Do **not** introduce a new compiled runtime just to implement an ordinary hook.

## Packaging a Reusable Hook

- Package config, scripts, and docs together
- Document the trigger event, purpose, side effects, dependencies, and disable path
- Explain what the hook reads, what it writes, and what it blocks

## Anti-Patterns

- Long-running hooks, watchers, background daemons, or fire-and-forget async work
- Heavy scans on every event when a narrower trigger would do
- Hidden network calls or uploads in the critical path
- Silent mutation of Git state (checkout, reset, clean, stash, stage, commit, push, or history rewriting) by default
- Interactive prompts or implicit approval steps
- Noisy stdout, ad-hoc output formats, or mixed machine/human output
- Logging raw prompts, secrets, credentials, or large tool outputs
- Monolithic hooks that mix unrelated responsibilities

## Portability

### GitHub Copilot: CLI, VS Code, and Cloud Agent

The same `.github/hooks/*.json` shape is intended to be portable across CLI, VS Code, and the cloud agent, but do not assume byte-identical payloads or identical discovery behavior on every surface. The CLI measurements in this repository are authoritative for CLI behavior; qualify VS Code/cloud claims unless you have tested them on those surfaces. Event names accept both camelCase (`preToolUse`) and PascalCase (`PreToolUse`), but prefer camelCase. Tool arguments may arrive as `toolArgs`/`tool_args` JSON strings or `toolInput`/`tool_input` objects.

One thing to know: the cloud agent only loads hooks from the repository's **default branch**. If your hook config is only on a feature branch, the cloud agent won't see it.

### Claude Code

Claude Code uses a different hook system:

- Settings in `~/.claude/settings.json` and `.claude/settings.json`
- Different event names and matcher syntax (regex, `if` conditions)
- Exit 2 = block, exit 1 = non-blocking error
- 5 hook types (command, http, mcp_tool, prompt, agent)
- 29+ events including `FileChanged`, `CwdChanged`, `ConfigChange`

The shared best practice is the same: keep hooks small, deterministic, explicit about I/O, and strict about side effects.

## Conventions

| Rule | Rationale |
| --- | --- |
| Keep one hook focused on one responsibility | Small hooks are easier to trust, debug, disable, and reuse |
| Default to observe-first behavior unless blocking or mutation is explicitly required | Hooks run in the critical path and should not surprise users or agents |
| Keep hooks synchronous, bounded by `timeoutSec`, and non-interactive | Lifecycle hooks must return quickly and cannot wait for prompts |
| Make scripts deterministic and idempotent | Re-runs should not create drift or duplicate side effects |
| Treat prompts, tool arguments, tool output, transcripts, and payload fields as untrusted and sensitive | Hook input may be hostile, private, or malformed |
| Redact secrets, credentials, tokens, and private content from stdout, stderr, and logs | Logs and deny reasons often outlive the session |
| Parse both camelCase and snake_case payload aliases when portability matters | CLI, VS Code, cloud agent, and future hosts may differ in payload shape |
| Use structured stdout for `preToolUse` decisions and exit `2` only when the event blocks by exit code or the hook must fail closed | Structured output gives the agent a clear reason and avoids ambiguous failures |
| Keep in-script tool filtering even when `matcher` is present | Matcher behavior can vary by host and version; script filtering is the reliable boundary |
| Avoid branch, index, and worktree mutation by default | Git-destructive behavior risks data loss and hidden state changes |
| Package reusable hooks with config, scripts, purpose, dependencies, side effects, and disable path | Consumers need to understand what runs, what it reads, what it writes, and what it blocks |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Place repository hook configs in `.github/hooks/*.json` with scripts under `.github/hooks/scripts/` | Assume hooks in a feature branch are visible to the cloud agent before they reach the default branch |
| Seed `$COPILOT_HOME/config.json` with trusted folders for non-interactive CLI or CI runs that need repository hooks | Expect untrusted workspaces to load repository hooks silently |
| Use `disableAllHooks` deliberately as a global or file-scoped kill switch | Hide a disable switch inside undocumented behavior |
| Resolve relative `bash`, `powershell`, `command`, and `cwd` paths from the workspace root | Resolve script paths as if they were relative to the JSON file |
| Provide both `bash` and `powershell` for published cross-platform hooks | Claim cross-platform support with only one platform entry |
| Read stdin once, validate the fields used, and keep stdout machine-readable when the event parses it | Mix diagnostics and JSON on stdout |
| Use Bash `set -euo pipefail` and PowerShell `Set-StrictMode -Version Latest` | Let unset variables, failed commands, or loose parsing pass silently |
| Use `jq`, Python, Node.js, PowerShell 7, or an existing project CLI when they are already reasonable dependencies | Introduce a compiled runtime for an ordinary hook |
| Use HTTP hooks only with explicit timeouts, allowed environment variables, and documented outbound data | Send private code, prompts, or tool output to third parties by default |
| Test scripts by piping representative JSON payloads into them manually | Validate hooks only by waiting for a live agent event |

## Checklist Before Opening a PR

- [ ] Hook configs live under `.github/hooks/*.json` or the reusable `hooks/**` package and use `version`, `hooks`, event names, `type`, command entries, `cwd`, `timeoutSec`, and `env` intentionally.
- [ ] Repository trust, `$COPILOT_HOME/config.json`, `trustedFolders`, and `disableAllHooks` behavior are documented for the target surface.
- [ ] Relative paths are valid from the workspace root; user-level hooks use absolute paths when they must work across repositories.
- [ ] Scripts read stdin once, parse payload aliases defensively, validate required fields, and quote shell variables.
- [ ] Blocking hooks use structured `permissionDecision` and `permissionDecisionReason` for `preToolUse`, or exit `2` only where that event requires it.
- [ ] stdout is clean machine-readable output when parsed; stderr carries human diagnostics.
- [ ] Hook runtime is bounded, deterministic, non-interactive, idempotent, and free of background daemons or watchers.
- [ ] Logs and deny reasons redact prompts, secrets, credentials, tokens, large outputs, and private content.
- [ ] Cross-platform claims are backed by Bash and PowerShell entries or a shared runtime exposed through both.
- [ ] Representative `sessionStart`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `errorOccurred`, and `agentStop` payloads have been tested manually where those events are used.
- [ ] The hook package documents trigger event, purpose, side effects, dependencies, disable path, inputs, outputs, writes, and blocks.

## References

- Hooks configuration reference: https://docs.github.com/en/copilot/reference/hooks-configuration
- About hooks: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-hooks
