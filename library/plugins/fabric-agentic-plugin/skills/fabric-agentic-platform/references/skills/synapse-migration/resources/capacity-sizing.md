# Capacity Sizing Reference

Use this table to estimate the Fabric capacity SKU needed based on current Synapse Spark pool configuration. This is a **planning reference only** — the migration workflow operates against whatever capacity is already assigned to the target workspace.

> **Note**: Fabric capacity is shared across all workload types (Spark, Warehouse, Power BI, Pipelines) in the workspace. If other workloads run on the same capacity, size up accordingly.

## Synapse Spark Pool → Fabric Capacity Mapping

| Synapse Pool Config | Total vCores | Typical Workload | Recommended Fabric SKU | Fabric CUs | Spark vCores Available |
|---|---|---|---|---|---|
| 3 Small nodes (4 vCore / 32 GB) | 12 | Dev/test, small datasets (<1 GB) | **F8** (dev) or **F16** | 8 / 16 | 8 / 16 |
| 3–5 Medium nodes (8 vCore / 64 GB) | 24–40 | Standard analytics, medium datasets | **F32** | 32 | 32 |
| 5–10 Medium nodes (8 vCore / 64 GB) | 40–80 | Production ETL, multiple concurrent jobs | **F64** | 64 | 64 |
| 3–10 Large nodes (16 vCore / 128 GB) | 48–160 | Heavy ETL, large datasets (10+ GB) | **F64** or **F128** | 64 / 128 | 64 / 128 |
| 10–20 Large nodes (16 vCore / 128 GB) | 160–320 | Enterprise workloads, many concurrent jobs | **F128** or **F256** | 128 / 256 | 128 / 256 |
| XL/XXL nodes or 20+ nodes | 200+ | Large-scale data engineering | **F256+** | 256+ | 256+ |

## Fabric Capacity SKU Quick Reference

| SKU | Capacity Units (CUs) | Max Spark vCores | Max Concurrent Spark Jobs | Burst | Typical Use |
|---|---|---|---|---|---|
| **F2** | 2 | 2 | 1 | Smoothed | Sandbox/POC only |
| **F4** | 4 | 4 | 1 | Smoothed | Individual developer |
| **F8** | 8 | 8 | 1 | Smoothed | Dev/test |
| **F16** | 16 | 16 | 1–2 | Smoothed | Small team dev |
| **F32** | 32 | 32 | 2–4 | Smoothed | Small production |
| **F64** | 64 | 64 | 4–8 | Smoothed | Standard production |
| **F128** | 128 | 128 | 8–16 | Smoothed | Enterprise production |
| **F256** | 256 | 256 | 16–32 | Smoothed | Large enterprise |
| **F512+** | 512+ | 512+ | 32+ | Smoothed | Enterprise-scale data engineering |

> Spark vCores and concurrent job limits are approximate and depend on node sizes selected in Custom Pools and current burst utilization. Fabric uses **burst and smoothing** — short spikes can exceed the CU baseline, but sustained usage is throttled to the SKU limit.

## Sizing Decision Guide

| Factor | How to Assess | Impact on SKU |
|---|---|---|
| **Peak concurrent notebooks/SJDs** | Count max parallel jobs during Synapse peak hours | More concurrency → larger SKU |
| **Largest single-job resource need** | Check Synapse executor/driver memory configs | Large executors → need enough CUs to allocate them |
| **Data volume per job** | Measure typical input dataset sizes | >10 GB per job → F64+; >100 GB → F128+ |
| **Shared capacity with other workloads** | Will Warehouse / Power BI / Pipelines share this capacity? | Shared → size up 1–2 tiers |
| **Burst vs. sustained** | Is Spark usage spiky (batch ETL) or continuous? | Spiky → can use smaller SKU with burst; sustained → size for peak |
| **Dev vs. production** | Dev can use Starter Pool on F8; prod needs Custom Pool | Dev = F8–F16; Prod = F32+ |

## Cost Model Comparison

| Aspect | Synapse Spark | Fabric Spark |
|---|---|---|
| **Billing unit** | Per-node, per-minute (when pool is active) | Per-capacity, per-hour (always-on or paused) |
| **Idle cost** | Zero (auto-pause after timeout) | Capacity cost continues unless paused/deallocated |
| **Scale model** | Node count autoscale (min–max per pool) | Capacity SKU (fixed CUs, burst smoothing) |
| **Pause/resume** | Auto-pause per pool (minutes granularity) | Capacity pause/resume (via Portal or REST API) |
| **Reservation pricing** | Azure Reserved Instances (1yr/3yr) | Fabric capacity reservations (1yr) |
| **Trial** | N/A | Fabric Trial capacity (F64 equivalent, 60 days) |

> **Cost tip**: For dev/test migrations, use a **Fabric Trial capacity** (free F64 for 60 days) or **F8 with pause/resume** to minimize cost during the migration validation period. Scale up for production.
