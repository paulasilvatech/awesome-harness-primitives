---
name: e2e-fabric-cost-estimation
description: >
  Estimate Microsoft Fabric capacity costs before migration by analyzing existing workload
  profiles (Spark, SQL, Power BI, Real-Time Intelligence) and recommending optimal SKU sizing,
  billing modes, and Reserved Instance strategies. Use when the user wants to:
  (1) estimate Fabric costs for a migration, (2) size a Fabric capacity SKU,
  (3) compare Fabric pricing tiers, (4) calculate storage/compute/network costs,
  (5) recommend Reserved vs. Pay-As-You-Go vs. Autoscale billing.
  Trigger phrases are scoped to Fabric capacity cost/sizing to avoid over-routing on generic
  cost, migration, or connection questions.
  Triggers: "estimate fabric cost", "fabric capacity sizing", "fabric sku recommendation",
  "fabric cost estimate", "fabric reserved instance", "fabric capacity pay-as-you-go",
  "fabric autoscale billing".
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: e2e-fabric-cost-estimation` (`az rest`: `--headers "x-ms-fabric-skill=e2e-fabric-cost-estimation"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering
> 3. **Pricing is region-specific.** Always resolve the capacity's Azure region (via the Fabric REST `GET /v1/capacities`, which returns `region`/`sku`/`state`, or via ARM) or ask the user *before* any price lookup, and state the region with every quoted figure.

> **🔴 MANDATORY LIVE-PRICING FETCH — whenever your answer contains a dollar figure.**
> Before presenting **any** dollar amount, cost, break-even point, billing-mode comparison, RI-vs-PAYG analysis, migration cost, or cost worksheet, you **must** run a shell command (`bash`/`powershell`) that calls the Azure Retail Prices API at `https://prices.azure.com/api/retail/prices`. This applies without exception to every *priced* answer — Databricks/Synapse migration cost, **Autoscale vs. base-SKU break-even**, RI-vs-PAYG break-even, cost worksheets, and billing-mode strategy. Fetch the live per-CU-hour PAYG rate (`priceType eq 'Consumption'`, `* Capacity Usage CU` meters), the reservation term totals, and the `autoscale for Spark Capacity Usage CU` rate **first**, then compute. Never answer a priced question from memorized or hardcoded rates, and never reason about break-even purely from formulas. If the meter lookup returns no rows, surface that to the user — **never** silently fall back to a hardcoded rate (e.g., do not assume `$0.18/CU-hr` for Autoscale; the Autoscale meter is a distinct rate that must be fetched).
> **Exception — pure capacity sizing:** a question answered purely in **capacity units** with *no dollar figure* (e.g., "which SKU fits 80 CUs?" or "how many CUs does a P2 map to?") is CU math, not pricing, and does not require a fetch. The moment you attach a dollar amount to that sizing answer, the fetch becomes mandatory.

> **🟠 CLARIFY FIRST, THEN ACT — do not assume defaults.**
> A priced request needs two inputs before you can fetch or compute: the **Azure region** and the **workload profile** (e.g. CU-hours/day, node/job details, or the source cluster sizes for a migration). If **either** is missing, your **first** response must **ask the user for the missing input(s) and STOP** — do **not** pick a default region (never assume `East US` or any other region to "get started"), do **not** call the pricing API, and do **not** produce estimates from assumed values. Only after the user supplies the missing inputs do you fetch live prices and compute. Asking is the correct behavior even though the mandatory-fetch rule applies to the *eventual* priced answer.

> **🔴 AUTOSCALE RATE IS A DISTINCT METER — never reuse the base/PAYG rate for it.**
> The `autoscale for Spark Capacity Usage CU` meter is a **separate** price from the base `* Capacity Usage CU` PAYG rate. You **must** fetch it with its own API call and read the returned `retailPrice`. It is a correctness bug to assign the base/PAYG rate (or a memorized figure such as `0.18`) to an autoscale variable — e.g. `autoscaleRate = paygRate` or `autoscaleRate = 0.18` is **forbidden**. If the autoscale meter lookup returns no rows, list all Fabric Spark meters for the region and surface that to the user; never substitute the base rate.

# Fabric Cost Estimation

## Prerequisite Knowledge

- [COMMON-CORE.md](../../common/COMMON-CORE.md) — Fabric topology, capacity concepts, authentication & token audiences
- [COMMON-CLI.md](../../common/COMMON-CLI.md) — CLI patterns for capacity discovery, authentication recipes (`az login`, token acquisition)

---

## Table of Contents

