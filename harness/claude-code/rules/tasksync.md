<!-- Generated from harness/github-copilot/instructions/tasksync.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Defines TaskSync V5 terminal task-request conventions for agents that intentionally run a continuous terminal-driven task loop.

# TaskSync V5 Conventions — Terminal Task Loop

These instructions apply only when a project intentionally uses TaskSync V5 to drive an agent through terminal-supplied tasks while the agent is running. They are authoritative for the TaskSync terminal input protocol, operational states, task-continuation priority, session tracking, and status messages; the active platform, user request, tool availability, safety policy, and explicit termination commands win where any TaskSync rule conflicts with higher-priority instructions.

## Terminal Input Protocol

Use a terminal input loop only for a TaskSync-enabled session. The universal task request command is:

```bash
python3 -c "import readline; task = input(''); print('Once done, ensure to follow ./tasksync.md file and ask for input again (add this to the todo list to not forget).')"
```

The universal question command is:

```bash
python3 -c "import readline; question = input('How can I help you? ')"
```

Legacy Windows examples may use `$task = Read-Host "Enter your task"` or `$task = Read-Host "Enter your task:"`; keep those examples only when the shell is PowerShell. Prefer the universal Python command for cross-platform terminal input. Treat `stop`, `end`, `terminate`, and `quit` as manual termination commands. Treat `none` as standby input rather than a new task.

## Operational States

Model TaskSync as explicit operational states instead of ad hoc chat behavior.

| State | Behavior | Transition |
| --- | --- | --- |
| State 1: Active Task Execution | Execute the current task with full focus, report progress for lengthy work, and avoid accepting unrelated terminal tasks until completion criteria are met. | Move to State 2 when the current task is fully complete or an urgent override is received. |
| State 2: Task Request Mode | Announce `Task completed. Requesting next task from terminal.` and request the next task through the terminal command. | Start the new task immediately when a task is provided; remain in standby on `none`; move to State 3 on termination command. |
| State 3: Manual Termination Only | Provide a concise session summary and confirm `Session terminated by user request.` | End only after explicit `stop`, `end`, `terminate`, or `quit`. |

Do not use TaskSync to bypass platform limits, user instructions, non-interactive constraints, or safety policy. A non-interactive environment may document the command without executing an input loop.

## Task Continuation Priority

Complete the current task or reach an explicit stopping point before processing a new terminal task. Completion criteria are: the current task is fully completed to specification, the user provides correction or redirection, or the terminal input includes urgent override text such as `stop current task`, `correction`, or `fix`.

Follow this processing order for terminal input: run the task request command, evaluate input for task content or special commands, begin task execution when task text exists, continue standby for `none`, execute termination protocol for `stop`, `quit`, `end`, or `terminate`, and handle urgent overrides before ordinary queued work.

## Session Tracking and Communication

Keep an in-memory task log during the session with a simple counter such as Task #1, Task #2, and current status. Use these status markers when useful: `[Tasksync Activated]`, `[Executing - Task #{}:]`, `Received task: ...`, `Urgent override detected. Stopping current task. Beginning: ...`, and `TaskSync Agent initialized. Requesting first task.`

Use chat for status information, and use the terminal command for interactive task input. Avoid phrases that imply an unintended automatic shutdown of an active TaskSync loop, including `Let me know if you need help`, `Feel free to ask`, `How can I help you`, `Is there anything else`, and `That's all for now`. When the user explicitly terminates, a concise final summary is appropriate.

## Configuration and Compatibility

TaskSync V5 references `./tasksync.md`, `instructions.md`, and `tasksync.chatmode.md` as project-level coordination artifacts. Do not assume those files exist unless the repository provides them, and do not require them for ordinary non-TaskSync work. The protocol uses `run_in_terminal` terminology in legacy examples; map it to the active terminal-execution tool only when that tool exists.

| Compatibility term | Meaning |
| --- | --- |
| `PRIMARY DIRECTIVE` | A TaskSync rule label from the original protocol; treat it as a TaskSync convention, not as higher authority than platform or user instructions. |
| `EMERGENCY OVERRIDE COMMAND` and `EMERGENCY ANTI-TERMINATION` | Legacy labels for retrying the terminal request loop when TaskSync is intentionally active. |
| `MANDATORY TERMINAL COMMAND EXECUTION`, `MANDATORY READ-HOST COMMAND`, `TERMINAL QUESTION MANDATORY`, and `NO AUTOMATIC TERMINATION EVER` | Legacy labels for requiring terminal task input within TaskSync sessions. |
| `Task Request Mode`, `Active Task Execution`, `Manual Termination Only`, `standby mode`, and `Continuous operation` | Names for the three-state loop and its idle behavior. |

## Good / Bad Examples

The examples below illustrate keeping TaskSync terminal input separate from ordinary completion language.

**Good:**

```text
[Executing - Task #2:]
Received task: fix database connection error
Urgent override detected. Stopping current task. Beginning: fix database connection error
Task completed. Requesting next task from terminal.
```

Why: The status identifies the task, records the urgent override, and routes the next task request through the TaskSync terminal channel.

**Bad:**

```text
The work is done. Let me know if you need help.
```

Why: In an active TaskSync session this implies the loop has ended and bypasses the terminal task request protocol.

## Baseline Compatibility Vocabulary

Preserve these legacy names, status labels, placeholders, paths, and configuration tokens when editing this instruction; they exist so older TaskSync, documentation, Dataverse, pandas, and troubleshooting examples remain searchable and recognizable.

