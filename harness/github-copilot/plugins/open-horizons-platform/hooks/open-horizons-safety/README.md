# Open Horizons safety hook

This hook requests explicit user confirmation before high-impact Open Horizons operations. It covers GitHub Copilot CLI and GitHub Copilot cloud agent hook surfaces; it does not claim VS Code hook support.

## Trigger and behavior

| Event | Behavior |
| --- | --- |
| `preToolUse` | Inspects command-execution tool input and requests confirmation for destructive infrastructure, cluster, repository, filesystem, or database commands. |
| `preMcpToolCall` | Applies the same policy to MCP tool names and arguments. |

The hook reads one JSON payload from stdin and emits `permissionDecision: ask` only when a risk pattern matches or the payload cannot be parsed safely. Safe operations produce no stdout. It never writes logs, sends network requests, or includes tool arguments in the decision reason.

## Dependencies and timeout

- Python 3 available as `python3` on Linux and macOS or `python` on Windows.
- Five-second timeout per event.
- No third-party Python packages.

## Disable or audit

Set `OPEN_HORIZONS_HOOK_MODE=off` to disable the policy or `OPEN_HORIZONS_HOOK_MODE=audit` to evaluate without requesting confirmation. The default is `ask`.

Uninstalling or disabling the plugin also removes the runtime hook.

## Direct payload tests

Run from the plugin root:

```bash
printf '%s' '{"hook_event_name":"preToolUse","toolName":"bash","toolInput":{"command":"terraform plan"}}' \
  | python3 hooks/open-horizons-safety/guard.py

printf '%s' '{"hook_event_name":"preToolUse","toolName":"bash","toolInput":{"command":"terraform apply"}}' \
  | python3 hooks/open-horizons-safety/guard.py
```

The first command emits nothing. The second emits a JSON `ask` decision without echoing the command.
