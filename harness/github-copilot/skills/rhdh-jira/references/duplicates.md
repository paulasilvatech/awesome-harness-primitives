# Duplicate Detection

Search for potentially duplicate issues before creating a new one or during refinement audits. Runs automatically - no user prompt.

Uses GraphQL for bulk reads (skip acli). Authentication setup: see `references/auth.md`.

## Modes

### Pre-creation check

Run before creating any issue. The goal is to prevent duplicates, not to find them retroactively.

Input: proposed issue summary + project + type.

### Audit check

Run during refinement (`refine` Check 2). The goal is to flag existing issues that may be duplicates of each other.

Input: an existing issue's key + summary.

## Detection Steps

### Step 1 - Extract keywords

Extract 2-3 distinctive keywords from the issue summary:

- Skip stop words (the, a, an, is, for, to, in, of, and, or, with)
- Skip project names (RHDH, Backstage, Red Hat)
- Skip generic action words (update, fix, add, remove, implement, create)
- Keep domain-specific terms (catalog, RBAC, dynamic plugins, CI/CD, operator, helm)

If fewer than 2 distinctive keywords remain, the summary is too generic for reliable detection. Skip the check and note: "Summary too generic for duplicate detection - verify manually."

### Step 2 - Search

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -H 'X-ExperimentalApi: JiraIssueSearch' \
  -d '{
    "query": "query FindDuplicates { jira { issueSearchStable(cloudId: \"'"$CLOUD_ID"'\", issueSearchInput: {jql: \"project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS) AND summary ~ \\\"KEYWORD1 KEYWORD2\\\" AND status != Closed ORDER BY updated DESC\"}, first: 10) { edges { node { key summary status { name } assignee { name } issueType { name } } } } } }"
  }'
```

For pre-creation checks, also add `AND key != \"CURRENT_KEY\"` if comparing against an existing issue.

For type-scoped checks, add `AND issuetype = \"TYPE\"` to narrow results (e.g., only search Features when creating a Feature).

### Step 3 - Score overlap

For each result, compute word overlap with the proposed/source summary:

```
overlap = (shared_words / max(words_in_source, words_in_candidate)) × 100
```

Case-insensitive. Ignore stop words in the overlap calculation.

### Step 4 - Classify

| Overlap | Classification | Action |
|---------|---------------|--------|
| >80% | Likely duplicate | **Pre-creation:** "This likely already exists as {KEY}: {summary}. Use the existing issue?" **Audit:** Flag as "likely duplicate - review." |
| 40-80% | Possibly related | **Pre-creation:** "Possibly related to {KEY}: {summary}. Still create?" **Audit:** Flag as "possibly related - check for overlap." |
| <40% | Not a match | Skip silently. |

### Step 5 - Check existing links

Before flagging, check if a `Duplicate` issue link already exists between the two issues. If already linked, skip - it's a known duplicate.

## Limits

- Surface at most 3 candidates. If more than 3 match above 40%, the keywords are too generic.
- Exclude Closed issues from results (already resolved).
- Do not flag sub-tasks as duplicates of their parent (common false positive).

## Pre-creation flow

The duplicate check is automatic and does not prompt the user before searching. The flow:

1. Agent prepares to create an issue
2. Run duplicate detection with the proposed summary
3. If likely duplicate found: present it and ask "Use the existing issue instead?"
4. If possibly related found: present candidates and ask "Still create?"
5. If no matches: proceed with creation silently

## Error Handling

| Error | Action |
|-------|--------|
| `issueSearchStable` fails | See SKILL.md Error Handling. Skip duplicate check, proceed with creation. |
| GraphQL rate limit (429) | Wait 5 seconds, retry once. If still fails, skip check and note "duplicate check skipped." |
| Summary has <2 distinctive keywords | Skip check. Note "summary too generic for duplicate detection." |
