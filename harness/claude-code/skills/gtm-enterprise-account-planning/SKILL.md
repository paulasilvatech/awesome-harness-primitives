---
name: gtm-enterprise-account-planning
description: >-
  Build enterprise account plans, MEDDICC qualification, stakeholder maps, economic-buyer
  validation, deal-health checks, and mutual action plans for complex sales cycles. Use when
  planning strategic enterprise deals, diagnosing stalled opportunities, deciding whether to send
  a proposal, or asking whether a stale MAP means the deal is dead.
license: MIT
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---

<!-- Generated from harness/github-copilot/skills/gtm-enterprise-account-planning/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Enterprise account planning

Strategic account planning turns complex sales cycles into a validated account summary, org chart, MEDDICC opportunity plan, and mutual action plan that shows whether a deal is moving or dying.

## When to invoke

- "How do I plan this enterprise deal?"
- "This deal has been in motion 3 months, why isn't it closing?"
- "Should I create a full account plan or simplified version?"
- "How do I know if this deal is actually moving?"
- "Help me with MEDDICC qualification and a mutual action plan."

## Account-plan depth

Use the full plan for strategic deals above average ACV, multiple stakeholders, sales cycles over 60 days, or complex legal, procurement, and security review. Use a simplified plan for the rest.

```
Is deal size above average ACV?
├─ No → Simplified plan: account summary + MEDDICC + next steps
└─ Yes → Continue...
    │
    Sales cycle >60 days?
    ├─ Yes → Full account plan
    └─ No → Simplified plan
```

| Component | Include | Standard |
| --- | --- | --- |
| Account summary | HQ, size, industry, subsidiaries, technical landscape, tools, platforms, top corporate initiatives, hypothesis: "How can we help?", LinkedIn keyword analysis | Build before first engagement, not after the deal is in motion. |
| Org chart | Name, title, location, LinkedIn, email, phone, notes, domain of responsibility, technical specialties, personal win | Map C-suite, directors, architects, leads, specialists, users, influencers, and blockers. Do not map only the buyer. |
| Opportunity plan | MEDDICC plus issues, risks, mitigation plans, help needed, responsible parties | Validate with the customer; do not fill with assumptions. |
| Mutual Action Plan | Action, your owner, customer owner, others involved, due date, status complete/in-progress | Use it as the running agenda for check-ins. If only your team has actions, it is a demo, not a deal. |

## Deal health and MAP discipline

The Mutual Action Plan is the strongest deal-health signal. Pipeline stage, verbal commitments, and "they love the product" are weaker than customer action.

| Signal | Green | Yellow | Red |
| --- | --- | --- | --- |
| MAP update cadence | Updated weekly | Updated bi-weekly | 3+ weeks stale |
| Ownership | Both sides have actions | Mostly your actions | Only your side has action items |
| Customer movement | Customer completing tasks on schedule | Customer slow to respond | Customer tasks pending for weeks |
| Stakeholders | New stakeholders appearing in MAP | Limited new access | No new stakeholders engaged |
| Dates | Dates moving up or holding | Dates slipping | All dates in the past |

```
Is MAP being updated weekly?
├─ Yes → Healthy
└─ No → Continue...
    │
    Has it been >3 weeks since last MAP update?
    ├─ Yes → Dead deal: qualify out or reset
    └─ No → At risk: escalate to champion
```

### Three-week MAP rule

- Week 1 of silence: send a MAP update: "Here's what we've completed. What's your status on <specific customer action>?"
- Week 2 of silence: escalate to the champion: "Haven't heard back on MAP. Are we still on track for <date>? If priorities shifted, let me know."
- Week 3 of silence: qualify out or reset: "It seems like timing might not be right. Should we pause and reconnect in <timeframe>, or is there a blocker I can help with?"

Do not keep deals in pipeline because "they said they want it." Verbal interest is not action. A stale MAP equals a stale deal.

## Economic-buyer validation

Deals often die at week 8 after a strong POC because the proposal reaches an economic buyer who has not agreed to the problem, ROI, risk, or strategic alignment.

| Role | What they do | What they do not do |
| --- | --- | --- |
| Champion | Influences, coaches, and sells internally on your behalf | Make the final purchase decision alone |
| Technical lead | Validates feasibility, integrations, and implementation risk | Own budget allocation |
| Economic Buyer | Controls budget allocation, makes final purchase decision, signs the contract | Absorb a price tag with no context |

