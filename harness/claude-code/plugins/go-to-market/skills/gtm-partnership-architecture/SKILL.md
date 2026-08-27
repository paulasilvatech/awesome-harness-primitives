---
name: gtm-partnership-architecture
description: >-
  Design and scale go-to-market partner ecosystems with tiering, value exchange, build-vs-partner
  decisions, co-marketing, and crawl-walk-run deployment. Use when asked to structure a partner
  program, decide whether to build or partner, recruit or tier partners, assess partnership
  leverage, or plan partner-led revenue motions.
license: MIT
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

<!-- Generated from harness/github-copilot/plugins/go-to-market/skills/gtm-partnership-architecture/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# GTM partnership architecture

Build and evaluate partner ecosystems by separating real economic commitments from co-marketing theater, choosing the right ecosystem control model, tiering partners by capability and strategic fit, and deploying partnerships through measurable crawl-walk-run gates.

## When to invoke

- "How do I structure a partner program?"
- "Should we build this or partner for it?"
- "How should we tier and recruit partners?"
- "Plan a crawl-walk-run partnership launch."
- "Is this partnership real or just co-marketing?"

## Partnership substance

Real partnerships require skin in the game. Ask: "If this partnership fails, what does each side lose?" If the answer is nothing, it is a handshake, not a partnership. Real commitments include spend, revenue share, co-investment, roadmap alignment, executive sponsorship, mutual risk, revenue guarantees, or dedicated engineering.

| Three-sided value | Questions to answer |
| --- | --- |
| Your company | Does the partnership create distribution, credibility, revenue, or product leverage you should not build yourself? |
| Partner | Does it improve revenue or margin, retention/stickiness, differentiation, or support burden? |
| Shared customers | Does it improve workflow, integration pain, vendor simplicity, or cost efficiency? |

Before pursuing any partner, document both sides' economic commitment and failure cost. If both sides can walk away at zero cost, reduce the motion to a lightweight test or decline it.

## Ecosystem control

Control discovery and trust, not every submission, unless the domain is regulated or security-critical.

| Model | Use when | Mechanisms | Risk |
| --- | --- | --- | --- |
| Curated gatekeeper | Brand damage risk is high, human review can scale, or partners are counted in dozens. | Review, certification/compliance/partnership checks, approved catalogs. | Slow growth and partner friction. |
| Open discovery | Network effects matter, partner count may reach hundreds or thousands, and low-quality entries can be moderated after publication. | Search, verified badges, usage stats, health scores, ratings, collections, recommendations, spam removal. | Quality variance and moderation overhead. |

Do not default to curated because of vague quality concerns. At 100+ partners, gatekeeping becomes the bottleneck; invest in high-quality discovery, trust, and self-service.

## Leverage hierarchy

| Rank | Leverage | Strength | Evidence |
| --- | --- | --- | --- |
| 1 | Requirement leverage | Strongest | Partner needs you for certification, compliance, marketplace eligibility, or partner status. |
| 2 | Economic leverage | Strong | You save or make money for the partner in their P&L terms. |
| 3 | Competitive leverage | Moderate | Exclusive or differentiated capability competitors would want. |
| 4 | Customer leverage | Moderate | Their customers request the integration in tickets, renewals, or deals. |
| 5 | Co-marketing leverage | Weak | Joint webinar, logo swap, co-branded blog, or press without economic pull. |

Qualify with: "If we do not do this partnership, what happens to you?" Answers like "we lose cloud provider certification" justify full investment; "nothing really changes" means walk away. Requirement leverage is why a certification line can close MSP deals faster than a generic pitch.

Use the partner's language in the business case: `cert/compliance` for requirement leverage, `saves/makes` for economic leverage, and `go/no-go` gates for phase decisions.

## Partner tiering

| Tier | Commitment | You provide | Partner provides | Timeline | Best for |
| --- | --- | --- | --- | --- | --- |
| Tier 1: Integration Partner | Self-serve | API/docs, documentation, Slack channel, office hours | Engineering resources and self-promotion | 2-6 months | Ambitious partners that can build with public APIs. |
| Tier 2: Partnership Partner | Joint Development | Dedicated channel, regular syncs, product input, platform co-marketing | Strategic fit and shared launch execution | 6-12 months | Partners where integration quality should accelerate. |
| Tier 3: Strategic Partner | Co-Development | Dedicated partner manager, executive relationship, custom co-marketing, revenue objectives | Roadmap commitment, executive engagement, field alignment | Ongoing | Marquee partners that shift positioning. |

Tier by strategic fit and partner capability. Do not over-tier or offer white-glove service to every partner; create a clear graduation path and avoid expectation mismatch.

## Crawl-walk-run deployment

