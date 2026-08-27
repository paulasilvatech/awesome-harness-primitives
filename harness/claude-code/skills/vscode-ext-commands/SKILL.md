---
name: vscode-ext-commands
description: >-
  Guide command contributions in VS Code extensions, including package.json command titles,
  categories, Command Palette visibility, Side Bar command naming, icons, enablement, when
  clauses, and view/title or view/item/context placement. Use when adding or updating commands in
  a VS Code extension.
---

<!-- Generated from harness/github-copilot/skills/vscode-ext-commands/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# VS Code extension command contribution

Add or update VS Code extension commands so `package.json` contributions expose clear Command Palette actions and correctly hidden Side Bar commands with titles, categories, icons, enablement, and menu placement.

## When to invoke

- "Add a command to my VS Code extension."
- "Update command contributions in `package.json`."
- "Make this command appear in the Command Palette."
- "Add a Side Bar button command with an icon and when clause."

## Command contribution rules

VS Code commands must always define a `title`, independent of category, visibility, or location.

| Command kind | Command ID pattern | Required fields | Visibility rule |
| --- | --- | --- | --- |
| Regular command | `<extensionId>.<commandName>` | `command`, `title`, `category` | Accessible in the Command Palette by default. |
| Side Bar command | `_extensionId.someCommand#sideBar` | `command`, `title`, `icon` | Side Bar exclusive commands should not be visible in the Command Palette. |
| View title command | Usually Side Bar pattern | `command`, `title`, `icon`; menu `group` | Contribute under `view/title` with a `when` clause and an order/position group. |
| View item context command | Usually Side Bar pattern | `command`, `title`; menu `group` | Contribute under `view/item/context` with a `when` clause matching item context. |

## Regular command pattern

- Define a user-facing `title` that starts with a verb.
- Define a `category` so Command Palette entries group under the extension name or feature area.
- Omit `icon` unless the command will be used in the Side Bar or another UI surface that displays icons.
- Keep command IDs stable; changing them breaks keybindings, menus, and user muscle memory.

## Side Bar command pattern

- Name Side Bar commands with a leading underscore and `#sideBar` suffix, for example `_extensionId.someCommand#sideBar`.
- Its name follows a special pattern, starting with underscore (`_`) and suffixed with `#sideBar`, like `_extensionId.someCommand#sideBar` for instance. Must define an `icon`, and may or may not have some rule for `enablement`.
- Define an `icon` because Side Bar buttons often render as icon-only actions.
- Add `enablement` when the command should be disabled instead of hidden.
- Add a menu `when` condition so the command is visible only in the intended view or item state.
- When contributing to `view/title` or `view/item/context`, specify an order or position through `group`, using terms relative to other command/button placement when needed; this is the original _order/position_ rule.
- Hide Side Bar exclusive commands from the Command Palette through an appropriate `menus.commandPalette` `when` condition.

## Examples

### Regular Command Palette command

```json
{
  "contributes": {
    "commands": [
      {
        "command": "extensionId.refreshData",
        "title": "Refresh Data",
        "category": "Extension Name"
      }
    ]
  }
}
```

### Side Bar exclusive command

```json
{
  "contributes": {
    "commands": [
      {
        "command": "_extensionId.refreshView#sideBar",
        "title": "Refresh View",
        "icon": "$(refresh)"
      }
    ],
    "menus": {
      "view/title": [
        {
          "command": "_extensionId.refreshView#sideBar",
          "when": "view == extensionId.views.main",
          "group": "navigation@10"
        }
      ],
      "commandPalette": [
        {
          "command": "_extensionId.refreshView#sideBar",
          "when": "false"
        }
      ]
    }
  }
}
```

## Gotchas

- **Do not omit `title`**: every command contribution needs one even when the command is hidden or icon-only.
- **Do not show Side Bar exclusive commands in the Command Palette**: hide them explicitly when they only make sense in a view.
- **Do not rely on menu position by accident**: use `group` order such as `navigation@10` when relative placement matters.
- **Do not use Side Bar naming for regular commands**: `_...#sideBar` communicates private UI placement.

## Output template

```markdown
## VS Code command contribution result

**Status:** ready | needs manifest context | blocked
**Command kind:** regular | Side Bar | view/title | view/item/context

| Command | Title | Category | Icon | Menu | Visibility |
| --- | --- | --- | --- | --- | --- |
| `<command id>` | `<title>` | `<category or n/a>` | `<icon or n/a>` | `<menu>` | `<Command Palette / Side Bar / hidden>` |

**Manifest changes:** `<package.json contribution summary>`
```

## Quality gate

- [ ] Every command defines a `title`.
- [ ] Regular commands define a `category` and remain accessible in the Command Palette.
- [ ] Side Bar command IDs start with `_` and end with `#sideBar`, for example `_extensionId.someCommand#sideBar`.
- [ ] Side Bar commands define an `icon`.
- [ ] Side Bar exclusive commands are hidden from the Command Palette.
- [ ] `view/title` and `view/item/context` menu contributions include an appropriate `when` condition.
- [ ] Menu placement uses `group` when order or relative position matters.
