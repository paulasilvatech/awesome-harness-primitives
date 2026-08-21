# Backstage safety hook

This `preToolUse` hook requests approval before Backstage app creation, dependency version
changes, package or TechDocs publication, deployments, and release operations. In a positively
detected `backstage/backstage` checkout it also protects root build, release, changeset-version,
and invalid root typecheck commands.

## Modes

Set `BACKSTAGE_EXPERT_HOOK_MODE` to:

- `ask` (default): emit a structured approval request for matched operations and malformed input.
- `audit`: inspect input but emit no decision.
- `off`: consume input and return without inspection.

The hook is synchronous, uses only the Python standard library, performs no network requests,
writes no files, and does not log tool arguments or credentials.

## Direct validation

```bash
python3 hooks/backstage-safety/test_guard.py
```

Repository hook paths resolve from the workspace root. The workspace kit therefore copies this
package to `hooks/backstage-safety/` when its optional repository-hook profile is selected.
