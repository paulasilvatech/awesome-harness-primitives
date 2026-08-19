# Fabric Cost Estimation Worksheet Template

Use live data from the APIs described in [pricing-api-reference.md](pricing-api-reference.md) to populate each field.

```text
╔══════════════════════════════════════════════════════════════════╗
║  FABRIC COST ESTIMATE — [Customer/Project Name]                 ║
║  Region: [detected from capacity / user-specified]              ║
║  Pricing as of: [today's UTC date]                              ║
║  Source: Azure Retail Prices API + Cost Management API          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ── CURRENT SPEND (from Cost Management API) ──                  ║
║  Databricks:     $[live] /month                                  ║
║  Synapse SQL:    $[live] /month                                  ║
║  Synapse Spark:  $[live] /month                                  ║
║  Power BI Prem:  $[live] /month                                  ║
║  Storage (ADLS): $[live] /month                                  ║
║  Total current:  $[sum]  /month                                  ║
║                                                                  ║
║  ── SOURCE WORKLOAD PROFILE ──                                   ║
║  Spark jobs:      [X] jobs/day, [Y] avg hours, [Z] nodes        ║
║  SQL queries:     [X] DWU-hours/day                              ║
║  Power BI:        [P-SKU] at [X]% utilization                    ║
║  Pipelines:       [X] runs/day, [Y] avg duration                 ║
║  Storage:         [X] TB total                                   ║
║                                                                  ║
║  ── FABRIC CU DEMAND ──                                          ║
║  Spark peak:      [X] CUs                                        ║
║  SQL peak:        [X] CUs                                        ║
║  PBI peak:        [X] CUs                                        ║
║  Pipeline peak:   [X] CUs                                        ║
║  Total peak:      [X] CUs                                        ║
║  Avg daily:       [X] CU-hours                                   ║
║                                                                  ║
║  ── RECOMMENDED CONFIGURATION ──                                 ║
║  Base SKU:        F[XX] ([Reserved/PAYG])                        ║
║  Spark billing:   [Autoscale Billing for Spark / Included in base]║
║  RI term:         [None / 1-Year / 3-Year]                       ║
║                                                                  ║
║  ── MONTHLY COST BREAKDOWN (live prices) ──                      ║
║  Capacity (base): $[from API] ([SKU] × [RI term])               ║
║  Spark autoscale: $[CU-hours × live rate]                        ║
║  Storage:         $[TB × live OneLake rate]                      ║
║  Network egress:  $[GB × live egress rate]                       ║
║  ─────────────────────────────────────────────────────           ║
║  TOTAL MONTHLY:   $[sum]                                         ║
║  TOTAL ANNUAL:    $[sum × 12]                                    ║
║                                                                  ║
║  ── SAVINGS vs. CURRENT ──                                       ║
║  Current monthly: $[from Cost Management API]                    ║
║  Fabric monthly:  $[calculated above]                            ║
║  Delta:           $[difference] ([percentage]%)                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```
