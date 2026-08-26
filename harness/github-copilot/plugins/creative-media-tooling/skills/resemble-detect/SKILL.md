---
name: resemble-detect
description: >-
  Detect synthetic or manipulated audio, image, video, and text with Resemble AI; trace audio synthesis sources; apply or detect watermarks; verify speaker identity; and inspect media intelligence. Use this skill when checking deepfakes, fake detection, synthetic media, authenticity, provenance, AI-written text, voice verification, watermarking, source tracing, or whether media is real or fake.
license: Apache-2.0
metadata:
  compatibility: Requires a Resemble AI API key from https://app.resemble.ai set as RESEMBLE_API_KEY. All media must be accessible through public HTTPS URLs except text detection.
---

# Resemble Detect media safety

Use Resemble AI to submit media or text for a completed detection job, interpret returned labels and scores, and produce a careful authenticity report that never claims real or fake without API evidence.

## When to invoke

- "Check whether this audio, video, image, or text is AI-generated."
- "Detect a deepfake or manipulated media file."
- "Verify media authenticity, provenance, watermark, or source tracing."
- "Identify the speaker or compare a voice against known profiles."
- "Ask questions about completed Resemble detection results."

## Prerequisites and context

- API key from https://app.resemble.ai set as `RESEMBLE_API_KEY`.
- Base docs URL: <https://docs.resemble.ai/welcome>.
- Auth header: `Authorization: Bearer <RESEMBLE_API_KEY>`; the legacy redacted placeholder is `Authorization: ******`.
- Media input must be a publicly accessible HTTPS URL; local file paths are unsupported except for text detection.
- `POST /text_detect` accepts inline text content.
- Do not use this skill for text-to-speech generation, voice cloning, or speech-to-text transcription.

## Core rule and capability map

Never declare media real or fake without a completed detection result. Every authenticity claim must be backed by a Resemble detect job with a returned `label`, `score` or `aggregated_score`, and `status: "completed"`. If the job is `processing`, wait. If it `failed`, report failure instead of substituting judgment.

| User wants to | Use this | API endpoint |
| --- | --- | --- |
| Check if media is AI-generated or deepfake | Deepfake Detection | `POST /detect` |
| Know which AI platform made fake audio | Audio Source Tracing | `POST /detect` with `audio_source_tracing: true` |
| Get speaker info, emotion, transcription, translation, abnormalities, or misinformation | Intelligence | `POST /intelligence` or `POST /detect` with `intelligence: true` |
| Ask questions about a completed detection | Detect Intelligence | `POST /detects/{uuid}/intelligence` |
| Apply an invisible watermark | Watermark Apply | `POST /watermark/apply` |
| Check if media contains a watermark | Watermark Detect | `POST /watermark/detect` |
| Verify a speaker against known profiles | Identity Search | `POST /identity/search` |
| Check if text is AI-generated | Text Detection | `POST /text_detect` |
| Create a voice identity profile | Identity Create | `POST /identity` |

When multiple capabilities apply, combine them in one `POST /detect` call with flags such as `intelligence: true`, `audio_source_tracing: true`, `visualize: true`, and `use_reverse_search: true` instead of making unnecessary separate requests.

## MCP tools and API reference

When the Resemble MCP server is connected, use these tools instead of raw API calls:

| Tool | Purpose |
| --- | --- |
| `resemble_docs_lookup` | Get comprehensive docs for any detect sub-topic. |
| `resemble_search` | Search across all documentation. |
| `resemble_api_endpoint` | Get exact OpenAPI spec for any endpoint. |
| `resemble_api_search` | Find endpoints by keyword. |
| `resemble_get_page` | Read specific documentation pages. |
| `resemble_list_topics` | List all available topics. |

Use `resemble_docs_lookup` with topic `"detect"`, then `resemble_api_endpoint` for exact request and response schemas before making calls. Full request/response schemas are bundled in `references/api-reference.md`; consult it before any API call, especially the sections for reading results by media type, intelligence, watermarking, identity speaker verification beta, and text detection.

## Detection workflows

### Full media forensics

1. Submit detection with relevant flags:

```json
{
  "url": "https://example.com/suspect.mp4",
  "visualize": true,
  "intelligence": true,
  "audio_source_tracing": true,
  "use_reverse_search": true
}
```

