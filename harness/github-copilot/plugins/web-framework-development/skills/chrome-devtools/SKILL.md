---
name: chrome-devtools
description: >-
  Handle `browser-related` tasks and control a live Chrome browser through Chrome DevTools MCP for browser automation, visual inspection, debugging, performance analysis, and emulation. Use when navigating pages, clicking elements, filling forms, handling `alerts/prompts.`, taking snapshots or screenshots, inspecting console and network activity, evaluating JavaScript, profiling Core Web Vitals, or testing viewport and network conditions.
license: "MIT"
---

# Chrome DevTools agent

Use Chrome DevTools MCP to operate a real browser tab, inspect accessibility snapshots and screenshots, debug console and network failures, evaluate page JavaScript, and capture performance evidence with stable element identifiers instead of guessing selectors.

## When to invoke

- "Open this page in Chrome and click through the form."
- "Take a screenshot and inspect what the browser renders."
- "Check the console and network errors for this failing page."
- "Profile this page for Core Web Vitals or layout shifts."
- "Emulate a mobile viewport or slow network condition."

## Prerequisites and context

- Chrome DevTools MCP must be available in the active environment.
- Interaction tools require `uid` values from the current accessibility snapshot; screenshots alone do not provide stable targets.
- Take a new snapshot after navigation, reloads, significant DOM changes, or modal/dialog state changes because `uid` values can change.

## Tool categories

| Category | Tools | Use |
| --- | --- | --- |
| Navigation and pages | `new_page`, `navigate_page`, `select_page`, `list_pages`, `close_page`, `wait_for` | Open a `tab/page.`, choose context, navigate, and wait for visible text. |
| Input and interaction | `click`, `fill`, `fill_form`, `hover`, `press_key`, `drag`, `handle_dialog`, `upload_file` | Operate controls using snapshot `uid` values. |
| Debugging and inspection | `take_snapshot`, `take_screenshot`, `list_console_messages`, `get_console_message`, `evaluate_script`, `list_network_requests`, `get_network_request` | Inspect DOM `text-based` accessibility tree, visuals, JavaScript errors, runtime state, and HTTP traffic, including `4xx/5xx` failures. |
| Emulation and performance | `resize_page`, `emulate`, `performance_start_trace`, `performance_stop_trace`, `performance_analyze_insight` | Test viewport/device conditions and `CPU/Network` or `network/CPU` throttling and profile load or interaction performance. |

## Workflow patterns

| Pattern | Steps | Evidence to report |
| --- | --- | --- |
| Snapshot-first interaction | Run `take_snapshot`, find the target `uid`, then call `click(uid=...)`, `fill(uid=..., value=...)`, or `press_key`; repeat snapshot after DOM changes. | Target role/name and action result. |
| Page failure triage | Run `list_console_messages`, `list_network_requests`, then inspect relevant entries with `get_console_message` or `get_network_request`. | Error text, status code, failed URL, initiator when available. |
| Visual verification | Use `take_snapshot` for structure and `take_screenshot` only when pixels, layout, or visual regression matter. | Screenshot path/description and matching accessibility evidence. |
| Performance profiling | Start trace with `performance_start_trace(reload=true, autoStop=true)` for a `load/trace` scenario or chosen interaction, stop or wait for auto-stop, then call `performance_analyze_insight`. | LCP, layout shift, long tasks, render-blocking resources, or other named insight. |
| Emulation | Set viewport or throttling with `resize_page` or `emulate`, rerun the scenario, then restore if needed. | Emulated condition and observed difference. |

## Gotchas

- **Use snapshots for element IDs**: `click` and `fill` need `uid` from `take_snapshot`; visual coordinates are brittle.
- **Refresh `uid` values after changes**: navigation, rerendering, and dialogs can invalidate prior snapshot IDs.
- **Check page context before acting**: run `list_pages` and `select_page` when multiple tabs are open or the active tab is uncertain.
- **Screenshots do not replace console/network evidence**: visual success can still hide failed API requests or JavaScript errors.
- **Performance traces need a defined scenario**: record page load or one user interaction, not an unbounded browsing session.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| Interaction hits the wrong element | Stale snapshot `uid` or wrong active page. | Run `list_pages`, `select_page`, and `take_snapshot` again before interacting. |
| `wait_for` times out | Text never appears, app is stuck, or wrong route loaded. | Check console and network, then verify current URL and snapshot. |
| Fill/click fails on custom control | Target `uid` belongs to wrapper, not focusable input. | Snapshot deeper nearby nodes; use `click` to focus then `press_key` or `fill` the input `uid`. |
| Performance trace has no useful insight | Scenario not captured or trace stopped too early. | Start a new trace with reload/interaction and wait for completion before analysis. |


- **Slow pages need explicit waits**: for `slow-loading` pages, wait for stable text or network evidence before declaring failure.

## Output template

```markdown
## Chrome DevTools result

**Status:** complete | needs follow-up | blocked
**Page:** <URL or page title>
**Scenario:** <navigation/debug/performance/emulation task>

### Evidence
- Snapshot: <role/name/uid evidence or not needed>
- Console: <errors or "none observed">
- Network: <failed requests or "none observed">
- Screenshot/performance: <artifact or insight>

### Actions performed
- `<tool>`: <result>
```

## Quality gate

- [ ] The correct page/tab was selected before interacting.
- [ ] Element interactions used current `uid` values from `take_snapshot`.
- [ ] Console and network evidence were checked for debugging tasks.
- [ ] Screenshots were used only when visual evidence was needed.
- [ ] Performance profiling included a bounded load or interaction scenario.
- [ ] The output follows `## Output template` exactly.
