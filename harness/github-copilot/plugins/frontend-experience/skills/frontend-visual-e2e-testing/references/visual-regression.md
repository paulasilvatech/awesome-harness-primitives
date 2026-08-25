# Visual regression policy

- Pin browser, OS/container, viewport, device scale, fonts, locale, timezone, color scheme, reduced motion, data, and animation.
- Separate baselines by environment where rendering differs.
- Mask only truly variable regions and document every mask.
- Review baseline changes as product changes.
- Pair image comparison with behavior and semantic assertions.
- Test real state and content, not blank placeholders.
- Keep screenshot thresholds narrow and evidence-backed.
- Do not compare baselines generated in a materially different environment.
