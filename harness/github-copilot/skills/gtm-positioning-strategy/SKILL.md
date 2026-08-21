---
name: gtm-positioning-strategy
description: >-
  Diagnose and improve go-to-market positioning by auditing competitor messaging, finding defensible differentiation, testing claims, and planning Crawl-Walk-Run rollout. Use when messaging sounds like competitors, conversion is weak despite awareness, sales cannot explain differentiation, buyers see the product as interchangeable, or a team wants to test positioning before rebrand.
license: MIT
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

# GTM positioning strategy

Turn generic product messaging into a defensible market position. Audit competitive language, identify structural advantage or under-served segments, test word choice and claims with real buyers, and return a rollout plan that reduces rebrand risk.

## When to invoke

- "Our messaging sounds exactly like competitors."
- "Brand awareness is strong but conversion is weak."
- "Sales cannot explain why we are different."
- "Buyers see us as interchangeable."
- "How do we test positioning claims before a rebrand?"

## Positioning diagnosis

| Symptom | Diagnosis | Action |
| --- | --- | --- |
| Competitors all claim "fastest", "most reliable", or "easiest to use" | Table-stakes language, not differentiation | Collect 5-7 homepage headlines and mark shared claims as commoditized. |
| Differentiation requires complex technical explanation | Positioning is too feature-led | Translate the feature into a buyer outcome, segment, or workflow claim. |
| Strong awareness but weak pipeline/conversion | Market knows the company but not why to choose it | Test a sharper category, segment/use case, or pain-specific claim. |
| Sales calls derail into comparison questions | Buyers see the product as interchangeable | Equip sales/product with a clear contrast narrative and proof. |
| Existing customers reject the new description | Repositioning overreaches the product | Rework until customers still recognize what the product does. |

A positioning problem is not fixed by saying "better." Find what the product can own now, what competitors cannot copy quickly, and what the best customers already value.

## Word choice and buyer psychology

The autonomous AI example shows why one word matters. "Autonomous AI agent" made developers think "cool, but scary" and managers worry about team replacement. Reframing the same capability as "AI teammate" made developers hear "this helps me" and managers hear "this makes my team more productive," improving enterprise deal progression.

| Avoid when selling to enterprises | Why it scares buyers | Prefer | Why it converts |
| --- | --- | --- | --- |
| Autonomous | Implies no control and human replacement | Teammate | Implies collaboration and help. |
| Replaces | Threatens job security | Augments | Makes humans better. |
| Fully automated | Removes human judgment | You stay in control | Reassures human oversight. |
| AI-first | Sounds vague or buzzword-driven | Handles repetitive work | Names the specific work removed. |

Positioning is what you do not say as much as what you say. A technically true claim such as "replaces developers" can kill enterprise deals if it triggers risk, loss of control, or headcount anxiety.

## Crawl-Walk-Run rollout

| Phase | Duration | Purpose | Actions | Measurement | Go/No-Go |
| --- | --- | --- | --- | --- | --- |
| Crawl | 1-2 weeks | Validate without product/org commitment | A/B test homepage headlines, run two outbound email sequences, ask customers whether the new description still fits | Website CTR, outbound reply rate, qualitative recognition | Move on if at least one variant beats incumbent by 20%+ and customers do not say "wait, that is not what you do." |
| Walk | 2-3 weeks | Align before public rebrand | Rewrite homepage, enterprise pages, CTAs, pitch deck, call scripts, email templates, documentation, and use-case-specific examples | Sales usability feedback, engagement by segment, no major confusion | Move on if sales says messaging is easier and metrics improve. |
| Run | 2-3 weeks and ongoing | Scale the validated position | Launch landing pages, run outbound campaigns by angle, update all customer-facing materials, train customer success, announce if appropriate | Pipeline volume, win rate, CAC efficiency, retention | Continue if conversion improves without churn or recognition loss. |

Do not run phases in parallel; mid-rollout messaging inconsistency makes results unreadable. Product work should follow validated positioning, not block it forever.

## Testing hierarchy

| Test | Sample | Measures | Signal strength | Use when |
| --- | --- | --- | --- | --- |
| Outbound Email A/B | 100 prospects per variant | Reply rate and meetings booked | High | Need real buyer intent before committing. |
| Sales call scripts | Half of AEs use A, half use B | Demo-to-trial conversion | High | Sales team can run controlled scripts. |
| Website homepage A/B | Current vs new headline and sub-headline | CTR on key CTAs | Moderate | Need fast market interest data. |
| Existing customer prompt | "If we described ourselves as [new positioning], would you still recognize us?" | Recognition and confusion | Qualitative | Avoid customer churn and category whiplash. |

Do not choose a winner by internal consensus. Your team is not the buyer.

## Positioning architecture

| Layer | Question | Output |
| --- | --- | --- |
| Market context | What problem is the market experiencing, why now, and what happens if it remains unsolved? | A short narrative about urgency and consequences. |
| Positioning statement | Who do we serve, what problem do we solve, how are we different, and why should buyers believe us? | One or two sentences. |
| Narrative | Why is the world changing, why do existing solutions fail, why is our approach better, and what future do we enable? | Sales and marketing story. |

