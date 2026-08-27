---
description: Review and improve AI prompts for safety, bias, security risks, and effectiveness.
argument-hint: "target=<prompt-text-or-file> mode=<review|improve|both>"
---

<!-- Generated from harness/github-copilot/prompts/ai-prompt-engineering-safety-review.prompt.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# /ai-prompt-engineering-safety-review

## Objective

Review and improve an AI prompt for safety, bias, security, privacy, effectiveness, robustness, performance, and maintainability while preserving the prompt's intended function and teaching the prompt-engineering principles behind each recommendation.

## When to Invoke

Use this prompt before shipping, reusing, or broadening an AI prompt, especially when the prompt may affect users, handle sensitive context, perform actions, generate code, or be exposed to untrusted input.

## Preconditions

- The original prompt text, prompt file, or selected prompt content is available.
- The intended task, domain, audience, and operating context are known or can be inferred safely.
- The reviewer may propose an improved version but must not change files unless explicitly asked.
- Applicable responsible AI, security, privacy, or organizational prompt standards are available when the team requires them.

## Inputs the Team Must Provide

- `target` — the prompt text, selected content, or file to review.
- `mode` — `review`, `improve`, or `both`.
- Intended use case, audience, domain, deployment surface, and tool permissions.
- Known policy, compliance, safety, security, privacy, or brand requirements.
- Ask the user for anything that is missing when the missing fact changes the safety judgement.

## What I Will Do

- Evaluate harmful-content, violence, hate speech, misinformation, illegal-activity, personal-harm, bias, privacy, data-exposure, prompt-injection, information-leakage, access-control, clarity, context, constraints, format, specificity, and completeness risks.
- Identify the prompt pattern: zero-shot, few-shot, chain-of-thought, role-based, or hybrid.
- Score effectiveness, pattern fit, context utilization, input validation, error handling, scalability, maintainability, token efficiency, response quality, consistency, and reliability on a 1–5 scale.
- Produce critical issues, strengths, safety measures, bias mitigation strategies, security enhancements, technical improvements, testing recommendations, edge cases, and educational insights.
- Generate an improved prompt when requested, keeping the original intent intact.

## What I Will NOT Do

- Weaken safety, privacy, access-control, or security guardrails to improve convenience.
- Rewrite the task into a materially different workflow without calling out the change.
- Claim compliance with Microsoft, OpenAI, Google AI, or industry best practices unless the prompt was checked against the available requirements.
- Include hidden chain-of-thought requirements; use concise reasoning summaries and observable evaluation criteria instead.
- Treat high-risk domains as ordinary prompts without explicit misuse, edge-case, and failure-mode analysis.

## Output Format

Return the review in this structure:

```markdown
# Prompt Analysis Report

## Original Prompt
[User's prompt here]

## Task Classification
- **Primary Task:** [Code generation, documentation, analysis, etc.]
- **Complexity Level:** [Simple, Moderate, Complex]
- **Domain:** [Technical, Creative, Analytical, etc.]

## Safety Assessment
- **Harmful Content Risk:** [Low/Medium/High] - [Specific concerns]
- **Violence & Hate Speech:** [Low/Medium/High] - [Specific concerns]
- **Misinformation Risk:** [Low/Medium/High] - [Specific concerns]
- **Illegal Activities:** [Low/Medium/High] - [Specific concerns]
- **Bias Detection:** [None/Minor/Major] - [Gender Bias, Racial Bias, Cultural Bias, Socioeconomic Bias, Ability Bias]
- **Privacy Risk:** [Low/Medium/High] - [Data Exposure concerns]
- **Security Vulnerabilities:** [None/Minor/Major] - [Prompt Injection, Information Leakage, Access Control]

## Effectiveness Evaluation
- **Clarity:** [Score 1-5] - [Detailed assessment]
- **Context Adequacy:** [Score 1-5] - [Detailed assessment]
- **Constraint Definition:** [Score 1-5] - [Detailed assessment]
- **Format Specification:** [Score 1-5] - [Detailed assessment]
- **Specificity:** [Score 1-5] - [Detailed assessment]
- **Completeness:** [Score 1-5] - [Detailed assessment]

## Advanced Pattern Analysis
- **Pattern Type:** [Zero-shot/Few-shot/Chain-of-thought/Role-based/Hybrid]
- **Pattern Effectiveness:** [Score 1-5] - [Detailed assessment]
- **Alternative Patterns:** [Suggestions for improvement]
- **Context Utilization:** [Score 1-5] - [Detailed assessment]

## Technical Robustness
- **Input Validation:** [Score 1-5] - [Detailed assessment]
- **Error Handling:** [Score 1-5] - [Detailed assessment]
- **Scalability:** [Score 1-5] - [Detailed assessment]
- **Maintainability:** [Score 1-5] - [Detailed assessment]
- **Versioning:** [Changes trackable and reversible]

## Performance Metrics
- **Token Efficiency:** [Score 1-5] - [Detailed assessment]
- **Response Quality:** [Score 1-5] - [Detailed assessment]
- **Response Time:** [Optimization opportunities]
- **Consistency:** [Score 1-5] - [Detailed assessment]
- **Reliability:** [Score 1-5] - [Detailed assessment]

## Critical Issues Identified
1. [Issue 1 with severity and impact]
2. [Issue 2 with severity and impact]
3. [Issue 3 with severity and impact]

## Strengths Identified
1. [Strength 1 with explanation]
2. [Strength 2 with explanation]
3. [Strength 3 with explanation]

# Improved Prompt

## Enhanced Version
[Complete improved prompt with all enhancements]

## Key Improvements Made
1. **Safety Strengthening:** [Specific safety improvement]
2. **Bias Mitigation:** [Specific bias reduction]
3. **Security Hardening:** [Specific security improvement]
4. **Clarity Enhancement:** [Specific clarity improvement]
5. **Best Practice Implementation:** [Specific best practice application]

## Safety Measures Added
- [Safety measure 1 with explanation]
- [Safety measure 2 with explanation]
- [Safety measure 3 with explanation]
- [Safety measure 4 with explanation]
- [Safety measure 5 with explanation]

## Bias Mitigation Strategies
- [Bias mitigation 1 with explanation]
- [Bias mitigation 2 with explanation]
- [Bias mitigation 3 with explanation]

## Security Enhancements
- [Security enhancement 1 with explanation]
- [Security enhancement 2 with explanation]
- [Security enhancement 3 with explanation]

## Technical Improvements
- [Technical improvement 1 with explanation]
- [Technical improvement 2 with explanation]
- [Technical improvement 3 with explanation]

# Testing Recommendations

## Test Cases
- [Test case 1 with expected outcome]
- [Test case 2 with expected outcome]
- [Test case 3 with expected outcome]
- [Test case 4 with expected outcome]
- [Test case 5 with expected outcome]

## Edge Case Testing
- [Edge case 1 with expected outcome]
- [Edge case 2 with expected outcome]
- [Edge case 3 with expected outcome]

## Safety Testing
- [Safety test 1 with expected outcome]
- [Safety test 2 with expected outcome]
- [Safety test 3 with expected outcome]

## Bias Testing
- [Bias test 1 with expected outcome]
- [Bias test 2 with expected outcome]
- [Bias test 3 with expected outcome]

## Usage Guidelines
- **Best For:** [Specific use cases]
- **Avoid When:** [Situations to avoid]
- **Considerations:** [Important factors]
- **Limitations:** [Known limitations and constraints]
- **Dependencies:** [Required context or prerequisites]

# Educational Insights

## Prompt Engineering Principles Applied
1. **Principle:** [Specific principle]
   - **Application:** [How it was applied]
   - **Benefit:** [Why it improves the prompt]

## Common Pitfalls Avoided
1. **Pitfall:** [Common mistake]
   - **Why It's Problematic:** [Explanation]
   - **How We Avoided It:** [Specific avoidance strategy]
```

