---
name: update-avm-modules-in-bicep
description: >-
  Update Azure Verified Modules (AVM) references in Bicep files by discovering avm/res modules,
  comparing MCR tag versions, reviewing breaking changes, editing versions and parameters, and
  validating with bicep lint and bicep build. Use when asked to update AVM modules in Bicep.
---

<!-- Generated from harness/github-copilot/plugins/azure-developer-tooling/skills/update-avm-modules-in-bicep/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Update AVM modules in Bicep

Update a Bicep file to the latest compatible Azure Verified Modules (AVM) versions by scanning `avm/res/{service}/{resource}` references, checking MCR tags, reviewing breaking changes, editing safely, and validating the result.

## When to invoke

- "Update Azure Verified Modules in this Bicep file."
- "Check AVM module versions and bump them safely."
- "Use MCR tags to update `avm/res` references."
- "Run `bicep lint` and `bicep build` after updating AVM modules."

## Prerequisites and context

- A target Bicep file such as `${file}` must be available.
- `bicep` must be installed to run `bicep lint` and `bicep build`.
- Network access must allow tag discovery from `https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list` and documentation review at `https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}`.

## AVM discovery rules

| Item | Rule |
| --- | --- |
| Module pattern | Match Azure Verified Modules in Bicep references using `avm/res/{service}/{resource}`. |
| Version source | Use the MCR tags API only for version discovery. |
| Tags endpoint | `https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list`. |
| Docs endpoint | `https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}`. |
| Version comparison | Parse the JSON `tags` array and sort by semantic versioning. |
| Uniqueness | Check each unique AVM module once, then apply all occurrences. |

## Procedure

1. Scan `${file}` and extract every AVM module reference, current version, and source line.
2. Identify all unique `avm/res/{service}/{resource}` modules.
3. Fetch the MCR tags list for each module from `https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list`.
4. Parse the JSON `tags` array, keep semantic versions, and compare the latest stable version with the current reference.
5. For each candidate update, review docs and release notes from `https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}` for breaking changes.
6. Apply non-breaking version updates and required parameter changes while preserving Bicep formatting and module intent.
7. Pause or report manual review required before applying updates that involve incompatible parameter changes, security/compliance modifications, or behavioral changes.
8. Run `bicep lint ${file}` and `bicep build ${file}`. Fix validation issues caused by the update.
9. Output only the final table and summary; limit progress updates to non-breaking changes.

## Breaking change policy

| Change type | Action |
| --- | --- |
| Compatible version bump | Update in place and validate. |
| Required parameter renamed, removed, or type-changed | Mark `Manual review required`; do not force the update without approval. |
| Security/compliance modification | Mark `Manual review required` with the docs link and risk. |
| Behavioral default change | Mark `Manual review required` and describe the behavior. |
| Validation failure after update | Mark `Failed`, revert or leave the file valid, and summarize the issue. |

## Tooling notes

Use portable CLI capabilities: read or grep for module references, web fetch for MCR tags and docs, edit the Bicep file, and execute `bicep lint` / `bicep build`. Ignore legacy VS Code-only tool tokens from the older prompt form: `#search`, `#searchResults`, `#fetch`, `#editFiles`, `#runCommands`, and `#todos`.

## Output template

```markdown
| Module | Current | Latest | Status | Action | Docs |
|--------|---------|--------|--------|--------|------|
| avm/res/compute/vm | 0.1.0 | 0.2.0 | Updated | Updated version and compatible parameters | [Docs](https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}) |
| avm/res/storage/account | 0.3.0 | 0.3.0 | Current | Current | [Docs](https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}) |
| avm/res/network/virtual-network | 0.4.0 | 0.5.0 | Manual review required | PAUSE for approval before breaking parameter changes | [Docs](https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}) |

### Summary of Updates

Describe updates made, validation results from `bicep lint` and `bicep build`, manual reviews needed, and issues encountered.
```

## Quality gate

- [ ] Every `avm/res/{service}/{resource}` reference in `${file}` was inventoried.
- [ ] Version discovery used only the MCR tags API and parsed the JSON `tags` array with semantic version sorting.
- [ ] Absolute URLs for MCR tags and AVM docs are preserved for every checked module.
- [ ] Breaking changes are not applied without approval; they are marked `Manual review required`.
- [ ] Updated Bicep remains valid and formatted for the changed references.
- [ ] `bicep lint ${file}` and `bicep build ${file}` pass, or failures are reported as `Failed` with evidence.
- [ ] The final answer contains only the results table and `### Summary of Updates`.

## References

- [Azure Verified Modules registry source](https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource})
- [MCR AVM tags endpoint](https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list)
