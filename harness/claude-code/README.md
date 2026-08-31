# Claude Code harness

This harness is generated from canonical content under [`harness/github-copilot/`](../github-copilot/README.md).

## Do not hand-edit generated primitives

The following directories and files are generated:

- `agents/`
- `rules/`
- `skills/`
- `commands/`
- `hooks/`
- `plugins/`
- `settings.json`
- `.claude-plugin/marketplace.json` at the repository root

Maintained Claude-specific source is limited to `scripts/`, `manifests/`, and the Claude Code specification and validation documents.

## Navigate

| Resource | Link |
| --- | --- |
| Claude Code catalog | [docs/catalog/claude-code.md](../../docs/catalog/claude-code.md) |
| Conversion and runtime contract | [docs/CLAUDE-CODE-HARNESS-SPEC.md](../../docs/CLAUDE-CODE-HARNESS-SPEC.md) |
| Dated evidence | [docs/CLAUDE-CODE-VALIDATION.md](../../docs/CLAUDE-CODE-VALIDATION.md) |
| Canonical source harness | [harness/github-copilot/](../github-copilot/README.md) |

## Regenerate and validate

```sh
python3 harness/claude-code/scripts/convert_from_copilot.py
python3 harness/claude-code/scripts/validate_primitives.py --strict
python3 harness/claude-code/scripts/generate_catalog.py
python3 harness/github-copilot/scripts/sync_installed_primitives.py \
  --manifest harness/claude-code/manifests/installed-primitives.json
```

Use the same commands with `--check` before publishing.
