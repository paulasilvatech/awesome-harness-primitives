---
name: git-flow-branch-creator
description: >-
  Analyze git status and diffs, classify work using the nvie Git Flow branching model, generate a
  semantic branch name, and create the branch from the correct source branch. Use this skill when
  the user asks to start a feature, bugfix, release, hotfix, or support branch, create a Git Flow
  branch, or choose a branch name from current changes.
allowed-tools: mcp__bash
---

<!-- Generated from harness/github-copilot/plugins/git-github-workflow/skills/git-flow-branch-creator/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Git Flow branch creator

Inspect current Git changes, classify the work under Git Flow, create a descriptive branch from the correct source branch, and report the evidence, command, and next steps.

## When to invoke

- "Create a Git Flow branch for these changes."
- "Start a feature branch from develop."
- "Create a hotfix branch for this production bug."
- "Name and create the right branch for my diff."
- "Prepare a release branch for version 2.1.0."

## Prerequisites and context

- Requires a Git repository with Git Flow-style base branches.
- Use `develop` as the source for `feature` and `release` branches.
- Use `master` as the source for `hotfix` branches unless the repository has an explicitly different production branch.
- Preserve uncommitted changes; `git checkout -b` carries them to the new branch when possible.

## Branch classification

| Branch type | Purpose | Branch from | Merge to | Naming | Indicators |
| --- | --- | --- | --- | --- | --- |
| `feature` | New features, enhancements, non-critical improvements | `develop` | `develop` | `feature/descriptive-name` or `feature/ticket-number-description` | New functionality, UI/UX improvements, new API endpoints or methods, non-breaking database schema additions, new configuration options, non-critical performance improvements. |
| `release` | Release preparation, version bumps, final testing | `develop` | `develop` and `master` | `release-X.Y.Z` | Version number changes, build configuration updates, documentation finalization, minor pre-release bug fixes, release notes updates, dependency version locks. |
| `hotfix` | Critical production bug fixes requiring immediate deployment | `master` | `develop` and `master` | `hotfix-X.Y.Z` or `hotfix/critical-issue-description` | Security vulnerability fixes, critical production bugs, data corruption fixes, service outage resolution, emergency configuration changes. |

Decision tree:

1. If the change fixes a critical production issue, security vulnerability, outage, data corruption, or emergency config problem, choose `hotfix`.
2. Else if the change prepares a release through version bump, release notes, final docs, build config, dependency locks, or release stabilization, choose `release`.
3. Else choose `feature` for additive, developmental, or non-critical corrective work.
4. If changes mix unrelated feature, hotfix, and release concerns, recommend splitting before creating a branch unless one concern clearly dominates.

## Branch naming

| Type | Format | Examples |
| --- | --- | --- |
| Feature | `feature/[ticket-number-]descriptive-name` | `feature/user-authentication`, `feature/PROJ-123-shopping-cart`, `feature/api-rate-limiting`, `feature/dashboard-redesign` |
| Release | `release-X.Y.Z` | `release-1.2.0`, `release-2.1.0`, `release-1.0.0` |
| Hotfix | `hotfix-X.Y.Z` or `hotfix/critical-description` | `hotfix-1.2.1`, `hotfix/security-patch`, `hotfix/payment-gateway-fix`, `hotfix-2.1.1` |

Name rules:

- Use lowercase kebab-case.
- Include a ticket number when visible in the user request, branch, commit text, or filenames.
- Keep the name concise but descriptive.
- Avoid vague names such as `feature/changes` or `hotfix/fix`.
- If a branch name already exists, append a small suffix such as `-2` or choose the next most specific name.

## Procedure

1. Run `git status` and identify current branch, staged files, unstaged files, and untracked files.
2. Run `git diff --cached` when staged changes exist; run `git diff` for unstaged changes. Use both when both staged and unstaged work matter.
3. Classify the change nature by files modified, scope, urgency, and whether the work is additive, corrective, or release-preparatory.
4. Select `feature`, `release`, or `hotfix` using the decision tree.
5. Verify the source branch exists locally or remotely: `develop` for feature/release, `master` for hotfix.
6. Generate a semantic branch name that follows the type's format.
7. Check for name conflicts with local and remote branches.
8. Create and switch to the branch with `git checkout -b [branch-name] [source-branch]`.
9. Verify with `git status --short --branch` and report next steps: commit changes, push branch, open PR, or split work.

