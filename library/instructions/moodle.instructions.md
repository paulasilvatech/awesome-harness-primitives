---
applyTo: "**/*.php,**/*.js,**/*.mustache,**/*.xml,**/*.css,**/*.scss"
description: "Enforces Moodle project conventions for plugin layout, PHP compatibility, security APIs, renderers, Mustache templates, JavaScript modules, and Moodle API usage."
name: "Moodle Conventions"
---

# Moodle Conventions — Plugin and Theme Development

These instructions apply to Moodle PHP, JavaScript, Mustache, XML, CSS, and SCSS files. They are authoritative for Moodle plugin layout, Frankenstyle names, Moodle API usage, security checks, renderers, templates, CLI scripts, and theme customization in matched files; the specific Moodle core version used by the project wins for PHP syntax, available APIs, and compatibility boundaries.

## Platform and Compatibility

Write code that matches the Moodle version in the repository, such as Moodle 3.11, Moodle 4.1 LTS, or later. Do not use PHP 7.4, PHP 8.0, or PHP 8.1 language features unless the target Moodle core version supports them. Follow the official Moodle Coding guidelines and prefer Moodle-recommended approaches when multiple implementations are possible.

## Plugin Structure and Frankenstyle Names

Use the Moodle component name as the namespace and directory authority.

| Plugin concern | Convention |
| --- | --- |
| Component names | Use Frankenstyle names such as `local_myplugin`, `mod_forum`, `block_mycatalog`, and `tool_mytool`. |
| Required files | Include `/version.php`; include `/settings.php`, `/lib.php`, or other entry points only when the plugin type or feature requires them. |
| Database | Put install schema in `/db/install.xml` and upgrades in `/db/upgrade.php`. |
| Language strings | Put strings under `/lang`. |
| Classes | Put PHP classes under `/classes` with Moodle namespaces that match the component. |
| Forms | Put Moodle forms in `classes/form` and extend `moodleform` where form handling is required. |
| Output | Put renderable output classes in `classes/output` and templates in `/templates`. |

Keep plugin directories compatible with standard Moodle plugin types including local, block, mod, auth, enrol, and tool.

## Security and Moodle APIs

Use Moodle security functions and APIs instead of direct superglobals, string-built SQL, or ad hoc permission checks.

- Require authentication with `require_login()` before protected pages or actions.
- Enforce permissions with `require_capability()` at the correct context.
- Read input with `required_param()` and `optional_param()` using the correct parameter type.
- Use `$DB` with SQL placeholders for database access.
- Prefer Moodle API functions over manual code whenever the API exists.
- Do not invent Moodle functions that do not exist.
- Include CLI script safeguards when creating scripts intended for Moodle CLI execution.

## Rendering, Templates, and JavaScript

Separate presentation from business logic.

| Area | Convention |
| --- | --- |
| HTML | Use renderers and Mustache templates rather than mixing HTML inside PHP. |
| Templates | Keep display markup in `.mustache` files under `/templates`. |
| JavaScript | Use AMD modules rather than inline scripts. |
| CSS and SCSS | Keep theme and plugin styling scoped to the plugin or theme responsibility. |
| External integrations | Use Moodle APIs and configured services rather than hand-rolled integration glue. |

## Database, Forms, and Upgrade Changes

Represent database schema changes in Moodle-owned files. Create new tables in `db/install.xml`, and write versioned upgrade logic in `db/upgrade.php` (`db/upgrade.php.` in legacy validator vocabulary). Generate forms with `moodleform` and route form data through Moodle parameter validation, capability checks, and APIs before persistence. Always include full file paths when describing or generating Moodle files so the component and plugin type are clear.

## Good / Bad Examples

The examples below illustrate safe parameter handling, login and capability checks, and placeholder-based database access.

**Good:**

```php
require_login();
$context = context_system::instance();
require_capability('local/myplugin:manage', $context);

$id = required_param('id', PARAM_INT);
$record = $DB->get_record('local_myplugin_items', ['id' => $id], '*', MUST_EXIST);
```

Why: The page requires a session, checks capability in context, validates input with `required_param()`, and uses `$DB` APIs instead of string-built SQL.

**Bad:**

```php
$id = $_GET['id'];
$record = $DB->get_record_sql("SELECT * FROM {local_myplugin_items} WHERE id = $id");
echo '<div>' . $record->name . '</div>';
```

Why: The code bypasses Moodle parameter handling, risks SQL injection, omits access checks, and mixes HTML into PHP instead of using a renderer and Mustache template.

## Conventions

| Rule | Rationale |
| --- | --- |
| Match the Moodle core version and supported PHP version | Unsupported syntax breaks deployments on older supported Moodle stacks. |
| Follow Moodle Coding guidelines | Code remains consistent with Moodle review and maintenance expectations. |
| Use Frankenstyle component namespaces | Autoloading and plugin ownership remain predictable. |
| Keep plugin files in `/db`, `/lang`, `/classes`, `/templates`, `/version.php`, `/settings.php`, and `/lib.php` as appropriate | Moodle discovers plugin metadata, schema, strings, classes, and output correctly. |
| Use `$DB` placeholders, `require_login()`, `require_capability()`, `required_param()`, and `optional_param()` | Authentication, authorization, input validation, and SQL safety are enforced. |
| Use renderers, `classes/output`, and Mustache templates for HTML | Presentation stays testable and theme-compatible. |
| Use AMD modules for JavaScript | Client behavior follows Moodle's module loading model. |
| Include full paths when generating Moodle files | Reviewers can verify the plugin type and component placement. |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use the Moodle component namespace such as `local_myplugin` | Use arbitrary namespaces that do not match the plugin component. |
| Put schema in `db/install.xml` and upgrades in `db/upgrade.php` | Modify database schema from unrelated PHP pages. |
| Build forms with `moodleform` | Hand-code Moodle form handling without validation. |
| Use `$DB` APIs with placeholders | Concatenate request parameters into SQL. |
| Render HTML through renderers and Mustache | Echo large HTML fragments from PHP classes. |
| Use AMD modules for JavaScript | Add inline scripts to PHP output. |
| Prefer documented Moodle APIs | Invent helper functions that Moodle core does not provide. |

## Checklist Before Opening a PR

- [ ] PHP syntax and APIs match the repository's Moodle core version and supported PHP runtime.
- [ ] Moodle Coding guidelines are followed.
- [ ] Plugin namespaces and paths use the correct Frankenstyle component name.
- [ ] New plugin files are placed under the appropriate `/db`, `/lang`, `/classes`, `/templates`, `/version.php`, `/settings.php`, or `/lib.php` paths.
- [ ] Protected actions call `require_login()` and `require_capability()` with the correct context.
- [ ] Input uses `required_param()` or `optional_param()` with explicit parameter types.
- [ ] Database code uses `$DB` APIs and SQL placeholders.
- [ ] HTML output uses renderers and Mustache templates, not inline PHP markup.
- [ ] JavaScript uses AMD modules instead of inline scripts.
- [ ] Any answer or generated change identifies files with full paths.

## References

- Moodle Coding guidelines: https://moodledev.io/general/development/policies/codingstyle
