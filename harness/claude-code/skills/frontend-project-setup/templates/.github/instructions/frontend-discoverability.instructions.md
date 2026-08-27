---
description: "Applies public-route metadata, canonical, crawl, structured-data, social-preview, manifest, icon, robots, and sitemap conventions. Use when editing detected frontend discoverability files."
applyTo: "__FRONTEND_DISCOVERABILITY_APPLY_TO__"
---

# Frontend Discoverability Conventions — Public Content and Assets

These instructions apply to detected public-route, metadata, manifest, icon, robots, sitemap, and rendering files. They are authoritative for technical discoverability and asset integrity in the matched files; access-control, privacy, legal, product-content, framework, and deployment policies win on conflict.

## Route and Crawl Policy

- Classify routes as public canonical, public alternate, private, sensitive, preview, redirect, error, or not applicable.
- Use access control for confidential content; never present `robots.txt` as confidentiality or guaranteed deindexing.
- Keep status codes, redirects, canonical URLs, locale alternates, crawlable links, robots policy, and sitemaps aligned with the deployed environment.

## Metadata and Structured Data

- Use unique descriptive titles and useful descriptions matching visible content.
- Generate structured data only for truthful visible content and an officially supported result type.
- Use stable absolute public URLs for canonical and social metadata.
- Do not add `meta keywords`, hidden text, keyword stuffing, or ranking and rich-result promises.

## Icons, Previews, and Manifests

- Preserve an approved SVG master and create only target-required bitmap, ICO, maskable, monochrome, touch, or native derivatives.
- Keep declared bitmap sizes accurate and use `sizes="any"` only for scalable resources.
- Exclude sensitive or user-specific content from preview assets.
- Keep manifest name, colors, icons, display, scope, and start URL aligned with actual application behavior.

## Conventions

| Rule | Rationale |
| --- | --- |
| Classify route visibility before metadata work. | Public and private surfaces require different crawl and disclosure behavior. |
| Match metadata and schema to visible content. | Misleading markup creates user, search, and policy risk. |
| Generate assets only for documented targets. | Unnecessary derivatives drift and create false compatibility claims. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Validate rendered output, status, URLs, schema, dimensions, and manifest behavior. | Infer runtime or preview behavior from source files alone. |
| Recheck target-service or store guidance before compatibility claims. | Treat one image dimension as a universal Open Graph requirement. |
| Report external preview and installability checks separately. | Promise ranking, indexing, rich results, preview refresh, or PWA installability. |

## Checklist Before Opening a PR

- [ ] Public, private, sensitive, preview, redirect, error, and alternate routes are classified.
- [ ] Rendered title, description, canonical, crawl, locale, sitemap, and schema behavior matches visible content.
- [ ] Social URLs are absolute and preview assets contain no sensitive data.
- [ ] SVG master and justified derivatives have accurate declarations.
- [ ] Manifest fields match real scope, start URL, display, colors, and icons.
- [ ] Automated and manual preview/installability checks ran or are explicit gaps.
