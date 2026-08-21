---
name: competitor-ad-intelligence
description: >-
  Analyze public competitor paid ads from Meta Ad Library and Google Ads Transparency Center, cluster creative hooks, inspect landing pages, infer funnel strategy, identify vulnerabilities, and recommend counter-plays. Use this skill when asked what ads a competitor is running, to tear down ad strategy, reverse-engineer a paid funnel, find paid ad angles, or audit the ad landscape.
license: MIT
metadata:
  author: GooseWorks
  compatibility: Cross-platform. Uses web search and public ad libraries only; no API keys or credentials required.
  source: https://github.com/gooseworks-ai/goose-skills
  version: "1.0"
---

# Competitor ad intelligence

Collect public paid-ad evidence for named competitors, analyze creative and landing-page patterns, then produce a strategic teardown with hooks, formats, positioning bets, vulnerabilities, and counter-plays.

## When to invoke

- "What ads is [competitor] running?"
- "Tear down [competitor]'s ad strategy."
- "Find new paid ad angles we haven't tried."
- "Reverse-engineer [competitor]'s paid funnel."
- "Audit the ad landscape before we launch."

## Intake

Gather these inputs before analysis:

| Input | Examples and defaults |
| --- | --- |
| Competitor names and domains | `apollo.io`, `clay.run` |
| Your product/domain | Used for comparison framing; preserve source labels like `product/domain**` when converting rough notes |
| Channels | Meta only, Google only, or both; default both |
| Depth level | Standard: ad scrape, creative analysis, landing page analysis. Deep: Standard plus historical comparison, funnel reconstruction, and counter-plays |
| Product category | Used to frame hooks and positioning |
| Known competitor landing pages | URLs already spotted in ads |

## Limits

- Use this skill for paid ad intelligence, not organic SEO competitor research or general website positioning analysis.
- If the request is organic/SEO research, stop and route to a more appropriate workflow.
- Use only public ad libraries, public landing pages, web search, and user-provided evidence.
- Do not use private APIs, credentials, scraping that bypasses access controls, or confidential competitor data.

## Procedure

1. Intake competitors, domains, product category, user's product/domain, channels, depth level, and known landing pages.
2. Search Meta Ad Library evidence for each competitor.
3. Search Google Ads Transparency Center evidence for each competitor.
4. Collect ad-level fields and group ads by platform, format, hook, CTA, landing page, and active duration.
5. Fetch and inspect unique landing pages.
6. Cluster campaigns by destination, messaging theme, and audience signal.
7. Analyze strategic intent, positioning bets, budget allocation, creative gaps, vulnerabilities, and counter-plays.
8. In Deep mode, add historical comparison from Web Archive evidence if available.

## Research sources and queries

| Source | Direct URL or query | Collect |
| --- | --- | --- |
| Meta Ad Library | `https://www.facebook.com/ads/harness/github-copilot/?active_status=active&ad_type=all&country=US&q=<competitor_name>` | Ad copy, visual type, CTA, landing page URL, active duration, platforms, A/B variations |
| Meta search | `web_search: site:facebook.com/ads/library "[competitor_name]"`; `web_search: "[competitor_name]" Meta Ad Library active ads`; `web_search: "[competitor_name]" facebook ads examples` | Publicly indexed ad examples and library pages |
| Google Ads Transparency Center | `https://adstransparency.google.com/?search_text=<competitor_name>` | Headline variants, description lines, ad type, landing page URL, geographic targeting if visible |
| Google search | `web_search: site:adstransparency.google.com "[competitor_name]"`; `web_search: "[competitor_name]" Google Ads transparency`; `web_search: "[competitor_name]" google search ads examples` | Public ad transparency results |
| Landing pages | `web_fetch: [landing_page_url]`, legacy `fetch_webpage: [landing_page_url]`, or `curl` when web fetching is unavailable | Hero, subheadline, CTA, proof, pricing, form fields, page type, message match |

Meta and Google public libraries may be incomplete. Apify actors for Meta Ad Library scraping are unreliable as of April 2026 due to Meta anti-scraping measures, so use `web_search` as the primary method.

## Ad evidence to collect

| Channel | Fields |
| --- | --- |
| Meta | Headline, primary text, visual type (`image`, `video`, `carousel`), CTA button text, landing page URL, active duration (`first seen`, still running or stopped), platforms (`Facebook`, `Instagram`, `Audience Network`), A/B tests with same landing page and different creative |
| Google | Up to 3 headline variants, description lines, ad type (`Search`, `Display`, `YouTube`, `Shopping`), landing page URL, geographic targeting if visible |
| Landing page | Hero headline, subheadline, primary CTA (`Demo`, `Free trial`, `Sign up`, `Download`), social proof, pricing visibility, form fields, page type (`General homepage`, `dedicated LP`, `feature page`, `use-case page`), message match score `1-10` |

