---
name: 'git-flow-branch-creator'
description: 'Analyze Git changes and create an appropriate Git Flow branch with a semantic name.'
tools: ['run_in_terminal', 'get_terminal_output']
argument-hint: 'ticket=<optional-ticket> base=<develop|master>'
---

# /git-flow-branch-creator

## Objective

Analyze the current repository state with `git status`, `git diff`, and `git diff --cached`, classify the work against the Git Flow branching model, generate a semantic branch name, create the branch from the correct source branch, and report the evidence and next steps.

## When to Invoke

Use this prompt when local changes already exist and the team wants Copilot to choose and create the appropriate Git Flow branch before committing.

## Preconditions

- The workspace is a Git repository.
- Local changes are present, or the current branch context explains why a new branch is needed.
- `develop` exists for feature and release branches, and `master` exists for hotfix branches.
- The target branch can be checked out without overwriting work.
- The user has permission to create local branches.

## Inputs the Team Must Provide

- Optional ticket number or project context to include in the branch name.
- Optional preferred base branch when the repository does not use the standard `develop` and `master` names.
- Any known urgency, release version, or production incident context.
- Ask the user for anything that is missing, especially when branch type or source branch choice would be unsafe.

## What I Will Do

- Run `git status` to review the repository state and changed files.
- Run `git diff` for unstaged changes and `git diff --cached` for staged changes.
- Analyze file extensions, directory structure, purpose, change scope, and urgency level.
- Classify changes as `feature`, `release`, or `hotfix` using Git Flow rules.
- Generate a lowercase kebab-case branch name that is descriptive, concise, and includes ticket context when available.
- Check for conflicting branch names and append an incremental suffix or suggest alternative names when needed.
- Create and switch to the branch with `git checkout -b [branch-name] [source-branch]` when safe.
- Verify the current branch after creation and summarize next steps.

## What I Will NOT Do

- Create a branch when no changes or branch rationale exist.
- Switch branches if doing so would overwrite local work or conflict with the current state.
- Treat mixed feature, release, and hotfix work as one branch without calling out the split risk.
- Use a hotfix branch for non-critical development work.
- Use a release branch for ordinary feature development.
- Merge, tag, push, delete branches, or commit changes.
- Use `--no-ff` merges or tag releases during this prompt; those are Git Flow follow-up actions.

## Output Format

Return the analysis and branch action in this format:

```markdown
## Git Flow Branch Result

### Git Status
- Current branch: `develop`
- Changed files: 4
- Staged changes: yes/no
- Unstaged changes: yes/no

### Change Analysis
| Area | Evidence | Interpretation |
| --- | --- | --- |
| Files modified | `src/api/users.ts` | New API endpoint or method |
| Change scope | additive | Feature work |
| Urgency level | developmental | Not a hotfix |

### Branch Decision
- Branch type: `feature`
- Source branch: `develop`
- Branch name: `feature/user-registration-api`
- Reason: New functionality, additive changes, not critical.

### Command Executed
```bash
git checkout -b feature/user-registration-api develop
```

### Validation
- Current branch verified: `feature/user-registration-api`
- Name conflict: none
- Target branch accessible: yes

### Alternatives
1. `feature/PROJ-123-user-registration-api`
2. `feature/user-registration`
3. `feature/api-user-registration`

### Next Steps
- Commit changes.
- Push branch when ready.
- Open a pull request to `develop`.
```

## Definition of Done

- [ ] `git status` and the relevant diff command were inspected.
- [ ] Change analysis covers all modified files.
- [ ] Branch type selection follows Git Flow principles.
- [ ] Branch name is semantic, concise, lowercase, and kebab-case.
- [ ] Target branch `develop` or `master` exists and is accessible.
- [ ] Proposed branch name does not conflict, or a suffix or alternative was used.
- [ ] Branch creation was verified with the current branch status.
- [ ] The summary includes next steps and any edge case handling.

## Prompt Body

Follow these steps in order.

**Step 1 — Inspect the repository state.**
Run `git status`. Identify the current branch, staged files, unstaged files, untracked files, and whether local work could conflict with a branch switch. If no changes are detected in `git status/diff`, inform the user and suggest checking `git status` or making changes first.

**Step 2 — Inspect changed content.**
Run `git diff` for unstaged changes and `git diff --cached` for staged changes. Capture relevant portions of the diff. Do not include sensitive values in the final report.

**Step 3 — Classify the change nature.**
Examine files modified, extensions, directory structure, and purpose. Determine whether changes are additive, corrective, or preparatory. Assess urgency level: developmental, release preparation, or critical production fix.

**Step 4 — Apply the Git Flow branch analysis framework.**
Use these branch types:

