---
name: "image-annotations"
description: >-
  Annotate screenshots, diagrams, and images with callout rectangles, arrows, labels, and color-coded
  highlights using PIL. Use this skill when you need to; highlight a specific area in a screenshot for
  a PR description; annotate before/after images to show what changed.
---
# Image Annotations

Add visual callouts to any image — screenshots, diagrams, architecture docs, demo frames — using PIL/Pillow. Highlights what changed or what to look at, so reviewers don't have to guess.

## When to Use This Skill

Use this skill when you need to:

- Highlight a specific area in a screenshot for a PR description
- Annotate before/after images to show what changed
- Add labels and callouts to diagrams or architecture images
- Create annotated frames for animated GIF demos

## Prerequisites

```bash
pip install Pillow -q
```

## Color Rules

- **Red (`#E63946`)** — only for "bad" / "removed" things (e.g., circling a bug being fixed)
- **Yellowish-orange (`#FF9F1C`)** — for neutral highlights ("look here", "new feature", etc.)
- Never use red just because it's eye-catching — red = bad/removed

## Font

- Use **Ink Free** (`C:/Windows/Fonts/Inkfree.ttf`) for a handwritten look on Windows
- On Linux/macOS, fall back to `ImageFont.load_default()`
- Size **36** for annotations on ~1400px-wide images
- `stroke_width=1` with `stroke_fill=<same color as fill>` — gives body without being too thick
- Do NOT use white stroke — looks like a bad glow effect

## Shapes

- Prefer **rounded rectangles** over circles/ellipses — less pixelation at edges
- `draw.rounded_rectangle([x1, y1, x2, y2], radius=14, outline=color, width=5)`
- **Padding 18px** around the target content

## Reference Snippet

```python
from PIL import Image, ImageDraw, ImageFont

# Setup
font = ImageFont.truetype('C:/Windows/Fonts/Inkfree.ttf', 36)  # or load_default()
color = '#FF9F1C'  # orange for highlights
stroke = 5
pad = 18

img = Image.open('screenshot.png')
draw = ImageDraw.Draw(img)

# Rounded rect with padding
draw.rounded_rectangle(
    [x1 - pad, y1 - pad, x2 + pad, y2 + pad],
    radius=14, outline=color, width=stroke
)

# Leader line (same thickness as rect)
draw.line([x2 + pad, cy, x2 + pad + 40, cy - 30], fill=color, width=stroke)

# Label — same-color stroke for body, NO white stroke
draw.text(
    (x2 + pad + 45, cy - 60), 'label text',
    fill=color, font=font, stroke_width=1, stroke_fill=color
)

img.save('annotated.png')
```

## Bundled Resources

- [Image annotation scripts and media workflows](references/annotation-script-and-media.md) — For implementing scripted annotations, image diffs, or GIF overlays, open this code-heavy reference.

## Guidelines

1. **All elements same thickness** — rect `width`, line `width`, and visual text weight should feel consistent (~5px)
2. Place labels **close to the rect** — short leader line (25-35px)
3. Labels can overlap content — the stroke gives enough contrast
4. **Show locally first** — verify before uploading to a PR
5. **Take screenshots at native 1x, control display size in HTML** — use `<img width="300">` in markdown, never resize with PIL (creates artifacts)
6. **Always check `Image.open(path).size` first** — HiDPI screenshots are larger than they appear (150% scaling = 1.5x CSS pixel dimensions)
7. **Short labels work better** — wide labels have fewer valid placements. Use 1-3 words when possible
8. **Verify with debug=True** — always check the first annotation of a new image with debug mode

## Limitations

- Ink Free font is Windows-only; other platforms need a fallback font
- PIL text rendering is basic — no rich text, no markdown
- Animated GIF annotations require frame-by-frame processing which can be slow for long recordings
- Algorithmic placement works best with 2-6 annotations; more than that may produce crowded results
