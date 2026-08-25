---
name: backstage-workspace-kit
description: "Plan, apply, inspect, or uninstall the Backstage Expert repository workspace kit for adopter or core profiles. Use when publishing bundled instructions and VS Code prompts into a target repository."
user-invocable: true
---

# Backstage Expert workspace kit

Publish repository-scoped assets that Agent Plugins 1.0 does not activate automatically. The
bundled script is dry-run-first, records managed-file hashes, and removes only unchanged files it
previously installed.

## When to invoke

- "Install Backstage Expert instructions in this repository."
- "Preview the Backstage VS Code prompts."
- "Apply the Backstage core contributor workspace profile."
- "Uninstall the Backstage workspace kit."

## Profiles

| Profile | Published assets |
| --- | --- |
| `adopter` | App, catalog, software-template, integration, and TechDocs instructions plus the four retained prompts. |
| `core` | AI, auth, integration, and TechDocs instructions plus the four retained prompts, tuned for core contribution workflows. |

## Procedure

1. Resolve the installed skill directory and target repository.
2. Preview:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile adopter
   ```

3. Review every create, unchanged, conflict, and managed-file result.
4. Apply only after approval:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile adopter \
     --apply
   ```

5. Re-run the dry-run to verify idempotence.
6. Uninstall only after previewing the removal plan:

   ```bash
   python3 scripts/install_workspace_kit.py \
     --target <repository> \
     --profile adopter \
     --uninstall
   ```

   Add `--apply` to perform the approved uninstall.

## Safety

- The default is a plan; no writes or removals occur without `--apply`.
- The script never overwrites `AGENTS.md` or `.github/copilot-instructions.md`.
- Existing differing files are conflicts and are not overwritten.
- Destinations and state paths must remain beneath the target and cannot traverse symlinks.
- State is stored in `.github/.backstage-expert-workspace-kit.json`.
- Uninstall removes only managed files whose current hash still matches the installed hash.

## Output template

```markdown
## Backstage workspace kit

**Mode:** plan | applied | uninstall-plan | uninstalled | blocked
**Profile:** adopter | core
**Target:** <path>

| Status | Destination |
| --- | --- |

### Validation
- Idempotence:
- Conflicts:
- State file:
```

## Progressive disclosure and bundled resources

- `scripts/install_workspace_kit.py`: deterministic workspace-kit installer.
- `scripts/test_install_workspace_kit.py`: focused installer behavior tests.

## Quality gate

- [ ] Target and profile are explicit.
- [ ] A dry-run was reviewed before apply or uninstall.
- [ ] No conflict or modified managed file was overwritten or removed.
- [ ] Managed-file state was written atomically.
- [ ] Apply is idempotent.
- [ ] VS Code prompts are reported as VS Code-only assets.
