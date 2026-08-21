# Create Issue

Create a Story, Task, Bug, or Spike from conversation context. Automatically infers the issue type based on what's being described. Leaf node in the hierarchy - no further decomposition offered.

## Workflow

### Step 1 - Determine Context

Two entry modes:

- **Chained from Epic**: Context carries down. The Epic's goal, AC, and dependencies are established. The grill narrows to implementation specifics.
- **Standalone**: Full grill. No parent Epic context.

If chained, the parent Epic key is known. If standalone, ask: "Is this part of an existing Epic? [Epic key / no]"

### Step 2 - Type Inference

Determine the issue type from the conversation context:

| Signal | Type | Project | Notes |
|--------|------|---------|-------|
| User-facing behavior change, UI, API contract | **Story** | RHIDP | Uses Story template |
| Internal: CI, refactoring, tooling, tests, infra | **Task** | RHIDP | Uses Task template |
| Something is broken, regression, unexpected behavior | **Bug** | RHDHBUGS | Uses Bug template. **Do not include customer information - RHDHBUGS is public.** |
| Bug from a support case | **Bug** | RHDHSUPP | Uses Bug template. Support-originated - link to customer case. See `references/support.md`. |
| CVE, vulnerability, security advisory | **Vulnerability** | RHIDP | Requires Security component. Uses Story template and grill questions. |
| "Investigate", "research", "spike", "explore", "POC", unknown scope | **Task** (spike) | RHIDP | Summary prefixed with `SPIKE:`. Requires time-boxed story points. |

Confirm the inference with the user: "This sounds like a {type}. Correct?"

If the user disagrees, adjust. Additional disambiguation questions:

- Story vs Task: "Is this user-facing (Story) or internal engineering work (Task)?"
- Bug project: "Is this from a support case? (RHDHSUPP) Or a product defect? (RHDHBUGS)"
- Vulnerability: "Is this a CVE or security advisory? (Vulnerability in RHIDP with Security component)"

### Step 3 - Draft from Context

Load the appropriate template and example from `assets/templates/` and `assets/examples/` (see `references/templates.md` for the mapping).

Synthesize: Draft as many template sections as possible from the conversation (and parent Epic if chained). If chained, pre-fill Background (link to parent Epic) and Dependencies.

Present the draft: "Here's what I have. Review and tell me what's missing."

### Step 4 - Fill Gaps

For unfilled sections, ask targeted questions based on the inferred type:

**Story gaps:**

1. **User story** - "As a \<persona\> trying to \<action\> I want \<outcome\>"
2. **Background** - context and motivation
3. **Out of scope** - what's not included
4. **Approach** - general technical path, schemas, class definitions
5. **Dependencies** - linked Stories/Epics, QE/Doc impact
6. **Acceptance Criteria** - edge cases, minimum test list, docs/demo/SOP needs

**Task gaps:**

1. **Task description** - what needs to happen and why
2. **Background** - context if not obvious
3. **Dependencies and Blockers** - QE/Doc impact
4. **Acceptance Criteria** - what does "done" look like

**Bug gaps:**

1. **Description of problem** - what's wrong
2. **Prerequisites** - setup, versions, operators
3. **Steps to Reproduce** - numbered steps
4. **Actual results** - what happens
5. **Expected results** - what should happen
6. **Reproducibility** - Always/Intermittent/Only Once
7. **Build Details** - version, environment
8. **Additional info** - logs, screenshots

**Spike gaps:**

1. **What are we investigating?** - the question to answer
2. **Why?** - what decision depends on this research
3. **Time-box** - "How many story points to allocate?" (required for spikes)
4. **Expected output** - what deliverable closes this spike (doc, ADR, prototype, go/no-go recommendation)

Skip questions the draft already answered.

### Step 5 - Challenge

Follow the challenging behavior in `references/grill.md`.

### Step 6 - Infer Fields

Infer all Jira fields per `references/grill.md` Field Inference. If chained, inherit Priority, Team, and Component from parent Epic. Key fields: Priority, Component, Assignee, and Story Points (required for Spikes as time-box).

### Step 7 - Review

Render the filled template and inferred fields as a temporary markdown file for user review:

```bash
cat > /tmp/issue-review.md << 'EOF'
## {Type}: {summary}

### Description
{filled template content}

### Fields
- **Type**: {inferred type}
- **Project**: {project}
- **Priority**: {value}
- **Component**: {value}
- **Assignee**: {value}
- **Story Points**: {value}
EOF
```

Present to the user: "Review the issue before creating. [approve / edit / cancel]"

### Step 8 - Duplicate Check

Run the pre-creation check from `references/duplicates.md`. Scope to the target project and type.

### Step 9 - Create Issue

Fill the template. Create the issue:

```bash
# Story
acli jira workitem create --project RHIDP --type Story \
  --summary "Story summary" \
  --description-file /tmp/story-desc.txt \
  --assignee "ACCOUNT_ID" \
  --priority "Major" \
  --component "Plugins" \
  --yes

# Bug (different project)
acli jira workitem create --project RHDHBUGS --type Bug \
  --summary "Bug summary" \
  --description-file /tmp/bug-desc.txt \
  --priority "Critical" \
  --yes

# Spike (Task with prefix)
acli jira workitem create --project RHIDP --type Task \
  --summary "SPIKE: Research multi-source catalog merging" \
  --description-file /tmp/spike-desc.txt \
  --assignee "ACCOUNT_ID" \
  --priority "Major" \
  --component "Plugins" \
  --yes
```

If a parent Epic exists, link via REST:

```bash
curl -s -X PUT -u "$AUTH" -H "Content-Type: application/json" \
  -d '{"fields": {"parent": {"key": "RHIDP-XXX"}}}' \
  "https://redhat.atlassian.net/rest/api/3/issue/RHIDP-YYY"
```

Set Story Points via REST if acli fails - follow API preference order in SKILL.md.

### Step 10 - Comments

Follow the comment suggestion behavior from `references/grill.md` - proactively suggest decision trail, elaboration, and abandoned paths as comments.

## Error Handling

| Error | Action |
|-------|--------|
| RHIDP/RHDHBUGS project inaccessible | Stop. User lacks project access. |
| Type inference ambiguous | Ask the user directly. |
| `acli create` fails | Fall back to REST API. |
| Parent Epic link fails | Report failure. Issue is created - user can link manually. |
| Spike without time-box | Do not create. Ask: "Spikes require a time-box. How many story points?" |

## Caveats

1. **Bugs go to RHDHBUGS.** Never create Bugs in RHIDP. RHDHBUGS is a public project - no customer information in the description.
2. **Spikes are Tasks, not a separate type.** Identified by the `SPIKE:` prefix in the summary. Always time-boxed.
3. **No further decomposition.** Stories, Tasks, and Bugs are leaf nodes. If the scope is too large for a single issue, suggest splitting into multiple issues or promoting to an Epic.
4. **Done Checklist.** Stories include a Done Checklist in the template. Remind the user this is part of the definition of done.