Validate these before sending a proposal:

- [ ] Economic Buyer identified by name and title, confirmed by the champion.
- [ ] Economic Buyer met at least by video call; in-person is better.
- [ ] Economic Buyer agrees on the problem in their own words.
- [ ] Economic Buyer agrees on success metrics and how ROI will be measured.
- [ ] Economic Buyer knows the price range before seeing the final proposal.
- [ ] Economic Buyer understands implementation, go-live, and value-realization timeline.

```
Have you met the Economic Buyer?
├─ No → Do not send yet; get EB access first
└─ Yes → Continue...
    │
    Does EB agree on problem and success metrics?
    ├─ Yes → Send proposal
    └─ No → Align with EB before sending
```

Ask the champion: "Before we finalize pricing, I'd love 15 minutes with <EB name> to make sure we're aligned on outcomes and timeline. Can you intro us?" If the champion blocks with "I can handle that, you don't need to talk to them," treat it as a red flag: they may lack EB access or fear the EB will kill the deal. Push back with value-context language, especially for deals over $50K.

## MEDDICC qualification

| Letter | Validate | Evidence to capture |
| --- | --- | --- |
| M - Metrics | How the customer measures success | Success criteria agreed with the Economic Buyer. |
| E - Economic Buyer | Who has budget authority | Name, title, meeting date, problem validation, price-range awareness. |
| D - Decision Criteria | What criteria decide the outcome | Technical, business, and political rubric. |
| D - Decision Process | How buying happens | Procurement, legal, security review, approvals, sequence, and owners. |
| I - Identified Pain | The articulated business pain | Customer's words, not your summary. |
| C - Champion | Who sells for you internally | Evidence they have influence, access, and personal motivation. |
| C - Competition | Alternatives under evaluation | Incumbent, build-vs-buy, no-decision risk, and competitive dynamic. |

Do not advance stages based on activity. Advance only when exit criteria are met.

| Stage | Activity | Exit criteria |
| --- | --- | --- |
| Stage 0 — Pipeline Generation | Prospecting | Qualified interest confirmed. |
| Stage 1 — Discovery | Environment, pain, requirements | Pain identified and stakeholders mapped. |
| Stage 2 — Demonstrating | Demo and champion building | Champion identified. |
| Stage 3 — Proving Value | POC or trial | Technical validation and POC success criteria complete. |
| Stage 4 — Proposal | Pricing, terms, scope | Proposal delivered after EB alignment. |
| Stage 5 — Paper Process | Legal, procurement, security | Approvals secured. |
| Stage 6 — Closed Won | Signature | Customer-success handoff. |

## Stakeholder and personal-win mapping

Committees do not buy; people buy. Map professional wins, professional risks, and personal motivations for every stakeholder.

| Dimension | Questions | Example for VP of Engineering |
| --- | --- | --- |
| Professional win | What do they get credit for? What pain goes away? How do they look good? | Reduce on-call burden, improve incident response, improve QBR uptime metrics, attract better engineering talent. |
| Professional risk | What happens if this fails? What is their reputation cost? Who is skeptical? | Team rejects tool, migration causes downtime, vendor fails after she selected it. |
| Personal motivation | New in role? Budget pressure? Promotion path? Burned by vendors? | New in role for 6 months, under pressure to improve uptime, previous monitoring tool failed. |

Turn generic value into personal value. "Our platform improves incident response time by 40%" becomes: "You mentioned on-call burden is burning out your team. Teams often reduce on-call pages by 40% in the first month, which helps retention, and the improved response time appears in QBR dashboards."

Use these questions:

- "What does success look like for you personally?"
- "What happens to your team if this works? If it doesn't?"
- "What are you being measured on this year?"
- "Who internally is skeptical? Why?"

## LinkedIn keyword analysis

Before engaging a strategic account, quantify their investment in your domain with LinkedIn searches.

| Step | Action | Interpretation |
| --- | --- | --- |
| 1 | Define 8-10 category terms, technical roles, and workflow keywords. | Avoid job-title-only searches because titles vary wildly. |
| 2 | Search LinkedIn for "<company name> + <keyword>" and record counts. | 120 DevOps results signals mature DevOps; 5 signals early maturity. |
| 3 | Map concentrations by location and department. | Concentrated teams identify where to target. |
| 4 | Compare counts to total employee count and refresh quarterly. | Hiring trends change and maturity is relative to company size. |

