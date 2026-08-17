---
applyTo: 'wp-content/plugins/**,wp-content/themes/**,**/*.php,**/*.inc,**/*.js,**/*.jsx,**/*.ts,**/*.tsx,**/*.css,**/*.scss,**/*.json'
description: 'Enforces secure WordPress plugin and theme conventions for hooks, coding standards, data handling, i18n, assets, REST, blocks, testing, and documentation.'
---

# WordPress Development Conventions — Plugins and Themes

These instructions apply to WordPress plugins, themes, PHP includes, JavaScript, TypeScript, CSS, SCSS, and JSON assets. They are authoritative for secure, performant, testable WordPress extension code that follows official WordPress practices; project-specific PHP version, build, deployment, and security policies win when they impose stricter requirements.

## Core Extension Principles

- Never modify WordPress core; extend through actions and filters.
- For plugins, include a valid plugin header and guard direct execution in entry PHP files.
- Use unique prefixes or PHP namespaces to avoid global collisions.
- Enqueue assets; never inline raw `<script>` or `<style>` in PHP templates.
- Make user-facing strings translatable and load the correct text domain.
- Prefer hooks, small functions, dependency injection where sensible, and clear separation of concerns.

```php
<?php
defined('ABSPATH') || exit;
/**
 * Plugin Name: Awesome Feature
 * Description: Example plugin scaffold.
 * Version: 0.1.0
 * Author: Example
 * License: GPL-2.0-or-later
 * Text Domain: awesome-feature
 * Domain Path: /languages
 */
```

## Coding Standards and Compatibility

Follow WordPress Coding Standards (WPCS), write DocBlocks for public APIs, and keep PHP compatible with PHP 7.4+ unless the project specifies a higher baseline. Prefer strict comparisons (`===`, `!==`) where appropriate, consistent array syntax and spacing per WPCS, WordPress JavaScript style for JS, `@wordpress/*` packages for block/editor code, BEM-like CSS class naming when helpful, and selectors that are not over-specific.

Use linting configurations like these when the project needs them:

```xml
<?xml version="1.0"?>
<ruleset name="Project WPCS">
  <description>WordPress Coding Standards for this project.</description>
  <file>./</file>
  <exclude-pattern>vendor/*</exclude-pattern>
  <exclude-pattern>node_modules/*</exclude-pattern>
  <rule ref="WordPress"/>
  <rule ref="WordPress-Docs"/>
  <rule ref="WordPress-Extra"/>
  <rule ref="PHPCompatibility"/>
  <config name="testVersion" value="7.4-"/>
</ruleset>
```

```json
{
  "require-dev": {
    "dealerdirect/phpcodesniffer-composer-installer": "^1.0",
    "wp-coding-standards/wpcs": "^3.0",
    "phpcompatibility/php-compatibility": "^9.0"
  },
  "scripts": {
    "lint:php": "phpcs -p",
    "fix:php": "phpcbf -p"
  }
}
```

```json
{
  "devDependencies": {
    "@wordpress/eslint-plugin": "^x.y.z"
  },
  "scripts": {
    "lint:js": "eslint ."
  }
}
```

## Security and Data Handling

Escape on output and sanitize on input.

| Concern | Required APIs and conventions |
| --- | --- |
| Escaping | Use `esc_html()`, `esc_attr()`, `esc_url()`, and `wp_kses_post()`. |
| Sanitization | Use `sanitize_text_field()`, `sanitize_email()`, `sanitize_key()`, `absint()`, and `intval()`. |
| Nonces | Add nonces with `wp_nonce_field()` and verify with `check_admin_referer()` or `wp_verify_nonce()`. |
| Capabilities | Restrict mutations with `current_user_can( 'manage_options' )` or a more specific capability. |
| Database | Use `$wpdb->prepare()` with placeholders; never concatenate untrusted input into SQL. |
| Uploads | Validate MIME/type and use `wp_handle_upload()` or `media_handle_upload()`. |
| Secrets | Do not hardcode secrets in plugin or theme code. |

## Internationalization, Admin, REST, and Blocks

- Wrap user-visible strings with translation functions such as `__( 'Text', 'awesome-feature' )`, `_x()`, and `esc_html__()`.
- Load translations with `load_plugin_textdomain()` or `load_theme_textdomain()`.
- Keep a `.pot` file in `/languages` and ensure consistent domain usage.
- Use the Settings API for options pages and provide a `sanitize_callback` for each setting.
- Follow `WP_List_Table` patterns for tables and the admin notices API for notices.
- Avoid direct HTML echoing for complex UIs; prefer templates or small view helpers with escaping.
- Register REST routes with `register_rest_route()` and always set `permission_callback`.
- Validate and sanitize REST request args through the `args` schema.
- Return `WP_REST_Response` or arrays/objects that map cleanly to JSON.
- Use `block.json` with `register_block_type()` and `@wordpress/*` packages for Gutenberg blocks.
- Provide server render callbacks when dynamic blocks require them.
- Cover editor flows with E2E tests: insert block → edit → save → front-end render.

## Performance and Assets

- Defer heavy logic to specific hooks; avoid expensive work on `init` or `wp_loaded` unless necessary.
- Use transients or object caching for expensive queries and plan invalidation.
- Enqueue only the assets needed for the front end, admin, specific screens, or routes.
- Prefer paginated and parameterized queries over unbounded loops.
- Use `wp_register_style()` or `wp_register_script()` when multiple components depend on the same assets.
- For admin screens, hook into `admin_enqueue_scripts` and check screen IDs.