| Phase | Duration | Scope | Go/no-go gate |
| --- | --- | --- | --- |
| Crawl | 4-8 weeks | 1-2 pilot customers, manual or lightweight non-production-grade integration, measured outcome. | 20%+ improvement on the stated metric, referenceable customers, and a scalable integration path. |
| Walk | 8-12 weeks | 5-10 additional customers, formal integration, joint announcements, webinars, sales enablement, playbooks. | 70%+ adoption rate of invited customers, active partner promotion, manageable support burden. |
| Run | 6-12 months ongoing | Full-scale APIs/native integrations, marketplace listing, joint enterprise sales, integrated customer success, QBRs and executive steering. | Crawl and Walk passed, both sides committed, ROI validates at scale. |

Most partnerships should fail in Crawl if the signal is weak. Do not skip Crawl, run phases in parallel, continue because of sunk cost, or move to the next phase without explicit Go/No-Go criteria.

If the pilot integration is not production-grade, say so plainly and keep the scope small until customer outcome data justifies investment.

## Partnership charter and launch execution

Require a written charter before launch.

| Charter area | Required content |
| --- | --- |
| Mutual goals | Success for your company, the partner, and customers. |
| Value exchange | What each side gives: engineering time, distribution, credibility, co-investment, co-marketing, or revenue share. |
| Timeline | Crawl, Walk, and Run dates, deliverables, and metrics. |
| Measurement | Revenue, influenced deals, retention, adoption, support load, dashboards, and monthly or quarterly reviews. |
| Governance | Decision owners, escalation path, QBR cadence, and exit criteria. |

Co-marketing is execution, not strategy. Before launch, finalize the joint value prop, identify 2-3 case study options, validate the technical integration to avoid launch-day bugs, prepare one-pager/deck/demo sales enablement, train support, and prepare marketplace listings. During launch week, coordinate press, blog posts, a webinar within two weeks, social campaign, sales briefing, and customer comms. After launch, track weekly adoption, triage support in a joint channel, publish a quantified case study, measure pipeline impact, and schedule the QBR.

## Decision trees

| Decision | Rule |
| --- | --- |
| Build-vs-partner | If the capability is core to product differentiation, build. If not core and building delays the roadmap by more than 6 months, partner. If delay is manageable but a credible partner needs you too, partner; otherwise build. |
| Which tier | If the partner has engineering resources to self-serve, start at Tier 1 and evaluate Tier 2 after 6 months. If not, use Tier 3 only for a marquee logo that shifts positioning; otherwise use Tier 2. |
| Continue or exit | If Crawl misses success criteria, end and learn. If Walk misses, end or restart Crawl with changes. Enter Run only after both gates pass. |

## Gotchas

- **Do not treat partnerships as a sales channel only**: they should expand platform capability, not just who buys it.
- **Do not launch without step-by-step integration pathways**: partners fail without implementation guidance.
- **Do not expect partners to self-promote**: provide co-marketing templates, resources, enablement, and support.
- **Do not create too many tiers**: two or three is usually optimal; more causes confusion.
- **Do not ghost after launch**: schedule recurring touchpoints and health management.
- **Do not pursue vanity partnerships**: brand names or funding links do not equal customer value.
- **Do not omit exit criteria**: define failure before emotions and sunk cost distort judgment.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `developer-ecosystem` | skill | The work is specifically a developer ecosystem, marketplace, API, or self-service builder motion. |
| `enterprise-account-planning` | skill | The partnership must be mapped into enterprise account strategy and partner-led versus direct sales motion. |
| `technical-product-pricing` | skill | The core problem is pricing, packaging, margin, or commercial terms for partnership deals. |

## Output template

```markdown
## Partnership architecture — <partner program or deal>

**Status:** pursue | test in Crawl | redesign | decline
**Partnership type:** Tier 1 Integration Partner | Tier 2 Partnership Partner | Tier 3 Strategic Partner
**Primary leverage:** requirement | economic | competitive | customer | co-marketing

| Area | Decision | Evidence |
| --- | --- | --- |
| Three-sided value | `<your company / partner / customer value>` | `<proof>` |
| Skin in the game | `<commitments on both sides>` | `<failure cost>` |
| Build vs partner | `<build or partner>` | `<core differentiation and roadmap impact>` |
| Deployment phase | `<Crawl, Walk, or Run>` | `<metric and gate>` |
| Charter | `<complete or gaps>` | `<owners, timeline, metrics, exit criteria>` |

**Next actions**
- <action 1>
- <action 2>
```

## Quality gate

- [ ] The recommendation identifies the three-sided value proposition.
- [ ] Both sides' economic commitments and failure costs are explicit.
- [ ] The leverage source is ranked using requirement, economic, competitive, customer, or co-marketing leverage.
- [ ] The partner tier matches strategic fit and partner capability without over-tiering.
- [ ] The Crawl, Walk, or Run phase has concrete metrics and Go/no-go gates.
- [ ] The charter covers goals, value exchange, timeline, measurement, governance, and exit criteria.
- [ ] Co-marketing work is tied to adoption and revenue outcomes, not treated as the partnership itself.

## References

- [Original technical product GTM source](https://github.com/beingsmit/technical-product-gtm)
- [Author profile](https://linkedin.com/in/smitkpatel)
