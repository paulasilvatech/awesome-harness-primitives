# SIFAP source layout

The workspace kit expects these target-repository paths when the full workshop fixture is present:

| Area | Expected path | Contract |
| --- | --- | --- |
| Legacy programs | `01-archaeology/legacy-sifap/natural-programs/` | Read-only evidence by default. |
| Adabas definitions | `01-archaeology/legacy-sifap/adabas-ddms/` | Read-only schema evidence. |
| Archaeology outputs | `01-archaeology/` outside `legacy-sifap/` | Stage 1 artifacts. |
| Modern specifications | `specs/<NNN>-<feature>/` | Requirements, plan, tasks, and test strategy. |
| Stage 2 workshop outputs | `02-modern-spec/` | Workshop-wide scope and architecture artifacts. |
| Stage 3 reports | `03-implementation/` | Implementation review artifacts. |
| Stage 4 outputs | `04-quality/` | Verification reports, migration mappings, and reconciliation evidence. |
| Stage 5 outputs | `05-operations/` | Issues, delegations, reviews, runbooks, and retrospective. |
| Backend | `backend/` | Created during implementation; do not assume it exists. |
| Frontend | `frontend/` | Created during implementation; do not assume it exists. |
| Infrastructure | `infra/` | Inspect before deciding whether to extend or create. |

Evidence precedence is: inspected source and executable tests, approved requirements and ADRs,
workshop discovery artifacts, then hypotheses. A missing expected path is a blocker for claims about
its content, not permission to fabricate a replacement.