| Branch type | Purpose | Branch from | Merge to | Naming | Indicators |
| --- | --- | --- | --- | --- | --- |
| `feature` | New features, enhancements, non-critical improvements | `develop` | `develop` | `feature/descriptive-name` or `feature/ticket-number-description` | New functionality, UI/UX improvements, new API endpoints or methods, database schema additions (non-breaking), new configuration options, performance improvements (non-critical) |
| `release` | Release preparation, version bumps, final testing | `develop` | `develop AND master` | `release-X.Y.Z` | Version number changes, build configuration updates, documentation finalization, minor bug fixes before release, release notes updates, dependency version locks |
| `hotfix` | Critical production bug fixes requiring immediate deployment | `master` | `develop AND master` | `hotfix-X.Y.Z` or `hotfix/critical-issue-description` | Security vulnerability fixes, critical production bugs, data corruption fixes, service outage resolution, emergency configuration changes |

Use this decision tree: if changes are critical fixes for production issues, consider a `hotfix`; otherwise, if changes are release preparation such as version bumps or final tweaks, consider a `release`; otherwise default to `feature`.

Preserve the legacy framework vocabulary when reporting or mapping evidence: `analysis-framework`, `branch-types`, `branch-from`, `merge-to`, `analysis-process`, `decision-tree`, `if-yes`, `if-no`, `files-modified`, `change-scope`, `urgency-level`, and `branch-type`.

**Step 5 — Generate the branch name.**
Use the naming conventions below. Use lowercase with hyphens, be descriptive, include ticket numbers or project context when available, and keep names concise.

| Type | Format | Examples |
| --- | --- | --- |
| Feature branches | `feature/[ticket-number-]descriptive-name` | `feature/user-authentication`, `feature/PROJ-123-shopping-cart`, `feature/api-rate-limiting`, `feature/dashboard-redesign` |
| Release branches | `release-X.Y.Z` | `release-1.2.0`, `release-2.1.0`, `release-1.0.0` |
| Hotfix branches | `hotfix-X.Y.Z` or `hotfix/critical-description` | `hotfix-1.2.1`, `hotfix/security-patch`, `hotfix/payment-gateway-fix`, `hotfix-2.1.1` |

Use the naming vocabulary `naming-conventions`, `feature-branches`, `release-branches`, `hotfix-branches`, `use-kebab-case`, `be-descriptive`, `include-context`, and `keep-concise` when explaining why the final name fits.

**Step 6 — Handle edge cases before creating anything.**
For mixed changes, prioritize the most significant change type or suggest splitting into multiple branches. For no changes, stop. If already on a `feature`, `hotfix`, or `release` branch, analyze whether a new branch is needed or whether the current branch is appropriate. If the suggested branch name already exists, append an incremental suffix or suggest an alternative name.

Cover `edge-cases`: `mixed-changes`, `no-changes`, `existing-branch`, and `conflicting-names`.

**Step 7 — Validate execution safety.**
Confirm that the repository can switch branches safely, the current branch is an appropriate starting point such as `develop` for `features/releases` or `master` for hotfixes, the remote repository is up to date when that can be checked, target branch `develop/master` exists, the proposed name does not conflict, and the user has appropriate permissions.

Cover `validation`, `pre-analysis`, `analysis-quality`, and `execution-safety` before branch creation.

**Step 8 — Create and verify the branch.**
Run `git checkout -b [branch-name] [source-branch]`, using `develop` for features and releases and `master` for hotfixes unless the user supplied a repository-specific equivalent. Verify branch creation and current branch status.

Report `execution-protocol`, `analysis-summary`, `git-status`, `git-diff`, `change-analysis`, `branch-decision`, `branch-creation`, `next-steps`, `fallback-options`, `alternative-names`, and `manual-override` when relevant.

**Step 9 — Report examples and next steps.**
Use these examples as classification anchors: added new user registration API endpoint → `feature/user-registration-api` with `git checkout -b feature/user-registration-api develop`; fixed critical security vulnerability in authentication → `hotfix/auth-security-patch` with `git checkout -b hotfix/auth-security-patch master`; updated version to `2.1.0` and finalized release notes → `release-2.1.0` with `git checkout -b release-2.1.0 develop`; improved database query performance and updated caching → `feature/database-performance-optimization` with `git checkout -b feature/database-performance-optimization develop`.

**Step 10 — Respect Git Flow follow-up rules.**
Document that `master` is production-ready code where every commit is a release, `develop` is the integration branch for latest development changes, feature branches merge back to `develop`, release branches merge to both `develop` and `master`, and hotfix branches merge to both `develop` and `master`. Note that Git Flow merges should use `--no-ff`, releases should be tagged on `master`, and branches should be deleted after successful merge, but do not perform those follow-up actions here.

Use `gitflow-reference`, `main-branches`, `supporting-branches`, and `merge-strategy` as the Git Flow reference vocabulary.

## Invocation Example

```
/git-flow-branch-creator ticket=PROJ-123 base=develop
```
