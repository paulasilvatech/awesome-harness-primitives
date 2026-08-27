---
name: content-management-systems
description: >-
  Build and modify content management systems by locating the correct theme, plugin, module,
  editor, content model, media, render, or export seam before changing code. Use this skill when
  working on WordPress, Shopify, Wix, Squarespace, Drupal, WooCommerce, Joomla, HubSpot CMS Hub,
  Webflow, Adobe Experience Manager, headless CMS work, CMS themes, plugins, apps, modules, admin
  panels, uploads, markdown pipelines, and static export workflows.
---

<!-- Generated from harness/github-copilot/plugins/cms-development/skills/content-management-systems/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Content management systems

Apply CMS-specific change discipline: identify the platform and owning seam, preserve authored content boundaries, make the smallest code change in the correct extension point, and validate both editor and rendered output.

## When to invoke

- "Update this WordPress theme template."
- "Add a Shopify section for this product page."
- "Fix media uploads in the CMS admin."
- "Change the Drupal content type and render output."
- "Review this static export pipeline for CMS pages."

## Platform and seam map

| Platform category | Examples | Owning seams to inspect first |
| --- | --- | --- |
| Self-hosted CMS | WordPress, Drupal, Joomla, WooCommerce | Theme hierarchy, plugins/modules, hooks/events, migrations, upload settings. |
| SaaS site builder | Wix, Squarespace, Webflow | Designer-exported code, embedded custom code, CMS collections, asset hosting, publish settings. |
| Commerce CMS | Shopify, WooCommerce | Product models, theme sections/templates, checkout constraints, app extension points, media libraries. |
| Hybrid/headless | HubSpot CMS Hub, Adobe Experience Manager, headless CMS stacks | Content schemas, delivery APIs, preview routes, render pipeline, static export or SSR layer. |

## First-pass procedure

1. Identify the platform category and concrete platform.
2. Find the owning seam before editing: theme/template, plugin/app/module, admin/editor surface, content model/storage, media pipeline, or export/render pipeline.
3. Separate authored content from code-owned assets.
4. Check whether final output is server-rendered, statically exported, or hosted remotely.
5. Change the smallest file at the owning seam, then validate the authoring path and final render path together.

## CMS rules

| Area | Rule | Why it matters |
| --- | --- | --- |
| Themes and templates | Follow platform naming, folder, template hierarchy, partial, section, and helper conventions. | CMS runtimes often select templates by name and location. |
| Extension logic | Put behavior in plugins, apps, modules, hooks, or extension points instead of scattering logic in templates. | Keeps upgrades and theme swaps survivable. |
| Content modeling | Prefer structured fields for metadata, SEO fields, taxonomy, slugs, excerpts, publish state, and canonical data. | Presentation markup is brittle storage. |
| Editor UX | Trace stored field, validation rule, preview path, permission check, and final render path together. | Editor success does not guarantee frontend correctness. |
| Media | Keep authored uploads separate from decorative theme assets. | Avoids deleting user media during theme deploys. |
| Static export | Validate rewritten permalinks, asset paths, and generated routes after build changes. | Static hosts expose broken relative links immediately. |

## Common workflows

### Themes and templates

Start at the template loader or theme runtime, not at a downstream include. Preserve hierarchy and partial naming. Keep presentation changes close to templates and shared theme helpers.

### Plugins, apps, and modules

Add behavior at the platform extension seam. Keep migrations, seed data, activation steps, registration, and configuration explicit and versioned.

### Admin and editor UX

Align forms with the stored content model. Preserve validation, CSRF or equivalent safeguards, permissions, previews, and publish-state behavior.

### Media and uploads

Use a dedicated upload path for authored media. Keep decorative imagery in the active theme folder. Default to conventional locations such as `uploads/` for authored media and `img/` for theme assets unless the platform dictates another convention. Expose configurable media directories with safe fallbacks.

### Content models and migrations

Distinguish pages, posts, products, entries, collections, taxonomies, and settings. Prefer migration files or exportable schema definitions over ad hoc runtime mutations.

### Markdown, HTML, and static export

Decide whether markdown is authored input, intermediate content, or build output before changing renderers. Pair renderer changes with preview or validation when feasible.

## Owning seam checklist

- Runtime bootstrap and request routing.
- Admin or editor controllers and view templates.
- Theme loading, template hierarchy, shared template helpers, sections, and partials.
- Repositories, models, schemas, migrations, or export definitions for content, taxonomy, and settings.
- Markdown or content transformation utilities.
- Static export, deploy, or render pipeline entry points.

## Gotchas

- **Do not store important metadata only in HTML**: slugs, SEO, taxonomy, and canonical data need structured fields.
- **Do not mix upload and theme asset folders**: authored media must survive theme replacement.
- **Do not patch generated output first**: find the source template, schema, or export step that owns it.

## Progressive disclosure and bundled resources

- `references/cms-platform-workflows.md`: compact mapping of common CMS platforms, extension surfaces, and media conventions.

CMS vocabulary to preserve in analysis: `self-hosted`, `hybrid/headless`, `static-exported`, `schema/migration`, `user-uploaded`, `theme-owned`, `author-facing`, `first-class`, and `non-trivial`.

## Output template

```markdown
## CMS change result

**Status:** complete | needs platform access | blocked
**Platform:** `<CMS or category>`
**Owning seam:** `<theme/plugin/module/editor/content model/media/export>`

### Changes
| Area | File or setting | Action | Validation |
| --- | --- | --- | --- |
| `<area>` | `<path or admin setting>` | `<change made>` | `<editor/render/build check>` |

### Notes
- Authored content boundary: `<preserved or changed intentionally>`
- Media handling: `<uploads/theme assets/configurable path>`
```

## Quality gate

- [ ] The concrete CMS platform or platform category was identified.
- [ ] The owning seam was located before editing.
- [ ] Authored content, generated output, and code-owned assets were kept distinct.
- [ ] Theme, plugin, module, app, section, or template conventions were preserved.
- [ ] Editor/admin behavior and final rendered output were both considered.
- [ ] Media paths used safe defaults such as `uploads/` and `img/` only when compatible with the platform.
- [ ] Static export changes validated permalinks and asset paths when applicable.
