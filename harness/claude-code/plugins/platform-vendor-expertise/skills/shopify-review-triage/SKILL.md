---
name: shopify-review-triage
description: >-
  Triage public Shopify App Store reviews into a P0-P3 product or support brief while preserving
  source links, first-pass labels, and human-check status. Use when asked to "triage app store
  reviews", "cluster 1-star reviews", "prioritize Shopify merchant feedback", "write a low-star
  review brief", or "decide what to fix first from public reviews".
license: MIT
metadata:
  author: Shopify App Review Brief - independent, not affiliated with or endorsed by Shopify Inc.
  compatibility: >-
    Cross-platform. Pure reasoning skill over review rows the user pastes - no network access,
    scripts, API keys, or system packages. Portable to any client that supports the Agent Skills
    SKILL.md format.
  source: "https://alfredtech2026.github.io/shopify-app-review-brief/guides/shopify-app-review-triage.html"
  version: "'1.0'"
---

<!-- Generated from harness/github-copilot/plugins/platform-vendor-expertise/skills/shopify-review-triage/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Shopify review triage

Turn supplied public Shopify App Store review rows into one prioritized P0-P3 brief that preserves source evidence, separates first-pass keyword classification from human checks, and identifies incident risk, repeated friction, pricing confusion, feature requests, and needs-human-read items.

## When to invoke

- "Triage these app store reviews."
- "What should we fix first from this Shopify feedback?"
- "Cluster our 1-star reviews."
- "Write a weekly low-star review brief."
- "Prioritize public Shopify App Store reviews for our app and competitors."

## Limits

- Use only public review text supplied by the user. Do not accept support tickets, merchant emails, order data, personal contact details, internal telemetry, or private merchant data.
- Never send email, post a developer reply, open a support ticket, message a reviewer, or publish anything.
- Never contact a reviewer or identify/profile them. Refer to "the reviewer".
- Do not fetch reviews yourself. The user must paste the rows they already opened.
- Do not make revenue, rating, outcome, legal, or compliance promises.
- Competitor reviews inform roadmap, positioning, or copy; they never create a P0 incident for the user's own app.

## Input rows and hard rules

Ask for one review per line. Prefer the five-field form:

```text
rating | app name | review date | public reviews URL | review text
```

Accept the shorter three-field form:

```text
rating | app name | review text
```

Rating suffix tokens: `star`, `stars`.

If field 1 is a bare 1-5, optionally followed by `star` or `stars`, treat `star` and `stars` as rating suffixes; otherwise treat it as the app name. Lines beginning with `#` are comments. Blank lines are skipped. A row without a link carries `source: not captured`; never guess a link. Higher-rated rows may be included but must not be presented as low-star signal.

Hard rules:

1. Public review text only; if private data appears, stop and identify affected rows for removal.
2. Do not invent review text, rating, date, app name, or source URL.
3. Keyword output is a sort, not a verdict; label it `first pass - not human-checked` until a person verifies it.
4. Phrase claims as reports: "the reviewer reports the editor showed a blank screen", not "the editor is broken".
5. Cover exactly the rows supplied and make no exhaustive-coverage claim.
6. Produce a draft for the team, not an external reply.

## Rubric

Lower-case review text and normalize curly apostrophes (`’` to `'`). Also match apostrophe-free contractions, so `wont load` classifies the same as `won't load`. Each row gets exactly one primary bucket: the first matching bucket in this order. Further matches are secondary annotations.

| Bucket | Priority | Meaning | Signal keywords | Suggested action |
| --- | --- | --- | --- | --- |
| Incident risk | P0 | Purchase path, app activation, or merchant data may be at stake now. | `won't load`, `won't open`, `won't close`, `can't close`, `cannot close`, `blank screen`, `broken`, `crash`, `stopped working`, `not working`, `doesn't work`, `does not work`, `checkout`, `losing sales`, `lost sales`, `error` | Try to reproduce on a test store today; if confirmed, treat as an incident, fix or mitigate, then let a human reply. |
| Repeated friction | P1 | The product works, but the same struggle repeats across reviews or support themes. | `confusing`, `unclear`, `hard to`, `difficult`, `complicated`, `clunky`, `slow`, `couldn't figure`, `could not figure`, `annoying`, `had to contact support`, `setup took`, `too many steps` | Log against a support theme; repeated rows can justify UX work before new features. |
| Pricing confusion | P2 | Expected payment and actual payment diverged. | `pricing`, `price`, `charged`, `charge`, `billing`, `billed`, `expensive`, `free plan`, `trial`, `refund`, `hidden fee`, `hidden cost`, `paywall` | Compare listing pricing and in-app upgrade prompts; clarify copy where they diverge. |
| Feature request | P3 | The merchant wants something missing or could not find it. | `wish`, `would be great`, `would love`, `please add`, `feature request`, `missing`, `if only`, `would like`, `no option to`, `needs an option`, `hope you add`, `add support for` | Add to the feature-request log with the review link; if it already exists, have a human reply with where to find it. |
| Needs human read | P2 provisional | No keyword matched or context is ambiguous. | No keyword matched. | A person reads the full review and files it manually. Sort last; do not treat as a judged severity. |

