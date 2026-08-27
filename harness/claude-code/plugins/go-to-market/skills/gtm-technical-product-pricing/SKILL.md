---
name: gtm-technical-product-pricing
description: >-
  Design pricing strategy for technical products by choosing seat-based, usage-based,
  outcome-based, hybrid, freemium, enterprise, and price-positioning models. Use when asked to
  price an API, developer tool, SaaS, infrastructure product, freemium tier, enterprise plan,
  price increase, or GTM monetization motion.
license: MIT
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

<!-- Generated from harness/github-copilot/plugins/go-to-market/skills/gtm-technical-product-pricing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Technical product pricing

Assess a technical product's value, cost, GTM motion, customer segment, and competitive alternatives, then recommend a pricing model, packaging thresholds, enterprise conversation structure, price-positioning signal, and price-increase path.

## When to invoke

- "How should we price this developer tool?"
- "Should this be usage-based or seat-based pricing?"
- "Where should our freemium tier end?"
- "Help structure enterprise pricing."
- "Should we raise prices?"

## Initial assessment

Collect these inputs before recommending pricing:

| Question | Why |
| --- | --- |
| Product type | API/platform, developer tool, SaaS application, or infrastructure have different units of value. |
| Current pricing | Existing price and duration expose underpricing and migration risk. |
| GTM motion | Self-serve, sales-assisted, enterprise, or hybrid changes packaging and contract terms. |
| Cost structure | Marginal cost per customer, user, unit, API call, compute unit, or storage unit sets the floor. |
| Competitive landscape | Alternatives include competitors, building in-house, manual work, existing tool plus switching cost, and doing nothing. |

## Value-ratio pricing

Anchor price to customer alternative cost rather than your internal cost. Enterprise buyers often compare your price to engineering time saved, risk reduced, downtime avoided, or revenue unlocked.

```text
Value Ratio = Customer's alternative cost / Your price
```

| Value Ratio | Interpretation | Action |
| --- | --- | --- |
| `> 10x` | Massively underpriced | Raise or repackage for value. |
| `> 5x` | Underpriced | Test higher tiers or enterprise pricing. |
| `3-5x` | Healthy pricing | Optimize packaging and expansion. |
| `< 3x` | Approaching ceiling | Improve differentiation before raising. |
| `< 2x` | Expensive | Segment better or strengthen proof of value. |

Calculate alternative cost from hours spent on manual process × hourly rate × frequency; cost of building in-house as engineers × months × loaded cost; cost of existing tool + switching cost + productivity loss; or cost of not solving the problem such as incidents, downtime, or churn. Do not benchmark only against competitors; that anchors a race to the bottom.

## Pricing model decision rules

| Model | Works when | Breaks when |
| --- | --- | --- |
| Seat-Based (`$X/user/month`) | Value scales with users, usage is uniform, predictable revenue matters. | Power users and casual users pay the same, one admin configures for 1,000 users, customers consolidate seats. |
| Usage-Based (`$X/unit`) | Usage varies significantly, marginal cost matters, value correlates with usage. | Bills are unpredictable, low-usage customers are uneconomic, high-usage discounts compress margins. |
| Outcome-Based (`$X/result`) | Outcomes are measurable, valuable, and attributable. | Outcomes depend on outside factors, measurement is disputed, customers game the metric. |
| Hybrid | A platform fee covers fixed costs and usage or outcome fees scale with value. | The base fee is too low to cover support or the variable unit is not tied to value. |

A common winning structure is `$500/month base + $0.05 per transaction`, API call, task completed, or record processed. Use a platform fee for fixed costs and variable pricing for upside.

```text
Does usage vary >5x between customers?
├─ Yes → Usage-based (or hybrid with usage component)
└─ No → Does value scale with team size?
   ├─ Yes → Seat-based
   └─ No → Can you measure customer outcomes reliably?
      ├─ Yes → Outcome-based (or hybrid)
      └─ No → Platform fee + feature-based tiers
```

## Freemium thresholds

Find the production boundary. Free should serve hobbyists, learners, awareness, community, and content; it should not let production users avoid payment forever.

| Usage level | User type | Willingness to pay |
| --- | --- | --- |
| `<100 units/mo` | Hobbyist/learner | `$0` and likely never paying. |
| `100-1K units/mo` | Side project | `$0-20/mo` and maybe. |
| `1K-10K units/mo` | Production use | `$50-200/mo` and likely to pay. |
| `>10K units/mo` | Business-critical | `$200-2K/mo` and must pay. |

Set the free tier just below where production usage starts, such as `1,000 units/month free` when production begins above that. Use these conversion triggers:

| Trigger | Best for | Conversion signal |
| --- | --- | --- |
| Usage limit | Platforms: API calls, tasks, records, value units. | User is building something real. |
| Team/collaboration gate | Tools. | User invites a second person. |
| Enterprise feature gate | Platforms. | Needs SSO, RBAC, audit logs, SLAs, or IT/security approval. |

## Enterprise pricing

Enterprise pricing is a conversation, not just a number on a page. Keep `Contact Sales` for unique requirements and value anchoring.

