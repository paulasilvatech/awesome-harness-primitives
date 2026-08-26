---
name: sifap-workspace-kit
description: >-
  Preview, publish, update, inspect, or uninstall managed SIFAP repository customizations with conflict detection, ownership hashes, transactional rollback, and safe archives. Use when installing the SIFAP core context, workshop agents and prompts, or traceability automation into a target repository.
user-invocable: true
argument-hint: "--target <repository> --profile core|workshop|automation|full [--apply|--uninstall]"
---

# SIFAP workspace kit

Publish repository-scoped assets that plugin installation does not activate automatically, with preview
as the default and managed ownership for every written destination.

## When to invoke

- "Preview the SIFAP workspace customizations."
- "Install the SIFAP workshop agents and prompts in this repository."
- "Add the SIFAP traceability workflow."
- "Uninstall only files managed by the SIFAP workspace kit."

## Inputs

Use `$ARGUMENTS` as script options. Require an explicit target and profile. `--apply` authorizes the
planned transaction; `--uninstall` selects an archive-based uninstall plan. Do not infer `--apply`.

## Profiles

| Profile | Published assets |
| --- | --- |
| `core` | Global SIFAP instructions, four stage agents, four SIFAP Skills, and core evidence/security instructions. |
| `workshop` | `core` plus backend, frontend, database, infrastructure, test, CI/CD instructions, and four stage prompts. |
| `automation` | Traceability validator and pinned GitHub Actions workflow. |
| `full` | Union of `workshop` and `automation`. |

## Procedure

1. Preview the selected profile:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile workshop
   ```

2. Review every create, update, unchanged, unmanaged-identical, retired, preserved, and conflict result.
3. Apply only after approval:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile workshop \
     --apply
   ```

4. Preview the same profile again and require every managed destination to be unchanged.
5. Preview uninstall with `--uninstall`; add `--apply` only after reviewing archive and preserve actions.

## Safety

- Preview mode writes no files.
- Any unmanaged or modified managed destination blocks the complete install/update transaction.
- New content and managed state are staged before commit; a commit failure restores prior files and state.
- Existing identical unmanaged files are not silently adopted.
- Paths that escape the target or traverse symlinks are rejected.
- Managed state is written atomically to `.github/.sifap-workspace-kit.json`.
- Uninstall archives unchanged managed files and preserves modified files.
- The publisher does not install dependencies, access networks, stage Git changes, commit, push, deploy,
  change repository settings, or mutate infrastructure.
- Switch profiles only after previewing and uninstalling the profile recorded in managed state.

## Progressive disclosure and bundled resources

- `scripts/install_workspace_kit.py`: transactional preview, apply, update, and uninstall publisher.
- `scripts/test_install_workspace_kit.py`: profile, conflict, idempotence, rollback, archive, and path-safety tests.
- `templates/copilot-instructions.md`: concise repository-wide SIFAP context.
- `templates/sifap-traceability.yml`: pinned workflow for the published validator.

## Limits

- This skill does not install or update the plugin itself.
- Project copies are publication artifacts, not a second canonical source.
- VS Code prompts remain VS Code-only after publication.
- The automation profile validates requirement lineage, not business correctness or implementation coverage.

## Output template

```markdown
## SIFAP workspace kit

**Mode:** install-plan | install-applied | uninstall-plan | uninstall-applied | blocked
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
- [ ] No conflict or modified managed file was overwritten or archived.
- [ ] Transaction failure coverage restores files and managed state.
- [ ] Retired and uninstalled destinations are archived or explicitly preserved when modified.
- [ ] State stays inside the target and is written atomically.
- [ ] Repeated apply is unchanged for every managed destination.
- [ ] VS Code-only prompts and runtime limitations are reported accurately.
- [ ] Target validation and Git status are reported without invented results.
