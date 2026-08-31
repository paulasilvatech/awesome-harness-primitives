---
description: "Use when writing or reviewing requirements, EARS specifications, acceptance criteria, traceability, and docs-backed requirements."
applyTo: "docs/**/*.md,specs/**/*.md,02-modern-spec/**/*.md"
---

# Requirements Conventions — EARS and Legacy Traceability

This file activates when you write or review Markdown under `docs/`, `specs/`, or `02-modern-spec/`. It teaches how to phrase requirements in EARS notation, assign REQ-IDs, and attach the mandatory `source_legacy:` line that CI enforces. It teaches the *form* of a good requirement — it does not decide *what* to require; that comes from the team's own reading of the legacy corpus.

> [!IMPORTANT]
> Before writing EARS requirements, the pair MUST have read their assigned Natural programs (hard gate — see [`LEGACY-EXPLORATION-CHECKLIST.md`](../../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md) and [`natural-adabas.instructions.md`](natural-adabas.instructions.md)).

## EARS Patterns

Every formal requirement uses one EARS template and the keyword `SHALL` for mandatory behavior (`SHOULD` for recommendations).

| Pattern | Template |
|---|---|
| Ubiquitous | `The <system> SHALL <response>.` |
| Event-driven | `WHEN <trigger>, the <system> SHALL <response>.` |
| State-driven | `WHILE <state>, the <system> SHALL <response>.` |
| Unwanted behavior | `IF <condition>, THEN the <system> SHALL <response>.` |
| Optional feature | `WHERE <feature is present>, the <system> SHALL <response>.` |

The [`ears-validate`](../skills/ears-validate/SKILL.md) skill owns the quality checklist for these statements.

## Anatomy of a Requirement

```markdown
### REQ-021 — Reject duplicate resource registration

WHEN a resource is submitted with an identifier that already exists,
the system SHALL reject the request and return HTTP 409.

- source_legacy: 01-archaeology/legacy-sifap/natural-programs/<PROGRAM>.NSP#L40-L88
- acceptance: Given an existing resource, When the same identifier is submitted,
  Then the response is 409 and no new record is created.
```

## REQ-ID Format

IDs are unique and take the form `REQ-NNN` (`REQ-021`) or `REQ-AREA-NNN` (`REQ-PAY-014`, `REQ-AUD-CORE-002`). The traceability gate recognizes a declaration only when the ID is a heading (`### REQ-021 — …`) or the start of a bold/list item (`- **REQ-021**:`, `REQ-021 - …`, `REQ-021:`). Free-standing mentions elsewhere in prose count as references, not declarations.

## Mandatory `source_legacy` Line

The `legacy-traceability` job in [`spec-quality.yml`](../workflows/spec-quality.yml) **fails the build** if any declared REQ-ID in `specs/` lacks a valid `source_legacy:` line within 20 lines of its declaration. A value is valid when it is one of:

- A path under `01-archaeology/legacy-sifap/natural-programs/` with extension `.NSP`, `.NSN`, `.NSS`, `.NSA`, `.NSL`, `.NSC`, `.NSM`, or `.jcl`.
- A path under `01-archaeology/legacy-sifap/adabas-ddms/` with extension `.NSD`, `.ddm`, or `.txt`.
- `[GREENFIELD] <one-line justification>` (justification must be non-empty).

An optional line anchor `#L<start>` or `#L<start>-L<end>` may follow the path, and the file **must actually exist on disk** — the gate reads it. Quotes are optional but must be balanced.

```markdown
- source_legacy: 01-archaeology/legacy-sifap/adabas-ddms/<DDM>.ddm#L12-L30
- source_legacy: "[GREENFIELD] no legacy audit trail exists; required for compliance"
```

> [!WARNING]
> A `source_legacy:` pointing at a non-existent file, a wrong directory, or an unlisted extension fails the gate exactly as a missing line does.

## Acceptance Criteria

Write acceptance criteria in Given/When/Then form, one per behavior, each testable and tied to its REQ-ID. Number them sequentially within the feature.

```markdown
- AC-021.1: Given a unique identifier, When submitted, Then the response is 201.
- AC-021.2: Given a duplicate identifier, When submitted, Then the response is 409.
```

## Test Traceability

The non-blocking `spec-traceability` job reports REQ-IDs that no test references yet. Cite the REQ-ID in a test comment so implementation and specification stay linked (see [`tests.instructions.md`](tests.instructions.md)).

```java
// REQ-021: duplicate identifier returns 409
@Test
void should_return_409_when_identifier_already_exists() { /* ... */ }
```

## Conventions

| Rule | Rationale |
|---|---|
| One EARS template per requirement | Unambiguous, testable phrasing |
| `SHALL` = mandatory, `SHOULD` = recommended | Consistent obligation language |
| Unique `REQ-NNN` / `REQ-AREA-NNN` IDs | Stable anchors for tests and traceability |
| `source_legacy:` within 20 lines of the ID | Passes the blocking legacy gate |
| Given/When/Then acceptance criteria | Directly convertible into tests |

## Do / Do Not

| Do | Do not |
|---|---|
| Cite a real legacy file (or `[GREENFIELD]`) | Invent a path or omit `source_legacy:` |
| Reference the source by `#L` line range | Assert what the legacy program does from memory |
| Keep IDs unique and declared as headings/list items | Reuse an ID or bury it mid-sentence |
| Write acceptance criteria as Given/When/Then | Leave a requirement without a testable check |

## Checklist Before Opening a PR

- [ ] Every requirement uses an EARS template with `SHALL`/`SHOULD`
- [ ] Every REQ-ID is unique and declared as a heading or list/bold item
- [ ] Every REQ-ID has a `source_legacy:` line within 20 lines pointing at a real file or `[GREENFIELD]`
- [ ] Legacy paths use the allowed directories and extensions, with optional `#L` ranges
- [ ] Acceptance criteria are Given/When/Then and map to the REQ-ID
- [ ] The pair read the cited legacy programs before writing the requirements
