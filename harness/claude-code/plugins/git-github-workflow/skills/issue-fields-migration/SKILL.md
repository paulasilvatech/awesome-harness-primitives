---
name: issue-fields-migration
description: >-
  Bulk-migrate GitHub metadata into organization issue fields from repository labels or Project V2
  fields. Use when asked to migrate labels to issue fields, copy project field values to issue
  fields, convert priority labels, adopt structured issue metadata, or clean up labels after
  migration.
---

<!-- Generated from harness/github-copilot/plugins/git-github-workflow/skills/issue-fields-migration/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Issue fields migration

Migrate existing GitHub issue metadata into organization-level issue fields by planning mappings, detecting conflicts, writing values idempotently through the REST API, and optionally removing label-based source labels only after explicit approval. This skill bulk-migrates both repo-scoped labels and cross-repo Project V2 metadata.

## When to invoke

- "Migrate my labels to issue fields."
- "Copy Project V2 field values to issue fields."
- "Convert p0/p1 labels into the Priority field."
- "Adopt issue fields and clean up old labels."
- "Move project metadata before deleting project fields."

## Prerequisites and context

- The target organization must have issue fields enabled.
- Issue fields must already exist at the organization level; every organization gets `Priority`, `Effort`, `Start date`, and `Target date` preconfigured, with up to 25 custom fields.
- For project field migration, issue fields must be added to the project.
- For label migration, source labels must exist on target repositories.
- The user needs write access to repositories and to the project when migrating project fields.
- `gh` CLI must be authenticated with scopes sufficient to read labels/projects and write issue field values.
- Use API header `X-GitHub-Api-Version: 2026-03-10` for issue fields endpoints.

## Migration sources

| Source | What migrates | Skip or warn |
| --- | --- | --- |
| Repo labels | Labels such as `p0`, `p1`, `p2`, `p3`, `priority/high`, or similar map to a single-select field such as `Priority`. | Detect multiple labels mapping to the same field on one issue before writing. |
| Project V2 fields | Single select, text, number, and date values copy to equivalent org-level issue fields. Use read operations such as `mcp__github__projects_list`, `mcp__github__projects_get`, `list_project_fields`, and `list_project_items` when those MCP tools are available. | Iteration fields have no issue field equivalent; draft items are not real issues and cannot receive values. |
| Existing issue field values | Existing target values are preserved. | Never overwrite a value that is already set; skip and report. |

## API and CLI commands

| Operation | Command |
| --- | --- |
| List org issue fields | `gh api /orgs/{org}/issue-fields -H "X-GitHub-Api-Version: 2026-03-10"` |
| Read issue field values | `gh api /repos/{owner}/{repo}/issues/{number}/issue-field-values -H "X-GitHub-Api-Version: 2026-03-10"` |
| Write issue field values | `gh api /repositories/{repo_id}/issues/{number}/issue-field-values -X POST -H "X-GitHub-Api-Version: 2026-03-10" --input -` |
| Get repository ID | `gh api /repos/{owner}/{repo} --jq .id` |
| List repo labels | `gh label list -R {owner}/{repo} --limit 1000 --json name,color,description` |
| List issues by label | `gh issue list -R {owner}/{repo} --label "{name}" --state all --json number,title,labels --limit 1000` |
| Remove label from issue | `gh api /repos/{owner}/{repo}/issues/{number}/labels/{label_name} -X DELETE` |

Use `references/issue-fields-api.md`, `references/projects-api.md`, `references/labels-api.md`, and `references/migration-workflow.md` for full command payloads and end-to-end examples.

## Procedure

1. Identify organization, repositories, source labels or project, target issue fields, and desired label-removal policy.
2. List organization issue fields and confirm target field names and option names.
3. For label migration, list labels and issues; URL-encode label names with spaces or special characters such as `good%20first%20issue` in REST paths.
4. For project migration, list project items and field values; skip iteration fields and draft items with notes.
5. Cache each repository ID per-repo and per-repository with `gh api /repos/{owner}/{repo} --jq .id`; the write endpoint uses integer `repository_id`, not `owner/repo`.
6. Read existing issue field values and skip any issue where the target value is already set.
7. Detect label conflicts before execution when one issue has multiple labels mapping to the same single_select field.
8. For migrations of 100+ issues, generate a standalone POSIX-compatible shell script instead of executing one API call at a time through the agent.
9. Write field values idempotently with the REST API; use single-select option names as strings, not option IDs.
10. Read values back and use `.single_select_option.name` for human-readable verification; `.value` may be an internal option ID like `1201`.
11. re-running the migration is safe because existing target values are skipped; remove labels only if the user explicitly approved removal after migration.

## Gotchas

- **Repository ID is required for writes**: `/repositories/{repo_id}/issues/{number}/issue-field-values` does not accept `owner/repo`.
- **Single-select writes use names**: send option names as strings, not option IDs.
- **Readback names are nested**: use `.single_select_option.name`; `.value` may be an integer ID.
- **`gh issue list` includes PRs**: include `type` in `--json` and filter `type == "Issue"` when PRs are out of scope.
- **`--limit 1000` truncates silently**: `gh issue list --limit 1000` stops at 1000 results; paginate with `--jq` and cursor-based pagination or split by date range when labels exceed 1000 issues.
- **macOS bash 3.x lacks `declare -A`**: generated scripts should be POSIX-compatible or explicitly require newer bash via `brew install bash`.
- **Label removal is optional**: never remove source labels without approval.

## Progressive disclosure and bundled resources

- `references/migration-workflow.md`: end-to-end workflow, payloads, dry-run structure, conflict handling, and execution examples.
- `references/issue-fields-api.md`: issue fields REST endpoints and value formats.
- `references/projects-api.md`: Project V2 field/item reads and mapping guidance.
- `references/labels-api.md`: label inventory, issue discovery, and label removal details.

## Output template

```markdown
## Issue fields migration result

**Status:** planned | migrated | blocked
**Organization:** `<org>`
**Source:** labels | Project V2
**Target field:** `<field name>`

### Mapping
| Source value | Target issue field | Target value | Issues matched | Conflicts |
| --- | --- | --- | --- | --- |
| `p0` | `Priority` | `High` | <count> | <count> |

### Execution
- Repository IDs cached: <count>
- Existing values skipped: <count>
- Values written: <count>
- Draft items skipped: <count>
- Iteration fields skipped: <count>
- Labels removed: <count or "not approved">

### Validation
- Readback command: `<command>`
- Sample verified issues: <numbers>
- Remaining risks: <pagination, permissions, conflicts, or "none">
```

## Quality gate

- [ ] Target issue fields exist and option names are known.
- [ ] `X-GitHub-Api-Version: 2026-03-10` is used on issue fields endpoints.
- [ ] Repository IDs are cached per repository before writes.
- [ ] Existing issue field values are preserved and skipped.
- [ ] Label conflicts, iteration fields, draft items, and PR filtering are handled explicitly.
- [ ] Migrations of 100+ issues use or produce a standalone resumable script.
- [ ] Label names in REST paths are URL-encoded.
- [ ] Source labels are removed only with explicit approval.
- [ ] Readback uses `.single_select_option.name` for human-readable values.

## References

- [Issue fields public preview changelog](https://github.blog/changelog/2026-03-12-issue-fields-structured-issue-metadata-is-in-public-preview/)