- `ABSOLUTE`, `ABSOLUTELY`, `ACTION`, `ACTIVATION`, `AFTER`, `ALLOWED`, `ALWAYS`, `ANNOUNCE`
- `ANNOUNCEMENT`, `ASKING`, `ASSESSMENT`, `ATTENTION`, `AUTOMATICALLY`, `BANNED`, `BEGIN`, `BEHAVIOR`
- `CHECKLIST`, `CIRCUMSTANCES`, `COMMUNICATION`, `COMPLETION`, `COMPLIANCE`, `CONCLUDE`, `CONCLUDING`, `CONTINUATION`
- `CONTINUE`, `CONTINUOUS`, `CONTINUOUSLY`, `CONVERSATION`, `CRITERIA`, `CRITICAL`, `CYCLE`, `DEFAULT`
- `DELAYS`, `DIRECT`, `DIRECTIVES`, `ENDINGS`, `ENFORCEMENT`, `ERROR`, `EVERY`, `EXCEPTION`
- `EXCEPTIONS`, `EXECUTE`, `FINAL`, `FLOW`, `FOLLOWED`, `FORBIDDEN`, `FOREVER`, `FROM`
- `FULL`, `GOODBYE`, `HANDLING`, `HELP`, `IMMEDIATE`, `IMMEDIATELY`, `INCOMPLETE`, `INDEFINITE`
- `INITIALIZATION`, `INPUT`, `MALFUNCTIONING`, `MANUAL`, `MODELS`, `MUST`, `NEVER`, `NONE`
- `OFFERS`, `ONLY`, `OPERATION`, `OPTIONAL`, `PAUSES`, `PAUSING`, `PHRASES`, `PRIORITY`
- `PROCESSING`, `PROTOCOL`, `PROVIDED`, `REQUEST`, `REQUESTING`, `REQUIRED`, `RESPONSES`, `RULE`
- `RULES`, `SEQUENCE`, `SESSION`, `SESSIONS`, `SHELL`, `SPECIAL`, `SPECIFICATION`, `STATE`
- `STATEMENTS`, `STATUS`, `STOP`, `SUMMARY`, `TASK`, `TASKS`, `TERMINATE`, `THAT`
- `THEN`, `THESE`, `THIS`, `TOOL`, `TRACKING`, `TRANSPARENCY`, `UNDER`, `URGENT`
- `USER`, `VALIDATION`, `WHATSOEVER`, `WITHOUT`, `active/completed/standby`, `auto-termination`, `chat/conversation/session`, `communication_protocol`
- `error_handling`, `operational_states`, `response_structure`, `session_management`, `success_criteria`, `task_continuation_priority`, `terminal_input_protocol`, `timeout_management`

## Conventions

| Rule | Rationale |
|---|---|
| Use TaskSync V5 only for sessions intentionally configured for terminal-driven task input | Ordinary agent sessions should not inherit an infinite input loop by accident |
| Request tasks with the universal `python3 -c` command, or `Read-Host` only in PowerShell-specific contexts | A single input mechanism keeps task intake predictable across shells |
| Complete the current task before processing a new ordinary task | Task switching without completion loses work and makes status tracking unreliable |
| Treat `stop`, `end`, `terminate`, and `quit` as manual termination commands | The user needs clear control over ending the loop |
| Treat `none` as standby and urgent override phrases as current-task interruption | Standby and override behavior remain explicit rather than inferred |
| Track task count, current status, and completed task history in memory | Status reporting and session summaries need reliable context |
| Keep TaskSync labels such as `PRIMARY DIRECTIVE` subordinate to platform and user instructions | Local protocol wording cannot override higher-priority safety or execution constraints |
| Avoid active-loop concluding phrases during TaskSync operation | The protocol depends on terminal task requests, not chat endings |

## Do / Do Not

| Do | Do not |
|---|---|
| Announce `Task completed. Requesting next task from terminal.` in an active TaskSync loop | End an active TaskSync loop with a generic offer for more help |
| Use the universal Python input command for cross-platform task requests | Use PowerShell `Read-Host` commands on non-PowerShell shells |
| Process `stop current task`, `correction`, and `fix` as urgent override indicators when they are supplied through the terminal | Interrupt current work for unrelated ordinary input before completion criteria are met |
| Maintain Task #1, Task #2, and current status in memory | Lose task history across loop iterations |
| Confirm `Session terminated by user request.` only after explicit termination input | Claim the session ended automatically |
| Document `./tasksync.md`, `instructions.md`, and `tasksync.chatmode.md` as optional project artifacts | Assume those files exist in every repository |
| Map `run_in_terminal` to the active tool only when available | Invent a terminal tool or execute unsupported input loops |

## Checklist Before Opening a PR

- [ ] TaskSync guidance is framed as conventions for intentional terminal-driven sessions, not universal agent behavior.
- [ ] The universal Python task request command and question command are preserved exactly.
- [ ] PowerShell `Read-Host` examples are clearly legacy or shell-specific.
- [ ] Operational states, task continuation priority, urgent override handling, standby behavior, and manual termination commands are documented.
- [ ] Session tracking covers task count, current status, completed tasks, and concise termination summaries.
- [ ] TaskSync labels do not claim authority over higher-priority platform, safety, user, or tool constraints.
- [ ] The file contains no automatic requirement to execute an unsupported terminal loop in non-interactive environments.
