---
name: nano-banana-pro-openrouter
description: >-
  Generate or edit images through OpenRouter with the `google/gemini-3-pro-image-preview` model.
  Use when prompt-only image generation, single-image edits, multi-image compositing, 1K/2K/4K
  output, or troubleshooting `OPENROUTER_API_KEY`, `uv`, and saved MEDIA files is requested.
metadata:
  primaryEnv: OPENROUTER_API_KEY
  requires: "{\"bins\": [\"uv\"], \"env\": [\"OPENROUTER_API_KEY\"]}"
---

<!-- Generated from harness/github-copilot/plugins/creative-media-tooling/skills/nano-banana-pro-openrouter/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Nano Banana Pro OpenRouter

Generate images, edit one source image, or compose up to three source images by running the bundled script against OpenRouter. Return saved image paths as media artifacts, not inline image contents.

## When to invoke

- "Generate an image with Nano Banana Pro."
- "Use OpenRouter to edit this image."
- "Composite these images into one output."
- "Create a 4K image from this prompt."
- "Fix `OPENROUTER_API_KEY` or `uv` errors from the image script."

## Prerequisites and context

| Requirement | Check | Fix if missing |
| --- | --- | --- |
| OpenRouter key | `OPENROUTER_API_KEY` is set in the environment. | Ask the user to set it; never invent or log a key. |
| Runner | `uv` is available. | Install with the documented macOS/Linux or Windows command below. |
| Script | `scripts/generate_image.py` exists in this skill package. | Do not replace it with ad hoc API calls. |
| Optional system prompt | `assets/SYSTEM_TEMPLATE` may exist and customize generation behavior. | Read it only when prompt behavior needs inspection or modification. |

## Image generation commands

Use `{baseDir}` as the absolute path to this skill directory when running the script.

| Task | Command |
| --- | --- |
| Prompt-only generation | `uv run {baseDir}/scripts/generate_image.py --prompt "A cinematic sunset over snow-capped mountains" --filename sunset.png` |
| Edit a single image | `uv run {baseDir}/scripts/generate_image.py --prompt "Replace the sky with a dramatic aurora" --input-image input.jpg --filename aurora.png` |
| Compose multiple images | `uv run {baseDir}/scripts/generate_image.py --prompt "Combine the subjects into a single studio portrait" --input-image face1.jpg --input-image face2.jpg --filename composite.png` |
| Set resolution | Add `--resolution 1K`, `--resolution 2K`, or `--resolution 4K`; default is `1K`. |

The `--resolution` flag accepts only the supported values listed above.

## Behavior and constraints

- Use model `google/gemini-3-pro-image-preview` through OpenRouter.
- Accept up to 3 input images by repeating `--input-image`.
- `--filename` may be relative, saving to the current directory, or absolute.
- If multiple images are returned, append `-1`, `-2`, and so on to the requested filename.
- Print one `MEDIA: <path>` line for each saved image.
- Do not read generated image bytes back into the response; report paths only.
- Retry transient HTTP 429 or network timeouts once after 30 seconds. Do not retry the same error more than twice.
- If the script exits non-zero, inspect stderr and map it to the troubleshooting table before retrying.

## Progressive disclosure and bundled resources

- `scripts/generate_image.py`: run this for every generation, edit, or composition request.
- `assets/SYSTEM_TEMPLATE`: optional system prompt customization loaded by the script; inspect only when prompt behavior must be explained or changed.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `OPENROUTER_API_KEY is not set` | Missing environment variable. | bash: `export OPENROUTER_API_KEY="sk-or-..."`; PowerShell: `$env:OPENROUTER_API_KEY = "sk-or-..."`. |
| `uv: command not found` or not recognized | `uv` is not installed or the terminal has not reloaded PATH. | macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`. Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`. Restart the terminal. |
| `AuthenticationError` or HTTP 401 | Key is invalid, revoked, or has no credits. | Verify the key at `https://openrouter.ai/settings/keys`. |
| HTTP 429 or timeout | Rate limit or transient network failure. | Retry once after 30 seconds, then surface the error. |

## Output template

```markdown
## Nano Banana Pro image result

**Status:** complete | blocked
**Model:** `google/gemini-3-pro-image-preview`
**Prompt:** <prompt used>
**Resolution:** `1K` | `2K` | `4K`

### Media
- `MEDIA: <saved-path>`

### Notes
- <input images used, retries, or blocker>
```

## Quality gate

- [ ] `OPENROUTER_API_KEY` is required but never printed or stored.
- [ ] The bundled `scripts/generate_image.py` command is used instead of hand-written OpenRouter calls.
- [ ] No more than 3 `--input-image` values are passed.
- [ ] Resolution is one of `1K`, `2K`, or `4K`, defaulting to `1K` when omitted.
- [ ] Every saved image is reported as `MEDIA: <path>` and image bytes are not pasted into the response.
- [ ] Transient retries follow the once-after-30-seconds rule and repeated failures are surfaced.

## References

- [uv installer for macOS/Linux](https://astral.sh/uv/install.sh)
- [uv installer for Windows](https://astral.sh/uv/install.ps1)
- [OpenRouter keys](https://openrouter.ai/settings/keys)
