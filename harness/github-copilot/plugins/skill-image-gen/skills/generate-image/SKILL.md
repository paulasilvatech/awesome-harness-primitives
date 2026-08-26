---
name: generate-image
description: >-
  Generate AI images and visual assets through OpenAI gpt-image-2 or Google Gemini image models. Use when the user asks to generate, create, or make images, textures, icons, sprites, artwork, mockups, product visuals, or batch image assets from a text description.
argument-hint: "[description of the image to generate]"
license: "MIT"
metadata:
  providers: "openai, gemini"
  version: "2.1.0"
---

# Generate image

Generate an image from a user prompt, choose an available provider from environment keys, call the provider API safely, decode the returned image, save it in a sensible project location, and report the output path.

## When to invoke

- "Generate an image of this concept."
- "Create a tileable game texture."
- "Make an icon or sprite for this app."
- "Use OpenAI gpt-image-2 for a polished mockup."
- "Use Gemini Nano Banana for quick visual iterations."

## Inputs

Use `$ARGUMENTS` as the image prompt. Preserve the user's subject, style, dimensions, file format, and output path when specified. If `$ARGUMENTS` is empty, use the most recent user request as the prompt; if no prompt exists, return `blocked` with the missing input instead of inventing an image.

## Prerequisites and context

- `SKILL_IMAGE_GEN_OPENAI_KEY` enables OpenAI image generation.
- `SKILL_IMAGE_GEN_GEMINI_KEY` enables Google Gemini image generation.
- Never print, commit, or persist API keys unless the user explicitly asks to configure the current shell profile.
- Save outputs under a relevant repository directory such as `assets/`, `images/`, `public/`, or the current directory.
- Create the output directory before writing the decoded image.

## Provider selection

| Environment | Provider choice | Rationale |
| --- | --- | --- |
| Only `SKILL_IMAGE_GEN_OPENAI_KEY` is set | OpenAI | Use the available key without asking. |
| Only `SKILL_IMAGE_GEN_GEMINI_KEY` is set | Gemini | Use the available key without asking. |
| Both keys are set and user names one | User's provider | Explicit request wins. |
| Both keys are set and no preference | OpenAI for polish or text rendering; Gemini for speed and iteration | Choose based on prompt context. |
| No keys are set | Onboarding | Explain both providers and ask for configuration in interactive environments; otherwise report blocked. |

## Onboarding

Only run onboarding when neither key is set. Explain the provider choices without generating anything:

| Provider | Model | Best for | Key URL |
| --- | --- | --- | --- |
| OpenAI | `gpt-image-2` | High quality, polished visuals, stronger text rendering, paid image generation. | https://platform.openai.com/api-keys |
| Google Gemini | Nano Banana / Gemini image models | Fast iteration, free tier availability, visual drafts and variations. | https://aistudio.google.com/apikey |

If the user provides a key in the same session, set only the corresponding process environment variable (`SKILL_IMAGE_GEN_OPENAI_KEY` or `SKILL_IMAGE_GEN_GEMINI_KEY`) for the current run. Persist to a shell profile only when explicitly requested.

## OpenAI API contract

| Field | Value |
| --- | --- |
| Method | `POST` |
| URL | `https://api.openai.com/v1/images/generations` |
| Headers | `Authorization: Bearer <SKILL_IMAGE_GEN_OPENAI_KEY>`, `Content-Type: application/json` |
| Default model | `gpt-image-2` |
| Alternative model | `gpt-image-1` |
| Default size | `1024x1024` |
| Size options | `1024x1024`, `1024x1536`, `1536x1024`, `auto` |
| Default quality | `medium` |
| Quality options | `low`, `medium`, `high` |

```json
{
  "model": "gpt-image-2",
  "prompt": "<user prompt>",
  "n": 1,
  "size": "1024x1024",
  "quality": "medium"
}
```

Decode `data[0].b64_json` when present. If `data[0].url` is returned instead, download that URL and save the image. Escape special characters in the prompt before placing it in JSON.

