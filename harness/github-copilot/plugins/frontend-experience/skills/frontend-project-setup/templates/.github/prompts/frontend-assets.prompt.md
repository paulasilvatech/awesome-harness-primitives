---
name: 'frontend-assets'
description: 'Generate or audit public metadata, canonical and crawl rules, structured data, social previews, icons, and Web App Manifest assets.'
argument-hint: 'Describe the public routes, target services/platforms, existing master assets, and destination.'
---

# /frontend-assets

## Objective

Generate or audit truthful public-web metadata and only the preview, icon, and manifest assets justified by approved target services and platforms.

Deliver the result to `${input:destination:response, edit, or file path}`. Limit edits to explicitly approved discoverability and asset files.

## When to Invoke

Run for public-route SEO, sharing previews, canonical and crawl policy, structured data, favicons, PWA manifests, app icons, or asset audits.

## Preconditions

- `${input:topic}` identifies public/private/preview route intent and target services or platforms.
- Existing framework metadata conventions, deployment URLs, visible content, and master assets can be inspected.
- Any requested generated asset has approved branding and a documented target requirement.

If route privacy, asset rights, or target requirements are unknown, return the decision gap and stop before writing.

## Inputs the Team Must Provide

| Input | Runtime source | Required | Handling |
| --- | --- | --- | --- |
| Discoverability/asset task | `${input:topic}` | Yes | Use as scope; ask and stop if undefined. |
| Selected routes/assets | `${selection}` | No | Treat empty selection as absent and inspect only approved files. |
| Destination | `${input:destination:response, edit, or file path}` | Yes | Response, bounded edit, or exact discoverability/asset path. |
| Target services/platforms | Prompt/repository | Yes for compatibility | Recheck official requirements before claims. |

## What I Will Do

- Use `frontend-discoverability-assets` and preserve framework metadata and asset pipelines.
- Classify public canonical, alternate, private, sensitive, preview, redirect, and error routes.
- Validate rendered titles, descriptions, canonical URLs, crawl rules, sitemaps, structured data, and social metadata.
- Preserve an approved SVG master and create only justified derivatives with accurate dimensions.
- Report external preview, search, installability, and store checks separately.

## What I Will NOT Do

- Promise ranking, crawling, indexing, rich results, preview refresh, installability, or store acceptance.
- Put private, personal, secret, or user-specific data in metadata, schemas, sitemaps, previews, or assets.
- Treat `robots.txt` as access control or guaranteed deindexing.
- Copy proprietary branding or create unapproved store assets.

## Output Format

- **Response:** return the audit/asset plan in Chat.
- **Edit:** modify only approved metadata and asset paths.
- **File path:** write only the exact requested output.

```markdown
## Frontend Asset Result

### Route Policy
| Route class | Canonical/index policy | Metadata | Evidence |
| --- | --- | --- | --- |

### Metadata and Assets
| Item | Target | Source/master | Output/change | Validation |
| --- | --- | --- | --- | --- |

### External Checks
- <search, preview, installability, or store check and result/gap>
```

## Definition of Done

- [ ] Route visibility and environment policy are classified.
- [ ] Metadata and structured data match visible public content.
- [ ] Canonical and social URLs are stable, absolute, and non-sensitive.
- [ ] SVG master and every derivative have approved rights, targets, and accurate declarations.
- [ ] Manifest scope, start URL, display, colors, and icons match application behavior.
- [ ] No unsupported guarantee is made and unrun external checks are explicit.

## Prompt Body

Complete discoverability or asset work for:

- **Topic:** `${input:topic}`
- **Destination:** `${input:destination:response, edit, or file path}`
- **Selected context:**
  ```text
  ${selection}
  ```

Follow these steps in order:

1. **Validate route and asset intent.** Confirm public/private/preview policy, target services/platforms, rights, and destination.
2. **Inspect local conventions.** Detect framework rendering, metadata APIs, routes, deployment URL handling, robots, sitemap, manifest, and asset pipeline.
3. **Generate or audit.** Apply `frontend-discoverability-assets`, preserve the SVG master, and modify only approved files.
4. **Validate rendered truth.** Check status, URLs, schema, dimensions, manifest fields, and absence of sensitive data or unsupported claims.
5. **Deliver conditionally.** Respect the destination and report external preview/installability checks separately.

One common preview image size is never a universal Open Graph requirement.

## Invocation Example

1. Select the public route and existing asset declarations.
2. Run **Chat: Run Prompt** and choose `/frontend-assets`.
3. Enter `Audit the article route, Open Graph preview, favicon, and manifest for production and preview environments` for `topic`.
4. Enter `response` for `destination`.
5. Verify no asset is generated without an approved target.

## Related Primitives

| Name | Type | Relationship |
| --- | --- | --- |
| `frontend-discoverability-assets` | skill | Owns route classification, metadata, preview, icon, and manifest criteria. |
| `frontend-product-designer` | agent | Resolves product-content, brand, and route-policy decisions. |
