# AI go-to-market core frameworks

Moved from `../SKILL.md` for progressive disclosure. Use this reference only when the activated workflow needs the detailed material below.

## Core Frameworks

### 1. The Real Enterprise AI Objection (It's Not What You Think)

**What I Learned Selling Autonomous AI Agents:**

Three months in, enterprise security reviews were passing fast. Good sign, right? Then the pattern emerged: security approved, but **operations rejected us**.

The objection wasn't "will the AI break production?" — they *assumed* it would break production eventually. The real question was:

**"Who's responsible when the agent does something wrong?"**

Not "do we trust the agent?" — "do we trust our *team* to handle this?"

**Why This Matters:**

Autonomous agents create a new operational burden. You're not selling AI capability, you're selling organizational readiness. When your agent halts production at 2am, who gets paged? Who fixes it? Who explains it to the VP?

**Framework: The Accountability Cascade**

Before deploying AI agents, enterprises need clear answers:

1. **L1 Response**: Who monitors the agent? (24/7 ops team, or dev team on-call?)
2. **L2 Escalation**: When agent action fails, who debugs? (Agent team, or product team?)
3. **L3 Ownership**: When something breaks badly, who owns customer communication?

If you can't answer all three, **they won't buy**. Doesn't matter how good your AI is.

**How This Changes Your Sales Process:**

**Old approach:**
- Demo the AI
- Show accuracy metrics
- Talk about ROI

**New approach:**
- Demo the AI
- Show the *failure modes* explicitly
- Ask: "Who on your team would handle this scenario?"
- Walk through their incident response process
- Map AI failures to their existing runbooks

**The Qualification Question:**

"Walk me through what happens when the agent takes an action that breaks a workflow. Who gets alerted? Who investigates? Who decides whether to roll back or fix forward?"

If they can't answer, they're not ready. Pause the deal and help them build the process first.

**Common Mistake:**

Treating this as a *product* objection ("we'll make the AI more accurate"). It's an *organizational* objection. More accuracy doesn't solve "who owns this at 2am?"

**Pattern I've Seen Work:**

Companies that succeed with AI agents already have:
- On-call rotations for production systems
- Incident response playbooks
- Blameless postmortem culture
- Clear escalation paths

Companies that struggle:
- Manual deployment processes
- Hero culture ("Steve fixes everything")
- No formal incident response
- Blame-focused culture

**Decision Criteria:**

Before demoing autonomous AI to enterprises, ask yourself: "If this breaks their production, who on *their* team owns the fix?" If you can't answer, they can't buy.

---

### 2. Copilot vs Agent vs Teammate (Three Different GTM Motions)

**The Positioning Trap:**

Early enterprise conversations, we positioned as "autonomous AI agent." Buyers flinched. One word change — "autonomous" → "AI teammate" — and deal progression improved measurably.

Why? **Word choice shapes buyer psychology.**

**The Three Framings:**

**1. Copilot (Safest, Lowest Value)**
- **What it means**: AI suggests, human decides every time
- **Buyer psychology**: Feels safe, non-threatening
- **GTM motion**: Developer adoption, bottoms-up
- **Use case**: Code completion, writing assistance, search
- **Objection**: "Is this worth paying for?" (low perceived value)

**2. Agent (Scariest, Highest Value)**
- **What it means**: AI acts autonomously, human reviews periodically
- **Buyer psychology**: Scary, implies replacing humans
- **GTM motion**: Enterprise sales, top-down
- **Use case**: Batch processing, automated workflows, ops
- **Objection**: "What if it breaks production?" (accountability fear)

**3. Teammate (Sweet Spot)**
- **What it means**: AI and human collaborate, split the work
- **Buyer psychology**: Partnership, not replacement
- **GTM motion**: Hybrid (dev adoption + manager approval)
- **Use case**: Most AI agent platforms
- **Objection**: "How do we integrate this into our workflow?" (process question)