## Definition of Done

- [ ] Safety, bias, security, privacy, effectiveness, best-practices, advanced-pattern, technical-robustness, and performance areas were assessed.
- [ ] Risk ratings and 1–5 scores include specific evidence or clearly labeled assumptions.
- [ ] Critical issues and strengths are prioritized and actionable.
- [ ] The improved prompt preserves the original task while adding guardrails, constraints, and clearer output requirements.
- [ ] Testing recommendations include normal cases, edge cases, safety tests, and bias tests.
- [ ] Educational insights explain the principles applied and common pitfalls avoided.

## Prompt Body

Follow these steps in order.

**Step 1 — Classify the prompt.** Identify the primary task, complexity level, and domain. Determine whether the pattern is zero-shot, few-shot, chain-of-thought, role-based, or hybrid. Note whether the prompt is technical, creative, analytical, code generation, documentation, analysis, or another category.

**Step 2 — Assess safety.** Evaluate harmful content risk, violence and hate speech, misinformation risk, illegal activities, and potential personal harm. Always prioritize safety over functionality, flag potential risks with mitigation strategies, consider edge cases and misuse scenarios, recommend constraints and guardrails, and ensure alignment with responsible AI principles.

**Step 3 — Detect and mitigate bias.** Check for gender bias, racial bias, cultural bias, socioeconomic bias, and ability bias. Identify stereotypes, assumptions, exclusionary language, or unequal outcomes. Recommend concrete wording and evaluation changes that reduce bias while preserving task effectiveness.

**Step 4 — Review security and privacy.** Evaluate data exposure, prompt injection, information leakage, and access control. Identify whether the prompt could reveal sensitive or personal data, leak system or model information, bypass authorization, or mishandle untrusted input.

**Step 5 — Evaluate effectiveness and best practices.** Score clarity, context adequacy, constraint definition, format specification, specificity, and completeness. Check industry standards, ethical considerations, documentation quality, self-documenting structure, and maintainability.

**Step 6 — Analyze advanced patterns and robustness.** Evaluate pattern effectiveness, alternative patterns, context utilization, constraint implementation, input validation, error handling, scalability, maintainability, and versioning. Make changes trackable and reversible.

**Step 7 — Review performance.** Score token efficiency, response quality, response time, consistency, and reliability. Suggest concise rewrites only when they do not remove needed safety or context.

**Step 8 — Produce the improved prompt.** When `mode` is `improve` or `both`, generate a complete enhanced version that includes safety strengthening, bias mitigation, security hardening, clarity enhancement, best-practice implementation, safety measures, bias mitigation strategies, security enhancements, and technical improvements.

**Step 9 — Add testing and educational guidance.** Provide test cases, edge cases, safety tests, bias tests, usage guidelines, dependencies, limitations, prompt-engineering principles applied, benefits, common pitfalls, and avoidance strategies.

**Step 10 — Validate the review.** Confirm that recommendations are actionable, explanations are detailed, broader impact is considered, educational value is maintained, and best practices from Microsoft, OpenAI, and Google AI are referenced only as applicable standards, not unsupported certification claims.

## Invocation Example

```
/ai-prompt-engineering-safety-review target=prompts/support-agent.prompt.md mode=both
```
