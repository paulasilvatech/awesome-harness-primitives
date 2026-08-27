---
name: automate-this
description: >-
  Analyze a screen recording of a repetitive manual workflow, extract frames and optional
  narration, reconstruct the process, and produce tested automation scripts. Use this skill when
  the user asks to automate a recorded task, turn a screen recording into a script, replace
  repetitive browser, spreadsheet, email, file-management, terminal, or macOS GUI steps, or create
  dry-run automation.
---

<!-- Generated from harness/github-copilot/skills/automate-this/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Automate this

Analyze a user-provided screen recording, infer the manual workflow from sampled frames and narration, then propose and build practical automation using tools already available on the user's machine.

## When to invoke

- "I recorded myself doing this task; automate it."
- "Turn this screen recording into a script."
- "Can you automate this repetitive browser and spreadsheet workflow?"
- "Make a dry-run script for the file organization I recorded."
- "Watch this video and suggest quick automation tiers."

## Inputs

Use the video file path supplied in `$ARGUMENTS` or in the user request. If no path is provided, ask for a recording path before running extraction commands. Treat recordings from `~/Desktop/` as common but not required.

## Prerequisites and context

- `ffmpeg` is required for frame extraction and audio extraction. If missing, surface `brew install ffmpeg` on macOS or the platform equivalent.
- `whisper` or `whisper-cpp` is optional and needed only when the recording has narration.
- Use project-local or user-approved working directories for extracted media. Keep the identifier `WORK_DIR` for command consistency and never expose frames beyond the current user.

```bash
command -v ffmpeg >/dev/null 2>&1 && ffmpeg -version 2>/dev/null | head -1 || echo "NO_FFMPEG"
command -v whisper >/dev/null 2>&1 || command -v whisper-cpp >/dev/null 2>&1 || echo "NO_WHISPER"
```

## Procedure

1. Check prerequisites and stop only when `NO_FFMPEG` appears.
2. Extract frames from `VIDEO_PATH` into `WORK_DIR/frames` at `fps=0.5`; use one frame every 4 seconds for recordings longer than 5 minutes or more than 150 frames.
3. Check for audio with `ffprobe`; when present and Whisper is available, transcribe it to `WORK_DIR/audio.txt`.
4. Reconstruct the workflow from frames and transcript before proposing automation.
5. Present the reconstruction and require user confirmation before Phase 3. A wrong reconstruction produces useless automation.
6. Fingerprint the environment, then propose up to three tiers: Quick Win, Script, Full Automation.
7. When the user chooses a tier, write complete code, test with a dry run, fix failures, then show the real run path.
8. Clean up `WORK_DIR` after analysis.

## Extraction commands

```bash
WORK_DIR=".copilot/automate-this/$(date +%Y%m%d-%H%M%S)"
chmod 700 .copilot 2>/dev/null || true
mkdir -p "$WORK_DIR/frames"
ffmpeg -y -i "<VIDEO_PATH>" -vf "fps=0.5" -q:v 2 -loglevel warning "$WORK_DIR/frames/frame_%04d.jpg"
ls "$WORK_DIR/frames/" | wc -l
```

```bash
ffprobe -i "<VIDEO_PATH>" -show_streams -select_streams a -loglevel error | head -5
ffmpeg -y -i "<VIDEO_PATH>" -ac 1 -ar 16000 -loglevel warning "$WORK_DIR/audio.wav"

if command -v whisper >/dev/null 2>&1; then
  whisper "$WORK_DIR/audio.wav" --model small --language en --output_format txt --output_dir "$WORK_DIR/"
  cat "$WORK_DIR/audio.txt"
elif command -v whisper-cpp >/dev/null 2>&1; then
  whisper-cpp -m "$(brew --prefix 2>/dev/null)/share/whisper-cpp/models/ggml-small.bin" -l en -f "$WORK_DIR/audio.wav" -otxt -of "$WORK_DIR/audio"
  cat "$WORK_DIR/audio.txt"
else
  echo "NO_WHISPER"
fi
```

If Whisper is missing and audio exists, tell the user they are missing narration context and offer `pip install openai-whisper` or `brew install whisper-cpp`; continue with visual analysis if they decline.

## Process reconstruction

Extract these facts in order:

| Area | Questions to answer |
| --- | --- |
| Applications used | Browser, terminal, Finder, mail client, spreadsheet, IDE, or other apps. |
| Sequence of actions | Click-by-click and step-by-step workflow. |
| Data flow | Copied text, downloads, form inputs, generated files, and handoffs. |
| Decision points | Pauses, reviews, approvals, and conditional choices. |
| Repetition patterns | Same action repeated with different inputs. |
| Pain points | Slow, error-prone, or tedious steps, especially those named in narration. |

