---
name: latchshot-page-capture
description: >-
  Capture public HTTP(S) webpages as local PNG, JPEG, or PDF artifacts through Latchshot. Use when
  the user needs screenshots, website thumbnails, full-page captures, PDFs, QA reports, archives,
  or social previews. Do not use for private or authenticated pages, raw HTML extraction,
  scraping, CAPTCHA bypass, arbitrary browser actions, or local-file capture.
---

<!-- Generated from harness/github-copilot/skills/latchshot-page-capture/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Latchshot page capture

Use the bundled dependency-free Node.js client to turn one public webpage URL into a validated local PNG, JPEG, or PDF artifact while keeping the LATCHSHOT_API_KEY out of chat, source, command arguments, and output.

## When to invoke

- "Capture a screenshot of this public webpage."
- "Save a full-page PNG for this URL."
- "Create a PDF of a public website."
- "Generate a website thumbnail artifact."
- "Check my remaining Latchshot render quota."

## Prerequisites and context

Require Node.js 20 or newer and network access. Authenticated capture and usage commands read the API key only from `LATCHSHOT_API_KEY` and send it only to the fixed `https://latchshot.fly.dev` origin. Never ask the user to paste the key into chat, a command argument, source code, a committed file, or output. Never print or return the key.

Latchshot is a hosted third-party service maintained by this skill's contributor. Keep its use optional and preserve local-browser workflows when the task needs private pages, authenticated pages, or unsupported browser actions.

## Request boundaries

| Request | Handle with Latchshot? | Rule |
| --- | --- | --- |
| Public `http://` or `https://` page screenshot | Yes | Capture one binary artifact. |
| PNG, JPEG, or PDF output | Yes | Infer from `.png`, `.jpg`, `.jpeg`, or `.pdf`, or pass `--format`. |
| Private page, intranet, login, cookie, CAPTCHA, signed URL, query secret, or non-web port | No | Reject instead of bypassing. |
| Raw HTML, DOM extraction, selectors, sessions, arbitrary JavaScript, clicking, typing, scraping, or anti-bot evasion | No | Latchshot is capture-only. |
| Local file capture | No | It accepts public webpage URLs only. |

This includes social-preview captures, but not authenticated/private, private/internal, or private-page access.

Use `--allow-query` only after confirming the query contains no credential, signature, token, customer data, or other secret.

## No-key demo

If `LATCHSHOT_API_KEY` is missing, use the no-key demo only when a bounded public viewport JPEG fits the request.

```bash
node scripts/latchshot.mjs demo \
  --url 'https://example.com' \
  --output './artifacts/example-demo.jpg'
```

The demo is JPEG-only, does not use an account or render quota, allows three attempts per IP address per hour, and accepts only width, height, query confirmation, and explicit overwrite options. The public URL is still sent to Latchshot with the coarse `agentskill` acquisition label. Treat the result as a proof artifact, not as customer activation or plan signup. For PNG, PDF, full-page, cleanup, or repeat work without a key, direct the user to https://latchshot.fly.dev/integrations.md#agent-skills and stop.

## Capture workflow

1. Confirm the target is a public HTTP or HTTPS page and the output path is user-approved.
2. Run the client from this skill directory.
3. Parse the one-line JSON result and confirm `ok`, `output`, `format`, `contentType`, and `bytes`.
4. Inspect the local artifact when the surrounding task requires visual or document verification.
5. Report the path and render or quota diagnostics without exposing the key.

Viewport capture:

```bash
node scripts/latchshot.mjs capture \
  --url 'https://example.com' \
  --output './artifacts/example.png'
```

Full-page capture with lazy content activation:

```bash
node scripts/latchshot.mjs capture \
  --url 'https://example.com' \
  --output './artifacts/example-full.png' \
  --full-page \
  --scroll-page
```

PDF capture:

```bash
node scripts/latchshot.mjs capture \
  --url 'https://example.com' \
  --output './artifacts/example.pdf' \
  --paper A4
```

Best-effort cleanup flags are not bypass tools; treat each cleanup as best-effort only: `--block-ads`, `--block-trackers`, `--block-chats`, `--hide-cookie-banners`, and `--hide-popups`. The client refuses to overwrite a file unless `--force` is explicit. Report render/quota diagnostics only. Run `node scripts/latchshot.mjs --help` for the exact bounded options.

## Usage and failure handling

Read quota without consuming render quota:

```bash
node scripts/latchshot.mjs usage
```

| Symptom or code | Response |
| --- | --- |
| Validation or authentication failure | Read the structured stderr code and message; do not retry. |
| `demo_limit` | Wait for the hourly reset; do not loop or switch identities. |
| `rate_limited` | Wait for the reported reset or retry-after boundary. |
| Render failure | State the failure, preserve any existing output file, and do not substitute another provider silently. |
| Commercial action requested | Keep upgrade, checkout, payment, implementation request, and plan changes user- and owner-controlled. |

The usage command is read-only.

## Progressive disclosure and bundled resources

| Resource | Use it when |
| --- | --- |
| `scripts/latchshot.mjs` | Running `demo`, `capture`, `usage`, or `--help` commands. |

## Output template

```markdown
## Latchshot capture result

**Status:** captured | demo-captured | blocked
**URL:** `<public URL>`
**Output:** `<local artifact path>`
**Format:** png | jpeg | pdf

### Render result
- `ok`: <true/false>
- `contentType`: <content type>
- `bytes`: <byte count>
- Diagnostics: <quota/reset/render notes with no API key>

### Boundaries checked
- Public HTTP(S): yes | no
- Query reviewed for secrets: yes | not applicable
- Auth/private/CAPTCHA/browser-action request: no | blocked because <reason>
```

## Quality gate

- [ ] The URL is a public HTTP or HTTPS page and is not private, authenticated, signed, or secret-bearing.
- [ ] The command reads authenticated credentials only from `LATCHSHOT_API_KEY`.
- [ ] The output path is explicit, local, and not overwritten unless `--force` was intentional.
- [ ] The JSON result was parsed for `ok`, `output`, `format`, `contentType`, and `bytes`.
- [ ] Rate limits and demo limits were not bypassed by looping or identity switching.
- [ ] No raw HTML extraction, scraping, CAPTCHA bypass, arbitrary browser action, or commercial action was attempted.

## References

- [Latchshot service origin](https://latchshot.fly.dev)
- [Agent Skills setup documentation](https://latchshot.fly.dev/integrations.md#agent-skills)
