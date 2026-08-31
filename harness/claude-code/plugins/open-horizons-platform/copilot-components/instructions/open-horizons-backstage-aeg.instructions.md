---
applyTo: "backstage/ai-kit/**,backstage/plugins/**/aeg/**,backstage/packages/backend/**/*aeg*,backstage/app-config*.yaml,docs/aeg-feature-scaffold/**"
description: "Use when editing the Open Horizons Backstage AEG feature, its proxy, actions, agent registry, configuration, or scaffold integration."
---

# Open Horizons Backstage AEG feature

These instructions apply to the Backstage AEG presentation, proxy, action, configuration, agent
registry, and scaffold integration matched by the `applyTo` globs. They are authoritative for passive
identity, lifecycle, tool-contract, and verification conventions in those files; the authenticated AEG
service owns runtime policy and authorization, while the `open-horizons-backstage-aeg-feature` skill
owns ordered workflows.

## Boundaries

- Keep Backstage as the authenticated presentation and integration surface; orchestration policy,
  lifecycle transitions, role enforcement, and audit decisions belong to the AEG service.
- Derive actor identity from the authenticated principal. Do not accept model-authored actor IDs,
  roles, tenant IDs, or identity claims in run, decision, or proposal requests.
- Keep G1 and G2 in the AEG decision workflow. Expose G3 pull-request and G4 production status and
  deep links only; never implement those approvals in chat.
- Keep logical AEG agent names independent of model providers, model IDs, and worker-engine defaults.
  Use `inherit` unless an approved run policy requires a specific engine.

## Contracts

- Use stable typed tools, bounded responses, explicit read-only or mutating classification, and
  server-side authorization for every invocation.
- Preserve `CONSTITUTION.md`, FRD/NFRD EARS requirements, ADRs, `specs/tasks.yaml`, findings, and
  `specs/traceability.yaml` as the lifecycle evidence chain.
- Keep the Backstage action and proxy thin. New lifecycle rules belong in the AEG service, not in
  frontend components, Scaffolder actions, or prompt text.
- Put endpoints and credentials in approved configuration and secret providers. Never expose them
  in frontend bundles, catalog entities, logs, tool schemas, or versioned app configuration.
- Return safe errors with correlation IDs; do not expose raw provider responses, prompts, tokens,
  stack traces, or authorization details.

## Verification

- Test authentication separately from authorization and verify denied tools are neither executable
  nor represented as successful.
- Add contract coverage for malformed input, unavailable dependencies, bounded lists, timeout,
  rejected G1/G2 decisions, and actor-field rejection.
- Verify G3/G4 remain status-only and that every mutating tool reaches a human approval boundary.
- Validate requirement-to-resource traceability and preserve missing evidence as an explicit blocker.

## Conventions

| Rule | Rationale |
| --- | --- |
| Derive the actor from the authenticated principal. | Model-authored identity fields permit impersonation and weaken audit evidence. |
| Keep lifecycle policy in the AEG service. | Thin Backstage adapters prevent policy drift across UI, actions, prompts, and APIs. |
| Classify every tool as read-only or mutating. | Hosts and hooks need stable metadata to enforce human approval. |
| Preserve AEG-native artifact names and traceability. | Stable evidence makes gates, findings, and delivery status independently reviewable. |
| Keep model and worker-engine choices outside logical agent identities. | The feature remains portable across supported execution engines. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Enforce authorization in the backend for every action. | Treat hidden UI controls or tool discovery as authorization. |
| Return bounded, typed results and safe correlation IDs. | Expose raw provider errors, prompts, credentials, or stack traces. |
| Keep G3 and G4 as status and deep-link surfaces. | Approve pull requests or production promotion through chat. |
| Add contract tests at authentication, authorization, and mutation boundaries. | Rely on instructions or agent prose as an enforcement control. |

## Checklist Before Opening a PR

- [ ] The change stays within the Backstage AEG feature and preserves the service responsibility split.
- [ ] Actor identity is server-derived and model-controlled actor fields are rejected.
- [ ] Tool schemas, bounds, mutation classification, and authorization behavior are tested.
- [ ] G1/G2 and G3/G4 approval boundaries remain distinct.
- [ ] Secrets, raw provider failures, prompts, and tokens do not enter frontend or model-visible output.
- [ ] AEG artifacts and requirement-to-resource traceability remain internally consistent.
- [ ] Focused Backstage tests and the AEG contract validator pass.

