---
applyTo: "**/*.html,**/*.css,**/*.js"
description: "Enforces accessible, professional HTML/CSS color usage conventions for backgrounds, text, accents, gradients, and contrast-sensitive browser styling."
---

# HTML CSS Color Conventions — Accessible Professional Styling

These instructions apply to HTML, CSS, and JavaScript files that create or update browser-rendered styles. They are authoritative for color palette balance, background colors, text colors, gradients, accents, and contrast-sensitive styling; product design systems, explicit user design specifications, and accessibility requirements win where they define stricter colors. Treat color names as full hue ranges: blue includes navy and sky blue, and similar ranges apply to red, green, purple, orange, yellow, pink, black, white, and gray.

## Color Definitions and Palette Balance

- Treat hot colors as oranges, reds, and yellows.
- Treat cool colors as blues, greens, and purples.
- Treat neutral colors as grays and grayscale variations.
- Treat binary colors as black and white.
- Apply the 60-30-10 rule to graphic design elements such as backgrounds, buttons, cards, containers, and navigation.

| Role | Usage | Preferred range |
| --- | --- | --- |
| Primary Color | 60% | Cool or light color |
| Secondary Color | 30% | Cool or light color |
| Accent | 10% | Complementary hot color |

## Background Colors

- Never use purple, magenta, red, orange, yellow, pink, or any hot color as a general background unless an explicit design specification requires it.
- Prefer white, off-white, light cool colors such as light blues and light greens, subtle neutral tones, and light gradients with minimal color shift.
- Keep large background areas calm so text, controls, and accents remain readable.

## Text Colors and Contrast

- Never use yellow text for normal content because it has poor contrast and readability.
- Avoid pink text unless a design specification requires it and contrast passes.
- Do not use pure white or light text on light backgrounds.
- Do not use pure black or dark text on dark backgrounds.
- Prefer dark neutral text such as `#1f2328`, `#24292f`, near-black values from `#000000` to `#333333` on light backgrounds, and dark grays such as `#4d4d4d` or `#6c757d`.
- Prefer near-white values from `#ffffff` to `#f0f2f3` on dark backgrounds.
- Use high-contrast combinations that satisfy WCAG accessibility standards.

## Colors to Avoid or Use Sparingly

- Avoid bright purples, magentas, bright pinks, neon colors, highly saturated hot colors, and low-contrast combinations unless explicitly required by design specifications or user request.
- Reserve hot colors such as red, orange, and yellow for critical alerts, warnings, errors, urgency, and importance.
- Limit hot colors to small accent areas instead of large sections.
- Prefer icons, bold text, labels, or shape changes before relying on hot color alone.

## Gradients

- Use gradients with subtle color transitions such as `#E6F2FF` to `#F5F7FA`.
- Keep gradients within the same color family.
- Avoid combining hot and cool colors in one gradient.
- Prefer linear gradients over radial gradients for backgrounds.
- Use gradients for background containers, sections, button hover states, interactive elements, drop shadows, depth effects, headers, navigation bars, cards, and panels when they remain restrained.

## Good / Bad Examples

The examples below illustrate accessible color and gradient choices.

**Good:**

```css
.card {
  background: linear-gradient(180deg, #E6F2FF 0%, #F5F7FA 100%);
  color: #24292f;
}

.card__warning {
  color: #8a4600;
  font-weight: 700;
}
```

Why: The background uses a subtle cool gradient, text uses a dark neutral color, and the warm color is limited to a warning accent.

**Bad:**

```css
.card {
  background: linear-gradient(90deg, magenta, yellow);
  color: pink;
}
```

Why: The background uses saturated hot and magenta colors, the text has poor contrast, and the palette ignores the 60-30-10 rule.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use the 60-30-10 rule for primary, secondary, and accent colors | Balanced palettes look intentional and readable |
| Prefer white, off-white, light cool, and subtle neutral backgrounds | Large surfaces should not compete with content |
| Use dark neutrals on light backgrounds and near-white on dark backgrounds | Text remains legible and contrast-friendly |
| Avoid yellow, pink, neon, highly saturated hot colors, and low-contrast combinations | These choices commonly fail accessibility or look unprofessional |
| Reserve red, orange, and yellow for alerts, warnings, errors, or small accents | Hot colors communicate urgency when used sparingly |
| Keep gradients subtle, linear, and within one color family | Gradients add depth without visual noise |
| Pair color with text, icons, or emphasis | Color alone is not an accessible signal |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use cool or light colors for the 60% and 30% palette roles | Make hot colors dominate the page |
| Use `#1f2328`, `#24292f`, `#4d4d4d`, or `#6c757d` on light backgrounds | Use yellow or pink for ordinary text |
| Use `#ffffff` to `#f0f2f3` on dark backgrounds | Put light text on light backgrounds or dark text on dark backgrounds |
| Use subtle gradients such as `#E6F2FF` to `#F5F7FA` | Combine hot and cool saturated colors in one gradient |
| Use red, orange, and yellow for small warnings or errors | Use hot colors as full-page backgrounds |
| Check WCAG contrast | Assume a color is readable because it looks bright |

## Checklist Before Opening a PR

- [ ] Primary, secondary, and accent colors follow the 60-30-10 rule or an explicit design system.
- [ ] Backgrounds avoid purple, magenta, red, orange, yellow, pink, and other hot colors unless explicitly required.
- [ ] Text colors maintain high contrast and avoid yellow, pink, light-on-light, and dark-on-dark combinations.
- [ ] Hot colors are limited to critical alerts, warnings, errors, urgency, or small accents.
- [ ] Gradients are subtle, linear where appropriate, and within a compatible color family.
- [ ] Color is not the only signal for status or interaction.
- [ ] WCAG accessibility contrast is checked for changed text and interactive elements.

## References

- Color Tool: <https://civicactions.github.io/uswds-color-tool/>
- Government or Professional Color Standards: <https://designsystem.digital.gov/design-tokens/color/overview/>
- UI Color Palette Best Practices: <https://www.interaction-design.org/literature/article/ui-color-palette>
- Color Combination Resource: <https://www.figma.com/resource-harness/github-copilot/color-combinations/>
