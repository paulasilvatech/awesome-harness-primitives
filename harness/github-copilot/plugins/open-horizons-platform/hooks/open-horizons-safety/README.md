# Open Horizons safety hook

This hook protects GitHub Copilot CLI and GitHub Copilot cloud agent sessions from high-impact
Open Horizons operations. It does not claim VS Code hook support.

## Behavior

| Event | Behavior |
| --- | --- |
| `preToolUse` | Requests approval for high-impact infrastructure and protected portal changes, and denies literal secrets in Backstage configuration. |
| `preMcpToolCall` | Requests approval for mutating AEG operations and high-impact commands exposed through MCP. |

Safe operations emit no output. Decisions contain a category and remediation only; tool arguments,
paths containing credentials, tokens, and secret values are never echoed.

## Runtime contract

- Python 3, using only the standard library.
- Five-second timeout per event.
- No files written, logs retained, packages installed, or network requests made.
- `OPEN_HORIZONS_HOOK_MODE=ask` is the default.
- `OPEN_HORIZONS_HOOK_MODE=audit` evaluates without emitting a decision.
- `OPEN_HORIZONS_HOOK_MODE=off` disables evaluation.

## Validation

Run from the plugin root:

```bash
python3 hooks/open-horizons-safety/test_guard.py
```

Plugin hook commands resolve from the installed plugin root. A workspace-kit copy must adjust its
command paths for the destination repository and is inactive until that workspace is trusted.