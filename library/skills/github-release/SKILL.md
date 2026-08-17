---
name: github-release
description: >-
  Run an end-to-end GitHub library release workflow with git and gh: inspect tags, classify public API changes, choose a SemVer bump, update CHANGELOG.md, create release/vX.Y.Z, push, and open a release PR. Use when asked to cut a release, bump a version, generate a changelog, create a release branch, or publish a new GitHub repository version.
metadata:
  compatibility: "requires: gh CLI and git"
---

# GitHub release

Release a single-package GitHub repository by reading tags and public diffs, selecting the next SemVer version, updating `CHANGELOG.md`, creating a release branch, and opening a pull request with `gh`. Keep steps 1 through 4 read-only; write only after the version is confirmed.

## When to invoke

- "Cut a new GitHub release."
- "Bump the version and generate a changelog."
- "Create a release branch and PR."
- "Let's ship a new version."
- "Publish a new version from this repository."

## Prerequisites and context

- Requires `gh` authenticated with `gh auth status` and a working `git` checkout inside a GitHub repository.
- Verify `gh repo view --json nameWithOwner` succeeds before release work.
- Start from a clean working tree unless the user explicitly directs how to handle local changes.
- Ask for the public-facing source directory once and store it as `PUBLIC_PATH`; examples include `src/`, `lib/`, `pkg/`, or `cmd/`; if empty, use `.`.
- Exclude `tests/`, `test/`, `spec/`, `__tests__/`, `docs/`, `*.lock`, `*-lock.json`, `*.sum`, generated files with a do-not-edit header, and build artifacts from public API classification.

## Procedure

1. Ensure `main` is current:

   ```bash
   git checkout main
   git pull origin main
   ```

2. Fetch and identify the latest version tag from git tags, not `gh release list`:

   ```bash
   git fetch --tags
   PREV_TAG=$(git tag --sort=-version:refname | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+' | head -1)
   echo "Latest tag: $PREV_TAG"
   git ls-remote --tags origin | grep "refs/tags/$PREV_TAG$"
   PREV_SHA=$(git rev-list -n 1 "$PREV_TAG" 2>/dev/null || git rev-list --max-parents=0 HEAD)
   ```

   `PREV_TAG` must preserve the tag spelling exactly, for example `v1.4.2`, while arithmetic strips a leading `v`. If no tag exists, set `PREV_TAG` to `(none)`, set `PREV_SHA` to `git rev-list --max-parents=0 HEAD`, default `NEXT_VERSION` to `1.0.0`, and skip SemVer arithmetic. If the tag is local-only or orphaned, warn before continuing.

3. Analyze the code diff as the primary signal:

   ```bash
   git diff "$PREV_SHA"..HEAD -- "$PUBLIC_PATH" \
     ':(exclude)tests/' ':(exclude)test/' ':(exclude)spec/' \
     ':(exclude)__tests__/' ':(exclude)docs/' \
     ':(exclude)*.lock' ':(exclude)*-lock.json' ':(exclude)*.sum'
   ```

   If the diff is huge, triage with `git diff "$PREV_SHA"..HEAD --stat -- "$PUBLIC_PATH"` and then focus on public interface files such as `index.*`, `api.*`, `exports.*`, `public.*`, `mod.*`, and `__init__.*`.

4. Read commit intent as the secondary signal:

   ```bash
   git log "$PREV_SHA"..HEAD --oneline --no-merges
   ```

   Use the bundled `references/commit-classification.md` only to interpret messages such as `feat: new API`, `fix: typo`, `chore: refactor`, or a one-line security fix whose intent is not self-explanatory from code; prefer the code diff when signals conflict.

5. Determine the highest SemVer bump and present the proposed `NEXT_VERSION` with evidence. Ask for confirmation before writing. Compute from `MAJOR.MINOR.PATCH` and format as `vMAJOR.MINOR.PATCH`; highest precedence wins: `MAJOR > MINOR > PATCH`.

6. Create and push the release branch only after confirmation:

   ```bash
   git checkout -b release/vX.Y.Z
   git push -u origin release/vX.Y.Z
   ```

7. Update or create `CHANGELOG.md` in Keep a Changelog format using today's `YYYY-MM-DD` date, show the proposed section to the user, then write it. Add or update the comparison link: `https://github.com/OWNER/REPO/compare/vPREV...vNEXT`.

8. Commit and push:

   ```bash
   git add CHANGELOG.md
   git commit -m "chore: release vX.Y.Z"
   git push origin release/vX.Y.Z
   ```

9. Open the release PR. Always use `--body-file`, not inline `--body`; inline `\n` can render literally in PowerShell. Create `release_pr_body.md` or an equivalent repo-local scratch file, then run:

   ```bash
   gh pr create --base main --head release/vX.Y.Z --title "Release vX.Y.Z" --body-file release_pr_body.md
   ```

10. Hand off tagging after merge:

   ```bash
   git tag vX.Y.Z <merge-commit-sha>
   git push origin vX.Y.Z
   ```

## SemVer classification

| Evidence from public diff | Bump | Changelog section |
| --- | --- | --- |
| Removed symbols, changed signatures, or breaking behavior changes | `MAJOR` | `Removed` or `Changed` with breaking note |
| New exported symbols or user-visible features such as `NewClient` or `WithTimeout` in `src/client.go` | `MINOR` | `Added` |
| Bug/logic fix, off-by-one correction, performance improvement, security fix, docs, chore only | `PATCH` | `Fixed` or `Security`; omit purely internal work |
| No commits since last tag | none | Report nothing to release |

