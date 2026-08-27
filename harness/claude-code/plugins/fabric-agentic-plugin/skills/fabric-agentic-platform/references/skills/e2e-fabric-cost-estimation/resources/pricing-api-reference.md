# Azure Pricing API Reference

Quick reference for the APIs used by the e2e-fabric-cost-estimation skill to fetch live pricing data.

> **Authentication**: For token acquisition patterns (`az account get-access-token`, bearer token flows), see [COMMON-CLI.md](../../../common/COMMON-CLI.md). This file covers only API-specific request/response details.

---

## 1. Azure Retail Prices API (Public, No Auth)

**Base URL**: `https://prices.azure.com/api/retail/prices`

### Key Filters for Fabric

| Purpose | OData Filter |
|---|---|
| All Fabric SKUs | `serviceName eq 'Microsoft Fabric'` |
| Fabric in specific region | `serviceName eq 'Microsoft Fabric' and armRegionName eq 'eastus'` |
| Capacity PAYG (per-CU-hour) | `serviceName eq 'Microsoft Fabric' and armRegionName eq 'eastus' and priceType eq 'Consumption'`, then match `meterName` ending in `Capacity Usage CU` with `unitOfMeasure eq '1 Hour'` and no `reservationTerm` (the property is absent on Consumption rows). The base compute rate is the **modal** `retailPrice` across those rows (a low, per-CU-hour figure — always read it from the API response; never hardcode a number from this doc). The legacy flat `meterName eq 'Fabric Capacity CU'` meter is now **reservation-only** and no longer carries a Consumption row. |
| Capacity reservation (term totals) | `armSkuName eq 'Fabric_Capacity_CU_Hour' and armRegionName eq 'eastus' and meterName eq 'Fabric Capacity CU'` (rows carry `reservationTerm` '1 Year'/'3 Years') |
| OneLake storage (tiered) | `serviceName eq 'Microsoft Fabric' and armRegionName eq 'eastus'` then match `meterName` in `OneLake Storage Hot/Cool/Cold Data Stored`, `Storage Mirroring Data Stored` |
| Autoscale Billing for Spark | `serviceName eq 'Microsoft Fabric' and armRegionName eq 'eastus' and meterName eq 'autoscale for Spark Capacity Usage CU'` |
| Network egress | `serviceName eq 'Bandwidth' and armRegionName eq 'eastus'` |
| Power BI | `serviceName eq 'Power BI'` |

> **Filters are case-sensitive and exact-match.** Use `armSkuName eq 'Fabric_Capacity_CU_Hour'` for capacity pricing — don't filter capacity rates by `skuName` alone (`skuName` exists as a response field but isn't a reliable capacity-price filter on its own). Invented meter names such as `meterName eq 'OneLake Storage'` or `meterName eq 'Spark Serverless'` return **zero rows** — they are not real Fabric meter names. If any filter returns zero rows, fall back to listing **all** Fabric meters for the region (`serviceName eq 'Microsoft Fabric' and armRegionName eq '<region>'`) and surface them to the user; never silently substitute a hardcoded rate.

### Response Fields

| Field | Description | Use For |
|---|---|---|
| `skuName` | Human-readable SKU label in the response (e.g., F64) | Not a reliable capacity-price filter — use `armSkuName eq 'Fabric_Capacity_CU_Hour'` to find the Fabric capacity meter |
| `meterName` | Billing meter name | Distinguishing compute vs. storage |
| `retailPrice` | List price per unit | PAYG calculation |
| `unitOfMeasure` | How price is measured (e.g., "1 Hour") | Correct monthly calculation |
| `reservationTerm` | Absent on PAYG rows; `"1 Year"` or `"3 Years"` on Reservation rows | RI vs. PAYG comparison — Consumption/PAYG rows **omit** this property (it is absent/null, not an empty string), so test for its presence rather than `== ""` |
| `type` | Price type: `Consumption` (PAYG) or `Reservation` | Distinguishing PAYG from RI rows — the **response field** is `type`; in OData `$filter` queries use `priceType eq 'Consumption'` |
| `armRegionName` | Azure region slug | Regional pricing |
| `effectiveStartDate` | When price takes effect | Checking for recent changes |

