# Icon Catalogs and Terms of Use

Use only official icon sets, and use them within their terms. This protects the work and keeps diagrams credible.

## Azure architecture icons

- **What.** The official Azure architecture icon set, downloadable as SVG from Microsoft Learn. draw.io and diagrams.net also ship an Azure shape library built from these.
- **Terms (summary).** The icons are provided to depict Azure products and services in architecture diagrams. Do not modify, distort, or re-color them, and do not use them to imply Microsoft endorsement. Always read the current terms on the download page before use.
- **In draw.io.** Enable the Azure shape libraries (More Shapes, then Networking and Azure), or reference a shape style. The newer Azure icon styles look like `sketch=0;...;shape=mscae/...` or use the `mxgraph.azure` and `mxgraph.mscae` stencils. Verify the exact style string in your draw.io version.

## Microsoft product icons

- **What.** Official icon sets for Microsoft 365, Microsoft Entra, Dynamics 365, Power Platform, and other product families, published by Microsoft.
- **Terms (summary).** For depicting the products in diagrams and documentation; do not alter them. Follow the Microsoft trademark and brand guidelines.

## GitHub Octicons and logos

- **Octicons.** GitHub's open icon set, MIT licensed. Free to use and embed (for example repo, issue, pull request, actions, workflow marks). Source as SVG.
- **GitHub logos (mark and wordmark).** Governed by the GitHub brand and trademark guidelines. Use the official Octocat mark and the GitHub wordmark unmodified, with adequate clear space, and do not imply endorsement.

## Choosing the right mark

| Element in the diagram | Icon source |
| --- | --- |
| Azure service (Foundry, APIM, Redis, AI Search, Container Apps, AKS, Key Vault, Monitor) | Azure architecture icons |
| Microsoft product (Entra, Microsoft 365, Power Platform) | Microsoft product icons |
| GitHub platform (repos, Actions, GitHub Copilot, GitHub Models) | GitHub Octicons or GitHub logo |
| Generic concept (user, internet, database without a brand) | draw.io general shapes |

## Practical rules

- Never re-color or stretch a product icon. Color the container or the connector instead.
- Keep one icon set per product family; do not mix official and look-alike third-party icons.
- Label every icon with the exact service name so the diagram is unambiguous.
- Keep clear space around the GitHub mark per its guidelines.

## Sources

- [Azure architecture icons](https://learn.microsoft.com/azure/architecture/icons/)
- [Microsoft brand and trademark guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks)
- [GitHub Octicons](https://primer.style/octicons/)
- [GitHub logos and usage](https://github.com/logos)
- [diagrams.net Azure shapes](https://www.drawio.com/doc/faq/shapes-azure)