When a commit says `fix: typo` but the diff removes a public method, classify as `MAJOR`. When a commit says `feat: new API` but only private internals changed, classify as `PATCH`. Document every conflict in the changelog review.

Treat HTTP API surface changes as public when the library exposes handlers, middleware, generated clients, or route contracts. Keep `PATH` changes only when they alter public CLI behavior.

## Changelog rules

Insert directly below `# Changelog`:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Deprecated
- ...

### Removed
- ...

### Fixed
- ...

### Security
- ...
```

Omit empty headings. Write plain English from the user's perspective, not raw commit messages. Map a new exported symbol to Added, a breaking removal to Removed, a breaking existing API change to Changed, a bug or perf fix to Fixed, and a security fix to Security.

## PowerShell equivalents

Use PowerShell-safe forms on Windows:

```PowerShell
git fetch --tags
$prevTag = git tag --sort='-version:refname' | Select-String '^[vV]?\d+\.\d+\.\d+' | Select-Object -First 1 -ExpandProperty Line
if ($prevTag) { $prevSha = git rev-list -n 1 $prevTag } else { $prevSha = git rev-list --max-parents=0 HEAD }
git diff "$($prevSha)..HEAD" -- $publicPath ':(exclude)tests/' ':(exclude)test/' ':(exclude)spec/' ':(exclude)__tests__/' ':(exclude)docs/' ':(exclude)*.lock' ':(exclude)*-lock.json' ':(exclude)*.sum'
```

For the PR body, use a here-string, write with `Out-File -FilePath release_pr_body.md -Encoding utf8 -NoNewline`, and pass `--body-file release_pr_body.md`. If `gh` usage appears unexpectedly, check `Get-Command gh`, `gh --version`, `git fetch --tags`, and `git diff --name-only $prevSha..HEAD -- src/`.

## Progressive disclosure and bundled resources

Read bundled references only when the release decision needs deeper rules:

- `references/semver-rules.md`: extended SemVer edge cases for `MAJOR`, `MINOR`, and `PATCH`.
- `references/commit-classification.md`: commit-message heuristics for secondary signal classification.

## Troubleshooting

| Situation | Resolution |
| --- | --- |
| `gh auth status` fails | Stop and tell the user to run `gh auth login`. |
| Not inside a git repo | Stop and tell the user to `cd` into the repository. |
| Working tree is dirty | Warn and ask whether to stash, commit, or abort. |
| No commits since last tag | Tell the user there is nothing to release. |
| Tag exists locally but not remotely | Warn that the tag appears local-only and ask whether to push or continue. |
| Tag points to no commit | Use `git rev-list --max-parents=0 HEAD` as the fallback diff base and warn. |
| Diff is empty for `PUBLIC_PATH` but commits exist | Warn that changes may be internal and ask whether to proceed. |
| `git push` fails | Report the error verbatim and suggest checking protected branch rules. |

## Gotchas

- **Do not use `gh release list` as source of truth**: releases are optional; tags are authoritative.
- **Do not create `release/vX.Y.Z` before version confirmation**: branch names must match the final version.
- **Do not use inline `--body` for multiline PR text**: use `--body-file` so markdown line breaks survive Bash and PowerShell.
- **Do not classify from commits alone**: code diff is primary; commit log is context.
- **IMPORTANT** defaults: represent no previous tag as `(none)`, default the first release to `1.0.0`, and use `git tag` only after the release PR merges.

## Output template

```markdown
## GitHub release result

**Status:** PR opened | ready for PR | blocked
**Previous tag:** `<PREV_TAG>`
**Previous SHA:** `<PREV_SHA>`
**Next version:** `<NEXT_VERSION>`
**Public path:** `<PUBLIC_PATH>`

### Classification
| Evidence | Bump impact | Changelog entry |
| --- | --- | --- |
| `<file or commit evidence>` | `MAJOR | MINOR | PATCH` | `<entry or omitted>` |

### Commands run
- `gh auth status`
- `gh repo view --json nameWithOwner`
- `git status`
- `git fetch --tags`
- `git diff <PREV_SHA>..HEAD -- <PUBLIC_PATH>`
- `git log <PREV_SHA>..HEAD --oneline --no-merges`
- `git checkout -b release/vX.Y.Z`
- `git push -u origin release/vX.Y.Z`
- `gh pr create --base main --head release/vX.Y.Z --title "Release vX.Y.Z" --body-file release_pr_body.md`

### Handoff
After merge, create the tag:
`git tag vX.Y.Z <merge-commit-sha>`
`git push origin vX.Y.Z`
```

## Quality gate

- [ ] `gh auth status`, `gh repo view --json nameWithOwner`, and `git status` were checked before changes.
- [ ] `PREV_TAG`, `PREV_SHA`, `PUBLIC_PATH`, and `NEXT_VERSION` are recorded.
- [ ] Public diff and commit log were both read; conflicts favor code diff.
- [ ] The proposed SemVer bump cites concrete public API evidence.
- [ ] `CHANGELOG.md` follows Keep a Changelog, omits empty sections, and includes the compare URL.
- [ ] The release branch is named `release/vX.Y.Z` and was created only after confirmation.
- [ ] The PR uses `--body-file` and includes the changelog section or a clear placeholder.
- [ ] The final handoff tells the user to tag the merge commit and push the tag.

## References

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [GitHub compare URL pattern](https://github.com/OWNER/REPO/compare/vPREV...vNEXT)