If a company has 50 employees with SRE in profiles, lead with reliability, uptime, and incident reduction. If it has 0, do not lead with an SRE value proposition.

## Common mistakes

| Mistake | Why it hurts | Correction |
| --- | --- | --- |
| Creating account plan too late | The first engagement is already unguided. | Build it before first contact. |
| MEDDICC filled with assumptions | Forecast and deal strategy become fiction. | Validate every element with the customer. |
| Stale Mutual Action Plan | Customer is not doing work. | Escalate at week 2; reset or qualify out at week 3. |
| Mapping only the buyer | Influencers, users, and blockers surprise you later. | Build the full org chart. |
| Ignoring personal wins | Business ROI alone may not motivate the humans buying. | Attach career, reputation, and workload wins to each stakeholder. |
| Skipping champion validation | You are selling alone. | Confirm the champion has influence, access, and willingness to sell internally. |
| Advancing stages by activity | A demo is not a POC and a POC is not EB approval. | Require stage exit criteria. |

## Terminology and preserved deal signals

Use these exact terms when they fit the account context: mid-market, check-in cadence, POC/trial validation, Environment/pain/requirements discovery, Issues/Risks mitigation, Green/yellow/red deal status, procurement/legal/security process, problem/solution alignment, career/reputation motivations, risk-averse stakeholders, and uptime/incident outcomes.

## Related primitives

| Name | Type | Use it when |
| --- | --- | --- |
| `enterprise-onboarding` | skill | The deal is closed and implementation, adoption, and customer-success handoff are the task. |
| `partnership-architecture` | skill | The opportunity depends on partner relationships, channel motion, or ecosystem strategy. |
| `technical-product-pricing` | skill | The account plan needs enterprise pricing, packaging, discounting, or commercial strategy. |

## Output template

```markdown
## Enterprise account plan - <account>

**Status:** healthy | at risk | reset required | qualify out
**Plan depth:** full account plan | simplified plan
**Deal stage:** Stage <0-6> - <name>

### Account summary
- Company: <HQ, size, industry, subsidiaries>
- Technical landscape: <infrastructure, tools, platforms>
- Corporate initiatives: <top initiatives>
- Hypothesis: <how we can help>
- LinkedIn keyword signals: <keywords, counts, departments, interpretation>

### Stakeholders and personal wins
| Person | Role | Influence | Personal win | Risk/blocker | Next action |
| --- | --- | --- | --- | --- | --- |
| <name> | <title> | EB / champion / evaluator / user / blocker | <win> | <risk> | <action> |

### MEDDICC
| Area | Current evidence | Gap | Next validation step |
| --- | --- | --- | --- |
| Metrics | <evidence> | <gap> | <step> |
| Economic Buyer | <evidence> | <gap> | <step> |
| Decision Criteria | <evidence> | <gap> | <step> |
| Decision Process | <evidence> | <gap> | <step> |
| Identified Pain | <evidence> | <gap> | <step> |
| Champion | <evidence> | <gap> | <step> |
| Competition | <evidence> | <gap> | <step> |

### Mutual action plan
| Action | Your owner | Customer owner | Others involved | Due date | Status |
| --- | --- | --- | --- | --- | --- |
| <action> | <owner> | <owner> | <names> | <date> | complete / in-progress / pending |

### Deal-health call
- MAP freshness: <weekly / bi-weekly / 3+ weeks stale>
- EB validation: <complete / incomplete>
- Proposal readiness: <ready / do not send yet>
- Recommendation: <specific action>
```

## Quality gate

- [ ] Plan depth is chosen from deal size, stakeholder complexity, and sales-cycle length.
- [ ] MEDDICC entries are marked as validated evidence or explicit gaps; no assumptions are presented as facts.
- [ ] Economic Buyer access, problem agreement, success metrics, price-range awareness, and timeline are checked before proposal readiness is approved.
- [ ] MAP health uses update cadence, customer-owned actions, stakeholder movement, and due dates.
- [ ] Every stakeholder has a professional win, professional risk, or personal motivation when enough information exists.
- [ ] Stage advancement is tied to exit criteria, not activity volume.
- [ ] Output follows the `## Output template` exactly.

## References

- [technical-product-gtm source](https://github.com/beingsmit/technical-product-gtm)
- [Smit Patel](https://linkedin.com/in/smitkpatel)
