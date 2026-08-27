---
name: gtm-0-to-1-launch
description: >-
  Launch new products from idea to first customers by choosing direct outreach over vanity press,
  diagnosing stalls with positioning/experience/alignment layers, finding the first 10-50
  customers, running 2-week experiments, validating PMF, and building launch playbooks. Use when
  launching products, finding early adopters, building launch week plans, or diagnosing stalled
  adoption.
license: MIT
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

<!-- Generated from harness/github-copilot/plugins/go-to-market/skills/gtm-0-to-1-launch/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# 0-to-1 launch

Take a new product, feature launch, or stalled adoption problem, transform it through first-customer GTM diagnosis and experiment design, and output a launch plan focused on learning, activation, and the first 10 customers rather than headlines.

## When to invoke

- "How do we launch this product?"
- "Find our first customers."
- "We launched but nobody is using it."
- "Should we do Product Hunt, press, or direct outreach?"
- "Build a 2-week experiment plan for early traction."

## Launch principles

| Principle | Use it because | Do instead |
| --- | --- | --- |
| Press does not equal growth | A press-heavy launch can produce `50K impressions`, `12 signups`, and `2 conversions` when the product is not self-serve ready. | Email 50 target customers directly, explain the problem, offer early access, and walk them through setup. |
| First 10 customers are for learning | Early revenue is less important than activation flow, objections, buyer identity, budget authority, and sales-cycle discovery. | Charge when possible; paying users give sharper feedback than free users. |
| Launches stall in layers | Weak conversion can be a positioning, experience, or alignment problem. | Diagnose the layer before spending engineering or marketing effort. |
| Experiments must compound | One-off wins vanish without a playbook. | Use a 2-week experiment cycle and document Goal → Steps → Expected output → Metrics → Risks. |
| Do not scale before PMF | Marketing spend hides weak retention and activation. | Wait for retention, organic growth, sales velocity, and qualitative pull. |

Direct outreach benchmark from the reference launch: `50 emails → 15 replies (30% reply rate) → 8 trials → 4 conversions (50% trial-to-paid)`.

## Three-layer diagnosis

| Layer | Symptoms | Diagnosis | Fix |
| --- | --- | --- | --- |
| Positioning problem | Messaging sounds like competitors; differentiation needs complex technical explanation; buyers treat you as interchangeable; sales derails into comparisons. | You are fighting an asymmetric war on the wrong front. | Map competitor claims, find a position they cannot easily copy, and test outbound messaging before committing product resources. |
| Experience problem | Strong awareness but weak activation; signups do not complete first workflow; too many entry points; docs are feature-centric. | Flexibility without opinionated defaults creates paradox of choice. | Pick 2-3 undeniable use cases, restrict onboarding to them, gate advanced features behind mastery, and rewrite help around jobs-to-be-done. |
| Alignment problem | Team says it is out of bandwidth for customers; functions optimize different metrics; every idea has equal weight; no north star. | Exploratory mode is destructive under constrained resources. | Define one north star, use it as the tiebreaker, cut work that does not help win a customer, and make progress visible weekly. |

Decision tree:

```text
Do prospects understand what you are?
├─ No → Layer 1: Positioning problem → Test new messaging before changing product
└─ Yes → Do users activate after signing up?
   ├─ No → Layer 2: Experience problem → Restrict onboarding to 2-3 use cases
   └─ Yes → Is the team aligned on what matters?
      ├─ No → Layer 3: Alignment problem → Single north star and weekly visibility
      └─ Yes → Keep iterating
```

## First-customer channels

| Channel | Best for | How to run it |
| --- | --- | --- |
| Personal network | First 2-3 customers and feedback calls | Say `I'm building [X], can I get your feedback?`; convert to paid when value is clear. |
| Direct outreach | Customers 3-20 and message testing | Build 100 target accounts, personalize to pain, test variants, and track reply/trial/paid rates. |
| Ceiling moment targeting | Highest-intent prospects | Find teams that adopted a comparable solution and hit its limit; message `We see teams that outgrow [incumbent] when they need [capability]. That's what we built.` |
| Community | Developer products or niche workflows | Post the problem, not hype; offer white-glove onboarding in Slack, Discord, forums, or relevant communities. |
| Partner-led entry | Markets where you lack distribution | Approach market leaders with a customer problem, start with a narrow integration, prove value in a 3-6 month pilot, build references, then leverage partner GTM. |

Use the supernode pattern only when your product owns critical data or workflows that other tools naturally need. Sequence partnerships by dominating 2-3 categories per quarter, then use joint customer stories.

## Experiment cycle and playbooks

