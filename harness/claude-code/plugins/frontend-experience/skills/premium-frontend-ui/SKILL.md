---
name: premium-frontend-ui
description: >-
  Craft immersive, high-performance web interfaces with advanced motion, typography, scroll-driven
  interactions, responsive polish, and product-specific visual direction. Use this skill when the
  user asks for premium frontend UI, sophisticated animations, Awwwards-style components, high-end
  landing pages, layout polish, or high-end visual design implementation.
metadata:
  author: Utkarsh Patrikar
  author_url: "https://github.com/utkarsh232005"
---

<!-- Generated from harness/github-copilot/plugins/frontend-experience/skills/premium-frontend-ui/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Premium frontend UI

Transform a functional frontend request into an immersive, high-performance interface by choosing a clear visual identity, layering motion intentionally, and enforcing accessibility and performance constraints before delivery.

## When to invoke

- "Build a premium landing page."
- "Create an Awwwards-style component."
- "Make this UI feel high-end and immersive."
- "Add sophisticated scroll-driven interactions."
- "Polish this frontend layout and motion system."

## Creative foundation

Commit to one visual identity before writing layout code; do not default to generic neutral UI.

| Direction | Use when | Design decisions |
| --- | --- | --- |
| Editorial Brutalism | Content needs authority, contrast, and sharp hierarchy. | High-contrast monochrome, oversized typography, raw grid structures, sharp rectangular edges. |
| Organic Fluidity | Brand should feel soft, expressive, and tactile. | Soft gradients, deeply rounded corners, glassmorphism overlays, bouncy spring-based physics. |
| Cyber / Technical | Product needs precision, systems, data, or developer energy. | Dark mode dominance, glowing neon accents, monospaced typography, rapid staggered reveal animations. |
| Cinematic Pacing | Storytelling and atmosphere matter more than density. | Full-viewport imagery, slow cross-fades, negative space, scroll-dependent storytelling. |

## Structural requirements

| Layer | Required implementation | Premium failure to avoid |
| --- | --- | --- |
| Entry sequence | Add a lightweight preloader or initialization state for fonts, first images, or 3D models, then transition with a split-door reveal, scale-up zoom, or staggered text sweep. | Blank initial screen or abrupt content pop-in. |
| Hero architecture | Use full-bleed containers such as `100vh` or `100dvh`; break headlines into word or character spans for cascading entrance animations. | A centered card that could belong to any SaaS template. |
| Depth | Add subtle floating elements, background clipping paths, layered media, or atmospheric surfaces behind primary copy. | Decorative shapes unrelated to hierarchy. |
| Navigation | Use sticky headers that react to scroll direction, hiding on scroll down and revealing on scroll up. | Standard static navbars with no contextual behavior. |
| Rich hover | Use previews, mega-menus, or product-relevant hover states where they help choice. | Hover decoration that reveals nothing useful. |

## Motion design system

| Pattern | Implementation guidance | Guardrail |
| --- | --- | --- |
| Scroll-driven narratives | Use GSAP ScrollTrigger or framework-equivalent timelines to tie progress to pinned containers, reveals, and transforms. | Do not make essential content inaccessible without scroll scripting. |
| Horizontal journeys | Translate vertical scroll into horizontal gallery or showcase movement only for content that benefits from sequencing. | Preserve keyboard and reduced-motion alternatives. |
| Parallax mapping | Assign different scroll speeds to background, midground, and foreground elements with subtle values. | Avoid nausea-inducing large deltas. |
| Magnetic components | Calculate pointer distance and move buttons slightly toward the cursor. | Limit to `@media (hover: hover) and (pointer: fine)`. |
| Custom cursor | Follow the pointer with interpolation or `lerp` only when it clarifies interaction. | Never replace native cursor affordances for text input. |
| Dimensional hover | Use `scale`, `rotateX`, and `translate3d` for tactile weight. | Avoid layout-affecting hover changes. |

## Typography and texture

