---
name: apple-appstore-reviewer
description: >-
  Review an iOS app codebase and metadata for likely Apple App Store rejection risks, compliance gaps, reviewer friction, and fast approval improvements. Use when asked to "review for App Store rejection", "check Apple review readiness", "audit IAP and privacy", "write reviewer notes", or "find App Store approval risks".
---

# Apple App Store reviewer

Audit an iOS app's source, project settings, metadata, and review flows from an App Store reviewer perspective, then produce prioritized recommendations with evidence and test steps.

## When to invoke

- "Review this app for App Store rejection risks."
- "Check whether our iOS app is ready for Apple review."
- "Audit privacy, permissions, IAP, and reviewer notes."
- "Find App Store approval blockers before submission."
- "Give short recommendations with test steps for App Store review."

## Prerequisites and context

- Review only at first pass; do not edit code or propose a PR until after the report.
- Use App Store Review Guidelines categories by topic. Cite exact numbers only when known from context.
- If repository evidence is incomplete, state assumptions and what to verify.
- Do not invent features, files, flows, or metadata that are not present.

## Review evidence to inspect

Start with `SwiftUI/UIKit` build clues and preserve the reviewer lens: produce best-effort fixes/improvements that reduce re-review risk. Include `Info.plist/entitlements`, `demo/test` access, `first-run` clarity, `test/verify` steps, and `Class/function` evidence when available.


| Area | Files, symbols, or flows | Rejection risk to assess |
| --- | --- | --- |
| App metadata and configuration | `Info.plist`, `*.entitlements`, signing capabilities, ATS settings, URL schemes, Associated Domains | Missing purpose strings, insecure transport, unsupported mania of capabilities. |
| Privacy | `PrivacyInfo.xcprivacy`, privacy policy links, SDK manifests, analytics and tracking code | Undisclosed collection, tracking, fingerprinting, missing privacy manifest. |
| Permissions | `NS*UsageDescription`, Photos, Camera, Location, Bluetooth, Push, background modes | Vague or missing usage text, launch-time prompts, over-requesting. |
| Monetization | StoreKit 2, StoreKit config, receipt validation, restore flows, paywalls, pricing copy | Digital goods outside IAP, missing restore, misleading price/trial copy. |
| Account and access | Login, third-party auth, Sign in with Apple, account deletion, demo account | Login wall without justification, no reviewer path, missing account deletion. |
| Content and safety | UGC, sharing, messaging, external links, claims, moderation/reporting | No moderation/report flow, medical/financial/safety claims needing substantiation. |
| Technical quality | App entry, core flows, crash-prone code, networking, offline states, blank screens | App appears broken, core loop unreachable, poor error handling. |
| UX and reviewability | Onboarding, empty states, paywall gates, support/legal links, reviewer notes | Reviewer cannot find the app's purpose or test key features. |

Evidence must include at least one file path and line range when available, class/function name, UI screen or route, specific Info.plist/entitlement setting, or network endpoint domain/path. If evidence is absent, label the finding as `Assumption` and explain what to check.

## Procedure

1. Identify the build system, UI framework, iOS minimum version, dependencies, app entry point, and top three user flows.
2. Determine the app's primary purpose and what is required to use it: account, permissions, purchase, network, or special data.
3. Inspect permissions, privacy manifests, entitlements, purchase flows, account flows, external links, and reviewer access.
4. Flag P0/P1 rejection risks first: missing usage descriptions, privacy disclosure gaps, broken IAP/restore, login walls, claims, misleading UI, or incomplete app behavior.
5. Complete the compliance checklist across privacy, payments, accounts, content, platform usage, stability, and UX.
6. Add optimization suggestions that reduce reviewer friction after compliance risks are covered.
7. Produce the report with no code changes.

## Criteria

### Severity definitions

| Priority | Meaning | Typical examples |
| --- | --- | --- |
| P0 blocker | Very likely rejection or app non-functional for review. | Crash on launch, external payment for digital features, reviewer cannot access core value. |
| P1 high | Common rejection reason or serious reviewer friction. | Missing permission string, subscription without visible restore, login wall with no demo/testing path. |
| P2 medium | Risky pattern, unclear compliance, or quality concern. | Weak offline handling, vague privacy copy, confusing paywall limitation. |
| P3 low | Nice-to-have improvement or polish. | Better empty states, clearer onboarding, more reviewer notes. |

### Hotspot checks

