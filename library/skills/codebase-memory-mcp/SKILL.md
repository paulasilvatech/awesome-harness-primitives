---
name: "codebase-memory-mcp"
description: >-
  Use a configured Codebase Memory MCP graph for architecture orientation, symbol lookup, callers and callees, dependency or data-flow tracing, impact analysis, and unfamiliar module discovery. Use this skill when a codebase-memory-mcp server is available or the user explicitly requests Codebase Memory.
---

# Codebase Memory MCP

Use a configured Codebase Memory graph as a discovery accelerator, confirm graph-derived conclusions against source snippets or local files, and fall back to normal repository exploration when the server, project, index, or capability is unavailable.

Use it for graph-backed discovery, natural-language exploration, and moderate-only index caveats.

## When to invoke

- "Use Codebase Memory to understand this module."
- "Trace callers and callees with the code graph."
- "What depends on this symbol?"
- "Use the MCP graph for impact analysis."
- "Find the architecture clusters for this repo."

## Procedure

1. Discover the Codebase Memory tools exposed by the current MCP client; clients may prefix or rename tool namespaces.
2. Call `list_projects` when available and use the exact indexed project name.
3. If the repository is not indexed, continue with local exploration or ask before calling `index_repository` when graph access is important.
4. Before branch-sensitive or edit-sensitive conclusions, use `index_status` and verify the actual version-control state.
5. Use `detect_changes` only when its Git base and head are valid for the checkout; if it unexpectedly reports zero changes, or the checkout uses another VCS, inspect that VCS status or diff before claiming no impact.
6. Use `get_architecture` once for unfamiliar structure. Request `clusters` to discover de-facto module seams.
7. Treat `cycles` as an opt-in whole-call-graph scan: `path` does not scope cycle detection, so verify relevant cycles before making module-local claims.
8. Use `search_graph` for definitions, implementations, routes, classes, interfaces, and related symbols. Prefer natural language for discovery and name or qualified-name patterns for known symbols. Narrow by label or path and set a result limit.
9. For exhaustive claims, increase `offset` by `limit` while `has_more` is true.
10. Use `search_code` or normal repository search for literal strings, configuration keys, test identifiers, error messages, and non-code files.
11. After graph search, use `get_code_snippet` with the returned qualified name. If source snippets are unavailable, open the local file before relying on the result.
12. Use `trace_path` for callers, callees, dependency paths, data flow, cross-service paths, and impact analysis. Include tests when the claim covers them. While `truncated` is true, pass `next` back as `cursor` with every other argument unchanged.
13. After identifying candidate files, call `check_index_coverage` for every cited path.
14. Before negative or exhaustive claims, also check relevant `scopes`; advance `scope_offset` to each `next_offset` while `has_more` is true.
15. Use `get_graph_schema` before custom `query_graph` calls. Reserve custom queries for bounded multi-hop or aggregate questions, apply `LIMIT` or `max_rows`, and use `graph="missed"` to audit files the main graph did not fully index.
16. Complete every relevant result stream before an exhaustive claim. When graph and checked-out source disagree, treat source as current and report likely index drift.

## Tool decision table

| Need | Preferred action | Avoid |
| --- | --- | --- |
| Project discovery | `list_projects`, then exact project name. | Guessing an indexed project name. |
| Staleness check | `index_status` plus VCS status when needed. | Claiming no changes from graph metadata alone. |
| Architecture orientation | `get_architecture` with `clusters`; use `cycles` only when wanted. | Treating `path` as a cycle-detection scope. |
| Symbol discovery | `search_graph` with labels, paths, limits, `offset`, and `has_more`. | Using broad graph search for exact strings. |
| Literal search | `search_code` or local grep. | Turning config keys or error text into semantic graph queries. |
| Source evidence | `get_code_snippet`, then local file if missing. | Citing a graph node without source confirmation. |
| Impact tracing | `trace_path` with cursor handling for `truncated` results. | Dropping later pages of a trace. |
| Coverage confidence | `check_index_coverage` and scoped pagination. | Making exhaustive negative claims from partial indexes. |
| Custom graph query | `get_graph_schema`, then bounded `query_graph` with `LIMIT` or `max_rows`. | Unbounded graph queries. |

## Indexing modes

| Mode | Use when | Trade-off |
| --- | --- | --- |
| `moderate` | Normal indexing. | Filters files while retaining similarity and semantic edges. |
| `fast` | User asks for a smoke index, or `moderate` is blocked and degraded fallback is useful. | Similarity and semantic edges are absent; disclose this. |
| `full` | Moderate-only discovery filters omit relevant supported files and extra indexing cost is justified. | More expensive; still honors `.gitignore`, `.cbmignore`, and always-skip rules. |

## Safety and fallbacks

- Do not install Codebase Memory or another third-party skill from this workflow.
- Do not call `delete_project`, ingest traces, update ADRs, or index a repository unless the user explicitly requested or approved the action; announce it before execution.
- Do not invent graph results. If the MCP server, project, index, or tool is unavailable, continue with normal repository exploration.
- Treat index coverage metadata as best-effort, not proof of completeness. Inspect local source for partial, skipped, excluded, stale, or otherwise uncovered paths.

## Output template

```markdown
## Codebase Memory result

**Status:** graph used | local fallback | blocked
**Project:** `<indexed project or not available>`

| Question | Tool or fallback | Evidence | Confidence |
| --- | --- | --- | --- |
| `<symbol/flow/module>` | `search_graph` / `trace_path` / local search | `<snippet, path, or result id>` | high/medium/low |

### Coverage and freshness
- `index_status`: `<result or not available>`
- `check_index_coverage`: `<paths/scopes checked or not available>`
- Source confirmation: `<files opened or snippets confirmed>`

### Limitations
- `<pagination, truncation, stale index, or fallback notes>`
```

## Quality gate

- [ ] Graph conclusions are confirmed with source snippets or local files before edits or strong claims.
- [ ] Project, index freshness, and branch/change status are checked when relevant.
- [ ] Paginated `has_more`, `offset`, `scope_offset`, `next_offset`, `truncated`, and `cursor` streams are completed for exhaustive claims.
- [ ] Literal strings and config keys use `search_code` or local repository search, not broad graph discovery.
- [ ] Custom `query_graph` calls are schema-informed and bounded by `LIMIT` or `max_rows`.
- [ ] Unsafe actions such as `delete_project`, trace ingestion, ADR updates, or indexing are not performed without explicit user request or approval.
- [ ] Fallback behavior is reported when graph capability is unavailable or stale.
