---
name: azure-pricing
description: >-
  Fetch live Azure Retail Prices API data and estimate Azure service, SKU, region, reservation, savings plan, spot, and Copilot Studio credit costs. Use when the user asks about Azure pricing, Azure costs, Azure billing, workload estimates, SKU comparison, Copilot Credits, Copilot Studio pricing, or agent usage estimation.
metadata:
  author: anthonychu
  compatibility: Requires internet access to prices.azure.com and learn.microsoft.com. No authentication needed.
  version: '1.2'
---

# Azure pricing

Fetch current Azure retail prices, normalize the user's service/SKU/region request into Azure Retail Prices API filters, calculate consumption or commitment estimates, and return a concise cost table with sources and assumptions.

## When to invoke

- "How much does a D4s v5 VM cost in West Europe?"
- "Compare Azure SKU prices across regions."
- "Estimate monthly Azure costs for this architecture."
- "What is the Copilot Studio agent cost for these users?"
- "Show reservation, savings plan, or spot pricing for this service."

## Prerequisites and context

- Use the public Azure Retail Prices API; no authentication is required.
- Use web access for Copilot Studio rates because Microsoft can change billing tables.
- Resolve human region names to `armRegionName` values; read `references/REGIONS.md` when unsure.
- Read `references/SERVICE-NAMES.md`, `references/COST-ESTIMATOR.md`, and `references/COPILOT-STUDIO-RATES.md` only when the request needs those details.

## Retail Prices API

Always call:

```http
GET https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview
```

Append `$filter` with OData syntax. Keep `api-version=2023-01-01-preview` because savings plan data appears in that version. URL-encode spaces as `%20` and quotes as `%27` when constructing a full URL such as `https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&$filter=serviceName eq 'Functions' and armRegionName eq 'eastus' and priceType eq 'Consumption'`.

| Field | Match rule | Examples |
| --- | --- | --- |
| `serviceName` | exact, case-sensitive | `Functions`, `Virtual Machines`, `Storage`, `Foundry Models`, `Azure Cosmos DB` |
| `serviceFamily` | exact, case-sensitive | `Compute`, `Storage`, `Databases`, `AI + Machine Learning` |
| `armRegionName` | exact lowercase Azure region | `eastus`, `westeurope`, `southeastasia` |
| `armSkuName` | exact ARM SKU | `Standard_D4s_v5`, `Standard_LRS` |
| `skuName` | exact or `contains` for discovery | `D4s v5` |
| `priceType` | exact | `Consumption`, `Reservation`, `DevTestConsumption` |
| `meterName` | `contains` works for partial terms | `Spot` |

Use `eq` for equality, `and` to combine predicates, and `contains(field, 'value')` for partial matches.

## Common filters

```text
serviceName eq 'Functions' and armRegionName eq 'eastus' and priceType eq 'Consumption'
armSkuName eq 'Standard_D4s_v5' and armRegionName eq 'westeurope' and priceType eq 'Consumption'
serviceName eq 'Storage' and armRegionName eq 'eastus'
armSkuName eq 'Standard_D4s_v5' and contains(meterName, 'Spot') and armRegionName eq 'eastus'
serviceName eq 'Virtual Machines' and priceType eq 'Reservation' and armRegionName eq 'eastus'
serviceName eq 'Foundry Models' and armRegionName eq 'eastus' and priceType eq 'Consumption'
serviceName eq 'Azure Cosmos DB' and armRegionName eq 'eastus' and priceType eq 'Consumption'
```

If a service name is uncertain, start with `serviceFamily` and inspect returned `serviceName` values before narrowing.

## Response fields and pricing rules

Parse the `Items` array and follow `NextPageLink` only when the first page is insufficient. Prefer rows where `isPrimaryMeterRegion` is `true` unless the user asks for non-primary meters.

| Response field | Use |
| --- | --- |
| `retailPrice`, `unitPrice`, `currencyCode` | Unit price and currency; prices are USD unless `currencyCode` is specified. |
| `unitOfMeasure` | Convert usage into billed units such as `1 Execution` or hours. |
| `serviceName`, `productName`, `skuName`, `armSkuName`, `meterName` | Identify the exact item quoted. |
| `armRegionName` | Confirm the region matched the request. |
| `priceType` | Distinguish `Consumption`, `Reservation`, and `DevTestConsumption`. |
| `savingsPlan` | Extract `unitPrice` and `term` such as `1 Year` or `3 Years`. |
| `Count`, `NextPageLink` | Detect pagination or over-broad filters. |

Supported `serviceFamily` values include `Analytics`, `Compute`, `Containers`, `Data`, `Databases`, `Developer Tools`, `Integration`, `Internet of Things`, `Management and Governance`, `Networking`, `Security`, `Storage`, `Web`, and `AI + Machine Learning`.

## Procedure

