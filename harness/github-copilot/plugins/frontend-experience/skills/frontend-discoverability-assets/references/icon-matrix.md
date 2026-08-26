# Icon and manifest matrix

| Asset | Add when | Verify |
| --- | --- | --- |
| SVG master | Product identity needs a scalable source | Clean geometry, brand approval, small-size simplification |
| Browser favicon | Supported browser route needs identity | Declared type/sizes, light/dark behavior where used |
| ICO | Legacy or target support requires it | Contained sizes and small rendering |
| PNG sizes | Manifest, browser, OS, or service requires bitmaps | Actual pixels match declaration |
| Maskable icon | PWA target uses maskable purpose | Safe zone and background across masks |
| Monochrome/pinned | Target platform documents it | Single-color legibility and current syntax |
| Touch/native icon | Approved platform or store target requires it | Current official dimensions, masking, alpha, and submission rules |

Manifest fields must match actual app behavior: name, short name, icons, theme/background colors, display, scope, and start URL.

Use `sizes="any"` only for scalable resources, as defined by the HTML link-type rules: https://html.spec.whatwg.org/multipage/links.html
