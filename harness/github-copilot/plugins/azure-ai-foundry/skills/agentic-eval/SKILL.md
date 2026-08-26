---
name: agentic-eval
description: >-
  Design evaluator-optimizer, reflection, rubric, LLM-as-judge, and test-driven refinement loops for AI agent outputs. Use when implementing self-critique, iterative improvement, quality gates, agent response evaluation, code refinement, or rubric-based scoring for generated code, reports, or analysis.
---

# Agentic evaluation patterns

Apply structured evaluation loops that generate, evaluate, critique, refine, and stop when objective criteria pass or iteration limits prevent further useful improvement.

## When to invoke

- "Add self-critique to this agent workflow."
- "Build an evaluator-optimizer loop for generated reports."
- "Create a rubric-based LLM-as-judge evaluator."
- "Improve generated code by running tests and fixing failures."
- "Measure and improve agent response quality."

## Evaluation loop patterns

```text
Generate -> Evaluate -> Critique -> Refine -> Output
    ^                              |
    +------------------------------+
```

| Pattern | Use when | Core rule |
| --- | --- | --- |
| Basic Reflection | One agent can judge and improve its own draft. | Return structured JSON with `PASS`/`FAIL` per criterion. |
| Evaluator-Optimizer | Quality-critical work benefits from separate generator and evaluator responsibilities. | Track `overall_score`, dimensions, and feedback. |
| Code-Specific Reflection | Generated code can be tested automatically. | Generate code, generate or run tests, fix errors, repeat. |
| Outcome-Based | Expected output or oracle exists. | Compare task, expected result, and actual output. |
| LLM-as-Judge | Need ranking or comparative assessment. | Compare output A and B against explicit criteria. |
| Rubric-Based | Dimensions have weights. | Score each dimension and compute weighted total. |

## Implementation details

Use clear criteria before generation starts. Set `max_iterations` to `3` by default and `3-5` only when cost and latency are acceptable. Stop when all criteria pass, `overall_score >= score_threshold`, tests pass, or scores stop improving.

Preserve these implementation names when translating examples into code: `reflect_and_refine`, `EvaluatorOptimizer`, `CodeReflector`, `evaluate_outcome`, `llm_judge`, `evaluate_with_rubric`, `generate`, `evaluate`, `optimize`, `run`, `run_tests`, `max_iterations`, `score_threshold`, `overall_score`, `criteria`, `critique_data`, `all_pass`, `failed`, `RUBRIC`, `accuracy`, `clarity`, and `completeness`.

Basic reflection skeleton:

```python
def reflect_and_refine(task: str, criteria: list[str], max_iterations: int = 3) -> str:
    output = llm(f"Complete this task:
{task}")
    for i in range(max_iterations):
        critique = llm(f"Evaluate this output against criteria: {criteria}
Output: {output}
Rate each: PASS/FAIL with feedback as JSON.")
        critique_data = json.loads(critique)
        all_pass = all(c["status"] == "PASS" for c in critique_data.values())
        if all_pass:
            return output
        failed = {k: v["feedback"] for k, v in critique_data.items() if v["status"] == "FAIL"}
        output = llm(f"Improve to address: {failed}
Original: {output}")
    return output
```

Evaluator-optimizer skeleton:

```python
class EvaluatorOptimizer:
    def __init__(self, score_threshold: float = 0.8):
        self.score_threshold = score_threshold

    def generate(self, task: str) -> str:
        return llm(f"Complete: {task}")

    def evaluate(self, output: str, task: str) -> dict:
        return json.loads(llm(f"Evaluate output for task: {task}
Output: {output}
Return JSON with overall_score and dimensions."))

    def optimize(self, output: str, feedback: dict) -> str:
        return llm(f"Improve based on feedback: {feedback}
Output: {output}")

    def run(self, task: str, max_iterations: int = 3) -> str:
        output = self.generate(task)
        for _ in range(max_iterations):
            evaluation = self.evaluate(output, task)
            if evaluation["overall_score"] >= self.score_threshold:
                break
            output = self.optimize(output, evaluation)
        return output
```

Code reflection skeleton:

```python
class CodeReflector:
    def reflect_and_fix(self, spec: str, max_iterations: int = 3) -> str:
        code = llm(f"Write Python code for: {spec}")
        tests = llm(f"Generate pytest tests for: {spec}
Code: {code}")
        for _ in range(max_iterations):
            result = run_tests(code, tests)
            if result["success"]:
                return code
            code = llm(f"Fix error: {result['error']}
Code: {code}")
        return code
```

## Evaluation criteria

| Criterion | Check |
| --- | --- |
| Clear criteria | Define specific measurable criteria before generation. |
| Structured output | Use JSON for reliable parsing of evaluation results. |
| Iteration limits | Prevent infinite loops with `max_iterations`. |
| Convergence | Stop if score does not improve between iterations. |
| History | Log the full trajectory for debugging and analysis. |
| Parse failures | Handle invalid evaluator JSON gracefully. |
| Safety | Do not let the optimizer remove requirements to pass the evaluator. |

Rubric example:

```python
RUBRIC = {
    "accuracy": {"weight": 0.4},
    "clarity": {"weight": 0.3},
    "completeness": {"weight": 0.3},
}
```

## Compatibility vocabulary

Preserve these legacy terms, API names, command placeholders, and literal phrases when applying or migrating this skill:

- `criteria/rubric`
- `quality-critical`
- `self-improvement`
- `single-shot`

## Output template

```markdown
## Agentic evaluation design

**Status:** designed | implemented | blocked
**Pattern:** Basic Reflection | Evaluator-Optimizer | Code-Specific Reflection | Outcome-Based | LLM-as-Judge | Rubric-Based

| Component | Responsibility | Inputs | Outputs | Stop condition |
| --- | --- | --- | --- | --- |
| Generator | <what creates the draft> | <task/spec> | <output> | <n/a> |
| Evaluator | <criteria or tests> | <output> | <JSON score/critique> | <threshold/pass> |
| Optimizer | <refinement action> | <feedback> | <revised output> | <max iterations/convergence> |

### Rubric or criteria
- <criterion>: <pass rule or weight>

### Validation
- <test, parse, score, or convergence check>
```

## Quality gate

- [ ] Criteria or rubric are defined before generation.
- [ ] Evaluator output is structured and parseable, preferably JSON.
- [ ] `max_iterations` and convergence checks prevent infinite refinement.
- [ ] Stop conditions are explicit and testable.
- [ ] Evaluation history is logged for debugging.
- [ ] Parse failures and non-improving iterations have fallback behavior.
- [ ] The optimizer preserves original task requirements rather than gaming the evaluator.
