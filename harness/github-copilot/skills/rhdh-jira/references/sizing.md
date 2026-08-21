# Sizing Guide

T-shirt sizing for Features and Epics, Fibonacci story points for Stories/Tasks. Use during issue creation grills and refinement to validate sizing.

## Feature Sizing (RHDHPLAN)

T-shirt size set via the `Size` field (`customfield_10795`).

| Size | Points | Effort | Notes |
|------|--------|--------|-------|
| **XS** | 1 | <30% of release (~2 development sprints) | Possibly should be an Epic |
| **S** | 2 | 30-60% of release (~2-3 development sprints) | |
| **M** | 3 | 60-90% of release (~3-4 development sprints) | |
| **L** | 4 | 90%+ of release (~4+ development sprints) | |
| **XL** | 5 | Whole release (~5 full development sprints) | Likely too big - split or create Outcome |

If multiple L or XL Epics exist within a Feature, the Feature scope may need to be reassessed.

## Epic Sizing (RHIDP)

T-shirt size set via the `Size` field (`customfield_10795`).

| Size | Points | Effort | Notes |
|------|--------|--------|-------|
| **XS** | 1 | ~1 sprint | Possibly should be a Story-sized issue |
| **S** | 2 | ~2 sprints | |
| **M** | 3 | ~3 sprints | |
| **L** | 4 | ~4 sprints | |
| **XL** | 5 | ~5 sprints | Likely too big - split or create Feature |

## Story/Task Sizing (RHIDP)

Story points set via `customfield_10028`. Uses Fibonacci scale.

| Points | Scope | Effort | Complexity |
|--------|-------|--------|------------|
| **1** | Extremely narrow: short AC, simple change, no/simple docs, may update existing tests | Few hours to 1 day | Little |
| **2** | Very narrow: short AC, simple changes, short docs, may add new test cases | 1-2 days | Little |
| **3** | Narrow: multiple/branched AC, new unit/integration tests, demo required, small doc updates | 3-5 days | Low |
| **5** | Broader: possibly new functionality, long/multiple PRs, affects multiple codebase areas, significant doc updates | 5-7 days | Medium |
| **8** | Very broad: may require research, new functionality, may work with external libraries, multiple codebase areas | Up to a sprint | High |
| **13** | Unbound scope: unknown PRs, interconnected AC branches, requires external team review | Not known | Very high |

**13-point stories should be split.** If the scope is unbound, consider breaking into smaller stories or creating a spike to reduce unknowns first.

## RHDHSUPP Sizing (Support Cases)

Story points for support interaction tracking. Different from engineering sizing - measures investigation and communication effort.

| Points | Scope | Time Spent |
|--------|-------|------------|
| **1** | Minimal investigation, minimal communication, quick solution | Few hours to 1 day |
| **2** | Some investigation, moderate communication, solution found quickly | 1-2 days |
| **3** | Moderately complex, in-depth investigation, time on understanding customer requirements | 2-4 days |
| **5** | Complex, possibly multi-team, extensive back-and-forth to reproduce | 4 days to 1 week |
| **8** | Highly complex, extensive research and collaboration, long-term solution needed | More than a week |
| **13** | Unbound: sitting unresolved, multiple back-and-forth with customer, too much time reproducing | Not known |

Support issues may result in follow-up RFE (RHDHPLAN) or product defect (RHDHBUGS) after investigation.

## Sizing Signals During Grill

Use these to challenge sizing during issue creation:

| Signal | Challenge |
|--------|-----------|
| AC count > 5 on a 3-point story | "That's a lot of acceptance criteria for 3 points - is this really a 3?" |
| Cross-team dependencies on a Small feature | "Cross-team coordination adds overhead - should this be Medium?" |
| "We need to investigate" in a Story | "This sounds like unknowns - should this be a spike first?" |
| XL Epic or Feature | "This is the largest size - can it be split into smaller deliverables?" |
| 13-point Story | "Unbound scope - split into smaller stories or create a spike to reduce unknowns." |
| XS Feature | "This might be small enough to be an Epic directly - does it need Feature-level tracking?" |
