---
name: "pr-screenshots"
description: >-
  Embed before/after screenshots and annotated images in pull request descriptions so reviewers can inspect visible changes quickly. Use this skill when a PR changes layout, styling, CSS, charts, dashboards, data visualizations, UI components, forms, modals, error messages, CLI output, or log formatting.
---

# PR screenshots

Prepare pull request screenshot evidence by choosing the right visual pairs, preserving comparison fidelity, uploading images through the host platform, and returning markdown ready for the PR description.

## When to invoke

- "Add before and after screenshots to this PR."
- "This CSS change needs visual evidence in the pull request."
- "Embed dashboard screenshots in the PR description."
- "Show reviewers the CLI output formatting change."
- "Add annotated images for this subtle UI change."

## Visual evidence rules

| Situation | Screenshot evidence | Notes |
| --- | --- | --- |
| Layout, styling, or CSS | Before and after from the same viewport and crop | Capture before state before changing code whenever possible. |
| Charts, dashboards, or data visualizations | Before and after with the same data fixture or date range | State the data condition briefly. |
| UI components, forms, or modals | Component state screenshots for each changed state | Include hover, validation, and error states when relevant. |
| Error messages, CLI output, or log formatting | Terminal or log screenshots only when text formatting matters | Prefer text snippets when screenshots add no value. |
| Subtle visual differences | Annotated screenshots with callouts | Use an image annotation workflow when the difference is not obvious. |

Place screenshots directly in the PR description body. Avoid hiding evidence in `<details>` blocks because reviewers are less likely to open collapsed content. Keep captions to one or two sentences and let the image carry most of the communication.

## PR description patterns

Use a simple pair for one visual change:

```markdown
**Before** - brief description of the problem:

![before](url-to-before-image)

**After** - brief description of the fix:

![after](url-to-after-image)
```

Use headings for multiple visual changes:

```markdown
## Filter bar alignment

**Before** - 1px border clash between adjacent buttons:

![before-filters](url)

**After** - borders overlap cleanly, hover tint added:

![after-filters](url)

## Chart tooltip

**Before** - tooltip clipped at container edge:

![before-tooltip](url)

**After** - tooltip repositions to stay visible:

![after-tooltip](url)
```

## Image sizing and fidelity

- Take screenshots at native 1x resolution; do not resize with PIL because resampling creates artifacts.
- Control display size in markdown with HTML only when images are too large:

```html
<img src="url" width="600" alt="description">
```

- Before and after pairs must use the same viewport width and crop. A different viewport or crop makes the comparison unreliable.
- Very large images over 10MB may not render inline on some platforms; crop to the relevant region before upload instead of compressing until text becomes blurry.

## Uploading images

### Azure DevOps

Upload images as PR attachments through the REST API:

```powershell
$token = az account get-access-token `
    --resource "499b84ac-1321-427f-aa17-267ca6975798" `
    --query accessToken -o tsv

$base = "https://{org}.visualstudio.com/{projectId}/_apis/git/repositories/{repoId}"
$url = "$base/pullRequests/{prId}/attachments/screenshot.png?api-version=7.1-preview.1"

# Use HttpClient; Invoke-RestMethod can corrupt binary data.
$client = New-Object System.Net.Http.HttpClient
$client.DefaultRequestHeaders.Authorization = `
    New-Object System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", $token)
$content = New-Object System.Net.Http.ByteArrayContent(
    , [System.IO.File]::ReadAllBytes("screenshot.png")
)
$content.Headers.ContentType = `
    [System.Net.Http.Headers.MediaTypeHeaderValue]::new("application/octet-stream")
$resp = $client.PostAsync($url, $content).Result
```

Reference the attachment in the PR description:

```markdown
![description](https://{org}.visualstudio.com/{projectId}/_apis/git/repositories/{repoId}/pullRequests/{prId}/attachments/screenshot.png)
```

Azure DevOps gotchas:

| Gotcha | Correct action |
| --- | --- |
| Markdown renderer is faster with `{org}.visualstudio.com` | Use `.visualstudio.com`, not `dev.azure.com/{org}`. |
| Attachment upload method | Use `POST`; `PUT` returns 405. |
| API version | Use `7.1-preview.1`. |
| Filename reuse | Use a new filename such as `screenshot-v2.png`; re-uploading the same name fails. |
| Binary upload | Use `HttpClient`; `Invoke-RestMethod` can corrupt binary data. |
| PR description paths | Use full URLs; repo-relative paths do not render as PR attachments. |
| Branch clutter | Do not commit images to the feature branch just for PR screenshots. |

### GitHub

GitHub does not provide a clean public API for uploading images directly into pull request descriptions. Prefer the active GitHub attachment workflow available in the host environment when present. If no uploader exists, use a documented workaround such as a `pr-assets` orphan branch and reference `github.com/{owner}/{repo}/blob/pr-assets/{file}?raw=true`, but call out that it is clunky and should not be the default when a first-class uploader is available.

## Platform wording

Use `Before/after` language when summarizing comparisons and preserve `BEFORE` state capture as a named risk because missing the initial image is error-prone. For Azure DevOps, mention the slower `dev.azure.com` rendering form only to reject it in favor of `.visualstudio.com`. For GitHub, mention the former drag-and-drop limitation when explaining why an attachment uploader or `pr-assets` workaround may be needed. Use `image-annotations` as the related skill name for subtle callouts, and call out when a same-name re-upload would fail.

## Output template

```markdown
## PR screenshot block

**Status:** ready | blocked
**PR:** <PR number or URL>
**Visual changes covered:** <count>

### Markdown to paste
<before/after markdown block with image URLs>

### Evidence notes
| Change | Before image | After image | Viewport/crop match | Notes |
| --- | --- | --- | --- | --- |
| `<area>` | `<url>` | `<url>` | `yes/no` | `<what reviewers should notice>` |

### Upload details
- Platform: GitHub | Azure DevOps | other
- Upload method: <attachment API, host uploader, or documented workaround>
- Files: <image filenames>
```

## Quality gate

- [ ] Every visible change that needs review has a before/after pair or a justified single screenshot.
- [ ] Before and after images use the same viewport width, crop, and relevant data state.
- [ ] Images are visible in the PR body, not hidden behind `<details>` by default.
- [ ] Captions are brief and point reviewers to the important difference.
- [ ] Azure DevOps uploads use `.visualstudio.com`, `POST`, `7.1-preview.1`, unique filenames, and `HttpClient`.
- [ ] GitHub images use an available attachment workflow or a clearly documented workaround.
- [ ] No screenshots are committed to the feature branch solely for PR display.
