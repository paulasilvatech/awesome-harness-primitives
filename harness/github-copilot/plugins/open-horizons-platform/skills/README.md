# Open Horizons Agent Skills

Skills in this directory provide reusable procedures for GitHub Copilot CLI, VS Code,
and compatible Agent Skills hosts. Discovery loads only `name` and `description`; the
full body and bundled resources load after activation.

This document defines naming and ownership. It intentionally omits a hand-maintained
inventory count or exhaustive skill table. Inspect the directories and the generated
repository catalog for the current package contents.

## Naming taxonomy

| Prefix | Capability boundary |
| --- | --- |
| `open-horizons-aeg-*` | AEG lifecycle and Backstage integration. |
| `open-horizons-*` | Product-specific engineering, operations, and publication. |
| `backstage-*` | Reusable Backstage development and operations. |
| `azure-*` | Azure architecture, infrastructure, and service operations. |
| `foundry-*` | Microsoft Foundry and application-agent work. |
| `github-*` | GitHub APIs, automation, and Copilot customization. |
| `python-*` | Reusable Python engineering workflows. |

Use lowercase kebab-case. A skill directory and its frontmatter `name` must match.
Prefer a domain-qualified name when it makes activation intent clear inside a large
repository. Avoid aliases that differ only by wording.

## AEG capability

`open-horizons-backstage-aeg-feature` is the reusable AEG capability. It owns lifecycle
artifacts, role workflows, authenticated actor handling, mutation classification, and the
adapter contract. The four `open-horizons-aeg-*` agents remain lean and load this skill
before acting.

`open-horizons-workspace-kit` publishes either the focused AEG profile or broader
repository assets. It is dry-run-first, conflict-blocking, hash-managed, and archives
unchanged managed files during uninstall.

## Package contract

Every skill follows these rules:

1. `SKILL.md` starts with valid frontmatter and one H1.
2. `name` matches the parent directory and `description` states what and when.
3. Ordered work uses a procedure; evaluative work uses criteria.
4. Detailed knowledge goes in `references/`, repeatable automation in `scripts/`, and
   static material in `assets/` or `templates/`.
5. Scripts use explicit inputs, bounded side effects, safe paths, and focused tests.
6. Cross-primitive references use installed names and types rather than relative links.
7. VS Code prompt files are never treated as CLI capabilities.
8. Live state, metrics, identity, cost, and validation results require evidence.

## Source ownership

Most directories are owned by this package. Shared generated copies are declared in
`harness/github-copilot/manifests/plugin-sources.json` and synchronized from their
canonical library sources. Do not edit a generated copy independently.

## Validation

From the repository root:

```bash
python3 harness/github-copilot/skills/skill-creator/scripts/validate_skill.py \
  harness/github-copilot/plugins/PACKAGE_NAME/skills/<skill-name>
python3 harness/github-copilot/scripts/validate_primitives.py --strict
python3 harness/github-copilot/scripts/audit_primitive_content.py --check
python3 harness/github-copilot/scripts/audit_primitive_capabilities.py --check
python3 harness/github-copilot/scripts/audit_primitive_redundancy.py --check
python3 harness/github-copilot/scripts/sync_plugin_components.py --check
```

Run every changed bundled script or focused test. Report environment-dependent runtime
checks separately from static validation.

## References

- [Agent Skills specification](https://agentskills.io/)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
