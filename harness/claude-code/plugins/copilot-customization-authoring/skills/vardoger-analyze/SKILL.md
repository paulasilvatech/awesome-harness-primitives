---
name: vardoger-analyze
description: >-
  Run the local vardoger CLI to analyze GitHub Copilot CLI conversation history and write
  personalized instructions into ~/.copilot/copilot-instructions.md. Use this skill when the user
  asks to personalize my copilot, analyze my copilot history, tailor Copilot to me, run vardoger,
  update my Copilot instructions from history, or make Copilot learn my style.
license: Apache-2.0
---

<!-- Generated from harness/github-copilot/plugins/copilot-customization-authoring/skills/vardoger-analyze/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Vardoger Copilot history analysis

Drive the local `vardoger` CLI to summarize GitHub Copilot CLI conversation history in batches, synthesize durable behavioral instructions, and write an idempotent fenced block into the user's Copilot instructions file.

## When to invoke

- "Personalize my Copilot from my CLI history."
- "Analyze my Copilot history with vardoger."
- "Tailor GitHub Copilot to my style."
- "Run vardoger and update my Copilot instructions."
- "Make Copilot learn my style from previous sessions."

## Prerequisites and context

- `vardoger` must be installed locally. Recommended install: `pipx install vardoger`; non-install execution can use `uvx vardoger --help`.
- The workflow runs entirely on the user's machine with no network calls and no uploads.
- `vardoger` reads GitHub Copilot CLI history from `~/.copilot/session-state/`.
- It writes checkpoint state to `~/.vardoger/state.json`, creating it on first run.
- It writes global personalization to `~/.copilot/copilot-instructions.md` between `<!-- vardoger:start -->` and `<!-- vardoger:end -->`, preserving hand-authored rules outside that block.
- For project scope, write with `--scope project --project <path>` instead of `--scope global`.

## Sandbox and permission rule

`vardoger` reads and writes outside the current workspace. When the host asks to approve a `vardoger` command, grant write access beyond the workspace. Without that approval, the first `vardoger prepare` call can fail with `PermissionError: ... ~/.vardoger/state.tmp` because the sandbox blocks writes outside the project.

## Procedure

1. Verify `vardoger` is on `PATH`:

```bash
if ! command -v vardoger >/dev/null 2>&1; then
  cat <<'INSTALL_EOF'
vardoger CLI is not installed.

This skill calls the vardoger CLI to read your Copilot CLI history and
write a personalization file, so the CLI must be on PATH.

Install options:

  # Recommended:
  pipx install vardoger

  # Or run without installing:
  uvx vardoger --help

If you do not have pipx, see https://pipx.pypa.io/stable/.

Project page: https://github.com/dstrupl/vardoger

After installing, re-run the personalization request.
INSTALL_EOF
  exit 1
fi
```

2. Check staleness:

```bash
vardoger status --platform copilot --json
```

If the output shows `"is_stale": false`, report that personalization is fresh and stop unless the user explicitly asked to force a rerun.

3. Get batch metadata:

```bash
vardoger prepare --platform copilot
```

This returns JSON such as `{"batches": 3, "total_conversations": 29}`. Record the batch count and total conversations.

4. For each batch number from 1 to N, run:

```bash
vardoger prepare --platform copilot --batch 1
```

Read the summarization prompt and conversation data, then write a concise bullet summary of behavioral signals. Repeat with `--batch 2`, `--batch 3`, and so on.

5. Get the synthesis prompt:

```bash
vardoger prepare --platform copilot --synthesize
```

6. Combine all batch summaries into one clean markdown personalization that follows the synthesis prompt.

7. Write the result:

```bash
echo "YOUR_PERSONALIZATION_HERE" | vardoger write --platform copilot --scope global
```

Replace `YOUR_PERSONALIZATION_HERE` with the actual markdown. Use `--scope project --project <path>` only when the user requested project-scoped personalization.

8. Report what was written, where it was written, and that reruns are idempotent because the fenced vardoger block is replaced.

## Personalization content rules

| Signal type | Include | Exclude |
| --- | --- | --- |
| Workflow preferences | Repeated command, validation, planning, and review habits | One-off task choices. |
| Communication style | Durable preferences for brevity, evidence, structure, or autonomy | Sensitive personal data or private content. |
| Code conventions | Cross-session patterns the user repeatedly applies | Repository secrets or credentials. |
| Tool usage | Reliable shortcuts and effective local workflows | Network upload claims; vardoger is local. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `vardoger CLI is not installed` | `vardoger` is missing from `PATH` | Install with `pipx install vardoger` or use `uvx vardoger --help`. |
| `PermissionError: ... ~/.vardoger/state.tmp` | Sandbox denied writes outside workspace | Approve the command with write access beyond the workspace. |
| `"is_stale": false` | Existing personalization is fresh | Stop and report freshness unless the user requested a forced rerun. |
| No batches returned | No readable Copilot CLI history | Report that `~/.copilot/session-state/` has no analyzable conversations. |


## Command forms

Use the exact batch command form `vardoger prepare --platform copilot --batch <N>` in generalized instructions, then substitute the concrete number when executing. Use the exact synthesis command `vardoger prepare --platform copilot --synthesize`. Each batch summary should be a bullet-point summary so synthesis can compare behavioral signals consistently.

## Output template

```markdown
## Vardoger personalization result

**Status:** written | fresh | blocked
**Scope:** global | project
**History source:** `~/.copilot/session-state/`
**Destination:** `~/.copilot/copilot-instructions.md` or `<project path>`

### Batch summary
| Batch | Conversations | Behavioral signals |
| --- | --- | --- |
| `<n>` | `<count>` | `<concise summary>` |

### Written personalization
<summary of durable instructions written; do not paste sensitive conversation content>

### Validation
- `vardoger status --platform copilot --json`: <result>
- `vardoger prepare --platform copilot`: <result>
- `vardoger write --platform copilot --scope <scope>`: <result>
```

## Quality gate

- [ ] `vardoger` installation was verified before running prepare or write commands.
- [ ] Staleness was checked with `vardoger status --platform copilot --json`.
- [ ] Every batch from `vardoger prepare --platform copilot` was summarized before synthesis.
- [ ] The synthesis prompt was fetched with `--synthesize` before writing.
- [ ] The write used `vardoger write --platform copilot --scope global` or an explicitly requested project scope.
- [ ] The report states the destination file and idempotent fenced block behavior.
- [ ] No sensitive data, credentials, or raw private conversation content is pasted into the final report.
## References

- [pipx documentation](https://pipx.pypa.io/stable/)
- [vardoger project](https://github.com/dstrupl/vardoger)
