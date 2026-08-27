---
name: napkin
description: >-
  Open and read a browser-based visual whiteboard for GitHub Copilot CLI collaboration. Use when
  the user says "let's napkin", "open a napkin", "start a whiteboard", "check the napkin", "look
  at the napkin", or asks GitHub Copilot to interpret sketches, sticky notes, diagrams, and shared
  napkin snapshots.
---

<!-- Generated from harness/github-copilot/plugins/napkin/skills/napkin/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Napkin visual whiteboard

Open an HTML browser whiteboard, guide the user to sketch or add sticky notes, then read the exported PNG snapshot and optional clipboard JSON so GitHub Copilot can respond as a plain-language collaborator.

## When to invoke

- "Let's napkin."
- "Open a napkin."
- "Start a whiteboard."
- "Check the napkin."
- "Look at my napkin and tell me what you think."

## Prerequisites and context

- The bundled HTML template is `assets/napkin.html` relative to this `SKILL.md` file.
- Runtime documentation images are `assets/step1-activate.svg`, `assets/step2-whiteboard.svg`, `assets/step3-draw.svg`, `assets/step4-share.svg`, and `assets/step5-response.svg`; they are illustrations, not inputs.
- The intended audience is lawyers, PMs, and business stakeholders. Keep language approachable, jargon-free, and non-technical.

## Procedure

1. For activation requests, copy `assets/napkin.html` to `~/Desktop/napkin.html`. If it already exists, ask whether to open the existing napkin or start fresh before overwriting.
2. Open the file in the default browser: macOS `open ~/Desktop/napkin.html`, Linux `xdg-open ~/Desktop/napkin.html`, Windows `start ~/Desktop/napkin.html`.
3. Tell the user:

```text
Your napkin is open in your browser!

Draw, sketch, or add sticky notes — whatever helps you think through your idea.

When you're ready for my input, click the green "Share with Copilot" button on the whiteboard, then come back here and say "check the napkin."
```

4. For reading requests, look for `napkin-snapshot.png` in order: `~/Downloads/napkin-snapshot.png`, then `~/Desktop/napkin-snapshot.png`.
5. Use the `view` tool on the PNG. The PNG is the primary channel because it captures freehand sketches, arrows, layout, annotations, circled items, crossed-out items, and canvas emphasis.
6. Try to read supplementary clipboard JSON: macOS `pbpaste`, Linux `xclip -selection clipboard -o`, Windows `powershell -command "Get-Clipboard"`. Missing JSON is not an error.
7. Synthesize visual content and JSON text into a conversational interpretation. End by offering a next step.

## Interpretation rules

| Source | Use it for | Rule |
| --- | --- | --- |
| PNG snapshot | Sketches, diagrams, flowcharts, groupings, arrows, layout, annotations, circled/crossed-out items. | Treat as primary. Do not skip it silently. |
| Clipboard JSON | Exact sticky note text, labels, positions, and colors. | Treat as supplementary. Continue without it if absent. |
| User prompt | Desired next step or question. | Answer the user's intent, not just the canvas contents. |

Response style examples:

- "I can see you've sketched out a three-stage process — it looks like you're thinking about X flowing into Y and then Z."
- "It looks like you've grouped these four ideas on the left and separated them from two items on the right. Are those different categories?"
- "I see arrows connecting A to B to C. Is this the workflow you're envisioning?"

## Responding back to the napkin

The agent cannot directly modify the browser canvas state because JavaScript owns it. Offer practical alternatives:

- Provide the response in the CLI and suggest the user add it manually.
- Create a separate markdown memo, checklist, or structured document from the napkin.
- When useful, create an updated copy of `napkin.html` with pre-loaded content.

## Tone and style

- Use an approachable, non-technical tone.
- Never use developer jargon without explaining it plainly.
- Treat the napkin as a creative collaborative space, not a formal input mechanism.
- Be encouraging about sketches regardless of artistic quality.
- Frame responses as building on the user's thinking, not grading or analyzing it.
- If the noob-mode skill is active, use its green/yellow/red risk indicator format when requesting file or bash permissions.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `napkin-snapshot.png` is missing | User has not clicked Share with Copilot or browser saved elsewhere. | Tell the user to open the whiteboard, click the green Share with Copilot button, return, and say "check the napkin" again. |
| `~/Desktop/napkin.html` is missing | No napkin has been started. | Say "It looks like we haven't started a napkin yet. Want me to open one for you?" |
| Clipboard lacks JSON | Browser or OS did not copy structured data. | Continue with PNG-only interpretation. |

## Progressive disclosure and bundled resources

- `assets/napkin.html`: browser HTML whiteboard template copied to the user's Desktop.
- `assets/step1-activate.svg`, `assets/step2-whiteboard.svg`, `assets/step3-draw.svg`, `assets/step4-share.svg`, `assets/step5-response.svg`: documentation illustrations only.

## Output template

```markdown
## Napkin result

**Status:** opened | interpreted | needs snapshot | blocked
**Napkin file:** `~/Desktop/napkin.html`
**Snapshot checked:** `<path or not found>`

### What I see
<plain-language interpretation of drawings, sticky notes, arrows, layout, and emphasis>

### Exact text captured
<clipboard JSON text summarized, or "No structured JSON found">

### Suggested next step
<offer to build on it, turn it into a document, or add suggestions>
```

## Quality gate

- [ ] Activation copies `assets/napkin.html` without overwriting an existing Desktop file without user choice.
- [ ] Browser open command matches the operating system.
- [ ] Reading checks `~/Downloads/napkin-snapshot.png` before `~/Desktop/napkin-snapshot.png`.
- [ ] Missing PNG produces clear instructions instead of silent failure.
- [ ] Clipboard JSON is attempted but never required.
- [ ] Response combines visual and structured sources in plain language and ends with a next step.
