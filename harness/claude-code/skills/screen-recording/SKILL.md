---
name: screen-recording
description: >-
  Create annotated GIF demos and screen recordings for pull requests, bug reports, release notes,
  and documentation. Use this skill when the user asks to record a UI workflow, capture a
  before/after demo, make an animated GIF, annotate interactions, or show a bug reproduction.
---

<!-- Generated from harness/github-copilot/skills/screen-recording/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Screen recording

Capture browser or desktop interactions, assemble them into a readable animated GIF, add annotations with intentional timing, and report the commands, files, and compatibility tradeoffs used.

## When to invoke

- "Record this UI workflow as an animated GIF."
- "Create a before/after demo for my PR."
- "Show this bug reproduction in a screen recording."
- "Add annotations to a GIF walkthrough."
- "Make a demo for documentation or release notes."

## Prerequisites and context

```bash
pip install playwright Pillow imageio numpy scipy mss -q
playwright install chromium
```

Use Playwright for browser capture, `mss` for desktop apps or terminals, `Pillow` for image operations, `numpy` and `scipy.ndimage` for frame-diff detection, and `imageio.v3.imwrite` for annotated GIF output.

## Procedure

1. Choose capture mode: Playwright for web pages; `mss` for desktop apps, terminals, or anything outside a browser.
2. Capture the raw frame sequence first and verify framing, viewport, and region before adding annotations.
3. Add annotations only after the sequence is correct. Use the `image-annotations` skill for complex callouts.
4. Tune timing last with variable durations: fast action, pause, annotation, and hero/final message.
5. Assemble the final GIF with `imageio.v3.imwrite` when fades or annotations matter.
6. Test a small isolated GIF for fade or annotation tweaks before rebuilding the full demo.
7. Deliver the output path, frame count, timing choices, and any compatibility limits.

## Browser capture

```python
from playwright.async_api import async_playwright

async def record_frames(url, steps, width=1400, height=900):
    """
    steps: list of dicts with 'action' (async callable taking page)
           and 'name' (frame filename)
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.goto(url, wait_until="networkidle")

        for step in steps:
            if step.get("action"):
                await step["action"](page)
                await page.wait_for_timeout(step.get("wait", 500))
            await page.screenshot(path=step["name"])

        await browser.close()
```

## GIF assembly and timing

Use `imageio`, not `PIL`, for GIF writing when animation fidelity matters. PIL's GIF encoder can merge visually similar frames and kill fades.

```python
import imageio.v3 as iio
from PIL import Image
import numpy as np

frames = []
durations = []

for frame_path, duration_ms in frame_list:
    img = Image.open(frame_path)
    frames.append(np.array(img))
    durations.append(duration_ms)

iio.imwrite("demo.gif", frames, duration=durations, loop=0)
```

| Phase | Duration | Why |
| --- | --- | --- |
| Fast action, typing, clicking | `100ms` | Feels natural and keeps energy. |
| Pause after action | `600-800ms` | Lets the viewer process what changed. |
| Hero/final message | `500ms+` | Gives the main takeaway time to land. |

## Annotation patterns

```python
from PIL import Image, ImageDraw, ImageFont

def annotate_frame(frame_path, annotations, out_path):
    img = Image.open(frame_path)
    draw = ImageDraw.Draw(img)

    for ann in annotations:
        # Apply annotation (rect, arrow, label, etc.)
        pass

    img.save(out_path)
```

```python
def apply_fade(base_frame, annotation_layer, alpha):
    """Blend annotation onto frame at given alpha (0.0 to 1.0)"""
    blended = Image.blend(
        base_frame.convert("RGBA"),
        annotation_layer.convert("RGBA"),
        alpha
    )
    return blended.convert("RGB")

faded_frames = [
    apply_fade(base, annotations, 0.5),
    apply_fade(base, annotations, 1.0),
]
```

At `10fps`, use 2 fade frames for `0.2s` total. At `30fps`, use 3-4 frames. Use `Type → pause → annotate`: show no annotation during fast action, pause first, then annotate. Use 64pt+ for the hero message and 38pt for details. GIF palettes do not kill gradients by themselves; 20 distinct alpha steps survive a 256-color palette.

## Desktop recording