| Step | Rule |
| --- | --- |
| Hypothesis | Test one variable: messaging, channel, pricing, onboarding, or feature. |
| Success criteria | Define the threshold before starting. |
| Duration | Run for 2 weeks maximum; if no signal by then, kill it. |
| Scale or stop | If it works, allocate 3x resources within a week. If not, move to the next test. |
| Documentation | Turn every successful experiment into a playbook with Goal, Steps, Expected output, Metrics, and Risks. |

Make decisions with about 70% information. Do not wait for perfect conditions, and do not keep failing experiments because of emotional investment.

## PMF validation

| Area | Signal |
| --- | --- |
| Retention | 40%+ of Week 1 users return in Week 4; usage increases over time; customers renew without sales push. |
| Organic growth | Word-of-mouth referrals happen; customers ask `can I add my team?`; inbound appears without paid marketing. |
| Sales velocity | Sales cycles shorten; win rates are greater than 30% of trials; customers say `we need this now`. |
| Qualitative | More than 40% would be very disappointed if the product went away; customers can articulate the use case; customers advocate publicly. |

If these signals are absent, do not scale marketing or sales yet.

## Press versus direct outreach

```text
Self-serve ready? Users get value in <10 min
├─ No → Direct outreach only; press will not convert
└─ Yes → Do you have >$1M funding or a major milestone to announce?
   ├─ Yes → Use both: press for awareness, outreach for conversion
   └─ No → Direct outreach first, press later
```

Press matters later for a Series A announcement or major milestone. In 0-to-1, optimize for activation and learning.

## Gotchas

- **Do not optimize for headlines**: 50K impressions and 12 signups is failure if activation is weak.
- **Do not launch without a target list**: build the 100-account list before launch week.
- **Do not offer unlimited flexibility**: opinionated defaults beat choice when users need an aha moment.
- **Do not give everything away free**: free users are polite; paying users reveal real objections.
- **Do not diagnose the wrong layer**: positioning fixes do not solve broken onboarding, and onboarding fixes do not solve indistinct positioning.
- **Do not treat partnerships as passive distribution**: partners need integration paths, support, and reference customers.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `product-led-growth` | skill | The product already has initial traction and needs scaling loops. |
| `positioning-strategy` | skill | The main task is category, differentiation, or message testing. |
| `partnership-architecture` | skill | The task is designing partner-led entry or integration strategy. |

## Source compatibility terms

Retain these launch-diagnosis terms from the original field guide: `Slack/Discord/forums`, `and-pray`, `better-funded`, `hand-holding`, `highest-intent`, `marketing/sales.**`, `non-essential`, `outcome-centric`, `product-market`, `three-layer`, `under-testing`, `word-of-mouth`, `TechCrunch`, and `VentureBeat`.

## Output template

```markdown
## 0-to-1 launch plan — <product>

**Status:** ready to test | needs positioning | needs activation fix | blocked
**North star:** <one metric tied to winning customers>
**Primary diagnosis:** positioning | experience | alignment | not stalled

### First-customer target
| Segment | Pain | Why now | Outreach angle | Target count |
| --- | --- | --- | --- | --- |
| `<segment>` | `<specific problem>` | `<trigger>` | `<message>` | 100 |

### Launch motion
| Channel | Experiment | Success criteria | Duration | Owner |
| --- | --- | --- | --- | --- |
| Direct outreach | `<variant>` | `<reply/trial/paid threshold>` | 2 weeks | `<owner>` |

### Playbook
**Goal:** <learning or conversion goal>
**Steps:**
1. <step>
2. <step>
**Expected output:** <artifact or metric>
**Metrics:** <activation, replies, trials, paid, retention>
**Risks:** <positioning, experience, alignment, partner, or channel risk>

### PMF check
- Retention: <evidence>
- Organic growth: <evidence>
- Sales velocity: <evidence>
- Qualitative pull: <evidence>
```

## Quality gate

- [ ] The plan targets learning from the first 10-50 customers, not vanity awareness.
- [ ] Any stalled launch is diagnosed against positioning, experience, and alignment before prescribing fixes.
- [ ] Direct outreach includes a concrete segment, pain, list size, message angle, and success metric.
- [ ] Every experiment has one variable, a 2-week limit, success criteria, and a kill or 3x decision rule.
- [ ] PMF claims include retention, organic growth, sales velocity, and qualitative evidence.
- [ ] Press, Product Hunt, or partner motions are recommended only when the product is ready for that channel.

## References

- [Technical product GTM source](https://github.com/beingsmit/technical-product-gtm)
- [Smit Patel](https://linkedin.com/in/smitkpatel)