- [ ] `Missing/incorrect` permission usage strings for `camera/photos/location` and other `NS*UsageDescription` keys were checked.
- [ ] `subscriptions/IAP`, subscription vs `non-consumable` handling, StoreKit restore, and external payment `prompts/links` were checked.
- [ ] `sign-in` flows, Sign in with Apple expectations, account deletion, and reviewer access were checked.
- [ ] `Health/medical`, `medical/financial`, and `Safety/emergency` claims were flagged for substantiation.
- [ ] `Moderation/reporting` exists for UGC and content flows where needed.
- [ ] `analytics/identifiers`, privacy manifests, and SDK disclosures align.
- [ ] Dead-ends, blank states, and `dead-ends` in the core loop were checked.
- [ ] P0/P1 items are separated from `P2/P3` polish.


- [ ] Privacy policy and `PrivacyInfo.xcprivacy` align with actual SDKs, analytics, identifiers, and tracking behavior.
- [ ] Every requested permission has a specific `NS*UsageDescription` and is requested near the feature that needs it.
- [ ] Digital goods/features use IAP; paywall copy shows price, recurring terms, trial limitations, and restore purchases.
- [ ] Third-party social login is checked against Sign in with Apple expectations.
- [ ] If account creation exists, account deletion is accessible in-app when applicable.
- [ ] UGC, sharing, messaging, or external links have moderation, reporting, blocking, or safety controls where expected.
- [ ] Medical, financial, safety, or emergency claims are substantiated and framed conservatively.
- [ ] The reviewer can install, launch, understand, and reach the core loop without hidden setup.

## Reviewer notes guidance

Draft App Store Connect notes with placeholders instead of real credentials:

| Note item | Include |
| --- | --- |
| Key paths | Steps to reach the app's main features. |
| Required account | `Username: {{reviewer_account}}`, `Password: {{reviewer_password}}`, or demo mode steps. |
| Permissions | Why each unusual permission is requested and where to trigger it. |
| IAP testing | Product names, test flow, restore path, and gated content explanation. |
| Limitations | Any region, hardware, content, or backend constraints the reviewer may hit. |
| Support/legal | Privacy policy, terms, support links, and account deletion path. |

## Limits

- Do not edit code or open PRs in the first pass.
- Do not claim compliance with a guideline without evidence.
- Do not provide legal advice; frame findings as App Store review risk.
- Offer an optional next pass only after the report: code patch plan, permission prompt wording, paywall/privacy copy, or pre-submission checklist.

## Output template

```markdown
## App Store review readiness report

**Status:** pass | fixes recommended | likely rejection risk
**App purpose:** <one sentence>
**Assumptions:** <none or explicit assumptions>

### Executive summary
- <5-10 bullets: purpose, top 3 approval risks, top 3 fast wins>

### Risk register
| Priority | Area | Finding | Why Review Might Reject | Evidence | Recommendation | Effort | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0/P1/P2/P3 | Privacy/IAP/Account/Permissions/Content/Technical/UX | <finding> | <reviewer concern> | <file/symbol/screen or Assumption> | <concrete fix> | S/M/L | High/Med/Low |

### Detailed findings
#### Privacy & Data Handling
- **What I saw:** <evidence>
- **Why it matters:** <risk>
- **What to change:** <recommendation>
- **How to test:** <verification steps>

#### Permissions & Entitlements
<same structure>

#### Monetization (IAP/Subscriptions)
<same structure>

#### Account & Authentication
<same structure>

#### Content / UGC / External Links
<same structure>

#### Technical Stability & Performance
<same structure>

#### UX & Reviewability
<same structure>

### Reviewer experience checklist
- Install & launch: pass/fail/unknown - <evidence>
- First-run clarity: pass/fail/unknown - <evidence>
- Required permissions: pass/fail/unknown - <evidence>
- Core feature access: pass/fail/unknown - <evidence>
- Purchase/restore path: pass/fail/unknown - <evidence>
- Links, support, legal pages: pass/fail/unknown - <evidence>
- Edge cases: pass/fail/unknown - <evidence>

### Suggested App Review Notes
<draft paste-ready reviewer notes with placeholders for credentials>

### Next pass option
- <optional code changes, patch plan, wording, or checklist after the review report>
```

## Quality gate

- [ ] No code was edited during the first pass.
- [ ] The report includes an executive summary, risk register, detailed findings, reviewer checklist, suggested reviewer notes, and next-pass option.
- [ ] Every finding has evidence or is labeled `Assumption` with verification steps.
- [ ] P0/P1 risks are listed before optimization suggestions.
- [ ] Recommendations are concrete, minimal, and include test steps.
- [ ] No features, metadata, accounts, or flows are invented.
- [ ] Claims are framed as review risk, not legal advice or guaranteed rejection.
