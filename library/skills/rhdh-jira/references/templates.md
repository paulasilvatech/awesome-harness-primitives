# Issue Templates

Jira wiki markup templates for each issue type. Each template lives in its own file under `assets/templates/`. Filled-in examples are under `assets/examples/`.

## Template Files

| Issue Type | Project | Template | Example |
|------------|---------|----------|---------|
| Feature | RHDHPLAN | `assets/templates/feature.txt` | `assets/examples/feature-example.txt` |
| Epic | RHIDP | `assets/templates/epic.txt` | `assets/examples/epic-example.txt` |
| Story | RHIDP | `assets/templates/story.txt` | `assets/examples/story-example.txt` |
| Task | RHIDP | `assets/templates/task.txt` | `assets/examples/task-example.txt` |
| Bug | RHDHBUGS | `assets/templates/bug.txt` | `assets/examples/bug-example.txt` |

Load the template file for the issue type being created. Read the example file for tone and detail calibration.

## Usage

Save a filled-in template to a temp file, then create the issue:

```bash
# Write filled template to file
cat > issue-desc.txt << 'EOF'
h1. EPIC Goal
Implement SSO integration for admin console.
...
EOF

# Create the issue
acli jira workitem create --project RHIDP --type Epic \
  --summary "SSO Integration for Admin Console" \
  --description-file issue-desc.txt \
  --assignee "@me" \
  --yes
```

## Field Requirements at Creation

Load `references/workflows.md` for full exit criteria per status. Key fields at creation (New status):

| Issue Type | Required Fields |
|------------|----------------|
| Feature | Assignee, Priority, Team |
| Epic | Assignee, Team, Priority, Component |
| Story | Assignee, Priority, Component |
| Task | Assignee, Priority, Component |
| Bug | Description (steps to reproduce), Priority |

## Notes

- **Feature Request** and **Outcome** templates exist in RHDHPLAN but are not used by the creation sub-commands. See `references/support.md` for Feature Request creation from support cases.
- **Bugs go to RHDHBUGS**, not RHIDP. Do not include customer information in RHDHBUGS - it's a public project.
- **Spikes** use the Task template with a `SPIKE:` prefix in the summary and a time-boxed story point estimate.
- **Sub-tasks** are created as children of an existing issue, not standalone. Use `acli jira workitem create --parent KEY` for sub-tasks.
