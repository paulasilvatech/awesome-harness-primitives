# Official icon and logo policy

Use this reference whenever a diagram depicts a Microsoft, Azure, or GitHub product or service. It distinguishes architecture icons with explicit diagram-use terms from corporate and product logos governed by stricter brand permissions.

Verification date: 2026-08-25. Recheck the relevant first-party source when this evidence is older than 90 days, a provider announces new branding, a product name or icon changed, or the requested use is outside architecture diagrams, training materials, or documentation.

## Source hierarchy

Choose assets in this order:

1. Product-family architecture icon set published by the provider with explicit terms for diagrams.
2. Official provider repository or package with a clear license covering the intended use.
3. Current corporate or product brand asset only when brand guidance permits the specific use or the user supplies permission.
4. Neutral draw.io shape with an exact text label.

Never use third-party icon aggregators, images copied from search results, reverse-engineered logos, screenshots, stale blog attachments, or unofficial redraws.

## First-party source registry

| Family | Official source | Permitted diagram use and constraints |
| --- | --- | --- |
| Azure services | [Azure Architecture Center icons](https://learn.microsoft.com/en-us/azure/architecture/icons/) | Microsoft permits copying, distributing, and displaying the supplied icons in architecture diagrams, training materials, or documentation. Do not crop, flip, rotate, distort, or use them to represent the user's product. Include the product name near the icon. |
| Microsoft Entra | [Microsoft Entra architecture icons](https://learn.microsoft.com/en-us/entra/architecture/architecture-icons) | Same architecture, training, and documentation permission. Do not use the architecture icons in marketing communications. |
| Microsoft Fabric | [Microsoft Fabric icons](https://learn.microsoft.com/en-us/fabric/fundamentals/icons) | Use product, experience, and item icons in diagrams, slide decks, training, or documentation without altering them. Label the exact product, experience, or item. |
| Power Platform | [Microsoft Power Platform icons](https://learn.microsoft.com/en-us/power-platform/guidance/icons) | Use in architecture diagrams, training materials, or documentation. Preserve the icons and use them only for the represented products. |
| Dynamics 365 | [Microsoft Dynamics 365 icons](https://learn.microsoft.com/en-us/dynamics365/get-started/icons) | Use in architecture diagrams, training materials, or documentation. Do not use removed or deprecated app icons from older packages. |
| Microsoft 365 | [Microsoft 365 architecture icons and templates](https://learn.microsoft.com/en-us/previous-versions/microsoft-365/solutions/architecture-icons-templates) | The first-party page is archived and retired. Treat it as a fallback source only, record that status, and look for a current product-specific source before use. |
| General Microsoft brand assets | [Microsoft Trademark and Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks) | Many logos, app icons, and product icons require a license. Product-family architecture terms do not grant unrestricted marketing or corporate-logo use. Block use when permission is unclear. |
| GitHub interface concepts | [GitHub Primer Octicons](https://github.com/primer/octicons) | Octicons are GitHub-built SVG interface icons and the repository code license is MIT. Use them for covered interface or workflow concepts, not as substitutes for GitHub corporate or product logos. |
| GitHub logos and product lockups | [GitHub brand logo guidance](https://brand.github.com/foundations/logo) | Use only in permitted contexts, with high contrast and secondary placement. Do not imply affiliation, use a GitHub mark as the user's logo, modify the mark, or use it without required permission. |
| GitHub Copilot | [GitHub Copilot brand guidance](https://brand.github.com/brand-identity/copilot) | Use current product lockups only when the use is permitted. The former standalone GitHub Copilot logo has been deprecated since 2025; do not reuse it. |

## Asset classification

| Diagram element | Correct asset choice |
| --- | --- |
| Named Azure, Entra, Fabric, Power Platform, Dynamics, or Microsoft 365 service | Current icon from that product family's official architecture set |
| GitHub repository, issue, pull request, branch, workflow, or code concept | Appropriate Octicon when it represents the interface concept |
| GitHub as a company, platform integration, or named product | Current permitted GitHub logo or product lockup under brand guidance |
| GitHub Copilot product | Current official GitHub Copilot lockup, never the deprecated standalone mark |
| User's application or internal service | Neutral custom container or generic symbol, not a Microsoft or GitHub product icon |
| Generic API gateway, database, queue, user, device, cloud, or internet | Neutral draw.io symbol unless a named product implements it |
| Third-party vendor product | That vendor's official current asset and terms, or a neutral labeled fallback |

## Brand integrity

- Preserve the original SVG paths, colors, view box, and aspect ratio.
- Do not crop, flip, rotate, stretch, skew, recolor, redraw, outline, add shadows, combine with other artwork, or place badges over a mark.
- Do not use a product icon as a decorative bullet, generic capability symbol, or logo for the user's system.
- Keep the exact current product or service name next to the icon.
- Keep adequate clear space and select a background that preserves contrast.
- Use containers and connectors for status, ownership, risk, and flow semantics instead of altering the icon.
- Do not imply that Microsoft, Azure, or GitHub sponsors, certifies, endorses, or owns the depicted solution.

## Acquisition and provenance record

Before embedding an official asset, capture:

| Field | Required value |
| --- | --- |
| Provider | `azure`, `microsoft`, or `github` |
| Product | Exact current product, service, experience, item, or permitted logo name |
| Source URL | First-party page or official repository URL |
| Terms URL | First-party terms, license, or brand-guidance URL |
| Retrieved | ISO date `YYYY-MM-DD` |
| Usage basis | `microsoft-architecture-terms`, `github-octicons-mit`, `github-brand-permission`, or `explicit-license` |
| SHA-256 | Hash of the exact local SVG bytes embedded in the diagram |
| Method | `embedded-svg` by default; `drawio-stencil` only after version-specific verification |

`scripts/add-icon.py` writes these values to the `mxCell`. Do not hand-edit the hash or mark an asset official without evidence.

## Safe embedding

- Download or otherwise obtain the SVG outside the script after satisfying the source terms. The helper never fetches network content.
- Keep the exact local SVG bytes and embed them as a percent-encoded data URI.
- Reject SVGs containing scripts, event handlers, foreign objects, external references, or external styles.
- Reject external image URLs in `.drawio`; they create tracking, availability, and reproducibility risks.
- Prefer embedded SVG over a built-in stencil because stencil names and artwork can vary with draw.io versions.
- If a stencil is required, record the draw.io version and visually verify it against the current official asset.

## Accessibility

- Pair every icon with a nearby text label using the exact product or service name.
- Do not use icon recognition or color as the only carrier of meaning.
- Keep labels readable at the intended publication size.
- Explain connector color, pattern, and line semantics in a legend.
- Use a high-contrast permitted logo variant; do not recolor a mark to force contrast.

## Review decision

Mark the icon review:

- `PASS` when the asset is official, permitted for the use, unmodified, labeled, self-contained, and provenance-complete.
- `BLOCKED` when permission, current asset identity, product naming, or source provenance cannot be established.
- `FAIL` when an unofficial, altered, deprecated, externally linked, misleading, or untraceable asset is present.

Use a neutral labeled fallback for a blocked asset only when the fallback cannot be mistaken for the vendor's mark.
