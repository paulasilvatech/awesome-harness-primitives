# Manual accessibility checklist

Use `pass`, `fail`, `blocked`, or `not applicable` and record the exact state, environment, and evidence.

| Area | Procedure | Result | Evidence / limitation |
| --- | --- | --- | --- |
| Keyboard | Complete the critical flow with Tab, Shift+Tab, Enter, Space, Escape, and arrows where applicable. |  |  |
| Focus | Check visibility, order, initial focus, trapping, restoration, sticky overlays, and async/route changes. |  |  |
| Screen reader | Exercise one relevant path with the approved AT/browser or native combination. |  |  |
| Zoom/reflow | Test the approved zoom or dynamic-type settings and text spacing without lost content or controls. |  |  |
| Contrast modes | Check high contrast or forced colors plus supported light/dark themes. |  |  |
| Motion | Enable reduced motion and verify equivalent state, progress, and comprehension. |  |  |
| Forms/errors | Verify labels, instructions, timing, associations, summary, retained input, and recovery. |  |  |
| Async/streaming | Verify loading, status, live updates, interruption rate, focus stability, stop, retry, and recovery. |  |  |
| Media/data | Verify alternatives, captions/transcripts, summaries, tables, and keyboard-accessible controls. |  |  |
| Native profile | Verify dynamic type, VoiceOver/TalkBack, safe areas, lifecycle, gestures, windows, menus, or shortcuts as applicable. |  |  |

A blocked required row blocks accessibility readiness until an owner accepts the evidence gap explicitly.