### Pagination

The API returns up to **1,000 items per page**. Use `NextPageLink` to paginate, and add retries for transient failures / 429s.

> **PowerShell note**: `-MaximumRetryCount` / `-RetryIntervalSec` require **PowerShell 7.4+**. On Windows PowerShell 5.1 or older pwsh, replace with an explicit retry loop.
```powershell
$allItems = @()
$url = "https://prices.azure.com/api/retail/prices?`$filter=serviceName eq 'Microsoft Fabric'"
do {
    $response = Invoke-RestMethod -Uri $url -MaximumRetryCount 3 -RetryIntervalSec 5
    $allItems += $response.Items
    $url = $response.NextPageLink
} while ($url)
```

### Monthly Cost Calculation

Pick the formula by row type — **reservation rows are term totals, not hourly rates**:

```text
PAYG capacity (priceType eq 'Consumption', meterName like '* Capacity Usage CU', unit "1 Hour"):
  monthly = paygCuHourRate × skuCUs × 730
  (paygCuHourRate = modal retailPrice across the '* Capacity Usage CU' Consumption rows -- read from the API, never hardcoded)

Reservation rows (reservationTerm "1 Year"/"3 Years"):
  reservationRetailPrice is the TERM TOTAL per CU — do NOT multiply by 730.
  1-Year RI monthly = reservationRetailPrice × skuCUs ÷ 12
  3-Year RI monthly = reservationRetailPrice × skuCUs ÷ 36

Storage ("1 GB/Month" unit):  monthly = price × GB_count
Egress ("1 GB" unit):         cost    = price × GB_transferred
```

Example (live, East US): reservation rows return `retailPrice` 938.0 ("1 Year") and 2814.0 ("3 Years") per CU.
For F64 (64 CUs): 1-yr RI monthly = 938 × 64 ÷ 12; 3-yr RI monthly = 2814 × 64 ÷ 36.

### Storage, Egress, and Serverless Rate Lookups

Runnable templates for the per-component rate lookups referenced by SKILL.md. Each ignores rows that carry a `reservationTerm` (those are RI prices, not the PAYG unit rate).

**OneLake storage rate** (`$/GB/month`) — OneLake storage is **tiered**; pick the meter matching the data's access pattern (Hot/Cool/Cold), plus `Storage Mirroring Data Stored` for mirrored replicas:

```powershell
$region = "eastus"
$tier = "Hot"   # Hot | Cool | Cold
$filter = "serviceName eq 'Microsoft Fabric' and armRegionName eq '$region' and meterName eq 'OneLake Storage $tier Data Stored'"
$encodedFilter = [uri]::EscapeDataString($filter)
$url = "https://prices.azure.com/api/retail/prices?`$filter=$encodedFilter"
$storagePrice = (Invoke-RestMethod -Uri $url -MaximumRetryCount 3 -RetryIntervalSec 5).Items |
  Where-Object { -not $_.reservationTerm } |
  Select-Object -First 1 -ExpandProperty retailPrice
if (-not $storagePrice) {
  Write-Warning "No row for tier '$tier' in $region — listing all OneLake storage meters:"
  $f = "serviceName eq 'Microsoft Fabric' and armRegionName eq '$region'"
  $u = "https://prices.azure.com/api/retail/prices?`$filter=$([uri]::EscapeDataString($f))"
  (Invoke-RestMethod -Uri $u -MaximumRetryCount 3 -RetryIntervalSec 5).Items |
    Where-Object { $_.meterName -like '*Storage*Data Stored*' } |
    Select-Object meterName, retailPrice, unitOfMeasure -Unique
}
Write-Output "OneLake $tier rate: `$$storagePrice/GB/month in $region"
```

**Network egress rate**:

```powershell
$region = "eastus"
$filter = "serviceName eq 'Bandwidth' and armRegionName eq '$region' and meterName eq 'Standard Data Transfer Out'"
$encodedFilter = [uri]::EscapeDataString($filter)
$url = "https://prices.azure.com/api/retail/prices?`$filter=$encodedFilter"
$egressItems = (Invoke-RestMethod -Uri $url).Items |
  Where-Object { -not $_.reservationTerm } |
  Select-Object meterName, retailPrice, unitOfMeasure, tierMinimumUnits