When raw notes contain labels such as `Score/10`, normalize them to message match score `1-10`.

## Creative analysis

### Hook pattern clustering

| Hook Type | Pattern | Example |
| --- | --- | --- |
| Fear/Loss | Risk of missing out or falling behind | "Your competitors are already using AI SDRs" |
| Outcome | Direct result promise | "10x your pipeline in 30 days" |
| Question | Challenges current assumption | "Still doing outbound manually?" |
| Social proof | Names customers or numbers | "Join 500+ B2B teams using [product]" |
| Contrarian | Challenges conventional wisdom | "Cold email isn't dead. Your copy is." |
| Empathy | Validates their pain | "We know SDR ramp time is brutal" |
| Product-led | Feature as hook | "[Feature] is live — see what's new" |

Count ads per competitor by hook type. Long-running ads suggest what converts; new ads suggest what they are testing.

Cluster headlines/openers before summarizing hook distribution; preserve strong labels such as `Fear/Loss**` as Fear/Loss.

### Format and CTA taxonomy

| Format | Meta | Google |
| --- | --- | --- |
| Static image | `[N]` | `N/A` |
| Video | `[N]` | `[N]` |
| Carousel | `[N]` | `N/A` |
| Search text | `N/A` | `[N]` |
| Display banner | `N/A` | `[N]` |

| CTA pattern | Examples |
| --- | --- |
| Urgency | "Start free", "Try now", "Get started today" |
| Low-friction | "See how it works", "Watch demo", "Learn more" |
| Outcome | "Book a demo", "Get your free audit", "Calculate your ROI" |

## Campaign and funnel analysis

Group campaigns by landing page destination, messaging theme, and audience signal.

| Dimension | Analysis |
| --- | --- |
| Strategic intent | Awareness, Lead gen, Free trial, Competitive displacement |
| Target persona | Role, pain, buying stage |
| Positioning bet | Market position they claim |
| Hook strategy | Fear/Loss, Outcome, Social proof, Contrarian, Product-led, Question, Empathy |
| Conversion path | Ad → LP → CTA → Demo call, Free Trial, or Content download |
| Longevity signal | First seen date → status; longer usually means likely working |
| A/B tests detected | Multiple creatives to same LP or same promise with different format |

```text
[Ad: Hook/Angle] → [LP: /landing-page-url] → [CTA: Book Demo]
                                               ↓
[Ad: Different angle] → [LP: /same-or-different] → [CTA: Free Trial]
```

## Budget allocation inference

Infer concentration from ad volume and platform distribution, not exact spend:

| Platform | Ad Count | % of Total | Estimated Focus |
| --- | --- | --- | --- |
| Meta (Facebook) | `[N]` | `[X%]` | Awareness / Retargeting |
| Meta (Instagram) | `[N]` | `[X%]` | Visual / younger audience |
| Google Search | `[N]` | `[X%]` | Bottom-funnel capture |
| Google Display | `[N]` | `[X%]` | Awareness / retargeting |
| YouTube | `[N]` | `[X%]` | Education / awareness |

## Strategic analysis

| Analysis | Questions to answer |
| --- | --- |
| Creative Gap Analysis | Which angles nobody is running? Which angles are overcrowded? Is there format white space such as no video? Which proof points are underutilized? Which CTAs do longest-running ads use? |
| Vulnerability Analysis | Where is there Message-LP mismatch, Single-persona dependency, Platform concentration, No social proof, Weak CTA, Generic positioning, or Stale creative? |
| Historical Comparison | In Deep Mode, use Web Archive evidence to ask: has positioning changed in the last 6-12 months, what campaigns retired, and what campaigns scaled? |
| Counter-Plays | For each vulnerability, propose a target weakness, ad angle, platform, headline, body, landing-page strategy, and why to test it |

Answer Why/why claims with evidence: why the competitor likely uses the pattern and why the counter-play is worth testing.

## Cost and environment

| Component | Cost |
| --- | --- |
| Ad library research (`web_search`) | Free |
| Landing page fetching (`web_fetch`, legacy `fetch_webpage`, or `curl`) | Free |
| Web Archive lookup in Deep mode | Free |
| Analysis | Free, using LLM reasoning |
| Total | Free |

