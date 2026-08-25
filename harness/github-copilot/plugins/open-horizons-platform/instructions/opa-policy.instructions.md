---
applyTo: "policies/**/*.rego,policies/kubernetes/constraint-templates/*.yaml,policies/kubernetes/constraints/*.yaml,scripts/golden-paths/**/policies/*.rego"
description: "Use when editing tracked Rego, OPA, Gatekeeper templates, or policy constraints."
---

# OPA and Gatekeeper Policies

## Conventions

- Keep policy evaluation pure and deterministic: no time-, network-, random-, or environment-dependent authorization decisions.
- Use explicit package names, rule names, input shapes, and defaults so undefined data cannot become an accidental allow.
- Return stable, actionable denial or violation messages without secrets or full sensitive objects.
- Normalize sets and object traversal deliberately; do not depend on iteration order.
- Keep allow and deny precedence explicit and fail closed for malformed or unsupported inputs.
- Align each Gatekeeper `ConstraintTemplate` name, generated constraint kind, parameters schema, targets, and Rego package.
- Scope constraints with deliberate match and exclusion rules; avoid exemptions broader than the documented compatibility need.
- Keep generated security-baseline policy under `scripts/golden-paths/` portable and deterministic.
- Add fixtures for allowed, denied, missing, malformed, boundary, and exemption cases.

## Verification

- Rego formatting, parsing, and policy tests pass with the repository-supported OPA tooling.
- Gatekeeper templates and constraints agree on API versions, kinds, names, and parameters.
- Repeated evaluation of identical input produces identical structured results.
