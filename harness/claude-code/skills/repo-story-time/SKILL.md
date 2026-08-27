---
name: repo-story-time
description: >-
  Analyze a Git repository and create two archaeology deliverables: REPOSITORY_SUMMARY.md with
  technical architecture and THE_STORY_OF_THIS_REPO.md with a narrative from commit history. Use
  when asked to summarize a repo, explain its architecture, inspect git history, identify
  contributors, or tell the story of repository evolution.
---

<!-- Generated from harness/github-copilot/skills/repo-story-time/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Repo story time

Turn repository structure, documentation, source files, and git history into two written artifacts: `REPOSITORY_SUMMARY.md` for technical understanding and `THE_STORY_OF_THIS_REPO.md` for the human narrative behind the code.

## When to invoke

- "Analyze this repo and summarize its architecture."
- "Tell the story of this repository from git history."
- "Create REPOSITORY_SUMMARY.md and THE_STORY_OF_THIS_REPO.md."
- "Who has worked on this repo and what changed over time?"
- "Do repository archaeology and write the findings to files."

## Deliverables

| File | Purpose | Required content |
| --- | --- | --- |
| `REPOSITORY_SUMMARY.md` | Technical architecture and purpose overview. | Overview, architecture, key components, technologies, data flow, team and ownership. |
| `THE_STORY_OF_THIS_REPO.md` | Narrative story from commit history. | A year in numbers, cast of characters, seasonal patterns, great themes, plot twists, current chapter. |

Create and write both files in the repository root. Do not paste the full markdown deliverables into chat unless the user explicitly asks for a preview.

## Repository exploration

Run repository-safe equivalents for the current shell. On PowerShell, these commands match the original workflow:

```powershell
Get-ChildItem -Recurse -Include "*.md","*.json","*.yaml","*.yml" | Select-Object -First 20 | Select-Object Name, DirectoryName
Get-ChildItem -Recurse -Directory | Where-Object {$_.Name -notmatch "(node_modules|\.git|bin|obj)"} | Select-Object -First 30 | Format-Table Name, FullName
```

On POSIX shells, use equivalent `find` commands that exclude `.git`, `node_modules`, `bin`, and `obj`. Then inspect configuration files such as `package.json`, `pom.xml`, `requirements.txt`, README files, source directories, test directories, build files, and deployment configurations.

## Technical analysis criteria

| Area | Questions to answer |
| --- | --- |
| Purpose | What problem does the repository solve and for whom? |
| Architecture | How is the code organized into apps, packages, modules, services, or libraries? |
| Technologies | Which languages, frameworks, runtimes, package managers, and platforms appear? |
| Key Components | Which modules, services, features, CLI entry points, APIs, tests, or docs matter most? |
| Data Flow | How does information enter, move through, persist, and leave the system? |
| Team and Ownership | Which contributors or teams appear to own different areas? |

## Commit history analysis

Run each command, inspect its output, then decide whether more targeted git commands are needed.

| Step | Command | Evidence captured |
| --- | --- | --- |
| Total commits | `git rev-list --all --count` | Repository lifetime size. |
| Last year count | `(git log --oneline --since="1 year ago").Count` | Recent activity volume in PowerShell. Use `git log --oneline --since="1 year ago" | wc -l` on POSIX. |
| Contributors | `git shortlog -sn --since="1 year ago" | Select-Object -First 20` | Main contributors and relative activity. |
| Activity by month | `git log --since="1 year ago" --format="%ai" | ForEach-Object { $_.Substring(0,7) } | Group-Object | Sort-Object Count -Descending | Select-Object -First 12` | Busy months. |
| Change themes | `git log --since="1 year ago" --oneline --grep="feat|fix|update|add|remove" | Select-Object -First 50` | Feature, fix, update, add, and remove patterns. |
| Hot files | `git log --since="1 year ago" --name-only --oneline | Where-Object { $_ -notmatch "^[a-f0-9]" } | Group-Object | Sort-Object Count -Descending | Select-Object -First 20` | Frequently changed files. |
| Merges | `git log --since="1 year ago" --merges --oneline | Select-Object -First 20` | Collaboration and integration patterns. |
| Seasonality | `git log --since="1 year ago" --format="%ai" | ForEach-Object { $_.Substring(5,2) } | Group-Object | Sort-Object Name` | Monthly rhythm and possible release/holiday effects. |

## Narrative synthesis

| Narrative element | What to look for |
| --- | --- |
| Characters | Main contributors, specialties, ownership zones, and collaboration style. |
| Seasons | Month/quarter rhythms, holidays, releases, incidents, and quiet periods. |
| Themes | Dominant work types: features, fixes, refactoring, documentation, tests, infrastructure. |
| Conflicts | Files or subsystems with frequent change, reversions, merge density, or recurring fixes. |
| Evolution | How the repository grew, shifted stacks, reorganized modules, or stabilized over time. |

Be specific. Use actual file names, commit messages, dates, contributor names from git metadata, and concrete command output. Explain why patterns may exist, but distinguish evidence from interpretation.

## Procedure

1. Explore repository structure and documentation.
2. Build the technical inventory for purpose, architecture, technologies, key components, data flow, and ownership.
3. Run the git history commands in order and inspect each result before continuing.
4. Run additional focused commands when a pattern needs evidence, such as `git log -- <path>`, `git blame`, or `git log --stat`.
5. Write `REPOSITORY_SUMMARY.md` and `THE_STORY_OF_THIS_REPO.md` in the repository root.
6. Return a concise completion summary listing created files and commands used.

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `ACTUALLY`
- `Build/deployment`
- `CREATE`
- `CREATED`
- `CRITICAL`
- `EXECUTE`
- `Monthly/quarterly`
- `WRITE`
- `copy/paste`
- `editFiles`
- `modules/services/features`
- `month/quarter`
- `non-technical`

## Output template

```markdown
## Repo story time result

**Status:** complete | blocked
**Files created:**
- `REPOSITORY_SUMMARY.md`
- `THE_STORY_OF_THIS_REPO.md`

### Evidence reviewed
- Structure: <commands/files inspected>
- Git history: <commands run>

### Notes
- <important caveat, missing history, shallow clone, or interpretation limit>
```

## Quality gate

- [ ] `REPOSITORY_SUMMARY.md` and `THE_STORY_OF_THIS_REPO.md` were actually created in the repository root.
- [ ] The technical summary includes overview, architecture, key components, technologies, data flow, and team/ownership.
- [ ] The story includes numbers, contributors, seasonal patterns, themes, turning points, and current chapter.
- [ ] Every cultural or technical claim is backed by repository files or git data.
- [ ] Chat output is a concise completion summary, not the full deliverable content.
- [ ] `_SUMMARY`, `_REPO`, `REPOSITORY_SUMMARY.md`, and `THE_STORY_OF_THIS_REPO.md` are preserved.