```

**Autoscale Billing for Spark rate** (`$/CU-hour`) — the meter is `autoscale for Spark Capacity Usage CU` (the names `Spark Serverless` / `Capacity Unit` do **not** exist and return zero rows):

```powershell
$region = "eastus"
$filter = "serviceName eq 'Microsoft Fabric' and armRegionName eq '$region' and meterName eq 'autoscale for Spark Capacity Usage CU'"
$encodedFilter = [uri]::EscapeDataString($filter)
$url = "https://prices.azure.com/api/retail/prices?`$filter=$encodedFilter"
$sparkRate = (Invoke-RestMethod -Uri $url -MaximumRetryCount 3 -RetryIntervalSec 5).Items |
  Where-Object { -not $_.reservationTerm } | Select-Object -First 1

if (-not $sparkRate) {
    Write-Warning "No autoscale Spark meter for $region — listing all Fabric Spark/capacity meters:"
    $f = "serviceName eq 'Microsoft Fabric' and armRegionName eq '$region'"
    $u = "https://prices.azure.com/api/retail/prices?`$filter=$([uri]::EscapeDataString($f))"
    (Invoke-RestMethod -Uri $u -MaximumRetryCount 3 -RetryIntervalSec 5).Items |
      Where-Object { $_.meterName -match 'Spark|Capacity Usage CU' } |
      Select-Object meterName, retailPrice, unitOfMeasure -Unique
    return
}
Write-Output "Autoscale Spark rate: `$$($sparkRate.retailPrice)/CU-hour in $region"
```

---

## 2. Azure Cost Management API (Auth Required)

**Base URL**: `https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CostManagement/query`

**Auth**: See [COMMON-CLI.md](../../../common/COMMON-CLI.md) — use `az rest` with `--resource https://management.azure.com`

### Key Queries

#### Last Month Spend by Service

```json
{
  "type": "ActualCost",
  "timeframe": "TheLastMonth",
  "dataset": {
    "granularity": "None",
    "aggregation": {
      "totalCost": { "name": "PreTaxCost", "function": "Sum" }
    },
    "grouping": [
      { "type": "Dimension", "name": "ServiceName" },
      { "type": "Dimension", "name": "MeterCategory" }
    ]
  }
}
```

#### Daily Trend (for peak detection)

```json
{
  "type": "ActualCost",
  "timeframe": "TheLastMonth",
  "dataset": {
    "granularity": "Daily",
    "aggregation": {
      "totalCost": { "name": "PreTaxCost", "function": "Sum" }
    },
    "grouping": [{ "type": "Dimension", "name": "ServiceName" }],
    "filter": {
      "dimensions": {
        "name": "ServiceName",
        "operator": "In",
        "values": ["Azure Databricks", "Azure Synapse Analytics", "HDInsight", "Power BI"]
      }
    }
  }
}
```

#### Resource-Level Breakdown

```json
{
  "type": "ActualCost",
  "timeframe": "TheLastMonth",
  "dataset": {
    "granularity": "None",
    "aggregation": {
      "totalCost": { "name": "PreTaxCost", "function": "Sum" }
    },
    "grouping": [
      { "type": "Dimension", "name": "ResourceId" },
      { "type": "Dimension", "name": "MeterSubCategory" }
    ],
    "filter": {
      "dimensions": {
        "name": "ServiceName",
        "operator": "In",
        "values": ["Azure Databricks"]
      }
    }
  }
}
```

### CLI Pattern (PowerShell)