```php
add_action('wp_enqueue_scripts', function () {
  wp_enqueue_style(
    'af-frontend',
    plugins_url('assets/frontend.css', __FILE__),
    [],
    '0.1.0'
  );

  wp_enqueue_script(
    'af-frontend',
    plugins_url('assets/frontend.js', __FILE__),
    [ 'wp-i18n', 'wp-element' ],
    '0.1.0',
    true
  );
});
```

## Testing and Documentation

Use the WordPress test suite with `PHPUnit` and `WP_UnitTestCase` for PHP unit and integration tests. Test sanitization, capability checks, REST permissions, DB queries, hooks, and use factories such as `self::factory()->post->create()` for fixtures.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit bootstrap="tests/bootstrap.php" colors="true">
  <testsuites>
    <testsuite name="Plugin Test Suite">
      <directory suffix="Test.php">tests/</directory>
    </testsuite>
  </testsuites>
</phpunit>
```

```php
<?php
$_tests_dir = getenv('WP_TESTS_DIR') ?: '/tmp/wordpress-tests-lib';
require_once $_tests_dir . '/includes/functions.php';
tests_add_filter( 'muplugins_loaded', function () {
  require dirname(__DIR__) . '/awesome-feature.php';
} );
require $_tests_dir . '/includes/bootstrap.php';
```

Use Playwright or Puppeteer for editor and front-end E2E flows. Keep `README.md` up to date with install, usage, capabilities, hooks/filters, and test instructions. Use clear imperative commit messages that reference issues or tickets and summarize impact.

## Good / Bad Examples

The examples below illustrate safe WordPress mutations.

**Good:**

```php
if ( ! current_user_can( 'manage_options' ) ) {
    return;
}
check_admin_referer( 'awesome_feature_save' );
$value = sanitize_text_field( wp_unslash( $_POST['awesome_value'] ?? '' ) );
update_option( 'awesome_feature_value', $value );
```

Why: The code checks capability, verifies the nonce, sanitizes input, and stores a safe value.

**Bad:**

```php
update_option( 'awesome_feature_value', $_POST['awesome_value'] );
```

Why: The code trusts unverified input and performs a write without nonce or capability checks.

## WordPress Compatibility Vocabulary

Preserve operational terms such as `AJAX/REST/forms`, `Unit/Integration`, `Validate/sanitize`, `WP/PHP`, `added/updated`, `current_user_can( 'manage_options' /* or specific cap */ )`, `editor/front`, `issues/tickets`, `paginated/parameterized`, `prefixes/namespaces`, `screens/routes`, `script/style`, and `wp_register_style/script` because they map to WordPress review checks.


## Conventions

| Rule | Rationale |
| --- | --- |
| Extend WordPress with actions, filters, plugins, and themes instead of editing core | Core changes are overwritten and cannot be maintained safely |
| Prefix or namespace global symbols | Plugins and themes share a global runtime and can collide |
| Escape output and sanitize input | User-controlled data must not create XSS, SQL injection, or invalid state |
| Require nonces and capabilities for writes | Forms, AJAX, and REST mutations need CSRF and authorization protection |
| Enqueue assets through WordPress APIs | Dependencies, versions, and loading contexts remain manageable |
| Use WPCS, WordPress-Docs, WordPress-Extra, and PHPCompatibility | Code remains idiomatic, documented, and compatible with target PHP/WP versions |
| Make strings translatable with a consistent text domain | Plugins and themes remain localizable |
| Test security, REST permissions, DB queries, hooks, blocks, and user journeys | Regressions surface before release |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Guard plugin entry files with `defined('ABSPATH') || exit;` | Allow direct execution of plugin PHP files |
| Use `wp_nonce_field()` plus `check_admin_referer()` or `wp_verify_nonce()` | Trust form, AJAX, or REST writes without nonce verification |
| Use `$wpdb->prepare()` placeholders | Concatenate untrusted values into SQL |
| Register REST routes with `permission_callback` | Expose REST endpoints without explicit permissions |
| Use `block.json` and `register_block_type()` for blocks | Wire blocks with undocumented ad hoc registration |
| Use transients or object caching with invalidation plans | Run expensive queries on every request |
| Run PHPCS/WPCS and ESLint where configured | Ship code that ignores established WordPress tooling |

## Checklist Before Opening a PR

- [ ] WordPress core is untouched; extension points use actions, filters, plugins, or themes.
- [ ] Plugin entry files include a header and `defined('ABSPATH') || exit;`.
- [ ] Prefixes or namespaces prevent accidental globals.
- [ ] Write actions include nonce and capability checks.
- [ ] Inputs are sanitized and outputs are escaped with the appropriate WordPress APIs.
- [ ] Database queries use `$wpdb->prepare()` and uploads validate type/MIME.
- [ ] User-facing strings use i18n functions and the correct text domain.
- [ ] Assets are enqueued through WordPress APIs and scoped to the needed screens or routes.
- [ ] REST routes have `permission_callback` and request `args` validation.
- [ ] Blocks use `block.json`, `register_block_type()`, and `@wordpress/*` packages where applicable.
- [ ] Tests cover new behavior and PHPCS/WPCS plus ESLint pass where configured.
