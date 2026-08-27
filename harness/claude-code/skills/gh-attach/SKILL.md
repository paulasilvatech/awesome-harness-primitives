---
name: gh-attach
description: >-
  Upload, download, and embed GitHub user-attachments with the gh attach extension for
  screenshots, images, PDFs, zip files, and videos. Use this skill when asked to attach a
  screenshot to a PR, add an image to an issue, embed before/after media, attach a local file, or
  download a GitHub attachment.
---

<!-- Generated from harness/github-copilot/skills/gh-attach/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# gh-attach

Use `gh attach` to move local files through GitHub's internal user-attachments flow, produce a renderable attachment URL, and embed or download that URL from pull requests, issues, and comments without exposing private repository attachments to anonymous viewers.

The printed URL is used as-is; GitHub renders it as image/video/file content and keeps private-repo visibility rules.

## When to invoke

- "Attach this screenshot to the PR."
- "Add this image to the issue comment."
- "Embed before and after screenshots."
- "Upload this zip file to GitHub."
- "Download this GitHub user attachment."

## Prerequisites and context

Install the GitHub CLI extension if it is missing:

```sh
gh extension list | grep -q 'gh attach' || gh extension install sudosubin/gh-attach
```

Authentication rules:

| Context | Requirement |
| --- | --- |
| Normal desktop use | `gh` must be authenticated so `gh-attach` can select the matching browser account. |
| Multiple browser accounts | Add `--browser <name> --profile <name>` when the wrong account is selected. |
| Headless use | Set `GH_ATTACH_SESSION_TOKEN` to the bare `user_session` cookie value. Treat `GH_ATTACH_SESSION_TOKEN` as a full account credential. |
| Private attachments | The URL renders only for authorized viewers; anonymous fetches returning 404 or 403 are expected. |
| GHES | Use `-R host/owner/repo` so the extension targets the correct host. |

## Procedure

1. Confirm the file exists and use an absolute quoted path for upload.
2. Upload with `gh attach`. Use `-R <owner>/<repo>` outside a repository; use `-R host/owner/repo` for GHES.
3. Capture the single-line URL exactly as printed.
4. Embed through GitHub CLI commands that support `--body-file -`, such as `gh pr comment`, `gh pr edit`, `gh issue comment`, or `gh issue edit`.
5. For downloads, specify the destination explicitly with `-O`.

```sh
URL=$(gh attach "$FILE" -R <owner>/<repo>)
printf '## Screenshots

%s
' "$URL" | gh pr comment <pr> -R <owner>/<repo> --body-file -
gh attach download "$URL" -O "$FILE"
```

## Attachment handling

| Task | Command shape | Notes |
| --- | --- | --- |
| Upload local file | `gh attach "$FILE" -R <owner>/<repo>` | Prints the user-attachments URL on one line. |
| Embed markdown | `printf '...%s...' "$URL" | gh pr comment <pr> --body-file -` | Always pipe with `--body-file -` to preserve formatting and avoid shell quoting issues. |
| Control image size | `<img width="800" src="$URL">` | Use HTML when the bare URL renders too large. |
| Download attachment | `gh attach download "$URL" -O "$FILE"` | Private attachments use the active `gh` token, with browser cookies as an authorization fallback. |

GitHub Cloud and GHES decide which file extensions and content types are accepted. Do not transform the URL; GitHub auto-renders images, videos, and file links where the URL is pasted.

The same `--body-file -` pattern applies to `gh pr comment/edit` and `gh issue comment/edit` workflows; use the command variant that matches whether you are creating or editing a comment.

## Gotchas

- **No public upload API exists**: `gh attach` uses GitHub's internal user-attachments endpoint and a browser session cookie.
- **Session cookies are credentials**: never print, commit, or share `GH_ATTACH_SESSION_TOKEN` or the `user_session` value.
- **Private URLs are still private**: a 404 or 403 from an anonymous request does not prove upload failure.
- **Use absolute paths**: relative file paths are easy to resolve against the wrong working directory when commenting on another repository.

## Output template

````markdown
## GitHub attachment result

**Status:** uploaded | embedded | downloaded | blocked
**Repository:** `<owner>/<repo or host/owner/repo>`

| File | Action | URL or destination | Evidence |
| --- | --- | --- | --- |
| `<absolute file path>` | `upload/embed/download` | `<attachment URL or output path>` | `<command result>` |

**Markdown used**
```markdown
<final markdown body or "not applicable">
```

**Validation**
- `gh attach`: pass | fail | not run
- GitHub comment/edit/download: pass | fail | not run
````

## Quality gate

- [ ] `gh-attach` is installed or the install command was provided.
- [ ] Uploads use an absolute quoted path and the correct `-R` owner/repo or host/owner/repo.
- [ ] `GH_ATTACH_SESSION_TOKEN` and browser cookie values are never exposed.
- [ ] PR and issue updates use `--body-file -` rather than fragile inline bodies.
- [ ] Private attachment visibility is described correctly as authorized-only.
- [ ] Downloads use `gh attach download "$URL" -O "$FILE"` with an explicit destination.
