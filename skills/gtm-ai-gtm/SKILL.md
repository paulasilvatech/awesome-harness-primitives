---
name: "gtm-ai-gtm"
description: >-
  Go-to-market strategy for AI products. Use when positioning AI products, handling "who is
  responsible when it breaks" objections, pricing variable-cost AI, choosing between
  copilot/agent/teammate framing, or selling autonomous tools into enterprises.
license: "MIT"
metadata:
  author: "Smit Patel (https://linkedin.com/in/smitkpatel)"
  source: "https://github.com/beingsmit/technical-product-gtm"
---
# AI Product GTM

Go-to-market strategy for AI products. These aren't generic AI principles — they're patterns from selling autonomous AI agents into enterprises where "autonomous" scared buyers and "teammate" converted them.

## When to Use

**Triggers:**
- "How do we position this AI product?"
- "Buyers say they're worried about AI breaking production"
- "Should we call it autonomous or copilot?"
- "How do we price AI when usage varies 10x by customer?"
- "Enterprise security passed but ops rejected us — why?"

**Context:**
- AI agent platforms (coding, support, ops)
- LLM-based applications
- Autonomous tools that *do* things (not just suggest)
- AI infrastructure
- Anything where the AI makes decisions

---

## Bundled Resources

- [AI go-to-market core frameworks](references/core-frameworks.md) — When developing full GTM strategy content, open this reference for the detailed frameworks and examples.

## Decision Trees

### Which Positioning Should I Use?

```
Does your AI act autonomously (no approval per action)?
├─ Yes → Who are you selling to?
│   ├─ Developers → "Agent" framing
│   └─ Enterprises → "Teammate" framing
└─ No → "Copilot" framing
```

### Which Pricing Model Should I Use?

```
Can you measure customer outcomes reliably?
├─ Yes → Outcome-based (or hybrid with outcome component)
└─ No → Continue...
    │
    Does usage vary 5x+ by customer?
    ├─ Yes → Hybrid (base + usage)
    └─ No → Seat-based
```

### Is This Buyer Ready for AI Agents?

```
Do they have incident response processes for tool failures?
├─ Yes → Continue...
│   │
│   Do they have on-call rotations for production systems?
│   ├─ Yes → Qualified buyer
│   └─ No → Help them build it first
└─ No → Not ready (come back in 6 months)
```

---

## Common Mistakes

**1. Using "autonomous" because it sounds impressive**
   - I've watched this slow deals. "Autonomous" scares enterprises. "Teammate" progresses faster.

**2. Hiding AI failure modes**
   - Buyers know real-world data is messy. If you don't show failures, they assume you're hiding them.

**3. Treating "will it break production?" as the objection**
   - Real objection: "who's responsible when it does?" Organizational readiness, not accuracy.

**4. Pricing usage-based AI like OpenAI**
   - Your cost structure isn't theirs. Price for 20-30% of customer's alternative cost.

**5. Skipping transparency docs before demo**
   - Order matters. Transparency → Control → Performance → Scale. Don't skip steps.

**6. Demoing perfect AI**
   - Show mistakes + recovery. Builds more trust than fake perfection.

**7. Selling to buyers who demand 100% accuracy**
   - They're not ready. Filter for mature buyers with incident response processes.

---

## Quick Reference

**Enterprise objection checklist:**
- [ ] "Who gets paged when AI breaks production?" → Map to their on-call rotation
- [ ] "Who debugs AI failures?" → Map to their incident response
- [ ] "Who owns customer communication?" → Map to their escalation path

**Positioning word choices:**
- ✅ Teammate, augments, accelerates, you stay in control
- ❌ Autonomous, replaces, fully automated, AI-first

**Demo structure:**
1. Problem with quantified cost (30s)
2. AI attempt including failure/uncertainty (60s)
3. Human review and override (30s)
4. Outcome with ROI (30s)

**Trust ladder:**
1. Transparency (model card, security, explainability)
2. Control (approval workflows, kill switches, confidence scores)
3. Performance (benchmarks, case studies, live demo)
4. Scale (enterprise deployments, compliance, SLAs)

**Pricing hybrid formula:**
- Base: $X/month (covers fixed costs)
- Variable: $Y per unit (20-30% of customer's alternative cost)

---

## Related Skills

- **positioning-strategy**: General positioning frameworks and testing
- **technical-product-pricing**: Pricing models including AI-specific patterns
- **enterprise-account-planning**: Enterprise AI deal management

---

*Based on enterprise AI agent GTM across developer tools and infrastructure. Patterns drawn from working enterprise deal cycles selling autonomous AI products — some carried directly, others supported alongside sales leadership — including the positioning trap diagnosis that shifted from feature competition to structural differentiation, the ceiling-moment qualification that improved outbound conversion significantly, and frameworks tested across security, operations, and engineering buyer personas. Not theory — lessons from deals where "autonomous" killed conversations and "teammate" converted.*
