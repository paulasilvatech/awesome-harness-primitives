---
name: exam-ready
description: >-
  Prepare a student for an exam from provided study material and syllabus only. Use when the user shares notes, a PDF, or syllabus topics and asks what to study, to explain a topic from notes, prepare with limited time, generate exam-ready definitions, key points, keywords, diagram notes, MCQ tricks, or practice questions.
---

# Exam ready

Transform provided notes or PDFs plus a syllabus into short, exam-ready study outputs for each topic, staying strictly inside the supplied material and prioritizing topics when time is limited.

## When to invoke

- "I have an exam tomorrow on this subject; use my notes."
- "Explain this topic from my notes for my exam."
- "What do I need to know about this syllabus topic?"
- "I only have 2 hours, help me prepare."
- "Quiz me on these topics from the PDF."

## Prerequisites and context

- The student must provide study material as a PDF or pasted notes.
- The student must provide a syllabus as pasted text or a topic list.
- Optional inputs: exam type (`MCQ`, short-answer, or long-answer) and time available.
- If no study material is provided, say: "Please share your notes or PDF first. I won't use outside knowledge."
- If no syllabus is provided, say: "Please list your syllabus topics so I cover exactly what's being tested."
- If exam type is missing, default to long-answer format but ask once: "Is this MCQ or written?"

## Topic extraction rules

For each syllabus topic, extract only what appears in the provided material.

| Output part | Rule |
| --- | --- |
| Definition | One exam-ready sentence explaining what the topic is. |
| Key points | 3-5 examiner-expected points, short enough to memorize. |
| Keywords | Bold important terms the student should include in answers. |
| Diagram | If a figure appears, describe what it shows and what to label in two lines. |
| Exam sentence | 1-2 ready-to-write sentences for written exams. |
| MCQ trick | For MCQ exams, replace exam sentence with a recognition or elimination cue. |
| Cross-reference | Flag repeated keywords that link this topic to another topic. |
| Practice question | One examiner-style recall or application question. |

Do not explain full textbook context, add outside knowledge, or cover topics the syllabus did not ask for. Never tell the student to "read more" or "refer to chapter X"; give the usable exam material directly.

## Triage mode

When the student gives a time constraint such as "I have X hours", start with a priority list. Rank topics by explicit mark weightage, frequency in the material, and breadth of subtopics. If no weightage is given, prioritize topics that appear most in the PDF or notes.

| Time available | Output depth |
| --- | --- |
| `≤1 hour` | Definition, key points, and exam sentence or MCQ trick only; skip diagrams. |
| `1-3 hours` | Add keywords and one practice question per topic. |
| `>3 hours` | Include diagrams, cross-references, and practice questions. |

Expand topics in priority order, not syllabus order, when triage mode is active.

## Handling mismatches and missing material

| Situation | Response |
| --- | --- |
| Topic not found in notes | `This topic was not found in your notes. Check your material.` |
| PDF uses a different name or scope | `Your notes cover this as <X> — answering based on that.` |
| Syllabus is broader than notes | Cover only the note-backed portion and mark the rest as not found. |
| Student asks for outside explanation | Decline outside knowledge and offer to answer if they provide material. |
| Keyword appears under multiple topics | Add a cross-reference so the student can connect answers. |

## Output template

```markdown
## Exam-ready plan

**Status:** ready | needs notes | needs syllabus | blocked
**Exam type:** MCQ | short-answer | long-answer | not specified
**Time mode:** triage | standard

### Priority list
1. <topic> — <reason>

### <Topic Name>

**Definition:** <1 sentence>

**Key Points:**
- <point 1>
- <point 2>
- <point 3>

**Keywords to use:** **keyword1**, **keyword2**, **keyword3**

**Diagram (if any):** <what it shows and what to label>

**Write this in your exam:**
<1-2 ready-to-write sentences>

**MCQ trick:**
<only for MCQ; omit written-answer line when used>

**Cross-references:** <only when another topic shares keywords>

**Practice question:**
<examiner-style question>
```

## Quality gate

- [ ] Study material and syllabus were both provided, or the required missing-input message was returned.
- [ ] Every topic answer stays strictly inside the provided material.
- [ ] Topics not found in the material are explicitly marked as not found.
- [ ] MCQ output uses MCQ tricks instead of written exam sentences.
- [ ] Time-constrained requests start with a priority list and reduce depth when `≤1 hour`.
- [ ] Definitions, key points, keywords, diagrams, exam sentences, and practice questions are concise.
- [ ] The output follows `## Output template` exactly.