2. Poll `GET /detect/{uuid}` at 2s → 5s → 10s intervals until `status` is `"completed"` or `"failed"`; most jobs complete in 10–60 seconds.
3. Read `metrics`, `image_metrics`, or `video_metrics` for the verdict.
4. Read `intelligence.description` and structured fields.
5. If audio is labeled `"fake"`, check `audio_source_tracing.label`.
6. Ask follow-up questions through Detect Intelligence if clarification is needed.
7. Check watermark provenance with `POST /watermark/detect` when relevant.

### Quick authenticity check

1. Submit minimal detection: `{ "url": "..." }`.
2. Poll until complete.
3. Check `label` and `aggregated_score` for audio, or `label` and `score` for image/video.
4. Report the result with score context and limitations.

### Provenance pipeline

1. Apply watermark to original content with `POST /watermark/apply`.
2. Distribute the `watermarked_media` URL.
3. Later verify provenance with `POST /watermark/detect`.

Supported formats: WAV, MP3, OGG, M4A, FLAC, MP4, MOV, AVI, WMV, JPG, PNG, GIF, and WEBP.

## Reading results and scores

| Media type | Result fields | Notes |
| --- | --- | --- |
| Audio | `metrics.label`, `metrics.aggregated_score` | Use for the main verdict. |
| Image | `image_metrics.label`, `image_metrics.score`, `ifl` | `ifl` is the Invisible Frequency Layer heatmap. |
| Video | `video_metrics` plus optional `metrics` | Video-with-audio returns both audio and frame/segment results. |
| Intelligence | `speaker_info`, `language`, `dialect`, `emotion`, `speaking_style`, `context`, `message`, `abnormalities`, `transcription`, `translation`, `misinformation` | Audio/video structured fields. |
| Image intelligence | `scene_description`, `subjects`, `authenticity_analysis`, `context_and_setting`, `abnormalities`, `misinformation` | Image structured fields. |

| Score range | Interpretation |
| --- | --- |
| 0.0–0.3 | Strong indication of authentic or real media. |
| 0.3–0.5 | Inconclusive; recommend additional analysis. |
| 0.5–0.7 | Likely synthetic; flag for review. |
| 0.7–1.0 | High confidence synthetic or AI-generated. |

Always say, for example, "The detection returned a score of 0.87, indicating high confidence that this audio is AI-generated." Never report only "it's fake." Detection results are analytical tools, not forensic certifications or legal evidence.

## Feature rules

| Feature | Required details |
| --- | --- |
| Detect Intelligence | Submit `POST /detects/{detect_uuid}/intelligence` only after detection reaches `status: "completed"`; poll `GET /detects/{detect_uuid}/intelligence/{question_uuid}`. A processing or failed detection returns 422. |
| Audio Source Tracing | Set `audio_source_tracing: true`; result appears under `audio_source_tracing.label`; source tracing only runs on audio labeled `"fake"`. Known labels include `resemble_ai`, `elevenlabs`, and `real`. Standalone queries use `GET /audio_source_tracings` and `GET /audio_source_tracings/{uuid}`. |
| Watermark Apply | `POST /watermark/apply` with `url`, optional `strength` from 0.0–1.0, optional `custom_message`; add `Prefer: wait` or poll `GET /watermark/apply/{uuid}/result`. |
| Watermark Detect | `POST /watermark/detect` with `url`; audio returns `has_watermark` and `confidence`; image/video returns `has_watermark`. |
| Identity | Beta; `POST /identity` with `audio_url` and `name`; `POST /identity/search` with `audio_url` and `top_k`; matches include `confidence` and `distance`. |
| Text Detection | Beta; requires `detect_beta_user` role or billing plan with `dfd_text`; `text` is required and max 100,000 chars; use `threshold`, `privacy_mode: true`, `callback_url`, `Prefer: wait`, or poll `GET /text_detect/{uuid}`; result includes `prediction` (`"ai"` or `"human"`) and `confidence`. |

Good Detect Intelligence questions include: "Summarize the detection results in plain language", "What specific indicators suggest this is AI-generated?", "How do the audio and video detection results differ?", "What is the confidence level and what does it mean?", and "Are there any inconsistencies in the analysis?"

## Privacy, gotchas, and errors