No API keys required. This skill uses publicly accessible ad libraries and web search.

## Gotchas

- **Do not treat ad count as exact spend**: it is a directional signal only.
- **Do not claim performance without longevity or volume evidence**: say "likely works" when the signal is long-running ads or repeated variants.
- **Do not overfit one channel**: Meta hooks and Google Search copy reveal different funnel stages.
- **Do not skip landing-page message match**: the paid funnel is ad → LP → CTA, not ad copy alone.

## Output template

```markdown
# Competitor Ad Intelligence Report — <DATE>

## Coverage
- Competitors analyzed: <list>
- Meta ads collected: <N>
- Google ads collected: <N>
- Unique landing pages analyzed: <N>
- Estimated active campaigns: <N>

## Executive Summary
<3-5 sentence summary of landscape, what is working, gaps, and vulnerabilities>

## Meta Ad Analysis
### Hook Distribution
| Hook Type | <Comp1> | <Comp2> | <Comp3> |
| --- | --- | --- | --- |
| Fear/Loss | <percent> | <percent> | <percent> |
| Outcome | <percent> | <percent> | <percent> |

### Top Performing Ads (Longest Running)
**<Competitor> — <Ad Title/Hook>**
> <Ad copy excerpt>
- Format: <Image/Video/Carousel>
- CTA: <text>
- Running since: <date>
- Why it likely works: <analysis>

## Google Ad Analysis
### Headline Patterns
<top headline structures with examples>

### Most Common CTAs
<ranked list>

## Campaign Breakdown
### Campaign 1: <Inferred Campaign Name>
- **Competitor:** <name>
- **Ads in cluster:** <N>
- **Platform(s):** <Meta / Google / Both>
- **Strategic intent:** <Awareness / Lead gen / Competitive displacement / etc.>
- **Target persona:** <description>
- **Hook strategy:** <type>
- **Landing page:** <URL>
  - Hero: "<headline text>"
  - CTA: "<button text>"
  - Message match: <score>/10
- **Longevity:** <First seen date → status>
- **A/B tests detected:** <Yes/No and what they are testing>

**Sample ad:**
> **Headline:** <text>
> **Body:** <text>
> **CTA:** <button>
> **Format:** <Image/Video/Carousel>

**Assessment:** <1-2 sentences>

## Funnel Map
`<ad hook>` → `<landing page>` → `<CTA>`

## Budget Allocation Estimate
| Platform | Share | Focus Area |
| --- | --- | --- |
| <platform> | <X%> | <intent> |

## Creative Gap Analysis
### Angles Nobody Is Running
1. <Angle> — Why it could work: <reasoning>

### Overcrowded Angles (Avoid or Differentiate)
- <Angle> — <N> of <N> competitors use this

### Format White Space
- <Format> is not being used by competitors on <platform>

## Vulnerability Report
### 1. <Vulnerability>
**Competitor:** <name>
**Evidence:** <observed evidence>
**Your opportunity:** <counter-position>

## Recommended Counter-Plays
### Counter-Play 1: <Name>
- **Target their weakness:** <vulnerability>
- **Your ad angle:** <hook>
- **Platform:** <where to run>
- **Proposed headline:** "<headline>"
- **Proposed body:** "<copy>"
- **LP strategy:** <what landing page should emphasize>
- **Why test this:** <rationale>
```

## Quality gate

- [ ] Competitors, domains, user's product/domain, channels, depth level, product category, and known landing pages are recorded.
- [ ] Meta and Google searches are run or explicitly marked out of scope.
- [ ] Every ad claim includes source evidence, platform, copy, format, CTA, landing page, and active-duration signal when visible.
- [ ] Landing pages are analyzed for hero, subheadline, CTA, proof, pricing, form fields, page type, and message match.
- [ ] Hook distribution, format distribution, CTA taxonomy, campaign clustering, funnel map, budget allocation estimate, creative gaps, vulnerabilities, and counter-plays are included.
- [ ] Deep mode includes historical comparison or explains why Web Archive evidence was unavailable.
- [ ] The report does not use private credentials, private APIs, or non-public data.

## References

- [GooseWorks source skill](https://github.com/gooseworks-ai/goose-skills)
- [Meta Ad Library search pattern](https://www.facebook.com/ads/harness/github-copilot/?active_status=active&ad_type=all&country=US&q=<competitor_name>)
- [Google Ads Transparency Center search pattern](https://adstransparency.google.com/?search_text=<competitor_name>)
