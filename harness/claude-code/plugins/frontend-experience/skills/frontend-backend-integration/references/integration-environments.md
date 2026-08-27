# Integration environments

| Environment | Purpose | Rules |
| --- | --- | --- |
| Mock | Deterministic frontend states | Reuse handlers across unit/component/browser where possible; label as mock |
| Contract | Schema or interaction compatibility | Pin provider/schema revision; fail on incompatible consumer expectation |
| Ephemeral | Real components with isolated dependencies | Seed synthetic data, use unique namespace, clean narrowly, record revisions |
| Staging | Deployment-level confidence | Keep environment policy, access, and test-data restrictions explicit |
| Production-like | Approved high-fidelity validation | No destructive or personal data; strict authorization and observability |

Record URLs without secrets, build and service revisions, fixture IDs, feature flags, locale/timezone, seed and cleanup, and network constraints. Never point destructive tests at shared production resources.
