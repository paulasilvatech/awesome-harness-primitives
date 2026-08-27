---
name: doublecheck
description: >-
  Runs a three-layer verification pipeline for AI output by extracting verifiable claims, checking
  web sources, applying adversarial hallucination review, and producing inline or full
  verification reports. Use this skill when the user asks to "doublecheck", "verify that", "run
  full verification", "fact-check this", or keep factual claim verification active.
---

<!-- Generated from harness/github-copilot/skills/doublecheck/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Doublecheck

Run a three-layer verification pipeline on AI-generated output. Extract every verifiable claim, find sources the user can check independently, flag hallucination patterns, and produce either inline verification or a full report.

## When to invoke

- "Turn on doublecheck."
- "Doublecheck that answer."
- "Run full verification on this text."
- "Fact-check these claims with sources."
- "Verify the citations and statistics."

## Prerequisites and context

- Use `web_search` for source verification when claims need external evidence.
- Use `assets/verification-report-template.md` for full reports.
- Do not claim a statement is true just because a source was found; report the source and let the user decide.

## Activation modes

Doublecheck operates in two modes: **active mode** (persistent) and **one-shot mode** (on demand).

| Mode | Trigger | Required behavior |
| --- | --- | --- |
| Active mode | User invokes the skill without specific text to verify. | Reply: `**Doublecheck is now active.** I'll verify factual claims in my responses before presenting them. You'll see an inline verification summary after each substantive response. Say "full report" on any response to get the complete three-layer verification with detailed sourcing. Turn it off anytime by saying "turn off doublecheck."` |
| One-shot mode | User provides text to verify or references previous output. | Run the complete three-layer pipeline and produce a full verification report. |
| Deactivation | User says "turn off doublecheck", "stop doublecheck", or similar. | Reply: `**Doublecheck is now off.** I'll respond normally without inline verification. You can reactivate it anytime.` |

Classify every active-mode response before sending it.

| Response type | Contains verifiable claims? | Action |
| --- | --- | --- |
| Factual analysis, legal guidance, regulatory interpretation, compliance guidance, case citations, statutory references | Yes, high density | Run a full verification report. |
| Summary of a document, research, or data | Yes, moderate density | Run inline verification on key claims. |
| Code generation, creative writing, brainstorming | Rarely | Skip verification and note that doublecheck mode does not apply to this type of content. |
| Casual conversation, clarifying questions, status updates | No | Skip verification silently. |

For inline verification, generate the response normally, add a `Verification` section, and list each checked claim with a confidence rating and source link where available:

```markdown
---
**Verification (N claims checked)**

- [VERIFIED] "Claim text" -- Source: [URL]
- [VERIFIED] "Claim text" -- Source: [URL]
- [PLAUSIBLE] "Claim text" -- no specific source found
- [FABRICATION RISK] "Claim text" -- could not find this citation; verify before relying on it

_Say "full report" for detailed three-layer verification with sources._
```

Auto-escalate to a full report when any claim is `DISPUTED` or `FABRICATION RISK`. Place this callout before the report summary:

```markdown
**Heads up:** I'm not confident about [specific claim]. I couldn't find a supporting source. You should verify this independently before relying on it.
```

Always use a full report for legal analysis, regulatory interpretation, compliance guidance, case citations, or statutory references.

## Layer 1: Self-audit

Re-read the target text with a critical lens. This layer extracts and analyzes claims before any web search.

| Step | Action | Required detail |
| --- | --- | --- |
| Extract claims | Go sentence by sentence and pull out every verifiable assertion. | Assign IDs `C1`, `C2`, `C3`, and so on. |
| Categorize claims | Label each claim by type. | Use the categories below. |
| Check internal consistency | Compare claims against each other. | Flag contradictory dates, incompatible statements, and assumptions contradicted later. |
| Initial confidence | Estimate whether each claim is likely accurate, high-risk, vague, or model-prone. | Use this for Layer 2 planning, not as final output. |

| Category | What to look for | Examples |
| --- | --- | --- |
| **Factual** | Assertions about how things are or were. | "Python was created in 1991", "The GPL requires derivative works to be open-sourced" |
| **Statistical** | Numbers, percentages, quantities. | "95% of enterprises use cloud services", "The contract has a 30-day termination clause" |
| **Citation** | References to documents, cases, laws, papers, or standards. | "Under Section 230 of the CDA...", "In *Mayo v. Prometheus* (2012)..." |
| **Entity** | Claims about people, organizations, products, or places. | "OpenAI was founded by Sam Altman and Elon Musk", "GDPR applies to EU residents" |
| **Causal** | Claims that X caused Y or X leads to Y. | "This vulnerability allows remote code execution", "The regulation was passed in response to the 2008 financial crisis" |
| **Temporal** | Dates, timelines, sequences. | "The deadline is March 15", "Version 2.0 was released before the security patch" |

## Layer 2: Source verification

For each extracted claim, search for external evidence and record URLs the user can visit independently.

1. Formulate a search query that would surface a primary source. For citations, search the exact title or case name. For statistics, search the number plus topic. For factual claims, search the key entities and relationship.
2. Run `web_search`. If the first search misses relevant results, reformulate once with different terms.
3. Decide whether the result directly supports, contradicts, or fails to address the claim.
4. Record the result with the source URL.

