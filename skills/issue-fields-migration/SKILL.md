---
name: "issue-fields-migration"
description: >-
  Bulk-migrate metadata to GitHub issue fields from two sources: repo labels (e.g. priority labels to
  a Priority field) and Project V2 fields. Use when users say "migrate my labels to issue fields",
  "migrate project fields to issue fields", "convert labels to issue fields", "copy project field
  values to issue fields", or ask about adopting issue fields. Issue fields are org-level typed
  metadata (single select, text, number, date) that replace label-based workarounds with structured,
  searchable, cross-repo fields.
---
# Issue Fields Migration

[Issue fields](https://github.blog/changelog/2026-03-12-issue-fields-structured-issue-metadata-is-in-public-preview/) are org-level typed metadata (single select, text, number, date) that replace label-based workarounds with structured, searchable, cross-repo fields. Every organization gets `Priority`, `Effort`, `Start date`, and `Target date` preconfigured, with support for up to 25 custom fields.

This skill bulk-migrates existing metadata into issue fields from two sources:

- **Repo labels**: Convert labels like `p0`, `p1`, `priority/high` into structured issue field values (e.g. the Priority field). Supports migrating multiple labels at once and optionally removing them after migration.
- **Project V2 fields**: Copy field values (single select, text, number, date, iteration) from a GitHub Project into the equivalent org-level issue fields.

## When to Use

- User added org-level issue fields that overlap with existing project fields
- User wants to copy values from project fields to issue fields before deleting the old project fields
- User asks about "migrating", "transferring", or "copying" project field data to issue fields
- User wants to convert repo labels (e.g., p0, p1, p2, p3) into issue field values (e.g., Priority field)
- User asks about replacing labels with issue fields or cleaning up labels after adopting issue fields

## Prerequisites

- The target org must have issue fields enabled
- The issue fields must already exist at the org level
- For project field migration: issue fields must be added to the project
- For label migration: labels must exist on the target repo(s)
- The user must have write access to the repos (and project, if migrating project fields)
- `gh` CLI must be authenticated with appropriate scopes

## Available Tools

### MCP Tools (read operations)

| Tool | Purpose |
|------|---------|
| `mcp__github__projects_list` | List project fields (`list_project_fields`), list project items with values (`list_project_items`) |
| `mcp__github__projects_get` | Get details of a specific project field or item |

### CLI / REST API

| Operation | Command |
|-----------|---------|
| List org issue fields | `gh api /orgs/{org}/issue-fields -H "X-GitHub-Api-Version: 2026-03-10"` |
| Read issue field values | `gh api /repos/{owner}/{repo}/issues/{number}/issue-field-values -H "X-GitHub-Api-Version: 2026-03-10"` |
| Write issue field values | `gh api /repositories/{repo_id}/issues/{number}/issue-field-values -X POST -H "X-GitHub-Api-Version: 2026-03-10" --input -` |
| Get repository ID | `gh api /repos/{owner}/{repo} --jq .id` |
| List repo labels | `gh label list -R {owner}/{repo} --limit 1000 --json name,color,description` |
| List issues by label | `gh issue list -R {owner}/{repo} --label "{name}" --state all --json number,title,labels --limit 1000` |
| Remove label from issue | `gh api /repos/{owner}/{repo}/issues/{number}/labels/{label_name} -X DELETE` |

See [references/issue-fields-api.md](references/issue-fields-api.md), [references/projects-api.md](references/projects-api.md), and [references/labels-api.md](references/labels-api.md) for full API details.

## Bundled Resources

- [Issue fields migration workflow](references/migration-workflow.md) — When executing a migration or needing concrete commands, open this end-to-end workflow and examples reference.

## Important Notes

- **Write endpoint quirk**: the REST API for writing issue field values uses `repository_id` (integer), not `owner/repo`. Always look up the repo ID first with `gh api /repos/{owner}/{repo} --jq .id`.
- **Single-select values**: the REST API accepts option **names** as strings (not option IDs). This makes mapping straightforward for both project fields and labels.
- **Reading values back**: when reading issue field values from the API response, use `.single_select_option.name` for the human-readable value. The `.value` property returns the internal option ID (an integer like `1201`), not the display name.
- **API version header**: all issue fields endpoints require `X-GitHub-Api-Version: 2026-03-10`.
- **Cross-repo items**: a project can contain issues from multiple repositories. Cache the repo ID per-repository to avoid redundant lookups.
- **Preserve existing values**: never overwrite an issue field value that is already set. Skip those items.
- **Iteration fields**: have no issue field equivalent. Always warn the user and skip.
- **Draft items**: project items that are not linked to real issues cannot have issue field values. Skip with a note.
- **Labels are repo-scoped**: unlike project fields, labels exist per-repo. The same label name may exist in multiple repos; migration applies separately to each.
- **Label conflicts**: an issue can have multiple labels that map to the same single_select field. Always detect and resolve these before execution.
- **Label removal is optional**: after migration, the user may want to keep labels as backup or remove them. Always ask before removing.
- **URL-encode label names**: labels with spaces or special characters must be URL-encoded when used in REST API paths (e.g., `good%20first%20issue`).
- **Script generation for scale**: for migrations of 100+ issues, generate a standalone shell script rather than executing API calls one at a time through the agent. This is faster, resumable, and avoids agent timeout issues.
- **Idempotent migrations**: re-running a migration is safe. Issues that already have the target field value set will be skipped. This means you can safely resume a partial migration without duplicating work.
- **`--limit 1000` truncation**: `gh issue list --limit 1000` silently stops at 1000 results. For labels with more issues, paginate with `--jq` and cursor-based pagination or run multiple filtered queries (e.g., by date range).
- **macOS bash version**: macOS ships with bash 3.x, which does not support `declare -A` (associative arrays). Generated scripts should use POSIX-compatible constructs or note the incompatibility and suggest `brew install bash`.
- **Issues vs PRs**: `gh issue list` returns both issues and pull requests. If the migration should only target issues, include `type` in `--json` output and filter for `type == "Issue"`.

