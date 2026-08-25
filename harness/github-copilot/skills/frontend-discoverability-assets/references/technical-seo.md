# Technical discoverability

## Public routes

- Return correct success, redirect, not-found, and error status behavior.
- Use descriptive titles, useful snippets, meaningful headings, crawlable links, stable URLs, and canonical handling.
- Include eligible canonical URLs in a sitemap only when it benefits discovery.
- Use locale and `hreflang` behavior only when the product publishes approved alternates.
- Ensure critical public content is rendered in a crawlable form for the selected architecture.

## Private and preview routes

- Require access control for confidential content.
- Keep preview, staging, authenticated, and sensitive URLs out of public discovery through deliberate environment policy.
- Do not rely on `robots.txt` as confidentiality or guaranteed deindexing.

## Structured data

Use the target search engine's official supported type and validation guidance. Data must match visible content, remain accurate, and avoid hidden or misleading claims. Valid syntax creates eligibility only.

Official starting points:

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- https://developers.google.com/search/docs/crawling-indexing/robots/intro
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
