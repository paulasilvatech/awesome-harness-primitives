---
name: technical-job-search
description: >-
  Help software engineers perform active job-search tasks: analyze job descriptions, tailor resumes, write concise cover letters, evaluate offers, and draft interview follow-ups. Use when the user asks to parse a JD, match a CV to a role, write application material, compare compensation, assess offer risk, or prepare post-interview outreach.
license: "MIT"
argument-hint: "Optional: the specific task — e.g. \"analyze this JD\", \"tailor my CV\", \"write cover letter\", \"evaluate this offer\""
---

# Technical job search

Turn a concrete job-search input such as a job description, resume, offer, or interview context into a structured hiring artifact that preserves the user's evidence, reduces generic prose, and produces decision-ready application material.

## When to invoke

- "Analyze this job description for must-haves and red flags."
- "Tailor my CV to this software engineer role."
- "Write a cover letter for this job application."
- "Evaluate this job offer and compensation package."
- "Draft a follow-up email after my interview."

## Inputs

Use `$ARGUMENTS` to determine the requested job-search action when it is provided. If `$ARGUMENTS` is empty, infer the action from the user's pasted material and ask only for missing essentials: job description for tailoring, resume for resume edits, offer details for offer evaluation, or interview context for follow-up email.

## Job description analysis

Separate explicit requirements from recruiter filler. Treat repeated items and words such as "required", "must", "minimum", and "need" as stronger signals than isolated "preferred" or "bonus" phrases.

| Extract | How to classify | Output rule |
| --- | --- | --- |
| Must-haves | Required or repeated technical skills, years of experience, domain knowledge, clearance, location, work authorization, or language requirements. | List as bullets and mark any hard blockers. |
| Nice-to-haves | Preferred, bonus, familiar-with, or mentioned once without being required. | Keep separate so the candidate does not self-reject. |
| Role problem | The business or engineering problem the hire is meant to solve. | Summarize in 2-3 sentences, using evidence from the JD. |
| Seniority signals | Verbs such as build, design, lead, define, mentor, own, influence, or set strategy. | Map to likely level and rewrite resume bullets to match that level. |
| Red flags | Undefined ownership, impossible stack breadth, vague team or product scope, urgency without clarity. | Surface as questions for the recruiter or hiring manager. |

Common red flags to call out:

- "Wear many hats" with no scope boundaries: risk of undefined ownership.
- 10+ must-have technologies for one role: unrealistic bar or poor planning.
- No team size, tech stack, roadmap, or shipped product: possible disorganization.
- "Fast-paced" plus after-hours language: probe on on-call and work-life expectations.

## Resume and CV tailoring

Use this section for `CV/resume` work. Do not `keyword-stuff`; match terms only where the candidate has real evidence.


Rewrite for the hiring manager first and ATS second. Match real evidence from the user's background to the role; never invent experience.

| Rule | Apply it like this | Avoid |
| --- | --- | --- |
| Match language exactly | If the JD says `distributed systems`, use `distributed systems`, not `large-scale systems`. | Keyword stuffing that repeats terms without evidence. |
| Lead with impact | Start bullets with result and scale: "Reduced P99 latency by 40%". | "Worked on performance improvements". |
| Quantify scope | Include users, QPS, revenue, cost saved, team size, incident volume, or latency. | Unmeasured claims such as "improved reliability". |
| Cut unrelated detail | Keep a two-page tailored CV over a four-page generic CV. | Keeping every old technology because it is impressive. |
| Mirror seniority | Entry: built; senior: designed; staff/principal: drove, defined, influenced. | Overstating ownership beyond the evidence. |

Use this bullet formula when possible: `Verb + technical object + method/constraint + measurable result`. Example: `Reduced checkout P99 latency by 40% by moving payment retries to an idempotent queue-backed workflow`.

## Cover letters and follow-up emails

Keep cover letters under 300 words in three short paragraphs, with no preamble such as "I am writing to apply for" and no prose restatement of the CV.

| Artifact | Required content | Hard limit |
| --- | --- | --- |
| Cover letter paragraph 1 | Why this company: product, technical challenge, published work, or problem space. | Be specific; never say only "I admire your mission". |
| Cover letter paragraph 2 | Why this candidate: one or two concrete background matches to the role. | Do not summarize the full career. |
| Cover letter paragraph 3 | Why now: one sentence on motivation at this career point. | Keep the whole letter under one page. |
| Follow-up email | Thank them, reference one specific conversation detail, reaffirm genuine interest. | Send within 24 hours; no multi-paragraph recap. |

Avoid "I am passionate about", "leader in the industry", "innovative company", and generic praise that could apply to any employer.

## Offer evaluation

Compare total compensation and role risk, not just base salary. Use market sources only as reference points and explain uncertainty when data is stale or sparse.

| Dimension | Questions to answer | Evidence to request |
| --- | --- | --- |
| Compensation | Base vs market, target bonus vs historical payout, equity annualized value, refreshers. | Offer letter, vesting schedule, strike price or valuation context, bonus plan. |
| Equity | Four-year vesting with one-year cliff is common; early-stage equity has dilution and liquidity risk. | Share count, fully diluted shares, latest valuation, exercise window. |
| Role clarity | What does "own" mean, what is already decided, who sets priorities? | Hiring manager answers, org chart, first-90-days plan. |
| Growth | What does next level require and how long do people typically take? | Leveling rubric, promotion examples, manager expectations. |
| Company health | Runway, revenue, growth, customer concentration, funding stage. | Written answers where possible, public filings or credible market data. |
| Engineering culture | PR review, incident postmortems, on-call load, remote/hybrid reality. | Team interview notes, written policy, sample on-call rotation. |

Offer red flags: pressure to decide in under 48 hours, equity with no liquidity path after 10+ private years, greenfield claims hiding unmaintained code, or refusal to put material terms in writing. Get everything in writing before accepting.

## Gotchas

- **Do not invent credentials or achievements**: tailor phrasing only from the user's real resume, notes, or interview details.
- **Do not optimize only for ATS**: keyword matching matters, but the hiring manager must still see impact and evidence.
- **Do not treat nice-to-haves as blockers**: many candidates self-select out because optional phrases are mixed with requirements.
- **Do not give legal or financial advice**: explain compensation mechanics and risk questions, and recommend a qualified advisor for contract, tax, visa, or equity exercise decisions.

## Output template

```markdown
## Job-search result — <task>

**Status:** ready | needs input | blocked
**Target role/company:** <role and company, or "not provided">
**Source material reviewed:** <JD/resume/offer/interview notes>

### Key findings
- <must-have, match, risk, or decision point>
- <must-have, match, risk, or decision point>

### Draft artifact
<tailored bullets, cover letter, follow-up email, offer comparison, or JD analysis>

### Open questions
- <question to ask recruiter, hiring manager, or user>
```

## Quality gate

- [ ] The response stays tied to an active job-search action, not broad career coaching.
- [ ] Must-haves and nice-to-haves are separated when analyzing a JD.
- [ ] Resume bullets preserve the user's actual experience and add no invented facts.
- [ ] Cover letters stay under 300 words and avoid generic company praise.
- [ ] Offer evaluation includes compensation, role clarity, company health, and written-term risks.
- [ ] Follow-up emails are concise and reference a real interview detail.
- [ ] The output follows `## Output template` exactly.
