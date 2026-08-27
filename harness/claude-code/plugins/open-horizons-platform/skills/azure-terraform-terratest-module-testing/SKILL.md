---
name: azure-terraform-terratest-module-testing
description: >-
  Creates, repairs, and runs scoped Terratest coverage for Open Horizons Terraform modules under
  tests/terraform. Use when adding module tests, testing validation failures, selecting static or
  plan coverage, or running an explicitly approved Azure integration test with safe cleanup.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/azure-terraform-terratest-module-testing/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Azure Terratest Module Testing

Test one Terraform module with the least expensive and least mutating mode that can prove the
requested behavior.

## When to invoke

- Add or repair a test under `tests/terraform/modules/`.
- Cover module inputs, outputs, validation, plan shape, or a negative path.
- Select between static, plan, and Azure integration testing.
- Diagnose a focused Terratest failure without changing unrelated infrastructure.

## Repository anchors

- Go module and dependency versions: `tests/terraform/go.mod`
- Current conventions and commands: `tests/terraform/README.md`
- Existing module tests: `tests/terraform/modules/*_test.go`
- CI behavior: `.github/workflows/terraform-test.yml`
- Implementation under test: the corresponding `terraform/modules/<name>/`

Inspect these anchors before authoring a test. Do not assume the README, workflow labels, and test
build tags are perfectly aligned; derive the runnable selector from the current Go files.

## Modes

| Mode | Approval | Allowed behavior |
| --- | --- | --- |
| `static` | Default | Compile tests, inspect files, and run checks that do not plan, apply, destroy, authenticate to Azure, or contact a remote backend. |
| `plan` | Explicit mode selection | Initialize with backend disabled, validate, and run a focused plan without applying. Stop if credentials, a remote backend, or provider API access was not approved. |
| `integration` | Exact environment approval | Create only uniquely named test resources through OIDC, enforce cost and timeout limits, and clean up only resources created by that test. |

## Procedure

1. Resolve one test file and its corresponding Terraform module. Read module inputs, outputs,
   validations, provider requirements, and nearby test patterns.
2. Select `static` unless the acceptance criterion requires a plan. Select `integration` only when
   the environment, OIDC identity, subscription, region, expected cost, unique resource-group
   identity, timeout, and cleanup are all explicitly approved.
3. Use `terraform.WithDefaultRetryableErrors` for operations affected by transient provider
   failures. Keep retry behavior bounded and do not convert deterministic validation failures into
   retries.
4. Prefer Terratest `*E` APIs such as `InitAndValidateE`, `PlanE`, or `DestroyE` when an error is an
   expected result or cleanup evidence must be reported. Assert the specific failure contract
   instead of accepting any error.
5. Keep static tests free of Azure credentials and resource changes. A compile-only baseline is:

   ```bash
   cd tests/terraform
   go test -run '^$' ./...
   ```

6. In plan mode, use a focused test selector, backend-disabled initialization, deterministic
   variables, and no saved plan unless the caller requested one. Do not assume a plan is offline;
   providers may query remote APIs.
7. In integration mode, generate a collision-resistant resource-group name owned by the test,
   register scoped cleanup immediately with `t.Cleanup`, and use OIDC (`ARM_USE_OIDC=true`).
   Cleanup may destroy only the Terraform resources or exact resource group created by that test.
8. Never list and delete resource groups by a shared substring, prefix, tag, or subscription-wide
   query. Existing broad cleanup elsewhere is not a pattern to copy.
9. Run the smallest selected test from `tests/terraform`, for example:

   ```bash
   go test -v -run '^TestExactName$' -timeout 30m ./modules
   ```

   Add `-tags=integration`, the approved timeout, and approved OIDC environment only for integration
   mode.
10. Report mode, selector, module, credentials used or not used, resource identity, timeout,
    cleanup result, test evidence, and residual resources.

## Output template

```markdown
## Terratest result

**Status:** completed | blocked
**Mode:** static | plan | integration
**Module/test:** <terraform module> / <exact Go test>

### Safety context
- Backend: disabled | <approved isolated backend>
- Azure/OIDC: not used | <approved environment and identity>
- Cost/timeout: <not applicable | approved bounds>
- Resource group: <not created | exact unique name>
- Cleanup: <not required | registered and verified | failed>

### Changes
- `<tests/terraform/...>`: <coverage added or repaired>

### Validation
- `<exact command>`: PASS | FAIL | NOT RUN - <evidence>

### Residual resources
- <none | exact resource and owner>
```

## Limits

- Never run integration mode from ambient credentials or a client secret.
- Never run `terraform apply` or `destroy` outside the test's approved integration lifecycle.
- Never use broad subscription or resource-group cleanup.
- Do not weaken assertions, skip cleanup, or raise timeout and cost limits merely to make a test pass.

## Quality gate

- [ ] The test maps to one current Terraform module and follows `tests/terraform/go.mod`.
- [ ] Static is the default; plan and integration have the required approval.
- [ ] Negative paths use `*E` APIs and assert a specific error.
- [ ] Retryable errors are bounded and only cover transient behavior.
- [ ] Integration identity, cost, unique resource group, timeout, and scoped cleanup are explicit.
- [ ] The exact focused command and cleanup evidence are reported.
