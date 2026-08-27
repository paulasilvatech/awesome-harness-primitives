# SIFAP traceability contract

Use one identifier shape throughout the workshop: `REQ-NNN`, with a three-digit sequence such as
`REQ-021`. Do not introduce area-qualified alternatives unless the repository first changes its
validator and all dependent artifacts through an approved migration.

Every requirement includes exactly one nearby `source_legacy:` value:

- a real file under `01-archaeology/legacy-sifap/natural-programs/`;
- a real file under `01-archaeology/legacy-sifap/adabas-ddms/`; or
- `[GREENFIELD]` followed by a concrete justification.

Line anchors are encouraged when stable. Never use a placeholder source in an approved requirement.
If evidence is unknown, keep the candidate outside the approved requirement set and record an open
question.

Acceptance criteria use Given/When/Then and tests cite the related `REQ-NNN`. Measure completeness by
requirement and risk coverage. Line or branch thresholds apply only when the target repository's build
configuration defines them.
