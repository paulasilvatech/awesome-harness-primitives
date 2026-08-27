# Native accessibility profiles

## Mobile

- Respect dynamic type, display scaling, safe areas, orientation, lifecycle, and platform navigation.
- Use native accessibility labels, hints, traits or roles, values, actions, and traversal order.
- Test with VoiceOver or TalkBack on an approved simulator/emulator or device when available.
- Provide alternatives for complex gestures and preserve focus through navigation, permissions, and async updates.

## Desktop

- Support menus, keyboard shortcuts, window resizing, minimum sizes, dialogs, file pickers, multiple windows, and system contrast settings.
- Keep focus within the active window or modal and restore it after closure.
- Verify accessible names and roles across the web shell and native bridge.
- Treat IPC, native dialogs, and web content as separate trust and accessibility boundaries.

Do not infer native support from browser DOM evidence.