```powershell
# 1. Build the query body from one of the templates above
$subscriptionId = (az account show --query id -o tsv)
$body = @{
    type      = "ActualCost"
    timeframe = "TheLastMonth"
    dataset   = @{
        granularity = "None"
        aggregation = @{ totalCost = @{ name = "PreTaxCost"; function = "Sum" } }
        grouping    = @(@{ type = "Dimension"; name = "ServiceName" },
                        @{ type = "Dimension"; name = "MeterCategory" })
        filter      = @{
            dimensions = @{ name = "ServiceName"; operator = "In"
                values = @("Azure Databricks", "Azure Synapse Analytics",
                           "HDInsight", "Power BI", "Microsoft Fabric") }
        }
    }
} | ConvertTo-Json -Depth 10

# 2. Write to temp file (avoids shell-escaping issues — see COMMON-CLI.md)
$bodyFile = "$env:TEMP\cost_mgmt_body.json"
$body | Out-File -FilePath $bodyFile -Encoding utf8NoBOM

# 3. Submit query
az rest --method post `
  --url "https://management.azure.com/subscriptions/$subscriptionId/providers/Microsoft.CostManagement/query?api-version=2025-03-01" `
  --body "@$bodyFile"
```

For daily granularity (peak-day detection), swap `granularity = "None"` for `granularity = "Daily"` and adjust the `grouping`/`filter` to match the **Daily Trend** template above.

> **Large line-item exports**: The Query API is best for aggregated/grouped summaries. For full transaction-level line items (e.g., reconciling every meter), use the asynchronous **Generate Cost Details Report** operation (`.../providers/Microsoft.CostManagement/generateCostDetailsReport`) rather than the (deprecated) Usage Details list — it returns a downloadable blob and avoids paging limits.

---

## 3. Fabric capacity discovery (Fabric REST + ARM)

**Region / SKU / state — two equivalent sources; use whichever you're already authenticated for:**

### Get Capacity Details (region, SKU, state) via the Fabric REST API

The core Fabric REST endpoint `GET /v1/capacities` returns `region`, `sku`, and `state` for each capacity the principal can access (scope `Capacity.Read.All`) — so ARM is **not** the only source of region:

~~~powershell
# https://learn.microsoft.com/en-us/rest/api/fabric/core/capacities/list-capacities
az rest --method get --resource https://api.fabric.microsoft.com `
  --url "https://api.fabric.microsoft.com/v1/capacities" `
  --query "value[].{name:displayName, sku:sku, region:region, state:state}"
~~~

### Get Capacity Details (region, SKU, state) via ARM

~~~powershell
# ARM is an equivalent source for the region + Azure resource metadata
az resource list --resource-type "Microsoft.Fabric/capacities" `
  --query "[].{name:name, region:location, sku:sku.name, state:properties.state}"
~~~

**Fabric Admin API (tenant-wide inventory / admin-only operations)**
- Base URL: `https://api.fabric.microsoft.com/v1/admin/capacities`
- Auth: See [COMMON-CLI.md](../../../common/COMMON-CLI.md) — use `az rest` with `--resource https://api.fabric.microsoft.com`
- Note: unlike the core `/v1/capacities` endpoint above, the **Admin** inventory API does **not** return Azure `location`/region — use it for tenant-wide admin metadata, and resolve region via `/v1/capacities` or ARM.
---

## 4. Source Platform APIs

### Databricks Clusters API

```text
GET https://<workspace_url>/api/2.0/clusters/list
Header: Authorization: Bearer <PAT>

Response fields: cluster_name, node_type_id, num_workers, autoscale.min_workers, autoscale.max_workers
```

### Synapse Pools

```powershell
# SQL Pools
az synapse sql pool list --workspace-name <ws> --resource-group <rg> `
  --query "[].{name:name, sku:sku.name, status:status}"

# Spark Pools
az synapse spark pool list --workspace-name <ws> --resource-group <rg> `
  --query "[].{name:name, nodeSize:nodeSize, nodeCount:nodeCount, autoScale:autoScale}"
```

---

## CU Equivalence Formulas (Not Prices)

