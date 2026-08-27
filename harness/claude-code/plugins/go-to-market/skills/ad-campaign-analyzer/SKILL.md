---
name: ad-campaign-analyzer
description: >-
  Analyze ad campaign performance data to diagnose waste, identify winners, validate A/B tests,
  compare channels, and recommend cuts, scaling, tests, and budget reallocation. Use when the user
  asks to analyze ad campaigns, find wasted spend, optimize Google Ads, Meta Ads, LinkedIn Ads,
  ROAS, CPA, CAC, or multi-channel ad budgets.
license: MIT
metadata:
  author: GooseWorks
  compatibility: >-
    Cross-platform. Pure reasoning skill over user-provided campaign exports (CSV, paste, or
    screenshot from Google, Meta, or LinkedIn) — no external tools, network calls, or API keys.
  source: "https://github.com/gooseworks-ai/goose-skills"
  version: "'1.0'"
---

<!-- Generated from harness/github-copilot/plugins/go-to-market/skills/ad-campaign-analyzer/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Ad campaign analyzer

Turn raw ad performance exports into a decision report that normalizes metrics, diagnoses waste, identifies winners, checks statistical significance, compares channels on equal terms, and recommends exactly what to pause, scale, test, or reallocate.

## When to invoke

- "Analyze my ad campaign performance."
- "Where am I wasting ad spend?"
- "Which ads should I pause or scale?"
- "Reallocate my ad budget across channels."
- "Which channel has the best ROAS or CAC?"

## Prerequisites and context

This is a pure reasoning skill; no external tools, network calls, API keys, or platform access are required. The user must provide campaign data as CSV export, pasted table, or screenshot from Google Ads, Meta Ads Manager, LinkedIn Campaign Manager, Twitter/X Ads, TikTok Ads, or another ad platform.

## Intake and normalization

Collect or infer:

| Input | Why it matters |
| --- | --- |
| Campaign data | Spend, impressions, clicks, conversions, and value are the analysis base. |
| Platform(s) | Google, Meta, LinkedIn, and other channels use different native column names. |
| Time period | Prevents comparing unlike date ranges. |
| Monthly budget | Enables over-spending vs under-spending and budget shift analysis. |
| Primary goal | Demos, Trials, Purchases, Leads, or another conversion define success. |
| Target metrics | Target CPA or ROAS determines pause/scale thresholds; benchmark if absent. |
| Known changes | Creative, budget, bid strategy, or targeting changes affect interpretation. |
| Channels running or considered | Supports current allocation and new-channel recommendations. |
| Funnel data | Lead → MQL rate, MQL → SQL rate, SQL → Close rate, Average deal size. |
| Constraints | Minimum spend, must-use platforms, and channel exclusions. |

Normalize platform exports into a shared table:

| Source | Key columns expected |
| --- | --- |
| Google Ads | Campaign, Ad Group, Keyword, Impressions, Clicks, CTR, CPC, Conversions, Conv Rate, Cost, Conv Value. |
| Meta Ads | Campaign, Ad Set, Ad, Impressions, Reach, Clicks, CTR, CPC, Conversions, Cost Per Result, Amount Spent, ROAS. |
| LinkedIn Ads | Campaign, Impressions, Clicks, CTR, CPC, Conversions, Cost, Leads. |

Standard dimensions: Dimension, Impressions, Clicks, CTR, CPC, Conversions, Conv Rate, CPA, Spend, Revenue/Value. For multi-channel data, produce a channel rollup with Channel, Monthly Spend, Impressions, Clicks, CTR, CPC, Conversions, Conv Rate, CPA, ROAS, and CAC. CAC is full customer acquisition cost when funnel data is available.

```text
Channel CAC = CPA ÷ (MQL rate × SQL rate × Close rate)
```

## Diagnostic rules

| Area | Signal | Action |
| --- | --- | --- |
| Zero-conversion keywords/ads | Spend > threshold with 0 conversions | Pause, add negatives, or isolate for more data. |
| High CPA outliers | CPA > 3x target | Pause, restructure, or fix landing page/offer mismatch. |
| Low CTR ads | CTR < 50% of campaign average | Replace creative or tighten targeting. |
| Broad match bleed | Search terms show irrelevant clicks | Add negative keywords. |
| Audience overlap | Same users hit by multiple campaigns | Exclude overlapping audiences. |
| Dayparting waste | Conversions cluster at certain hours while spend runs 24/7 | Set ad schedule. |
| Top-performing keywords | Lowest CPA and highest conversion rate | Increase bid and add variants. |
| Winning ads | Highest CTR + conversion-rate combination | Scale spend and clone into relevant ad groups. |
| Best audiences | Lowest CPA segment | Increase budget allocation. |
| Best times | Peak conversion hours/days | Concentrate budget. |

Campaign-level health checks compare CTR, CPC, Conv Rate, CPA, ROAS, and Impression Share against target or benchmark. Treat Impression Share `>60%` as a healthy starting point when growth is constrained by availability rather than waste.

## Statistical significance and funnel analysis

Use significance checks for A/B tests on ad variants, audiences, and landing pages:

```text
Test: [Variant A] vs [Variant B]
Metric: [Conv Rate / CTR / CPA]
Variant A: [X%] (n=[sample_size])
Variant B: [Y%] (n=[sample_size])
Confidence level: [X%]
Verdict: [Statistically significant / Not enough data / Too close to call]
Recommended action: [Pick winner / Continue test / Increase budget to reach significance]
```