**The Positioning Shift:**

**Before:** "Autonomous AI agent that handles complex workflows end-to-end"
- Developers: "Cool, but scary"
- Managers: "Will this replace our team?"
- Deal progression: Slow

**After:** "AI teammate that pairs with your engineers on complex tasks"
- Developers: "This helps me"
- Managers: "This makes my team more productive"
- Deal progression: Three enterprise deals that had stalled 4+ months closed within 8 weeks of the shift

**Specific Language Choices That Mattered:**

❌ **Don't say:**
- "Autonomous" (scary)
- "Replaces" (threatening)
- "Fully automated" (no control)
- "AI-first" (what does that even mean?)

✅ **Do say:**
- "Teammate" (collaborative)
- "Augments" or "Accelerates" (helping, not replacing)
- "You stay in control" (reassuring)
- "Handles the repetitive work" (specific value)

**How to Choose Your Framing:**

```
Does your AI make decisions without human approval?
├─ Yes → Are you selling to developers or enterprises?
│   ├─ Developers → "Agent" framing (they want autonomous)
│   └─ Enterprises → "Teammate" framing (they want control)
└─ No → "Copilot" framing (augmentation, not automation)
```

**The Hard Truth:**

You can build an agent but position it as a copilot. You can't build a copilot and position it as an agent. **Product capabilities set a ceiling, positioning chooses where you land below it.**

**Common Mistake:**

Using "autonomous" because it sounds impressive. Impressive ≠ trusted. If buyers flinch at your positioning, you've lost them.

---

### 3. The AI Pricing Problem (When Usage Varies 10x)

**The Pattern:**

Every AI company I've worked with faces this: Customer A uses 1,000 API calls/month. Customer B uses 10,000. Do you charge Customer B 10x more? If yes, they churn. If no, your margins collapse.

**The Three Models:**

**1. Seat-Based ($X per user/month)**
- **When it works**: AI augments human work predictably
- **Example**: Code completion, writing assistant
- **Problem**: Doesn't capture AI value scaling
- **Real risk**: High-usage customers are your best customers, but they subsidize low-usage ones

**2. Usage-Based ($X per API call / prediction / hour)**
- **When it works**: AI does variable work, customers understand the unit
- **Example**: Image generation, transcription, batch ML
- **Problem**: Sticker shock for high-usage customers
- **Real risk**: Customers optimize to use *less* of your product

**3. Outcome-Based ($X per outcome achieved)**
- **When it works**: You can measure outcomes reliably
- **Example**: "Pay per bug fixed" or "Pay per support ticket resolved"
- **Problem**: Hard to measure, easy to game
- **Real risk**: You bear all the risk if AI doesn't perform

**What Actually Works (Hybrid):**

Base fee (covers fixed costs) + variable fee (scales with value).

**Example structure:**
- Base: $X/month per team (access to platform)
- Variable: $Y per successful action/outcome
- Why this works:
  - Base covers infra/support costs
  - Variable aligns with customer value
  - High-usage customers aren't punished (they're getting more value)

**The Pricing Conversation I Wish I'd Had Earlier:**

When pricing usage-based AI:

**Ask the customer:**
"How much would it cost you to do this manually?"

If it's $0.10 per API call but saves them $2 in labor, you're underpriced. If it costs $0.50 per call but saves them $0.40, they won't use it enough to matter.

**Pricing Rule:**

Your variable cost should be **20-30% of customer's alternative cost**. High enough to capture value, low enough that they'll use it liberally.

**Common Mistake:**

Copying OpenAI's pricing ($0.01 per 1K tokens) because "that's what everyone does." Your cost structure isn't OpenAI's cost structure. Your value isn't OpenAI's value. Price for *your* business.

---

### 4. The AI Trust Ladder (From Someone Who Climbed It)

**The Pattern:**

You can't sell AI by saying "trust us, it works." You build trust in stages.

