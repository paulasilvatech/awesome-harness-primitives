---
name: "conventional-branch"
description: >-
  Create, normalize, validate, and check out Git branches following the Conventional Branch specification with feature/, bugfix/, hotfix/, release/, and chore/ prefixes. Use when creating a new branch, naming a branch, or checking branch-name compliance.
---

# Conventional branch

Creates or validates Git branch names that follow the Conventional Branch format, detects the repository base branch, checks out the base, and creates the new branch when requested.

## When to invoke

- "Create a conventional branch for this task."
- "Name a branch for this bug fix."
- "Check whether this branch name follows the spec."
- "Create feature/issue-123-add-oauth from the default branch."
- "What branch type should I use?"

## Branch format

```text
<type>/<description>
```

| Type | Alias | Purpose |
| --- | --- | --- |
| `feature/` | `feat/` | New features or enhancements. |
| `bugfix/` | `fix/` | Bug fixes. |
| `hotfix/` | - | Urgent production fixes. |
| `release/` | - | Release preparation; dots allowed in versions such as `release/v1.2.0`. |
| `chore/` | - | Non-code tasks: deps, docs, config, automation. |

`main`, `master`, and `develop` are trunk branches. Do not create new branches with those names; branch off them instead.

## Naming rules

- Lowercase only; no uppercase letters.
- Use alphanumerics, hyphens, and dots: `a-z`, `0-9`, `-`, `.`.
- Allow dots only in `release/` version descriptions.
- Do not use underscores, spaces, or special characters.
- Do not use consecutive hyphens `--`, consecutive dots `..`, or hyphen-dot adjacency `-.` or `.-`.
- Do not start or end the description with a hyphen or dot.
- Prefer kebab-case with 2-5 words and about 50 characters total.

## Procedure

1. Determine branch type from the task; default to `feature` when uncertain.
2. Build the description from the task and include ticket or issue numbers, such as `feature/issue-123-add-oauth`, when supplied.
3. Normalize the name: lowercase, replace underscores and spaces with hyphens, collapse repeated hyphens, strip leading/trailing hyphens and dots.
4. Validate against the naming rules.
5. Detect the base branch using the remote default, then local trunks in priority order `develop`, `main`, `master`.
6. If asked to create the branch, check out and update the base, then create the branch.

```bash
git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||'
for b in develop main master; do
  git show-ref --verify --quiet "refs/heads/$b" && echo "$b" && break
done
git checkout <base>
git pull origin <base>
git checkout -b <type>/<description>
git push -u origin <branch-name>
```

Only run `git push -u origin <branch-name>` when the user asks to push or publish.

## Examples

| Valid | Why |
| --- | --- |
| `main` | Trunk branch. |
| `master` | Trunk branch. |
| `develop` | Trunk branch. |
| `feature/add-login-page` | Feature branch in kebab-case. |
| `feat/add-login-page` | Accepted alias. |
| `bugfix/fix-header-bug` | Bug fix branch. |
| `fix/header-bug` | Accepted alias. |
| `hotfix/security-patch` | Urgent production fix. |
| `release/v1.2.0` | Release branch with version dots. |
| `chore/update-dependencies` | Maintenance branch. |
| `feature/issue-123-new-login` | Includes issue number. |

| Invalid | Problem | Correction |
| --- | --- | --- |
| `Feature/Add-Login` | Uppercase letters. | `feature/add-login` |
| `feature/new--login` | Consecutive hyphens. | `feature/new-login` |
| `feature/-new-login` | Leading hyphen. | `feature/new-login` |
| `feature/new-login-` | Trailing hyphen. | `feature/new-login` |
| `release/v1.-2.0` | Hyphen adjacent to dot. | `release/v1.2.0` |
| `fix/header bug` | Space. | `fix/header-bug` |
| `fix/header_bug` | Underscore. | `fix/header-bug` |
| `unknown/some-task` | Unknown prefix type. | Choose an allowed type. |

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `git-commit` | skill | The task is commit message generation or commit execution, not branch naming. |

## Branch and commit alignment examples

| Branch | Typical commit |
| --- | --- |
| `feature/add-oauth-login` | `feat: add login page` |
| `bugfix/fix-header` | `fix: header overflow on mobile` |
| `chore/update-deps` | `chore: bump lodash to 5.0` |
| `release/v1.2.0` | `chore: release v1.2.0` |

Use `feature/*` with `feat:` commits where possible. Good descriptions include `fix-header`, `fix-header-overflow`, and `update-ci-config`; weak descriptions include `fix-bug` and `new-feature`.

## Output template

```markdown
### Conventional branch result

**Status:** created | name only | invalid | blocked
**Base branch:** `<base>`
**Branch name:** `<type>/<description>`

**Validation**
- Type: pass | fail
- Description format: pass | fail
- Trunk handling: pass | fail

**Commands run**
- `git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||'`
- `git checkout <base>`
- `git pull origin <base>`
- `git checkout -b <type>/<description>`

**Next step:** `git push -u origin <branch-name>` when ready.
```

## Quality gate

- [ ] Branch name follows `<type>/<description>` or is an existing trunk branch.
- [ ] Type is `feature`, `feat`, `bugfix`, `fix`, `hotfix`, `release`, or `chore`.
- [ ] Description is lowercase kebab-case with no invalid dot or hyphen sequences.
- [ ] Dots appear only for `release/` versions.
- [ ] The base branch was detected before creating a branch.
- [ ] Push was not run unless requested.

## References

- [Conventional Branch](https://conventional-branch.github.io)
- [Conventional Commits](https://www.conventionalcommits.org)