## Examples

| Scenario | Analysis | Branch | Command |
| --- | --- | --- | --- |
| Added a new user registration API endpoint | New functionality, additive, not critical. | `feature/user-registration-api` | `git checkout -b feature/user-registration-api develop` |
| Fixed critical security vulnerability in authentication | Security fix, production-critical, immediate deployment. | `hotfix/auth-security-patch` | `git checkout -b hotfix/auth-security-patch master` |
| Updated version to 2.1.0 and finalized release notes | Release preparation, version bump, documentation. | `release-2.1.0` | `git checkout -b release-2.1.0 develop` |
| Improved database query performance and updated caching | Non-critical performance enhancement. | `feature/database-performance-optimization` | `git checkout -b feature/database-performance-optimization develop` |

## Gotchas

- **Do not create a hotfix from `develop`**: Git Flow hotfixes start from production (`master`) and merge back to both `master` and `develop`.
- **Do not hide mixed work in one branch**: if unrelated release, hotfix, and feature changes are present, split them before branch creation.
- **Do not assume no changes means no branch**: if the user explicitly requested a branch name for planned work, create it from their intent even when the diff is empty.
- **Use `--no-ff` at merge time**: branch creation does not merge, but Git Flow preserves branch history with `--no-ff` merges and release tags on `master`.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `develop` or `master` does not exist locally | Branch exists only on remote or repository uses a different production branch. | Check `git branch -a`; use `origin/develop`, `origin/master`, or the repository's documented base. |
| `git checkout -b` fails because branch exists | Local name conflict. | Choose a more specific name or append `-2`. |
| Checkout would overwrite files | Uncommitted changes conflict with source branch. | Stop and report the conflict; do not stash or discard without explicit user request. |
| No diff is present | Planned branch or clean working tree. | Classify from the user request; otherwise report that there is no change evidence. |


## Legacy field mapping

The original Git Flow prompt used XML-style field names. Preserve their meaning when reporting analysis or translating old output: `analysis-framework`, `branch-types`, `branch-type`, `branch-from`, `merge-to`, `feature-branches`, `release-branches`, `hotfix-branches`, `naming-conventions`, `analysis-process`, `change-scope`, `files-modified`, `urgency-level`, `decision-tree`, `if-yes`, `if-no`, `use-kebab-case`, `be-descriptive`, `include-context`, `keep-concise`, `edge-cases`, `mixed-changes`, `no-changes`, `existing-branch`, `conflicting-names`, `validation`, `pre-analysis`, `analysis-quality`, `execution-safety`, `execution-protocol`, `analysis-summary`, `git-status`, `git-diff`, `change-analysis`, `branch-decision`, `branch-creation`, `next-steps`, `fallback-options`, `alternative-names`, `manual-override`, `gitflow-reference`, `main-branches`, `supporting-branches`, `merge-strategy`, `develop/master`, `features/releases`, `feature/hotfix/release`, and `status/diff`.

## Output template

```markdown
## Git Flow branch result

**Status:** created | blocked | recommendation only
**Current branch before:** `<branch>`
**Branch type:** `feature | release | hotfix`
**New branch:** `<branch-name>`
**Source branch:** `develop | master | <other>`

### Evidence
- `git status`: <summary>
- `git diff` / `git diff --cached`: <summary of relevant changes>
- Classification: <why this branch type fits>

### Command
```bash
git checkout -b <branch-name> <source-branch>
```

### Next steps
- <commit, push, PR, split work, or release-tag guidance>
```

## Quality gate

- [ ] `git status` was reviewed before branch creation.
- [ ] `git diff`, `git diff --cached`, or the explicit user request was used as classification evidence.
- [ ] Branch type follows Git Flow: `feature` and `release` from `develop`, `hotfix` from `master`.
- [ ] Branch name is lowercase kebab-case and matches the selected type's format.
- [ ] Existing local and remote branch names were checked before creation.
- [ ] Branch creation was verified with `git status --short --branch`.
- [ ] Mixed or conflicting changes were reported instead of silently misclassified.