**First: Transparency (Before First Demo)**

Send these three docs before they ask:
- Model card (what model, trained on what, accuracy on what benchmarks)
- Security whitepaper (where data goes, how it's processed)
- Explainability doc (how to interpret AI decisions)

**Why this works:**
Buyers expect to do diligence. If you send docs *before they ask*, you look confident and credible.

**Second: Control (In the Demo)**

Show them the safety mechanisms:
- How users approve/reject AI suggestions
- Kill switches and rollback mechanisms
- Confidence scores and when AI says "I'm not sure"

**Why this works:**
Fear of "runaway AI" is real. Showing control mechanisms proves you thought about failure modes.

**Third: Performance (Week 4-8)**

Prove it works:
- Benchmarks vs baseline (human or previous tool)
- Case study from similar company
- Live demo on their data (if possible)

**Why this works:**
Proof beats promises. One customer saying "we saved X hours/week" is worth 100 marketing claims.

**Fourth: Scale (When They're Serious)**

Show enterprise readiness:
- Enterprise deployment examples
- Performance at scale (latency, throughput, error rates)
- Compliance docs (SOC 2, GDPR, etc.)

**Why this works:**
Enterprises don't deploy MVPs. They need proof you won't fall over at 1000 users.

**The Mistake I Made:**

Trying to prove performance before explaining how the AI worked. Buyers didn't trust the benchmarks because they didn't understand the system. **Order matters.**

**Decision Criteria:**

If buyers ask "how does this work?" before you've demoed, you skipped transparency. Back up and send the docs.

---

### 5. The Enterprise AI Demo (Show Failure, Not Just Success)

**What Doesn't Work:**

Canned demo where AI magically solves everything. Buyers think "this won't work on our messy data."

**What Works:**

Show the AI making a mistake and recovering. Seriously.

**Demo Structure That Works:**

**1. The Problem (30 seconds)**
"Your engineers spend hours on [specific task]. Here's what that looks like."
- Show: Current manual workflow
- Quantify: Time × Engineers × Weeks = Total cost

**2. The AI Attempt (60 seconds)**
"Here's the AI handling the same task."
- Show: AI analyzing, taking action
- **Key move**: Have AI encounter an error or uncertainty
- Show: AI re-analyzing, recovering, or asking for help
- **Narrate**: "Notice it didn't get it perfect first time. It handles uncertainty like a human would."

**3. The Human Review (30 seconds)**
"Here's where the engineer reviews and approves."
- Show: Engineer examining AI's work
- **Key move**: Show the engineer overriding or adjusting something
- **Narrate**: "Human stays in control. AI handles repetitive work, human handles judgment calls."

**4. The Outcome (30 seconds)**
"[X hours] → [Y minutes]. Engineer still owns the outcome, AI accelerates execution."
- Quantify: Time reduction, cost savings, capacity freed

**Why This Works:**

- Showing failure → Builds trust (you're not hiding anything)
- Showing recovery → Proves AI is robust
- Showing human override → Gives them control
- Quantifying savings → Makes ROI concrete

**The Pattern I've Seen:**

Demos with perfect AI → Buyers skeptical
Demos with imperfect AI that recovers → Buyers engaged

**Common Mistake:**

Cherry-picking examples where AI is 100% accurate. Buyers know real-world data is messy. If you don't show messiness, they assume you're hiding it.

---

### 6. The "Who Owns This?" Objection Handler

**The Objection:**

"This looks great, but what happens when the AI does something wrong?"

**Bad Answer:**
"Our AI is 95% accurate, and we're improving it every week."
(Translation: "It will break production 5% of the time, good luck with that")

**Good Answer:**
"Great question. Let's walk through a failure scenario together."

**Then Ask:**

1. "When the AI takes an action that causes an error, who on your team investigates?"
2. "Do you have an incident response process for tooling failures?"
3. "Who owns rollback decisions — the engineer who approved it, or the ops team?"

**What This Does:**

- Shifts from "will it fail?" (yes, it will) to "how do we handle failures?"
- Makes them think through operational readiness
- Reveals whether they're ready for AI agents

**The Follow-Up:**

"Here's what we recommend: Start with low-risk environments. Let the AI handle non-critical workflows for 2-4 weeks. See how your team handles its mistakes. Then expand scope when you're confident in the process."

**Why This Works:**

You're not selling perfection. You're selling a tool that requires operational maturity. **Filtering for mature buyers is better than convincing immature ones.**

**The Pattern:**

Mature buyers say: "We already have runbooks for tool failures, we'll add AI to them."
Immature buyers say: "Can you make it never fail?"

**Decision Criteria:**

If a buyer demands 100% accuracy, walk away. They're not ready. Come back when they have incident response processes.

---

### 7. The AI Positioning Trap (Fighting Asymmetric Wars)

**The Pattern:**

You're competing in the AI agent space. Every competitor's homepage says the same thing: "Automate [workflow] with AI." Your differentiation requires explaining complex technical benchmarks that buyers don't understand.

This is the positioning trap: **competing on features against better-funded companies on their battlefield.**

**How to Diagnose It:**

1. Collect homepage messaging from 5-7 direct competitors
2. Identify shared claims (these are commoditized — you can't win here)
3. Map where you have structural advantage (not just product features)
4. Find the position competitors can't easily copy

**Structural advantages that work for AI positioning:**
- Unique data or workflow ownership (you control something competitors can't replicate)
- Deployment flexibility (on-prem, private cloud, customer-controlled infrastructure)
- Pricing model innovation (outcome-based, usage-based when competitors are seat-based)
- Community or ecosystem (network effects that compound over time)

Feature advantages that don't last:
- "Better accuracy" (competitors catch up in one sprint)
- "Faster inference" (infrastructure commoditizes)
- "More integrations" (easy to copy)

**The Test:**

For every positioning claim, ask: Can a competitor copy this with a single product sprint? If yes, it's not defensible. Don't build your GTM on it.

**Common Mistake:**

Claiming you're "better" at what everyone does. In AI, benchmarks change monthly. Position on what's structurally different about your approach, not what's temporarily better about your model.

---

### 8. Ceiling Moment Qualification (Finding High-Intent AI Buyers)

**The Pattern:**

The highest-intent enterprise buyers for AI agents are people who've already adopted a comparable tool and hit its limits. They've invested in learning, they understand the problem space, and they have a clear business case for the upgrade.

**How to Identify Ceiling Moments:**

The prospect has:
- Used a copilot/assistant tool for 6+ months
- Hit its limitations (can't handle complex tasks, doesn't work with their stack, not autonomous enough)
- Low switching costs (the mental model transfers)
- Clear business case ("we're spending X hours on this manually even with the current tool")

**How to Target Them:**

1. Identify the tool(s) your AI product complements or displaces
2. Build target lists of companies known to use those tools
3. Craft outreach around the limitation, not your features:
   - "Teams using [incumbent] often hit a ceiling when they need [capability your product provides]"
   - Acknowledge the incumbent has value (don't trash-talk)
   - Position as "next level," not replacement

**Why This Converts Better:**

Ceiling-moment conversations convert 3-5x vs cold outreach because:
- Prospect already understands the problem
- They've already invested in the category
- They have internal budget allocated
- They can articulate what's missing

**The Qualification Question:**

"What's the most complex task you've tried to automate with your current tool, and where did it break down?"

If they have a specific answer with specific pain, they're a ceiling-moment buyer. If they say "it works fine," they're not ready.

**Common Mistake:**

Trying to convince tool-naive prospects to adopt AI agents. Bad conversion rates, long education cycles, and they'll compare you to "doing nothing" instead of "doing it better." Target buyers who already believe in the category.

---

