---
name: frontend-project-setup
description: >-
  Inspect, preview, install, update, and uninstall optional frontend instructions, VS Code
  prompts, and a named Playwright MCP workspace entry with ownership hashes and conflict
  protection. Use this skill when a consuming repository wants frontend-experience workspace
  companions.
---

<!-- Generated from harness/github-copilot/skills/frontend-project-setup/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Frontend project setup

Publish optional workspace companions without treating them as direct plugin components or overwriting repository-owned customizations.

## When to invoke

- "Preview the frontend-experience workspace companions."
- "Install scoped frontend instructions and VS Code prompts."
- "Update the frontend companions without overwriting local edits."
- "Add the pinned Playwright MCP entry to VS Code."
- "Uninstall only the frontend-experience files this setup owns."

## Prerequisites and context

- Select one existing workspace root. The root and its relevant parents must not be symlinks.
- Review existing `.github/copilot-instructions.md`, `.github/instructions/`, `.github/prompts/`, `.github/agents/`, `.github/skills/`, `.vscode/mcp.json`, package manifests, frontend roots, test roots, public routes, and project scripts.
- The script uses only the Python standard library, performs no network access, and never installs dependencies.
- Prompt files are VS Code-only; the portable plugin remains usable through skills and agents.

## Procedure

1. Run a no-write preview:

   ```sh
   python3 scripts/install_companions.py --workspace <workspace> --action plan
   ```

2. Review detected stack, rendered `applyTo` scopes, and every `create`, `update`, `unchanged`, `conflict`, or `skipped` action.
   Discoverability companions are selected automatically only when public web-route evidence is detected; use `--discoverability include` or `--discoverability exclude` for an explicit override.
3. Resolve conflicts or deliberately choose `--force`; never use force as an implicit default.
4. Apply only after explicit approval:

   ```sh
   python3 scripts/install_companions.py --workspace <workspace> --action apply --approve
   ```

5. Add the VS Code Playwright server only when requested:

   ```sh
   python3 scripts/install_companions.py --workspace <workspace> --action apply --approve --include-vscode-mcp
   ```

6. Repeat plan/apply to verify owned unchanged files are idempotent.
7. Uninstall owned, unmodified files and the owned MCP server entry:

   ```sh
   python3 scripts/install_companions.py --workspace <workspace> --action uninstall --approve
   ```

## Ownership and conflict rules

- Ownership metadata lives at `.github/frontend-experience-companions.json` and records template edition plus content hashes, never secrets.
- Unowned existing files are conflicts unless byte-identical to the rendered template.
- Modified owned files are conflicts during update and are preserved during uninstall.
- `--force` may replace only the listed companion file or the named `playwright` server entry after `--approve`; it never replaces an entire existing VS Code MCP file.
- Any conflict is detected before writes, so non-force conflict mode performs no partial installation.
- Writes are staged and rolled back after an interrupted operation.
- Path traversal, absolute template destinations, symlinked files/directories, and resolved destinations outside the workspace are rejected.

## Published companions

| Path | Responsibility |
| --- | --- |
| `.github/instructions/frontend-experience.instructions.md` | Passive implementation conventions scoped to detected frontend roots |
| `.github/instructions/frontend-testing.instructions.md` | Passive test and evidence conventions scoped to detected test roots |
| `.github/instructions/frontend-discoverability.instructions.md` | Passive public-route, metadata, manifest, icon, robots, and sitemap conventions |
| `.github/prompts/frontend-design.prompt.md` | VS Code design-contract action |
| `.github/prompts/frontend-build.prompt.md` | VS Code bounded implementation action |
| `.github/prompts/frontend-validate.prompt.md` | VS Code independent QA action |
| `.github/prompts/frontend-assets.prompt.md` | VS Code metadata and asset action |
| `.vscode/mcp.json` `servers.playwright` | Optional VS Code translation of the verified pinned MCP server |

## Limits

- Do not install dependencies, browser binaries, SDKs, or extensions.
- Do not claim the VS Code MCP server or prompts are active until tool discovery and Chat: Run Prompt are verified.
- Do not publish globally or outside the selected workspace.
- Do not remove modified, unowned, or unknown files during uninstall.

## Progressive disclosure and bundled resources

- [scripts/install_companions.py](scripts/install_companions.py): deterministic preview/apply/uninstall publisher.
- [templates/.github/instructions/](templates/.github/instructions/): rendered instruction templates.
- [templates/.github/prompts/](templates/.github/prompts/): VS Code prompt templates.
- [templates/.vscode/mcp.json](templates/.vscode/mcp.json): named VS Code MCP server entry source.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Frontend companion setup result
**Status:** planned | applied | conflict | uninstalled | blocked
**Workspace:** <absolute path>
**Template edition:** <edition>

### Detection
- Frontend roots:
- Frameworks:
- Existing customizations:

### Actions
| Path or entry | Action | Reason |
| --- | --- | --- |

### Validation
- No external writes:
- Repeated apply:
- Modified files preserved:
- VS Code runtime checks:
```

## Quality gate

- [ ] A dry-run occurred before any requested write.
- [ ] The selected workspace, frontend roots, stack, tests, public routes, and conflicts are visible.
- [ ] Writes require `--approve`, and `--force` is explicit.
- [ ] Conflict mode makes no partial writes.
- [ ] Ownership, hashes, edition, idempotency, path safety, and rollback behavior are preserved.
- [ ] Uninstall removes only unmodified owned content and the unchanged named MCP entry.
- [ ] VS Code prompt and MCP runtime checks are reported separately from static installation.