Tie-breaks and tie-break rules:

1. Most severe wins; a broken checkout plus billing surprise is one P0 item with pricing noted as secondary.
2. Repetition escalates friction or pricing one level when the same theme appears in three or more reviews within about 60 days.
3. Reviews older than one year are background unless corroborated by a recent row.
4. When unsure, choose needs human read.
5. One review stays one item; secondary matches never become duplicate brief items and never double-counts a merchant.

## Human pass

Before promoting any first-pass item, ask a person on the team to:

- read the original review at the source link;
- for P0 candidates, reproduce on a development store and check the error tracker and support inbox for matching signals from the same period;
- record `reproduced`, `not reproduced`, or `attempted - notes attached`.

Until that happens, every item remains `first pass - not human-checked`, including the summary line. Known limits to state when relevant: keyword matching is English-only, misses sarcasm and context, can misfile a review that mentions `checkout` in passing, and sees only the rows supplied.

## Gotchas

- **The Shopify App Store has no stable per-review permalink**: cite the listing's public reviews page, keep the rating filter if supplied such as `.../reviews?ratings%5B%5D=1`, and pin the item with review date plus the reviewer's first few words.
- **Prefer the five-field input form**: a three-field row folds everything after the second `|` into the review text.
- **`checkout` is noisy**: a P0 based only on the word `checkout` needs human read before promotion.
- **`missing` and `error` cross buckets**: primary order resolves the first pass; the human pass fixes wrong guesses.
- **Non-English reviews land in needs human read**: do not translate and classify as if a keyword matched.

## Output template

```markdown
# Low-star review brief - {portfolio or team name} - week of {YYYY-MM-DD}

Triaged {N} rows supplied: {P0 count} incident risk, {P1 count} repeated friction, {P2 count} pricing confusion, {P3 count} feature request, {needs-human-read count} needs human read - first pass, not human-checked.

Scope: {apps monitored} - {competitors watched} - {N} rows supplied, {date range}.
Covers only the rows supplied - no claim of exhaustive coverage.
Reviews are customer reports, not verified defects. Items marked "first pass" are
unverified keyword matches; "human-checked" means a person read the review and checked it.

## P0 - Incident risk
- **{App} - {signal in a few words}** ({rating} stars, {review date}, [source]({public reviews URL}))
  - Reviewer reports: {one sentence, in their words where possible}
  - Secondary signals: {none or pricing/friction/feature}
  - Status: first pass - not human-checked / human-checked
  - Reproduced: {yes / no / attempted - notes}
  - Next action: {action} - owner {name}, due {date}

## P1 - Repeated friction
- **{App} - {theme}** ({rating} stars, {date}, [source]({public reviews URL}); also seen: {where})
  - Status: first pass - not human-checked / human-checked
  - Next action: {UX or docs change} - owner {name}, due {date}

## P2 - Pricing confusion
- **{App} - {signal}** ({rating} stars, {date}, [source]({public reviews URL}))
  - Expected vs. actual: {one line}
  - Status: first pass - not human-checked / human-checked
  - Next action: {copy or prompt change} - owner {name}, due {date}

## P3 - Feature requests
- **{App} - {request}** ({rating} stars, {date}, [source]({public reviews URL})) - {log it, or already exists so reply with where to find it}

## Needs human read
- **{App}** ({rating} stars, {date}, [source]({public reviews URL})) - {no keyword matched; what a human should look for}

## Competitor watch
- **{Competitor} - {signal}**: {what it implies for our roadmap, copy, or positioning}

## Decisions this week
- {one decision or experiment, with the rows that motivated it}
```

## Quality gate

- [ ] Every item names exactly one bucket and priority from the rubric.
- [ ] Every item carries a source link or `source: not captured`.
- [ ] No review text, rating, date, app name, or URL was invented.
- [ ] Every unverified item says `first pass - not human-checked`.
- [ ] Claims are phrased as reviewer reports, not verified defects.
- [ ] The scope line says how many rows were supplied and makes no coverage claim.
- [ ] No private data survived into the output.
- [ ] Nothing was sent, posted, or published.

## References

- [Public Shopify review triage guide](https://alfredtech2026.github.io/shopify-app-review-brief/guides/shopify-app-review-triage.html)