- Use extreme but controlled type hierarchy: fluid headlines with `clamp()` up to `12vw`, crisp body copy around `16px-18px` minimum.
- Prefer specific variable fonts or premium typefaces over unconsidered system defaults.
- Add atmospheric CSS/SVG noise overlays with `mix-blend-mode: overlay` and opacity around `0.02 - 0.05` to avoid digital sterility.
- Use `backdrop-filter: blur(x)` with thin semi-transparent borders for frosted-glass depth only when the surface has content or hierarchy value.
- Make headings, labels, and calls to action product-specific; never ship placeholder metrics or vague "learn more" clusters when concrete content exists.

## Performance and accessibility guardrails

| Guardrail | Apply it |
| --- | --- |
| Hardware acceleration | Animate only `transform` and `opacity`; avoid animating `width`, `height`, `top`, or `margin`. |
| Render optimization | Apply `will-change: transform` only shortly before expensive motion and remove it after animation. |
| Touch degradation | Wrap custom cursor and heavy hover logic in `@media (hover: hover) and (pointer: fine)`. |
| Motion preference | Wrap heavy continuous animation in `@media (prefers-reduced-motion: no-preference)`. |
| Accessibility | Preserve semantic structure, focus order, contrast, keyboard behavior, touch targets, zoom readability, and reduced-motion alternatives. |

## Implementation ecosystem

| Target | Preferred tools |
| --- | --- |
| React / Next.js | Framer Motion for layout transitions and spring physics; Lenis (`@studio-freight/lenis`) for smooth scrolling; React Three Fiber (`@react-three/fiber`) for WebGL or 3D interactions when requested. |
| Vanilla / HTML / Astro | GSAP (GreenSock Animation Platform) for timeline sequencing; Lenis via CDN for smooth scrolling when appropriate; SplitType for accessible typography chunking. |

## Gotchas

- **Beautiful stutter is still failure**: composited animation and reduced-motion support are mandatory, not polish.
- **Premium is not more decoration**: every badge, blur, grain, shadow, and motion cue must communicate state, hierarchy, or brand intent.
- **Scroll hijacking can harm users**: use smooth scrolling conservatively and test keyboard, touch, and reduced-motion paths.
- **Generic hero sections erase identity**: choose a direction and encode it in typography, density, spacing, motion, and content.

Aim for award-level, top-tier craft without sacrificing engineering. industry-standard libraries are acceptable, but still remove `will-change` post-animation, tune parallax scroll-speeds, keep scroll-smoothed behavior accessible, and prefer ultra-thin borders only when they reinforce hierarchy.

## Output template

```markdown
## Premium frontend UI result

**Status:** implemented | designed | blocked
**Visual direction:** <Editorial Brutalism | Organic Fluidity | Cyber / Technical | Cinematic Pacing | custom>
**Target:** <framework/page/component>

| Layer | Decision | Evidence in implementation |
| --- | --- | --- |
| Entry | `<preloader or initialization>` | `<file/component>` |
| Hero/layout | `<structure>` | `<file/component>` |
| Motion | `<timeline/interactions>` | `<file/component>` |
| Typography/texture | `<type and surface rules>` | `<file/component>` |
| Performance/accessibility | `<guardrails>` | `<checks>` |

**Validation**
- Responsive breakpoints: <checked/not checked>
- Reduced motion: <checked/not checked>
- Keyboard/focus: <checked/not checked>
- Performance risk: <notes>
```

## Quality gate

- [ ] A strong visual identity was chosen before layout code.
- [ ] Entry sequence, hero architecture, depth, navigation, and hover behavior were considered or explicitly scoped out.
- [ ] Motion uses `transform` and `opacity` instead of layout-triggering properties.
- [ ] Custom cursor, magnetic hover, and heavy animations are gated for pointer and reduced-motion preferences.
- [ ] Typography uses fluid hierarchy and product-specific content rather than generic copy.
- [ ] Accessibility semantics, focus order, contrast, touch targets, zoom, and reduced-motion behavior were checked.
- [ ] The final output reports implementation files and validation evidence.

## References

- [Author profile](https://github.com/utkarsh232005)
