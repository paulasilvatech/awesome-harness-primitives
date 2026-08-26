---
applyTo: "backstage/server/agent-api-maf/*.py,backstage/server/agent-api-maf/**/*.py,backstage/server/agent-api-maf/requirements.txt,docs/aeg-feature-scaffold/orchestrator/**/*.py,docs/aeg-feature-scaffold/orchestrator/pyproject.toml"
description: "Use when editing Agent Framework, FoundryChatClient, tool, workflow, hosting, or checkpoint code in tracked MAF runtimes."
---

# Microsoft Agent Framework

The owning manifest defines the supported API surface. The Backstage runtime currently pins `agent-framework-foundry==1.11.0` and `agent-framework-foundry-hosting==1.0.0b260813`; the AEG orchestrator declares `agent-framework>=1.13`. Keep these statements aligned with the manifests and do not assume the two runtimes use one version.

## Conventions

- Use only `Agent`, `FoundryChatClient`, `tool`, workflow, hosting, and checkpoint APIs supported by the owning manifest.
- Keep model deployment selection in the Foundry routing contract and authenticate through `DefaultAzureCredential` or workload identity.
- Define tools with typed inputs, bounded outputs, stable names, clear mutation classification, and execution-time authorization.
- Keep conversations and streaming asynchronous, cancellation-aware, and bounded by iteration, timeout, and budget limits.
- Serialize only versioned, schema-valid checkpoint state. Never checkpoint credentials, provider clients, open handles, or unredacted sensitive content.
- Treat checkpoint restoration as a trust boundary; allowlist restored types, validate ownership and integrity, and reject replay or incompatible versions.
- Preserve pending human decisions across suspension without treating a prior approval as valid for changed inputs.
- Keep hosted-agent and local FastAPI contracts compatible without leaking provider-specific response objects.
- Use the `microsoft-agent-framework` skill for setup, migration, or operational procedures.

## Verification

- Tests run against dependencies resolved from the owning manifest.
- Tool, stream, checkpoint-resume, invalid-checkpoint, cancellation, and provider-failure paths are covered.
- Logs and traces contain stable IDs and redacted metadata rather than prompts, tokens, or checkpoint payloads.

## Do / Do Not

| Do | Do not |
| --- | --- |
| Resolve APIs from the owning manifest and keep tools typed and authorized. | Assume separate runtimes share one SDK version or trust tool visibility as permission. |
| Bound asynchronous work and validate checkpoint integrity and ownership. | Persist credentials, provider clients, open handles, or raw sensitive content. |

## Checklist Before Opening a PR

- [ ] The change matches this instruction's `applyTo` scope.
- [ ] Dependency and API choices match the owning manifest.
- [ ] Tool, stream, cancellation, checkpoint, and provider-failure tests pass.
- [ ] Identity, mutation approval, and restored-state trust boundaries remain enforced.
- [ ] Logs and traces contain only redacted metadata and stable IDs.