## Google Gemini API contract

| Field | Value |
| --- | --- |
| Method | `POST` |
| URL shape | `https://ai.google.dev/gemini-api/docs/models<model>:generateContent` |
| Headers | `x-goog-api-key: <SKILL_IMAGE_GEN_GEMINI_KEY>`, `Content-Type: application/json` |
| Default model | `gemini-2.0-flash-exp` |
| Alternative model | `gemini-2.5-flash-image` |
| Response image | `candidates[0].content.parts[]` item with `inlineData.data` and `inlineData.mimeType` |

```json
{
  "contents": [{"parts": [{"text": "Generate an image: <user prompt>"}]}],
  "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}
```

Handle API errors in `error`, safety blocks in `promptFeedback.blockReason`, and filtered completions with `finishReason: "SAFETY"`.

## Prompt enrichment

| User asks for | Add prompt constraints |
| --- | --- |
| Game texture | `seamless`, `tileable`, `game asset`, material detail, no perspective seams. |
| Icon | Simple silhouette, centered composition, transparent or plain background when supported. |
| Sprite | Consistent camera angle, clean outline, limited palette, animation frame constraints if needed. |
| Mockup | Product context, UI/device frame, readable text only when needed. |
| Batch generation | Keep a shared style seed in prose and vary only the requested subject. |

For batch generation, make independent API calls in parallel when tooling allows it, but write each output to a distinct path.

## Procedure

1. Read `$ARGUMENTS` and determine prompt, provider preference, output directory, file name, and batch count.
2. Check `SKILL_IMAGE_GEN_OPENAI_KEY` and `SKILL_IMAGE_GEN_GEMINI_KEY`.
3. Select the provider using the provider table; run onboarding or return blocked when no key is available.
4. Enrich the prompt only with constraints that match the user's requested asset type.
5. Send the provider request with escaped JSON and without logging secrets.
6. Decode `b64_json` or `inlineData.data`, or download `data[0].url` when OpenAI returns a URL.
7. Save the image, create parent directories first, and verify the file exists and has a nonzero size.
8. Report the saved path, provider, model, and any safety or API warnings.

## Gotchas

- **Do not leak keys**: redact `Authorization` and `x-goog-api-key` values in logs and responses.
- **Do not resize user-requested textures after generation**: post-generation resizing can break seamless tiling or pixel art sharpness.
- **Do not assume text will be perfect**: prefer OpenAI for text-heavy images and keep text short.
- **Do not overwrite existing assets silently**: choose a unique file name unless the user asked to replace a specific file.

## Key handling note

Check whether `SKILL_IMAGE_GEN_OPENAI_KEY` and/or `SKILL_IMAGE_GEN_GEMINI_KEY` are available before choosing a provider.

## Output template

```markdown
## Image generation result

**Status:** complete | blocked | failed
**Provider:** OpenAI | Gemini | none
**Model:** `<model>`
**Prompt:** `<final prompt summary>`
**Output:** `<path/to/image>`

### Files
- `<path/to/image>`: <format>, <size if known>, <nonzero bytes verified>

### Validation
- API response decoded: pass | fail
- Output directory created: pass | fail
- Image file exists and is nonzero: pass | fail
```

## Quality gate

- [ ] `$ARGUMENTS` or conversation context supplied a concrete image prompt.
- [ ] Provider selection followed the available environment keys and user preference.
- [ ] `SKILL_IMAGE_GEN_OPENAI_KEY` and `SKILL_IMAGE_GEN_GEMINI_KEY` were never printed or committed.
- [ ] The request used the correct provider URL, headers, model, size, and quality or modality fields.
- [ ] The response was decoded from `data[0].b64_json`, `data[0].url`, or `inlineData.data` as appropriate.
- [ ] The output directory exists and the saved image is nonzero bytes.
- [ ] Safety blocks, API errors, or missing keys are reported as blocked or failed with actionable detail.

## References

- [OpenAI API keys](https://platform.openai.com/api-keys)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)
