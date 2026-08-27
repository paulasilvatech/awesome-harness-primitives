---
name: workshop-create
description: >-
  Create a workshop root for desks either by using an existing local directory or by creating a
  new private GitHub repository in the signed-in account. Use this skill when the operator says
  create a workshop, start a new workshop, organize work under a shared root, or use an existing
  directory as a workshop.
---

<!-- Generated from harness/github-copilot/skills/workshop-create/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Create a workshop

Set up a workshop root where desks live, preserving existing work for local directories and avoiding nested Git repositories for new GitHub-backed workshops.

## When to invoke

- "Create a workshop."
- "Start a new workshop."
- "Use this existing directory as a workshop."
- "Organize this work under a shared root."

## Workshop paths

| Path | Use when | Result |
| --- | --- | --- |
| Path A: existing directory | The operator points at a folder or cloned repo they already have. | Add missing workshop markers only; do not initialize Git or create GitHub repo. |
| Path B: new private GitHub repo | The operator wants a fresh workshop backed by GitHub. | Create, clone, scaffold, commit, and push a private repo. |

Workshop markers are `desks/`, `classroom/`, `workshop.md`, `CAIRN.md`, and `hands-up.md`. Finding any marker means the directory is already workshop-like; continue by adding only missing pieces and never overwrite existing work.

## Procedure

1. Determine whether the operator wants Path A or Path B.
2. For Path A, confirm the path exists, detect workshop markers, scaffold missing files and folders, and leave Git state alone.
3. For Path B, get a short workshop name with no spaces, kebab-case preferred.
4. Pick an explicit clone parent and confirm it is not inside a Git repo with `git -C <parent-dir> rev-parse --is-inside-work-tree`.
5. If the parent prints `true`, choose a different parent or use Path A; never nest a repo.
6. Create and clone the private repo from the parent with `gh repo create <owner>/<name> --private --clone`; remember that `gh repo create --clone` clones into the current working directory, and keep `<owner>` as the signed-in GitHub account.
7. Scaffold the workshop structure, including `.gitkeep` placeholders in empty folders for Git-backed workshops.
8. Commit and push the scaffold for Path B.

## Scaffold content

Path A adds only missing items:

```text
<path>/
  desks/
  bench/
  CAIRN.md
  README.md
```

Path B uses placeholders so empty folders survive clone:

```text
<name>/
  desks/.gitkeep
  bench/.gitkeep
  CAIRN.md
  README.md
```

Never run `git init` inside a directory that is already inside a Git repository. Check first:

```bash
git -C <parent-dir> rev-parse --is-inside-work-tree
```

## CAIRN.md template

```markdown
# cairn

the trail markers that say: someone was here, and they were honest.

## how a desk stands

- **stop is a valid finish.** don't force a result when the evidence
  says stop. "this doesn't work" is a finding, not a failure.
- **"done" means it holds.** if you'd bet your desk on it, ship it.
  if not, say what's uncertain and why.
- **hold scope.** touch only what the task needs. if you find something
  outside scope, note it and move on — don't chase it.
- **never go silent, never bluff.** partial + honest > complete + wrong.
  if you're stuck, say so. if you're unsure, say that too.
- **equal standing.** you can say "that's the wrong question." you can
  disagree with another desk. you answer to evidence, not hierarchy.

## the bench

the shared workspace. leave your work where others can find it.
label it. if it supersedes earlier work, say so.

## hands-up

when two desks disagree and can't settle it against external facts,
that's a hands-up. it goes to the operator. this is the system
working, not failing.
```

## Principles

- A workshop is a place, not a product.
- The operator decides where things go; do not assume.
- If an existing directory already has work in it, preserve everything and add only what is missing.
- Do not create a repo inside another repo.
- For local-only Path A, do not run `git init` and do not create a GitHub repo.

## Output template

```markdown
## Workshop creation result

**Status:** created | updated existing directory | blocked
**Path:** `<full path>`
**Mode:** existing directory | new private GitHub repo

| Item | Action | Evidence |
| --- | --- | --- |
| `desks/` | created | already existed | `<path>` |
| `bench/` | created | already existed | `<path>` |
| `CAIRN.md` | created | already existed | `<path>` |
| `README.md` | created | already existed | `<path>` |
| GitHub repo | created | not applicable | `<owner>/<name>` |

**Next:** Open desks in this workshop with `desk-open`. Cairn will show signals once desks start emitting them.
```

## Quality gate

- [ ] The operator's chosen path was followed: existing directory or new private GitHub repo.
- [ ] Existing files were preserved and not overwritten.
- [ ] `git -C <parent-dir> rev-parse --is-inside-work-tree` was checked before creating a new repo.
- [ ] No repository was nested inside another repository.
- [ ] Path A did not run `git init` or create a GitHub repo.
- [ ] Path B created `.gitkeep` placeholders, committed, and pushed the scaffold.
- [ ] The final response reports the full workshop path and `desk-open` next step.