| Topic | Section |
|---|---|
| Fabric Billing Model Overview | [§ Billing Model](#fabric-billing-model) |
| Capacity Unit (CU) Reference | [§ CU Reference](#capacity-unit-reference) |
| Workload Cost Estimation | [§ Workload Estimation](#workload-cost-estimation) |
| Storage Pricing | [§ Storage](#storage-pricing) |
| Network Pricing | [§ Network](#network-egress-pricing) |
| Billing Mode Strategy | [§ Billing Strategy](#billing-mode-strategy) |
| SKU Sizing Decision Tree | [§ SKU Sizing](#sku-sizing-decision-tree) |
| Migration Cost Worksheet | [§ Worksheet](#migration-cost-worksheet) |
| Pricing API Reference | [pricing-api-reference.md](resources/pricing-api-reference.md) |
| Must / Prefer / Avoid | [§ Must / Prefer / Avoid](#must--prefer--avoid) |
---

## Fabric Billing Model

Microsoft Fabric uses a **unified capacity model** where all workloads share a pool of **Capacity Units (CUs)**. Understanding the billing dimensions:

| Dimension | Description | Billing Mechanism |
|---|---|---|
| **Compute (CU-seconds)** | Processing power consumed by queries, Spark jobs, pipelines | CU consumption against capacity SKU |
| **Storage (GB/month)** | OneLake storage for Delta tables, Files, shortcuts | Per-GB monthly rate |
| **Network egress (GB)** | Data leaving Azure region | Per-GB egress charges |
| **Capacity reservation** | Base SKU commitment (F2–F8192) | Monthly or annual commitment |

### Billing Modes

| Mode | Description | Best For |
|---|---|---|
| **Reserved Instance (RI)** | 1-year or 3-year commitment; significant discount (compute from live API) | Steady-state base load |
| **Pay-As-You-Go (PAYG)** | Hourly billing; no commitment; full list price | Testing, unpredictable workloads |
| **Autoscale Billing for Spark** | Opt-in serverless model; Spark jobs offloaded from capacity and billed per Spark CU-hour. Bursting & smoothing disabled for Spark; does not consume capacity CUs | Isolating variable Spark spend from steady-state capacity |
| **Fabric Trial** | Trial capacity (size varies by tenant/eligibility — commonly up to F64 for 60 days); verify current trial terms before use; never size production from it | Evaluation only |

### Capacity SKU Tiers — Live Pricing Lookup

**Do NOT use hardcoded prices.** Always fetch current pricing from the Azure Retail Prices API at runtime.

#### Step 1: Detect Customer Region

If the customer already has a Fabric capacity, get its region, SKU, and state from the core Fabric REST API — `GET https://api.fabric.microsoft.com/v1/capacities` returns `region`, `sku`, and `state` per capacity. Azure Resource Manager (`az resource list`) is an equivalent fallback; only the Fabric **Admin** API (`/v1/admin/capacities`) omits region. See the templates in [`resources/pricing-api-reference.md`](resources/pricing-api-reference.md#3-fabric-capacity-discovery-fabric-rest--arm).

If no capacity exists yet, ask the user which Azure region they plan to deploy in.

#### Step 2: Fetch Live Fabric Pricing

Query the **Azure Retail Prices API** (public, no auth required). **For every priced question — including Autoscale-vs-base break-even and billing-mode (PAYG/RI/pause-resume) strategy — your first action must be to actually run this fetch in a shell (`bash`/`powershell`) before any calculation.** Do not reason about break-even or billing trade-offs from formulas alone; run the command, then compute from the returned `retailPrice` rows:

```bash
curl -s "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&\$filter=serviceName%20eq%20'Microsoft%20Fabric'%20and%20armRegionName%20eq%20'<region>'" | jq '.Items[] | {meterName, retailPrice, unitOfMeasure, type, reservationTerm}'
```

Use the reference template in [`resources/pricing-api-reference.md`](resources/pricing-api-reference.md#pagination) to paginate `NextPageLink` results, then filter to the **Fabric capacity meters** for the selected region. The Retail Prices API does **not** return one row per F-SKU — matching `^F\d+` against `skuName`/`armSkuName` returns nothing. **PAYG** per-CU-hour is now billed on per-workload Consumption meters whose `meterName` ends in `Capacity Usage CU` (`priceType eq 'Consumption'`, `unitOfMeasure eq '1 Hour'`); take the **modal** `retailPrice` across them for the base compute rate (a low, per-CU-hour figure — always use the value the API returns; do **not** copy any illustrative number from this skill). **Reservations** come from `meterName eq 'Fabric Capacity CU'` (the legacy flat meter is now reservation-only). Read the per-CU rates from those rows.

#### Step 3: Build the Pricing Table

The API gives you a **per-CU rate**, not per-SKU prices. Build the per-SKU table by multiplying that per-CU rate by each SKU's CU count from the documented SKU→CU map (`F`*n* = *n* CUs, e.g. F64 = 64, F128 = 128, F256 = 256, F512 = 512, F1024 = 1024, F2048 = 2048, F4096 = 4096, F8192 = 8192).

Convert each `reservationTerm` bucket to a **monthly** figure correctly (the reservation rows are **term totals**, not hourly rates):

- **PAYG monthly** = `consumptionCuHourRate × skuCUs × 730` (Consumption row, `priceType eq 'Consumption'`, `meterName` like `* Capacity Usage CU`)
- **1-Year RI monthly** = `reservationRetailPrice × skuCUs ÷ 12` (do **not** multiply by 730)
- **3-Year RI monthly** = `reservationRetailPrice × skuCUs ÷ 36`

See the monthly conversion guidance in [`resources/pricing-api-reference.md`](resources/pricing-api-reference.md#monthly-cost-calculation).

#### Step 4: Present to User

Present the pricing table with the region explicitly stated:

```text
Fabric Capacity Pricing — Region: [detected_region] (live as of [today's date])

| SKU | CUs | Monthly PAYG | 1-Year RI | 3-Year RI | RI Savings |
|-----|-----|-------------|-----------|-----------|------------|
| F4  | 4   | $[live]     | $[live]   | $[live]   | [calc]%    |
| ... | ... | ...         | ...       | ...       | ...        |

Source: Azure Retail Prices API (prices.azure.com)
```

> **IMPORTANT**: If the API is unreachable, inform the user and direct them to the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/). Never fall back to hardcoded prices — they go stale.

---

## Capacity Unit Reference

### CU Consumption by Workload

| Workload | CU Consumption Model | Key Metric |
|---|---|---|
| **Spark** (notebooks, SJD) | CU-seconds during active Spark session | vCores × duration |
| **SQL DW** (warehouse queries) | CU-seconds per query | Query complexity × data scanned |
| **Power BI** (semantic models, reports) | CU-seconds per query/refresh | Dataset size, refresh frequency, DAX complexity |
| **Data Pipelines** | CU-seconds per activity execution | Activity type, data volume moved |
| **Eventhouse / KQL** | CU-seconds per query + ingestion | Ingestion rate, query frequency |
| **Dataflows Gen2** | CU-seconds per refresh | Transform complexity, data volume |
| **OneLake** | Storage only (no CU for at-rest) | GB stored |

### Spark CU Mapping (Critical for Migration)

> **Documented conversion**: **1 Fabric CU = 2 Spark vCores** ([Fabric Spark concurrency limits](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-job-concurrency-and-queueing)). So a node's CU equivalent is `vCores ÷ 2`. The vCore counts below are pool node defaults; always validate effective consumption via a pilot before committing to SKU sizing.

| Spark Pool Node Size | vCores | Memory | CU Equivalent per Node (vCores ÷ 2) |
|---|---|---|---|
| Small | 4 vCores | 32 GB | 2 CUs |
| Medium | 8 vCores | 64 GB | 4 CUs |
| Large | 16 vCores | 128 GB | 8 CUs |
| X-Large | 32 vCores | 256 GB | 16 CUs |
| XX-Large | 64 vCores | 512 GB | 32 CUs |

An F64 capacity provides 128 Spark vCores at the base, burstable up to 3× (384 vCores) via Spark bursting on the standard (capacity-billed) model.

**Spark billing has two distinct models** — keep them separate:

1. **Standard (capacity-billed) Spark**: Spark jobs consume CUs from the capacity SKU. Bursting (up to 3×) and smoothing apply. CU-hours consumed = `nodes × CU-per-node × active-seconds / 3600`, billed against the capacity.
2. **Autoscale Billing for Spark (opt-in, serverless)**: A separate billing model where Spark jobs are **offloaded from the capacity** and billed per Spark CU-hour at the `autoscale for Spark Capacity Usage CU` meter. Under this model Spark jobs do **not** consume capacity CUs, and **bursting and smoothing are disabled for Spark**. You set a max Spark CU ceiling; only active session time is billed. Use it to isolate variable Spark spend from the steady-state capacity — it is **not** a "burst above base capacity" on the same SKU.

### Databricks to Fabric Spark Mapping

> **⚠️ Unvalidated heuristic**: These mappings are approximate and not officially documented by Microsoft. Validate via a pilot workload before committing to capacity sizing.

| Databricks Cluster Config | Fabric Equivalent | CU Estimation |
|---|---|---|
| 2× Standard_D4ds_v5 (4 vCores each) | 2× Small nodes | ~4 CUs peak |
| 4× Standard_D8ds_v5 (8 vCores each) | 4× Medium nodes | ~16 CUs peak |
| 8× Standard_D16s_v5 (16 vCores each) | 8× Large nodes | ~64 CUs peak |
| Autoscale 2–10 workers (D4s) | Autoscale 2–10 Small nodes | ~4–20 CUs burst |

---

## Workload Cost Estimation

### Step 0: Detect Current Spend (Source Platform)

Before estimating Fabric costs, pull the customer's actual current spend using Azure Cost Management. Use the query templates and CLI pattern from [`resources/pricing-api-reference.md § Azure Cost Management API`](resources/pricing-api-reference.md#2-azure-cost-management-api-auth-required):

- **Last month by service** (group by `ServiceName`, filter to Databricks / Synapse / HDInsight / Power BI / Microsoft Fabric): establishes the per-product baseline
- **Daily trend** (granularity `Daily`, group by `ServiceName`): reveals peak days, which map to peak CU demand

Parse the response to extract:
- **Total last-month spend** by service (Databricks, Synapse, HDInsight, Power BI)
- **Resource breakdown** (compute vs. storage vs. networking)
- **Peak vs. average** daily cost patterns

#### Non-Azure Source Platforms (AWS, GCP, Databricks, Snowflake, Teradata)

When the source is not on Azure, pull current spend live from that platform — **never hardcode or guess source-side prices**. Prefer the customer's **actual billing/consumption**; use a public list-price API only where one exists; otherwise use the official pricing page or invoice and state the source and date. See [`resources/pricing-api-reference.md § Source Platform Pricing (Multi-Cloud)`](resources/pricing-api-reference.md#4-source-platform-pricing-multi-cloud) for verified endpoints (AWS Price List, GCP Cloud Billing Catalog) and the actual-usage queries for Databricks/Snowflake.

#### Databricks-Specific: Get Cluster Utilization

See [pricing-api-reference.md § Databricks Clusters API](resources/pricing-api-reference.md#databricks-clusters-api). Obtain a token per [COMMON-CLI.md](../../common/COMMON-CLI.md) and call `GET /api/2.0/clusters/list`. Key fields: `cluster_name`, `node_type_id`, `num_workers`, `autoscale`.

#### Synapse-Specific: Get Pool Configuration

See [pricing-api-reference.md § Synapse Pools](resources/pricing-api-reference.md#synapse-pools) for `az synapse sql pool` and `az synapse spark pool` CLI commands.

### Step 1: Profile Existing Workloads

Gather these metrics from the source platform:

| Source Platform | Metrics to Collect | Where to Find |
|---|---|---|
| **Databricks** | Cluster hours/day, DBU consumption, worker count, node types | Cluster metrics, billing console |
| **Synapse Spark** | Pool hours, node count, node size | Synapse Studio → Monitor → Apache Spark pools |
| **Synapse SQL** | DWU-hours/day, query count, data scanned | DMVs, Azure Monitor |
| **Azure SQL/SQLDB** | DTU/vCore hours, query patterns | Performance Insights |
| **Power BI Premium** | P-SKU size, refresh frequency, user count | Power BI Admin portal |
| **HDInsight** | VM hours, cluster size, HDFS storage | Azure billing |
| **AWS Redshift / EMR** | Node type, node count, cluster hours, storage GB | AWS Cost Explorer; cluster config via AWS CLI |
| **Google BigQuery / Dataproc** | Slots or on-demand TB scanned; Dataproc vCPU-hours | Cloud Billing export; GCP console |
| **Snowflake** | Warehouse size, credits consumed/day, storage TB | `ACCOUNT_USAGE.METERING_DAILY_HISTORY` |
| **Teradata Vantage** | Node/AMP count, TCore, storage; or marketplace metered units | Customer invoice / cloud marketplace metering |

### Step 2: Map to Fabric CU Demand

**Spark workloads** (most common migration scenario):

```text
Daily CU demand = Σ (job_duration_hours × nodes × CU_per_node)
                  where CU_per_node = node_vCores ÷ 2

Example:
- 3 Spark jobs/day
- Job 1: 2 hours × 4 Medium nodes (4 CU each) = 2 × 4 × 4 = 32 CU-hours
- Job 2: 1 hour × 2 Small nodes (2 CU each) = 1 × 2 × 2 = 4 CU-hours
- Job 3: 0.5 hours × 8 Large nodes (8 CU each) = 0.5 × 8 × 8 = 32 CU-hours
- Total daily: 68 CU-hours
- Peak concurrent: 32 CUs (Job 1 or Job 3)
```

**SQL warehouse workloads** (Synapse Dedicated SQL / DW):

Do **not** size from a DWU-to-CU formula — Microsoft publishes no official conversion, so any `DWU ÷ 2` number is non-actionable for a committed SKU. Instead, drive the estimate from the customer's **actual billing signal** and validate with a pilot:

```text
Workflow (measured, not heuristic):
1. Pull the customer's real DWU-hours/day from their Synapse invoice line
   or Azure Cost Management (Meter: "cDWU" / "Compute"), not from peak DWU.
2. Run a representative workload on the smallest candidate Fabric F-SKU and
   read measured CU-seconds from the Capacity Metrics app (see § Validation).
3. Scale that measured CU/DWU-hour ratio to the customer's total DWU-hours,
   then feed the resulting CU demand into the live-API SKU pricing lookup.
4. Present the number as pilot-validated, never as a formula output.
```

> **⚠️ No committed sizing without a pilot.** If a pilot is not yet possible, surface DWU-hours as an *input to be measured* and mark the estimate as blocked on pilot data — do not emit a DWU ÷ 2 CU figure as a deliverable.

**Power BI workloads**:

```text
CU demand ≈ P-SKU CU equivalent × utilization%

P1 = 64 CUs (F64), P2 = 128 CUs (F128), P3 = 256 CUs (F256), P4 = 512 CUs (F512), P5 = 1024 CUs (F1024)
EM1/A1 = 8 CUs (F8), EM2/A2 = 16 CUs (F16), EM3/A3 = 32 CUs (F32)

Example — single Power BI P-SKU, like-for-like migration:
- P2 at 70% avg utilization, 15 refreshes/day
- P2 direct equivalent = 128 CUs (F128)
- Effective sustained demand: 128 × 0.70 ≈ 90 CUs. Refresh bursts are short and
  absorbed by capacity smoothing, so the sustained concurrent demand stays ~90 CUs.
- Apply the 1.2× safety factor to the *demand* (NOT the source nameplate):
  90 × 1.2 = 108 CUs → round up to next tier → **F128**
- F128 is the direct P-SKU equivalent and already provides headroom over a
  sub-100% workload. Do NOT multiply the source P-SKU's *rated* nameplate
  (128) by the safety factor — the nameplate already exceeds the utilized
  demand, so 128 × 1.2 → F256 double-counts headroom and over-provisions.
```

### Step 3: Aggregate and Size

```text
Sized CU = max over time of (Σ concurrent CU across all workloads in that window) + headroom
           (workloads share one capacity; size to the worst-case *concurrent sum*,
            NOT max(individual workload peaks) — peaks in different workloads can coincide)

Build a time-bucketed demand curve (e.g., hourly) summing Spark + SQL + PBI + Pipelines
CU in each bucket, then take the maximum bucket.

Recommended SKU = next SKU above (max_concurrent_CU × 1.2 safety factor)
  where max_concurrent_CU is the worst-case *effective/measured* concurrent CU
  DEMAND (already utilization-adjusted) — NOT a source SKU's rated nameplate.
  For a single Power BI P-SKU like-for-like migration, the recommendation is the
  direct CU-equivalent tier (P1→F64, P2→F128, P3→F256); do not inflate it further.

Two billing options for Spark:
  A) Standard (capacity-billed): include Spark CU in the concurrent sum above (one SKU).
  B) Autoscale Billing for Spark: size the base SKU for SQL + PBI + Pipelines only;
     Spark is offloaded and billed separately (does not consume capacity CUs).
```

Note: capacity smoothing redistributes *short* bursts (interactive ~5–64 min, background up to 24 h) but does not lower the steady-state concurrent sum — size for the sustained concurrent demand.

---

## Storage Pricing

### Live Lookup: OneLake Storage Rate

Fetch the OneLake storage rate for the customer's region from the Azure Retail Prices API. OneLake storage is **tiered** — there is no single `OneLake Storage` meter (that filter returns zero rows). Use the tiered meter names and pick the tier matching the data's access pattern: `OneLake Storage Hot Data Stored`, `OneLake Storage Cool Data Stored`, `OneLake Storage Cold Data Stored`, and `Storage Mirroring Data Stored` for mirrored replicas (filter: `serviceName eq 'Microsoft Fabric' and armRegionName eq '<region>'`, ignore rows with a `reservationTerm`). If a filter returns zero rows, list all Fabric storage meters for the region and surface them to the user — never silently use a hardcoded rate. See the runnable template in [`resources/pricing-api-reference.md`](resources/pricing-api-reference.md#storage-egress-and-serverless-rate-lookups).

### Storage Types and Pricing Model

| Storage Type | Pricing Lookup Filter | Notes |
|---|---|---|
| **OneLake (managed Delta/Parquet)** | `meterName eq 'OneLake Storage Hot Data Stored'` (or Cool/Cold) | Primary Fabric storage; tiered by access pattern |
| **OneLake Shortcuts (no copy)** | $0 (shortcut metadata only) | Source storage fees still apply |
| **ADLS Gen2 (source, via shortcut)** | `serviceName eq 'Storage' and skuName eq 'Hot LRS'` | Existing storage; no duplication |
| **Mirroring storage** | `meterName eq 'Storage Mirroring Data Stored'` | Delta replica in OneLake |

### Estimating Storage from Existing Platforms

| Source | Metric | Fabric Equivalent |
|---|---|---|
| Databricks DBFS / managed tables | Total Delta table size (GB) | Same size in OneLake Tables/ |
| Synapse Spark managed tables | ADLS Gen2 synfs container size | Migrate or shortcut; same size |
| Synapse SQL DW storage | `DBCC PDW_SHOWSPACEUSED` | Approximately same (Delta format) |
| Power BI datasets | Model size (compressed, in-memory) | Dataset import = compressed × 2–4 for uncompressed Delta |
| HDInsight HDFS | HDFS `du` output | Convert to Delta; typically 30–60% compression vs raw |

---

## Network Egress Pricing

### Live Lookup: Egress Rates

Fetch bandwidth/egress rates for the customer's region using filter `serviceName eq 'Bandwidth' and armRegionName eq '<region>' and meterName eq 'Standard Data Transfer Out'` (ignore rows with a `reservationTerm`). See the runnable template in [`resources/pricing-api-reference.md`](resources/pricing-api-reference.md#storage-egress-and-serverless-rate-lookups).

### Egress Cost Model

Azure egress is **tiered**, and the source of the data changes which meter applies. Never apply a single flat per-GB rate — resolve the tier and source first, then look up the live rate.

| Scenario | Pricing Source | Mitigation |
|---|---|---|
| Same region (intra-region) | Free | Keep capacity and storage co-located |
| First tier of internet egress | Bandwidth API: first 100 GB/month is free (`meterName eq 'Standard Data Transfer Out'`), then tiered | Batch small transfers under the free allotment |
| Internet egress (above free tier) | Bandwidth API: tiered by monthly volume — rate steps down as GB rise | Minimize public downloads; price each tier band separately |
| Cross-region (inter-region) | Bandwidth API: `meterName eq 'Inter Region Data Transfer Out'` | Use OneLake regional shortcuts |
| Cross-cloud source (AWS/GCP → Fabric) | **Source cloud's** egress meter (AWS Data Transfer Out / GCP Network Egress), not Azure | Stage via same-cloud shortcut; egress billed by the origin cloud |
| Private Link / Private Endpoint | Standard egress **plus** the PE hourly fee **plus** per-GB PE data-processing charge | Use for compliance; budget all three components |

**Migration egress estimate**: For a one-time migration, split the moved volume across the applicable tier bands (free → tier 1 → tier 2 …) at the live per-tier rate, and add the **source cloud's** egress cost when migrating from AWS/GCP. Same-region intra-Azure movement: $0.

---

## Billing Mode Strategy

### Decision Framework

```text
┌─────────────────────────────────────────────────────────────┐
│ Is the workload Spark-heavy (>50% of CU demand)?            │
│                                                             │
│ YES → Consider Autoscale Billing for Spark (offloads Spark  │
│       from capacity, billed separately) + Reserved Instance │
│       sized for the non-Spark base (SQL + PBI + Pipelines). │
│       Alternative: one capacity-billed SKU sized for the    │
│       full concurrent sum if you prefer a single bill.      │
│                                                             │
│ NO → Is demand predictable and steady?                     │
│      YES → Reserved Instance (1-year or 3-year)            │
│      NO  → Pay-As-You-Go (for evaluation period)          │
│            then reassess after 30 days of metrics          │
│                                                             │
│ Intermittent (dev/test, scheduled batch windows)?          │
│   → Pause/resume the capacity (billing stops while paused) │
│     instead of, or combined with, PAYG.                    │
└─────────────────────────────────────────────────────────────┘
```

### Spark-Heavy Workloads: Autoscale Billing for Spark vs. Standard Capacity

Spark has **two distinct billing models** — choose one, they are not additive on the same Spark job:

- **Standard (capacity-billed)**: Spark consumes CUs from the capacity SKU (with 3× bursting and smoothing). Size one SKU to cover the concurrent CU sum of *all* workloads (SQL + PBI + Pipelines + Spark) over time.
- **Autoscale Billing for Spark (opt-in serverless)**: Spark jobs are **offloaded from the capacity** and billed separately per Spark CU-hour at the `autoscale for Spark Capacity Usage CU` meter. Bursting and smoothing are **disabled** for Spark, and these jobs do **not** consume capacity CUs. This lets you size the base capacity for non-Spark steady-state (SQL DW + Power BI + Pipelines) and pay for Spark independently with a max Spark CU ceiling.

Fetch the autoscale Spark rate (`$/CU-hour`) live — **do not reuse the base/PAYG rate and never hardcode a value.** Your first action for any autoscale/break-even question must be to run this fetch in a shell and read the `retailPrice` the API returns:

```bash
curl -s "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&\$filter=serviceName%20eq%20'Microsoft%20Fabric'%20and%20armRegionName%20eq%20'<region>'%20and%20meterName%20eq%20'autoscale%20for%20Spark%20Capacity%20Usage%20CU'" | jq '.Items[] | select(.reservationTerm == null) | {meterName, retailPrice, unitOfMeasure, armRegionName}'
```

Use the `retailPrice` value from the returned row for the autoscale rate. If no row is returned for the region, list all Fabric Spark meters for the region and surface them — do **not** assume, copy, or reuse the base rate. See the runnable template in [`resources/pricing-api-reference.md`](resources/pricing-api-reference.md#storage-egress-and-serverless-rate-lookups).

**Estimation formula** (Autoscale Billing model, using live rates):

```text
Example (fill in live prices from API):
- SQL DW peak: 16 CUs
- Power BI peak: 8 CUs
- Spark peak: 64 CUs (but only 4 hours/day)
- Pipelines: 4 CUs

Base capacity (standard, capacity-billed): sized for SQL + PBI + Pipelines = 16 + 8 + 4 = 28 CUs raw
  → apply 1.2× safety: 28 × 1.2 = 33.6 CUs → round up to next tier → **F64**
  Monthly cost: [look up F64 1-Year RI rate from API, amortized ÷ 12]

Spark (Autoscale Billing, offloaded from capacity):
  64 CU × 4 hours/day × 30 days = 7,680 CU-hours/month
  Cost: 7,680 × [live 'autoscale for Spark Capacity Usage CU' rate from API]

Total: [base RI ÷ 12] + [Spark autoscale] + [storage] + [egress]
Compare vs. current spend from Cost Management API above.
```

### Reserved Instance vs. PAYG Break-Even

Do **not** rely on static utilization thresholds. Compute the break-even point from **live** pricing for the specific SKU and region:

```text
monthlyAmortizedReservationCost = skuCUs × reservationRetailPrice ÷ (12 for 1-yr | 36 for 3-yr)
paygMonthlyAtFullUse            = skuCUs × paygCuHourRate × 730
breakEvenHoursPerMonth          = monthlyAmortizedReservationCost ÷ (skuCUs × paygCuHourRate)

→ If expected billed hours/month > breakEvenHoursPerMonth, the RI wins.
→ Express RI savings as (paygMonthlyAtFullUse − monthlyAmortizedReservationCost) ÷ paygMonthlyAtFullUse.
```

Both `reservationRetailPrice` (term total) and `paygCuHourRate` (`priceType eq 'Consumption'`, from the `* Capacity Usage CU` meters) come from the Retail Prices API. For highly variable / seasonal demand, pair a smaller RI base with PAYG or Autoscale Billing for Spark for the variable portion.

---

## SKU Sizing Decision Tree

### Input Variables

Gather from the user:

1. **Peak concurrent CU demand** across all workloads
2. **Average daily CU-hours** consumed
3. **Workload mix** (% Spark vs. SQL vs. PBI vs. other)
4. **Growth forecast** (12-month projection)
5. **Compliance requirements** (Private Link, dedicated capacity)
6. **Budget constraints** (monthly ceiling)

### Sizing Algorithm

```text
1. Build a time-bucketed concurrent-demand curve; concurrent_CU = Σ workload CU per bucket
2. peak_CU = max concurrent_CU over the curve (NOT max of individual workload peaks)
3. Pick the CU basis by billing mode (Spark is the only workload that can be offloaded):
     If using Autoscale Billing for Spark:
       basis_CU = max concurrent (SQL + PBI + Pipelines)   # Spark offloaded, billed separately
     Else (standard, capacity-billed):
       basis_CU = peak_CU                                  # Spark included in the concurrent sum
4. Apply the growth forecast to the CU DEMAND, before sizing (never to a chosen SKU —
   multiplying a SKU by a growth factor can invent a tier that does not exist):
     projected_CU = basis_CU × (1 + growth_rate)
5. Apply the 1.2x safety factor to the projected demand (BOTH billing modes, incl. the
   Autoscale base):
     sized_CU = projected_CU × 1.2
6. Round UP to the next real SKU tier. The ONLY valid Fabric capacity tiers are
   **F2, F4, F8, F16, F32, F64, F128, F256, F512, F1024, F2048, F4096, F8192**
   (CUs double at each step). There are NO in-between sizes: never name an
   interpolated tier such as F48, F96, F192, or F1500 — always snap to an
   existing tier from that list, even in comparisons, ranges, or asides.
7. Validate: chosen-SKU monthly cost ≤ budget constraint
8. If budget exceeded: recommend workload optimization or phased migration
```

### Quick-Reference SKU Selector

Feed the **sized CU** into this table — i.e. first run steps 1–5 of the Sizing Algorithm to compute `sized_CU = peak_CU × (1 + growth_rate) × 1.2`, then map that value (NOT the raw peak demand) to a tier. The safety factor and growth are already baked into the left column, so do not apply them again.

| Sized CU (after growth + 1.2× safety) | Recommended Base SKU | Notes |
|---|---|---|
| ≤ 2 CUs | F2 | Trial / very small dev |
| 3–4 CUs | F4 | Dev/test, small team |
| 5–8 CUs | F8 | Small production |
| 9–16 CUs | F16 | Medium production |
| 17–32 CUs | F32 | Standard production |
| 33–64 CUs | F64 | Large production, multiple teams |
| 65–128 CUs | F128 | Enterprise |
| 129–256 CUs | F256 | Large enterprise |
| 257–512 CUs | F512 | Very large enterprise |
| 513–1024 CUs | F1024 | Multi-team enterprise platform |
| 1025–2048 CUs | F2048 | Very large estate |
| 2049–4096 CUs | F4096 | Hyperscale estate |
| 4097–8192 CUs | F8192 | Largest single-capacity tier |
| > 8192 CUs | Multiple capacities | Discuss multi-capacity architecture / workspace partitioning |

---

## Migration Cost Worksheet

### Template: Present to User

When estimating migration costs, use live data from the APIs above. Generate a worksheet covering these key sections:

- **Header** — Customer/project name, region, pricing date, data sources
- **Current Spend** — Live monthly costs per platform (Databricks, Synapse SQL/Spark, Power BI Premium, Storage) from Cost Management API
- **Source Workload Profile** — Spark jobs/day, SQL DWU-hours/day, Power BI SKU utilization, pipeline runs, storage TB
- **Fabric CU Demand** — Peak and average CU estimates per workload type and total
- **Recommended Configuration** — Base SKU (F-tier), Spark billing mode, RI term
- **Monthly Cost Breakdown** — Capacity, Spark autoscale, storage, and network egress from live API prices
- **Savings vs. Current** — Delta and percentage change

See [`resources/cost-estimation-worksheet.md`](resources/cost-estimation-worksheet.md) for the full printable template.

---

## Must / Prefer / Avoid

### MUST DO
- **Always fetch live pricing — on both sides of the comparison.** Target (Fabric) prices come from the Azure Retail Prices API (`prices.azure.com`); source-platform prices come from that platform's live billing/price API or the customer's actual invoice. Never hardcode dollar amounts for either side.
- **Never finalize a SKU or committed cost from a heuristic conversion alone.** Treat all *cross-platform* vCore→CU and DWU→CU mappings as *pilot-validation inputs only* (the in-Fabric 1 CU = 2 Spark vCores ratio is documented, but source-engine → Fabric equivalence is not). Present heuristic-derived numbers as preliminary, and require a pilot workload (measured CU consumption from the Capacity Metrics app) before any committed sizing or RI purchase.
- **Detect the customer's region** from their existing Fabric capacity or ask explicitly — pricing varies by region
- **Pull current spend via Azure Cost Management API** when the customer has Azure subscription access — establishes the baseline for comparison
- **Always ask for source workload profile** before estimating — never assume workload sizes
- **Include all cost dimensions** — compute (CU), storage, network egress, and any premium features (Private Link, BCDR)
- **State data sources clearly** — region, currency, API query date, and link to Azure Pricing Calculator for validation
- **Account for Autoscale Billing for Spark separately** when Spark is >50% of CU demand — under that model Spark is offloaded from the capacity and billed independently; do not lump it into base capacity
- **Apply a 1.2× safety factor** to peak CU demand before selecting SKU
- **Include Reserved Instance analysis** — show PAYG vs. 1-year vs. 3-year comparison for the recommended SKU
- **Present the cost worksheet template** with all line items filled from live data

### PREFER
- **Autoscale Billing for Spark for Spark-heavy workloads** — offloads Spark from the capacity and bills it separately, avoiding over-provisioning the base SKU for bursty Spark jobs (bursting & smoothing are disabled for Spark under this model)
- **Reserved Instance base + Autoscale Billing for Spark** as the default recommendation for mixed Spark-heavy workloads
- **OneLake Shortcuts over data copy** for existing ADLS Gen2 data — avoids double storage cost
- **Co-located capacity and storage** in the same Azure region — eliminates cross-region egress
- **Phased migration** approach when budget constraints exist — start with F8/F16 and scale up
- **Monthly utilization monitoring** after migration — recommend RI only after 30+ days of actual usage data
- **Workload smoothing** in estimates — Fabric smooths interactive bursts over ~5–64 min and background jobs over up to 24 h; smoothing is **disabled for Spark under Autoscale Billing**. It redistributes bursts but does not lower steady-state concurrent demand.

### AVOID
- **Do not hardcode prices** — always use a live source (Azure Retail Prices API for Fabric; the source platform's price API or actual invoice for the current spend); hardcoded values go stale
- **Do not invent prices for platforms without a public price API** (Databricks DBU, Snowflake credits, Teradata) — use the customer's actual usage/invoice or the official pricing page, and cite it
- **Do not quote prices without stating the source and date** — always include "from Azure Retail Prices API as of [date]"
- **Do not recommend 3-year RI without established steady-state** — wait until workload patterns are proven (minimum 3 months)
- **Do not size capacity for peak Spark alone** — either include Spark in the concurrent CU sum (standard) or offload it via Autoscale Billing for Spark; base SKU covers non-Spark steady-state
- **Do not ignore Power BI CU consumption** — semantic model refreshes and interactive queries consume significant CUs
- **Do not forget network egress** for multi-region or hybrid architectures
- **Do not mix up CU and vCore** — CUs are Fabric's unified billing unit; vCores are Spark execution resources. Within Fabric Spark the vCore→CU ratio is *documented* (1 CU = 2 Spark vCores, see the Spark CU Mapping section), so Fabric pool node → CU is deterministic. What is heuristic is **cross-platform** equivalence — mapping a source engine's vCores (Databricks/Synapse/EMR) to Fabric CUs — which must be pilot-validated before committing to SKU sizing
- **Do not skip the Cost Management API check** — if the user has Azure access, always establish their current baseline spend programmatically

---

## Examples

### Example 1: Databricks Migration Cost Estimate

**User prompt**: "I have 5 Databricks Spark jobs running daily on 4×D8s_v5 clusters for ~3 hours each, plus a Power BI P1 and 2TB of Delta tables. What will this cost in Fabric?"

**Agent workflow**:
1. Detect region (ask user or check existing capacity via `GET /v1/capacities` or ARM — see [§ Fabric capacity discovery](resources/pricing-api-reference.md#3-fabric-capacity-discovery-fabric-rest--arm))
2. Pull current Databricks spend via [Cost Management API](resources/pricing-api-reference.md#2-azure-cost-management-api-auth-required)
3. Fetch live Fabric pricing using the [Retail Prices pagination pattern](resources/pricing-api-reference.md#pagination)
4. Calculate CU demand and present worksheet

**CU calculation logic**:
```text
Spark: 5 jobs × 3h × 4 nodes × 4 CU/node (D8s_v5 = 8 vCores = Medium = 4 CU) = 240 CU-hours/day
Peak concurrent (2 jobs overlap): 2 × 4 × 4 = 32 CUs → candidate for Autoscale Billing for Spark
PBI: P1 = 64 CUs (F64 equivalent) — steady-state base
Storage: 2 TB × OneLake tiered rate (from API)

Recommended config (Autoscale Billing for Spark option):
  Base: F64 (1-Year RI) — covers Power BI P1 steady-state
  Spark: Autoscale Billing — 240 CU-hours/day × 30 days × live 'autoscale for Spark Capacity Usage CU' rate
  Storage: 2 TB × 1024 GB × live OneLake Hot rate
  Total = (Base RI ÷ 12) + Spark Autoscale + Storage
```

**Price lookup**: Filter the Retail Prices API by `armSkuName eq 'Fabric_Capacity_CU_Hour'` + `armRegionName eq '<region>'` + `meterName eq 'Fabric Capacity CU'`. `reservationTerm` **is** a filterable OData field, so you can pull the 1-Year rows directly with `reservationTerm eq '1 Year'` (or read the field off each returned row) — amortize that term total ÷ 12 × 64 CUs. Use `meterName eq 'autoscale for Spark Capacity Usage CU'` for the Spark rate, and `meterName eq 'OneLake Storage Hot Data Stored'` for storage. See [pricing-api-reference.md](resources/pricing-api-reference.md) for full pagination and filter patterns.

### Example 2: Synapse SQL DW Migration

**User prompt**: "We run a Synapse DW1000c for 18 hours/day and have 5TB of warehouse data."

**Agent workflow**:
1. Get current Synapse spend via [Cost Management API](resources/pricing-api-reference.md#2-azure-cost-management-api-auth-required) (filter: `"Azure Synapse Analytics"`)
2. Fetch live Fabric pricing using the [Retail Prices pagination pattern](resources/pricing-api-reference.md#pagination) for customer's region
3. Calculate CU demand and recommend SKU

**CU calculation logic**:
```text
Sizing input: the customer's measured DWU-hours/day from their Synapse invoice
(DW1000c × 18h ≈ 18,000 DWU-hours/day) — NOT a DWU ÷ 2 CU formula.
Pilot the workload on a candidate F-SKU, read CU-seconds from Capacity Metrics,
and scale the measured CU/DWU-hour ratio to total DWU-hours.
Do NOT apply an assumed engine-efficiency discount; size from the pilot's measured CU,
not from a guessed "% less CU" factor.
Pilot-start SKU: F512 as a conservative starting tier to run the pilot on.

Pricing (from API):
  F512 PAYG monthly: paygCuHourRate × 512 CUs × 730   (priceType eq 'Consumption', '* Capacity Usage CU' meter)
  F512 1-yr RI monthly: reservationRetailPrice × 512 CUs ÷ 12   (reservation row is a TERM TOTAL, not ×730)
  Storage: 5 TB × 1024 × OneLake Hot rate

Recommendation: Start F512 PAYG → monitor 30 days → right-size down (e.g., to F256 RI) if measured CU is lower
```
