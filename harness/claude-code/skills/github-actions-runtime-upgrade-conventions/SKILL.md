---
name: github-actions-runtime-upgrade-conventions
description: >-
  Upgrade GitHub Actions workflow dependencies to supported runtimes while preserving behavior.
  Use this skill when logs report deprecated Node.js action runtimes, when editing
  `.github/workflows/*.yml` or `.github/workflows/*.yaml`, or when choosing pinned action versions
  and validating upgraded workflow runs.
---

<!-- Generated from harness/github-copilot/skills/github-actions-runtime-upgrade-conventions/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GitHub Actions runtime upgrade conventions

Modernize GitHub Actions action versions without changing workflow behavior: select compatible stable major releases, pin runtime/dependency actions immutably, validate post-upgrade workflow parsing and execution, and document each upgrade.

## When to invoke

- "Fix this GitHub Actions deprecated runtime warning."
- "Upgrade actions/setup-node to a supported runtime."
- "Review workflow action pins in `.github/workflows`."
- "Move this workflow off an old Node.js action runtime."
- "Prepare PR notes for action runtime upgrades."

## Upgrade rules

| Rule | Required behavior |
| --- | --- |
| Stable major | Prefer the latest stable major version compatible with the workflow. |
| Immutable pin | Resolve the target release to a full commit SHA and use that SHA in `uses:`. |
| Version comment | Add an optional version comment such as `# v4.3.1` beside the SHA. |
| No mutable final pins | Do not leave final `uses:` values pinned to `@v4`, `@main`, branches, or moving tags. |
| Small changes | Upgrade one action at a time per commit, or one tightly related group. |
| Behavior preservation | Keep triggers/permissions, inputs, outputs, release/signing/artifact behavior unchanged unless intentionally requested. |

## Actions to prioritize

| Group | Examples | Why |
| --- | --- | --- |
| First-party actions | `actions/*` | They commonly drive runtime deprecation warnings and have clear release lines; review first-party actions before third-party guesses. |
| Setup actions | `actions/setup-*`, `actions/setup-node`, `actions/setup-python`, `actions/setup-dotnet` | Runtime migrations often appear here first and affect downstream build steps. |
| Warning-named actions | Any action explicitly named in workflow logs | The log identifies the actual blocker. |

## Pinning pattern

Use a full SHA in `uses:` and keep the human-readable release only as a comment:

```yaml
steps:
  - uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608 # v4.3.1
  - uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8 # v4.0.4
```

When recommending an upgrade, first identify the latest compatible release, then resolve the release tag to its commit SHA, then update the workflow.

## Verification checklist

| Check | Evidence |
| --- | --- |
| Workflow parse | Edited `.github/workflows/*.yml` or `.github/workflows/*.yaml` remains valid YAML. |
| Behavior preservation | Triggers, `permissions`, `env`, `with`, `secrets`, matrix strategy, and job dependencies are unchanged unless documented. |
| Run validation | Affected workflows re-run successfully, or equivalent local build/test commands pass when workflow execution is unavailable. |
| Output validation | Release, signing, cache, and artifact steps still produce expected outputs where applicable. |
| Runtime warning scan | New logs contain no new deprecation warnings or runtime migration notes. |

## PR note content

Include these details in PR summaries or comments:

| Item | Format |
| --- | --- |
| Actions upgraded | `<owner/action>` from `<old ref>` -> `<new sha> # <version>`. |
| Compatibility caveat | Any action that could not move to a new major and why. |
| Validation | Workflow run links, rerun names, or local command results. |
| Behavior changes | State `none` unless a change was intentional. |

## Gotchas

- **Do not pin to mutable tags in final recommendations**: `@v4` and `@main` can move after review.
- **Do not "fix" runtime warnings by changing unrelated workflow logic**: isolate action upgrades from behavior changes.
- **Do not batch unrelated actions**: small upgrade sets make failures attributable.
- **Dependabot is not a substitute for validation**: automated bumps still need behavior-preserving checks.

## Output template

```markdown
## GitHub Actions runtime upgrade

**Status:** complete | needs validation | blocked
**Workflow:** `.github/workflows/<name>.yml`

| Action | Old ref | New ref | Reason | Validation |
| --- | --- | --- | --- | --- |
| `<owner/action>` | `<old>` | `<sha> # <version>` | <runtime warning or upgrade> | <run or command> |

### Behavior preservation
- Triggers changed: yes | no
- Permissions changed: yes | no
- Inputs/outputs changed: yes | no

### PR notes
- <summary line>
```

## Quality gate

- [ ] Every changed `uses:` reference is pinned to a full commit SHA, not a mutable tag or branch.
- [ ] The target release is the latest compatible stable major or the exception is documented.
- [ ] Workflow triggers, permissions, inputs, outputs, and artifacts are preserved unless intentionally changed.
- [ ] Edited workflow YAML parses.
- [ ] The affected workflow or equivalent validation ran successfully, or the blocker is reported.
- [ ] PR notes list old -> new action refs, validation, and any action that could not upgrade.