Prefer primary and authoritative sources: official documentation, specifications, standards, court records, legislative texts, regulatory filings, peer-reviewed publications, official organizational sites, press releases, and established reference works. Mark news articles, blog posts, and wiki pages as secondary when used.

Citations are the highest-risk category and often look plausible-sounding. Citations get the strictest treatment. Search the exact case name, statute, section number, paper title, standard, or document. If the citation cannot be found at all, rate it `FABRICATION RISK`.

## Layer 3: Adversarial review

Assume the target text contains errors and actively try to find them.

| Hallucination pattern | What to check |
| --- | --- |
| Fabricated citations | A cited case, paper, statute, or standard cannot be found in Layer 2. |
| Precise numbers without sources | A statistic such as "78% of companies" has no identifiable source. |
| Confident specificity on uncertain topics | Exact dates, dollar amounts, or attributions are stated where experts disagree or data is unavailable. |
| Plausible-but-wrong associations | A ruling, quote, law, product behavior, or event is assigned to the wrong entity. |
| Temporal confusion | Something outdated is described as current, or event order is wrong. |
| Overgeneralization | A rule is presented as universal when it applies only by jurisdiction, context, or time period. |
| Missing qualifiers | Nuance, limitations, exceptions, or counterarguments are omitted. |

For each major claim, ask: What would make this claim wrong? Is there a common misconception here? Would a subject matter expert object? Is this claim potentially outdated relative to the current date?

Escalate prominently when a citation cannot be found, a statistic has no identifiable source, a legal or regulatory claim contradicts authoritative sources, or a disputed claim is stated with high confidence.

## Confidence ratings

| Rating | Meaning | What the user should do |
| --- | --- | --- |
| **VERIFIED** | Supporting source found and linked. | Spot-check the source if the claim is critical. |
| **PLAUSIBLE** | Consistent with general knowledge, no specific source found. | Treat as reasonable but unconfirmed. |
| **UNVERIFIED** | No supporting or contradicting evidence found. | Do not rely on it without independent verification. |
| **DISPUTED** | Contradicting evidence found from a credible source. | Review the contradiction; the claim may be wrong. |
| **FABRICATION RISK** | Matches hallucination patterns such as unfindable citation or unsourced precise statistic. | Assume it is wrong until confirmed by a primary source. |

Report principles:

- Provide links, not final verdicts.
- Present both sides when sources conflict.
- Mark vague or subjective claims as unfalsifiable when applicable.
- Distinguish "could not verify" from "wrong".
- Lead with the items that need the most attention.

## Domain-specific scrutiny

| Domain | Extra checks |
| --- | --- |
| Legal | Verify case names, citations, holdings, statutory references, regulatory interpretations, jurisdiction, majority/minority rule distinctions, and paraphrases of statutory language. |
| Medical and scientific | Confirm studies exist, results are accurately described, guidelines are current, and dosages, protocols, or diagnostic criteria are flagged as high risk. |
| Financial and regulatory | Verify dollar amounts, dates, thresholds, jurisdictions, and current tax or regulatory rules. |
| Technical and security | Verify CVE numbers, vulnerability descriptions, affected versions, API specifications, configuration instructions, and version-specific details. |

## Progressive disclosure and bundled resources

- `assets/verification-report-template.md`: use for complete three-layer verification reports, auto-escalation reports, and all high-stakes content.

## Output template

```markdown
## Doublecheck verification report

**Status:** verified | needs human review | blocked
**Target:** <text, response, document, or claim set reviewed>
**Claims checked:** <count>

### Summary
| Rating | Count | Notes |
| --- | ---: | --- |
| VERIFIED | <n> | <short note> |
| PLAUSIBLE | <n> | <short note> |
| UNVERIFIED | <n> | <short note> |
| DISPUTED | <n> | <short note> |
| FABRICATION RISK | <n> | <short note> |

### Claim verification
| ID | Claim | Category | Rating | Sources | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | <claim text> | factual/statistical/citation/entity/causal/temporal | VERIFIED | <URL> | <evidence or caveat> |

### Adversarial review
- <hallucination pattern or red flag checked>: <result>

### Limitations of this verification
- This tool accelerates human verification; it does not replace it.
- Web search results may not include the most recent information or paywalled sources.
- The adversarial review uses the same underlying model that may have produced the original output. It catches many issues but cannot catch all of them.
- A claim rated VERIFIED means a supporting source was found, not that the claim is definitely correct. Sources can be wrong too.
- Claims rated PLAUSIBLE may still be wrong. The absence of contradicting evidence is not proof of accuracy.
```

## Quality gate

- [ ] Every verifiable claim has an ID and category.
- [ ] Internal contradictions were checked before web search.
- [ ] Citations, precise statistics, dates, and high-risk claims were searched with `web_search`.
- [ ] Every source-backed claim includes a URL.
- [ ] `DISPUTED` and `FABRICATION RISK` claims are escalated before the summary.
- [ ] Legal, regulatory, compliance, case-citation, and statutory content uses the full report.
- [ ] Full reports follow `assets/verification-report-template.md` and include limitations.
- [ ] Inline verification ends with `_Say "full report" for detailed three-layer verification with sources._`