Use this confirmation format before automation:

```markdown
Here's what I see you doing in this recording:

1. Open <application> and navigate to <location>
2. <step>
3. <step>

You repeated steps <range> <count> times for <variants>.

Narration notes: <pain point or "none detected">

Does this match what you were doing? Anything I got wrong or missed?
```

## Environment fingerprint

```bash
echo "=== OS ===" && uname -a
echo "=== Shell ===" && echo $SHELL
echo "=== Python ===" && { command -v python3 && python3 --version 2>&1; } || echo "not installed"
echo "=== Node ===" && { command -v node && node --version 2>&1; } || echo "not installed"
echo "=== Homebrew ===" && { command -v brew && echo "installed"; } || echo "not installed"
echo "=== Common Tools ===" && for cmd in curl jq playwright selenium osascript automator crontab; do command -v $cmd >/dev/null 2>&1 && echo "$cmd: yes" || echo "$cmd: no"; done
```

Constrain recommendations to available tools unless installing one tool clearly unlocks the best path.

## Automation strategy matrix

| Workflow type | First choice | Fallbacks and notes |
| --- | --- | --- |
| Browser-based workflows | Public API or direct URL with query parameters | `curl`, `wget`, then Playwright or Selenium for UI-only flows. Prefer Playwright when clicking is unavoidable. |
| Spreadsheet and data workflows | Python with pandas | `csvkit` for quick CSV operations; openpyxl when output must remain Excel format. |
| Email workflows | Existing provider API or SMTP | macOS `osascript` for Mail.app; Python `smtplib` and `imaplib` for cross-platform send/read. |
| File management workflows | Shell scripts with `find` and `xargs` | `fswatch` or `watchman` for triggered automation. Date/type folder organization is often a 3-line shell script. |
| Terminal/CLI workflows | Shell aliases, shell functions, or loops | Makefiles for project-specific task sets. Repeated commands with different arguments become a loop. |
| macOS-specific workflows | AppleScript/JXA or Shortcuts.app | `automator` for file workflows; `launchd` plist files for schedules, preferred over cron on macOS. |
| Cross-application workflows | Replace clipboard handoffs with file, API, or direct integration | Preserve human review steps when the recording shows judgment. |

## Proposal tiers

| Tier | Setup target | Use when | Required content |
| --- | --- | --- | --- |
| Tier 1 - Quick Win | Under 5 minutes | One painful step can be simplified. | Alias, one-liner, keyboard shortcut, AppleScript snippet, or shell function. |
| Tier 2 - Script | Under 30 minutes | The full common path can be automated manually on demand. | Complete Bash, Python, or Node script with errors and dry run. |
| Tier 3 - Full Automation | Under 2 hours | Scheduling, logging, notifications, or integration scaffolding is valuable. | Tier 2 plus cron, `launchd`, or GitHub Actions, logging, and failure notification. |

Every script must include a dry run, avoid hardcoded secrets, account for missing files or changed formats, and say how to undo changes.

## Automation terminology

Use exact operational terms when they match the user's workflow: `$WORK_DIR`, `--dry-run`, `HTTP`, `TMPDIR`, `XXXXXX`, `automate-this-`, `command-line`, `double-click`, `end-to-end`, `file-based`, `mid-process`, `move/copy/rename`, `multi-app`, `multi-step`, `per-run`, `security`, `triggered-on-change`, and `visual-only`.

## Output template

```markdown
## Automate this - <recording name>

**Status:** reconstructed | proposed | built | blocked
**Recording:** `<VIDEO_PATH>`
**Working directory:** `<WORK_DIR>`

### Reconstruction
1. <observed step>
2. <observed step>

### Automation proposals
#### Tier 1: <name>
**What it automates:** <steps>
**What stays manual:** <steps>
**Time savings:** <estimate>
**Prerequisites:** <none or tools>
**How it works:** <plain-English summary>
**The code:**
```bash
<complete code>
```
**How to test it:** <dry-run steps>
**How to undo:** <rollback>

### Validation
- Prerequisites checked: pass | fail
- Reconstruction confirmed: yes | no
- Dry run: pass | fail
- Cleanup: pass | fail
```

## Quality gate

- [ ] `NO_FFMPEG` and `NO_WHISPER` checks were interpreted correctly.
- [ ] `VIDEO_PATH` and `WORK_DIR` are explicit in the output.
- [ ] Frames and audio were extracted only as needed and cleaned up afterward.
- [ ] The user confirmed the reconstruction before automation was built.
- [ ] Proposals match installed tools from the environment fingerprint.
- [ ] Each script includes dry-run behavior, error handling, and undo instructions.
- [ ] Secrets are read from environment variables, keychain access, or prompts, never hardcoded.