- **Use `zero_retention_mode: true` for sensitive media**: media is auto-deleted after analysis; the URL is redacted and `media_deleted` becomes true post-completion.
- **Use `privacy_mode: true` for text detection**: text content is not stored after analysis.
- **Callback security matters**: if using `callback_url`, require HTTPS and authentication on the receiving endpoint.
- **Do not submit local file paths**: the API requires public HTTPS URLs for media.
- **Do not send text longer than 100,000 characters**: split into chunks or report the limit.
- **Do not poll faster than 1s**: start at 2s and back off exponentially.
- **Do not expect source tracing on real audio**: it only runs for audio labeled `"fake"`.
- **Warn on beta access errors**: Identity and Text Detection are beta features.

| Error | Cause | Resolution |
| --- | --- | --- |
| 400 | Invalid request body or missing `url` | Check required parameters. |
| 401 | Invalid or missing API key | Verify `RESEMBLE_API_KEY`. |
| 404 | Detection UUID not found | Verify the UUID from the creation response. |
| 422 | Detection not completed for Intelligence | Wait for detection to reach `completed` status. |
| 429 | Rate limited | Back off and retry with exponential delay. |
| 500 | Server error | Retry once, then report to the user. |

## Progressive disclosure and bundled resources

- `references/api-reference.md`: exact endpoint schemas and response shapes for detection, intelligence, source tracing, watermarking, identity, and text detection.


## Resemble vocabulary and preserved examples

The iron law is literal: `NEVER DECLARE MEDIA AS REAL OR FAKE WITHOUT A COMPLETED DETECTION RESULT.` Preserve the terms `IRON`, `LAW`, `NEVER`, `DECLARE`, `MEDIA`, `REAL`, `FAKE`, `WITHOUT`, `COMPLETED`, `DETECTION`, and `RESULT` when summarizing policy. Use `Authorization: ******` only as a redacted placeholder; never expose a real key. Relevant detection wording includes `authentic/real`, `synthetic/AI-generated`, `human-written`, `machine-written`, `natural-language`, `visual/auditory`, `heatmap/visualization`, `video-with-audio`, `round-trip`, `auto-delete`, `GDPR`, `compliance-sensitive`, `GDPR/compliance-sensitive`, `production-ready`, and `decision-making`. Reference anchors from `references/api-reference.md` include `reading-results-by-media-type`, `identity--speaker-verification-beta`, and `text-detection`. Preserved payload examples include `{ "query": "..." }`, `{ audio_url, name }`, `{ audio_url, top_k }`, `{ has_watermark, confidence }`, and `{ has_watermark }`. The docs URL is `https://docs.resemble.ai/welcome`.

## Output template

```markdown
### Resemble Detect result

**Status:** completed | processing | failed | blocked
**Input:** <public HTTPS URL or text summary>
**Capability:** deepfake detection | intelligence | watermark | identity | text detection | source tracing
**Job ID:** `<uuid or none>`

**Verdict**
- Label / prediction: `<label>`
- Score / confidence: `<number>`
- Interpretation: <score range context and limitation>

**Evidence**
| Field | Value |
| --- | --- |
| `status` | `<completed/failed>` |
| `metrics` / `image_metrics` / `video_metrics` | `<summary>` |
| `audio_source_tracing.label` | `<value or not applicable>` |
| `intelligence` | `<summary or not requested>` |
| `watermark` | `<has_watermark/confidence or not requested>` |

**Next steps**
- <follow-up intelligence question, watermark check, source tracing, manual review, or limitation>
```

## Quality gate

- [ ] No authenticity claim is made without `status: "completed"` and returned label plus score or confidence.
- [ ] Media inputs are public HTTPS URLs unless the task uses `POST /text_detect` with inline text.
- [ ] The correct endpoint and flags are selected from the capability map.
- [ ] Polling uses backoff and stops at `completed` or `failed`.
- [ ] Results include score context and limitations, not only a label.
- [ ] Sensitive media uses or recommends `zero_retention_mode: true`; sensitive text uses or recommends `privacy_mode: true`.
- [ ] Beta features are identified when Identity or Text Detection is used.
- [ ] `references/api-reference.md` is consulted before API calls that need exact schema details.

## References

- [Resemble AI dashboard](https://app.resemble.ai)
- [Resemble documentation](https://docs.resemble.ai/welcome)