Minimum samples: 100 clicks per variant for CTR tests and 30 conversions per variant for CPA tests. Below that, call the result inconclusive unless the business risk requires an immediate stop.

Represent the funnel explicitly:

```text
Impressions: [N] (100%)
     ↓ CTR: [X%]
Clicks: [N] ([X%] of impressions)
     ↓ Landing page → Conversion: [X%]
Conversions: [N] ([X%] of clicks)
     ↓ Conversion → Revenue: $[X] avg
Revenue: $[N]
```

Diagnose drop-offs at Impression → Click, Click → Conversion, and Conversion → Revenue. Map each to rate, benchmark, likely cause, and fix.

## Budget reallocation

For multi-channel data, rank each channel by CPA, Funnel-Adj CAC, Share of Spend, Share of Conversions, and Efficiency Index.

```text
Efficiency Index = Conversion share ÷ Spend share
```

Interpretation: `> 1.0` means under-invested, `= 1.0` means proportional, and `< 1.0` means over-invested. Then estimate marginal return from saturation signals such as Google Search impression share, Meta frequency, or LinkedIn volume ceilings.

Check funnel stage coverage: Awareness (Meta Display, YouTube), Consideration (Google Search, Meta retargeting), Decision (Google Brand, Google Search), and Retargeting (Meta, Google Display). Build budget shifts with current spend, recommended spend, change, and reasoning. Include conservative `+/- 20%`, aggressive `+/- 40%`, and budget-increase scenarios when data supports them.


## Channel vocabulary and verdict labels

Preserve native channel terminology in the analysis: `FB/IG`, `Google / Meta / LinkedIn`, `channel-level`, `cross-channel`, `Revenue/Value`, `close-rate`, `X/month`, `Keywords/Audiences`, `budget/bids`, and `keywords/ads**`. Use `Good/Okay/Poor` as compact health labels when a dashboard-style output is clearer than prose, and use `Copy/targeting` as the combined fix when weak CTR can be caused by either message or audience mismatch.

## Output template

```markdown
# Ad Campaign Analysis — [Product/Client] — [DATE]

Period: [Date range]
Total spend: $[X]
Platform(s): [Google / Meta / LinkedIn]
Primary goal: [Conversions / Revenue / Leads]

## Executive Summary
[3-5 sentences: verdict, biggest win, biggest problem, and top recommendation]

## Performance Dashboard
| Campaign | Spend | Impressions | Clicks | CTR | CPC | Conversions | CPA | ROAS | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Name] | $[X] | [N] | [N] | [X%] | $[X] | [N] | $[X] | [X] | [Scale/Optimize/Pause] |

## Budget Waste Report
**Total estimated waste:** $[X] ([X%] of total spend)

### Wasted on zero-conversion items: $[X]
[List of keywords/ads/audiences with spend but no conversions]

### Wasted on high-CPA items: $[X]
[List of items with CPA > 3x target]

### Recommended saves: $[X]/month
[Specific items to pause]

## Winners to Scale
| Item | CPA | Conv Rate | Current Spend | Recommended Spend |
| --- | --- | --- | --- | --- |

## A/B Test Results
### [Test Name]
- Variant A: [Metric] (n=[N])
- Variant B: [Metric] (n=[N])
- Confidence: [X%]
- **Verdict:** [Winner / Continue / Inconclusive]

## Budget Reallocation
| Channel | Current | Recommended | Change | Why |
| --- | --- | --- | --- | --- |
| [Channel] | $[X] | $[Y] | [+/-$Z] | [1-line reason] |

**Projected impact:**
- Conversions: [N] → [N] (+[X%])
- Blended CPA: $[X] → $[Y] (-[X%])

### Funnel Stage Coverage
[Coverage map with gaps identified]

### New Channel Recommendations
#### [Channel Name]
- **Why test:** [Reasoning]
- **Recommended test budget:** $[X]/mo for [X weeks]
- **Success criteria:** CPA < $[X]
- **Competitors using it:** [Yes/No — who]

## Action Plan
### Immediate (This Week)
- [ ] **Pause:** [Specific keywords, ads, audiences]
- [ ] **Scale:** [Specific items and bid/budget changes]
- [ ] **Add negatives:** [Specific keywords]
- [ ] **Reallocate:** [Specific dollar shifts]

### This Month
- [ ] **Test:** [New ad angles, audiences, landing pages]
- [ ] **Restructure:** [Ad groups to split or merge]
- [ ] **Optimize:** [Bid strategy changes]
- [ ] **Monitor reallocation:** Track CPA shifts and diminishing returns

### Next Month
- [ ] **Expand:** [New campaigns or channels]
- [ ] **Re-evaluate:** Run this analysis again with new data
```

Save to `campaign-analysis-[YYYY-MM-DD].md` in the current working directory or the user-specified path.

## Quality gate

- [ ] Data was normalized into comparable CTR, CPC, conversion rate, CPA, ROAS, and CAC fields.
- [ ] Spend waste, winners, and inconclusive areas were separated.
- [ ] A/B tests used sample-size rules: 100 clicks per variant for CTR or 30 conversions per variant for CPA.
- [ ] Multi-channel recommendations used Efficiency Index and funnel-adjusted CAC when funnel data exists.
- [ ] Every pause, scale, test, or reallocation recommendation includes numeric evidence.
- [ ] The output includes an immediate, monthly, and next-month action plan.

## References

- [GooseWorks source skill](https://github.com/gooseworks-ai/goose-skills)
