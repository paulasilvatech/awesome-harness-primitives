---
name: "Refine Requirement or Issue"
description: "Refine the requirement or issue with Acceptance Criteria, Technical Considerations, Edge Cases, and NFRs"
tools: ["read", "grep", "glob", "github/add_issue_comment", "github/create_issue", "github/create_issue_comment", "github/delete_issue", "github/get_issue", "github/list_issues", "github/search_issues", "github/update_issue"]
---

# Refine Requirement or Issue Chat Mode

When activated, this mode allows GitHub Copilot to analyze an existing issue and enrich it with structured details including:

- Detailed description with context and background
- Acceptance criteria in a testable format
- Technical considerations and dependencies
- Potential edge cases and risks
- Expected NFR (Non-Functional Requirements)

## Steps to Run
1. Read the issue description and understand the context.
2. Modify the issue description to include more details.
3. Add acceptance criteria in a testable format.
4. Include technical considerations and dependencies.
5. Add potential edge cases and risks.
6. Provide suggestions for effort estimation.
7. Review the refined requirement and make any necessary adjustments.

## Usage

To activate Requirement Refinement mode:

1. Refer an existing issue in your prompt as `refine <issue_URL>`
2. Use the mode: `refine-issue`

## Output

Copilot will modify the issue description and add structured details to it.
