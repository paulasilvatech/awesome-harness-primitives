---
name: gtm-product-led-growth
description: >-
  Build and evaluate product-led growth motions for self-serve acquisition, activation, freemium
  conversion, growth equations, channel economics, PQL handoff, forecasting, and PLG versus
  sales-led decisions. Use when asked whether to build PLG or sales-led, drive self-serve
  adoption, fix freemium conversion, plan developer-led adoption, choose growth channels, or test
  whether PLG will work.
license: MIT
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

<!-- Generated from harness/github-copilot/plugins/go-to-market/skills/gtm-product-led-growth/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Product-led growth

Assess whether PLG is the right motion, then convert the product and channel facts into activation fixes, growth equations, channel decisions, PQL handoffs, forecasts, and executable growth playbooks.

## When to invoke

- "Should we build PLG or sales-led?"
- "How do we drive self-serve adoption?"
- "Freemium to paid conversion isn't working."
- "Which growth channels should we invest in?"
- "How do I know if PLG will work?"

## PLG reality check

Do not assume PLG is better because it is trendy. In a six-month parallel test, PLG produced high volume, low ACV around `$5K`, fast time-to-revenue, and higher churn; sales-led produced lower volume, high ACV around `$50K`, slower time-to-revenue, and lower churn. Sales won `10x` on revenue despite `10x` less volume because product complexity plus buyer seniority required integration, change management, and multi-stakeholder alignment. Developers loved self-serve, but they were not the economic buyer.

| Motion | Works when | Breaks when |
| --- | --- | --- |
| PLG | Value is obvious in first `5 minutes`; implementation is trivial; individual user gets value without team buy-in; no procurement or legal hurdles; buyer = user. | Product requires integration/setup, buyer differs from user, legal/security friction appears, or the product needs education. |
| Sales-led | Product requires integration/setup; multiple stakeholders need alignment; buyer ≠ user; deal size justifies human touch; customer needs education to see value. | Small deals cannot support human touch and users can already self-serve. |
| Hybrid | Self-serve discovery works but expansion needs human help. | Sales engages too early and kills trust. |

```text
Can users get value in <10 min without docs?
├─ No → Sales-led required
└─ Yes → Can they self-serve implementation?
    ├─ No → Sales-led required
    └─ Yes → Is buyer = user?
        ├─ No → Hybrid (PLG + sales-assist)
        └─ Yes → Pure PLG viable
```

## Growth equation

Growth compounds when you systematize the relationship between inputs and outputs. Replace "do more marketing" with channel equations: activity input → traffic output → conversions.

| Channel | Example equation | Decision use |
| --- | --- | --- |
| Organic Search | `1 quality blog post → 400 users/month → 5% conversion = 20 new users` | Scale content only after actual conversion matches the hypothesis. |
| Paid Ads | `$1K spend at 8% conversion on 100K impressions = 8K clicks → conversions at X%` | Scale only when CAC, retention, and LTV support it. |
| Community Events | `1 event → 60 attendees → 35% conversion = 21 users` | Compare event-sourced retention against other channels. |
| Referral | `1 integration partner → N referred users → conversions at Y%` | Track partner quality separately from volume. |

Test each equation with a small sample, measure actual conversion, compare reality to hypothesis, scale if validated, and kill if four weeks of data disproves the channel. Cheap CAC is not good CAC if retention is weak.

## Channel economics

Track channel economics monthly. Quarterly, reallocate `3x` budget to winners and kill losers.

| Metric | Formula or rule | Why it matters |
| --- | --- | --- |
| CAC | Total spend / new users | Shows acquisition cost by source. |
| Conversion rate | Signups → paying | Separates traffic quality from volume. |
| Retention | `30-day` and `90-day` retention by source | Reveals whether users from a cheap channel stay. |
| LTV | Revenue over customer lifetime, by channel | Determines how much CAC can be justified. |
| Payback period | Time to recoup CAC | Controls cash efficiency. |

```text
CAC < (LTV × margin)?
├─ No → Kill within 4 weeks
└─ Yes → 90-day retention > 60%?
    ├─ No → Optimize (improve activation/onboarding)
    └─ Yes → Scale aggressively (3x budget)
```

Decision rule: CAC < `(LTV × margin)` means scale aggressively; CAC ≈ `(LTV × margin)` means optimize but do not scale; CAC > `(LTV × margin)` means kill within `4 weeks` unless the fix is obvious and fast.

## Activation and time to first value

Users decide product value in the first `5-10 minutes`. If TTFV exceeds `10 minutes`, treat activation as broken.

| Audit step | Good target | Fix |
| --- | --- | --- |
| Sign up as a new user | Aha moment without docs | Remove documentation dependency from the core path. |
| Time to first value | `<10 min` | Pre-load sample data and let users complete the first action immediately. |
| Steps before value | Few, obvious, reversible | Skip non-essential setup: email confirmation, profile, and settings can wait. |
| Feature exposure | One core workflow first | Use progressive disclosure instead of showing every feature upfront. |
| Tutorial style | Interactive tutorial > video > text docs | Let users click through a working example. |

Before: sign up → confirm email → fill profile → configure settings → read docs → first action. After: sign up → pre-loaded sample data → first action and immediate aha moment.

## Monetization handoff

PLG often works at `$1K-$10K ARR`. Between `$20K-$50K`, procurement, legal, security, and multi-stakeholder buy-in can break the motion. Use a hybrid instead of forcing self-serve.

