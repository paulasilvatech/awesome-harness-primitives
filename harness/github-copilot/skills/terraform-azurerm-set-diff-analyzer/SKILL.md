---
name: "terraform-azurerm-set-diff-analyzer"
description: >-
  Analyze Terraform plan JSON for AzureRM Provider Set-type attribute noise and separate order-only false-positive diffs from real Azure resource changes. Use when Application Gateway, Load Balancer, Firewall, Front Door, NSG, or other Azure resources show many changed elements after one add, remove, or reorder.
license: "MIT"
---

# Terraform AzureRM set diff analyzer

Generate Terraform plan JSON, run the bundled analyzer, and classify noisy AzureRM Set-type diffs as false positives or actual infrastructure changes from `terraform plan`.

## When to invoke

- "This Terraform plan shows all Application Gateway blocks changed after one edit."
- "Analyze AzureRM set diffs in plan.json."
- "Filter false-positive Terraform diffs in CI."
- "Is this Load Balancer, Firewall, Front Door, or NSG plan change real?"

## Prerequisites and context

- Python 3.8+ is required. If `python` is unavailable, use `python3`, install with a package manager such as `apt install python3` or `brew install python3`, or use https://www.python.org/downloads/.
- Terraform must be able to create a saved plan and render JSON in the target workspace.
- The analyzer uses only the Python standard library; `ModuleNotFoundError` usually means the wrong interpreter is being invoked.

## Procedure

1. Generate a binary Terraform plan: `terraform plan -out=plan.tfplan`.
2. Convert it to JSON: `terraform show -json plan.tfplan > plan.json`.
3. Run the bundled analyzer: `python scripts/analyze_plan.py plan.json` or `python3 scripts/analyze_plan.py plan.json`.
4. Read the classification before approving, rejecting, or suppressing plan noise in CI/CD.

## Diff classification

| Plan signal | Likely classification | Review action |
| --- | --- | --- |
| One element added or removed and sibling Set elements appear reordered | False-positive diff | Confirm identity keys match and suppress only the order-only noise; this is the classic added/removed Set case. |
| Attribute values changed inside the same logical element | Actual change | Review as a real resource update. |
| Element identity key changed | Actual change | Treat as delete/create even if nested values look similar. |
| Many AzureRM nested blocks changed after one edit | Suspect Set ordering | Compare by stable keys rather than displayed position. |
| Unsupported resource or attribute | Unknown | Use `references/azurerm_set_attributes.md` or the provider schema before classifying. |

Terraform's `Set` type is unordered, but plan display can make internally reordered nested blocks look like position-by-position changes. AzureRM resources with nested collections such as Application Gateway, Load Balancer, Firewall, Front Door, and NSG expose this often.

## Progressive disclosure and bundled resources

- `scripts/analyze_plan.py`: deterministic analyzer for Terraform plan JSON.
- `scripts/README.md`: full options, output formats, exit codes, and CI/CD examples.
- `references/azurerm_set_attributes.md`: supported AzureRM resources and attributes.
- `references/azurerm_set_attributes.json`: machine-readable Set attribute catalog.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `python: command not found` | System exposes Python as `python3`. | Run `python3 scripts/analyze_plan.py plan.json` or install Python 3.8+. |
| `ModuleNotFoundError` | Wrong interpreter or broken environment. | Use Python 3.8+; the script needs only the standard library. |
| Analyzer reports unknown attributes | Catalog does not cover that nested block. | Inspect `references/azurerm_set_attributes.md` and manually compare stable keys. |

## Output template

```markdown
## Terraform AzureRM set diff analysis - <plan file>

**Status:** false-positive diffs found | actual changes found | mixed | blocked
**Command:** `python scripts/analyze_plan.py <plan.json>`

| Resource | Attribute path | Classification | Evidence | Action |
| --- | --- | --- | --- | --- |
| `<azurerm resource>` | `<nested Set path>` | `false positive` | `<same keys, reordered>` | `<safe to ignore in review>` |
| `<azurerm resource>` | `<attribute>` | `actual change` | `<value or identity changed>` | `<review/apply decision>` |

### Validation
- `terraform plan -out=plan.tfplan`: <pass/fail/not run>
- `terraform show -json plan.tfplan > plan.json`: <pass/fail/not run>
- Analyzer exit code: <code>
```

## Quality gate

- [ ] Plan JSON came from `terraform show -json plan.tfplan`, not from human plan text.
- [ ] Every false-positive claim is backed by stable identity-key comparison, not visual similarity.
- [ ] Actual value changes, identity changes, additions, and removals remain visible in the output.
- [ ] Unsupported attributes are labeled unknown instead of suppressed.
- [ ] `scripts/README.md` was used for CI/CD options or exit-code behavior when automation is requested.

## References

- [Python downloads](https://www.python.org/downloads/)
