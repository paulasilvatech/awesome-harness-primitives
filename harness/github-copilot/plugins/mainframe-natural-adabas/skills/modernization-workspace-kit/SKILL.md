---
name: modernization-workspace-kit
description: >-
  Preview, publish, update, inspect, or uninstall managed modernization repository customizations with conflict detection, ownership hashes, transactional rollback, and safe archives. Use when installing a mainframe modernization track's context, stage agents, prompts, instructions, or automation into a target repository.
user-invocable: true
argument-hint: "--target <repository> --profile core|workshop|automation|full [--apply|--uninstall]"
---

# Modernization workspace kit

Publish repository-scoped assets that plugin installation does not activate automatically, with preview as the default and managed ownership for every written destination.

## When to invoke

- "Preview the workspace customizations for this modernization track."
- "Install the stage agents and prompts in this repository."
- "Add the traceability automation."
- "Uninstall only files managed by the workspace kit."

## Inputs

Use `$ARGUMENTS` as script options. Require an explicit target and profile. `--apply` authorizes the planned transaction; `--uninstall` selects an archive-based uninstall plan. Do not infer `--apply`.

## Policy and mechanism

This skill is the mechanism. The asset policy lives in `workspace-kit.json` at the root of the plugin that
carries this generated copy, so each modernization track publishes its own assets through the same tested
publisher.

| Manifest key | Meaning |
| --- | --- |
| `kitName` | Label used in reports and transaction temp directories. |
| `stateFile` | Target-relative managed-state path; the backup path derives from it. |
| `globalInstructions` | Package-relative source for the repository-wide instructions file. |
| `agents`, `prompts` | File names published from the package `agents/` and `prompts/` directories. |
| `skills` | Skill directory names published as trees. |
| `coreInstructions`, `workshopInstructions` | Instruction file names per profile. |
| `automation` | `source` and `destination` pairs for workflows and scripts. |

A missing or malformed manifest is a hard error; the publisher never falls back to defaults.

## Profiles

| Profile | Published assets |
| --- | --- |
| `core` | Global instructions, stage agents, project skills, and core instructions. |
| `workshop` | `core` plus workshop instructions and stage prompts. |
| `automation` | The manifest's automation entries only. |
| `full` | Union of `workshop` and `automation`. |

## Procedure

1. Preview the selected profile:

   ```bash
   python3 scripts/install_workspace_kit.py --target <repository> --profile workshop
   ```

2. Review every create, update, unchanged, unmanaged-identical, retired, preserved, and conflict result.
3. Apply only after approval by repeating the command with `--apply`.
4. Preview the same profile again and require every managed destination to be unchanged.
5. Preview uninstall with `--uninstall`; add `--apply` only after reviewing archive and preserve actions.

## Safety

- Preview mode writes no files.
- Any unmanaged or modified managed destination blocks the complete install or update transaction.
- New content and managed state are staged before commit; a commit failure restores prior files and state.
- Existing identical unmanaged files are not silently adopted.
- Paths that escape the target or traverse symlinks are rejected.
- Managed state is written atomically to the manifest's `stateFile`.
- Uninstall archives unchanged managed files and preserves modified files.
- The publisher does not install dependencies, access networks, stage Git changes, commit, push, deploy,
  change repository settings, or mutate infrastructure.
- Switch profiles only after previewing and uninstalling the profile recorded in managed state.

## Progressive disclosure and bundled resources

- `scripts/install_workspace_kit.py`: transactional preview, apply, update, and uninstall publisher.
- `scripts/test_install_workspace_kit.py`: profile, conflict, idempotence, rollback, archive, manifest, and path-safety tests.

## Limits

- This skill does not install or update the plugin itself.
- Project copies are publication artifacts, not a second canonical source.
- VS Code prompts remain VS Code-only after publication.
- Automation entries are published as declared; the publisher does not validate what they do.

## Output template

```markdown
## Workspace kit result

**Mode:** install-plan | install-applied | uninstall-plan | uninstall-applied | blocked
**Kit:** <kitName>
**Profile:** core | workshop | automation | full
**Target:** <repository>

### Summary
| Status | Count |
| --- | ---: |

### Changed or blocked destinations
- <status>: <target-relative path>

### Validation
- Idempotence: <pass, fail, or not run>
- Target checks: <command/result or not run>
```

## Quality gate

- [ ] Target and profile are explicit and preview was reviewed before apply or uninstall.
- [ ] The plugin's `workspace-kit.json` was read and no default was assumed.
- [ ] No conflict or modified managed file was overwritten or archived.
- [ ] Transaction failure coverage restores files and managed state.
- [ ] Retired and uninstalled destinations are archived or explicitly preserved when modified.
- [ ] State stays inside the target and is written atomically.
- [ ] Repeated apply is unchanged for every managed destination.
- [ ] VS Code-only prompts and runtime limitations are reported accurately.