| Segment | Motion | Handoff rule |
| --- | --- | --- |
| `$0-$10K` | PLG | Self-serve sign-up → free tier → paid tier → credit card checkout → automated onboarding. |
| `$10K-$50K` | Sales-Assisted | Self-serve discovery → sales engages on usage signals → human-negotiated contract → dedicated onboarding. |
| `$50K+` | Enterprise | Outbound or inbound lead → demo → POC → proposal → legal/security review → executive sponsor. |

PQL signals combine usage depth, expansion, and buying intent: daily active use, core features used, approaching limits, multiple users from the same company, team features, integrations, requests for SSO/compliance/SLAs, and questions about team pricing. Bad handoff: "Hey, I saw you signed up." Good handoff: "Your team is using [specific feature] across 12 repos. We can help you [specific value]. Want 15 minutes?"

## Forecasting and playbooks

Forecasts are always wrong; plans still force thinking and accountability. Model three scenarios and update monthly.

| Scenario | Example |
| --- | --- |
| Baseline | Organic search `35% growth → 40K new users`; paid flat `→ 2K`; community `10% growth → 400`; total `42.4K`. |
| Upside | Organic `50% growth (3x content) → 48K`; paid `2x spend → 4K`; partnerships `→ 3K`; total `55K`. |
| Downside | Organic `0% growth → 26K`; paid CPA doubles `→ 1K`; total `27K`. |

After every successful campaign or experiment, write a one-page playbook:

```text
PLAYBOOK: [Channel/Tactic Name]

Goal: [What outcome]
Steps: [Numbered, specific enough for someone unfamiliar]
Expected Output: [Specific metrics]
Metrics to Track: [How to measure]
Risks & Mitigations: [What could go wrong]
Owner: [Name]
Last Updated: [Date]
```

The test: someone who was not involved can execute the playbook. Review quarterly, remove playbooks that no longer work, update evolved ones, and keep growth knowledge out of one person's head.

## Common mistakes

| Mistake | Why it fails | Correction |
| --- | --- | --- |
| Assuming PLG always works | Product complexity plus buyer seniority can make sales-led win. | Test PLG and sales-led before committing. |
| No channel economics | CAC without retention and LTV hides bad users. | Track CAC, conversion, 30/90-day retention, LTV, and payback by channel. |
| Free tier too generous or too limited | Too generous blocks conversion; too limited blocks activation. | Allow `10-20` aha moments. |
| No growth equation | "Do more marketing" is not a strategy. | Map inputs → outputs → conversions per channel. |
| Scaling before validating | Unproven channels waste budget. | Use `4 weeks` of data before scaling; kill decisively if economics fail. |
| Sales engaging too early | Human outreach on `<$5K` deals scares self-serve users. | Wait for PQL signals and use specific, value-based handoff. |
| Growth knowledge trapped in one person's head | Experiments cannot be repeated. | Document each successful experiment as a playbook. |

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `technical-product-pricing` | skill | Freemium thresholds, packaging, pricing gates, or willingness-to-pay analysis drive the decision. |
| `developer-ecosystem` | skill | The task is developer-specific community, integrations, advocacy, or ecosystem adoption. |
| `0-to-1-launch` | skill | The product still needs first customers before PLG can scale. |

## Growth vocabulary

Use the original GTM terms when they clarify the diagnosis: hand-holding, procurement/legal hurdles, SSO/compliance buying signals, multi-user expansion, over-invest and under-invest channel allocation errors, one-off wins, and forecast-and-forget planning mistakes.

## Output template

```markdown
## Product-led growth recommendation - <product or motion>

**Status:** PLG viable | sales-led recommended | hybrid recommended | needs test
**Primary constraint:** <activation | implementation | buyer mismatch | channel economics | pricing>
**Decision:** <one-sentence recommendation>

| Area | Evidence | Decision | Next action |
| --- | --- | --- | --- |
| PLG readiness | <TTFV, implementation, buyer=user> | <pass/fail> | <test or fix> |
| Activation | <TTFV and aha steps> | <pass/fail> | <onboarding change> |
| Channel economics | <CAC, conversion, retention, LTV, payback> | <scale/optimize/kill> | <budget or experiment> |
| Monetization | <ARR band and PQL signals> | <PLG/sales-assist/enterprise> | <handoff> |
| Forecast | <baseline/upside/downside> | <target range> | <monthly update> |

### Growth equation
`<activity input> → <traffic output> → <conversion> = <new users or revenue>`

### Playbook to write
`PLAYBOOK: <channel/tactic>` with Goal, Steps, Expected Output, Metrics to Track, Risks & Mitigations, Owner, Last Updated.
```

## Quality gate

- [ ] The recommendation explicitly chooses PLG, sales-led, hybrid, or needs-test.
- [ ] TTFV is evaluated against `<10 min` and the first aha moment is identified.
- [ ] Buyer/user alignment and implementation complexity are assessed.
- [ ] Channel economics include CAC, conversion, 30/90-day retention, LTV, and payback.
- [ ] Channels are marked scale, optimize, or kill using `CAC < (LTV × margin)` and `90-day retention > 60%`.
- [ ] PQL signals and sales handoff timing are specific, not generic.
- [ ] Forecast includes baseline, upside, downside, and monthly update expectations.