| Variable | Pricing effect |
| --- | --- |
| Deployment model | Self-serve cloud, dedicated cloud, on-prem, and hybrid have different cost floors; on-prem often commands `2-5x` cloud because support complexity rises. |
| Usage scale | Seats, API volume, and data volume get volume discounts, but never below cost to serve + `40%` margin. |
| Support level | Premium support: `1.5-2x` base; dedicated CSM: `2-3x`; 24/7 support with SLA: `3-5x`. |
| Compliance | SOC 2, HIPAA, FedRAMP, and data residency add audits, infrastructure, and process; price `1.5-2x` base per compliance standard. |

When a prospect asks cost: do not lead with a number. Ask about users, seats, units, cloud vs on-prem, compliance, support, and integrations; anchor to savings; then present three options: Good, Better, Best. Most buyers pick Better.

## Price as positioning

| Price | Signal | Attracts | Risk |
| --- | --- | --- | --- |
| `$0` | Open source or free tier for try-before-buy developers. | Individual contributors and experimenters. | Perceived as not enterprise-ready. |
| `$20-100/month` | Teams and small businesses. | Self-serve buyers and startups. | Enterprises may not take it seriously. |
| `$500-2,000/month` | Production workloads. | Growing companies with budget. | Some startups priced out. |
| `$5,000-50,000/year` | Enterprise. | Mid-market and enterprise. | Requires sales team. |
| `$100K+/year` | Mission-critical infrastructure. | Large enterprises. | Long sales cycles and heavy support. |

If you price at `$50/month` while targeting enterprise, price undermines positioning. Price for the customer you want, not only the customer you have.

## Price increases

Raise prices when value ratio is `> 5x` for most customers, win rates are above `40%`, there has been no pricing pushback in the last 6 months, customers expand faster than expected, or competitors raised prices without losing share.

```text
Is value ratio > 5x for most customers?
├─ Yes → Raise prices
└─ No → Are win rates > 40%?
   ├─ Yes → Price is not the problem; consider raising
   └─ No → Are you losing deals specifically on price?
      ├─ Yes → Do not raise; improve value or segment better
      └─ No → Something else is wrong: product, positioning, or sales
```

Raise without losing customers by grandfathering existing customers for `12-24 months`, adding value to justify the increase, and using `5-10%` annual escalator clauses in enterprise contracts. Communicate: "We're investing in [specific improvements]. To continue this level of investment, we're updating our pricing on [date]. Your current plan is locked in at your current rate until [grandfather date]." Do not apologize; frame it as investment.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `ai-gtm` | skill | Pricing AI-specific products with variable AI costs or input/output pricing. |
| `product-led-growth` | skill | Designing PLG conversion and freemium activation loops. |
| `enterprise-account-planning` | skill | Structuring enterprise deal strategy and negotiation. |
| `positioning-strategy` | skill | Positioning, segmentation, and messaging beyond price. |


## Pricing examples and deal vocabulary

Use concrete pricing anchors when useful: a platform company charging `15K/year` and raising enterprise to `45K/year.` can be underpriced if the customer saves far more. Cost inputs may be per `customer/user/unit`; beware `month-end` sticker shock in usage pricing, `already-discounted` discount stacking, and enterprise bundles with `nice-to-haves`. Hybrid models combine `usage/outcome` economics, enterprise discovery asks for `users/seats/units`, and AI pricing may require `variable-cost` analysis. High-price infrastructure can be `mission-critical` rather than merely expensive.

## Output template

```markdown
## Technical product pricing recommendation — <product>

**Status:** recommended | needs data | blocked
**Product type:** API/platform | developer tool | SaaS | infrastructure
**GTM motion:** self-serve | sales-assisted | enterprise | hybrid

### Value and floor
- Alternative cost: $<amount> based on <method>
- Current or proposed price: $<amount>
- Value Ratio: <ratio>x (<interpretation>)
- Marginal cost floor: $<amount or unknown>

### Recommended model
| Component | Recommendation | Rationale |
| --- | --- | --- |
| Base fee | $<amount> | <reason> |
| Usage unit | $<amount>/<unit> | <reason> |
| Free tier | <threshold> | <production boundary> |
| Enterprise | <packaging> | <deployment/support/compliance logic> |

### Packaging and positioning
- Target customer: <segment>
- Price signal: <signal>
- Free-to-paid trigger: <usage/team/enterprise gate>

### Price-change plan
- Grandfathering: <12-24 month plan or none>
- Added value: <features/services>
- Contract terms: <annual escalator or discount guardrail>
```

## Quality gate

- [ ] Product type, current pricing, GTM motion, cost structure, and alternatives were assessed or marked unknown.
- [ ] Value Ratio was calculated or the missing inputs were named.
- [ ] The pricing model choice follows the usage, seat, outcome, or hybrid decision rules.
- [ ] Freemium thresholds separate learners from production users.
- [ ] Enterprise pricing accounts for deployment, scale, support, and compliance.
- [ ] Price positioning matches the target customer segment.
- [ ] Any price increase includes timing signals, grandfathering, added value, and communication plan.

## References

- [Technical product GTM source](https://github.com/beingsmit/technical-product-gtm)
- [Smit Patel](https://linkedin.com/in/smitkpatel)
