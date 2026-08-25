# Permanent instructions (GitHub Copilot) for this Backstage repository

This is the platform Backstage repository with the AEG integration installed.

## System map

- `/aeg` proxy in `app-config.yaml` -> AEG orchestrator (Azure Container App)
- Custom Scaffolder action in `packages/backend`: `aeg:run:start`
- AEG templates are imported from the `aeg-platform` repository; do not edit
  local copies
- Chat agents are registered from `backstage/ai-kit/agents` in `aeg-platform`
- An existing chat plugin is already in place: do not modify registrations for
  other agents

## AEG-native artifact model

When you describe or extend the workflow, use the native AEG artifacts:
- `CONSTITUTION.md` seeds the run at N0
- `specs/FRD_*.md` and `specs/NFRD_*.md` carry EARS requirement IDs
- `docs/adr/ADR-*.md` records architecture decisions
- `specs/tasks.yaml` plans approved implementation work
- `specs/traceability.yaml` closes the requirement-to-resource chain
- Findings drive loop back-edges; G1/G2 are orchestrator gates, G3/G4 stay in
  GitHub
- Generated applications use engine harnesses under
  `backstage/template-aeg-application/skeleton/harness/`

## Rules

1. Secrets: NEVER store them in versioned `app-config*.yaml`; use environment
   variables and the secrets provider. Hooks block credential-like literals.
2. `aeg:run:start` is a thin client. Any new orchestration rule belongs in the
   orchestrator, not in Backstage. Reject requests to "just add a small rule"
   to the action.
3. G3/G4: never build UI that approves PRs or production promotion; surface
   status and deep-links only.
4. Changes to the proxy, auth, or the custom action require a dedicated PR
   with platform-team review.
5. Local testing: use `yarn dev` with a development `AEG_API_TOKEN`; never
   point a local machine at the production orchestrator.
6. Do not reintroduce external requirements-tooling terminology in this
   repository's prompts, docs, or UI copy.
