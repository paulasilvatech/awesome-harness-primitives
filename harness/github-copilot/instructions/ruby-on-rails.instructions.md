---
applyTo: "**/*.rb"
description: "Enforces Ruby on Rails conventions for models, controllers, routing, persistence, APIs, frontend integration, jobs, testing, configuration, and maintainability."
---

# Ruby on Rails Conventions — Application Code Discipline

These instructions apply to Ruby files matched by `**/*.rb` in Rails applications. They are authoritative for Rails structure, naming, controllers, models, services, persistence, APIs, background jobs, tests, and maintainable Ruby style; repository-specific architecture, security, and test framework rules win when they define stricter conventions.

## Ruby Style and Application Structure

- Follow the RuboCop Style Guide and the formatter already used by the project, such as `rubocop`, `standardrb`, or `rufo`.
- Use `snake_case` for variables and methods, and `CamelCase` for classes and modules.
- Keep methods short and focused with early returns, guard clauses, and private methods.
- Prefer meaningful names over short generic names; comment complex paths with YARD or RDoc only when the code needs explanation.
- Apply the Single Responsibility Principle and prefer composition over inheritance.
- Use Rails generators such as `rails generate` to scaffold models, controllers, and migrations consistently.
- Construct file paths with `Rails.root.join(...)` instead of hardcoding separators.

## Controllers, Routing, and Authorization

- Follow RESTful routing with `resources` and conventional controller actions.
- Keep controllers thin; put business logic in models, service objects, command/query objects, or other focused collaborators.
- Use `before_action` callbacks sparingly for loading and authorization, not business logic.
- Use strong parameters to whitelist attributes securely.
- Define authorization policies in `app/policies` when access rules require reusable policy logic.
- Use namespaced routes such as `/api/v1/` for API versioning.

## Models, Persistence, and Queries

| Concern | Convention |
| --- | --- |
| Associations | Use `class_name` and `foreign_key` when relationships are not conventional |
| Validation | Prefer enums, typed attributes, and validations that make model state clear |
| Migrations | Keep migrations database-agnostic and avoid raw SQL when possible |
| Constraints | Add `null: false`, `unique: true`, indexes for foreign keys, and indexes for frequently queried columns at the database level |
| Large datasets | Use `find_each` instead of loading entire relations |
| Query reuse | Put scoped queries in models or query objects under `app/queries` |
| Caching | Use `Rails.cache` for expensive computations or frequently accessed data |

Keep secrets and configuration out of source by using `Rails.application.credentials` or environment variables. Do not rely only on model validations for uniqueness or nullability when the database can enforce the invariant.

## App Directories and Boundaries

Use conventional application directories for focused responsibilities:

| Directory | Responsibility |
| --- | --- |
| `app/services` | Service objects that encapsulate reusable business logic |
| `app/forms` | Form objects that manage validation and submission flows |
| `app/serializers` | JSON serializers such as `ActiveModel::Serializer` or `fast_jsonapi` |
| `app/policies` | Authorization policies |
| `app/graphql` | GraphQL schemas, queries, and mutations |
| `app/validators` | Custom validators |
| `app/queries` | Complex ActiveRecord query objects |
| `app/types` | Custom data types and coercion logic for ActiveModel |

Use partials or view components to reduce duplication and keep views focused on presentation.

## API Development

- Return proper HTTP status codes such as `200 OK`, `201 Created`, and `422 Unprocessable Entity`.
- Serialize responses with `ActiveModel::Serializer`, `fast_jsonapi`, custom serializers, or presenters so internal models do not leak into response contracts.
- Paginate large endpoints with `kaminari` or `pagy`.
- Avoid N+1 queries with `includes` when eager loading related data.
- Rate limit sensitive endpoints with middleware or gems such as `rack-attack`.
- Return structured JSON errors with codes, messages, and details.
- Log request and response metadata for debugging, observability, and auditing without exposing sensitive data.
- Document endpoints with OpenAPI (Swagger), `rswag`, or `apipie-rails`.
- Use `rack-cors` only when cross-origin access is required and configured deliberately.

## Frontend and Assets

- Use `app/javascript` for JavaScript packs, modules, and frontend logic in Rails 6+ projects using Webpacker or esbuild.
- Organize JavaScript by components or domains, not by file type alone.
- Use Hotwire, Turbo, and Stimulus for Rails-native interactivity when they fit the app.
- Organize styles with SCSS modules, Tailwind, or BEM conventions under `app/assets/stylesheets`.
- Use semantic HTML and accessibility practices; avoid inline JavaScript and inline styles.
- Use `data-*` attributes to bridge Rails-rendered HTML and Stimulus behavior.
- Optimize assets through the asset pipeline or bundlers, use environment-specific asset loading, and improve time-to-first-paint (`TTFP`) with lazy loading, Turbo Frames, and deferred JavaScript where appropriate.

