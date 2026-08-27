---
name: gtm-ai-gtm
description: >-
  Create go-to-market strategy for AI products, including enterprise positioning, buyer readiness,
  trust sequencing, variable-cost pricing, and copilot/agent/teammate framing. Use this skill when
  positioning AI products, handling production-responsibility objections, pricing variable-cost
  AI, or selling autonomous tools into enterprises.
license: MIT
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

<!-- Generated from harness/github-copilot/plugins/go-to-market/skills/gtm-ai-gtm/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AI product GTM

Turn an AI product, buyer concern, pricing problem, or enterprise sales blocker into positioning, qualification, demo, trust, and pricing recommendations for AI go-to-market and to-market execution.

## When to invoke

- "How do we position this AI product?"
- "Buyers say they're worried about AI breaking production."
- "Should we call it autonomous, agent, copilot, or teammate?"
- "How do we price AI when usage varies 10x by customer?"
- "Enterprise security passed but ops rejected us; why?"

## Positioning decisions

Use wording that matches buyer risk tolerance rather than internal architecture pride.

```text
Does your AI act autonomously with no approval per action?
├─ Yes → Who are you selling to?
│   ├─ Developers → "Agent" framing
│   └─ Enterprises → "Teammate" framing
└─ No → "copilot" framing
```

| Framing | Use when | Avoid when |
| --- | --- | --- |
| copilot | The AI suggests and a human approves each action. | The product actually takes unsupervised action. |
| Agent | Technical developer buyers expect automation and can inspect failure modes. | Enterprise buyers hear "autonomous" as unmanaged risk. |
| Teammate | Enterprise buyers need accountability, escalation, and control language. | The product is only a passive recommendation widget. |

Prefer words like teammate, augments, accelerates, and you stay in control. Avoid leading with autonomous, replaces, fully automated, or AI-first when the buyer has not accepted the operating model.

## Buyer readiness and trust ladder

Qualify AI-agent buyers by operational maturity, not by enthusiasm.

```text
Do they have incident response processes for tool failures?
├─ Yes → Continue
│   └─ Do they have on-call rotations for production systems?
│       ├─ Yes → Qualified buyer
│       └─ No → Help them build it first
└─ No → Not ready; come back in 6 months
```

The real objection behind "will it break production?" is "who is responsible when it does?" Map the answer to the buyer's operating model.

| Enterprise objection | Map it to |
| --- | --- |
| "Who gets paged when AI breaks production?" | Their on-call rotation. |
| "Who debugs AI failures?" | Their incident response process. |
| "Who owns customer communication?" | Their escalation path. |

Trust sequence matters: Transparency → Control → Performance → Scale. Provide model cards, security notes, and explainability before the demo; then show approval workflows, kill switches, and confidence scores; then benchmarks, case studies, and live demo; then enterprise deployments, compliance, and SLAs.

## Pricing and demo patterns

```text
Can you measure customer outcomes reliably?
├─ Yes → Outcome-based, or hybrid with outcome component
└─ No → Does usage vary 5x+ by customer?
    ├─ Yes → Hybrid: base + usage
    └─ No → Seat-based
```

Pricing hybrid formula:

```text
Base: $X/month (covers fixed costs)
Variable: $Y per unit (20-30% of customer's alternative cost)
```

Demo structure:

1. Problem with quantified cost (30s).
2. AI attempt including failure or uncertainty (60s).
3. Human review and override (30s).
4. Outcome with ROI (30s).

Show mistakes plus recovery. That builds more trust than a perfect AI demo that looks staged because buyers know real-world data is messy. Name failure/uncertainty explicitly.

## Common mistakes

| Mistake | Why it loses deals | Correction |
| --- | --- | --- |
| Using "autonomous" because it sounds impressive | It scares enterprises and slows deals. | Use "teammate" once the product takes action. |
| Hiding AI failure modes | Buyers assume missing failure examples are being concealed. | Show failures, recovery, and ownership. |
| Treating "will it break production?" as the objection | The buyer is asking about responsibility. | Map failure ownership to incident response and on-call. |
| Pricing usage-based AI like OpenAI | Your cost structure and customer value are different. | Price for 20-30% of the customer's alternative cost. |
| Skipping transparency docs before demo | Buyers need proof before performance claims. | Sequence Transparency → Control → Performance → Scale. |
| Demoing perfect AI | Fake perfection reduces trust. | Include uncertainty, review, and override. |
| Selling to buyers demanding 100% accuracy | They are not ready for agentic AI. | Filter for mature buyers with incident response. |

Also preserve the ceiling-moment qualification insight: when a buyer cannot define responsibility for failures, the deal has hit an operating-model ceiling rather than a feature objection.

## Progressive disclosure and bundled resources

- `references/core-frameworks.md`: detailed AI go-to-market frameworks and examples for full GTM strategy work.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `positioning-strategy` | skill | You need general positioning frameworks outside AI-agent GTM. |
| `technical-product-pricing` | skill | You need broader pricing model work beyond AI variable-cost patterns. |
| `enterprise-account-planning` | skill | You need account strategy for enterprise AI deal management. |

## Output template

```markdown
## AI GTM recommendation — <product or deal>

**Positioning:** copilot | agent | teammate
**Buyer readiness:** qualified | needs operating model | not ready
**Pricing model:** seat-based | hybrid base + usage | outcome-based

| Decision | Recommendation | Rationale | Evidence needed |
| --- | --- | --- | --- |
| Framing | <copilot/agent/teammate wording> | <why it fits buyer risk> | <proof to gather> |
| Trust sequence | <next trust asset> | <why now> | <doc, demo, benchmark, SLA> |
| Pricing | <model and unit> | <cost/value logic> | <usage, alternative cost, outcome metric> |

### Demo plan
1. <30s problem and quantified cost>
2. <60s AI attempt with failure or uncertainty>
3. <30s human review or override>
4. <30s ROI outcome>
```

## Quality gate

- [ ] The recommendation chooses copilot, agent, or teammate framing with buyer-specific rationale.
- [ ] Production-responsibility objections are mapped to on-call, incident response, and escalation ownership.
- [ ] Trust assets follow Transparency → Control → Performance → Scale.
- [ ] Pricing accounts for 5x+ or 10x usage variance and uses 20-30% of alternative cost when relevant.
- [ ] The demo plan includes failure or uncertainty plus recovery.
- [ ] Buyer readiness is qualified before recommending autonomous or teammate messaging.

## References

- [technical-product-gtm source](https://github.com/beingsmit/technical-product-gtm)
- [Smit Patel](https://linkedin.com/in/smitkpatel)
