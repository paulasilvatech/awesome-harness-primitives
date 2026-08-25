---
name: frontend-mobile-desktop-testing
description: "Plan and verify mobile and desktop frontend behavior across React Native, Expo, Flutter, SwiftUI, Compose, Electron, Tauri, simulators, emulators, devices, lifecycle, gestures, windows, shortcuts, IPC, offline, and native accessibility. Use this skill when a non-browser surface requires runtime evidence."
---

# Frontend mobile and desktop testing

Select platform-appropriate evidence for native, hybrid, and desktop-shell experiences without pretending browser tests prove device or operating-system behavior.

## When to invoke

- "Create a device test matrix for this mobile app."
- "Validate React Native, Expo, Flutter, SwiftUI, or Compose behavior."
- "Test Electron or Tauri window, shortcut, IPC, and offline flows."
- "Review lifecycle, deep links, permissions, gestures, and safe areas."
- "Plan simulator, emulator, and real-device accessibility evidence."

## Profile detection

Detect framework, versions, native projects, build tools, package identifiers, navigation, permissions, deep links, update mechanism, test runners, CI, supported OS versions, architectures, and approved devices.

Read [references/device-matrix.md](references/device-matrix.md) before selecting coverage. A profile may be `not applicable` only with evidence.

## Mobile testing

Read [references/mobile-testing.md](references/mobile-testing.md).

Cover when applicable: cold/warm start, foreground/background, termination, state restoration, deep links, permissions, safe areas, orientation, keyboard, gestures with alternatives, offline sync, conflict, push, app updates, dynamic type, VoiceOver/TalkBack, memory, battery, and frame behavior.

## Desktop testing

Read [references/desktop-testing.md](references/desktop-testing.md).

Cover when applicable: first launch, window creation, resizing, minimum size, restore, multiple windows, menus, shortcuts, dialogs, file access, drag/drop alternatives, IPC trust boundaries, offline, updates, packaging, OS themes, high contrast, and screen-reader behavior.

## Evidence rules

- Separate unit/component, simulator/emulator, real device, packaged build, and OS-specific evidence.
- Record OS, device/model, architecture, runtime, app build, locale, permissions, network, accessibility settings, and lifecycle state.
- Use the repository's established Maestro, Detox, Appium, XCTest, XCUITest, JUnit, Compose UI, Espresso, Flutter, Playwright, or WebdriverIO setup.
- Treat platform credentials and device-farm uploads as explicit operational boundaries.

## Limits

- Do not install a device runner, simulator, SDK, or paid service implicitly.
- Do not claim native iOS or Android implementation capability without a representative pilot.
- Do not treat web DOM or a desktop renderer test as proof of native shell, IPC, packaging, or OS behavior.
- Do not capture real notifications, contacts, files, photos, accounts, or personal data in fixtures or evidence.

## Progressive disclosure and bundled resources

- [references/device-matrix.md](references/device-matrix.md): risk-based matrix.
- [references/mobile-testing.md](references/mobile-testing.md): mobile lifecycle and accessibility.
- [references/desktop-testing.md](references/desktop-testing.md): windows, native bridge, and packaging.
- [evals/evals.json](evals/evals.json): representative output evaluations.

## Output template

```markdown
## Mobile/desktop test result
**Status:** ready | needs environment | blocked
**Profile:** <framework, platform, version>

### Matrix
| OS/device/build | Lifecycle/window state | Input/accessibility | Scenario | Result |
| --- | --- | --- | --- | --- |

### Evidence gaps
- <real device, packaging, credential, store, or OS check>
```

## Quality gate

- [ ] Framework, platform versions, build type, support matrix, runners, and operational boundaries were detected.
- [ ] Lifecycle, permissions, deep links, safe areas, input, offline, update, and accessibility behavior is covered when applicable.
- [ ] Window, menu, shortcut, dialog, file, IPC, packaging, and OS behavior is covered for desktop profiles.
- [ ] Simulator/emulator, real-device, packaged-build, and OS evidence remain distinct.
- [ ] Environment metadata and safe synthetic data make results reproducible.
- [ ] Unsupported profiles and unavailable evidence are explicit.
