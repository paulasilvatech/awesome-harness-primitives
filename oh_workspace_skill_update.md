---
name: open-horizons-workspace-kit
description: >-
  Plans, applies, inspects, or uninstalls Open Horizons repository customizations with conflict detection and managed-file state. Use when publishing the AEG feature, the full toolkit, instructions, VS Code prompts, safety hooks, MCP configuration, workflows, or issue templates to a target repository.
user-invocable: true
---

# Open Horizons workspace kit

Publish repository-scoped assets that plugin installation does not activate automatically, or create
explicit project copies for teams that require checked-in primitives. Planning is the default and
uninstall archives unchanged managed files while preserving files changed after installation.

## When to invoke

- "Install the Open Horizons AEG feature in this repository."
- "Preview the Open Horizons instructions and VS Code prompts."
- "Publish the Open Horizons workflow and issue-template automation."
- "Uninstall only files managed by the Open Horizons workspace kit."

## Profiles

| Profile | Published assets |
| --- | --- |
| `aeg` | Four AEG agents, the AEG feature skill, one instruction, five VS Code prompts, and the safety hook. |
| `core` | `AGENTS.md`, repository instructions, all agents, skills, instructions, prompts, safety hook, and workspace MCP configuration. |
| `automation` | Self-contained GitHub Actions workflows and issue templates. |
| `full` | The union of `core` and `automation`. |

The AEG profile does not fabricate an AEG endpoint. Its agents return `blocked` until an authenticated
`open-horizons-aeg` MCP server exposes the contract documented by the AEG feature skill.
The target-specific agent validation workflow is not published because it requires an
application-owned routing contract and service source tree that are not bundled here.

## Procedure

1. Resolve this installed skill directory and select an existing target repository.
2. Preview one explicit profile:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile aeg
   ```

3. Review every create, update, unchanged, unmanaged-identical, and conflict result.
4. Apply only after approval:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile aeg \
     --apply
   ```

5. Repeat the dry run and require every managed destination to be `unchanged`.
6. Preview uninstall with the same profile, then add `--apply` only after review:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile aeg \
     --uninstall
   ```

## Safety

- No file changes occur without `--apply`.
- Any conflict blocks the complete apply before the first write.
- Existing identical files are not silently adopted as managed files.
- Paths that escape the target or traverse symlinks are rejected.
- State is written atomically to `.github/.open-horizons-workspace-kit.json`.
- Uninstall archives only managed files whose hash still matches the installed hash.
- The installer does not install dependencies, call networks, stage, commit, push, deploy, or prune
  unrelated files.

## Progressive disclosure and bundled resources

- `scripts/install_workspace_kit.py`: repeatable plan, apply, and archive implementation.
- `scripts/test_install_workspace_kit.py`: focused transaction and safety tests.
- `templates/mcp.json`: workspace MCP syntax corresponding to the plugin's portable MCP manifest.

## Limits

- Do not use this skill to install or update the plugin itself.
- Do not switch profiles over managed state; preview and uninstall the current profile first.
- Do not claim VS Code prompts run in GitHub Copilot CLI or Agent Host.
- Do not treat project copies as a second canonical source; update the plugin package and republish.

## Output template

```markdown
## Open Horizons workspace kit

**Mode:** install-plan | installed | uninstall-plan | uninstalled | blocked
**Profile:** aeg | core | automation | full
**Target:** <repository>

### Summary
| Status | Count |
| --- | ---: |

### Changed or blocked destinations
- <status>: <target-relative path>

### Validation
- Idempotence: <pass, fail, or not run>
- Target checks: <command and result, or not run>
```

## Quality gate

- [ ] Target and profile are explicit.
- [ ] A dry run was reviewed before apply or uninstall.
- [ ] No conflict or modified managed file was overwritten or archived.
- [ ] Managed state was written atomically and remains inside the target.
- [ ] Apply is idempotent for every managed destination.
- [ ] AEG runtime availability is reported separately from static publication.
- [ ] VS Code-only prompts are identified as such.
- [ ] Target validation and Git status are reported without invented results.

## References

- [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-repository-instructions/add-repository-instructions)
- [VS Code prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)