Headline formats that keep the claim testable:

| Format | Example shape | Watch out for |
| --- | --- | --- |
| `The [adjective] [category] that [differentiator]` | `The customizable platform for [workflow]` | Do not cram in multiple benefits. |
| `[Product] for [specific use case]` | `Infrastructure for autonomous teams` | Ensure the segment is real and reachable. |
| `[Product] that [core benefit]` | `The enterprise-grade alternative to [incumbent]` | Avoid defensive competitor-name positioning unless the comparison is strategic. |

Use the sub-headline to clarify who, why, and how the product differs from status quo: "Deploy anywhere. Scale instantly. Your infrastructure, your rules." or "Enterprise-grade. No lock-in. Works with your existing stack."

Prefer specific, real-time operational proof over vague superlatives. Avoid generic best-in-class language unless independent evidence makes the claim believable.

## Defensibility assessment

| Positioning basis | Strength | Decision rule |
| --- | --- | --- |
| Structural advantage | Strongest | Use when competitors cannot copy the claim with a sprint: unique data ownership, on-prem deployment, deployment flexibility, pricing model, or network effects. |
| Market position | Strong if first | Use when the company can credibly own a category before copycats react. |
| Product feature | Weak | Avoid as the primary claim when competitors can match it quickly. |

Ask four questions for every claim:

- Can a competitor copy this with one product sprint? If yes, it is not defensible.
- Do we have a structural advantage? If no, treat it as temporary.
- Is it credible with the current product? If no, do not claim it yet.
- Can we own it before competitors react? If no, narrow the segment.

## Decision trees

```text
Should we reposition?
Is brand awareness strong but conversion weak?
├─ Yes → Positioning problem; test new angles.
└─ No → Does our messaging sound like competitors?
   ├─ Yes → Positioning problem.
   └─ No → Not primarily positioning.
```

```text
Which angle should we test?
Do we have structural advantage competitors cannot copy?
├─ Yes → Position on structural advantage.
└─ No → Are we first in a category?
   ├─ Yes → Position on category ownership.
   └─ No → Find an under-served segment/use case.
```

```text
Move from Crawl to Walk?
Did new positioning outperform incumbent by 20%+?
├─ Yes → Move to Walk.
└─ No → Did the test run at least two weeks?
   ├─ No → Run longer.
   └─ Yes → Try another angle or keep incumbent.
```

## Common mistakes

| Mistake | Why it fails | Correction |
| --- | --- | --- |
| Claiming to be better at what everyone does | Unbelievable in crowded markets | Choose a different angle. |
| Positioning on easily-copied features | Creates a treadmill | Anchor on structural advantage or under-served workflows. |
| Waiting for perfect product before positioning | Delays learning | Test claims and let product follow validated messaging. |
| Testing too many angles simultaneously | Cannot attribute results | Test one clear claim at a time. |
| Skipping Crawl | Full rebrand risk is too high | Validate before public commitment. |
| One positioning for every persona | Different buyers care about different outcomes | Tailor proof and examples by persona. |
| Generic "best-in-class", `in-class`, or "innovative" language | Does not differentiate | Use concrete outcomes and proof. |

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `ai-gtm` | skill | The task is AI-specific naming such as copilot, agent, companion, or teammate. |
| `technical-product-pricing` | skill | Price is the positioning signal or packaging strategy. |
| `0-to-1-launch` | skill | A new product launch needs launch sequencing beyond positioning. |

## Output template

```markdown
## Positioning strategy

**Status:** recommended | needs more evidence | blocked
**Current position:** <one sentence>
**Recommended position:** <one sentence>
**Primary risk:** <risk>

### Diagnosis
| Symptom | Evidence | Implication |
| --- | --- | --- |
| <symptom> | <competitor/customer/sales evidence> | <positioning issue> |

### Claim to test
**Headline:** <headline>
**Sub-headline:** <sub-headline>
**Differentiation basis:** structural advantage | market position | feature | under-served segment
**Why it is defensible:** <reason>

### Crawl-Walk-Run plan
| Phase | Test or action | Metric | Go/No-Go |
| --- | --- | --- | --- |
| Crawl | <test> | <metric> | <threshold> |
| Walk | <alignment action> | <metric> | <threshold> |
| Run | <scale action> | <metric> | <threshold> |

### Messaging guardrails
- Say: <words or claims>
- Do not say: <words or claims>
```

## Quality gate

- [ ] Competitor messaging or buyer confusion was used as evidence, not internal preference alone.
- [ ] The recommendation names one primary position rather than multiple simultaneous positions.
- [ ] The position is credible with the current product and mapped to structural advantage, market position, feature, or under-served segment.
- [ ] Scary or vague words are replaced with buyer-safe language when enterprise trust matters.
- [ ] The Crawl phase includes a measurable test and a Go/No-Go threshold, preferably 20%+ improvement over incumbent.
- [ ] Existing customer recognition risk is checked before Walk or Run.
- [ ] The output includes a concrete headline, sub-headline, rollout plan, and messaging guardrails.

## References

- [Source repository](https://github.com/beingsmit/technical-product-gtm)
- [Author profile](https://linkedin.com/in/smitkpatel)