1. Identify service, SKU, region, usage quantity, period, currency, and pricing model from the user's request.
2. Ask at most one focused clarifying question only when a missing value changes the estimate materially.
3. Resolve region names such as "East US", "West Europe", and "Southeast Asia" to `eastus`, `westeurope`, and `southeastasia`.
4. Build the narrowest safe `$filter`, fetch the API URL, parse `Items`, and broaden only when results are empty.
5. Calculate monthly and annual estimates using the units and formulas in `references/COST-ESTIMATOR.md`.
6. For Copilot Studio, fetch current rates from Microsoft before calculating and use `references/COPILOT-STUDIO-RATES.md` only as fallback context.
7. Return assumptions, unit prices, estimate math, and the exact pricing source.

## Copilot Studio agent cost estimation

Use this section for Copilot Studio pricing, Copilot Credits, or agent usage costs.

| Fact | Rule |
| --- | --- |
| Credit value | `1 Copilot Credit = $0.01 USD`. |
| Pooling | Credits are pooled across the entire tenant. |
| Employee-facing agents | M365 Copilot licensed users get classic answers, generative answers, and tenant graph grounding at zero cost. |
| Overage | Overage enforcement triggers at 125% of prepaid capacity. |

Gather agent type, number of users, `interactions_per_month`, knowledge percentage, tenant graph percentage, tool calls per session, flow actions, and prompt modifier tier. Compute `total_sessions = users × interactions_per_month`, then apply current rates for knowledge, tenant graph grounding, generative answers, classic answers, agent actions, agent flows, and prompt modifiers.

Fetch these source URLs before calculating Copilot Studio billing when web access is available:

| URL | Content |
| --- | --- |
| https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management | Billing rates table, examples, and overage enforcement rules. |
| https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing | Licensing options, M365 Copilot inclusions, prepaid and pay-as-you-go context. |

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| Empty results | Remove `priceType` or `armRegionName`, then rediscover exact `serviceName` and `skuName`. |
| Wrong service name | Query by `serviceFamily` first because `serviceName` is case-sensitive. |
| Missing savings plan data | Verify `api-version=2023-01-01-preview` and inspect the `savingsPlan` array. |
| URL errors | Encode spaces as `%20`, quotes as `%27`, and keep `$filter` as a query parameter. |
| Too many results | Add `armRegionName`, `armSkuName`, `meterName`, or `priceType`. |

## Progressive disclosure and bundled resources

- `references/REGIONS.md`: Azure display names mapped to `armRegionName` values.
- `references/SERVICE-NAMES.md`: common Azure `serviceName` casing.
- `references/COST-ESTIMATOR.md`: monthly and annual estimate formulas.
- `references/COPILOT-STUDIO-RATES.md`: cached Copilot Studio billing formulas and examples.

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `'AI + Machine Learning'`
- `'Compute'`
- `'Consumption'`
- `'D4s v5'`
- `'Databases'`
- `'DevTestConsumption'`
- `'Functions'`
- `'Reservation'`
- `'Spot'`
- `'Standard_D4s_v5'`
- `'Standard_LRS'`
- `'Storage'`
- `'Virtual Machines'`
- `'eastus'`
- `'southeastasia'`
- `'westeurope'`
- `2023-01-01-preview`
- `JSON`
- `basic/standard/premium`
- `built-in`
- `by-step`
- `employee/customer`
- `interactions/month`
- `monthly/annual`
- `real-time`

## Open Horizons integration

- Scope pricing analysis to the platform objective, deployment environment, and current Horizon stage.
- Preserve Open Horizons Azure resource, region, ownership, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Azure pricing estimate — <service or workload>

**Status:** priced | estimated | blocked
**Pricing source:** <Azure Retail Prices API URL or Microsoft Copilot Studio URL>
**Assumptions:** <region, SKU, usage period, currency, and missing inputs>

| Item | Region | SKU/Meter | Price type | Unit price | Usage | Monthly estimate | Annual estimate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <service> | <armRegionName> | <skuName or meterName> | <Consumption/Reservation/SavingsPlan/Spot> | <price and unit> | <quantity> | <cost> | <cost> |

### Calculation
- <formula with numbers>

### Notes
- <primary meter, savings plan, Copilot Credit, or licensing caveat>
```

## Quality gate

- [ ] The exact API URL or Microsoft pricing URL used for the answer is reported.
- [ ] Region names were resolved to `armRegionName` values and shown in the output.
- [ ] The estimate uses `api-version=2023-01-01-preview` when querying Azure Retail Prices.
- [ ] `Items`, `NextPageLink`, `isPrimaryMeterRegion`, and `savingsPlan` were handled when present.
- [ ] Unit conversions are explicit enough for the user to audit the monthly and annual totals.
- [ ] Copilot Studio estimates fetched current Microsoft billing rates or clearly used the cached fallback.

## References

- [Azure Retail Prices API](https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview)
- [Copilot Studio requirements, messages, and management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)
- [Copilot Studio billing and licensing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing)