```python
import mss
from PIL import Image
import time

def record_gif(output_path, region=None, duration=5, fps=8):
    """Record screen region to GIF. region = {left, top, width, height} or None for full screen."""
    with mss.mss() as sct:
        if region is None:
            region = sct.monitors[1]

        frames = []
        t_end = time.time() + duration
        while time.time() < t_end:
            t0 = time.time()
            shot = sct.grab(region)
            frames.append(Image.frombytes('RGB', shot.size, shot.rgb))
            time.sleep(max(0, 1 / fps - (time.time() - t0)))

    frames[0].save(output_path, save_all=True, append_images=frames[1:],
                   duration=int(1000 / fps), loop=0, optimize=True)
    return len(frames)

record_gif('demo.gif', region={'left': 0, 'top': 0, 'width': 800, 'height': 500}, duration=3)
```

A tested target is `3s` at `8fps` for 24 frames, around `31KB`. Keep fps ≤ 10 for reasonable file sizes. `PIL.save(save_all=True)` is acceptable for simple recordings, but use `imageio.v3.imwrite` for annotated GIFs and fade effects.

For window capture on Windows, reuse `find_window()` from the `ui-screenshots` skill, then capture the rectangle:

```python
import ctypes
from ctypes import c_int, Structure, byref, windll

class RECT(Structure):
    _fields_ = [('left', c_int), ('top', c_int), ('right', c_int), ('bottom', c_int)]

hwnd = find_window('My App')[0][0]
rect = RECT()
windll.user32.GetWindowRect(hwnd, byref(rect))
region = {'left': rect.left, 'top': rect.top,
          'width': rect.right - rect.left, 'height': rect.bottom - rect.top}
record_gif('app-demo.gif', region=region, duration=5, fps=8)
```

## Diff-based cluster detection

```python
import numpy as np
from scipy import ndimage

def find_changed_clusters(frame_a, frame_b, threshold=30, min_pixels=300, dilate=5):
    """Find bounding boxes of changed regions between two frames."""
    diff = np.abs(frame_b.astype(float) - frame_a.astype(float)).max(axis=2)
    mask = diff > threshold
    dilated = ndimage.binary_dilation(mask, iterations=dilate)
    labeled, n = ndimage.label(dilated)
    clusters = []
    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        if len(ys) < min_pixels:
            continue
        clusters.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
    return sorted(clusters, key=lambda c: -c[4])
```

## Format compatibility

| Format | VS Code Preview | GitHub | Browser |
| --- | --- | --- | --- |
| GIF | Animates | Yes | Yes |
| WebP | Static only | Yes | Yes |
| MP4 | Broken |  | Yes |

GIF is the only universally supported animated format across VS Code preview, GitHub markdown, and browsers. GIF is limited to 256 colors per frame, has no audio, and can become several MB with 50+ high-resolution frames; crop to the relevant area or use MP4 for narrated demos when VS Code preview support is not required.

## Gotchas

- **Build iteratively**: get the frame sequence right first, add annotations second, and tune timing last.
- **Test animations in isolation**: create a small test GIF with 10 bare frames, fade frames, 15 hold frames, and a frame counter such as `F{i}/{total} a={alpha:.0%} FADE` before rebuilding the full demo.
- **Avoid low-FPS typing**: 10fps is the minimum for typing and interaction; lower rates look stuttery.
- **Do not rely on PIL for annotated fades**: visually similar frames may be merged.

## Script and timing vocabulary

For non-trivial demos, build a dedicated script such as `annotate_gif.py` or `annotate_gif` rather than inline one-off code. Preserve the `multi-step`, `pop-in`, `typing/interaction`, and `small_font` concepts when describing frame counters, annotation timing, and readable debug overlays.

## Output template

```markdown
### Screen recording result

**Status:** complete | needs iteration | blocked
**Output file:** `<path/to/demo.gif>`
**Capture mode:** Playwright | mss desktop | window region
**Dimensions:** `<width>x<height>`
**Frames:** `<count>`
**Timing:** `<fast action ms> / <pause ms> / <hero ms>`

**Artifacts**
- Raw frames: `<directory or none>`
- Annotation script: `<script path or none>`
- Final GIF: `<path>`

**Compatibility**
- GitHub: pass | fail
- VS Code preview: pass | fail
- Browser: pass | fail
```

## Quality gate

- [ ] Required packages and browser runtime are installed or the blocker is reported.
- [ ] Capture mode matches the target: Playwright for web, `mss` for desktop, window region when needed.
- [ ] Raw sequence was verified before annotations were added.
- [ ] Final assembly uses `imageio.v3.imwrite` when annotations or fades are present.
- [ ] Timing includes fast action, processing pause, and hero/final hold durations.
- [ ] FPS is at least 10 for typing or interaction and no more than needed for size.
- [ ] Significant changes are annotated after the action, not during the action.
- [ ] GIF compatibility and limitations are reported.
