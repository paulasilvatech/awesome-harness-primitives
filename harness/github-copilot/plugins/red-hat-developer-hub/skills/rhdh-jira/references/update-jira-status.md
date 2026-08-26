# Update Jira Status

Update a Jira issue with the current session's progress. Detects the related issue, adds a status comment summarizing the session, and proposes status transitions. Checks upward through the hierarchy and suggests parent transitions when all siblings are complete.

On-demand - run when you're at a natural stopping point.

Authentication setup: see `references/auth.md`. All examples below assume `AUTH`, `CLOUD_ID`, and `GRAPHQL_URL` are set per that file.

## Workflow

### Step 1 - Detect Related Issue

Search for the Jira issue related to the current session. Check in priority order - stop at the first match:

1. **Conversation context** - scan for issue keys mentioned in the conversation (RHIDP-1234, RHDHPLAN-567, RHDHBUGS-890)
2. **Git branch name** - parse the current branch for an issue key pattern:

   ```bash
   git branch --show-current 2>/dev/null | grep -oE '(RHIDP|RHDHPLAN|RHDHBUGS|RHDHSUPP)-[0-9]+'
   ```

3. **PR title/description** - if a PR exists for the current branch, check its title:

   ```bash
   gh pr view --json title,body 2>/dev/null
   ```

4. **Recent commits** - scan commit messages on the current branch:

   ```bash
   git log --oneline -10 2>/dev/null | grep -oE '(RHIDP|RHDHPLAN|RHDHBUGS|RHDHSUPP)-[0-9]+'
   ```

5. **Keyword search** - if no key found, extract topic keywords from the conversation and search Jira:

   ```bash
   jql: "project in (RHIDP, RHDHPLAN, RHDHSUPP, RHDHBUGS) AND summary ~ \"KEYWORD1 KEYWORD2\" AND status != Closed AND assignee = currentUser() ORDER BY updated DESC"
   ```

   Present candidates: "I found these possibly related issues - which one?"

If multiple distinct keys are found, ask: "This session touches multiple issues: {keys}. Which one(s) to update?"

If no match at all: "No related issue found. Want to create one?" → route to the appropriate creation command.

### Step 2 - Fetch Current Issue State

Query the issue to understand its current state:

```bash
acli jira workitem view ISSUE_KEY --json
```

Or via GraphQL for richer data (components, sprint, parent):

```bash
curl -s -u "$AUTH" "$GRAPHQL_URL" -X POST \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "query IssueState { jira { issueByKey(key: \"ISSUE_KEY\", cloudId: \"'"$CLOUD_ID"'\") { key summary status { name } issueType { name } priority { name } assignee { name accountId } storyPoints parentIssue { key summary status { name } } fields { edges { node { __typename name ... on JiraSprintField { selectedSprintsConnection { edges { node { name state } } } } } } } } } }"
  }'
```

Note the current status - this determines which transitions are available.

### Step 3 - Compose Status Comment

Summarize the current session's progress as a short status comment. The comment should be:

- **Concise** - 2-5 sentences. Not a full session log.
- **Actionable** - what was done, what's the current state, what's next (if applicable)
- **Factual** - avoid subjective assessments. State what happened.

Templates by situation:

**Work in progress:**
> "Started implementation. [Approach/what was done]. Next: [what remains]."

**Hit a blocker:**
> "Blocked on [dependency/issue]. [What was tried]. Waiting for [person/resolution]."

**Implementation complete, PR up:**
> "Implementation complete. PR: [link]. [Brief description of changes]."

**PR merged:**
> "PR merged and verified. [Any follow-up needed]."

**Abandoned approach:**
> "Investigated [approach]. Abandoned because [reason]. Switching to [alternative]."

**Scope discovery:**
> "Investigation revealed [finding]. Scope is [larger/smaller/different] than expected. [Recommendation]."

Confirm the comment with the user before posting:

> "Proposed status comment:\n\n{comment}\n\nPost this? [y/N/edit]"

Add via:

```bash
acli jira workitem comment --key ISSUE_KEY --comment "comment text" --yes
```

### Step 4 - Propose Status Transition

Based on session activity, propose a transition if applicable. Load `references/workflows.md` for exit criteria at the target status.

| Session activity | Proposed transition |
|-----------------|-------------------|
| Started working | New/To Do → In Progress |
| PR up for review | In Progress → Review |
| PR merged | Review → Closed |
| All work done, awaiting release | In Progress/Review → Release Pending |
| Descoped / won't fix | Any → Closed (with resolution + comment per Team Conventions in SKILL.md) |

Before proposing a transition, verify exit criteria are met for the target status. If not, flag what's missing: "To move to Review, you need: [missing fields]. Set them first?"

**Check for Jira automation.** Before suggesting a parent transition in Step 6, fetch the parent's current status first. Jira automation rules may have already cascaded the transition (e.g., child moving to In Progress automatically moves parent Epic to In Progress). If the parent already transitioned, skip the suggestion.

If no transition is applicable, skip this step silently.

Confirm with the user:

> "Move {KEY} from {current} to {target}? [y/N]"

Apply via:

```bash
acli jira workitem transition --key ISSUE_KEY --status "TARGET" --yes
```

### Step 5 - Propose Issue Links

If the session revealed dependencies or related issues not yet tracked:

- "You mentioned {KEY2} is blocking this - add a Blocks link?"
- "You discovered {KEY3} is related - add a Related link?"

Add via:

```bash
acli jira workitem link create --key ISSUE_KEY --link-type "Blocks" --target-key TARGET_KEY --yes
```

### Step 6 - Upward Cascade Check

After updating the issue, check if parent issues should transition too. One level at a time, each with confirmation.

If the issue has no `parentIssue` in the Step 2 response, skip the cascade check entirely.

**Check parent Epic:**

Query siblings of the updated issue:

```bash
jql: "parent = {epic_key}"
```

If ALL siblings are in a terminal status for their type - Closed for Stories/Tasks, Closed or Release Pending for Bugs:
> "All stories under {epic_key} ({epic_summary}) are complete. Transition Epic to Dev Complete? [y/N]"

If the user confirms, transition the Epic. Add a status comment: "All child issues complete. Transitioning to Dev Complete."

**Check parent Feature:**

If the Epic was transitioned, query sibling Epics of the parent Feature:

```bash
jql: "parent = {feature_key} AND issuetype = Epic"
```

If ALL sibling Epics are in Release Pending or Closed (Dev Complete is not sufficient - Epics still need Release Notes fields and demo links):
> "All Epics under {feature_key} ({feature_summary}) are complete. The Feature Owner is {owner}. Recommend reaching out to {owner} to transition the Feature to Release Pending."

Do not transition the Feature directly - that's the Feature Owner's responsibility. Suggest reaching out instead.

## Error Handling

| Error | Action |
|-------|--------|
| No issue detected | Offer keyword search. If no match, suggest creating an issue. |
| `git` not available | Skip git-based detection. Continue with conversation context and keyword search. |
| `gh` not available | Skip PR detection. Continue with other methods. |
| Issue is Closed | "This issue is already Closed. Open a new issue or reopen?" |
| Transition fails | Check exit criteria. Report which fields are missing. |
| Comment fails | Report error. Issue state is unchanged. |
| Parent query returns 0 siblings | Skip cascade check - issue may be unlinked. |

## Caveats

1. **On-demand only.** The agent does not proactively suggest status updates. Run this when you're ready.
2. **Git detection is best-effort.** Branch naming conventions vary - the agent always confirms before acting.
3. **Upward cascade stops at Feature.** The agent suggests the Feature transition but defers to the Feature Owner to apply it.
4. **Multiple issues per session.** If the session touched multiple issues, the agent asks which one(s) to update. Each update runs the full workflow independently.
5. **Resolution field.** When closing or descoping, set the resolution field and add a rationale comment - same convention as `refine.md` remediation.
