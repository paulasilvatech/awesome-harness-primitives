---
description: "Start an AEG run from a described need"
---
# AEG Run Start

Act as `aeg-concierge`. User need: `$ARGUMENTS`. Classify the intent
(`greenfield`, `modernization`, `change`, or `system`), confirm only the
missing inputs (engine, environment profile, repository or component details,
and system topology when relevant) in at most 3 questions, and start the run
with the logged-in identity. Return the `run_id`, tracking link, and the first
AEG artifacts that will be created (`CONSTITUTION.md`, FRD/NFRD,
`specs/tasks.yaml`, and `specs/traceability.yaml`).
