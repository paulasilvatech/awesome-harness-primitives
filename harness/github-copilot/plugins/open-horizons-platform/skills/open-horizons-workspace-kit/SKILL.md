---
name: open-horizons-workspace-kit
description: "Plan or publish the Open Horizons repository workspace kit from the installed plugin. Use when the user asks to install, synchronize, preview, or update GitHub Copilot instructions, VS Code prompts, hooks, workflows, issue forms, governance files, or optional project agents and skills in a target repository."
user-invocable: true
---

# Open Horizons workspace kit

Publish repository-scoped assets that GitHub Copilot plugin installation does not activate automatically. The bundled installer plans every destination, detects conflicts before writing, and requires an explicit `--apply` flag for changes.

## When to invoke

- "Install the Open Horizons instructions and prompts in this repository."
- "Preview the Open Horizons `.github` workspace kit."
- "Add the plugin hooks and workflows to this project."
- "Synchronize the Open Horizons repository customizations."
- "Install the agents and skills directly in `.github` without relying on the plugin."

## Component groups

| Group | Published content | Default |
| --- | --- | ---: |
| `governance` | Root `AGENTS.md`, repository Copilot instructions, model-routing convention, and customization docs | Yes |
| `instructions` | Path-specific `.instructions.md` files | Yes |
| `prompts` | VS Code `.prompt.md` files | Yes |
| `automation` | Workflows, issue forms, pull request template, Dependabot, and the self-contained CodeQL workflow | Yes |
| `hooks` | Canonical safety hook package plus repository hook configuration | Yes |
| `mcp` | Workspace `.github/mcp.json` translated from the Agent Plugins 1.0 MCP configuration | Yes |
| `runtime` | Project `.github/agents/` and `.github/skills/` copies | Yes; required for the bundled VS Code prompts and useful when the plugin is unavailable |

The installer publishes a separately validated workspace MCP template because Agent Plugins 1.0 and workspace MCP configurations use different transport vocabulary. The script rejects a stale template before planning or writing files.

## Prerequisites and context

- Run `scripts/install_workspace_kit.py` from this skill package with Python 3.
- The target directory must exist and be a Git repository unless `--allow-non-git` is explicitly supplied for scaffolding or tests.
- Inspect the dry-run before using `--apply`.
- Existing differing files are conflicts. The installer performs no writes until all conflicts are resolved or `--force` is supplied.

## Procedure

1. Resolve this skill directory and the target repository.
2. Preview the default complementary kit:

   ```bash
   python3 scripts/install_workspace_kit.py --target <repository>
   ```

3. Select component groups when the complete default kit is too broad:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --components instructions,prompts,hooks
   ```

4. Review every `create`, `unchanged`, and `conflict` result.
5. Apply only after approval:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --components instructions,prompts,hooks \
     --apply
   ```

6. Use `--force` only after reviewing differing destination files. It replaces conflicts but never deletes unrelated files.
7. Run the target repository's existing validation commands and review `git status --short`.

## Safety behavior

- Dry-run is the default; no destination changes occur without `--apply`.
- A conflicting file aborts the complete apply before the first write unless `--force` is present.
- Destination paths are resolved beneath the target root; symlink escapes are rejected.
- Source symlinks are rejected.
- The installer copies files only. It does not delete, prune, stage, commit, push, install dependencies, or contact external services.
- Identical files remain unchanged.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| Target is not a Git repository | Select the correct repository or use `--allow-non-git` only for intentional scaffolding. |
| Apply reports conflicts | Review the listed files; merge manually or rerun with explicitly approved `--force`. |
| Hook script cannot be found | Include the `hooks` group so both the root hook package and `.github/hooks` configuration are copied. |
| Agents or skills should not be duplicated in `.github` | Select explicit component groups and omit `runtime`; confirm that no copied prompt depends on a missing named agent. |
| MCP tools are missing | Include the `mcp` group or install the plugin; verify Node.js, Docker, Azure authentication, and outbound HTTPS prerequisites. |

## Progressive disclosure and bundled resources

- `scripts/install_workspace_kit.py`: deterministic dry-run and copy installer for the component groups above.
- `templates/mcp.json`: workspace MCP configuration kept semantically synchronized with plugin-root `mcp.json`.

## Limits

- Do not use this skill to install or update the GitHub Copilot plugin itself.
- Do not infer permission to overwrite target files; `--force` requires explicit user approval.
- Do not claim prompts execute in GitHub Copilot CLI; copied prompts are VS Code-only.
- Do not copy Agent Plugins 1.0 `mcp.json` directly into `.github/`; use the validated workspace template.

## Output template

```markdown
## Open Horizons workspace kit

**Mode:** plan | applied | blocked
**Target:** <repository>
**Components:** <selected groups>

### Summary
- Create: <count>
- Overwrite: <count>
- Unchanged: <count>
- Conflicts: <count>

### Conflicts or changes
- <status>: <target-relative path>

### Validation
- Installer exit: <code>
- Target validation: <command and result, or not run>
```

## Quality gate

- [ ] The target path and selected component groups are explicit.
- [ ] A dry-run was reviewed before apply.
- [ ] No conflict was overwritten without explicit approval.
- [ ] Instructions, prompts, hooks, and automation landed in their documented discovery paths.
- [ ] Runtime agents and skills are present when copied prompts reference named agents, or the selected reduced component set documents that dependency.
- [ ] Workspace MCP configuration passed the plugin-to-workspace transport mapping check.
- [ ] Target validation and `git status --short` were reviewed.