> **⚠️ Unvalidated heuristics**: These are community-derived approximations, not officially published Microsoft equivalences. The Power BI P-SKU → CU mapping is based on the [published Fabric capacity equivalents](https://learn.microsoft.com/en-us/fabric/enterprise/licenses#capacity). The Databricks/Synapse mappings are not documented by Microsoft — always validate via a pilot workload.

| Source Metric | Fabric CU Formula |
|---|---|
| Databricks vCores | `vCores ÷ 2 ≈ CU` (1 CU = 2 Spark vCores, matching this skill's Fabric mapping — unvalidated cross-cloud heuristic, confirm via pilot) |
| Synapse DWU | No official Microsoft conversion — treat DWU-hours as an **input to be pilot-validated** (see SKILL.md § SQL warehouse workloads). Do **not** use a `DWU ÷ 2` formula for committed sizing. |
| HDInsight worker vCores | `vCores ÷ 2 ≈ CU` (1 CU = 2 Spark vCores, matching this skill's Fabric mapping — unvalidated cross-cloud heuristic, confirm via pilot) |
| Power BI P1 | `64 CUs` (F64 equivalent — per Microsoft docs) |
| Power BI P2 | `128 CUs` (F128 equivalent) |
| Power BI P3 | `256 CUs` (F256 equivalent) |

> These are capacity equivalences (how much compute power), not price equivalences. Always use live prices from the Retail Prices API for dollar amounts.

---

## 5. Source Platform Pricing (Multi-Cloud)

For a **migration comparison**, the *source* platform's cost must also be live — never hardcode or guess source-side prices. Prefer the customer's **actual billing/consumption** (most accurate); fall back to a public list-price API only where one exists. Where no programmatic price API exists, use the official pricing page or the customer's invoice and **state the source and date**.

| Source platform | Live list-price API | Actual-spend source (preferred) |
|---|---|---|
| **Azure** (Synapse, HDInsight, Azure Databricks infra, Power BI) | Azure Retail Prices API — anonymous (§1) | Azure Cost Management API (§2) |
| **AWS** (Redshift, EMR, EC2, S3) | AWS Price List **Bulk** API — anonymous; or **Query** API (creds) | AWS Cost Explorer / Cost & Usage Report |
| **Databricks** (any cloud — DBU) | **No public price API** — DBU list prices on the [Databricks pricing page](https://www.databricks.com/product/pricing) | `system.billing.usage` joined with `system.billing.list_prices` (Unity Catalog system tables) + cloud infra cost |
| **Google Cloud** (BigQuery, Dataproc) | Cloud Billing **Catalog** API (API key or OAuth) | Cloud Billing BigQuery export |
| **Snowflake** | **No public price API** — credit list price is published per edition/region | `SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY` (credits) × credit price |
| **Teradata Vantage** | **No public price API** — cloud-marketplace metered rates or direct quote | Customer invoice / cloud marketplace consumption metrics |

### AWS Price List Bulk API (anonymous)

```text
# 1. Service offer index (lists every service offer file)
GET https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json

# 2. Current price file for a specific service (e.g., Redshift, EMR, EC2)
GET https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRedshift/current/index.json
```

```bash
# Query API (filterable; requires AWS credentials)
aws pricing get-products --service-code AmazonRedshift \
  --filters "Type=TERM_MATCH,Field=location,Value=US East (N. Virginia)" --region us-east-1

# Actual historical spend (requires credentials)
aws ce get-cost-and-usage --time-period Start=2025-01-01,End=2025-02-01 \
  --granularity MONTHLY --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE
```

### Google Cloud Billing Catalog API (API key or OAuth)

```text
# List billable services to find a service ID (e.g., BigQuery, Dataproc)
GET https://cloudbilling.googleapis.com/v1/services?key=<API_KEY>

# List SKUs (unit prices) for a service
GET https://cloudbilling.googleapis.com/v1/services/{serviceId}/skus?key=<API_KEY>
```

> For auth/token patterns (AWS credentials, GCP OAuth, Databricks/Snowflake tokens), see [COMMON-CLI.md](../../../common/COMMON-CLI.md). Do not embed secrets in scripts.

### Databricks & Snowflake actual usage (no list-price API)

```sql
-- Databricks (Unity Catalog system tables): actual list-priced usage
SELECT usage_date, sku_name, SUM(usage_quantity) AS dbus
FROM system.billing.usage
GROUP BY usage_date, sku_name;
-- Join system.billing.list_prices for the effective DBU rate.

-- Snowflake: actual credit consumption (apply the account's credit price)
SELECT service_type, SUM(credits_used) AS credits
FROM snowflake.account_usage.metering_daily_history
WHERE usage_date >= DATEADD('month', -1, CURRENT_DATE)
GROUP BY service_type;
```