## Background Jobs, Debugging, and Commands

Use ActiveJob for non-blocking work such as sending emails, syncing with APIs, and other slow operations. Debug with `byebug`, `pry`, or logger utilities instead of `puts`.

| Command | Purpose |
| --- | --- |
| `rails db:migrate` | Apply migrations |
| `rails db:seed` | Populate initial data |
| `rails db:rollback` | Revert the last migration |
| `rails console` | Inspect the app in a REPL |
| `rails server` | Start the development server |
| `rails test` | Run the test suite |
| `rails routes` | List routes |
| `rails assets:precompile` | Compile production assets |

## Testing

- Write isolated unit tests for models, services, and helpers using `test/models` for Minitest or `spec/models` for RSpec.
- Cover end-to-end logic with request, system, feature, or integration tests using tools such as Capybara, Cypress, or Playwright.
- Use fixtures in Minitest or `FactoryBot` in RSpec to set up test data.
- Use `before` in RSpec or `setup` in Minitest for common state.
- Stub external APIs with `WebMock`, `VCR`, or `stub_request`.
- Avoid `sleep`; use `perform_enqueued_jobs`, `ActiveJob::TestHelper`, or `have_enqueued_job` matchers.
- Keep database state clean with `rails test:prepare`, `DatabaseCleaner`, or `transactional_fixtures`.
- Use `SimpleCov` when coverage tracking is part of the project, and keep tests fast, reliable, and not dependent on timestamps, random order, or randomized data unless controlled.

## Rails Idioms and Test Labels

Use Rails predicates such as `.present?`, `.blank?`, and `.any?` instead of manual `nil/empty` checks. Use `unless` for negative conditions only when it stays clear, and avoid `unless` with `else`. Preserve naming language for `variables/methods` and `classes/modules.` while keeping Ruby style idiomatic. Recognize `request/response` API metadata, `CORS`, `rack-cors`, `real-time` Hotwire behavior, `.scss` assets, `system tests`, `feature specs`, `test/controllers`, `spec/requests`, and RSpec tags such as `:model`, `:request`, and `:feature`.

## Good / Bad Examples

The examples below illustrate thin controllers and service boundaries.

**Good:**

```ruby
class OrdersController < ApplicationController
  def create
    order = Orders::Create.call(order_params)
    render json: OrderSerializer.new(order), status: :created
  end

  private

  def order_params
    params.require(:order).permit(:customer_id, :sku)
  end
end
```

Why: The controller validates input boundaries, delegates business work, serializes output, and returns an explicit status.

**Bad:**

```ruby
class OrdersController < ApplicationController
  def create
    puts params.inspect
    Order.create!(params[:order])
  end
end
```

Why: The action logs unsafely, skips strong parameters, embeds persistence directly, and returns no structured response.

## Conventions

| Rule | Rationale |
| --- | --- |
| Follow RuboCop-compatible style and Rails naming | Consistent Ruby is easier to review and maintain |
| Keep controllers thin with strong parameters and RESTful routes | HTTP glue stays separate from business behavior |
| Put reusable business, form, query, policy, serializer, GraphQL, validator, and type logic in the appropriate `app/` directory | Boundaries stay discoverable |
| Enforce indexes, nullability, and uniqueness at the database level | Database constraints protect data beyond model validation |
| Use explicit serializers, status codes, pagination, rate limiting, and structured errors for APIs | Clients receive stable contracts and predictable failures |
| Test models, services, APIs, jobs, and user flows with isolated dependencies | Regressions are caught without slow or brittle tests |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use `find_each` for large relation iteration | Load large datasets into memory unnecessarily |
| Use `includes` to prevent N+1 queries | Hide query explosions behind view rendering |
| Use `Rails.cache` for expensive stable computations | Recompute the same costly value on every request |
| Use `Rails.application.credentials` or ENV variables for secrets | Commit credentials or API keys |
| Use `byebug`, `pry`, or logger utilities | Leave `puts` debugging in application code |
| Use ActiveJob for slow email or API work | Block request threads with non-critical external calls |

## Checklist Before Opening a PR

- [ ] Ruby style matches the project's RuboCop, `standardrb`, or `rufo` setup.
- [ ] Controllers are thin, RESTful, authorized, and use strong parameters.
- [ ] Business logic, forms, queries, policies, serializers, GraphQL code, validators, and custom types live in the appropriate `app/` directories.
- [ ] Migrations include indexes, foreign-key indexes, `null: false`, and uniqueness constraints where needed.
- [ ] API endpoints return explicit statuses, serialized responses, structured errors, and no sensitive data.
- [ ] Frontend code uses Rails asset and Hotwire conventions when present.
- [ ] Background work uses ActiveJob when requests should not block.
- [ ] Tests cover unit, request/system, jobs, and integrations without external API calls or brittle sleeps.
