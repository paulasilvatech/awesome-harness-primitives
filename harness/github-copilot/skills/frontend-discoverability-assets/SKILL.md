---
name: frontend-discoverability-assets
description: "Generate or audit public-web metadata, canonical URLs, crawl policy, structured data, social previews, favicons, app icons, Web App Manifests, robots rules, and sitemaps without ranking guarantees. Use this skill when frontend work involves SEO, sharing previews, PWA identity, or public-route discoverability."
---

# Frontend discoverability and assets

Apply discoverability only to public, indexable web content and generate only assets justified by the target browsers, platforms, stores, or sharing services.

## When to invoke

- "Audit this public page's SEO and metadata."
- "Generate canonical, Open Graph, structured data, robots, and sitemap rules."
- "Create favicon, app icon, maskable icon, and Web App Manifest requirements."
- "Review social preview assets for this site."
- "Protect private and preview routes from indexing."

## Route classification

Classify every route as public canonical, public duplicate/alternate, authenticated, private, sensitive, preview/staging, error, redirect, or not applicable.

Access control protects confidential content. `robots.txt` manages crawler access but is not a confidentiality or reliable deindexing mechanism.

Read [references/technical-seo.md](references/technical-seo.md).

## Metadata and structured data

- Use unique descriptive titles and useful descriptions based on visible content.
- Use stable canonical URLs and deliberate duplicate, locale, and redirect behavior.
- Keep navigation and links crawlable where public discovery is intended.
- Generate structured data only for truthful visible content and an officially supported result type.
- Do not emit `meta keywords`, hidden text, keyword stuffing, or ranking promises.

## Social previews

Read [references/social-metadata.md](references/social-metadata.md). Provide Open Graph title, type, URL, image, description, and image alternative text when applicable. Use stable absolute deployed asset URLs and no sensitive or user-specific content.

One common fallback size, including `1200 x 630`, is a project choice, not an Open Graph requirement. Recheck target-service requirements before claiming compatibility.

## Icons and manifests

Read [references/icon-matrix.md](references/icon-matrix.md).

- Preserve a professional SVG master.
- Generate PNG, ICO, maskable, monochrome, touch, or native derivatives only when required.
- Validate small-size legibility and declare bitmap sizes accurately.
- Use `sizes="any"` only for a truly scalable icon.
- Align manifest name, colors, icons, display, scope, and start URL with actual behavior.
- Do not claim PWA installability or store readiness without the applicable runtime checks.

Use [assets/metadata-checklist.md](assets/metadata-checklist.md) and [assets/public-content-review.md](assets/public-content-review.md).

## Procedure

1. Detect framework, rendering, routing, deployment URL rules, public routes, existing metadata, assets, robots, sitemap, and manifest generation.
2. Classify routes and identify canonical, alternate, private, preview, and error behavior.
3. Propose or implement metadata and assets through existing framework conventions.
4. Validate rendered output, status codes, absolute URLs, schema truthfulness, asset dimensions, and environment policy.
5. Record automated checks plus manual target-service preview checks that remain unrun.

## Limits

- Do not promise ranking, crawling, indexing, rich results, preview refresh, or PWA installability.
- Do not expose private data in metadata, structured data, sitemaps, previews, or assets.
- Do not generate store assets without current official target requirements.
- Do not replace framework metadata or asset pipelines without an approved reason.

## Progressive disclosure and bundled resources

- [references/technical-seo.md](references/technical-seo.md): route, crawl, canonical, sitemap, and structured-data rules.
- [references/social-metadata.md](references/social-metadata.md): preview metadata and validation.
- [references/icon-matrix.md](references/icon-matrix.md): master and derivative decision matrix.
- [assets/metadata-checklist.md](assets/metadata-checklist.md): implementation and audit checklist.
- [assets/public-content-review.md](assets/public-content-review.md): representative public/private/preview scenario.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Discoverability and asset result
**Status:** ready | needs revision | blocked

### Route policy
| Route class | Canonical/index policy | Metadata | Evidence |
| --- | --- | --- | --- |

### Metadata and assets
| Item | Existing | Change | Validation |
| --- | --- | --- | --- |

### Unrun external checks
- <preview, search, installability, or store check and reason>
```

## Quality gate

- [ ] Public, duplicate, private, sensitive, preview, error, and redirect routes are classified when applicable.
- [ ] Titles, descriptions, canonical URLs, crawl rules, sitemaps, locale behavior, and structured data match visible content and environment policy.
- [ ] Social metadata uses public absolute URLs and contains no sensitive data.
- [ ] An SVG master is preserved and every derivative has a target requirement.
- [ ] Rendered metadata, schema, asset dimensions, and manifest fields were checked.
- [ ] No ranking, indexing, rich-result, preview, installability, or store guarantee is made.
