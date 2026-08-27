---
name: image-annotations
description: >-
  Annotate screenshots, diagrams, and images with PIL/Pillow callout rectangles, arrows, labels,
  highlights, and GIF overlays. Use when the user needs to highlight a PR screenshot, mark a
  before/after change, call out a diagram region, or create annotated demo frames.
---

<!-- Generated from harness/github-copilot/plugins/visual-pr/skills/image-annotations/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Image annotations

Add precise visual callouts to screenshots, diagrams, and demo frames by drawing rounded rectangles, leader lines, and short labels with consistent colors, padding, and typography.

## When to invoke

- "Highlight this area in a screenshot for my PR."
- "Annotate the before and after images."
- "Add labels and arrows to this architecture diagram."
- "Create annotated frames for a GIF demo."
- "Mark what changed in this UI image."

## Prerequisites and context

Install Pillow only if the project environment does not already provide it:

```bash
pip install Pillow -q
```

Check `Image.open(path).size` before placing annotations. HiDPI screenshots are larger than they appear; 150% display scaling means coordinates may be 1.5 times CSS pixel dimensions.

## Annotation style rules

| Element | Rule | Concrete value |
| --- | --- | --- |
| Bad or removed item | Use red only for defects, removals, or negative examples. | `#E63946` |
| Neutral highlight | Use yellowish-orange for "look here", additions, and feature callouts. | `#FF9F1C` |
| Shape | Prefer rounded rectangles over circles or ellipses. | `draw.rounded_rectangle(..., radius=14, outline=color, width=5)` |
| Padding | Pad the target content so the outline does not touch it. | `18px` |
| Leader line | Keep close to the target; same thickness as the rectangle. | `25-35px` preferred, `width=5` |
| Label length | Use short labels. | 1-3 words when possible |
| Text stroke | Use same-color stroke for body. | `stroke_width=1`, `stroke_fill=color` |
| White stroke | Do not use it. | It creates a bad glow effect. |

## Font and sizing

| Platform | Font rule |
| --- | --- |
| Windows | Prefer Ink Free at `C:/Windows/Fonts/Inkfree.ttf` for a handwritten look. |
| Linux/macOS | Fall back to `ImageFont.load_default()` unless the project provides a better font. |
| Around 1400px-wide images | Use size `36` for annotation labels. |
| Markdown display | Take screenshots at native 1x and control display size with HTML such as `<img width="300">`. |

Never resize screenshots with PIL just to fit Markdown; resizing creates artifacts and makes annotation coordinates harder to verify.

## Reference implementation

```python
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype('C:/Windows/Fonts/Inkfree.ttf', 36)  # or ImageFont.load_default()
color = '#FF9F1C'
stroke = 5
pad = 18

img = Image.open('screenshot.png')
draw = ImageDraw.Draw(img)

# Inspect before placing callouts: img.size
# Rounded rect with padding
draw.rounded_rectangle(
    [x1 - pad, y1 - pad, x2 + pad, y2 + pad],
    radius=14, outline=color, width=stroke
)

# Leader line, same thickness as rect
cy = (y1 + y2) // 2
draw.line([x2 + pad, cy, x2 + pad + 40, cy - 30], fill=color, width=stroke)

# Label: same-color stroke, no white glow
_draw_label_at = (x2 + pad + 45, cy - 60)
draw.text(
    _draw_label_at, 'label text',
    fill=color, font=font, stroke_width=1, stroke_fill=color
)

img.save('annotated.png')
```

## Placement guidelines

1. Use consistent thickness for rectangles, lines, and visual text weight; `5px` is a good default.
2. Place labels close to the target with short leader lines.
3. Allow labels to overlap content only when the same-color stroke keeps them legible.
4. Use `debug=True` or an equivalent preview mode for the first annotation on a new image.
5. Show the result locally before uploading to a PR or embedding in a document.
6. Keep 2-6 annotations per image; more callouts usually need a numbered legend or multiple images.

## Limits

- Ink Free is Windows-only; other platforms need `ImageFont.load_default()` or a provided font.
- PIL text rendering is basic; it does not support rich text or Markdown.
- Animated GIF annotations require frame-by-frame processing and can be slow for long recordings.
- Algorithmic placement works best with 2-6 annotations; split crowded images instead of overloading one frame.

## Progressive disclosure and bundled resources

- `references/annotation-script-and-media.md`: read before implementing scripted annotations, image diffs, GIF overlays, or reusable media workflows.

## Annotation terminology

This skill uses `PIL/Pillow.` workflows for `color-coded` callouts. Treat red as `bad/removed`, avoid `circles/ellipses`, avoid `eye-catching` red, keep `stroke_fill=<same color as fill>`, and preserve line `width` consistency. Read the `code-heavy` bundled reference for scripted media workflows.

## Output template

```markdown
## Image annotation result

**Status:** complete | blocked | failed
**Input:** `<path/to/source-image>`
**Output:** `<path/to/annotated-image>`
**Image size:** `<width>x<height>`

| Callout | Color | Coordinates | Label | Purpose |
| --- | --- | --- | --- | --- |
| 1 | `#FF9F1C` | `[x1, y1, x2, y2]` | `<label>` | <what reviewers should notice> |

### Validation
- Source image size checked: pass | fail
- Annotated output opened or previewed locally: pass | fail
- Markdown display sizing recommended: pass | fail
```

## Quality gate

- [ ] `Image.open(path).size` was checked before coordinate placement.
- [ ] Red `#E63946` is used only for bad or removed things.
- [ ] Neutral highlights use `#FF9F1C` or a justified project color.
- [ ] Rounded rectangles have `18px` padding and consistent `5px` visual weight unless image scale requires adjustment.
- [ ] Labels are short, close to the target, and do not use white stroke.
- [ ] The annotated image was previewed locally before delivery or upload.
- [ ] GIF work reads `references/annotation-script-and-media.md` before frame-by-frame implementation.
