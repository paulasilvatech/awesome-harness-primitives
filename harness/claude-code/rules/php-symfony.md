---
paths:
  - "**/*.php"
  - "**/*.yaml"
  - "**/*.yml"
  - "**/*.xml"
  - "**/*.twig"
---

<!-- Generated from harness/github-copilot/instructions/php-symfony.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Symfony conventions for project structure, configuration, dependency injection, controllers, Doctrine, Twig, forms, validation, security, assets, Messenger, and testing.

# Symfony Conventions — Framework-First Applications

These instructions apply to Symfony PHP, YAML, XML, and Twig files matched by the Symfony globs. They are authoritative for Symfony application structure, configuration, services, controllers, Doctrine, templates, forms, validation, i18n, security, assets, Messenger, and tests; repository-specific architecture, security, deployment, and coding-standard rules win when they are stricter.

## Project Structure and Configuration

Use the default Symfony directory structure with application code in `src/`, configuration in `config/`, and templates in `templates/`. Do not create bundles for application code; organize with PHP namespaces instead. Assume current stable or LTS Symfony, autowiring and autoconfiguration enabled, Doctrine ORM when persistence is needed, Twig for templating, Symfony Forms, Validator, Security, Messenger as needed, PHPUnit for tests, and attribute-based configuration where supported.

| Configuration type | Convention | Rationale |
| --- | --- | --- |
| Infrastructure values | Use environment variables and `.env` files | Deployment-specific values stay outside code |
| Application behavior | Use parameters in `config/services.yaml` | Behavior is explicit and reviewable |
| Secrets | Use Symfony Secrets | API keys and credentials stay out of VCS |
| Parameter names | Prefix with `app.` and keep names short and descriptive | Avoids collisions and unclear configuration |
| Rarely changing constants | Use PHP constants | Static domain values remain discoverable in code |

Do not use environment variables to control application behavior that belongs in parameters or code.

## Services and Dependency Injection

- Use dependency injection exclusively; prefer constructor injection.
- Use autowiring and autoconfiguration by default.
- Keep services private whenever possible.
- Avoid retrieving services with `$container->get()` in application code.
- Use YAML as the preferred service configuration format.
- Introduce interfaces when they improve decoupling or clarify a boundary, not for every class by default.

## Controllers and HTTP Boundaries

- Extend `AbstractController` where it fits project style.
- Keep controllers thin and focused on request/response glue.
- Do not put business logic in controllers.
- Use attributes for routing, caching, and security when supported.
- Inject services instead of pulling them from the container.
- Use Entity Value Resolvers when they simplify controller signatures.
- Put complex queries in repositories rather than hiding them in controllers.

## Doctrine, Twig, Forms, and Validation

| Area | Convention |
| --- | --- |
| Doctrine entities | Keep them plain PHP objects with PHP attribute mapping |
| Repositories | Use for querying; avoid business logic there |
| Migrations | Use migrations for every schema change |
| Twig names | Use `snake_case` for template names, directories, and variables |
| Twig fragments | Prefix fragments with an underscore |
| Twig output | Escape by default and avoid `|raw` unless trusted and sanitized |
| Forms | Define forms as PHP classes, not directly in controllers |
| Buttons | Put form buttons in templates; define submit buttons in controllers only when multiple submits require it |
| Validation | Define constraints on the underlying object and validate at boundaries |
| Reusable validation | Prefer object-level validation over form-only validation |

Use one controller action to render and process each form when the flow is a standard Symfony form submission.

## Internationalization, Security, Assets, and Messenger

- Use XLIFF translation files and translation keys instead of literal content strings.
- Make translation keys descriptive by purpose, not by template location.
- Prefer a single firewall unless the app genuinely has multiple security systems.
- Use the auto password hasher.
- Use voters for complex authorization logic.
- Avoid complex security expressions in attributes.
- Use AssetMapper for web assets and avoid unnecessary frontend build complexity unless the application requires it.
- Use Symfony Messenger for async and background tasks, keep message handlers small, and configure failure transports.

## Testing and Quality

- Write functional tests with `WebTestCase`.
- Add smoke tests so public URLs respond successfully.
- Hard-code URLs in functional tests instead of generating routes.
- Use unit tests for isolated logic.
- Add more specific tests incrementally as behavior evolves.
- Prefer clarity over abstraction, Symfony conventions over custom patterns, explicit readable configuration, and measured optimization over premature tuning.
- Use Symfony Demo as a reference implementation for idiomatic choices.

## Environment Terminology

Use environment variables for `infrastructure-related` values and `.env` files for `environment-specific` values. Keep application behavior in Symfony parameters instead of conflating deployment infrastructure with business configuration.

## Good / Bad Examples

The examples below illustrate controller thinness and dependency injection.

**Good:**

```php
#[Route('/orders/{id}', name: 'order_show')]
public function show(Order $order, OrderPresenter $presenter): Response
{
    return $this->render('order/show.html.twig', [
        'order' => $presenter->present($order),
    ]);
}
```

Why: The controller uses attributes, an Entity Value Resolver, injected services, and delegates presentation behavior.

**Bad:**

```php
public function show(int $id): Response
{
    $order = $this->container->get('doctrine')->getRepository(Order::class)->find($id);
    // business logic here
}
```

Why: The controller pulls services from the container, hides queries and business logic in the HTTP layer, and weakens testability.

## Conventions

| Rule | Rationale |
| --- | --- |
| Use default Symfony directories and namespaces instead of application bundles | Symfony conventions reduce custom framework code |
| Separate environment infrastructure, application parameters, and secrets | Configuration remains deployable without leaking credentials |
| Prefer constructor injection with private autowired services | Dependencies stay explicit and testable |
| Keep controllers, repositories, templates, forms, and validators focused on their layer | Logic stays maintainable and reusable |
| Escape Twig output and avoid unsanitized `|raw` | Prevents cross-site scripting |
| Use voters, Messenger, AssetMapper, XLIFF, and PHPUnit where their Symfony component fits | Framework-supported tools stay integrated |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Put application code in `src/` and configuration in `config/` | Create bundles for normal application code |
| Configure application behavior with `app.` parameters | Drive business behavior through environment variables |
| Store secrets with Symfony Secrets | Commit API keys or credentials |
| Define forms as PHP classes | Build complex forms directly in controllers |
| Use migrations for schema changes | Change schemas manually without migration files |
| Use `WebTestCase` and smoke tests for public URLs | Rely only on unit tests for HTTP behavior |

## Checklist Before Opening a PR

- [ ] Code follows default Symfony structure and does not introduce application bundles.
- [ ] Infrastructure config, app parameters, constants, and secrets are stored in the correct place.
- [ ] Services use constructor injection, autowiring, autoconfiguration, and private visibility where possible.
- [ ] Controllers stay thin and use attributes, injected services, and explicit repository queries where appropriate.
- [ ] Doctrine entities, repositories, migrations, Twig templates, forms, and validators follow their layer conventions.
- [ ] Security uses appropriate firewalls, auto password hasher, voters, and simple attributes.
- [ ] Messenger handlers are small and failure transports are configured for async work.
- [ ] Functional, smoke, and unit tests cover the changed behavior.
