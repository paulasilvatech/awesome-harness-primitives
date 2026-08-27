---
name: gsap-framer-scroll-animation
description: >-
  Build production scroll animations and scroll effects in vanilla JS, React, or Next.js using
  GSAP ScrollTrigger or Framer Motion/Motion v12. Use when asked for scroll-triggered reveals,
  parallax, pinned sections, horizontal scroll, scrubbed timelines, ScrollSmoother, matchMedia,
  useScroll, useTransform, useSpring, whileInView, variants, sticky sections, Apple-like scroll,
  progress bars, entrance animations, or GitHub Copilot prompts for scroll motion.
metadata:
  author: Utkarsh Patrikar
  author_url: "https://github.com/utkarsh232005"
---

<!-- Generated from harness/github-copilot/plugins/web-framework-development/skills/gsap-framer-scroll-animation/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GSAP and Framer scroll animation

Choose GSAP ScrollTrigger or Framer Motion/Motion v12 for scroll-driven motion, then implement accessible, performant animation patterns with the correct imports, hooks, cleanup, and reference recipes.

## When to invoke

- "Animate this section as I scroll."
- "Build a pinned GSAP ScrollTrigger timeline."
- "Make a Framer Motion scroll progress bar with useScroll."
- "Create parallax or Apple-like scroll effects in Next.js."
- "Generate GitHub Copilot prompts for GSAP or Framer scroll animation code."

## Library selector

| Need | Use |
| --- | --- |
| Vanilla JS, Webflow, Vue, pinning, horizontal scroll, complex timelines, scrubbing, snapping, ScrollSmoother, matchMedia | GSAP ScrollTrigger. |
| React or Next.js declarative motion, `whileInView`, `useScroll`, `useTransform`, `useSpring`, variants | Framer Motion / Motion v12. |
| Both in one Next.js app | Use references to prevent duplicated scroll listeners, conflicting transforms, and hydration errors. |
| Creative philosophy and design polish | Use the `premium-frontend-ui` skill for when and why to animate; this skill owns how. |

## Prerequisites and context

Install only the library needed by the chosen approach:

```bash
npm install gsap
npm install motion
npm install framer-motion
```

GSAP setup:

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
```

Framer/Motion v12 setup:

```js
import { motion, useScroll, useTransform, useSpring } from 'motion/react';
// legacy: import { motion } from 'framer-motion'
```

## Progressive disclosure and bundled resources

| File | Contents |
| --- | --- |
| `references/gsap.md` | ScrollTrigger API, recipes, React `useGSAP`, Lenis, `matchMedia`, accessibility, pinning, scrub, snapping, horizontal scroll, ScrollSmoother. |
| `references/framer.md` | `useScroll`, `useTransform`, variants, Motion v12 notes, Next.js tips, `whileInView`, `useSpring`, and scroll recipes. |

Read the relevant reference before generating non-trivial code.

## Common patterns

### Fade-in on enter with GSAP

```js
gsap.from('.card', {
  opacity: 0, y: 50, stagger: 0.15, duration: 0.8,
  scrollTrigger: { trigger: '.card', start: 'top 85%' }
});
```

### Fade-in on enter with Framer Motion

```jsx
<motion.div
  initial={{ opacity: 0, y: 40 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: '-80px' }}
  transition={{ duration: 0.6 }}
/>
```

### Scrubbed GSAP transform

```js
gsap.to('.hero-img', {
  scale: 1.3, opacity: 0, ease: 'none',
  scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
});
```

### Scroll-linked Framer transform

```jsx
const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] });
const y = useTransform(scrollYProgress, [0, 1], [0, -100]);
return <motion.div style={{ y }} />;
```

### Pinned GSAP timeline

```js
const tl = gsap.timeline({
  scrollTrigger: { trigger: '.section', pin: true, scrub: 1, start: 'top top', end: '+=200%' }
});
tl.from('.title', { opacity: 0, y: 60 }).from('.img', { scale: 0.85 });
```

## Implementation rules

| Area | Rule |
| --- | --- |
| GSAP registration | Always call `gsap.registerPlugin(ScrollTrigger)` before using ScrollTrigger. |
| GSAP scrub | Use `ease: 'none'` for scrubbed animations. |
| GSAP React | Use `useGSAP` from `@gsap/react`, not plain `useEffect`, so ScrollTriggers are cleaned up. |
| GSAP debug | Use `markers: true` only during development; remove before production. |
| Framer transform | Put `useTransform` output in the `style` prop of a `motion.*` element, not a plain `div`. |
| Next.js | Add `'use client'` to files using motion hooks. |
| Performance | Animate `transform` and `opacity`; avoid `width`, `height`, and `box-shadow`. |
| Accessibility | Check `prefers-reduced-motion` and provide reduced or disabled motion paths. |
| Prompting | Provide selector, base image, scroll range, start/end strings, scrub/toggleActions, hook choice, offset values, and exact errors. |

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `/fix`
- `@workspace`
- `MUST`
- `auto-cleans`
- `cross-reference`
- `design-level`
- `in-view`
- `mid-2025`
- `re-renders`
- `ready-to-use`
- `references/`
- `scroll-linked`

## Output template

```markdown
## Scroll animation implementation

**Status:** implemented | planned | blocked
**Library:** GSAP ScrollTrigger | Framer Motion/Motion v12
**Target:** <vanilla JS | React | Next.js>

### Files changed
| File | Pattern | Notes |
| --- | --- | --- |
| `<path>` | <fade-in/parallax/pinned/progress/horizontal> | <cleanup/accessibility/performance notes> |

### Validation
- Package setup: <present/needed>
- Reduced motion: <handled/not handled>
- Runtime check: <pass/fail/not run>
```

## Quality gate

- [ ] The library choice matches the requested framework and animation complexity.
- [ ] Required package and imports are present.
- [ ] GSAP code registers ScrollTrigger and cleans up React triggers with `useGSAP` when applicable.
- [ ] Framer code uses `motion.*`, `style`, and `'use client'` when hooks run in Next.js.
- [ ] Scrubbed animations use `ease: 'none'`.
- [ ] Motion respects `prefers-reduced-motion`.
- [ ] Animations primarily use `transform` and `opacity`.

## References

- [Author profile](https://github.com/utkarsh232005)
